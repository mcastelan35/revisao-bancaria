"""
jurisprudencia.py — repertório jurisprudencial validado e espelho da petição inicial

O repertório (`referencia/repertorio-jurisprudencial.md`) guarda, por regra do motor (R01…) ou
tese própria (PJ-VULN…), os julgados que a petição pode citar: ementa na íntegra, copiada do
inteiro teor lido no conector Jusbrasil, com identificação completa e a url canônica. O agente
não lê o arquivo inteiro: pede só os julgados das regras do caso.

    python3 revisao.py jurisprudencia consultar --regras R01,R04
    python3 revisao.py jurisprudencia cobertura
    python3 revisao.py jurisprudencia validar
    python3 revisao.py espelho payload.json --saida DIR

Formato de uma entrada (o parser é estrito; o validador diz a linha do defeito):

    ## R04 — TAC vedada em contratos pós-30/04/2008
    Tese: <a tese como o autor a sustenta>

    ### STJ · REsp 1.251.331/RS
    - regras: R04, R06
    - posicao: FAV | ADV          (ADV = limite fixado pelo STJ/STF, vira ressalva)
    - tribunal: STJ | STF | TJPR | TJSP | TRF4 …   (tribunal local só entra FAV)
    - classe_numero, orgao, relator, julgamento (AAAA-MM-DD), publicacao (AAAA-MM-DD),
      precedente_qualificado, url (jusbrasil.com.br ou, para o TJPR, o link permanente do
      portal do tribunal), verificado_em (AAAA-MM-DD),
      status (VERIFICADO | CONFERIR), uso_na_peca, observacao
    ementa:
    > texto integral, uma ou mais linhas

Só sai na consulta e no espelho o que está VERIFICADO e dentro da validade (VALIDADE_DIAS desde
`verificado_em`); o resto vira aviso. Só biblioteca padrão.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

from .comum import rodar_autoteste

PASTA_SKILL = Path(__file__).resolve().parent.parent
CAMINHO_PADRAO = PASTA_SKILL / "referencia" / "repertorio-jurisprudencial.md"

CAMPOS = ("regras", "posicao", "tribunal", "classe_numero", "orgao", "relator", "julgamento",
          "publicacao", "precedente_qualificado", "url", "verificado_em", "status", "uso_na_peca",
          "observacao")
CAMPOS_DATA = ("julgamento", "publicacao", "verificado_em")
POSICOES = ("FAV", "ADV")
STATUS = ("VERIFICADO", "CONFERIR")
SUPERIORES = ("STF", "STJ")
VALIDADE_DIAS = 365                  # revalidar no Jusbrasil uma vez por ano
EMENTA_MINIMA = 80                   # caracteres: menos que isso é trecho, não ementa
PREFIXO_URL = "https://www.jusbrasil.com.br/"
# Fonte oficial do próprio tribunal, admitida para os acórdãos dele quando o inteiro teor do
# Jusbrasil vem sem ementa (Câmaras Cíveis do TJPR): url é o link permanente do acórdão no portal.
FONTES_OFICIAIS = {"TJPR": "https://portal.tjpr.jus.br/jurisprudencia/j/"}


def fonte_valida(url: str, tribunal: str) -> bool:
    """A url aponta para o Jusbrasil ou para o portal oficial do próprio tribunal do julgado."""
    oficial = FONTES_OFICIAIS.get(tribunal)
    return url.startswith(PREFIXO_URL) or bool(oficial and url.startswith(oficial))

RE_TESE = re.compile(r"^## ((?:R\d{2})|(?:[A-Z]{2,}-[A-Z0-9-]+)) — (.+)$")
RE_CAMPO = re.compile(r"^- ([a-z_]+):\s*(.*)$")
RE_TRIBUNAL = re.compile(r"^(STF|STJ|TJ[A-Z]{2}|TJDFT|TRF[1-6])$")
RE_ID = re.compile(r"^(R\d{2}|[A-Z]{2,}-[A-Z0-9-]+)$")

# Ordem de citação na peça: precedente vinculante primeiro, depois o tribunal local do escritório.
ORDEM_TRIBUNAL = {"STF": 0, "STJ": 1, "TJPR": 2}


class RepertorioErro(ValueError):
    """Repertório com defeito de formato (o `validar` lista todos; o `ler` para no primeiro)."""


# ─────────────────────────────────────────────────────────────────────
# leitura
# ─────────────────────────────────────────────────────────────────────

def _parse(texto: str) -> tuple[dict, list[dict], list[str]]:
    """(teses, entradas, defeitos de formato). Linhas dentro de cercas ``` são ignoradas."""
    teses: dict = {}
    entradas: list[dict] = []
    defeitos: list[str] = []
    tese = entrada = None
    na_ementa = cerca = False

    def fechar():
        nonlocal entrada, na_ementa
        if entrada is not None:
            entrada["ementa"] = "\n".join(entrada["ementa"]).strip()
            entradas.append(entrada)
        entrada, na_ementa = None, False

    for n, linha in enumerate(texto.splitlines(), 1):
        if linha.lstrip().startswith("```"):
            cerca = not cerca
            continue
        if cerca:
            continue
        if linha.startswith("## "):
            fechar()
            m = RE_TESE.match(linha.strip())
            tese = m.group(1) if m else None
            if m:
                if tese in teses:
                    defeitos.append(f"linha {n}: tese {tese} repetida")
                teses[tese] = {"id": tese, "titulo": m.group(2).strip(), "tese": "", "linha": n}
            continue
        if tese is None:
            if linha.startswith("### "):
                defeitos.append(f"linha {n}: julgado fora de uma seção de tese (## <ID> — título)")
            continue
        if linha.startswith("### "):
            fechar()
            entrada = {"titulo": linha[4:].strip(), "tese_id": tese, "linha": n, "ementa": []}
            continue
        if entrada is None:
            if linha.startswith("Tese:"):
                teses[tese]["tese"] = linha[5:].strip()
            continue
        if na_ementa:
            if linha.startswith(">"):
                entrada["ementa"].append(linha[1:].removeprefix(" ").rstrip())
            elif linha.strip():
                defeitos.append(f"linha {n}: texto fora do bloco '> ' da ementa em {entrada['titulo']}")
            continue
        if linha.strip() == "ementa:":
            na_ementa = True
            continue
        m = RE_CAMPO.match(linha)
        if m:
            chave, valor = m.groups()
            if chave not in CAMPOS:
                defeitos.append(f"linha {n}: campo desconhecido '{chave}' em {entrada['titulo']}")
            elif chave in entrada:
                defeitos.append(f"linha {n}: campo '{chave}' repetido em {entrada['titulo']}")
            else:
                entrada[chave] = valor.strip()
        elif linha.strip():
            defeitos.append(f"linha {n}: linha fora do formato em {entrada['titulo']}: {linha.strip()[:60]}")
    fechar()
    for e in entradas:
        if "regras" in e:
            e["regras"] = [r.strip() for r in e["regras"].split(",") if r.strip()]
    return teses, entradas, defeitos


