"""
conta_corrente.py — motor determinístico da rota CONTA
Versão 1.1.0 · 2026-09-20
Skill: revisao-bancaria

Escopo: conta corrente, cheque especial e conta garantida a partir de extratos.
O motor é PURO: não parseia PDF, não chama conector. Recebe lançamentos no CSV
canônico (extraídos e aprovados na camada C1) e vetores de taxa (obtidos pelo
conector na camada C2). Devolve números e vereditos.

Princípios (herdados do calculo.py):
  1. Precisão plena no cálculo; arredondamento apenas na exibição.
  2. Nenhuma função presume dado ausente: levanta erro explícito.
  3. A reconciliação contra o saldo impresso no extrato é a guarda que valida
     a extração — divergência ou competência faltante é lacuna bloqueante.
  4. Convenção de cálculo sempre declarada (linear_mes | linear_30 | exponencial_30).
  5. Sinal: saldo NEGATIVO = devedor. SMD e juros incidem só sobre saldo devedor.
  6. Taxas sempre em FRAÇÃO decimal mensal (0,03 = 3% a.m.); escala fora do
     plausível é recusada (guard_taxa de comum.py), nunca reinterpretada.

Formatação, parse pt-BR, competências e guarda de escala vêm de comum.py.

Executar `python3 revisao.py autoteste --modulo conta_corrente` roda a suíte de autoteste embutida.
"""

from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import date, timedelta

from .comum import (brl_rs, parse_num_ptbr, competencia, fim_do_mes, dias_no_mes,
                    competencias_entre, guard_taxa, CORTE_TEMA_929, rodar_autoteste, saida_utf8)

competencia_de = competencia   # alias para funções cujo parâmetro se chama `competencia`

# ─────────────────────────────────────────────────────────────────────
# 1. MODELO DE DADOS — CSV canônico
# ─────────────────────────────────────────────────────────────────────

CLASSES = ("ENCARGO", "MOVIMENTO", "ESTORNO")
NATUREZAS = ("D", "C")
RUBRICAS = ("juros", "iof", "tarifa", "seguro", "cp", "mora", "multa", "outro")

#: Convenções de taxa-dia (ver `_taxa_dia`):
#:   linear_mes      — taxa_am / nº de dias da competência. DEFAULT. É a única que
#:                     reproduz exatamente a taxa contratual sobre o SMD em qualquer
#:                     mês (31 dias × i/31 = i; 28 × i/28 = i).
#:   linear_30       — taxa_am / 30. Em mês de 31 dias cobra 31 × i/30 = 3,1% para
#:                     i = 3%; em fevereiro cobra menos que o contratado.
#:   exponencial_30  — (1+i)^(1/30) − 1. Sem capitalização diária no motor, 30 dias
#:                     sobre 1.000 a 3% rendem 29,57 em vez de 30,00.
#: linear_30 e exponencial_30 ficam disponíveis para impugnação comparável: quando
#: o laudo adversário usa uma delas, o motor roda na mesma régua e a diferença é
#: só o que se discute (juros, capitalização, encargos), não a convenção.
CONVENCOES = ("linear_mes", "linear_30", "exponencial_30")
CONVENCAO_PADRAO = "linear_mes"

CSV_CABECALHO = "data;historico;natureza;valor;classe;rubrica;contrato_ref;saldo_informado"


@dataclass
class Lancamento:
    data: date
    historico: str
    natureza: str            # D (débito) | C (crédito)
    valor: float             # sempre positivo
    classe: str              # ENCARGO | MOVIMENTO | ESTORNO
    rubrica: str | None = None      # obrigatória quando ENCARGO/ESTORNO
    contrato_ref: str | None = None  # id do contrato externo (nexo cruzado)
    saldo_informado: float | None = None  # saldo impresso no extrato APÓS este lançamento

    def __post_init__(self):
        if self.natureza not in NATUREZAS:
            raise ValueError(f"natureza inválida: {self.natureza!r} em {self.data} {self.historico!r}")
        if self.classe not in CLASSES:
            raise ValueError(f"classe inválida: {self.classe!r} em {self.data} {self.historico!r}")
        if self.valor is None or self.valor < 0:
            raise ValueError(f"valor inválido: {self.valor!r} em {self.data} {self.historico!r}")
        if self.classe in ("ENCARGO", "ESTORNO") and self.rubrica not in RUBRICAS:
            raise ValueError(
                f"lançamento {self.classe} sem rubrica válida em {self.data} {self.historico!r} "
                f"— classificar na C1 antes de rodar o motor (regra 0: nunca presumir)")

    @property
    def delta(self) -> float:
        """Efeito no saldo: crédito soma, débito subtrai."""
        return self.valor if self.natureza == "C" else -self.valor


#: Parse numérico: o de comum.py, estrito — recusa '1.500' (milhar ou 1,5?) e
#: '1,234.56' (en-US). Número ambíguo na extração é lacuna, não palpite.
_parse_num = parse_num_ptbr


def carregar_csv(texto: str) -> list[Lancamento]:
    """Carrega o CSV canônico. Separador ';'. Cabeçalho obrigatório.

    Campos: data (yyyy-mm-dd);historico;natureza;valor;classe;rubrica;contrato_ref;saldo_informado
    rubrica, contrato_ref e saldo_informado podem ficar vazios.
    Número ambíguo ou malformado levanta ValueError com o nº e o texto da linha.
    A saída vem ordenada por data de forma ESTÁVEL (ordem do CSV dentro do dia).
    """
    linhas = [l for l in texto.strip().splitlines() if l.strip()]
    if not linhas:
        raise ValueError("CSV vazio")
    cab = linhas[0].strip().lower().replace(" ", "")
    if cab != CSV_CABECALHO.replace(" ", ""):
        raise ValueError(f"cabeçalho inválido. Esperado: {CSV_CABECALHO}")
    out: list[Lancamento] = []
    for i, linha in enumerate(linhas[1:], start=2):
        campos = [c.strip() for c in linha.split(";")]
        if len(campos) != 8:
            raise ValueError(f"linha {i} ({linha.strip()!r}): esperados 8 campos, recebidos {len(campos)}")
        d, hist, nat, val, cls, rub, ref, si = campos
        try:
            valor = parse_num_ptbr(val)
            saldo_inf = parse_num_ptbr(si) if si else None
            data = date.fromisoformat(d)
        except ValueError as e:
            raise ValueError(f"linha {i} ({linha.strip()!r}): {e}") from None
        out.append(Lancamento(
            data=data,
            historico=hist,
            natureza=nat.upper(),
            valor=valor,
            classe=cls.upper(),
            rubrica=rub.lower() or None,
            contrato_ref=ref or None,
            saldo_informado=saldo_inf,
        ))
    if not out:
        raise ValueError("CSV sem lançamentos")
    return sorted(out, key=lambda l: l.data)


# ─────────────────────────────────────────────────────────────────────
# 2. RECONSTRUÇÃO DO SALDO E RECONCILIAÇÃO (guarda da extração)
# ─────────────────────────────────────────────────────────────────────

#: Convenção da janela quando `data_inicial` não é informada.
JANELA_SEM_DATA_INICIAL = ("início no 1º lançamento: saldo_inicial é o saldo de abertura "
                           "do dia do 1º lançamento; dias anteriores não entram na série")
JANELA_COM_DATA_INICIAL = ("início em data_inicial: saldo_inicial é o saldo de abertura "
                           "desse dia (saldo anterior impresso no extrato)")


def _ordenar(lancs: list[Lancamento]) -> list[Lancamento]:
    """Ordena por data de forma ESTÁVEL — lançamentos do mesmo dia mantêm a
    ordem do CSV (sorted() do Python é estável)."""
    return sorted(lancs, key=lambda l: l.data)


def _janela(lancs: list[Lancamento], data_final: date | None,
            data_inicial: date | None) -> tuple[date, date]:
    """(ini, fim) da série. `lancs` já ordenados e não vazios."""
    if data_inicial is not None and lancs[0].data < data_inicial:
        raise ValueError(
            f"lançamento em {lancs[0].data.isoformat()} anterior à data_inicial "
            f"{data_inicial.isoformat()} — saldo inicial informado não cobre o extrato")
    ini = data_inicial or lancs[0].data
    fim = data_final or lancs[-1].data
    if fim < ini:
        raise ValueError("data_final anterior ao início da série")
    return ini, fim


