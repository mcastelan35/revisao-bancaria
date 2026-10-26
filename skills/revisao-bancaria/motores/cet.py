"""
cet.py — Custo efetivo real e auditoria do CET declarado
Sub-módulo determinístico do plugin `revisao-bancaria`.

PARA QUE SERVE
--------------
O `calculo.py` compara TAXA CONTRATADA contra TAXA MÉDIA BACEN — é o eixo do
excesso. Este módulo cobre um eixo diferente e independente: o CUSTO EFETIVO
REALMENTE PRATICADO contra o CUSTO EFETIVO INFORMADO ao tomador.

Ele resolve três casos que o `calculo.py` não cobre:

  1. Operação PÓS-FIXADA (CDI, TR, IPCA, SELIC). O saldo não decorre de uma taxa
     fixa: decorre do fator acumulado do indexador multiplicado pelo fator do
     spread. Reconstruir isso exige a série diária do SGS/BACEN.
  2. Auditoria do CET (Res. CMN 4.881/2020). O demonstrativo anexo ao instrumento
     frequentemente omite o indexador, usa base divergente do valor do título ou
     informa spread diferente do pactuado. Isso é achado autônomo, independente
     de haver ou não excesso no saldo.
  3. Contrato em que o SALDO CONFERE. Quando a reconstrução bate com o apurado
     pelo credor, não há excesso a decotar — mas pode haver vício informacional
     de ordem de grandeza. Sem este módulo a skill não tem o que dizer nesses casos.

REGRA 0 (proibição de presunção) VALE AQUI TAMBÉM
-------------------------------------------------
A série do indexador vem do SGS/BACEN (ver `referencia/bacen-consulta.md`). O spread, a
convenção e as datas vêm do instrumento. Nada é estimado. Se a série não cobre o
período, é lacuna bloqueante — não interpolar.

CONVENÇÃO
---------
Padrão do mercado bancário brasileiro para pós-fixado em CDI: capitalização
diária do fator do indexador sobre DIAS ÚTEIS, e spread convertido na base
dias_uteis/252. A convenção é parâmetro explícito, nunca implícita.

Executar `python3 revisao.py autoteste --modulo cet` roda a suíte de autoteste embutida.
"""

from __future__ import annotations

import json
import re

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from decimal import Decimal as D, ROUND_HALF_UP, getcontext

from .comum import brl, brl_rs, pct, pt, rodar_autoteste, saida_utf8  # formatação pt-BR única para todos os motores

getcontext().prec = 28

BASE_DU = D(252)
TOLERANCIA_CET_REL = D("0.05")   # CET-01: divergência relativa tolerada entre CET declarado e esperado ex-ante


def _ultimo_dia_util_civil_antes(d: date) -> date:
    """Último dia de segunda a sexta ESTRITAMENTE anterior a `d` (sem feriados — quem
    sabe de feriado é a série SGS). É a ponta que a reconstrução semiaberta precisa."""
    d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


# ─────────────────────────────────────────────────────────────────────
# 1. SÉRIE DO INDEXADOR
# ─────────────────────────────────────────────────────────────────────

def carregar_serie_sgs(registros: list[dict]) -> dict[date, D]:
    """Converte o JSON cru do SGS/BACEN em {data: fator_diario_decimal}.

    registros: [{"data": "18/07/2025", "valor": "0.055131"}, ...]
               O SGS devolve a taxa diária JÁ em percentual ao dia.
    Séries diárias do SGS publicam apenas dias úteis — a própria série define o
    calendário. Não montar calendário próprio nem preencher feriado.
    """
    if not registros:
        raise ValueError("série vazia: lacuna bloqueante, não estimar indexador")
    serie: dict[date, D] = {}
    for r in registros:
        d = datetime.strptime(r["data"], "%d/%m/%Y").date()
        serie[d] = D(str(r["valor"])) / D(100)
    return serie


def carregar_de_consultar_indice(resposta: dict | str) -> dict[date, D]:
    """Adaptador para a tool `consultar_indice` do conector Radar Apogeu.

    A tool devolve JSON com `pontos` já no formato do SGS, mais `fator_acumulado`
    e `variacao_acumulada_pct` — use `conferir_fator()` para cruzar a reconstrução
    contra o fator do conector antes de assinar qualquer laudo.

    A identidade da série está em `cabecalho.serie.nome` (e `unidade`,
    `periodicidade`, `segmento`) — não em `serie.nome`.

    Alternativa a `consultar_taxa_bacen` com `pontos="completos"`, que devolve a
    mesma série e o mesmo `fator_acumulado` num payload mais enxuto.
    """
    if isinstance(resposta, str):
        resposta = json.loads(resposta)
    pontos = resposta.get("pontos")
    if not pontos:
        raise ValueError("resposta do conector sem pontos: lacuna bloqueante, não estimar")
    return carregar_serie_sgs(pontos)


def carregar_de_consultar_taxa_bacen(resposta: dict | str) -> dict[date, D]:
    """Adaptador para a tool `consultar_taxa_bacen` do conector Radar Apogeu.

    A tool serve do CACHE PERSISTENTE do conector (rápida e resiliente, cai no
    SGS ao vivo só para o que faltar) e devolve dois canais: um texto formatado
    (`  18/07/2025: 0.055131` por linha) e um payload estruturado. Este adaptador
    aceita os dois — passe o dicionário quando tiver, o texto quando só houver
    texto.

    RECORTE DE TEXTO — a razão de existir a checagem abaixo. No modo padrão
    (`pontos: "resumo"`) o texto lista no máximo 60 pontos e marca a omissão.
    Um produtório calculado sobre esse recorte sai errado sem nenhum outro
    sintoma: `cobertura()` e `verificar_ponta_da_serie()` PASSAM, porque o corte
    preserva justamente o primeiro e o último ponto. Por isso o recorte aqui é
    erro duro, não aviso.

    Para série diária de indexador, chame a tool com `pontos: "completos"`.
    """
    if isinstance(resposta, dict):
        # Aceita tanto o payload já desempacotado quanto o envelope MCP cru
        # ({content: [{type: 'text', text: ...}], structuredContent: {...}}) —
        # passar o envelope inteiro é o que um agente faz naturalmente.
        envelope = resposta
        estruturado = envelope.get("structuredContent")
        if isinstance(estruturado, dict):
            resposta = estruturado

        # Payload estruturado: em modo 'resumo' a série íntegra está em `dados`;
        # em 'completos' ela está no texto e `dados` não vem.
        pontos = resposta.get("dados")
        if pontos:
            return carregar_serie_sgs(pontos)

        texto = resposta.get("texto") or resposta.get("text") or ""
        if not texto:
            conteudo = envelope.get("content")
            if isinstance(conteudo, list):
                texto = "".join(
                    bloco.get("text", "")
                    for bloco in conteudo
                    if isinstance(bloco, dict) and bloco.get("type") == "text"
                )
        if not texto:
            raise ValueError(
                "resposta do conector sem pontos: lacuna bloqueante, não estimar"
            )
    else:
        texto = resposta

    if "OMITIDOS DESTE TEXTO" in texto or "pontos omitidos" in texto:
        raise ValueError(
            "resposta do conector RECORTADA: o texto lista só parte dos pontos. "
            "Nenhum produtório calculado sobre ele vale. Rechame "
            'consultar_taxa_bacen com pontos="completos" (ou use consultar_indice).'
        )

    serie: dict[date, D] = {}
    for m in re.finditer(r"(\d{2}/\d{2}/\d{4})\s*:\s*([-\d.,]+)", texto):
        d = datetime.strptime(m.group(1), "%d/%m/%Y").date()
        serie[d] = D(m.group(2).replace(",", ".")) / D(100)
    if not serie:
        raise ValueError("nenhum ponto reconhecido na resposta do conector: "
                         "lacuna bloqueante, não estimar")

    # Segunda rede: o conector informa quantos pontos existem na janela. Se a
    # contagem não bate com o que foi parseado, a série está incompleta.
    if isinstance(resposta, dict):
        total = resposta.get("pontos_total")
        if isinstance(total, int) and total != len(serie):
            raise ValueError(
                f"série incompleta: o conector reporta {total} ponto(s) na janela "
                f"e só {len(serie)} foram lidos. Rechame com pontos=\"completos\"."
            )
    return serie


def carregar_de_linhas(linhas: list[dict]) -> dict[date, D]:
    """Adaptador genérico para série já tabulada em lista de dicionários.

    Aceita a chave de data como `data` ou `data_ponto`, em `dd/mm/aaaa` ou `aaaa-mm-dd`.
    Serve para reaproveitar série que o usuário forneça em planilha ou que venha de
    ferramenta auxiliar.

    NÃO é um caminho de obtenção de dado. A fonte da série continua sendo o conector —
    ver `referencia/bacen-consulta.md`. Usar este adaptador com dado de origem não declarada é
    violação da regra 0.
    """
    if not linhas:
        raise ValueError("série vazia: lacuna bloqueante, não estimar")
    serie: dict[date, D] = {}
    for r in linhas:
        bruto = r.get("data_ponto") or r.get("data")
        if bruto is None:
            raise ValueError("linha do cache sem data: " + repr(r))
        b = str(bruto)
        d = (datetime.strptime(b, "%Y-%m-%d").date() if "-" in b
             else datetime.strptime(b, "%d/%m/%Y").date())
        serie[d] = D(str(r["valor"])) / D(100)
    return serie