def _data(valor: str) -> date | None:
    try:
        return date.fromisoformat(valor)
    except (TypeError, ValueError):
        return None


def _ids_regras() -> set[str]:
    from . import regras
    return {r["id"] for r in regras.carregar_dados()["regras"]}


def validar(texto: str | None = None, ids_regras: set[str] | None = None,
            hoje: str | None = None) -> dict:
    """{"erros": [...], "avisos": [...], "teses": n, "entradas": n}. Erro = entrada que não pode ser
    citada como está; aviso = entrada vencida ou detalhe a revisar."""
    texto = CAMINHO_PADRAO.read_text(encoding="utf-8") if texto is None else texto
    ids_regras = _ids_regras() if ids_regras is None else ids_regras
    dia = _data(hoje) if hoje else date.today()
    teses, entradas, erros = _parse(texto)
    avisos: list[str] = []
    for t in teses.values():
        if t["id"].startswith("R") and t["id"] not in ids_regras:
            erros.append(f"linha {t['linha']}: tese {t['id']} não é regra do motor")
        if not t["tese"]:
            erros.append(f"linha {t['linha']}: tese {t['id']} sem a linha 'Tese:'")
    urls: dict = {}
    for e in entradas:
        onde = f"linha {e['linha']} ({e['titulo']})"
        faltam = [c for c in CAMPOS if not e.get(c)]
        if faltam:
            erros.append(f"{onde}: faltam {', '.join(faltam)}")
        if len(e["ementa"]) < EMENTA_MINIMA:
            erros.append(f"{onde}: ementa ausente ou curta demais para ser a íntegra")
        for r in e.get("regras", []):
            if not RE_ID.match(r) or (r.startswith("R") and r not in ids_regras) or \
                    (not r.startswith("R") and r not in teses):
                erros.append(f"{onde}: regra/tese inexistente '{r}'")
        if e.get("regras") and e["tese_id"] not in e["regras"]:
            erros.append(f"{onde}: está sob {e['tese_id']} mas 'regras' não inclui {e['tese_id']}")
        if e.get("posicao") and e["posicao"] not in POSICOES:
            erros.append(f"{onde}: posicao '{e['posicao']}' fora de {POSICOES}")
        tribunal = e.get("tribunal", "")
        if tribunal and not RE_TRIBUNAL.match(tribunal):
            erros.append(f"{onde}: tribunal '{tribunal}' fora do padrão (STJ, STF, TJPR, TRF4…)")
        if tribunal and tribunal not in SUPERIORES and e.get("posicao") == "ADV":
            erros.append(f"{onde}: tribunal local só entra favorável (posicao FAV)")
        if e.get("status") and e["status"] not in STATUS:
            erros.append(f"{onde}: status '{e['status']}' fora de {STATUS}")
        url = e.get("url", "")
        if url and not fonte_valida(url, e.get("tribunal", "")):
            erros.append(f"{onde}: url fora do Jusbrasil e do portal oficial do tribunal ({url[:60]})")
        if url in urls:
            erros.append(f"{onde}: julgado repetido (mesma url da linha {urls[url]}); "
                         "liste as regras numa entrada só")
        urls.setdefault(url, e["linha"])
        datas = {c: _data(e.get(c)) for c in CAMPOS_DATA}
        for c, d in datas.items():
            if e.get(c) and d is None:
                erros.append(f"{onde}: {c} '{e.get(c)}' não é AAAA-MM-DD")
            elif d and d > dia:
                erros.append(f"{onde}: {c} {d} no futuro")
        if datas["julgamento"] and datas["publicacao"] and datas["julgamento"] > datas["publicacao"]:
            avisos.append(f"{onde}: julgamento depois da publicação")
        if datas["verificado_em"] and dia - datas["verificado_em"] > timedelta(days=VALIDADE_DIAS):
            avisos.append(f"{onde}: verificação vencida em {datas['verificado_em'] + timedelta(days=VALIDADE_DIAS)}")
        if e.get("status") == "CONFERIR":
            avisos.append(f"{onde}: status CONFERIR — não sai na consulta")
    return {"erros": erros, "avisos": avisos, "teses": len(teses), "entradas": len(entradas)}