def recompor_saldo_diario(lancs: list[Lancamento], saldo_inicial: float,
                          data_final: date | None = None,
                          data_inicial: date | None = None) -> dict[date, float]:
    """Saldo de FECHAMENTO de cada dia. Dias sem movimento carregam o saldo anterior.

    Janela:
      data_inicial — data do saldo inicial informado no extrato: a série começa
                     nesse dia com `saldo_inicial` como saldo de abertura (os
                     lançamentos desse dia, se houver, incidem sobre ele).
                     None: começa no 1º lançamento (JANELA_SEM_DATA_INICIAL).
      data_final   — default: data do último lançamento.
    `lancs` é ordenado por data de forma estável; não precisa vir ordenado.
    """
    if not lancs:
        raise ValueError("sem lançamentos")
    lancs = _ordenar(lancs)
    ini, fim = _janela(lancs, data_final, data_inicial)
    por_dia: dict[date, list[Lancamento]] = {}
    for l in lancs:
        por_dia.setdefault(l.data, []).append(l)
    saldos: dict[date, float] = {}
    saldo = saldo_inicial
    d = ini
    while d <= fim:
        for l in por_dia.get(d, []):
            saldo += l.delta
        saldos[d] = saldo
        d += timedelta(days=1)
    return saldos


def reconciliar(lancs: list[Lancamento], saldo_inicial: float,
                tolerancia: float = 0.01,
                data_inicial: date | None = None) -> dict:
    """Confere o saldo recomputado contra o saldo_informado do extrato e
    verifica continuidade de competências. É a prova de que a extração da C1
    está íntegra: lançamento perdido, duplicado ou com valor errado desalinha
    o saldo e aparece aqui.

    Conferência por DIA: o saldo de fechamento recomputado do dia é comparado
    com o saldo_informado do ÚLTIMO lançamento daquele dia que o tenha (ordem
    do CSV). Saldos intermediários do mesmo dia são ignorados — quando a C1
    reordena lançamentos intradia eles perdem sentido e gerariam divergências
    falsas. Convenção para a C1: informar o saldo de fechamento do dia na
    última linha do dia.

    `lancs` é ordenado por data de forma estável. `data_inicial` (data do saldo
    inicial) entra na régua de competências.

    Retorna: { veredito: CONFORME|DIVERGENTE, pontos_conferidos, divergencias:[...],
               competencias:[...], competencias_sem_lancamento:[...],
               saldos_intradia_ignorados, janela }
    Veredito DIVERGENTE ou competência faltante = lacuna bloqueante: a análise
    NÃO prossegue (voltar à C1 e corrigir a extração ou pedir o extrato faltante).
    """
    if not lancs:
        raise ValueError("sem lançamentos")
    lancs = _ordenar(lancs)
    ini, fim = _janela(lancs, None, data_inicial)
    por_dia: dict[date, list[Lancamento]] = {}
    for l in lancs:
        por_dia.setdefault(l.data, []).append(l)
    saldo = saldo_inicial
    divergencias, pontos, ignorados = [], 0, 0
    comps_com_lanc = set()
    if data_inicial is not None:
        comps_com_lanc.add(competencia(ini))     # o saldo inicial datado prova o extrato do mês
    for d, do_dia in por_dia.items():            # ordem de inserção = ordem de data
        for l in do_dia:
            saldo += l.delta
        comps_com_lanc.add(competencia(d))
        com_saldo = [l for l in do_dia if l.saldo_informado is not None]
        if not com_saldo:
            continue
        ref = com_saldo[-1]
        ignorados += len(com_saldo) - 1
        pontos += 1
        dif = saldo - ref.saldo_informado
        if abs(dif) > tolerancia:
            divergencias.append({
                "data": d.isoformat(), "historico": ref.historico,
                "saldo_recomputado": round(saldo, 2),
                "saldo_informado": round(ref.saldo_informado, 2),
                "diferenca": round(dif, 2),
            })
            # realinha para localizar TODAS as quebras, não só a primeira
            saldo = ref.saldo_informado
    todas = competencias_entre(ini, fim)
    faltantes = [c for c in todas if c not in comps_com_lanc]
    return {
        "veredito": "CONFORME" if not divergencias and not faltantes else "DIVERGENTE",
        "pontos_conferidos": pontos,
        "divergencias": divergencias,
        "competencias": todas,
        "competencias_sem_lancamento": faltantes,
        "saldos_intradia_ignorados": ignorados,
        "janela": {
            "data_inicial": ini.isoformat(), "data_final": fim.isoformat(),
            "convencao": JANELA_COM_DATA_INICIAL if data_inicial else JANELA_SEM_DATA_INICIAL,
        },
    }


# ─────────────────────────────────────────────────────────────────────
# 3. SMD (MÉTODO HAMBURGUÊS) E PERFIL DA CONTA
# ─────────────────────────────────────────────────────────────────────

def smd_hamburgues(saldos: dict[date, float], competencia: str,
                   base: str = "dias_corridos") -> dict:
    """Saldo médio devedor da competência pelo método hamburguês.

    base:
      dias_corridos  — Σ saldos devedores diários / nº de dias da competência (padrão)
      dias_devedores — Σ saldos devedores diários / nº de dias com saldo devedor

    A convenção usada DEVE constar da metodologia do entregável.
    """
    dias = [(d, s) for d, s in saldos.items() if competencia_de(d) == competencia]
    if not dias:
        raise ValueError(f"competência {competencia} sem saldos — lacuna bloqueante")
    soma_dev = sum(-s for _, s in dias if s < 0)
    n_dev = sum(1 for _, s in dias if s < 0)
    n_total = len(dias)
    if base == "dias_corridos":
        smd = soma_dev / n_total
    elif base == "dias_devedores":
        smd = soma_dev / n_dev if n_dev else 0.0
    else:
        raise ValueError(f"base inválida: {base!r}")
    return {
        "competencia": competencia, "smd": smd, "base": base,
        "dias": n_total, "dias_devedores": n_dev,
        "soma_saldos_devedores": soma_dev,
        "maior_saldo_devedor": max((-s for _, s in dias if s < 0), default=0.0),
    }


def perfil_conta(saldos: dict[date, float]) -> dict:
    """Visão geral: quanto a conta 'roda no vermelho'. Alimenta a C2."""
    n = len(saldos)
    dev = [(d, s) for d, s in saldos.items() if s < 0]
    return {
        "dias": n,
        "dias_devedores": len(dev),
        "pct_dias_devedores": round(100 * len(dev) / n, 1) if n else 0.0,
        "maior_saldo_devedor": max((-s for _, s in dev), default=0.0),
        "data_maior_saldo_devedor": min(dev, key=lambda x: x[1])[0].isoformat() if dev else None,
    }


def _taxa_dia(taxa_am: float, convencao: str = CONVENCAO_PADRAO,
              competencia: str | int | None = None) -> float:
    """Taxa-dia a partir da taxa mensal (fração decimal), pela convenção.

    convencao:
      linear_mes      — taxa_am / dias_no_mes(competencia). DEFAULT. Reproduz a taxa
                        contratual exata sobre o SMD em qualquer mês (31 × i/31 = i).
                        Exige `competencia` ("YYYY-MM") ou o nº de dias do mês (int).
      linear_30       — taxa_am / 30. Mês de 31 dias cobra 3,1% para i = 3%.
      exponencial_30  — (1+i)^(1/30) − 1. Sem capitalização diária, 30 dias sobre
                        1.000 a 3% rendem 29,57 em vez de 30,00.
    As duas últimas existem para impugnação comparável (mesma régua do laudo adversário).
    """
    if convencao == "linear_mes":
        if competencia is None:
            raise ValueError("linear_mes exige a competência ('YYYY-MM') ou o nº de dias do mês")
        n = competencia if isinstance(competencia, int) else dias_no_mes(competencia)
        return taxa_am / n
    if convencao == "linear_30":
        return taxa_am / 30.0
    if convencao == "exponencial_30":
        return (1.0 + taxa_am) ** (1.0 / 30.0) - 1.0
    raise ValueError(f"convenção inválida: {convencao!r}. Use uma de {CONVENCOES}")