def verificar_ponta_da_serie(ultimo_ponto: date, data_base: date,
                             tolerancia_dias: int = 0) -> dict:
    """Confere se a série devolvida pelo conector alcança a data-base da apuração.

    A `consultar_taxa_bacen` serve do cache do conector e completa ao vivo o que
    faltar, mas a ponta da série pode não chegar à data-base — o SGS publica com
    atraso, e feriado ou indisponibilidade encurtam o período retornado.

    Faltando dias, é LACUNA BLOQUEANTE: reconsultar, ou recuar a data-base para o
    último ponto efetivamente disponível e declarar isso na metodologia. Jamais
    truncar em silêncio nem repetir o último fator para os dias faltantes.

    CRITÉRIO — o mesmo de `cobertura()`. O conector reporta `ponta.alcanca_data_final`
    contra `data_final` INCLUSIVE (existe ponto publicado para a própria data?). O
    motor precisa de menos: a reconstrução é semiaberta `[liberacao, data_base)` (ver
    `dias_uteis()`), então a ponta necessária é o último dia útil civil (seg-sex)
    estritamente anterior à data-base — série que termina na sexta cobre data-base
    na segunda. `cobre` e `dias_faltantes` seguem o critério do motor;
    `alcanca_data_base` e `dias_ate_data_base` conservam o critério do conector,
    para conferência cruzada com o que ele reportou.
    """
    necessaria = _ultimo_dia_util_civil_antes(data_base)
    falta = (necessaria - ultimo_ponto).days
    return {"ultimo_ponto": ultimo_ponto, "data_base": data_base,
            "ponta_necessaria": necessaria,
            "dias_faltantes": max(falta, 0),
            "dias_ate_data_base": max((data_base - ultimo_ponto).days, 0),
            "alcanca_data_base": ultimo_ponto >= data_base,
            "cobre": falta <= tolerancia_dias,
            "acao": ("cache suficiente" if falta <= tolerancia_dias else
                     f"completar {falta} dia(s) pelo caminho ao vivo "
                     f"(ponta necessária: {necessaria.strftime('%d/%m/%Y')})")}


def conferir_fator(serie: dict[date, D],
                   fator_conector: D | float | str,
                   inicio: date | None = None, fim: date | None = None,
                   tolerancia: D | float | str | None = None,
                   tolerancia_rel: D | float | str = D("1e-7"),
                   casas_conector: int | None = None) -> dict:
    """Cruza o produtório local com o `fator_acumulado` devolvido pelo conector.

    TOLERÂNCIA. O conector devolve o fator com um número finito de casas, então a
    comparação é RELATIVA (`tolerancia_rel`, padrão 1e-7) — uma tolerância absoluta
    fixa acusa divergência falsa em fator grande arredondado. Quando se sabe em
    quantas casas o conector publica, informe `casas_conector`: o produtório local é
    quantizado (HALF_UP) nessas casas antes da comparação, e o resultado traz
    `local_comparado`. `tolerancia` (absoluta) é legado e, se informada, prevalece.

    O QUE ESTA FUNÇÃO CONFERE: que a série carregada é exatamente a série que o
    conector serviu. É a guarda que pega os dois modos de falha silenciosa —
    série lida pela metade (texto recortado) e calendário divergente (feriado,
    chunking). `cobertura()` e `verificar_ponta_da_serie()` NÃO pegam nenhum dos
    dois: o recorte preserva justamente o primeiro e o último ponto.

    INTERVALO FECHADO, de propósito. O `fator_acumulado` do conector é o
    produtório de TODOS os pontos da janela `[data_inicial, data_final]` que ele
    devolveu. Por isso o padrão aqui é a série inteira, e um intervalo informado
    é fechado nas duas pontas. Não confundir com `dias_uteis()`, que é
    semiaberto `[inicio, fim)` — essa é a convenção do CDI para a reconstrução
    financeira, e comparar uma contra a outra acusa divergência de um dia em
    todo contrato cuja data-base caia em dia útil publicado.

    Rodar SEMPRE que o fator estiver disponível — as duas tools do conector o
    devolvem, então não custa chamada extra.
    """
    if isinstance(fator_conector, date):
        raise TypeError(
            "conferir_fator mudou de assinatura: agora é "
            "conferir_fator(serie, fator_conector, inicio=None, fim=None). "
            "O intervalo é FECHADO e opcional — o padrão é a série inteira, que "
            "é o que o fator_acumulado do conector cobre."
        )
    datas = janela_fechada(serie, inicio, fim)
    local = fator_indexador(serie, datas)
    remoto = D(str(fator_conector))
    local_cmp = local
    if casas_conector is not None:
        if casas_conector < 0:
            raise ValueError(f"casas_conector inválido: {casas_conector}")
        local_cmp = local.quantize(D(1).scaleb(-casas_conector), rounding=ROUND_HALF_UP)
    dif = abs(local_cmp - remoto)
    dif_rel = (dif / abs(remoto)) if remoto else dif
    if tolerancia is not None:                      # legado: absoluta
        confere = dif <= D(str(tolerancia))
    else:
        confere = dif_rel <= D(str(tolerancia_rel))
    return {"local": local, "local_comparado": local_cmp, "conector": remoto,
            "diferenca": dif, "diferenca_rel": dif_rel,
            "confere": confere,
            "tolerancia_rel": None if tolerancia is not None else D(str(tolerancia_rel)),
            "tolerancia_abs": None if tolerancia is None else D(str(tolerancia)),
            "casas_conector": casas_conector,
            "pontos": len(datas),
            "primeiro": datas[0] if datas else None,
            "ultimo": datas[-1] if datas else None}


def janela_fechada(serie: dict[date, D], inicio: date | None = None,
                   fim: date | None = None) -> list[date]:
    """Datas da série no intervalo FECHADO [inicio, fim]; padrão, a série toda.

    É a janela que o conector usa para o `fator_acumulado`. Para a reconstrução
    financeira do CDI use `dias_uteis()`, que é semiaberto.
    """
    return sorted(k for k in serie
                  if (inicio is None or k >= inicio) and (fim is None or k <= fim))


def dias_uteis(serie: dict[date, D], inicio: date, fim: date) -> list[date]:
    """Dias úteis no intervalo SEMIABERTO [inicio, fim) — convenção de RECONSTRUÇÃO.

    Semiaberta à direita porque, na reconstrução de saldo, o encargo do dia do
    vencimento é acumulado ANTES do abatimento do pagamento: o dia final entra
    pela mão do pagamento, não pela do encargo.

    NÃO use esta função para auditar fator declarado pelo credor num intervalo
    que ele mesmo anunciou como fechado — use `dias_uteis_fechado()`. Misturar
    as duas produz dois números para a mesma grandeza. Ver `auditar_fator_declarado()`.
    """
    if fim < inicio:
        raise ValueError(f"intervalo invertido: {inicio} .. {fim}")
    return sorted(k for k in serie if inicio <= k < fim)


def dias_uteis_fechado(serie: dict[date, D], inicio: date, fim: date) -> list[date]:
    """Dias úteis no intervalo FECHADO [inicio, fim] — convenção de AUDITORIA.

    É a convenção que reproduz o `fator_acumulado` devolvido pelo conector para a
    janela consultada, e portanto a única cabível quando se confronta o fator que o
    credor declarou ter aplicado contra a série oficial no intervalo por ele indicado.
    """
    if fim < inicio:
        raise ValueError(f"intervalo invertido: {inicio} .. {fim}")
    return sorted(k for k in serie if inicio <= k <= fim)


def auditar_fator_declarado(serie: dict[date, D], inicio: date, fim: date,
                            fator_declarado: D | float,
                            fator_conector: D | float | None = None) -> dict:
    """Confronta o fator de indexação que o credor aplicou contra a série oficial.

    Apura nas DUAS convenções e adota a de menor excesso, porque impugnação que
    escolhe sistematicamente a leitura mais favorável ao credor e ainda assim
    encontra erro é muito mais difícil de rebater. A convenção adotada e a
    descartada vão as duas ao relatório — a divergência entre elas é dado de
    metodologia, não ruído a esconder.

    `fator_conector`, quando informado, prevalece sobre o produtório local na
    convenção fechada: é a fonte autoritativa, e a conferência entre ambos é a
    guarda contra série carregada pela metade.
    """
    fator_declarado = D(str(fator_declarado))
    f_fech = D(str(fator_conector)) if fator_conector is not None else \
        fator_indexador(serie, dias_uteis_fechado(serie, inicio, fim))
    f_semi = fator_indexador(serie, dias_uteis(serie, inicio, fim))
    exc_fech = fator_declarado / f_fech - D(1)
    exc_semi = fator_declarado / f_semi - D(1)
    adotada = "fechada" if abs(exc_fech) <= abs(exc_semi) else "semiaberta"
    excesso = exc_fech if adotada == "fechada" else exc_semi
    return {"fator_declarado": fator_declarado,
            "fator_janela_fechada": f_fech, "fator_janela_semiaberta": f_semi,
            "excesso_fechada": exc_fech, "excesso_semiaberta": exc_semi,
            "convencao_adotada": adotada, "excesso": excesso,
            "pontos_fechada": len(dias_uteis_fechado(serie, inicio, fim)),
            "pontos_semiaberta": len(dias_uteis(serie, inicio, fim)),
            "confere": abs(excesso) <= D("0.0001"),
            "veredito": "CONFORME" if abs(excesso) <= D("0.0001") else "DIVERGENTE",
            "fonte_fechada": "conector" if fator_conector is not None else "produtório local"}