def ler(caminho: Path | None = None) -> tuple[dict, list[dict]]:
    """(teses, entradas) do repertório; levanta RepertorioErro se o formato tiver defeito."""
    texto = Path(caminho or CAMINHO_PADRAO).read_text(encoding="utf-8")
    teses, entradas, defeitos = _parse(texto)
    if defeitos:
        raise RepertorioErro(f"repertório com defeito de formato: {defeitos[0]} "
                             f"(+{len(defeitos) - 1}); rode `jurisprudencia validar`")
    return teses, entradas


# ─────────────────────────────────────────────────────────────────────
# consulta
# ─────────────────────────────────────────────────────────────────────

def _citavel(e: dict, dia: date) -> str | None:
    """None se a entrada pode ser citada; senão o motivo."""
    if e.get("status") != "VERIFICADO":
        return f"status {e.get('status') or 'ausente'}"
    verificado = _data(e.get("verificado_em"))
    if verificado is None:
        return "sem data de verificação"
    if dia - verificado > timedelta(days=VALIDADE_DIAS):
        return f"verificação vencida (verificado em {verificado})"
    if any(not e.get(c) for c in CAMPOS) or len(e.get("ementa", "")) < EMENTA_MINIMA:
        return "entrada incompleta"
    return None


def _qualificado(e: dict) -> bool:
    """`precedente_qualificado` preenchido com tema, súmula ou IRDR (e não "não …" ou "—")."""
    valor = (e.get("precedente_qualificado") or "").strip().lower()
    return bool(valor) and not valor.startswith(("não", "nao", "—", "-"))