def juros_hamburgues(saldos: dict[date, float], competencia: str, taxa_am: float,
                     convencao: str = CONVENCAO_PADRAO) -> float:
    """Juros da competência: Σ saldo devedor diário × taxa-dia (convenção declarada)."""
    td = _taxa_dia(taxa_am, convencao, competencia)
    return sum(-s * td for d, s in saldos.items()
               if competencia_de(d) == competencia and s < 0)


# ─────────────────────────────────────────────────────────────────────
# 4. CENÁRIOS DE RECOMPOSIÇÃO
# ─────────────────────────────────────────────────────────────────────

@dataclass
class CenarioConta:
    """Parâmetros de um cenário de recomposição.

    nome                — rótulo do cenário
    condicao            — condição de aplicabilidade, declarada no entregável
    taxa                — float (taxa fixa % a.m. em decimal) OU dict {"YYYY-MM": taxa}
                          (vetor mensal, ex.: taxa média BACEN da modalidade).
                          Competência faltante no vetor = lacuna bloqueante.
    expurgar_rubricas   — rubricas de ENCARGO expurgadas do fluxo (os juros
                          lançados são SEMPRE expurgados e recompostos pelo motor,
                          exceto se recompor_juros=False)
    recompor_juros      — True: expurga os juros cobrados e recompõe pela taxa do
                          cenário. False: mantém os juros como cobrados (cenário
                          de ataque restrito a encargos acessórios)
    capitalizacao       — "mensal": juros incorporam ao capital no fechamento da
                          competência. "nenhuma": juros vão a conta apartada e os
                          créditos os quitam primeiro (imputação do art. 354 do CC)
    convencao           — linear_mes (default) | linear_30 | exponencial_30

    Taxas em FRAÇÃO decimal mensal (0,03 = 3% a.m.). `taxa_da_competencia` passa
    pela guard_taxa de comum: 7.9 (pontos percentuais) levanta ValueError — o
    motor não adivinha escala.
    """
    nome: str
    condicao: str
    taxa: float | dict | None
    expurgar_rubricas: frozenset = frozenset()
    recompor_juros: bool = True
    capitalizacao: str = "mensal"
    convencao: str = CONVENCAO_PADRAO

    def taxa_da_competencia(self, comp: str) -> float:
        if not self.recompor_juros:
            return 0.0
        if isinstance(self.taxa, dict):
            if comp not in self.taxa:
                raise ValueError(
                    f"cenário {self.nome!r}: taxa da competência {comp} ausente do vetor "
                    f"— lacuna bloqueante (obter a série completa no conector)")
            return guard_taxa(float(self.taxa[comp]), f"cenário {self.nome!r}, taxa de {comp}")
        if self.taxa is None:
            raise ValueError("taxa ausente: nenhuma taxa comprovada nos documentos para este cenário, "
                             "que por isso não foi apurado (lacuna)")
        return guard_taxa(float(self.taxa), f"cenário {self.nome!r}, taxa")


def _cenarios_padrao(taxa_contratada: float | None,
                     taxa_media: dict | None,
                     rubricas_sem_lastro: frozenset,
                     convencao: str = CONVENCAO_PADRAO) -> list[CenarioConta]:
    """A trinca padrão da rota CONTA. A camada C4 declara a condição de
    aplicabilidade de cada um no entregável; nenhum é 'o certo' a priori."""
    return [
        CenarioConta(
            nome="C1_TAXA_MEDIA",
            condicao=("Taxa contratada abusiva (razão ≥ limiar) ou não comprovada "
                      "(Súmula 530/STJ): juros recompostos pela taxa média BACEN da "
                      "modalidade, capitalização mensal; encargos sem lastro expurgados"),
            taxa=taxa_media, expurgar_rubricas=rubricas_sem_lastro,
            recompor_juros=True, capitalizacao="mensal", convencao=convencao),
        CenarioConta(
            nome="C2_CAP_MENSAL",
            condicao=("Taxa contratada mantida; expurgo apenas da capitalização "
                      "diária não pactuada — juros recompostos pela taxa contratada "
                      "com incorporação mensal; encargos sem lastro expurgados"),
            taxa=taxa_contratada, expurgar_rubricas=rubricas_sem_lastro,
            recompor_juros=True, capitalizacao="mensal", convencao=convencao),
        CenarioConta(
            nome="C3_TAXA_LIMPA",
            condicao=("Juros e capitalização mantidos como cobrados; ataque restrito "
                      "aos encargos sem lastro contratual (tarifas, seguros, CP "
                      "disfarçada) e seu efeito composto no saldo"),
            taxa=None, expurgar_rubricas=rubricas_sem_lastro,
            recompor_juros=False, capitalizacao="mensal", convencao=convencao),
    ]


def recompor_cenario(lancs: list[Lancamento], saldo_inicial: float,
                     cen: CenarioConta, data_final: date | None = None,
                     data_inicial: date | None = None) -> dict:
    """Reconstrói a conta sob o cenário, dia a dia.

    Mecânica:
      - ENCARGO com rubrica em expurgar_rubricas: fora do fluxo (e o ESTORNO
        pareado pela mesma rubrica também, para não creditar duas vezes).
      - ENCARGO 'juros' (e 'mora' sobre o rotativo): expurgado quando
        recompor_juros=True; o motor recompõe pelo método hamburguês. O ESTORNO
        de juros/mora segue o MESMO tratamento do encargo pareado (simétrico):
        se o encargo saiu do fluxo, o estorno também sai — senão o estorno
        entraria como crédito no capital e o cliente receberia em dobro.
        `juros_cobrados` da competência já é líquido (encargo − estorno).
      - Crédito: quita primeiro os juros pendentes (art. 354 do CC), o restante
        amortiza o capital. Com capitalizacao='mensal' os juros incorporam no
        fechamento e a imputação é absorvida pelo saldo único.
      - Juros do dia incidem só sobre capital devedor; dia credor não rende.
      - Taxa-dia pela convenção do cenário (default linear_mes: i / dias do mês).

    Janela: ver `recompor_saldo_diario` (data_inicial = data do saldo inicial).

    Retorna dict com séries por competência e totais. 'excesso' > 0 significa
    que o banco cobrou mais do que o cenário admite.
    """
    if cen.capitalizacao not in ("mensal", "nenhuma"):
        raise ValueError(f"capitalizacao inválida: {cen.capitalizacao!r}")
    lancs = _ordenar(lancs)
    saldos_orig = recompor_saldo_diario(lancs, saldo_inicial, data_final, data_inicial)
    ini, fim = min(saldos_orig), max(saldos_orig)
    por_dia: dict[date, list[Lancamento]] = {}
    for l in lancs:
        por_dia.setdefault(l.data, []).append(l)

    td_cache: dict[str, float] = {}
    capital = saldo_inicial          # negativo = devedor
    juros_pend = 0.0                 # juros vencidos não capitalizados (>= 0)
    juros_mes = 0.0
    expurgado_por_rubrica: dict[str, float] = {}
    juros_cobrados_mes = 0.0
    competencias: list[dict] = []
    comp_atual = competencia(ini)

    def fechar_mes(comp: str):
        nonlocal capital, juros_pend, juros_mes, juros_cobrados_mes
        if cen.capitalizacao == "mensal":
            capital -= juros_mes
        else:
            juros_pend += juros_mes
        saldo_rev = capital - juros_pend
        # saldo original no fechamento da competência
        dfim = min(fim_do_mes(date.fromisoformat(comp + "-01")), fim)
        saldo_ori = saldos_orig[dfim]
        competencias.append({
            "competencia": comp,
            "juros_recompostos": round(juros_mes, 2),
            "juros_cobrados": round(juros_cobrados_mes, 2),
            "saldo_original": round(saldo_ori, 2),
            "saldo_revisado": round(saldo_rev, 2),
            "excesso_acumulado": round(saldo_rev - saldo_ori, 2),
        })
        juros_mes = 0.0
        juros_cobrados_mes = 0.0

    d = ini
    while d <= fim:
        comp = competencia(d)
        if comp != comp_atual:
            fechar_mes(comp_atual)
            comp_atual = comp
        for l in por_dia.get(d, []):
            # ENCARGO e ESTORNO de juros/mora recebem o mesmo tratamento (simetria)
            eh_juros = l.classe in ("ENCARGO", "ESTORNO") and l.rubrica in ("juros", "mora")
            if eh_juros and cen.recompor_juros:
                juros_cobrados_mes += l.valor if l.natureza == "D" else -l.valor
                continue  # expurgado: o motor recompõe
            if eh_juros and not cen.recompor_juros:
                juros_cobrados_mes += l.valor if l.natureza == "D" else -l.valor
                capital += l.delta
                continue
            if l.classe in ("ENCARGO", "ESTORNO") and l.rubrica in cen.expurgar_rubricas:
                if l.classe == "ENCARGO":
                    expurgado_por_rubrica[l.rubrica] = \
                        expurgado_por_rubrica.get(l.rubrica, 0.0) + l.delta * -1
                continue  # fora do fluxo (estorno pareado idem)
            if l.natureza == "C":
                v = l.valor
                if juros_pend > 0:               # art. 354: juros primeiro
                    quit = min(v, juros_pend)
                    juros_pend -= quit
                    v -= quit
                capital += v
            else:
                capital += l.delta
        if capital < 0:
            if comp not in td_cache:
                td_cache[comp] = _taxa_dia(cen.taxa_da_competencia(comp), cen.convencao, comp) \
                    if cen.recompor_juros else 0.0
            juros_mes += -capital * td_cache[comp]
        d += timedelta(days=1)
    fechar_mes(comp_atual)

    excesso_final = competencias[-1]["excesso_acumulado"]
    indebito = []
    anterior = 0.0
    for c in competencias:
        inc = round(c["excesso_acumulado"] - anterior, 2)
        anterior = c["excesso_acumulado"]
        if abs(inc) >= 0.01:
            indebito.append({
                "valor": inc,
                "data_inicial": fim_do_mes(date.fromisoformat(c["competencia"] + "-01")).isoformat(),
                "rotulo": f"excesso {c['competencia']}",
            })
        c["excesso_da_competencia"] = inc
    return {
        "cenario": cen.nome,
        "condicao": cen.condicao,
        "parametros": {
            "taxa": cen.taxa if not isinstance(cen.taxa, dict) else "vetor mensal",
            "recompor_juros": cen.recompor_juros,
            "capitalizacao": cen.capitalizacao,
            "convencao": cen.convencao,
            "expurgar_rubricas": sorted(cen.expurgar_rubricas),
        },
        "janela": {
            "data_inicial": ini.isoformat(), "data_final": fim.isoformat(),
            "convencao": JANELA_COM_DATA_INICIAL if data_inicial else JANELA_SEM_DATA_INICIAL,
        },
        "competencias": competencias,
        "expurgado_por_rubrica": {k: round(v, 2) for k, v in expurgado_por_rubrica.items()},
        "saldo_final_original": competencias[-1]["saldo_original"],
        "saldo_final_revisado": competencias[-1]["saldo_revisado"],
        "excesso_final": excesso_final,
        "favoravel": excesso_final > 0.005,
        "indebito_por_competencia": indebito,
    }