def cobertura(serie: dict[date, D], inicio: date, fim: date,
              pontos_esperados: int | None = None) -> dict:
    """Verifica se as PONTAS da série cobrem o período.

    ATENÇÃO AO QUE ELA NÃO FAZ: compara apenas `min(serie)` e `max(serie)`, então
    uma série com buraco no MIOLO passa como "cobertura integral". Quem detecta
    lacuna interna é `conferir_fator()`, cruzando o produtório local contra o
    `fator_acumulado` do conector — rode sempre as duas.

    `pontos_esperados` (o `pontos_total` que o conector devolve) fecha essa
    brecha quando disponível: contagem divergente vira falha de cobertura.

    PONTA FINAL. A reconstrução só usa pontos `< fim` (`dias_uteis()` é semiaberta),
    então a série NÃO precisa ter ponto em `fim`: basta alcançar o último dia útil
    civil (seg-sex) estritamente anterior a `fim`. Série que termina na sexta cobre
    data-base na segunda. O conector reporta a ponta contra `data_final` inclusive —
    ver `verificar_ponta_da_serie()` para a correspondência entre os dois critérios.
    (Feriado na véspera da data-base torna o critério civil conservador: acusa falta
    de um ponto que a série oficial não publica — bloqueia, não passa.)

    Falha de cobertura é lacuna bloqueante — não interpolar, não estimar.
    """
    if not serie:
        return {"cobre": False, "motivo": "série vazia"}
    ini_s, fim_s = min(serie), max(serie)
    fim_necessario = _ultimo_dia_util_civil_antes(fim)
    faltas = []
    if inicio < ini_s:
        faltas.append(f"série começa em {ini_s.strftime('%d/%m/%Y')}, "
                      f"após o início do período ({inicio.strftime('%d/%m/%Y')})")
    if fim_necessario > fim_s:
        faltas.append(f"série termina em {fim_s.strftime('%d/%m/%Y')}, "
                      f"antes do fim do período ({fim.strftime('%d/%m/%Y')}) — a "
                      f"reconstrução exige pontos até {fim_necessario.strftime('%d/%m/%Y')}, "
                      f"último dia útil civil anterior à data-base")
    if pontos_esperados is not None and pontos_esperados != len(serie):
        faltas.append(f"o conector reporta {pontos_esperados} ponto(s) na janela e "
                      f"a série carregada tem {len(serie)} — lacuna no miolo")
    return {"cobre": not faltas, "motivo": "; ".join(faltas) or "cobertura das pontas OK",
            "primeira": ini_s, "ultima": fim_s, "ponta_necessaria": fim_necessario,
            "pontos": len(serie),
            "detecta_lacuna_interna": pontos_esperados is not None}


# ─────────────────────────────────────────────────────────────────────
# 2. FATORES
# ─────────────────────────────────────────────────────────────────────

def fator_indexador(serie: dict[date, D], datas: list[date]) -> D:
    """Produtório de (1 + taxa_do_dia) sobre os dias úteis informados."""
    f = D(1)
    for d in datas:
        f *= (D(1) + serie[d])
    return f


def fator_spread(spread_aa: D | float, n_du: int, base: D = BASE_DU) -> D:
    """Fator do spread na convenção dias úteis / 252."""
    s = D(str(spread_aa))
    if s < 0:
        raise ValueError("spread negativo")
    if n_du < 0:
        raise ValueError("número de dias úteis negativo")
    return (D(1) + s) ** (D(n_du) / base)


def anualizar(fator: D, n_du: int, base: D = BASE_DU) -> D:
    """Converte fator acumulado em taxa efetiva ao ano."""
    if n_du <= 0:
        raise ValueError("não é possível anualizar sobre zero dia útil")
    return fator ** (base / D(n_du)) - D(1)


def spread_mensal_para_anual(r_mensal: D | float) -> D:
    """0,25% a.m. capitalizado -> 3,041596% a.a. Usado para conferir o duodécuplo."""
    return (D(1) + D(str(r_mensal))) ** 12 - D(1)


def compor_aa(indexador_aa: D | float, spread_aa: D | float) -> D:
    """Composição de taxas efetivas anuais: (1 + indexador)·(1 + spread) − 1.
    É o CET esperado ex-ante de um pós-fixado (Res. CMN 4.881/2020: calculado com o
    indexador vigente na contratação), e a taxa contratual composta da mora."""
    return (D(1) + D(str(indexador_aa))) * (D(1) + D(str(spread_aa))) - D(1)


# ─────────────────────────────────────────────────────────────────────
# 3. RECONSTRUÇÃO DO SALDO PÓS-FIXADO
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Pagamento:
    data: date
    valor: D

    def __post_init__(self):
        self.valor = D(str(self.valor))


def _alocar_pagamentos(serie: dict[date, D], liberacao: date, data_base: date,
                       pagamentos: list[Pagamento]) -> tuple[dict[date, D], D, list[dict]]:
    """Aloca os pagamentos ao calendário de dias úteis da reconstrução.

    Devolve `(por_dia, no_fim, deslocados)`:
      por_dia    — {dia_util: valor} com pagamentos AGREGADOS por data (dois no mesmo
                   dia somam; nunca se sobrescrevem);
      no_fim     — soma dos pagamentos com data na data-base ou entre o último dia
                   útil processado e a data-base. A reconstrução é semiaberta
                   (`dias_uteis()`), então esses pagamentos são abatidos NO FIM,
                   sobre o saldo do último dia, sem encargo daquele dia;
      deslocados — [{"data_original", "data_aplicada", "valor", "motivo"}]: pagamento
                   em dia que não é dia útil da série (sábado, domingo, feriado) vai
                   para o PRÓXIMO dia útil da série, e pagamento do bloco `no_fim` é
                   registrado contra o último dia útil processado.

    Pagamento fora de [liberacao, data_base] é ValueError — não há onde lançá-lo.
    """
    dus = dias_uteis(serie, liberacao, data_base)
    por_dia: dict[date, D] = {}
    no_fim = D(0)
    deslocados: list[dict] = []
    for p in pagamentos:
        if p.data < liberacao or p.data > data_base:
            raise ValueError(
                f"pagamento de {brl_rs(p.valor)} em {p.data.strftime('%d/%m/%Y')} fora do "
                f"período [{liberacao.strftime('%d/%m/%Y')}, {data_base.strftime('%d/%m/%Y')}]")
        alvo = next((d for d in dus if d >= p.data), None)
        if alvo is None:
            no_fim += p.valor
            deslocados.append({
                "data_original": p.data, "data_aplicada": dus[-1] if dus else None,
                "valor": p.valor,
                "motivo": "na data-base ou após o último dia útil processado — abatido no fim, "
                          "sobre o saldo do último dia útil, sem encargo do dia"})
            continue
        por_dia[alvo] = por_dia.get(alvo, D(0)) + p.valor
        if alvo != p.data:
            deslocados.append({
                "data_original": p.data, "data_aplicada": alvo, "valor": p.valor,
                "motivo": "data não é dia útil da série — deslocado para o próximo dia útil"})
    return por_dia, no_fim, deslocados