ORGAOS_UNIFORMIZADORES = ("corte especial", "segunda seção", "primeira seção", "terceira seção",
                          "plenário", "tribunal pleno", "órgão especial")


def _ordem(e: dict) -> tuple:
    """Tribunal (STF, STJ, TJPR, demais), depois precedente qualificado ou de órgão uniformizador,
    depois o mais recente."""
    orgao = (e.get("orgao") or "").lower()
    peso = 0 if _qualificado(e) or orgao.startswith(ORGAOS_UNIFORMIZADORES) else 1
    recente = -(_data(e.get("julgamento")) or date.min).toordinal()
    return (ORDEM_TRIBUNAL.get(e.get("tribunal"), 3), peso, recente)


def _cautela(e: dict) -> str:
    obs = (e.get("observacao") or "").strip()
    return "" if obs in ("", "—", "-") else f" *Cautela:* {obs}"


def _publica(e: dict) -> dict:
    return {c: e.get(c) for c in ("titulo", *CAMPOS, "ementa")}


def consultar(ids, incluir_adversos: bool = True, hoje: str | None = None,
              caminho: Path | None = None) -> dict:
    """Julgados citáveis por regra/tese: {"teses": {id: {titulo, tese, favoraveis, adversos}},
    "sem_cobertura": [ids sem nenhum favorável citável], "avisos": [...]}."""
    teses, entradas = ler(caminho)
    dia = _data(hoje) if hoje else date.today()
    saida: dict = {"teses": {}, "sem_cobertura": [], "avisos": []}
    for i in dict.fromkeys(ids):
        fav, adv = [], []
        for e in entradas:
            if i not in e.get("regras", []):
                continue
            motivo = _citavel(e, dia)
            if motivo:
                saida["avisos"].append(f"{i}: {e['titulo']} fora da consulta — {motivo}")
                continue
            (fav if e["posicao"] == "FAV" else adv).append(e)
        t = teses.get(i, {})
        bloco = {"titulo": t.get("titulo"), "tese": t.get("tese"),
                 "favoraveis": [_publica(e) for e in sorted(fav, key=_ordem)]}
        if incluir_adversos:
            bloco["adversos"] = [_publica(e) for e in sorted(adv, key=_ordem)]
        saida["teses"][i] = bloco
        if not fav:
            saida["sem_cobertura"].append(i)
    return saida


def cobertura(hoje: str | None = None, caminho: Path | None = None) -> dict:
    """Por regra do motor: favoráveis STJ/STF, favoráveis locais e adversos citáveis. Lista as
    regras T1 vigentes sem favorável de tribunal superior — a fila da próxima onda de pesquisa."""
    from . import regras
    _, entradas = ler(caminho)
    dia = _data(hoje) if hoje else date.today()
    linhas, faltam_t1 = [], []
    for r in regras.carregar_dados()["regras"]:
        cit = [e for e in entradas if r["id"] in e.get("regras", []) and not _citavel(e, dia)]
        sup = sum(e["posicao"] == "FAV" and e["tribunal"] in SUPERIORES for e in cit)
        loc = sum(e["posicao"] == "FAV" and e["tribunal"] not in SUPERIORES for e in cit)
        adv = sum(e["posicao"] == "ADV" for e in cit)
        linhas.append({"id": r["id"], "tier": r.get("tier"), "status": r.get("status"),
                       "fav_superior": sup, "fav_local": loc, "adversos": adv})
        if r.get("tier") == "T1" and not sup:
            faltam_t1.append(r["id"])
    return {"regras": linhas, "t1_sem_superior": faltam_t1,
            "entradas_citaveis": sum(not _citavel(e, dia) for e in entradas)}


# ─────────────────────────────────────────────────────────────────────
# espelho da petição inicial
# ─────────────────────────────────────────────────────────────────────