def rodar_trinca(lancs: list[Lancamento], saldo_inicial: float,
                 taxa_contratada: float | None, taxa_media: dict | None,
                 rubricas_sem_lastro: set | frozenset = frozenset(),
                 convencao: str = CONVENCAO_PADRAO,
                 data_final: date | None = None,
                 data_inicial: date | None = None) -> list[dict]:
    """Executa os três cenários padrão. Cenário sem insumo (ex.: sem taxa
    contratada comprovada) ou com taxa em escala implausível (guard_taxa) é
    omitido com registro do motivo — nunca estimado."""
    out = []
    for cen in _cenarios_padrao(taxa_contratada, taxa_media,
                                frozenset(rubricas_sem_lastro), convencao):
        try:
            out.append(recompor_cenario(lancs, saldo_inicial, cen, data_final, data_inicial))
        except ValueError as e:
            out.append({"cenario": cen.nome, "omitido": True, "motivo": str(e)})
    return out


# ─────────────────────────────────────────────────────────────────────
# 5. NEXO CRUZADO E ENCONTRO DE CONTAS
# ─────────────────────────────────────────────────────────────────────

def nexo_cruzado(lancs: list[Lancamento]) -> dict:
    """Agrupa débitos vinculados a contratos externos (contrato_ref).
    Esses valores NÃO são expurgados pelo motor: são reportados para o
    encontro de contas com a rota INSTRUMENTO (rota AMBAS)."""
    grupos: dict[str, dict] = {}
    for l in lancs:
        if not l.contrato_ref:
            continue
        g = grupos.setdefault(l.contrato_ref, {"total_debitado": 0.0, "lancamentos": 0,
                                               "primeiro": l.data, "ultimo": l.data})
        g["total_debitado"] += -l.delta
        g["lancamentos"] += 1
        g["primeiro"] = min(g["primeiro"], l.data)
        g["ultimo"] = max(g["ultimo"], l.data)
    return {ref: {**g, "total_debitado": round(g["total_debitado"], 2),
                  "primeiro": g["primeiro"].isoformat(), "ultimo": g["ultimo"].isoformat()}
            for ref, g in grupos.items()}


def encontro_de_contas(resultado_cenario: dict) -> dict:
    """Sumário do cenário para o entregável e para o atualizar_debito do conector.
    A modulação do dobro (Tema 929, corte em CORTE_TEMA_929 = 30/03/2021) é
    aplicada na camada C6 — o motor entrega a série datada e as duas bases.

    Bases:
      - os incrementos NEGATIVOS entram (abatem a base da fase em que caem), de
        modo que base_simples + base_dobro == excesso_final (2 casas);
      - a competência que CONTÉM o corte (2021-03) vai INTEIRA na base simples —
        critério de menor excesso (o incremento mensal não é datável dentro do
        mês); competências posteriores vão na base dobro.
    """
    comp_corte = competencia(CORTE_TEMA_929)
    simples = dobro_base = 0.0
    for i in resultado_cenario.get("indebito_por_competencia", []):
        comp = competencia(date.fromisoformat(i["data_inicial"]))
        if comp <= comp_corte:
            simples += i["valor"]
        else:
            dobro_base += i["valor"]
    return {
        "cenario": resultado_cenario["cenario"],
        "excesso_final": resultado_cenario["excesso_final"],
        "favoravel": resultado_cenario["favoravel"],
        "base_repeticao_simples": round(simples, 2),
        "base_repeticao_dobro": round(dobro_base, 2),
        "competencia_corte": comp_corte,
        "nota": ("valores nominais por competência; incrementos negativos abatem a base "
                 f"da respectiva fase (simples + dobro = excesso final); a competência "
                 f"{comp_corte}, que contém o corte de {CORTE_TEMA_929.isoformat()} (Tema 929), "
                 "entra inteira na base simples — critério de menor excesso; correção "
                 "monetária e a aplicação do dobro vão ao conector (atualizar_debito, "
                 "valores[]) na C6"),
    }


# ─────────────────────────────────────────────────────────────────────
# 6. BLOCO `conta` DO PAYLOAD
# ─────────────────────────────────────────────────────────────────────

def _copiar(origem: dict, chaves: tuple[str, ...], onde: str) -> dict:
    """Só as `chaves` que `origem` tem, copiadas (nenhuma referência compartilhada)."""
    if not isinstance(origem, dict):
        raise ValueError(f"{onde}: esperado dict, recebido {type(origem).__name__}")
    return {k: deepcopy(origem[k]) for k in chaves if k in origem}