@dataclass
class ReconstrucaoPosFixada:
    """Reconstrói, dia útil a dia útil, a evolução do saldo de uma operação
    indexada, e devolve a memória completa para o demonstrativo.

    Convenção de amortização: os encargos do DIA do vencimento são acumulados
    ANTES de abater o pagamento. Fixar isso é obrigatório — apurar de outro modo
    produz divergência de dezenas de reais e dois números para a mesma grandeza.

    Pagamentos (ver `_alocar_pagamentos`): agregados por data; em dia não útil da
    série vão para o próximo dia útil (a linha recebe `data_original` e o objeto
    lista `pagamentos_deslocados`); na data-base são abatidos sobre o saldo do
    último dia útil, sem encargo do dia; fora do período, ou acima do saldo, é
    ValueError — nunca saldo negativo em silêncio.

    Memória: em toda linha, `saldo_anterior + encargo_indexador + encargo_spread
    − amortizacao == saldo`. O spread incide sobre o saldo JÁ corrigido pelo
    indexador no dia (é a ordem do próprio cálculo `saldo·(1+i)·f_dia`), por isso
    `encargo_spread = saldo·(1+i)·(f_dia − 1)` — sem o termo cruzado a soma das
    rubricas não fecha com o crescimento do saldo.
    """
    principal: D
    liberacao: date
    data_base: date
    spread_aa: D
    serie: dict[date, D] = field(default_factory=dict)
    pagamentos: list[Pagamento] = field(default_factory=list)
    linhas: list[dict] = field(default_factory=list)
    pagamentos_deslocados: list[dict] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.principal = D(str(self.principal))
        self.spread_aa = D(str(self.spread_aa))
        if self.principal <= 0:
            raise ValueError(f"principal inválido: {self.principal}")
        cob = cobertura(self.serie, self.liberacao, self.data_base)
        if not cob["cobre"]:
            raise ValueError(f"série do indexador não cobre o período — {cob['motivo']}. "
                             "Lacuna bloqueante (regra 0): obter a série, não estimar.")
        pg, no_fim, self.pagamentos_deslocados = _alocar_pagamentos(
            self.serie, self.liberacao, self.data_base, self.pagamentos)
        orig: dict[date, date] = {}          # dia aplicado -> data original mais antiga
        for x in self.pagamentos_deslocados:
            if x["data_aplicada"] is not None:
                orig[x["data_aplicada"]] = min(orig.get(x["data_aplicada"], x["data_original"]),
                                               x["data_original"])
        f_dia = fator_spread(self.spread_aa, 1)
        saldo = self.principal
        for d in dias_uteis(self.serie, self.liberacao, self.data_base):
            i = self.serie[d]
            anterior = saldo
            enc_idx = saldo * i
            enc_spr = saldo * (D(1) + i) * (f_dia - D(1))
            saldo = saldo * (D(1) + i) * f_dia
            amort = pg.get(d, D(0))
            if amort > saldo:
                raise ValueError(
                    f"pagamento excede o saldo em {d.strftime('%d/%m/%Y')}: pagamento "
                    f"{brl_rs(amort)} contra saldo (após encargos do dia) {brl_rs(saldo)}")
            saldo -= amort
            self.linhas.append({
                "data": d, "data_original": orig.get(d), "taxa_dia": i,
                "saldo_anterior": anterior, "encargo_indexador": enc_idx,
                "encargo_spread": enc_spr, "amortizacao": amort, "saldo": saldo,
            })
        if not self.linhas:
            raise ValueError("nenhum dia útil no período — verificar datas")
        if no_fim:
            ult = self.linhas[-1]
            if no_fim > ult["saldo"]:
                raise ValueError(
                    f"pagamento excede o saldo em {self.data_base.strftime('%d/%m/%Y')}: "
                    f"pagamento {brl_rs(no_fim)} contra saldo {brl_rs(ult['saldo'])}")
            ult["saldo"] -= no_fim
            ult["amortizacao"] += no_fim

    @property
    def n_du(self) -> int:
        return len(self.linhas)

    @property
    def saldo_final(self) -> D:
        return self.linhas[-1]["saldo"]

    @property
    def total_amortizado(self) -> D:
        return sum((l["amortizacao"] for l in self.linhas), D(0))

    @property
    def fator_indexador_periodo(self) -> D:
        return fator_indexador(self.serie, [l["data"] for l in self.linhas])

    @property
    def indexador_aa(self) -> D:
        return anualizar(self.fator_indexador_periodo, self.n_du)

    @property
    def custo_efetivo_aa(self) -> D:
        f = self.fator_indexador_periodo * fator_spread(self.spread_aa, self.n_du)
        return anualizar(f, self.n_du)


def conferir_saldo(reconstruido: D, apurado_credor: D,
                   tolerancia_pct: D | float = 0.5) -> dict:
    """Confronta a reconstrução com o saldo apurado pelo credor.

    A skill NÃO parte do pressuposto de que há excesso. Quando o saldo confere,
    dizer isso de forma destacada é o que dá credibilidade ao que vem depois.

    Saldo apurado ausente ou zero é LACUNA, não "CONFORME": sem o número do credor
    não há o que confrontar.
    """
    reconstruido, apurado_credor = D(str(reconstruido)), D(str(apurado_credor))
    if apurado_credor <= 0:
        raise ValueError("saldo apurado pelo credor ausente ou zero — lacuna bloqueante "
                         "(regra 0): obter o saldo do credor, não presumir conformidade")
    dif = apurado_credor - reconstruido
    dif_pct = dif / apurado_credor * D(100)
    tol = D(str(tolerancia_pct))
    return {"reconstruido": reconstruido, "apurado_credor": apurado_credor,
            "diferenca": dif, "diferenca_pct": dif_pct,
            "confere": abs(dif_pct) <= tol,
            "veredito": "CONFORME" if abs(dif_pct) <= tol else "DIVERGENTE"}


# ─────────────────────────────────────────────────────────────────────
# 4. AUDITORIA DO CET DECLARADO (Res. CMN 4.881/2020)
# ─────────────────────────────────────────────────────────────────────

@dataclass
class CETDeclarado:
    """Dados extraídos do demonstrativo de CET anexo ao instrumento.
    Todo campo vem do documento. Campo ausente fica None e vira lacuna."""
    cet_aa: D | None = None
    cet_am: D | None = None
    encargos_aa: D | None = None
    encargos_am: D | None = None
    base_calculo: D | None = None
    total_devido: D | None = None
    iof_total: D | None = None

    def __post_init__(self):
        for k, v in list(self.__dict__.items()):
            if v is not None:
                setattr(self, k, D(str(v)))