VERMELHOS = {"Ilícito", "Ilícito parcial", "Divergência", "Contradição", "Excesso", "Prejudicial",
             "Não discriminado", "Base de cálculo"}
AMBARES = {"Lacuna", "A demonstrar", "A verificar", "Excessivo", "Inconsistência"}
ORDEM_TIER = {"T1": 0, "T2": 1}


def _citacao(e: dict) -> str:
    """Identificação completa, no padrão de citação forense."""
    partes = [e["tribunal"], e["classe_numero"], e["relator"], e["orgao"],
              f"julgado em {_br(e['julgamento'])}", f"publicado em {_br(e['publicacao'])}"]
    if _qualificado(e):
        partes.append(e["precedente_qualificado"])
    return ", ".join(partes)


def _br(iso: str) -> str:
    d = _data(iso)
    return d.strftime("%d/%m/%Y") if d else iso


def _ementa_md(texto: str) -> list[str]:
    return [f"> {l}" if l else ">" for l in texto.splitlines()]


def espelho(payload: dict, skill_peticao: str | None = None, hoje: str | None = None,
            caminho: Path | None = None) -> tuple[str, dict]:
    """Markdown do espelho da inicial e um resumo {teses, julgados, sem_jurisprudencia, avisos}.

    Só entram os achados contra o banco (vermelho) ou pendentes (âmbar), T1 antes de T2; cada um
    puxa os julgados citáveis das regras em `achados[*].regras`. Nada é inventado: o que falta
    vira item de "Pendências antes de protocolar"."""
    from . import regras as motor_regras
    dados_regras = {r["id"]: r for r in motor_regras.carregar_dados()["regras"]}
    achados = [a for a in payload.get("achados", []) if a.get("resultado") in VERMELHOS | AMBARES]
    achados.sort(key=lambda a: (ORDEM_TIER.get(a.get("tier"), 2), a.get("resultado") in AMBARES))
    ids = [r for a in achados for r in a.get("regras", [])]
    consulta = consultar(ids, hoje=hoje, caminho=caminho) if ids else \
        {"teses": {}, "sem_cobertura": [], "avisos": []}
    ident = payload.get("identificacao", {})
    L: list[str] = []
    w = L.append

    w(f"# Espelho da petição inicial — {payload.get('titulo', 'análise')}")
    w("")
    w(f"Referência do laudo: {ident.get('referencia', '—')} · gerado em "
      f"{_br(hoje) if hoje else date.today().strftime('%d/%m/%Y')}")
    w("")
    w("> Roteiro para redigir a inicial, não a petição. Os fatos e os números vêm do laudo; "
      "a jurisprudência vem do repertório do plugin, com ementa conferida no inteiro teor pelo "
      "Jusbrasil e link de acesso. Não acrescente julgado que não esteja aqui sem antes validá-lo.")
    w("")
    w(f"**Formato de redação:** " + (f"skill de petição canônica do escritório `{skill_peticao}` — "
      "ela define endereçamento, qualificação, estilo e estrutura; este espelho entra como insumo."
      if skill_peticao else "neutro (nenhuma skill de petição configurada no `operador`)."))
    w("")
    w("## 1. Endereçamento e partes")
    w("")
    w("[A PREENCHER] Juízo competente, qualificação completa do autor e da instituição financeira.")
    w("")
    w("## 2. Dos fatos")
    w("")
    for rot, val, *_ in ident.get("campos", []):
        w(f"- **{rot}:** {val}")
    for p in payload.get("objeto", []):
        w("")
        w(p)
    if payload.get("documentos"):
        w("")
        w("Documentos que instruem a inicial:")
        for d in payload["documentos"]:
            w(f"- {' · '.join(str(x) for x in d if x)}")
    w("")
    w("## 3. Do direito")
    sem_juris, julgados = [], 0
    for n, a in enumerate(achados, 1):
        w("")
        w(f"### 3.{n}. {a.get('titulo', 'Achado')} ({a.get('tier', '—')} · {a.get('resultado')})")
        w("")
        w(f"- **Achado do laudo ({a.get('id', '—')}):** {a.get('detalhe', '')}")
        if a.get("fundamento"):
            w(f"- **Fundamento legal:** {a['fundamento']}")
        if a.get("resultado") in AMBARES:
            w("- **Atenção:** achado pendente de prova — sustente como pedido de perícia ou "
              "de exibição, não como fato provado.")
        if not a.get("regras"):
            sem_juris.append(f"{a.get('id', '—')} sem regra vinculada no payload (`achados[*].regras`)")
            continue
        for rid in a["regras"]:
            regra = dados_regras.get(rid, {})
            bloco = consulta["teses"].get(rid, {})
            if regra.get("status") in ("suspensa", "sem_precedente_consolidado") or regra.get("alerta"):
                w(f"- **Alerta {rid}:** status `{regra.get('status')}`. {regra.get('alerta') or ''}".rstrip())
            if bloco.get("tese"):
                w(f"- **Tese ({rid}):** {bloco['tese']}")
            fav = bloco.get("favoraveis", [])
            if not fav:
                sem_juris.append(f"{a.get('id', '—')}/{rid}: nenhum julgado validado no repertório")
                continue
            w("")
            w(f"Jurisprudência ({rid}):")
            for e in fav:
                julgados += 1
                w("")
                w(f"**{_citacao(e)}.** Uso: {e['uso_na_peca']}{_cautela(e)}")
                w("")
                L.extend(_ementa_md(e["ementa"]))
                w("")
                w(f"Fonte: {e['url']}")
            for e in bloco.get("adversos", []):
                julgados += 1
                w("")
                w(f"**Argumento contrário previsto — {_citacao(e)}.** {e['uso_na_peca']}{_cautela(e)}")
                w("")
                L.extend(_ementa_md(e["ementa"]))
                w("")
                w(f"Fonte: {e['url']}")
    w("")
    w("## 4. Das provas")
    w("")
    pendentes = [a for a in achados if a.get("resultado") in AMBARES]
    if pendentes:
        w("- Perícia contábil para os achados pendentes: " +
          ", ".join(a.get("id", "—") for a in pendentes) + ".")
    if payload.get("lacunas"):
        w("- Exibição de documentos (art. 396 do CPC) para suprir as lacunas:")
        for l in payload["lacunas"]:
            w(f"  - {l}")
    if not pendentes and not payload.get("lacunas"):
        w("- Prova documental (contrato e demonstrativos que instruem a inicial).")
    w("")
    w("## 5. Dos pedidos")
    w("")
    vistos = set()
    for a in achados:
        for rid in a.get("regras", []):
            if rid in vistos or rid not in dados_regras:
                continue
            vistos.add(rid)
            w(f"- {rid} — {dados_regras[rid]['nome']}: {dados_regras[rid].get('consequencia', '')}")
    w("- Condenação nas custas e nos honorários advocatícios.")
    w("")
    w("## 6. Do valor da causa")
    w("")
    w(f"{payload['valor_causa']}" if payload.get("valor_causa") else
      "[A DEFINIR] Proveito econômico pretendido, conforme os valores apurados no laudo.")
    w("")
    w("## 7. Pendências antes de protocolar")
    w("")
    pend = [*sem_juris, *consulta["avisos"],
            *(f"Ressalva do laudo: {r}" for r in payload.get("ressalvas", [])),
            *(f"Premissa não comprovada: {p}" for p in payload.get("premissas", []))]
    if not pend:
        w("- Nenhuma.")
    for p in pend:
        w(f"- {p}")
    w("")
    resumo = {"teses": len(achados), "julgados": julgados, "sem_jurisprudencia": sem_juris,
              "avisos": consulta["avisos"]}
    return "\n".join(L), resumo