def bloco_payload(reconciliacao: dict, trinca: list[dict], cenario_lider, encontro: dict,
                  series: list[dict], correcao: dict | None = None) -> dict:
    """Bloco `conta` do payload do renderizador (`ramo: "conta"`, ver
    `referencia/payload-schema.md`), montado das SAÍDAS dos motores — nenhum número é digitado.

    reconciliacao   saída de `reconciliar`
    trinca          saída de `rodar_trinca` (cenário omitido segue com `omitido` e `motivo`)
    cenario_lider   nome do cenário ("C1_TAXA_MEDIA") ou o dict dele, o mesmo que foi a
                    `encontro_de_contas`
    encontro        saída de `encontro_de_contas(cenario_lider)`
    series          [{serie, codigo, procedencia, periodo}] da consulta ao conector
    correcao        opcional: {valor_corrigido, data_final, indice, hash} do `atualizar_debito`

    Copia só os campos que o payload usa. Não julga o conteúdo: veredito DIVERGENTE, competência
    sem lançamento, líder omitido ou soma que não fecha seguem para o bloco e são RECUSADOS por
    `relatorios.validar` — a trava é uma só, no renderizador."""
    if not isinstance(trinca, list) or not isinstance(series, list):
        raise ValueError("trinca e series devem ser listas")
    rec = _copiar(reconciliacao, ("veredito", "pontos_conferidos", "divergencias",
                                  "competencias_sem_lancamento"), "reconciliacao")
    if "janela" in reconciliacao:
        rec["janela"] = _copiar(reconciliacao["janela"], ("data_inicial", "data_final"),
                                "reconciliacao.janela")
    cenarios = []
    for k, c in enumerate(trinca):
        omitido = isinstance(c, dict) and c.get("omitido")
        cenarios.append(_copiar(c, ("cenario", "omitido", "motivo") if omitido else
                                ("cenario", "condicao", "excesso_final", "favoravel"), f"trinca[{k}]"))
    bloco = {
        "reconciliacao": rec,
        "cenarios": cenarios,
        "cenario_lider": cenario_lider["cenario"] if isinstance(cenario_lider, dict) else cenario_lider,
        "encontro": _copiar(encontro, ("cenario", "excesso_final", "base_repeticao_simples",
                                       "base_repeticao_dobro", "competencia_corte", "nota"), "encontro"),
        "series": [_copiar(s, ("serie", "codigo", "procedencia", "periodo"), f"series[{k}]")
                   for k, s in enumerate(series)],
    }
    if correcao is not None:
        bloco["correcao"] = _copiar(correcao, ("valor_corrigido", "data_final", "indice", "hash"),
                                    "correcao")
    return bloco


# ─────────────────────────────────────────────────────────────────────
# 7. EXIBIÇÃO
# ─────────────────────────────────────────────────────────────────────

def brl(v: float) -> str:
    """'R$ 1.234,57' — delega a comum.brl_rs (Decimal, ROUND_HALF_UP, igual nos motores)."""
    return brl_rs(v)


# ─────────────────────────────────────────────────────────────────────
# 8. AUTOTESTE
# ─────────────────────────────────────────────────────────────────────