def auditar_cet(declarado: CETDeclarado, custo_real_aa: D,
                valor_do_titulo: D, spread_contratual_am: D | None = None,
                iof_documento_descritivo: D | None = None,
                indexador_aa_na_contratacao: D | float | None = None,
                spread_aa: D | float | None = None) -> dict:
    """Confronta o CET declarado com o custo efetivo apurado e com o instrumento.

    Devolve os achados JÁ classificados. Cada achado carrega o fundamento —
    o relatório só transcreve.

    CET-01 — EX-ANTE, não ex-post. Em pós-fixado o CET é calculado com o indexador
    vigente na contratação (Res. CMN 4.881/2020); o custo realizado depende do
    indexador que veio depois e NÃO serve para acusar o CET declarado. Por isso:
      • com `indexador_aa_na_contratacao` e `spread_aa`, o CET esperado é
        `compor_aa(indexador, spread)` e a divergência relativa acima de
        `TOLERANCIA_CET_REL` (5%) é CET-01 `Ilícito` T1;
      • sem eles, CET-01 nunca é "Ilícito": custo ex-post ≥ 1,15× o CET declarado
        vira `A verificar` T2, e a ausência do indexador é registrada em `lacunas`.
    `custo_real_aa` zero (reconstrução não feita) também é lacuna, não silêncio.
    """
    custo_real_aa = D(str(custo_real_aa))
    valor_do_titulo = D(str(valor_do_titulo))
    achados, lacunas = [], []
    tem_ex_ante = indexador_aa_na_contratacao is not None and spread_aa is not None
    cet_esperado = compor_aa(indexador_aa_na_contratacao, spread_aa) if tem_ex_ante else None
    div_ex_ante = None
    if (indexador_aa_na_contratacao is None) != (spread_aa is None):
        lacunas.append("indexador na contratação e spread anual devem ser informados JUNTOS "
                       "para auditar o CET ex-ante — só um deles foi informado")
    if custo_real_aa <= 0:
        lacunas.append("custo efetivo apurado ex-post ausente ou zero — reconstrução do saldo "
                       "não realizada; a comparação ex-post do CET-01 não foi feita")

    if declarado.cet_aa is None:
        lacunas.append("CET anual não consta do demonstrativo anexo")
        razao = None
    else:
        razao = ((custo_real_aa / declarado.cet_aa)
                 if (declarado.cet_aa and custo_real_aa > 0) else None)
        if tem_ex_ante:
            div_ex_ante = (abs(declarado.cet_aa - cet_esperado) / cet_esperado
                           if cet_esperado else None)
            if div_ex_ante is not None and div_ex_ante > TOLERANCIA_CET_REL:
                achados.append({
                    "id": "CET-01", "tier": "T1", "resultado": "Ilícito",
                    "titulo": "CET declarado incompatível com o custo esperado na contratação",
                    "medida": pct(div_ex_ante * 100, 2),
                    "detalhe": (f"CET declarado de {pct(declarado.cet_aa * 100, 4)} a.a. contra "
                                f"CET esperado ex-ante de {pct(cet_esperado * 100, 4)} a.a. — "
                                f"indexador vigente na contratação de "
                                f"{pct(D(str(indexador_aa_na_contratacao)) * 100, 4)} a.a. "
                                f"composto com spread de {pct(D(str(spread_aa)) * 100, 4)} a.a. "
                                f"(divergência relativa de {pct(div_ex_ante * 100, 2)}; "
                                f"tolerância {pct(TOLERANCIA_CET_REL * 100, 0)})."
                                + (f" Custo efetivo apurado ex-post: "
                                   f"{pct(custo_real_aa * 100, 4)} a.a." if custo_real_aa > 0 else "")),
                    "fundamento": ("Resolução CMN 4.881/2020; art. 28, §2º, I, 'd', da Lei "
                                   "10.931/2004; art. 422 do Código Civil."),
                })
        else:
            lacunas.append("indexador vigente na contratação não informado — CET-01 não pode "
                           "ser afirmado como ilícito (Res. CMN 4.881/2020: em pós-fixado o CET "
                           "é calculado com o indexador da contratação); a comparação ex-post "
                           "é apenas indicativa")
            if razao is not None and razao >= D("1.15"):
                achados.append({
                    "id": "CET-01", "tier": "T2", "resultado": "A verificar",
                    "titulo": "Custo efetivo ex-post muito acima do CET declarado — "
                              "exige o indexador da contratação para concluir",
                    "medida": pt(f"{razao:.2f}") + "x",
                    "detalhe": (f"custo efetivo apurado ex-post de {pct(custo_real_aa * 100, 4)} "
                                f"a.a. contra CET declarado ex-ante de "
                                f"{pct(declarado.cet_aa * 100, 4)} a.a.; a comparação válida "
                                f"exige o indexador vigente na contratação — informar "
                                f"`indexador_aa_na_contratacao` e `spread_aa`."),
                    "fundamento": ("Resolução CMN 4.881/2020; art. 28, §2º, I, 'd', da Lei "
                                   "10.931/2004; art. 422 do Código Civil."),
                })

    if declarado.base_calculo is not None and valor_do_titulo:
        div = abs(declarado.base_calculo - valor_do_titulo) / valor_do_titulo
        if div > D("0.01"):
            achados.append({
                "id": "CET-02", "tier": "T1", "resultado": "Ilícito",
                "titulo": "Demonstrativo de CET calculado sobre base divergente do título",
                "medida": pct(div * 100, 2),
                "detalhe": (f"Base do demonstrativo {brl_rs(declarado.base_calculo)} contra "
                            f"valor do instrumento {brl_rs(valor_do_titulo)}."),
                "fundamento": "Resolução CMN 4.881/2020, arts. 1º e 2º.",
            })

    if spread_contratual_am is not None and declarado.encargos_am is not None:
        sc = D(str(spread_contratual_am))
        if abs(declarado.encargos_am - sc) > D("0.0001"):
            achados.append({
                "id": "CET-03", "tier": "T2", "resultado": "Divergência",
                "titulo": "Encargos financeiros do anexo divergem do spread do instrumento",
                "medida": pt(f"{(declarado.encargos_am - sc) * 100:.4f}") + " p.p. a.m.",
                "detalhe": (f"Anexo informa {pct(declarado.encargos_am * 100, 4)} a.m.; o "
                            f"instrumento pactua {pct(sc * 100, 4)} a.m."),
                "fundamento": "Art. 28, §2º, I, 'd', da Lei 10.931/2004.",
            })

    if declarado.iof_total is not None and iof_documento_descritivo is not None:
        i2 = D(str(iof_documento_descritivo))
        if abs(declarado.iof_total - i2) > D("1"):
            achados.append({
                "id": "CET-04", "tier": "T2", "resultado": "Divergência",
                "titulo": "IOF divergente entre documentos do próprio credor",
                "medida": brl_rs(abs(declarado.iof_total - i2)),
                "detalhe": (f"Anexo de contratação {brl_rs(declarado.iof_total)}; documento "
                            f"descritivo {brl_rs(i2)}."),
                "fundamento": "Tema 621/STJ (REsp 1.251.331/RS) — IOF financiado exige pactuação expressa.",
            })

    return {"achados": achados, "lacunas": lacunas, "razao_custo_cet": razao,
            "custo_real_aa": custo_real_aa,
            "cet_esperado_aa": cet_esperado, "divergencia_ex_ante": div_ex_ante}


# ─────────────────────────────────────────────────────────────────────
# 5. CENÁRIOS CONTRAFACTUAIS
# ─────────────────────────────────────────────────────────────────────

def cenario_taxa_fixa(principal: D, liberacao: date, data_base: date,
                      taxa_aa: D, serie: dict[date, D],
                      pagamentos: list[Pagamento]) -> D:
    """Saldo na data-base caso a dívida houvesse evoluído a uma taxa efetiva fixa.

    Usa o MESMO calendário de dias úteis da reconstrução real — e a MESMA
    alocação de pagamentos (`_alocar_pagamentos`) — para que a comparação isole
    a taxa e não o calendário.
    """
    principal, taxa_aa = D(str(principal)), D(str(taxa_aa))
    pg, no_fim, _ = _alocar_pagamentos(serie, liberacao, data_base, pagamentos)
    f_dia = (D(1) + taxa_aa) ** (D(1) / BASE_DU)
    saldo = principal
    for d in dias_uteis(serie, liberacao, data_base):
        saldo = saldo * f_dia - pg.get(d, D(0))
    return saldo - no_fim


def tabela_contrafactual(rec: ReconstrucaoPosFixada, apurado_credor: D,
                         cenarios: dict[str, D]) -> list[dict]:
    """Monta a tabela de cenários do relatório.

    cenarios: {"Ao CET declarado no anexo": D("0.0666"), ...}
    Mede o diferencial entre o custo informado e o praticado. NÃO é proposta de
    recomposição do saldo — o relatório deve dizer isso expressamente.
    """
    apurado_credor = D(str(apurado_credor))
    linhas = [
        {"premissa": "Apurado pela credora", "taxa": None,
         "saldo": apurado_credor, "diferenca": None},
        {"premissa": "Recalculado pela metodologia pactuada",
         "taxa": rec.custo_efetivo_aa, "saldo": rec.saldo_final,
         "diferenca": apurado_credor - rec.saldo_final},
    ]
    for nome, taxa in cenarios.items():
        s = cenario_taxa_fixa(rec.principal, rec.liberacao, rec.data_base,
                              taxa, rec.serie, rec.pagamentos)
        linhas.append({"premissa": nome, "taxa": D(str(taxa)), "saldo": s,
                       "diferenca": apurado_credor - s})
    return linhas


# ─────────────────────────────────────────────────────────────────────
# 6. ENCARGOS DE MORA PROJETADOS
# ─────────────────────────────────────────────────────────────────────

def auditar_taxa_mora(taxa_dia_praticada: D | float, indexador_aa: D,
                      juros_mora_am: D | float = D("0.01")) -> dict:
    """Confronta a taxa diária que o credor projeta na planilha de inadimplência
    com os encargos moratórios efetivamente pactuados.

    Aparece em intimação do art. 26 da Lei 9.514/97, em planilha de cobrança e em
    demonstrativo de cumprimento de sentença. É achado autônomo.
    """
    td = D(str(taxa_dia_praticada))
    mora_aa = (D(1) + D(str(juros_mora_am))) ** 12 - D(1)
    contratual_aa = compor_aa(indexador_aa, mora_aa)
    praticada_aa = (D(1) + td) ** 365 - D(1)
    contratual_dia = (D(1) + contratual_aa) ** (D(1) / D(365)) - D(1)
    return {"praticada_dia": td, "praticada_aa": praticada_aa,
            "contratual_dia": contratual_dia, "contratual_aa": contratual_aa,
            "excesso_pp_aa": (praticada_aa - contratual_aa) * D(100),
            "excede": praticada_aa > contratual_aa}


def acrescimos_nao_discriminados(serie_valores: list[tuple[str, D]],
                                 taxa_dia: D | float,
                                 tolerancia: D | float = 50) -> list[dict]:
    """Varre uma projeção diária de débito e isola os saltos que a taxa declarada
    não explica. Cada salto é acréscimo sem rubrica — achado de não discriminação.

    serie_valores: [("17/06", D("1596229.99")), ("18/06", D("1597481.43")), ...]
    """
    td, tol = D(str(taxa_dia)), D(str(tolerancia))
    fora = []
    for (d1, v1), (d2, v2) in zip(serie_valores, serie_valores[1:]):
        v1, v2 = D(str(v1)), D(str(v2))
        esperado = v1 * td
        observado = v2 - v1
        excedente = observado - esperado
        if abs(excedente) > tol:
            fora.append({"de": d1, "para": d2, "observado": observado,
                         "esperado": esperado, "excedente": excedente})
    return fora


# `brl`, `brl_rs`, `pct` e `pt` vêm de comum.py (Decimal, ROUND_HALF_UP) — uma única
# formatação pt-BR para todos os motores; a versão local (ROUND_HALF_EVEN via
# format) foi removida para não divergir no centavo.


# ─────────────────────────────────────────────────────────────────────
# 7. AUTOTESTE
# ─────────────────────────────────────────────────────────────────────