def gerar_espelho(payload: dict, saida: Path, skill_peticao: str | None = None,
                  hoje: str | None = None) -> tuple[Path, dict]:
    """Grava `espelho-peticao-<slug>.md` em `saida` e devolve (arquivo, resumo)."""
    if not isinstance(payload.get("achados"), list):
        raise ValueError("payload sem a lista `achados` — o espelho parte dos achados do laudo")
    texto, resumo = espelho(payload, skill_peticao=skill_peticao, hoje=hoje)
    slug = payload.get("identificacao", {}).get("slug", "analise")
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    arquivo = saida / f"espelho-peticao-{slug}.md"
    arquivo.write_text(texto, encoding="utf-8")
    return arquivo, resumo


# ─────────────────────────────────────────────────────────────────────
# autoteste
# ─────────────────────────────────────────────────────────────────────

EMENTA_TESTE = ("RECURSO ESPECIAL. CONTRATO BANCÁRIO. TARIFA DE ABERTURA DE CRÉDITO. "
                "Texto de teste com tamanho suficiente para passar pelo mínimo da ementa integral.")


def _entrada_teste(titulo="STJ · REsp 1/RS", regras="R04", posicao="FAV", tribunal="STJ",
                   url="https://www.jusbrasil.com.br/jurisprudencia/stj/1", verificado="2026-10-27",
                   status="VERIFICADO", ementa=EMENTA_TESTE, extra="") -> str:
    return (f"### {titulo}\n- regras: {regras}\n- posicao: {posicao}\n- tribunal: {tribunal}\n"
            "- classe_numero: REsp 1/RS\n- orgao: Segunda Seção\n- relator: Min. Teste\n"
            "- julgamento: 2013-08-28\n- publicacao: 2013-10-24\n- precedente_qualificado: Tema 618/STJ\n"
            f"- url: {url}\n- verificado_em: {verificado}\n- status: {status}\n"
            f"- uso_na_peca: prova a tese\n- observacao: —\n{extra}ementa:\n> {ementa}\n")