def _testes() -> tuple[int, int]:
    ok = fail = 0

    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond:
            ok += 1; print(f"  PASS  {nome} {extra}")
        else:
            fail += 1; print(f"  FAIL  {nome} {extra}")

    # ── CSV canônico ──────────────────────────────────────────────
    csv = (CSV_CABECALHO + "\n"
           "2025-01-05;TED RECEBIDA;C;10.000,00;MOVIMENTO;;;-5.000,00\n"
           "2025-01-02;SAQUE;D;15000;MOVIMENTO;;;\n")
    ls = carregar_csv(csv)
    chk("csv parseia e ordena por data", ls[0].data == date(2025, 1, 2))
    chk("csv aceita pt-BR e ponto decimal", ls[1].valor == 10000.0 and ls[0].valor == 15000.0)
    try:
        carregar_csv(CSV_CABECALHO + "\n2025-01-02;JUROS;D;100;ENCARGO;;;")
        chk("encargo sem rubrica é rejeitado", False)
    except ValueError:
        chk("encargo sem rubrica é rejeitado", True)

    # ── saldo diário ──────────────────────────────────────────────
    sal = recompor_saldo_diario(ls, saldo_inicial=0.0)
    chk("saldo diário: débito no dia 2", sal[date(2025, 1, 2)] == -15000.0)
    chk("saldo diário: dia sem movimento carrega", sal[date(2025, 1, 4)] == -15000.0)
    chk("saldo diário: crédito no dia 5", sal[date(2025, 1, 5)] == -5000.0)

    # ── reconciliação (guarda da extração) ────────────────────────
    rec = reconciliar(ls, saldo_inicial=0.0)
    chk("reconciliação CONFORME quando saldo bate",
        rec["veredito"] == "CONFORME" and rec["pontos_conferidos"] == 1)
    ls_adulterado = carregar_csv(
        CSV_CABECALHO + "\n2025-01-02;SAQUE;D;15000;MOVIMENTO;;;-14.000,00\n")
    rec2 = reconciliar(ls_adulterado, saldo_inicial=0.0)
    chk("reconciliação acusa lançamento extraído errado",
        rec2["veredito"] == "DIVERGENTE" and len(rec2["divergencias"]) == 1)
    ls_gap = carregar_csv(CSV_CABECALHO + "\n2025-01-02;A;D;100;MOVIMENTO;;;\n"
                          "2025-03-02;B;D;100;MOVIMENTO;;;\n")
    rec3 = reconciliar(ls_gap, saldo_inicial=0.0)
    chk("competência faltante vira lacuna bloqueante",
        rec3["competencias_sem_lancamento"] == ["2025-02"] and rec3["veredito"] == "DIVERGENTE")

    # ── SMD hamburguês (caso fechado à mão) ───────────────────────
    # jan/2025 (31 dias): devedor -3.100,00 do dia 1 ao 10 (10 dias); zero depois
    csv_smd = (CSV_CABECALHO + "\n"
               "2025-01-01;SAQUE;D;3100;MOVIMENTO;;;\n"
               "2025-01-11;DEPOSITO;C;3100;MOVIMENTO;;;\n"
               "2025-01-31;NADA;D;0;MOVIMENTO;;;\n")
    ls_smd = carregar_csv(csv_smd)
    s_smd = recompor_saldo_diario(ls_smd, 0.0)
    r_smd = smd_hamburgues(s_smd, "2025-01")
    chk("SMD dias corridos = 31.000/31 = 1.000", abs(r_smd["smd"] - 1000.0) < 1e-9,
        f"[{r_smd['smd']:.2f}]")
    r_smd2 = smd_hamburgues(s_smd, "2025-01", base="dias_devedores")
    chk("SMD dias devedores = 31.000/10 = 3.100", abs(r_smd2["smd"] - 3100.0) < 1e-9)
    chk("perfil da conta conta 10 dias devedores",
        perfil_conta(s_smd)["dias_devedores"] == 10)

    # ── juros hamburguês ──────────────────────────────────────────
    # SD constante 1.000 por 30 dias (abr), taxa 3% a.m. linear → 30 × 1000 × 0,001 = 30
    csv_j = CSV_CABECALHO + "\n2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n2025-04-30;M;D;0;MOVIMENTO;;;\n"
    s_j = recompor_saldo_diario(carregar_csv(csv_j), 0.0)
    j = juros_hamburgues(s_j, "2025-04", 0.03, "linear_30")
    chk("juros hamburguês linear fecha à mão", abs(j - 30.0) < 1e-9, f"[{j:.4f}]")
    j2 = juros_hamburgues(s_j, "2025-04", 0.03, "exponencial_30")
    chk("convenção exponencial < linear para mesma taxa", 0 < j2 < j)

    # ── cenário: recomposição básica ──────────────────────────────
    # banco cobrou 100 de juros; recomposto a 3% a.m. sobre SD 1.000 × 30d = 30 → excesso ≈ 70
    csv_c = (CSV_CABECALHO + "\n"
             "2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n"
             "2025-04-30;JUROS COBRADOS;D;100;ENCARGO;juros;;\n")
    ls_c = carregar_csv(csv_c)
    cen = CenarioConta("T", "teste", taxa=0.03)
    r = recompor_cenario(ls_c, 0.0, cen)
    chk("cenário expurga juros cobrados e recompõe",
        abs(r["competencias"][0]["juros_recompostos"] - 30.0) < 0.01)
    chk("excesso final = cobrado − recomposto", abs(r["excesso_final"] - 70.0) < 0.01,
        f"[{r['excesso_final']:.2f}]")
    chk("juros cobrados registrados por competência",
        r["competencias"][0]["juros_cobrados"] == 100.0)

    # ── capitalização mensal incorpora no fechamento ──────────────
    csv_2m = (CSV_CABECALHO + "\n"
              "2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n"
              "2025-05-30;FIM;D;0;MOVIMENTO;;;\n")
    r2m = recompor_cenario(carregar_csv(csv_2m), 0.0, CenarioConta("T", "t", taxa=0.03))
    # linear_mes (default): abr: 30 dias × 1000 × 0,03/30 = 30 → capital 1030;
    # mai (31 dias, série vai só até 30/05): 30 dias × 1030 × 0,03/31 = 927/31 = 29,90
    # (era 30,90 sob linear_30: 30 × 1030 × 0,001)
    chk("capitalização mensal: juros de maio sobre 1.030",
        abs(r2m["competencias"][1]["juros_recompostos"] - 29.90) < 0.01,
        f"[{r2m['competencias'][1]['juros_recompostos']:.2f}]")
    r2m30 = recompor_cenario(carregar_csv(csv_2m), 0.0,
                             CenarioConta("T", "t", taxa=0.03, convencao="linear_30"))
    chk("capitalização mensal (linear_30): juros de maio = 30 × 1.030 × 0,001 = 30,90",
        abs(r2m30["competencias"][1]["juros_recompostos"] - 30.90) < 0.01,
        f"[{r2m30['competencias'][1]['juros_recompostos']:.2f}]")

    # ── dia credor não rende ──────────────────────────────────────
    csv_cred = (CSV_CABECALHO + "\n"
                "2025-04-01;DEPOSITO;C;5000;MOVIMENTO;;;\n"
                "2025-04-30;FIM;D;0;MOVIMENTO;;;\n")
    r_cred = recompor_cenario(carregar_csv(csv_cred), 0.0, CenarioConta("T", "t", taxa=0.03))
    chk("saldo credor não gera juros", r_cred["competencias"][0]["juros_recompostos"] == 0.0)

    # ── imputação do art. 354 (capitalizacao='nenhuma') ───────────
    # abr: SD 1000 × 30d × 0,1% = 30 de juros pendentes; crédito de 30 em maio
    # deve quitar SÓ os juros — capital permanece 1.000 devedor
    csv_354 = (CSV_CABECALHO + "\n"
               "2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n"
               "2025-05-01;PAGTO;C;30;MOVIMENTO;;;\n"
               "2025-05-30;FIM;D;0;MOVIMENTO;;;\n")
    r354 = recompor_cenario(carregar_csv(csv_354), 0.0,
                            CenarioConta("T", "t", taxa=0.03, capitalizacao="nenhuma"))
    # maio: capital segue -1000 → juros de maio (linear_mes, 31 dias, série até 30/05)
    # = 30 × 1000 × 0,03/31 = 900/31 = 29,03 (era 30,00 sob linear_30)
    chk("art. 354: crédito quita juros antes do capital",
        abs(r354["competencias"][1]["juros_recompostos"] - 29.03) < 0.01,
        f"[{r354['competencias'][1]['juros_recompostos']:.2f}]")
    chk("art. 354: saldo revisado separa capital e juros pendentes",
        abs(r354["competencias"][1]["saldo_revisado"] - (-1029.03)) < 0.01,
        f"[{r354['competencias'][1]['saldo_revisado']:.2f}]")

    # ── expurgo de tarifa tem efeito composto ─────────────────────
    # banco: saque 1.000 + tarifa 500 no dia 1; cobra 45 de juros (3% s/ 1.500).
    # revisado (3% a.m., tarifa expurgada): juros = 30d × 1.000 × 0,1% = 30.
    # excesso = 500 (nominal) + 15 (juros sobre a tarifa) = 515.
    csv_tar = (CSV_CABECALHO + "\n"
               "2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n"
               "2025-04-01;TARIFA;D;500;ENCARGO;tarifa;;\n"
               "2025-04-30;JUROS;D;45;ENCARGO;juros;;\n")
    cen_t = CenarioConta("T", "t", taxa=0.03, expurgar_rubricas=frozenset({"tarifa"}))
    r_t = recompor_cenario(carregar_csv(csv_tar), 0.0, cen_t)
    chk("tarifa expurgada sai do fluxo e é totalizada",
        r_t["expurgado_por_rubrica"].get("tarifa") == 500.0)
    chk("excesso da tarifa > nominal (efeito composto)",
        abs(r_t["excesso_final"] - 515.0) < 0.01, f"[{r_t['excesso_final']:.2f}]")

    # ── estorno pareado com rubrica expurgada não duplica ─────────
    # juros mantidos como cobrados (C3): expurgo de tarifa + estorno pareado
    # deve zerar — se o estorno entrasse, haveria crédito em dobro (excesso -500).
    csv_est = (CSV_CABECALHO + "\n"
               "2025-04-01;SAQUE;D;1000;MOVIMENTO;;;\n"
               "2025-04-02;TARIFA;D;500;ENCARGO;tarifa;;\n"
               "2025-04-03;ESTORNO TARIFA;C;500;ESTORNO;tarifa;;\n"
               "2025-04-30;FIM;D;0;MOVIMENTO;;;\n")
    cen_t3 = CenarioConta("T3", "t", taxa=None, recompor_juros=False,
                          expurgar_rubricas=frozenset({"tarifa"}))
    r_est = recompor_cenario(carregar_csv(csv_est), 0.0, cen_t3)
    chk("estorno pareado também sai do fluxo (sem crédito em dobro)",
        abs(r_est["excesso_final"]) < 0.01, f"[{r_est['excesso_final']:.2f}]")

    # ── vetor de taxa média: competência faltante bloqueia ────────
    try:
        recompor_cenario(carregar_csv(csv_2m), 0.0,
                         CenarioConta("T", "t", taxa={"2025-04": 0.02}))
        chk("competência sem taxa no vetor é lacuna bloqueante", False)
    except ValueError:
        chk("competência sem taxa no vetor é lacuna bloqueante", True)

    # ── trinca padrão ─────────────────────────────────────────────
    tr = rodar_trinca(ls_c, 0.0, taxa_contratada=0.08,
                      taxa_media={"2025-04": 0.03}, rubricas_sem_lastro={"tarifa"})
    chk("trinca devolve os três cenários", [t["cenario"] for t in tr] ==
        ["C1_TAXA_MEDIA", "C2_CAP_MENSAL", "C3_TAXA_LIMPA"])
    chk("C1 (média 3%) mais favorável que C2 (contratada 8%)",
        tr[0]["excesso_final"] > tr[1]["excesso_final"])
    chk("C3 mantém juros cobrados (excesso zero sem encargo expurgável)",
        abs(tr[2]["excesso_final"]) < 0.01)
    tr2 = rodar_trinca(ls_c, 0.0, taxa_contratada=None,
                       taxa_media={"2025-04": 0.03})
    chk("cenário sem insumo é omitido com motivo, nunca estimado",
        tr2[1].get("omitido") is True and "taxa ausente" in tr2[1]["motivo"])

    # ── taxa média acima da contratada: cenário desfavorável sinalizado ──
    tr3 = rodar_trinca(ls_c, 0.0, taxa_contratada=0.02, taxa_media={"2025-04": 0.15})
    chk("cenário desfavorável sai com favoravel=False, não é escondido",
        tr3[0]["favoravel"] is False and tr3[0]["excesso_final"] < 0)

    # ── nexo cruzado e encontro de contas ─────────────────────────
    csv_nx = (CSV_CABECALHO + "\n"
              "2025-04-05;PARC CCB 123;D;800;MOVIMENTO;;CCB-123;\n"
              "2025-05-05;PARC CCB 123;D;800;MOVIMENTO;;CCB-123;\n")
    nx = nexo_cruzado(carregar_csv(csv_nx))
    chk("nexo cruzado agrupa por contrato", nx["CCB-123"]["total_debitado"] == 1600.0
        and nx["CCB-123"]["lancamentos"] == 2)
    ec = encontro_de_contas(r)
    chk("encontro de contas separa base simples/dobro pelo corte 30/03/2021",
        ec["base_repeticao_dobro"] == round(r["excesso_final"], 2)
        and ec["base_repeticao_simples"] == 0.0)

    # ── indébito por competência soma o excesso final ─────────────
    soma = sum(i["valor"] for i in r_t["indebito_por_competencia"])
    chk("série de indébito soma o excesso final",
        abs(soma - r_t["excesso_final"]) < 0.01)

    chk("brl pt-BR", brl(1234.5) == "R$ 1.234,50")
    chk("brl delega a comum.brl_rs (HALF_UP, negativo)",
        brl(0.125) == "R$ 0,13" and brl(-1500) == "R$ -1.500,00")

    # ═════════════════════════════════════════════════════════════════
    # Regressões v1.1.0 — valores fixos conferidos à mão
    # ═════════════════════════════════════════════════════════════════

    # ── (1) parse estrito de comum: '1.500' ambíguo e '1,234.56' en-US ──
    for ruim in ("1.500", "1,234.56"):
        try:
            carregar_csv(CSV_CABECALHO + f"\n2025-01-02;SAQUE;D;{ruim};MOVIMENTO;;;")
            chk(f"csv recusa número ambíguo {ruim!r}", False)
        except ValueError as e:
            chk(f"csv recusa número ambíguo {ruim!r} com a linha no erro",
                "linha 2" in str(e) and ruim in str(e), f"[{e}]")
    try:
        carregar_csv(CSV_CABECALHO + "\n2025-01-02;SAQUE;D;100;MOVIMENTO;;;1.500")
        chk("csv recusa saldo_informado ambíguo", False)
    except ValueError as e:
        chk("csv recusa saldo_informado ambíguo", "linha 2" in str(e))

    # ── (2) ESTORNO de juros simétrico ao ENCARGO ─────────────────────
    # saque 1.000 em 01/01/2024; juros 100 em 31/01; estorno juros 100 em 05/02.
    # C1 a 3% a.m. (linear_mes): jan 31 × 1000 × 0,03/31 = 30,00 → capital 1.030;
    # fev (29 dias): 5 × 1030 × 0,03/29 = 5,3276 → revisado -1.035,33;
    # original em 05/02 = -1.000 (o banco estornou o que cobrou) → excesso -35,33.
    # Sem a simetria, o estorno entraria como crédito de capital (dobro): +64,78.
    csv_ej = (CSV_CABECALHO + "\n"
              "2024-01-01;SAQUE;D;1000;MOVIMENTO;;;\n"
              "2024-01-31;JUROS;D;100;ENCARGO;juros;;\n"
              "2024-02-05;ESTORNO JUROS;C;100;ESTORNO;juros;;\n")
    tr_ej = rodar_trinca(carregar_csv(csv_ej), 0.0, taxa_contratada=None,
                         taxa_media={"2024-01": 0.03, "2024-02": 0.03})
    c1 = tr_ej[0]
    jc = sum(c["juros_cobrados"] for c in c1["competencias"])
    chk("estorno de juros: juros_cobrados líquidos no período = 0,00",
        c1["cenario"] == "C1_TAXA_MEDIA" and abs(jc) < 0.005, f"[{jc:.2f}]")
    chk("estorno de juros expurgado junto com o encargo: excesso_final = -35,33",
        abs(c1["excesso_final"] - (-35.33)) < 0.005, f"[{c1['excesso_final']:.2f}]")
    chk("estorno de juros: excesso de janeiro = 70,00 (1.100 − 1.030)",
        abs(c1["competencias"][0]["excesso_acumulado"] - 70.0) < 0.005)
    # C3 (juros mantidos): encargo e estorno entram ambos no capital → excesso 0
    chk("estorno de juros em C3 (juros mantidos) entra no capital como o encargo",
        abs(tr_ej[2]["excesso_final"]) < 0.005, f"[{tr_ej[2]['excesso_final']:.2f}]")

    # ── (3) janela: data_inicial do saldo informado ───────────────────
    # saldo_inicial -3.100 em 01/01/2024; único lançamento D 0,00 em 15/01.
    # jan/2024 (31 dias): 31 × 3.100 = 96.100 → SMD dias corridos 3.100,00
    ls_jan = carregar_csv(CSV_CABECALHO + "\n2024-01-15;NADA;D;0,00;MOVIMENTO;;;\n")
    s_jan = recompor_saldo_diario(ls_jan, -3100.0, data_final=date(2024, 1, 31),
                                  data_inicial=date(2024, 1, 1))
    r_jan = smd_hamburgues(s_jan, "2024-01")
    chk("data_inicial: SMD jan/2024 = 96.100/31 = 3.100,00, dias = 31",
        abs(r_jan["smd"] - 3100.0) < 1e-9 and r_jan["dias"] == 31
        and abs(r_jan["soma_saldos_devedores"] - 96100.0) < 1e-9,
        f"[smd {r_jan['smd']:.2f} dias {r_jan['dias']} soma {r_jan['soma_saldos_devedores']:.2f}]")
    s_jan0 = recompor_saldo_diario(ls_jan, -3100.0, data_final=date(2024, 1, 31))
    r_jan0 = smd_hamburgues(s_jan0, "2024-01")
    chk("sem data_inicial mantém o comportamento: começa no 1º lançamento (17 dias, 52.700)",
        r_jan0["dias"] == 17 and abs(r_jan0["soma_saldos_devedores"] - 52700.0) < 1e-9)
    try:
        recompor_saldo_diario(ls_jan, -3100.0, data_inicial=date(2024, 1, 20))
        chk("data_inicial posterior ao 1º lançamento é recusada", False)
    except ValueError:
        chk("data_inicial posterior ao 1º lançamento é recusada", True)
    rec_jan = reconciliar(ls_jan, -3100.0, data_inicial=date(2023, 12, 20))
    chk("reconciliar propaga data_inicial na régua de competências",
        rec_jan["competencias"] == ["2023-12", "2024-01"] and rec_jan["veredito"] == "CONFORME"
        and rec_jan["janela"]["data_inicial"] == "2023-12-20")
    tr_jan = rodar_trinca(ls_jan, -3100.0, taxa_contratada=None, taxa_media={"2024-01": 0.03},
                          data_final=date(2024, 1, 31), data_inicial=date(2024, 1, 1))
    # C1: 31 × 3.100 × 0,03/31 = 93,00 de juros recompostos
    chk("rodar_trinca propaga data_inicial: juros jan = 31 × 3.100 × 0,03/31 = 93,00",
        tr_jan[0]["janela"]["data_inicial"] == "2024-01-01"
        and abs(tr_jan[0]["competencias"][0]["juros_recompostos"] - 93.0) < 0.005,
        f"[{tr_jan[0]['competencias'][0]['juros_recompostos']:.2f}]")
    chk("janela declara a convenção quando data_inicial é None",
        "1º lançamento" in tr_ej[0]["janela"]["convencao"])

    # ── (4) ordenação estável por data ────────────────────────────────
    L = lambda d, nat, v, si=None: Lancamento(date.fromisoformat(d), "X", nat, v, "MOVIMENTO",
                                              saldo_informado=si)
    fora = [L("2025-01-05", "D", 100), L("2025-01-02", "C", 50), L("2025-01-10", "D", 30)]
    em_ordem = sorted(fora, key=lambda l: l.data)
    s_fora, s_ordem = recompor_saldo_diario(fora, 0.0), recompor_saldo_diario(em_ordem, 0.0)
    chk("recompor_saldo_diario ordena por data: [05,02,10] == ordenado; saldo 10/01 = -80",
        s_fora == s_ordem and s_fora[date(2025, 1, 10)] == -80.0
        and min(s_fora) == date(2025, 1, 2) and len(s_fora) == 9)
    chk("reconciliar ordena por data (mesmo resultado)",
        reconciliar(fora, 0.0) == reconciliar(em_ordem, 0.0))
    mesmo_dia = [L("2025-01-02", "D", 100, -100.0), L("2025-01-02", "C", 50, -50.0),
                 L("2025-01-01", "D", 0)]
    ordenado = sorted(mesmo_dia, key=lambda l: l.data)
    chk("ordenação estável preserva a ordem do CSV dentro do dia",
        [l.natureza for l in ordenado] == ["D", "D", "C"])

    # ── (5) convenção linear_mes (default) vs linear_30 ───────────────
    # saldo -1.000 constante em jan/2024 (31 dias), 3% a.m.
    ls_cv = carregar_csv(CSV_CABECALHO + "\n2024-01-01;SAQUE;D;1000;MOVIMENTO;;;\n")
    s_cv = recompor_saldo_diario(ls_cv, 0.0, data_final=date(2024, 1, 31))
    j_mes = juros_hamburgues(s_cv, "2024-01", 0.03)
    j_30 = juros_hamburgues(s_cv, "2024-01", 0.03, "linear_30")
    chk("linear_mes (default): 31 × 1.000 × 0,03/31 = 30,00", abs(j_mes - 30.0) < 1e-9,
        f"[{j_mes:.4f}]")
    chk("linear_30: 31 × 1.000 × 0,03/30 = 31,00", abs(j_30 - 31.0) < 1e-9, f"[{j_30:.4f}]")
    chk("CONVENCOES e defaults apontam para linear_mes",
        CONVENCOES == ("linear_mes", "linear_30", "exponencial_30")
        and CenarioConta("T", "t", taxa=0.03).convencao == "linear_mes"
        and _cenarios_padrao(0.03, None, frozenset())[0].convencao == "linear_mes"
        and abs(_taxa_dia(0.03, "linear_mes", "2024-02") - 0.03 / 29) < 1e-15
        and abs(_taxa_dia(0.03, "linear_mes", 29) - 0.03 / 29) < 1e-15)
    try:
        _taxa_dia(0.03, "linear_mes")
        chk("linear_mes sem competência é recusada", False)
    except ValueError:
        chk("linear_mes sem competência é recusada", True)

    # ── (6) encontro de contas: negativos entram; 2021-03 inteira na simples ──
    sint = {"cenario": "S", "excesso_final": 73.07, "favoravel": True,
            "indebito_por_competencia": [
                {"valor": 50.0, "data_inicial": "2021-02-28", "rotulo": "excesso 2021-02"},
                {"valor": 20.0, "data_inicial": "2021-03-31", "rotulo": "excesso 2021-03"},
                {"valor": 30.0, "data_inicial": "2021-04-30", "rotulo": "excesso 2021-04"},
                {"valor": -26.93, "data_inicial": "2021-05-31", "rotulo": "excesso 2021-05"}]}
    ec6 = encontro_de_contas(sint)
    chk("encontro: simples 70,00 (2021-02 + 2021-03 inteira), dobro 3,07 (30 − 26,93)",
        ec6["base_repeticao_simples"] == 70.0 and ec6["base_repeticao_dobro"] == 3.07,
        f"[{ec6['base_repeticao_simples']} / {ec6['base_repeticao_dobro']}]")
    chk("encontro: simples + dobro = excesso_final = 73,07",
        round(ec6["base_repeticao_simples"] + ec6["base_repeticao_dobro"], 2) == 73.07
        == ec6["excesso_final"] and "2021-03" in ec6["nota"] and "menor excesso" in ec6["nota"])

    # ── (7) guarda de escala: taxa 7.9 (pontos percentuais) ───────────
    tr79 = rodar_trinca(ls_c, 0.0, taxa_contratada=7.9, taxa_media={"2025-04": 0.03})
    chk("taxa_contratada=7.9 → C2 omitido com motivo 'fração decimal'",
        tr79[1]["cenario"] == "C2_CAP_MENSAL" and tr79[1].get("omitido") is True
        and "fração decimal" in tr79[1]["motivo"] and not tr79[0].get("omitido"),
        f"[{tr79[1].get('motivo', '')[:60]}]")
    try:
        CenarioConta("T", "t", taxa={"2025-04": 3.0}).taxa_da_competencia("2025-04")
        chk("vetor mensal em pontos percentuais é recusado", False)
    except ValueError as e:
        chk("vetor mensal em pontos percentuais é recusado", "fração decimal" in str(e))

    # ── (9) reconciliação por dia: só o último saldo_informado do dia ─
    # extrato: SAQUE 100 (saldo -100), DEP 50 (saldo -50) no mesmo dia.
    csv_inv = (CSV_CABECALHO + "\n"
               "2025-01-02;DEPOSITO;C;50;MOVIMENTO;;;\n"
               "2025-01-02;SAQUE;D;100;MOVIMENTO;;;-50,00\n")      # ordem invertida, saldo só no último
    r_inv = reconciliar(carregar_csv(csv_inv), 0.0)
    chk("intradia invertido com saldo só no último → CONFORME (fechamento -50)",
        r_inv["veredito"] == "CONFORME" and r_inv["pontos_conferidos"] == 1
        and r_inv["saldos_intradia_ignorados"] == 0)
    csv_inv2 = (CSV_CABECALHO + "\n"
                "2025-01-02;DEPOSITO;C;50;MOVIMENTO;;;-50,00\n"     # fechamento na 1ª linha
                "2025-01-02;SAQUE;D;100;MOVIMENTO;;;\n")
    r_inv2 = reconciliar(carregar_csv(csv_inv2), 0.0)
    chk("conferência diferida ao fim do dia (antes: 50 vs -50 = divergência falsa)",
        r_inv2["veredito"] == "CONFORME" and r_inv2["pontos_conferidos"] == 1)
    csv_ext = (CSV_CABECALHO + "\n"
               "2025-01-02;SAQUE;D;100;MOVIMENTO;;;-100,00\n"
               "2025-01-02;DEPOSITO;C;50;MOVIMENTO;;;-50,00\n")
    r_ext = reconciliar(carregar_csv(csv_ext), 0.0)
    chk("saldo intermediário do dia é ignorado (1 ignorado, 1 ponto, CONFORME)",
        r_ext["veredito"] == "CONFORME" and r_ext["saldos_intradia_ignorados"] == 1
        and r_ext["pontos_conferidos"] == 1)

    # ── bloco `conta` do payload: copia das saídas dos motores, sem número digitado ──
    serie_b = [{"serie": "Taxa média — modalidade de teste", "codigo": "000000",
                "procedencia": "teste", "periodo": "2025-04", "extra": "fora do payload"}]
    bloco = bloco_payload(reconciliar(ls_c, 0.0), tr, "C1_TAXA_MEDIA", encontro_de_contas(tr[0]), serie_b)
    chk("bloco_payload tem só os blocos do payload e o líder pelo nome",
        list(bloco) == ["reconciliacao", "cenarios", "cenario_lider", "encontro", "series"]
        and bloco["cenario_lider"] == "C1_TAXA_MEDIA" and "correcao" not in bloco)
    chk("bloco_payload copia os números da trinca e do encontro sem alterá-los",
        [c["cenario"] for c in bloco["cenarios"]] == [t["cenario"] for t in tr]
        and bloco["cenarios"][0]["excesso_final"] == tr[0]["excesso_final"]
        and bloco["encontro"]["base_repeticao_dobro"] == encontro_de_contas(tr[0])["base_repeticao_dobro"]
        and "parametros" not in bloco["cenarios"][0] and "extra" not in bloco["series"][0]
        and set(bloco["reconciliacao"]["janela"]) == {"data_inicial", "data_final"})
    bloco2 = bloco_payload(reconciliar(ls_c, 0.0), tr2, tr2[0], encontro_de_contas(tr2[0]), [],
                           {"valor_corrigido": 1.0, "data_final": "2025-05-30", "indice": "x", "hash": "h",
                            "memoria": "fora"})
    chk("bloco_payload aceita o dict do líder, preserva o omitido com motivo e a correção",
        bloco2["cenario_lider"] == "C1_TAXA_MEDIA" and bloco2["cenarios"][1] ==
        {"cenario": "C2_CAP_MENSAL", "omitido": True, "motivo": tr2[1]["motivo"]}
        and set(bloco2["correcao"]) == {"valor_corrigido", "data_final", "indice", "hash"})
    try:
        bloco_payload("não é dict", tr, "C1_TAXA_MEDIA", {}, [])
        chk("bloco_payload recusa reconciliação que não é dict", False)
    except ValueError:
        chk("bloco_payload recusa reconciliação que não é dict", True)

    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("conta_corrente", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    raise SystemExit(1 if autoteste()["falharam"] else 0)