def _testes() -> tuple[int, int]:
    ok = fail = 0

    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond:
            ok += 1
            print(f"  PASS  {nome} {extra}")
        else:
            fail += 1
            print(f"  FAIL  {nome} {extra}")

    # série sintética: 0,05% ao dia útil, seg-sex, 2025-07-18 .. 2026-04-30
    import datetime as dt
    regs, d = [], dt.date(2025, 7, 18)
    while d <= dt.date(2026, 4, 30):
        if d.weekday() < 5:
            regs.append({"data": d.strftime("%d/%m/%Y"), "valor": "0.050000"})
        d += dt.timedelta(days=1)
    serie = carregar_serie_sgs(regs)
    chk("serie carregada so com dias uteis", len(serie) == len(regs))

    cob = cobertura(serie, dt.date(2025, 7, 18), dt.date(2026, 4, 10))
    chk("cobertura integral detectada", cob["cobre"])
    cob2 = cobertura(serie, dt.date(2024, 1, 1), dt.date(2026, 4, 10))
    chk("falta de cobertura e detectada", not cob2["cobre"])

    try:
        carregar_serie_sgs([])
        chk("serie vazia deve falhar", False)
    except ValueError:
        chk("serie vazia e lacuna bloqueante", True)

    rec = ReconstrucaoPosFixada(
        principal=D("1000000"), liberacao=dt.date(2025, 7, 18),
        data_base=dt.date(2026, 4, 10), spread_aa=D("0.03041596"), serie=serie,
        pagamentos=[Pagamento(dt.date(2025, 8, 22), D("20000")),
                    Pagamento(dt.date(2025, 9, 22), D("20000"))])
    chk("reconstrucao gera uma linha por dia util", rec.n_du == len(dias_uteis(
        serie, dt.date(2025, 7, 18), dt.date(2026, 4, 10))))
    chk("total amortizado confere", rec.total_amortizado == D("40000"))
    chk("saldo cresce com indexador alto e amortizacao baixa",
        rec.saldo_final > D("1000000") - D("40000"))
    idx = rec.indexador_aa * 100
    chk("indexador anualizado coerente", D("12") < idx < D("14"), f"({idx:.4f}% a.a.)")
    ce = rec.custo_efetivo_aa
    chk("custo efetivo supera o indexador puro", ce > rec.indexador_aa)

    try:
        ReconstrucaoPosFixada(principal=D("1000"), liberacao=dt.date(2020, 1, 1),
                              data_base=dt.date(2026, 4, 10), spread_aa=D("0.03"),
                              serie=serie)
        chk("periodo fora da serie deve falhar", False)
    except ValueError:
        chk("periodo fora da serie e lacuna bloqueante", True)

    c = conferir_saldo(rec.saldo_final, rec.saldo_final * D("1.0015"))
    chk("divergencia de 0,15% e CONFORME", c["confere"] and c["veredito"] == "CONFORME")
    c2 = conferir_saldo(rec.saldo_final, rec.saldo_final * D("1.08"))
    chk("divergencia de 8% e DIVERGENTE", not c2["confere"])

    dec = CETDeclarado(cet_aa=D("0.0666"), encargos_am=D("0.0045"),
                       base_calculo=D("3166077.58"), iof_total=D("83769.05"))
    aud = auditar_cet(dec, custo_real_aa=D("0.183737"), valor_do_titulo=D("1415330.57"),
                      spread_contratual_am=D("0.0025"),
                      iof_documento_descritivo=D("2202.07"))
    ids = {a["id"] for a in aud["achados"]}
    _c01 = [a for a in aud["achados"] if a["id"] == "CET-01"]
    chk("CET-01 sem indexador da contratacao: emitido como 'A verificar', nunca Ilicito",
        len(_c01) == 1 and _c01[0]["resultado"] == "A verificar" and _c01[0]["tier"] == "T2")
    chk("CET-01 sem indexador registra lacuna", any("indexador" in l for l in aud["lacunas"]))
    chk("CET-02 detectado (base divergente)", "CET-02" in ids)
    _c02 = next(a for a in aud["achados"] if a["id"] == "CET-02")
    chk("CET-02 formata moeda em pt-BR (brl_rs)",
        "R$ 3.166.077,58" in _c02["detalhe"] and "3,166,077.58" not in _c02["detalhe"],
        f"-> {_c02['detalhe']}")
    _c04 = next(a for a in aud["achados"] if a["id"] == "CET-04")
    chk("CET-04 formata moeda em pt-BR", "R$ 83.769,05" in _c04["detalhe"] and _c04["medida"] == "R$ 81.566,98")
    chk("CET-03 detectado (spread divergente)", "CET-03" in ids)
    chk("CET-04 detectado (IOF divergente)", "CET-04" in ids)
    chk("razao custo/CET calculada", aud["razao_custo_cet"] > D("2.7"),
        f"({aud['razao_custo_cet']:.2f}x)")

    dec_ok = CETDeclarado(cet_aa=D("0.1830"), base_calculo=D("1415330.57"))
    aud_ok = auditar_cet(dec_ok, D("0.183737"), D("1415330.57"))
    chk("CET aderente nao gera achado", aud_ok["achados"] == [])

    tab = tabela_contrafactual(rec, rec.saldo_final,
                               {"Ao CET declarado": D("0.0666")})
    chk("tabela contrafactual tem 3 linhas", len(tab) == 3)
    chk("cenario a taxa menor produz saldo menor",
        tab[2]["saldo"] < tab[0]["saldo"])

    m = auditar_taxa_mora(D("0.000784"), D("0.148796"))
    chk("mora praticada acima da contratada e detectada", m["excede"])
    chk("excesso em pontos percentuais calculado", m["excesso_pp_aa"] > D("3"),
        f"({m['excesso_pp_aa']:.2f} p.p. a.a.)")
    m2 = auditar_taxa_mora(D("0.000699"), D("0.148796"))
    chk("mora dentro do pactuado nao acusa excesso", not m2["excede"])

    saltos = acrescimos_nao_discriminados(
        [("01", D("1000000")), ("02", D("1000784")), ("03", D("1005000"))],
        D("0.000784"))
    chk("salto sem rubrica isolado", len(saltos) == 1 and saltos[0]["de"] == "02")

    chk("brl formata pt-BR", brl(1547563.74) == "1.547.563,74", f"-> {brl(1547563.74)}")

    # --- adaptadores do conector Radar Apogeu ---
    resp_ind = {"cabecalho": {"pontos": 3}, "fator_acumulado": "1.00165484",
                "pontos": [{"data": "18/07/2025", "valor": "0.055131"},
                           {"data": "21/07/2025", "valor": "0.055131"},
                           {"data": "22/07/2025", "valor": "0.055131"}]}
    s_ind = carregar_de_consultar_indice(resp_ind)
    chk("adaptador consultar_indice carrega os pontos", len(s_ind) == 3)
    chk("adaptador aceita string JSON",
        len(carregar_de_consultar_indice(json.dumps(resp_ind))) == 3)
    cf = conferir_fator(s_ind, resp_ind["fator_acumulado"])
    chk("fator local confere com o do conector (serie inteira)", cf["confere"],
        f"(local {cf['local']:.8f} x conector {cf['conector']})")
    chk("conferencia cobre todos os pontos carregados", cf["pontos"] == 3)
    cf2 = conferir_fator(s_ind, "1.5")
    chk("divergencia de fator e detectada", not cf2["confere"])
    # A janela do conector e FECHADA: incluir o ultimo dia nao pode divergir.
    cf3 = conferir_fator(s_ind, resp_ind["fator_acumulado"],
                         dt.date(2025, 7, 18), dt.date(2025, 7, 22))
    chk("janela fechada bate com o fator do conector", cf3["confere"])
    _ordem = False
    try:
        conferir_fator(s_ind, dt.date(2025, 7, 18), dt.date(2025, 7, 23))
    except TypeError:
        _ordem = True
    chk("assinatura antiga (posicional) falha alto", _ordem)

    txt = ("Serie SGS 12 - CDI - taxa diaria\n  18/07/2025: 0.055131\n"
           "  21/07/2025: 0.055131\n  22/07/2025: 0.055131\n")
    s_txt = carregar_de_consultar_taxa_bacen(txt)
    chk("adaptador consultar_taxa_bacen parseia o texto do cache", len(s_txt) == 3)
    chk("os dois adaptadores produzem a mesma serie", s_txt == s_ind)
    _vazio = False
    try:
        carregar_de_consultar_taxa_bacen("sem pontos aqui")
    except ValueError:
        _vazio = True
    chk("resposta sem ponto e lacuna bloqueante", _vazio)

    # Recorte de texto: 60 de N pontos. cobertura() e verificar_ponta_da_serie()
    # passariam — o corte preserva as duas pontas. Tem de ser erro duro aqui.
    txt_cortado = ("Serie SGS 12 - CDI\n  18/07/2025: 0.055131\n"
                   "  ... 1190 de 1250 pontos OMITIDOS DESTE TEXTO (o recorte e so "
                   "de exibicao) ...\n  22/07/2025: 0.055131\n")
    _cortado = False
    try:
        carregar_de_consultar_taxa_bacen(txt_cortado)
    except ValueError as e:
        _cortado = "RECORTADA" in str(e)
    chk("texto recortado do conector e recusado", _cortado)

    # Payload estruturado em modo 'resumo': a serie integra vem em `dados`.
    s_pay = carregar_de_consultar_taxa_bacen(
        {"pontos_total": 3, "dados": resp_ind["pontos"]})
    chk("adaptador aceita o payload estruturado", s_pay == s_ind)

    # Contagem divergente: o conector diz 1250, o texto rendeu 3.
    _conta = False
    try:
        carregar_de_consultar_taxa_bacen({"pontos_total": 1250, "texto": txt})
    except ValueError as e:
        _conta = "incompleta" in str(e)
    chk("contagem divergente de pontos e recusada", _conta)

    # Envelope MCP cru: e o que um agente passa naturalmente.
    env_estruturado = {"content": [{"type": "text", "text": txt}],
                       "structuredContent": {"pontos_total": 3, "dados": resp_ind["pontos"]}}
    chk("adaptador aceita o envelope MCP com structuredContent",
        carregar_de_consultar_taxa_bacen(env_estruturado) == s_ind)
    env_so_texto = {"content": [{"type": "text", "text": txt}]}
    chk("adaptador aceita o envelope MCP so com content/text",
        carregar_de_consultar_taxa_bacen(env_so_texto) == s_ind)

    # cobertura(): cega ao miolo por construcao; pontos_esperados fecha a brecha.
    cob_ok = cobertura(s_ind, dt.date(2025, 7, 18), dt.date(2025, 7, 22))
    chk("cobertura das pontas passa sem pontos_esperados", cob_ok["cobre"])
    chk("cobertura declara que nao detecta lacuna interna",
        cob_ok["detecta_lacuna_interna"] is False)
    cob_furo = cobertura(s_ind, dt.date(2025, 7, 18), dt.date(2025, 7, 22),
                         pontos_esperados=1250)
    chk("contagem divergente reprova a cobertura", not cob_furo["cobre"],
        f"-> {cob_furo['motivo']}")

    # --- adaptador generico de linhas + guarda de ponta de serie ---
    rows = [{"data_ponto": "2025-07-18", "valor": "0.055131"},
            {"data_ponto": "2025-07-21", "valor": "0.055131"},
            {"data_ponto": "2025-07-22", "valor": "0.055131"}]
    s_lin = carregar_de_linhas(rows)
    chk("adaptador generico carrega datas ISO", len(s_lin) == 3)
    chk("adaptador generico bate com o do conector", s_lin == s_ind)
    chk("adaptador generico aceita dd/mm/aaaa",
        len(carregar_de_linhas([{"data": "18/07/2025", "valor": "0.055131"}])) == 1)
    _vaz = False
    try:
        carregar_de_linhas([])
    except ValueError:
        _vaz = True
    chk("serie vazia em lista e lacuna bloqueante", _vaz)
    d1 = verificar_ponta_da_serie(dt.date(2026, 7, 31), dt.date(2026, 4, 10))
    chk("serie alcanca a data-base", d1["cobre"] and d1["dias_faltantes"] == 0)
    # 17/08/2026 e segunda: a ponta necessaria e sexta 14/08 -> faltam 14 dias (nao 17);
    # o criterio do conector (data_final inclusive) fica em dias_ate_data_base.
    d2 = verificar_ponta_da_serie(dt.date(2026, 7, 31), dt.date(2026, 8, 17))
    chk("ponta curta e detectada (ate o dia util anterior a data-base)",
        not d2["cobre"] and d2["dias_faltantes"] == 14
        and d2["ponta_necessaria"] == dt.date(2026, 8, 14)
        and d2["dias_ate_data_base"] == 17 and d2["alcanca_data_base"] is False)

    # ── auditoria de fator declarado — as duas convenções ────────────
    dias = [date(2025, 1, d) for d in (2, 3, 6, 7, 8, 9, 10)]
    ser = {d: D("0.0005") for d in dias}
    f_fech = fator_indexador(ser, dias_uteis_fechado(ser, dias[0], dias[-1]))
    f_semi = fator_indexador(ser, dias_uteis(ser, dias[0], dias[-1]))
    chk("janela fechada inclui o ultimo ponto", len(dias_uteis_fechado(ser, dias[0], dias[-1])) == 7)
    chk("janela semiaberta exclui o ultimo ponto", len(dias_uteis(ser, dias[0], dias[-1])) == 6)
    chk("as duas convencoes divergem", f_fech != f_semi)
    aud = auditar_fator_declarado(ser, dias[0], dias[-1], f_fech)
    chk("fator identico ao real e CONFORME", aud["veredito"] == "CONFORME")
    aud2 = auditar_fator_declarado(ser, dias[0], dias[-1], f_fech * D("1.01"))
    chk("fator inflado e DIVERGENTE", aud2["veredito"] == "DIVERGENTE")
    chk("auditoria adota a convencao de menor excesso",
        abs(aud2["excesso"]) == min(abs(aud2["excesso_fechada"]), abs(aud2["excesso_semiaberta"])))
    chk("auditoria reporta as duas convencoes",
        aud2["fator_janela_fechada"] != aud2["fator_janela_semiaberta"])
    aud3 = auditar_fator_declarado(ser, dias[0], dias[-1], f_fech, fator_conector=f_fech)
    chk("fator do conector prevalece na convencao fechada", aud3["fonte_fechada"] == "conector")

    # ── item 1/5/8: pagamentos (agregacao, deslocamento, data-base, excesso) e memoria ──
    # serie sintetica: 0,05% ao dia util, 01/08/2025 .. 29/08/2025 (01/08 e sexta)
    regs_ago, d = [], dt.date(2025, 8, 1)
    while d <= dt.date(2025, 8, 29):
        if d.weekday() < 5:
            regs_ago.append({"data": d.strftime("%d/%m/%Y"), "valor": "0.050000"})
        d += dt.timedelta(days=1)
    ser_ago = carregar_serie_sgs(regs_ago)
    base = dict(principal=D("100000"), liberacao=dt.date(2025, 8, 1), spread_aa=D(0), serie=ser_ago)
    r0 = ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base)
    # 11 dias uteis em [01/08, 18/08): 100.000 x 1,0005^11 = 100.551,3770645639...
    chk("saldo sem pagamento fixo: 11 DU a 0,05% = 100.551,37706456",
        r0.n_du == 11 and abs(r0.saldo_final - D("100551.37706456")) < D("1e-6"),
        f"({r0.saldo_final:.8f})")
    r1 = ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                               pagamentos=[Pagamento(dt.date(2025, 8, 18), D("50000"))])
    chk("pagamento NA data-base e abatido: total_amortizado = 50.000",
        r1.total_amortizado == D("50000"))
    chk("pagamento na data-base: saldo_final = saldo sem pagamento - 50.000 (sem encargo do dia)",
        r1.saldo_final == r0.saldo_final - D("50000") and r1.n_du == 11)
    chk("pagamento na data-base fica registrado com data_original na ultima linha",
        r1.linhas[-1]["data_original"] == dt.date(2025, 8, 18)
        and len(r1.pagamentos_deslocados) == 1)
    r2 = ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                               pagamentos=[Pagamento(dt.date(2025, 8, 8), 100),
                                           Pagamento(dt.date(2025, 8, 8), 200)])
    l08 = next(l for l in r2.linhas if l["data"] == dt.date(2025, 8, 8))
    chk("dois pagamentos no mesmo dia SOMAM: amortizacao de 300 em 08/08",
        l08["amortizacao"] == D("300") and r2.total_amortizado == D("300"))
    chk("linha sem deslocamento tem data_original None e sem pagamentos_deslocados",
        l08["data_original"] is None and r2.pagamentos_deslocados == [])
    # sabado 16/08 -> proximo dia util da serie e segunda 18/08 (data_base 22/08 para haver linha)
    r3 = ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 22), **base,
                               pagamentos=[Pagamento(dt.date(2025, 8, 16), 1000)])
    l18 = next(l for l in r3.linhas if l["data"] == dt.date(2025, 8, 18))
    chk("pagamento em sabado 16/08 aparece na linha de 18/08 com data_original 16/08",
        l18["amortizacao"] == D("1000") and l18["data_original"] == dt.date(2025, 8, 16))
    chk("pagamentos_deslocados registra 16/08 -> 18/08",
        len(r3.pagamentos_deslocados) == 1
        and r3.pagamentos_deslocados[0]["data_original"] == dt.date(2025, 8, 16)
        and r3.pagamentos_deslocados[0]["data_aplicada"] == dt.date(2025, 8, 18)
        and r3.pagamentos_deslocados[0]["valor"] == D("1000"))
    for _dp in (dt.date(2025, 7, 31), dt.date(2025, 8, 19)):
        _fora = False
        try:
            ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                                  pagamentos=[Pagamento(_dp, 1)])
        except ValueError as e:
            _fora = "fora do período" in str(e)
        chk(f"pagamento em {_dp.strftime('%d/%m')} fora de [01/08, 18/08] e ValueError", _fora)
    _exc = False
    try:
        ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                              pagamentos=[Pagamento(dt.date(2025, 8, 8), D("200000"))])
    except ValueError as e:
        _exc = "pagamento excede o saldo em 08/08/2025" in str(e)
    chk("pagamento maior que o saldo e ValueError com a data (item 8)", _exc)
    _exc2 = False
    try:
        ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                              pagamentos=[Pagamento(dt.date(2025, 8, 18), D("100600"))])
    except ValueError as e:
        _exc2 = "pagamento excede o saldo em 18/08/2025" in str(e)
    chk("pagamento na data-base maior que o saldo tambem e ValueError", _exc2)
    chk("pagamento igual ao saldo zera sem erro",
        ReconstrucaoPosFixada(data_base=dt.date(2025, 8, 18), **base,
                              pagamentos=[Pagamento(dt.date(2025, 8, 18), r0.saldo_final)]
                              ).saldo_final == D(0))

    def _memoria_fecha(r):
        return all(abs(l["saldo_anterior"] + l["encargo_indexador"] + l["encargo_spread"]
                       - l["amortizacao"] - l["saldo"]) < D("1e-9") for l in r.linhas)
    chk("memoria fecha com spread (R$ 1M, 9 meses): saldo_ant + enc_idx + enc_spr - amort == saldo",
        _memoria_fecha(rec))
    chk("memoria fecha com pagamento na data-base", _memoria_fecha(r1) and _memoria_fecha(r3))
    chk("encargo_spread inclui o termo cruzado saldo*i*(f_dia-1)",
        rec.linhas[0]["encargo_spread"] == rec.linhas[0]["saldo_anterior"]
        * (D(1) + rec.linhas[0]["taxa_dia"]) * (fator_spread(rec.spread_aa, 1) - D(1)))
    chk("cenario_taxa_fixa usa a mesma alocacao de pagamentos (taxa 0: 100.000 - 51.000)",
        cenario_taxa_fixa(D("100000"), dt.date(2025, 8, 1), dt.date(2025, 8, 18), D(0), ser_ago,
                          [Pagamento(dt.date(2025, 8, 16), 1000),
                           Pagamento(dt.date(2025, 8, 18), 50000)]) == D("49000"))

    # ── item 2: cobertura ate o dia util anterior a data-base ──
    regs_set, d = [], dt.date(2025, 9, 1)
    while d <= dt.date(2025, 9, 26):                       # termina na sexta 26/09
        if d.weekday() < 5:
            regs_set.append({"data": d.strftime("%d/%m/%Y"), "valor": "0.050000"})
        d += dt.timedelta(days=1)
    ser_set = carregar_serie_sgs(regs_set)
    cs1 = cobertura(ser_set, dt.date(2025, 9, 1), dt.date(2025, 9, 29))
    chk("serie ate sexta 26/09 cobre data-base segunda 29/09",
        cs1["cobre"] and cs1["ponta_necessaria"] == dt.date(2025, 9, 26))
    cs2 = cobertura(ser_set, dt.date(2025, 9, 1), dt.date(2025, 9, 30))
    chk("serie ate sexta 26/09 NAO cobre data-base terca 30/09",
        not cs2["cobre"] and "série termina em 26/09/2025" in cs2["motivo"], f"-> {cs2['motivo']}")
    chk("reconstrucao aceita data-base na segunda com serie ate sexta (20 DU)",
        ReconstrucaoPosFixada(principal=1000, liberacao=dt.date(2025, 9, 1),
                              data_base=dt.date(2025, 9, 29), spread_aa=0, serie=ser_set).n_du == 20)
    v1 = verificar_ponta_da_serie(dt.date(2025, 9, 26), dt.date(2025, 9, 29))
    chk("verificar_ponta: sexta cobre segunda (conector diria que nao alcanca)",
        v1["cobre"] and v1["dias_faltantes"] == 0 and v1["alcanca_data_base"] is False)
    v2 = verificar_ponta_da_serie(dt.date(2025, 9, 26), dt.date(2025, 9, 30))
    chk("verificar_ponta: sexta nao cobre terca (falta segunda 29/09)",
        not v2["cobre"] and v2["dias_faltantes"] == 3 and v2["ponta_necessaria"] == dt.date(2025, 9, 29))

    # ── item 3: CET-01 ex-ante (Res. CMN 4.881/2020) ──
    dec5 = CETDeclarado(cet_aa=D("0.05"))
    a1 = auditar_cet(dec5, custo_real_aa=D("0.165"), valor_do_titulo=D("100000"),
                     indexador_aa_na_contratacao=D("0.019"), spread_aa=D("0.03"))
    chk("CET esperado ex-ante = (1,019 x 1,03) - 1 = 4,957%", a1["cet_esperado_aa"] == D("0.04957"))
    chk("CET 5,0% vs esperado 4,957% (0,87% rel.): sem achado CET-01",
        not any(a["id"] == "CET-01" for a in a1["achados"]) and a1["divergencia_ex_ante"] < D("0.05"))
    a2 = auditar_cet(dec5, custo_real_aa=D("0.165"), valor_do_titulo=D("100000"))
    c01 = [a for a in a2["achados"] if a["id"] == "CET-01"]
    chk("custo real 16,5% sem indexador: CET-01 'A verificar' T2, nunca Ilicito",
        len(c01) == 1 and c01[0]["resultado"] == "A verificar" and c01[0]["tier"] == "T2")
    chk("detalhe ex-post em pt-BR com os dois valores",
        "16,5000% a.a." in c01[0]["detalhe"] and "5,0000% a.a." in c01[0]["detalhe"]
        and "indexador vigente na contratação" in c01[0]["detalhe"] and c01[0]["medida"] == "3,30x")
    chk("sem indexador: lacuna registrada e cet_esperado None",
        any("indexador" in l for l in a2["lacunas"]) and a2["cet_esperado_aa"] is None)
    a3 = auditar_cet(CETDeclarado(cet_aa=D("0.09")), D("0.165"), D("100000"),
                     indexador_aa_na_contratacao=D("0.019"), spread_aa=D("0.03"))
    c01 = [a for a in a3["achados"] if a["id"] == "CET-01"]
    chk("CET 9% vs esperado 4,957%: Ilicito T1",
        len(c01) == 1 and c01[0]["resultado"] == "Ilícito" and c01[0]["tier"] == "T1")
    chk("detalhe mostra declarado vs esperado ex-ante",
        "9,0000% a.a." in c01[0]["detalhe"] and "4,9570% a.a." in c01[0]["detalhe"])
    a4 = auditar_cet(dec5, D("0.165"), D("100000"), indexador_aa_na_contratacao=D("0.019"))
    chk("so um dos dois parametros ex-ante: lacuna, e CET-01 continua 'A verificar'",
        any("JUNTOS" in l for l in a4["lacunas"])
        and all(a["resultado"] != "Ilícito" for a in a4["achados"] if a["id"] == "CET-01"))

    # ── item 6: conferir_fator com tolerancia relativa e casas do conector ──
    s_q = carregar_serie_sgs([{"data": "01/09/2025", "valor": "127.59998863"}])  # fator 2,2759998863
    cq = conferir_fator(s_q, "2.276000", casas_conector=6)
    chk("fator local 2,2759998863 x conector '2.276000' com casas_conector=6 confere",
        cq["confere"] and cq["local_comparado"] == D("2.276000") and cq["diferenca"] == 0)
    cq2 = conferir_fator(s_q, "2.276000", tolerancia_rel=D("1e-9"))
    chk("sem quantizar, tolerancia relativa 1e-9 acusa a diferenca (5e-8)",
        not cq2["confere"] and cq2["local"] == D("2.2759998863"))
    cq3 = conferir_fator(s_q, "2.276000")
    chk("tolerancia relativa padrao 1e-7 aceita diferenca relativa de 5e-8",
        cq3["confere"] and D("4.9e-8") < cq3["diferenca_rel"] < D("5.1e-8"))
    chk("tolerancia absoluta legada ainda e aceita",
        not conferir_fator(s_q, "2.276000", tolerancia="1e-9")["confere"])

    # ── item 7: lacunas explicitas ──
    _lac = False
    try:
        conferir_saldo(D("1000"), D(0))
    except ValueError as e:
        _lac = "lacuna" in str(e) and "ausente ou zero" in str(e)
    chk("conferir_saldo com apurado 0 e ValueError (lacuna), nao CONFORME", _lac)
    a0 = auditar_cet(dec5, D(0), D("100000"))
    chk("auditar_cet com custo_real_aa == 0 registra lacuna e nao emite CET-01",
        any("custo efetivo" in l for l in a0["lacunas"])
        and not any(a["id"] == "CET-01" for a in a0["achados"]) and a0["razao_custo_cet"] is None)

    # ── item 4: brl delegado a comum (HALF_UP) ──
    chk("brl delega a comum: HALF_UP e negativo",
        brl(0.125) == "0,13" and brl_rs(-1500) == "R$ -1.500,00" and pct(D("0.04957") * 100, 4) == "4,9570%")

    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("cet", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    print("\n  motores/cet.py — autoteste\n")
    raise SystemExit(1 if autoteste()["falharam"] else 0)
