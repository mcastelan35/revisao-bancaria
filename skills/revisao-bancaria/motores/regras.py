"""
regras.py — motor de regras determinístico da skill revisao-bancaria
Versão 1.0.0 · 2026-10-26

O agente não lê o `dados/regras-bancarias.json` inteiro (~30 mil tokens): recebe só as regras
aplicáveis ao caso, com corte temporal, regime, status e validade das pendências já resolvidos.

    python3 revisao.py regras --tipo consumo_pf --regime consumerista --data-contrato 2019-05-02
    from motores import regras; regras.avaliar("consumo_pf", "consumerista", "2019-05-02")

Para cada regra, na ordem do JSON, o PRIMEIRO passo que exclui decide o destino
(`aplicaveis`, `confirmar` — aplicável, mas falta dado ou decisão — ou `nao_aplicaveis`):

  0. `categorias` informadas e a categoria da regra fora delas → ignorada (só contada).
  1. `status: superada` → não aplicável.
  2. Regra em `regras_desligadas` do tipo → não aplicável.
  3. Tipo: tags de `tipo_contrato` expandidas pelos `grupos`; `empresarial_pj` em regime
     consumerista (CDC mitigado) também casa as regras `consumo_pf`. Sem casamento: repetição
     de indébito consumerista de outro tipo → `confirmar`; o resto → não aplicável.
  4. Regime: bloco `regime` com `aplica: false` → não aplicável; regra só `consumo_pf` em
     regime civil-empresarial → não aplicável; `empresarial_pj` civil-empresarial com regra fora
     de `regras_sem_cdc` e sem bloco `regime` → `confirmar`.
  5. Corte temporal pela `base` do marco (contrato, pagamento, operacao ou
     contrato_ou_consolidacao). Posições: anterior = data < marco; anterior_ou_igual = data <=
     marco; posterior = data > marco.

Nada é presumido: dado ausente vira `confirmar` com o motivo, nunca aplicação silenciosa.
Executar `python3 revisao.py autoteste --modulo regras` roda a suíte de autoteste embutida.
"""

from __future__ import annotations

import copy
import json
import re
import unicodedata
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

from .comum import arredondar, rodar_autoteste, saida_utf8

CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "dados" / "regras-bancarias.json"

REGIMES = ("consumerista", "civil_empresarial")
FORMATOS = ("resumo", "padrao", "completo")
POSICOES = ("anterior", "anterior_ou_igual", "posterior")
BASES = ("contrato", "pagamento", "operacao", "contrato_ou_consolidacao")
STATUS_NAO_CONCLUSIVOS = ("suspensa", "sem_precedente_consolidado")
#: Chaves de `teste` que o agente recebe; as demais (descricao, nomes_equivalentes, requer_motor)
#: ficam na regra integral (`regra()`).
CHAVES_TESTE = ("logica", "campos_necessarios", "requer_consulta_bacen", "parametros",
                "usar_deteccao_padroes", "requer_sub_skill")

NOTA_PAGAMENTO = ("corte por pagamento: reparte a apuração (cada pagamento antes ou depois do "
                  "marco), não exclui a regra")
NOTA_OPERACAO = "corte pela data da operação de rotativo/parcelamento, não pela data do contrato"

# ─────────────────────────────────────────────────────────────────────
# 1. DADOS
# ─────────────────────────────────────────────────────────────────────

_CACHE: dict[str, tuple[tuple[int, int], dict]] = {}


def carregar_dados(caminho=None) -> dict:
    """Lê o JSON de regras (UTF-8). Cache por caminho: a mesma instância volta enquanto o arquivo
    não mudar (tamanho e data); quem for alterar o conteúdo deve copiá-lo antes."""
    arq = Path(caminho) if caminho else CAMINHO_PADRAO
    chave = str(arq.resolve())
    estado = arq.stat()
    assinatura = (estado.st_mtime_ns, estado.st_size)
    guardado = _CACHE.get(chave)
    if guardado and guardado[0] == assinatura:
        return guardado[1]
    dados = json.loads(arq.read_text(encoding="utf-8"))
    _CACHE[chave] = (assinatura, dados)
    return dados


def _dados(dados) -> dict:
    return carregar_dados() if dados is None else dados


def _data(valor, nome: str = "data") -> date | None:
    """Aceita date, datetime ou 'AAAA-MM-DD'; vazio vira None."""
    if valor is None:
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        texto = valor.strip()
        if not texto:
            return None
        try:
            return date.fromisoformat(texto)
        except ValueError:
            pass
    raise ValueError(f"{nome} inválida: {valor!r} (use AAAA-MM-DD)")