def _testes() -> tuple[int, int]:
    ok = fail = 0

    def chk(nome, cond):
        nonlocal ok, fail
        ok += bool(cond); fail += (not cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {nome}")

    ids = {"R04", "R06", "R13"}
    cab = "## R04 — TAC\n\nTese: TAC indevida.\n\n"
    base = cab + _entrada_teste()
    v = validar(base, ids, hoje="2026-10-27")
    chk("entrada completa valida", not v["erros"] and v["entradas"] == 1)
    chk("cerca de código ignorada", validar("```\n" + base + "```\n", ids, "2026-10-27")["entradas"] == 0)
    chk("julgado fora de seção recusado", any("fora de uma seção" in e for e in validar(
        "```\n" + cab + "```\n" + _entrada_teste() + "\n" + base, ids, "2026-10-27")["erros"]))
    chk("TJ adverso recusado", any("só entra favorável" in e for e in validar(
        cab + _entrada_teste(tribunal="TJPR", posicao="ADV"), ids, "2026-10-27")["erros"]))
    chk("url fora do Jusbrasil recusada", any("fora do Jusbrasil" in e for e in validar(
        cab + _entrada_teste(url="https://exemplo.com/x"), ids, "2026-10-27")["erros"]))
    portal = FONTES_OFICIAIS["TJPR"] + "4100000000000001/Ac%C3%B3rd%C3%A3o-x"
    chk("portal oficial aceito para o próprio tribunal", not validar(
        cab + _entrada_teste(tribunal="TJPR", url=portal), ids, "2026-10-27")["erros"])
    chk("portal do TJPR recusado para outro tribunal", any("fora do Jusbrasil" in e for e in validar(
        cab + _entrada_teste(url=portal), ids, "2026-10-27")["erros"]))
    chk("regra inexistente recusada", any("inexistente" in e for e in validar(
        cab + _entrada_teste(regras="R04, R99"), ids, "2026-10-27")["erros"]))
    chk("ementa curta recusada", any("ementa" in e for e in validar(
        cab + _entrada_teste(ementa="RECURSO ESPECIAL."), ids, "2026-10-27")["erros"]))
    chk("data futura recusada", any("no futuro" in e for e in validar(
        cab + _entrada_teste(verificado="2027-01-01"), ids, "2026-10-27")["erros"]))
    dup = cab + _entrada_teste() + "\n" + _entrada_teste(titulo="STJ · REsp 2/RS")
    chk("julgado repetido recusado", any("repetido" in e for e in validar(dup, ids, "2026-10-27")["erros"]))
    chk("campo desconhecido recusado", any("desconhecido" in e for e in validar(
        cab + _entrada_teste(extra="- relatorx: y\n"), ids, "2026-10-27")["erros"]))
    chk("fora da seção da regra recusado", any("não inclui R04" in e for e in validar(
        cab + _entrada_teste(regras="R06"), ids, "2026-10-27")["erros"]))
    vencida = validar(base, ids, hoje="2028-01-01")
    chk("verificação vencida vira aviso", not any("vencida" in e for e in vencida["erros"])
        and any("vencida" in a for a in vencida["avisos"]))

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        arq = Path(tmp) / "rep.md"
        arq.write_text(base + "\n" + _entrada_teste(
            titulo="TJPR · Apelação 1", tribunal="TJPR", url=PREFIXO_URL + "jurisprudencia/tj-pr/2")
            + "\n" + _entrada_teste(titulo="STJ · REsp 3/RS", status="CONFERIR",
                                    url=PREFIXO_URL + "jurisprudencia/stj/3"), encoding="utf-8")
        c = consultar(["R04", "R13"], hoje="2026-10-27", caminho=arq)
        fav = c["teses"]["R04"]["favoraveis"]
        chk("consulta: só VERIFICADO", len(fav) == 2 and all(e["status"] == "VERIFICADO" for e in fav))
        chk("consulta: STJ antes do TJ", [e["tribunal"] for e in fav] == ["STJ", "TJPR"])
        chk("consulta: CONFERIR vira aviso", any("CONFERIR" in a for a in c["avisos"]))
        chk("consulta: sem cobertura listada", c["sem_cobertura"] == ["R13"])
        chk("consulta: vencida sai", not consultar(["R04"], hoje="2028-01-01", caminho=arq)
            ["teses"]["R04"]["favoraveis"])
        payload = {"titulo": "Teste", "identificacao": {"referencia": "REF-1", "slug": "t",
                                                         "campos": [["Contrato", "CCB", "instrumento"]]},
                   "achados": [{"id": "A1", "tier": "T1", "resultado": "Ilícito", "titulo": "TAC",
                                "detalhe": "cobrada", "fundamento": "Súmula 565/STJ", "regras": ["R04"]},
                               {"id": "A2", "tier": "T2", "resultado": "Conforme", "titulo": "IOF",
                                "detalhe": "ok", "fundamento": "—", "regras": ["R25"]},
                               {"id": "A3", "tier": "T1", "resultado": "A verificar", "titulo": "Seguro",
                                "detalhe": "?", "fundamento": "—"}],
                   "lacunas": ["extrato ausente"]}
        md, resumo = espelho(payload, hoje="2026-10-27", caminho=arq)
        chk("espelho: ementa e fonte presentes", EMENTA_TESTE in md and PREFIXO_URL + "jurisprudencia/stj/1" in md)
        chk("espelho: achado pró-banco fora", "IOF" not in md)
        chk("espelho: CONFERIR não citado", "jurisprudencia/stj/3" not in md)
        chk("espelho: achado sem regra é pendência", any("A3 sem regra" in s for s in resumo["sem_jurisprudencia"]))
        chk("espelho: perícia e exibição", "Perícia contábil" in md and "art. 396" in md)
        chk("espelho: formato neutro sem skill", "neutro" in md)
        md2, _ = espelho(payload, skill_peticao="peticoes-escritorio", hoje="2026-10-27", caminho=arq)
        chk("espelho: skill canônica nomeada", "`peticoes-escritorio`" in md2)
    turma = {"tribunal": "STJ", "orgao": "Terceira Turma", "precedente_qualificado": "não",
             "julgamento": "2026-06-15"}
    secao = {"tribunal": "STJ", "orgao": "Corte Especial", "precedente_qualificado": "não (embargos)",
             "julgamento": "2020-10-21"}
    chk("ordem: órgão uniformizador antes de Turma mais recente", sorted([turma, secao], key=_ordem)[0] is secao)
    chk("qualificado: 'não (…)' não conta", not _qualificado({"precedente_qualificado": "não (embargos)"})
        and _qualificado({"precedente_qualificado": "Tema 52/STJ"}))

    real = validar()
    chk(f"repertório do plugin sem erros ({real['entradas']} entradas)", not real["erros"])
    for e in real["erros"][:10]:
        print(f"        {e}")
    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("jurisprudencia", _testes, verbose)