def _br(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def _iso(d: date | None) -> str | None:
    return d.isoformat() if d else None


def tipo_contrato(id_tipo: str, dados: dict | None = None) -> dict:
    """O tipo de contrato `id_tipo`; ValueError listando os válidos se não existir."""
    dados = _dados(dados)
    tipos = dados["tipos_contrato"]["tipos"]
    for t in tipos:
        if t["id"] == id_tipo:
            return t
    raise ValueError(f"tipo de contrato inválido: {id_tipo!r}. Tipos válidos: "
                     + ", ".join(t["id"] for t in tipos))


def _regime(regime) -> str:
    if isinstance(regime, str) and regime.strip() in (*REGIMES, "civil-empresarial"):
        return regime.strip().replace("-", "_")
    raise ValueError(f"regime inválido: {regime!r}. Use 'consumerista' ou 'civil_empresarial' "
                     "(aceita o alias 'civil-empresarial')")


def _categorias(categorias) -> list[str] | None:
    if categorias is None:
        return None
    if isinstance(categorias, str):
        categorias = categorias.split(",")
    return [c.strip() for c in categorias if str(c).strip()]


# ─────────────────────────────────────────────────────────────────────
# 2. DATAS E MARCOS
# ─────────────────────────────────────────────────────────────────────

def relacao(data, marco_data) -> str:
    """'anterior' (data < marco), 'igual' ou 'posterior' (data > marco)."""
    d, m = _data(data, "data"), _data(marco_data, "data do marco")
    if d is None or m is None:
        raise ValueError("relacao() exige as duas datas")
    return "anterior" if d < m else ("igual" if d == m else "posterior")


def posicao_atende(posicao: str, rel: str) -> bool:
    """A posição que a regra exige (`anterior`, `anterior_ou_igual`, `posterior`) é atendida
    pela relação `rel` entre a data do caso e o marco?"""
    if posicao == "anterior":
        return rel == "anterior"
    if posicao == "anterior_ou_igual":
        return rel in ("anterior", "igual")
    if posicao == "posterior":
        return rel == "posterior"
    raise ValueError(f"posição inválida: {posicao!r}. Use uma de {', '.join(POSICOES)}")


def resolver_marcos(data_contrato=None, data_consolidacao=None, dados: dict | None = None) -> dict:
    """Posição do contrato (e da consolidação, no MT10) em cada marco temporal, com a `base` do
    corte. Data ausente → relação `None`."""
    dados = _dados(dados)
    dc = _data(data_contrato, "data_contrato")
    dk = _data(data_consolidacao, "data_consolidacao")
    saida = {}
    for m in dados["marcos_temporais"]["marcos"]:
        md = date.fromisoformat(m["data"])
        item = {"data": m["data"], "base": m["base"], "evento": m["evento"],
                "contrato": relacao(dc, md) if dc else None}
        if m["base"] == "contrato_ou_consolidacao":
            item["consolidacao"] = relacao(dk, md) if dk else None
        elif m["base"] == "pagamento":
            item["nota"] = NOTA_PAGAMENTO
        elif m["base"] == "operacao":
            item["nota"] = NOTA_OPERACAO
        saida[m["id"]] = item
    return saida


# ─────────────────────────────────────────────────────────────────────
# 3. APLICABILIDADE
# ─────────────────────────────────────────────────────────────────────

def _grupos(dados: dict) -> dict[str, list[str]]:
    return {k: v for k, v in dados["tipos_contrato"].get("grupos", {}).items() if isinstance(v, list)}


def _expandir(tags: list[str], grupos: dict[str, list[str]]) -> set[str]:
    expandido: set[str] = set()
    for tag in tags:
        expandido.update(grupos[tag] if tag in grupos else [tag])
    return expandido


def _decidir(r: dict, tipo: dict, regime: str, dc: date | None, dk: date | None,
             grupos: dict, marcos: dict) -> tuple[str, str | None, dict | None]:
    """(destino, motivo, corte). Destino: 'aplicavel' | 'confirmar' | 'nao_aplicavel'."""
    tid = tipo["id"]
    rid = r["id"]
    # 1 — superada
    if r.get("status") == "superada":
        return "nao_aplicavel", "regra superada", None
    # 2 — desligada no tipo
    if rid in tipo.get("regras_desligadas", []):
        return "nao_aplicavel", f"desligada no tipo {tid} (regras_desligadas)", None
    # 3 — casamento de tipo
    tags = list(r.get("tipo_contrato", []))
    expandido = _expandir(tags, grupos)
    casa = tid in expandido or (tid == "empresarial_pj" and regime == "consumerista"
                                and "consumo_pf" in expandido)
    if not casa:
        if (r.get("categoria") == "repeticao_indebito" and regime == "consumerista"
                and tid not in ("consumo_pf", "empresarial_pj")):
            return ("confirmar", "repetição segue o regime (regra de conduta 9): confirmar a "
                    f"relação de consumo no tipo {tid}", None)
        return "nao_aplicavel", f"tipo_contrato {', '.join(tags)} não inclui {tid}", None
    # 4 — regime
    bloco_regime = r.get("regime")
    if bloco_regime and (bloco_regime.get(regime) or {}).get("aplica") is False:
        return "nao_aplicavel", f"não se aplica no regime {regime}", None
    if tid == "consumo_pf" and regime == "civil_empresarial" and tags == ["consumo_pf"]:
        return "nao_aplicavel", "regra consumerista — regime civil-empresarial", None
    if (tid == "empresarial_pj" and regime == "civil_empresarial"
            and rid not in tipo.get("regras_sem_cdc", []) and not bloco_regime):
        return ("confirmar", "fora de regras_sem_cdc: confirmar que a tese não depende do CDC "
                "(regra de conduta 18)", None)
    # 5 — corte temporal
    corte_regra = r.get("corte_temporal") or {}
    mk = corte_regra.get("marco")
    if not mk:
        return "aplicavel", None, None
    if mk not in marcos:
        raise KeyError(f"marco {mk} citado pela regra {rid} não existe em marcos_temporais")
    marco = marcos[mk]
    md = date.fromisoformat(marco["data"])
    br = _br(md)
    posicao = corte_regra.get("posicao")
    base = marco["base"]
    corte = {"marco": mk, "data": marco["data"], "base": base, "posicao": posicao}
    if base == "contrato":
        if dc is None:
            return "confirmar", f"data do contrato ausente — corte {mk} ({br})", None
        rel = relacao(dc, md)
        if not posicao_atende(posicao, rel):
            return ("nao_aplicavel", f"{mk} ({br}): contrato {rel} ao marco — a regra exige "
                    f"{posicao}", None)
        return "aplicavel", None, None
    if base in ("pagamento", "operacao"):
        return "aplicavel", None, corte
    if base == "contrato_ou_consolidacao":
        if dc is None or dk is None:
            return "confirmar", f"datar contrato e consolidação ({mk})", None
        ok_contrato = posicao_atende(posicao, relacao(dc, md))
        ok_consolidacao = posicao_atende(posicao, relacao(dk, md))
        if ok_contrato and ok_consolidacao:
            corte["leitura"] = "contrato e consolidação atendem ao marco"
        elif not ok_contrato and not ok_consolidacao:
            return "nao_aplicavel", f"{mk}: contrato e consolidação fora do marco", None
        else:
            quem = "o contrato" if ok_contrato else "a consolidação"
            corte["leitura"] = (f"só {quem} atende ao marco — critério temporal divergente "
                                "(ver pendências)")
        return "aplicavel", None, corte
    raise ValueError(f"base de marco inválida: {base!r} ({mk})")


def _marco_da_leitura(regime_por_marco: dict) -> str | None:
    """'MT04' a partir das chaves 'anterior_a_MT04' / 'posterior_a_MT04'."""
    for chave in regime_por_marco:
        achado = re.fullmatch(r"(?:anterior|posterior)_a_(MT\d+)", chave)
        if achado:
            return achado.group(1)
    return None


def _item(r: dict, regime: str, dc: date | None, hoje: date, dados: dict, marcos: dict,
          formato: str, motivo: str | None, corte: dict | None) -> dict:
    """Monta o item de uma regra aplicável ou a confirmar, no formato pedido."""
    conclusiva = r.get("status") not in STATUS_NAO_CONCLUSIVOS
    exige_pesquisa = not conclusiva
    tier = r.get("tier")
    consequencia = r.get("consequencia")
    alerta = r.get("alerta") or None
    extras: dict = {}

    resolvido = (r.get("regime") or {}).get(regime)
    if resolvido:
        tier = resolvido.get("tier", tier)
        consequencia = resolvido.get("consequencia", consequencia)

    por_marco = r.get("regime_por_marco")
    mt = _marco_da_leitura(por_marco) if por_marco else None
    if mt:
        if dc is None:
            extras["leitura_por_marco_pendente"] = True
        else:
            rel = relacao(dc, marcos[mt]["data"])
            leitura = por_marco.get(f"anterior_a_{mt}" if rel == "anterior" else f"posterior_a_{mt}")
            if leitura:
                consequencia = leitura.get("consequencia", consequencia)
                if "fundamentacao" in leitura:
                    extras["fundamentacao_marco"] = leitura["fundamentacao"]
                if leitura.get("alerta"):
                    alerta = f"{alerta} {leitura['alerta']}" if alerta else leitura["alerta"]
                if leitura.get("exige_pesquisa") is True:
                    exige_pesquisa = True

    pendencias_json = dados.get("pendencias_jurisprudenciais", {})
    validade = pendencias_json.get("validade_dias", 90)
    modelo_alerta = pendencias_json.get("alerta_vencido", "")
    pendencias, alertas_vencidos = [], []
    for tema in pendencias_json.get("temas", []):
        if r["id"] not in tema.get("regras_afetadas", []):
            continue
        verificado = date.fromisoformat(tema["verificado_em"])
        vencida = (hoje - verificado).days > validade
        pendencias.append({"tema": tema["tema"], "status": tema["status"],
                           "verificado_em": tema["verificado_em"], "vencida": vencida})
        if vencida:
            alertas_vencidos.append(modelo_alerta.replace("{tema}", tema["tema"])
                                    .replace("{verificado_em}", _br(verificado)))

    item = {"id": r["id"], "categoria": r["categoria"], "nome": r["nome"], "status": r["status"],
            "tier": tier, "resultado_se_positivo": r["resultado_se_positivo"],
            "consequencia": consequencia,
            "teste": {k: r["teste"][k] for k in CHAVES_TESTE if k in r["teste"]}}
    if alerta:
        item["alerta"] = alerta
    item.update(conclusiva=conclusiva, exige_pesquisa=exige_pesquisa, pendencias=pendencias,
                alertas_vencidos=alertas_vencidos)
    if corte:
        item["corte"] = corte
    if motivo:
        item["motivo"] = motivo
    termos = (r.get("padroes_deteccao") or {}).get("termos_suspeitos")
    if termos:
        item["termos_suspeitos"] = termos
    for chave in ("implementacao", "resultado_se_sem_conta_grafica"):
        if chave in r:
            item[chave] = r[chave]
    item.update(extras)

    if formato == "resumo":
        enxuto = {k: item[k] for k in ("id", "categoria", "nome", "tier", "status", "conclusiva")}
        for chave in ("corte", "motivo"):
            if chave in item:
                enxuto[chave] = item[chave]
        if alertas_vencidos:
            enxuto["alertas_vencidos"] = alertas_vencidos
        return copy.deepcopy(enxuto)
    if formato == "completo":
        item["descricao"] = r["descricao"]
        item["fundamentacao"] = r["fundamentacao"]
        for chave in ("observacao_metodologica", "regime", "regime_por_marco"):
            if chave in r:
                item[chave] = r[chave]
    return copy.deepcopy(item)


def avaliar(tipo: str, regime: str, data_contrato=None, *, data_consolidacao=None,
            categorias=None, hoje=None, formato: str = "padrao", dados: dict | None = None) -> dict:
    """Regras aplicáveis ao caso (ver o passo a passo no cabeçalho do módulo).

    tipo       id de `tipos_contrato.tipos` (ValueError lista os válidos)
    regime     'consumerista' | 'civil_empresarial' (aceita 'civil-empresarial')
    datas      date ou 'AAAA-MM-DD'; ausente → regras com corte pela data voltam em `confirmar`
    categorias só as regras dessas categorias entram (as outras são apenas contadas)
    hoje       data da análise, para validar as pendências jurisprudenciais (padrão: hoje)
    formato    'resumo' | 'padrao' | 'completo'
    """
    dados = _dados(dados)
    tipo_obj = tipo_contrato(tipo, dados)
    regime = _regime(regime)
    if formato not in FORMATOS:
        raise ValueError(f"formato inválido: {formato!r}. Use um de {', '.join(FORMATOS)}")
    dc = _data(data_contrato, "data_contrato")
    dk = _data(data_consolidacao, "data_consolidacao")
    hoje_d = _data(hoje, "hoje") or date.today()
    cats = _categorias(categorias)

    grupos = _grupos(dados)
    marcos = {m["id"]: m for m in dados["marcos_temporais"]["marcos"]}
    aplicaveis, confirmar, nao_aplicaveis = [], [], []
    nao_conclusivas, com_alerta_vencido = [], []
    omitidas = 0
    for r in dados["regras"]:
        if cats is not None and r["categoria"] not in cats:
            omitidas += 1
            continue
        destino, motivo, corte = _decidir(r, tipo_obj, regime, dc, dk, grupos, marcos)
        if destino == "nao_aplicavel":
            nao_aplicaveis.append({"id": r["id"], "nome": r["nome"], "motivo": motivo})
            continue
        item = _item(r, regime, dc, hoje_d, dados, marcos, formato, motivo, corte)
        (aplicaveis if destino == "aplicavel" else confirmar).append(item)
        if r.get("status") in STATUS_NAO_CONCLUSIVOS:
            nao_conclusivas.append(r["id"])
        if item.get("alertas_vencidos"):
            com_alerta_vencido.append(r["id"])

    tipo_saida = {k: copy.deepcopy(tipo_obj[k]) for k in
                  ("id", "nome", "cdc_aplicavel", "regras_desligadas",
                   "campos_extras_obrigatorios", "gate_obrigatorio") if k in tipo_obj}
    return {
        "versao_regras": dados.get("versao"),
        "hoje": hoje_d.isoformat(),
        "entrada": {"tipo": tipo, "regime": regime, "data_contrato": _iso(dc),
                    "data_consolidacao": _iso(dk), "categorias": cats},
        "tipo": tipo_saida,
        "marcos": resolver_marcos(dc, dk, dados),
        "aplicaveis": aplicaveis,
        "confirmar": confirmar,
        "nao_aplicaveis": nao_aplicaveis,
        "resumo": {"aplicaveis": len(aplicaveis), "confirmar": len(confirmar),
                   "nao_aplicaveis": len(nao_aplicaveis), "omitidas_por_categoria": omitidas,
                   "nao_conclusivas": nao_conclusivas, "com_alerta_vencido": com_alerta_vencido},
    }


# ─────────────────────────────────────────────────────────────────────
# 4. CONSULTAS
# ─────────────────────────────────────────────────────────────────────

def regra(id, dados: dict | None = None) -> dict:
    """A regra integral (cópia). Id inexistente → KeyError."""
    dados = _dados(dados)
    alvo = str(id).strip().upper()
    for r in dados["regras"]:
        if r["id"].upper() == alvo:
            return copy.deepcopy(r)
    ids = [r["id"] for r in dados["regras"]]
    raise KeyError(f"regra {id!r} não existe (válidas: {ids[0]} a {ids[-1]})" if ids
                   else f"regra {id!r} não existe")


def sumula(numero, dados: dict | None = None) -> dict:
    """A súmula (número e texto integral). Número fora do acervo → KeyError."""
    dados = _dados(dados)
    try:
        n = int(str(numero).strip())
    except ValueError:
        raise ValueError(f"número de súmula inválido: {numero!r}") from None
    for s in dados["sumulas_consolidadas"]["sumulas"]:
        if s["numero"] == n:
            return copy.deepcopy(s)
    raise KeyError(f"súmula {n} não consta de sumulas_consolidadas — fora do acervo do plugin: "
                   "remeter a pesquisa-jurisprudencial-jusia")


def _sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn").casefold()


def series(modalidade: str | None = None, buscar: str | None = None,
           dados: dict | None = None) -> list[dict]:
    """Mapeamento modalidade → série SGS/BACEN. Sem filtros, o mapeamento inteiro;
    `modalidade` é igualdade exata; `buscar` é substring sem acento e sem caixa em
    `modalidade` + `nome`."""
    dados = _dados(dados)
    achadas = list(dados["series_bacen_por_modalidade"]["mapeamento"])
    if modalidade is not None:
        achadas = [s for s in achadas if s["modalidade"] == modalidade]
    if buscar is not None:
        consulta = _sem_acento(buscar)
        achadas = [s for s in achadas if consulta in _sem_acento(f"{s['modalidade']} {s['nome']}")]
    return copy.deepcopy(achadas)


def classificar_razao(contratada_am, media_am, dados: dict | None = None) -> dict:
    """Razão taxa contratada / taxa média BACEN, ambas em % a.m. (pontos percentuais, 2.99), em
    aritmética decimal, com os limiares da R15 (`teste.parametros`): < zona cinzenta → `licita`;
    >= zona cinzenta e < forte → `zona_cinzenta`; >= forte → `ilicita`."""
    dados = _dados(dados)
    c, m = Decimal(str(contratada_am)), Decimal(str(media_am))
    if m <= 0:
        raise ValueError(f"media_am deve ser maior que zero (taxa média BACEN em % a.m.): {media_am!r}")
    if c < 0:
        raise ValueError(f"contratada_am não pode ser negativa: {contratada_am!r}")
    parametros = regra("R15", dados)["teste"]["parametros"]
    zona = Decimal(str(parametros["limiar_zona_cinzenta"]))
    forte = Decimal(str(parametros["limiar_forte"]))
    razao = c / m
    limite_zona, limite_forte = m * zona, m * forte      # comparação exata, sem dividir
    if c < limite_zona:
        classificacao, rotulo = "licita", "dentro da faixa de mercado"
    elif c < limite_forte:
        classificacao, rotulo = "zona_cinzenta", "zona de abusividade"
    else:
        classificacao, rotulo = "ilicita", "fortemente abusiva"
    return {
        "razao": arredondar(razao, 4),
        "razao_txt": f"{arredondar(razao, 2):.2f}".replace(".", ",") + "x",
        "classificacao": classificacao,
        "rotulo": rotulo,
        "limiares_am": {"zona_cinzenta": arredondar(limite_zona, 4),
                        "forte": arredondar(limite_forte, 4)},
        "contratada_am": float(c),
        "media_am": float(m),
    }


# ─────────────────────────────────────────────────────────────────────
# 5. INTEGRIDADE DO JSON
# ─────────────────────────────────────────────────────────────────────

def validar_dados(dados: dict | None = None) -> list[str]:
    """Problemas de integridade do JSON de regras (lista vazia = íntegro): grupos derivados dos
    tipos; tags de `tipo_contrato` que são tipo ou grupo; marcos, posições e bases válidos;
    `regras_afetadas` derivado do corte das regras; regras citadas existentes; ids únicos."""
    dados = _dados(dados)
    problemas: list[str] = []
    regras = dados.get("regras", [])
    tipos = dados.get("tipos_contrato", {}).get("tipos", [])
    marcos = dados.get("marcos_temporais", {}).get("marcos", [])
    ids_regra = [r.get("id") for r in regras]
    ids_tipo = [t.get("id") for t in tipos]
    ids_marco = [m.get("id") for m in marcos]

    for rotulo, ids in (("regra", ids_regra), ("tipo", ids_tipo), ("marco", ids_marco)):
        for repetido in sorted({i for i in ids if ids.count(i) > 1}, key=str):
            problemas.append(f"id de {rotulo} duplicado: {repetido}")
    existentes = set(ids_regra)

    grupos = dados.get("tipos_contrato", {}).get("grupos", {})
    derivados = {
        "todos": ids_tipo,
        "todos_sfn": [t.get("id") for t in tipos if t.get("credor_sfn", True)],
        "todos_sem_lei_especifica": [t.get("id") for t in tipos if not t.get("legislacao_especifica")],
    }
    for nome, esperado in derivados.items():
        if grupos.get(nome) != esperado:
            problemas.append(f"tipos_contrato.grupos.{nome} {grupos.get(nome)} difere do derivado "
                             f"dos tipos {esperado}")
    validos = set(ids_tipo) | set(derivados)

    por_marco: dict[str, set[str]] = {}
    for r in regras:
        rid = r.get("id")
        for tag in r.get("tipo_contrato", []):
            if tag not in validos:
                problemas.append(f"{rid}: tipo_contrato {tag!r} não é tipo nem grupo")
        corte = r.get("corte_temporal") or {}
        mk = corte.get("marco")
        posicao = corte.get("posicao")
        if mk:
            if mk not in ids_marco:
                problemas.append(f"{rid}: corte_temporal.marco {mk} não existe em marcos_temporais")
            por_marco.setdefault(mk, set()).add(rid)
        if (mk or posicao is not None) and posicao not in POSICOES:
            problemas.append(f"{rid}: corte_temporal.posicao inválida: {posicao!r} "
                             f"(use {', '.join(POSICOES)})")
        for chave in r.get("regime_por_marco") or {}:
            for citado in re.findall(r"MT\d+", chave):
                if citado not in ids_marco:
                    problemas.append(f"{rid}: regime_por_marco cita o marco {citado}, que não existe")
                por_marco.setdefault(citado, set()).add(rid)

    for m in marcos:
        mid = m.get("id")
        if m.get("base") not in BASES:
            problemas.append(f"{mid}.base inválida: {m.get('base')!r} (use {', '.join(BASES)})")
        atual, esperado = set(m.get("regras_afetadas", [])), por_marco.get(mid, set())
        if atual != esperado:
            problemas.append(f"{mid}.regras_afetadas {sorted(atual)} difere do derivado do corte "
                             f"das regras {sorted(esperado)}")

    for t in tipos:
        for campo in ("regras_desligadas", "regras_sem_cdc", "regras_especificas"):
            for rid in t.get(campo) or []:
                if rid not in existentes:
                    problemas.append(f"tipo {t.get('id')}.{campo}: a regra {rid} não existe")
    for tema in dados.get("pendencias_jurisprudenciais", {}).get("temas", []):
        for rid in tema.get("regras_afetadas", []):
            if rid not in existentes:
                problemas.append(f"pendência {tema.get('tema')!r}: a regra {rid} não existe")
    return problemas


# ─────────────────────────────────────────────────────────────────────
# 6. AUTOTESTE
# ─────────────────────────────────────────────────────────────────────

def _testes() -> tuple[int, int]:
    ok = fail = 0

    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond:
            ok += 1; print(f"  PASS  {nome} {extra}")
        else:
            fail += 1; print(f"  FAIL  {nome} {extra}")

    def levanta(excecao, fn, *a, **k):
        try:
            fn(*a, **k)
        except excecao:
            return True
        except Exception:                                                   # noqa: BLE001
            return False
        return False

    dados = carregar_dados()
    R = {r["id"]: r for r in dados["regras"]}
    M = {m["id"]: m for m in dados["marcos_temporais"]["marcos"]}
    HOJE = "2026-10-26"

    def na_data(mt, dias=0):
        """Data do marco, deslocada em `dias`: os testes de fronteira partem do próprio JSON."""
        return (date.fromisoformat(M[mt]["data"]) + timedelta(days=dias)).isoformat()

    def avalia(tipo="consumo_pf", regime="consumerista", dc="2019-05-02", **k):
        k.setdefault("hoje", HOJE)
        return avaliar(tipo, regime, dc, **k)

    def onde(saida, rid):
        for lista in ("aplicaveis", "confirmar", "nao_aplicaveis"):
            for item in saida[lista]:
                if item["id"] == rid:
                    return lista, item
        return None, None

    # ── integridade do JSON ───────────────────────────────────────
    problemas = validar_dados(dados)
    chk("validar_dados: JSON real íntegro", problemas == [], str(problemas[:2]))
    adulterado = copy.deepcopy(dados)
    adulterado["tipos_contrato"]["grupos"]["todos_sfn"].append("consumo_pf")
    adulterado["regras"][0]["corte_temporal"]["marco"] = "MT99"
    adulterado["marcos_temporais"]["marcos"][0]["base"] = "inventada"
    achados = " | ".join(validar_dados(adulterado))
    chk("validar_dados acusa grupo, marco e base adulterados",
        "todos_sfn" in achados and "MT99" in achados and "inventada" in achados)
    chk("carregar_dados guarda em cache por caminho", carregar_dados() is dados)

    # ── datas, relações e posições (fronteira = data igual ao marco) ──
    chk("relacao: anterior, igual e posterior",
        (relacao("2017-08-31", "2017-09-01"), relacao("2017-09-01", "2017-09-01"),
         relacao(date(2017, 9, 2), date(2017, 9, 1))) == ("anterior", "igual", "posterior"))
    tabela = {"anterior": (True, False, False), "anterior_ou_igual": (True, True, False),
              "posterior": (False, False, True)}
    chk("posicao_atende: anterior < marco, anterior_ou_igual <= marco, posterior > marco",
        all(tuple(posicao_atende(p, r) for r in ("anterior", "igual", "posterior")) == esperado
            for p, esperado in tabela.items()))
    chk("posicao_atende recusa posição desconhecida", levanta(ValueError, posicao_atende, "depois", "igual"))

    chk("fronteira 'anterior' (R01, MT04): no dia do marco NÃO atende, na véspera atende",
        onde(avalia(dc=na_data("MT04")), "R01")[0] == "nao_aplicaveis"
        and onde(avalia(dc=na_data("MT04", -1)), "R01")[0] == "aplicaveis")
    chk("fronteira 'anterior_ou_igual' (R05, MT02): no dia do marco atende, no dia seguinte não",
        onde(avalia(dc=na_data("MT02")), "R05")[0] == "aplicaveis"
        and onde(avalia(dc=na_data("MT02", 1)), "R05")[0] == "nao_aplicaveis")
    chk("fronteira 'posterior' (R04, MT02): no dia do marco NÃO atende, no dia seguinte atende",
        onde(avalia(dc=na_data("MT02")), "R04")[0] == "nao_aplicaveis"
        and onde(avalia(dc=na_data("MT02", 1)), "R04")[0] == "aplicaveis")
    d_mt02 = date.fromisoformat(M["MT02"]["data"]).strftime("%d/%m/%Y")
    chk("motivo do corte traz marco, data e posição exigida",
        onde(avalia(dc=na_data("MT02")), "R04")[1]["motivo"]
        == f"MT02 ({d_mt02}): contrato igual ao marco — a regra exige posterior")

    mar = resolver_marcos("2019-05-02", None)
    chk("resolver_marcos: relação, base e notas por base",
        mar["MT04"]["contrato"] == "posterior" and mar["MT02"]["base"] == "contrato"
        and "reparte a apuração" in mar["MT05"]["nota"] and "operação" in mar["MT06"]["nota"]
        and mar["MT10"]["consolidacao"] is None and "consolidacao" not in mar["MT01"])
    chk("resolver_marcos sem datas: relações nulas", resolver_marcos()["MT01"]["contrato"] is None)

    # ── um caso de cada destino ───────────────────────────────────
    caso = avalia()
    chk("destino aplicável: R15 em consumo_pf", onde(caso, "R15")[0] == "aplicaveis")
    chk("destino não aplicável: R17 (cédulas) em consumo_pf, com motivo de tipo",
        onde(caso, "R17")[0] == "nao_aplicaveis"
        and onde(caso, "R17")[1]["motivo"] == "tipo_contrato cedula_rural, cedula_comercial, "
        "cedula_industrial não inclui consumo_pf")
    sem_data = avalia(dc=None)
    chk("destino confirmar: R04 sem data do contrato",
        onde(sem_data, "R04")[0] == "confirmar"
        and onde(sem_data, "R04")[1]["motivo"] == f"data do contrato ausente — corte MT02 ({d_mt02})")
    chk("resumo conta os três destinos e fecha com todas as regras",
        sum(caso["resumo"][k] for k in ("aplicaveis", "confirmar", "nao_aplicaveis")) == len(dados["regras"])
        and caso["resumo"]["omitidas_por_categoria"] == 0)

    # ── grupos, desligadas, regime ────────────────────────────────
    sfh = avalia("sfh", dc=na_data("MT10", -30), data_consolidacao=na_data("MT10", -10))
    chk("regra desligada no tipo: R15 em sfh",
        onde(sfh, "R15")[1]["motivo"] == "desligada no tipo sfh (regras_desligadas)")
    chk("grupo todos_sem_lei_especifica: R21 vale em cartao_credito e não em sfh",
        onde(avalia("cartao_credito"), "R21")[0] == "aplicaveis" and onde(sfh, "R21")[0] == "nao_aplicaveis")
    sem_desligar = copy.deepcopy(dados)
    for t in sem_desligar["tipos_contrato"]["tipos"]:
        if t["id"] == "imobiliario_fora_sfi":
            t["regras_desligadas"] = [x for x in t["regras_desligadas"] if x != "R18"]
    grupo = onde(avaliar("imobiliario_fora_sfi", "consumerista", "2019-01-01", hoje=HOJE,
                         dados=sem_desligar), "R18")
    chk("grupo todos_sfn exclui o tipo com credor_sfn: false",
        grupo[0] == "nao_aplicaveis" and grupo[1]["motivo"] == "tipo_contrato todos_sfn não inclui imobiliario_fora_sfi"
        and onde(avalia(dc="2019-01-01"), "R18")[0] == "aplicaveis")
    cons = onde(avalia(), "R15")[1]
    civ = onde(avalia(regime="civil_empresarial"), "R15")[1]
    blocos = R["R15"]["regime"]
    chk("R15: tier e consequência vêm do bloco regime",
        (cons["tier"], cons["consequencia"]) == (blocos["consumerista"]["tier"], blocos["consumerista"]["consequencia"])
        and (civ["tier"], civ["consequencia"]) == (blocos["civil_empresarial"]["tier"], blocos["civil_empresarial"]["consequencia"])
        and cons["tier"] != civ["tier"])
    chk("regime aceita o alias civil-empresarial",
        avalia(regime="civil-empresarial")["entrada"]["regime"] == "civil_empresarial")
    pj_c = avalia("empresarial_pj", "consumerista")
    chk("empresarial_pj consumerista (CDC mitigado): regras consumo_pf casam",
        onde(pj_c, "R04")[0] == "aplicaveis")
    pj_e = avalia("empresarial_pj", "civil_empresarial", dc=na_data("MT04", -1))
    chk("empresarial_pj civil-empresarial: fora de regras_sem_cdc vai a confirmar, dentro aplica",
        onde(pj_e, "R11")[0] == "confirmar" and "regra de conduta 18" in onde(pj_e, "R11")[1]["motivo"]
        and onde(pj_e, "R01")[0] == "aplicaveis" and onde(pj_e, "R15")[0] == "aplicaveis"
        and onde(pj_e, "R04")[0] == "nao_aplicaveis")
    chk("consumo_pf civil-empresarial: regra só consumerista é não aplicável",
        onde(avalia(regime="civil_empresarial"), "R04")[1]["motivo"]
        == "regra consumerista — regime civil-empresarial")
    cartao = avalia("cartao_credito")
    chk("repetição consumerista em tipo que não é consumo_pf/empresarial_pj vai a confirmar",
        onde(cartao, "R26")[0] == "confirmar" and "regra de conduta 9" in onde(cartao, "R26")[1]["motivo"]
        and onde(avalia("cartao_credito", regime="civil_empresarial"), "R26")[0] == "nao_aplicaveis")

    # ── corte por pagamento, operação e consolidação ──────────────
    chk("corte por pagamento (MT05) não exclui: aplicável com `corte`",
        onde(caso, "R26")[1]["corte"] == {"marco": "MT05", "data": M["MT05"]["data"],
                                          "base": "pagamento", "posicao": "posterior"})
    r23 = onde(avalia("cartao_credito", dc="2020-01-01"), "R23")
    chk("corte por operação (MT06) não exclui pela data do contrato",
        r23[0] == "aplicaveis" and r23[1]["corte"]["base"] == "operacao")

    def r40(dc, dk):
        return onde(avalia("sfh", dc=dc, data_consolidacao=dk), "R40")
    antes, depois_ = na_data("MT10", -30), na_data("MT10", 30)
    chk("MT10 sem as duas datas → confirmar",
        r40(None, None)[0] == "confirmar" and r40(antes, None)[1]["motivo"] == "datar contrato e consolidação (MT10)")
    chk("MT10 contrato e consolidação antes do marco → aplicável",
        r40(antes, antes)[1]["corte"]["leitura"] == "contrato e consolidação atendem ao marco")
    chk("MT10 nenhum dos dois antes do marco → não aplicável",
        r40(depois_, depois_)[0] == "nao_aplicaveis"
        and r40(depois_, depois_)[1]["motivo"] == "MT10: contrato e consolidação fora do marco")
    chk("MT10 só o contrato antes → aplicável com a leitura divergente",
        r40(antes, depois_)[1]["corte"]["leitura"] == "só o contrato atende ao marco — critério temporal "
        "divergente (ver pendências)")
    chk("MT10 só a consolidação antes → aplicável com a leitura divergente",
        r40(depois_, antes)[1]["corte"]["leitura"].startswith("só a consolidação atende ao marco"))

    # ── R03: regime_por_marco ─────────────────────────────────────
    por_marco = R["R03"]["regime_por_marco"]
    r03_antes = onde(avalia(dc=na_data("MT04", -1)), "R03")[1]
    r03_depois = onde(avalia(dc=na_data("MT04")), "R03")[1]
    r03_sem = onde(avalia(dc=None), "R03")[1]
    chk("R03 antes do MT04: consequência, fundamentação e sem alerta da leitura posterior",
        r03_antes["consequencia"] == por_marco["anterior_a_MT04"]["consequencia"]
        and r03_antes["fundamentacao_marco"] == por_marco["anterior_a_MT04"]["fundamentacao"]
        and "alerta" not in r03_antes and "leitura_por_marco_pendente" not in r03_antes)
    chk("R03 no dia do MT04 já é posterior: alerta, pesquisa e termos suspeitos",
        r03_depois["consequencia"] == por_marco["posterior_a_MT04"]["consequencia"]
        and r03_depois["alerta"] == por_marco["posterior_a_MT04"]["alerta"]
        and r03_depois["exige_pesquisa"] is True
        and r03_depois["termos_suspeitos"] == R["R03"]["padroes_deteccao"]["termos_suspeitos"])
    chk("R03 sem data do contrato: consequência geral e leitura pendente",
        r03_sem["leitura_por_marco_pendente"] is True and r03_sem["consequencia"] == R["R03"]["consequencia"]
        and "fundamentacao_marco" not in r03_sem)

    # ── pendências, conclusiva e alertas vencidos (hoje fixo) ─────
    tema = next(t for t in dados["pendencias_jurisprudenciais"]["temas"] if "R15" in t["regras_afetadas"])
    limite = date.fromisoformat(tema["verificado_em"]) + timedelta(days=dados["pendencias_jurisprudenciais"]["validade_dias"])
    ate, depois = avalia(hoje=limite), avalia(hoje=limite + timedelta(days=1))
    chk("pendência no último dia da validade ainda vale; no dia seguinte vence",
        onde(ate, "R15")[1]["pendencias"][0]["vencida"] is False and "R15" not in ate["resumo"]["com_alerta_vencido"]
        and onde(ate, "R15")[1]["alertas_vencidos"] == []
        and onde(depois, "R15")[1]["pendencias"][0]["vencida"] is True
        and "R15" in depois["resumo"]["com_alerta_vencido"])
    alerta = onde(depois, "R15")[1]["alertas_vencidos"][0]
    chk("alerta vencido preenche tema e data em dd/mm/aaaa",
        alerta == dados["pendencias_jurisprudenciais"]["alerta_vencido"].replace("{tema}", tema["tema"]).replace(
            "{verificado_em}", date.fromisoformat(tema["verificado_em"]).strftime("%d/%m/%Y")))
    chk("regra suspensa não é conclusiva e exige pesquisa; a vigente é conclusiva",
        cons["conclusiva"] is False and cons["exige_pesquisa"] is True and "R15" in caso["resumo"]["nao_conclusivas"]
        and onde(caso, "R28")[1]["conclusiva"] is True and onde(caso, "R28")[1]["exige_pesquisa"] is False)

    # ── categorias e formatos ─────────────────────────────────────
    so_tarifas = avalia(categorias=["tarifas"])
    n_tarifas = sum(1 for r in dados["regras"] if r["categoria"] == "tarifas")
    chk("categorias: só a categoria pedida entra e o resto é contado",
        {i["id"] for k in ("aplicaveis", "confirmar", "nao_aplicaveis") for i in so_tarifas[k]}
        == {r["id"] for r in dados["regras"] if r["categoria"] == "tarifas"}
        and so_tarifas["resumo"]["omitidas_por_categoria"] == len(dados["regras"]) - n_tarifas)
    resumo = onde(avalia(formato="resumo"), "R26")[1]
    completo = onde(avalia(formato="completo"), "R15")[1]
    padrao = onde(caso, "R15")[1]
    chk("formato resumo: poucos campos, com `corte` quando há",
        set(resumo) == {"id", "categoria", "nome", "tier", "status", "conclusiva", "corte"})
    chk("formato completo: padrão mais descricao, fundamentacao e bloco regime integral",
        set(padrao) < set(completo) and completo["regime"] == R["R15"]["regime"]
        and completo["fundamentacao"] == R["R15"]["fundamentacao"])
    chk("teste do item só traz as chaves acordadas",
        set(padrao["teste"]) == {"logica", "campos_necessarios", "requer_consulta_bacen", "parametros"})
    chk("tipo, regime e formato inválidos levantam ValueError",
        levanta(ValueError, avaliar, "inexistente", "consumerista")
        and levanta(ValueError, avaliar, "consumo_pf", "outro")
        and levanta(ValueError, avaliar, "consumo_pf", "consumerista", formato="longo"))

    # ── consultas ─────────────────────────────────────────────────
    chk("regra integral e KeyError", regra("R15") == R["R15"] and levanta(KeyError, regra, "R99"))
    chk("súmula 530 e KeyError", sumula(530)["numero"] == 530 and levanta(KeyError, sumula, 1))
    mapa = dados["series_bacen_por_modalidade"]["mapeamento"]
    chk("series: tudo, por modalidade exata e por busca sem acento e sem caixa",
        series() == mapa and [s["serie"] for s in series(modalidade="cartao_rotativo")] == [25477]
        and len(series(buscar="CARTÃO")) == len(series(buscar="cartao")) > 0
        and "cartao_rotativo" in {s["modalidade"] for s in series(buscar="Rotativo")})

    # ── razão contratada / média: faixas e exatamente nos limiares ─
    lic, zon, fort = classificar_razao(2.99, 2.0), classificar_razao(3.00, 2.0), classificar_razao(4.00, 2.0)
    chk("razão 1,495x → licita; exatamente 1,5x → zona_cinzenta; exatamente 2,0x → ilicita",
        (lic["classificacao"], zon["classificacao"], fort["classificacao"]) == ("licita", "zona_cinzenta", "ilicita")
        and zon["razao"] == 1.5 and zon["razao_txt"] == "1,50x" and fort["rotulo"] == "fortemente abusiva")
    chk("0,03 / 0,02 dá exatamente 1,5 (Decimal, não float)",
        classificar_razao(0.03, 0.02)["classificacao"] == "zona_cinzenta" and classificar_razao(0.03, 0.02)["razao"] == 1.5)
    r158 = classificar_razao(4.74, 3.0)
    chk("razao_txt com 2 casas e vírgula; limiares em % a.m. (média × limiar)",
        r158["razao_txt"] == "1,58x" and r158["limiares_am"] == {"zona_cinzenta": 4.5, "forte": 6.0}
        and r158["classificacao"] == "zona_cinzenta")
    chk("razão: média <= 0 e contratada negativa levantam ValueError",
        levanta(ValueError, classificar_razao, 2.0, 0) and levanta(ValueError, classificar_razao, -1, 2.0))

    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("regras", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    print("Autoteste — motores/regras.py v1.0.0\n")
    raise SystemExit(1 if autoteste()["falharam"] else 0)
