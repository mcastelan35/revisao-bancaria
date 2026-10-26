"""
calculo.py — núcleo determinístico da skill revisao-bancaria
Versão 1.3.0 · 2026-10-09

Substitui as fórmulas soltas da L3. Toda simulação de cenário DEVE passar por aqui.
Executar `python3 revisao.py autoteste --modulo calculo` roda a suíte de autoteste embutida.

Princípios:
  1. Precisão plena no cálculo; arredondamento apenas na exibição.
  2. Última parcela sempre fecha o saldo em zero (parcela de ajuste).
  3. Taxa nunca entra sem unidade declarada.
  4. Decote de encargo financiado: o VALOR PRESENTE do impacto é o próprio encargo;
     a soma nominal das diferenças de parcela já embute juros e não é valor presente —
     nunca corrigi-la monetariamente como se fosse.
  5. Nenhuma função presume dado ausente: levanta erro explícito.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .comum import brl, fim_do_mes, rodar_autoteste, saida_utf8  # brl: Decimal ROUND_HALF_UP, único para todos os motores

# ─────────────────────────────────────────────────────────────────────
# 1. NORMALIZAÇÃO DE TAXA
# ─────────────────────────────────────────────────────────────────────

UNIDADES = ("am_efetiva", "aa_efetiva", "aa_nominal")
LIMITE_ENTRADA_AM = 100.0    # % a.m. — acima disso é escala trocada
LIMITE_ENTRADA_AA = 2000.0   # % a.a. — rotativo chega a 400% a.a.; 2000% já é escala trocada


def normalizar_taxa(valor: float, unidade: str) -> float:
    """Converte qualquer taxa declarada para taxa mensal efetiva em decimal.

    unidade:
      "am_efetiva"  — 2.85 significa 2,85% ao mês efetivo
      "aa_efetiva"  — 40.10 significa 40,10% ao ano efetivo -> raiz 12
      "aa_nominal"  — 34.20 significa 34,20% ao ano nominal -> divisão por 12

    A escolha entre aa_efetiva e aa_nominal muda o resultado de forma material.
    Nunca inferir: a cláusula precisa ser lida e a unidade declarada pelo operador.

    Limite de entrada por unidade: mensal acima de 100% é erro de escala; anual
    admite até 2000% (cheque especial a 150% a.a. e rotativo a 400% a.a. existem).
    """
    if unidade not in UNIDADES:
        raise ValueError(f"unidade inválida: {unidade!r}. Use uma de {UNIDADES}")
    if valor is None:
        raise ValueError("taxa ausente — a skill não prossegue sem taxa (regra de conduta 1)")
    if valor < 0:
        raise ValueError(f"taxa negativa não admitida: {valor}")
    limite = LIMITE_ENTRADA_AM if unidade.startswith("am_") else LIMITE_ENTRADA_AA
    if valor > limite:
        raise ValueError(
            f"taxa de {valor}% ({unidade}) — provável erro de escala (decimal informado como "
            f"percentual? unidade trocada?). Limite de entrada: {limite}% para "
            f"{'mensal' if unidade.startswith('am_') else 'anual'}")

    r = valor / 100.0
    if unidade == "am_efetiva":
        return r
    if unidade == "aa_efetiva":
        return (1 + r) ** (1 / 12) - 1
    return r / 12  # aa_nominal


def mensal_para_anual_efetiva(r_mensal: float) -> float:
    return (1 + r_mensal) ** 12 - 1


# ─────────────────────────────────────────────────────────────────────
# 2. CONVENÇÃO DE PRAZO
# ─────────────────────────────────────────────────────────────────────

def prazo_em_periodos(inicio: date, fim: date, convencao: str = "meses_civis") -> float:
    """convencao: 'meses_civis' | 'dias_30_360' | 'dias_corridos'

    Em contratos longos as três divergem de forma material. A convenção adotada
    deve constar da seção de premissas do relatório.

    meses_civis — regra de fim de mês: se o dia de início não existe no mês de fim
    (31 vs 29), o último dia do mês de fim é o equivalente. 31/01→29/02 completa 1 mês;
    31/01→28/02/2024 não (28 não é o último dia de fevereiro bissexto).
    """
    if convencao == "meses_civis":
        n = (fim.year - inicio.year) * 12 + (fim.month - inicio.month)
        dia_equivalente = min(inicio.day, fim_do_mes(fim).day)
        if fim.day < dia_equivalente:
            n -= 1
        return float(n)
    dias = (fim - inicio).days
    if convencao == "dias_corridos":
        return dias / 30.0
    if convencao == "dias_30_360":
        d1 = min(inicio.day, 30)
        d2 = min(fim.day, 30) if d1 == 30 else fim.day
        return (((fim.year - inicio.year) * 360 + (fim.month - inicio.month) * 30 + (d2 - d1)) / 30.0)
    raise ValueError(f"convenção de prazo desconhecida: {convencao!r}")


# ─────────────────────────────────────────────────────────────────────
# 3. VALOR PRESENTE E CARÊNCIA
# ─────────────────────────────────────────────────────────────────────

def aplicar_carencia(pv: float, r: float, meses: int, capitaliza: bool = True) -> float:
    """Carência com juros capitalizados eleva o valor presente da série.
    Se os juros forem pagos durante a carência (capitaliza=False), o PV não muda.
    """
    if meses < 0:
        raise ValueError("carência negativa")
    return pv * (1 + r) ** meses if capitaliza else pv


# ─────────────────────────────────────────────────────────────────────
# 4. PRICE
# ─────────────────────────────────────────────────────────────────────

def pmt_price(pv: float, r: float, n: float, antecipado: bool = False) -> float:
    """Prestação do sistema francês.

    Guardas: r == 0 (divisão por zero) e n <= 0.
    antecipado=True para leasing e operações com 1ª parcela na contratação.
    """
    if n <= 0:
        raise ValueError(f"prazo inválido: n={n}")
    if pv <= 0:
        raise ValueError(f"valor presente inválido: pv={pv}")
    if r == 0:
        pmt = pv / n
    else:
        pmt = pv * r / (1 - (1 + r) ** -n)
    return pmt / (1 + r) if antecipado else pmt


def tabela_price(pv: float, r: float, n: int, antecipado: bool = False) -> list[dict]:
    """Tabela de amortização com parcela de ajuste na última competência.

    POSTECIPADO (padrão): juros em todo período, 1ª prestação em t=1. A última
    prestação é recalculada como saldo_anterior * (1 + r), garantindo saldo final
    exatamente zero mesmo com arredondamento a centavos.

    ANTECIPADO (leasing, 1ª parcela na contratação): a 1ª linha é em t0 — juros
    zero, prestação = amortização = PMT antecipada, saldo = pv − PMT; das linhas
    2..n a mecânica é a postecipada sobre o saldo já reduzido, e a última fecha
    como ajuste. Aplicar a PMT antecipada (annuity-due) na mecânica postecipada
    deixava um balão na última parcela.
    """
    n = int(n)
    pmt = pmt_price(pv, r, n, antecipado)
    saldo, linhas = pv, []
    for k in range(1, n + 1):
        if antecipado and k == 1:
            juros = 0.0                        # t0: nada correu ainda
            prestacao = pmt
            amort = pmt
            novo = 0.0 if n == 1 else saldo - amort
        else:
            juros = saldo * r
            if k == n:
                prestacao = saldo + juros      # parcela de ajuste
                amort = saldo
                novo = 0.0
            else:
                prestacao = pmt
                amort = prestacao - juros
                novo = saldo - amort
        linhas.append({"n": k, "saldo_inicial": saldo, "prestacao": prestacao,
                       "juros": juros, "amortizacao": amort, "saldo_final": novo})
        saldo = novo
    return linhas


# ─────────────────────────────────────────────────────────────────────
# 5. SAC
# ─────────────────────────────────────────────────────────────────────

def tabela_sac(pv: float, r: float, n: int) -> list[dict]:
    """Sistema de amortização constante.

    ATENÇÃO METODOLÓGICA: mantidos pv e n, a amortização é pv/n em qualquer taxa.
    Logo o SALDO DEVEDOR é idêntico nos cenários contratado e revisado — o que
    diverge é a PRESTAÇÃO. Relatórios de contrato SAC devem plotar a prestação,
    nunca duas curvas de saldo (elas se sobrepõem).
    """
    n = int(n)
    if n <= 0:
        raise ValueError(f"prazo inválido: n={n}")
    if pv <= 0:
        raise ValueError(f"valor presente inválido: pv={pv}")
    if r < 0:
        raise ValueError("taxa negativa")
    amort = pv / n
    saldo, linhas = pv, []
    for k in range(1, n + 1):
        juros = saldo * r
        a = saldo if k == n else amort      # fecha resíduo na última
        prestacao = a + juros
        novo = saldo - a
        linhas.append({"n": k, "saldo_inicial": saldo, "prestacao": prestacao,
                       "juros": juros, "amortizacao": a, "saldo_final": novo})
        saldo = novo
    return linhas



def tabela_tabelada(pv: float, r: float, percentuais: list[float]) -> list[dict]:
    """Cronograma TABELADO — o próprio instrumento fixa o percentual de amortização
    do saldo de principal em cada competência (ex.: sistemas de prestação variável — SPV —,
    planos de amortização variável, contratos com balão).

    NÃO arbitra sistema: os percentuais vêm do documento. Se o instrumento não os
    traz, isso é lacuna bloqueante (regra 0), não é caso de presumir Price ou SAC.

    percentuais: lista em pontos percentuais (1.71 = 1,71% do saldo de principal).
    A última competência é forçada a fechar o resíduo.
    """
    if not percentuais:
        raise ValueError("cronograma tabelado exige a lista de percentuais do instrumento")
    if pv <= 0:
        raise ValueError(f"valor presente inválido: pv={pv}")
    if r < 0:
        raise ValueError("taxa negativa")
    if any(p < 0 for p in percentuais):
        raise ValueError("percentual negativo no cronograma")
    saldo, linhas = pv, []
    n = len(percentuais)
    for k, pct in enumerate(percentuais, 1):
        juros = saldo * r
        a = saldo if k == n else saldo * (pct / 100.0)
        if a > saldo:
            a = saldo
        prestacao = a + juros
        novo = saldo - a
        linhas.append({"n": k, "saldo_inicial": saldo, "prestacao": prestacao,
                       "juros": juros, "amortizacao": a, "saldo_final": novo,
                       "pct_contratual": pct})
        saldo = novo
    return linhas


def amortizacao_negativa(linhas: list[dict]) -> dict:
    """Detecta competências em que a PRESTAÇÃO não cobre os juros do período
    (amortização < 0): a parcela de juros impagos é o que o credor incorpora ao
    saldo — e esse é o anatocismo real do SFH (TRF4 AC 5002846-95.2016.4.04.7112;
    STJ REsp 1.476.395/RS).

    Histórico (v1.3.0): até a v1.2.0 o critério era `amortizacao < juros`, que é a
    situação NORMAL do início de qualquer Price e gerava achado falso. Em cronograma
    tabelado (amortização = saldo × pct ≥ 0) a amortização negativa é impossível:
    o que ocorre ali é amortização LENTA, não negativa.
    """
    negativas = [l["n"] for l in linhas if l["amortizacao"] < 0]
    impagos = sum(-l["amortizacao"] for l in linhas if l["amortizacao"] < 0)
    return {"ocorre": bool(negativas), "competencias": negativas,
            "quantidade": len(negativas),
            "primeira": negativas[0] if negativas else None,
            "ultima": negativas[-1] if negativas else None,
            "juros_impagos_nominal": impagos}


# ─────────────────────────────────────────────────────────────────────
# 5-B. SFH / SFI — saldo indexado com prestação do documento
# ─────────────────────────────────────────────────────────────────────

ORDENS_SFH = ("corrige_antes", "amortiza_antes")
IMPAGOS_SFH = ("apartado", "incorporado")


def tabela_sfh(pv: float, r: float, indexador: list[float], prestacoes: list[float],
               ordem: str = "corrige_antes", juros_impagos: str = "apartado") -> dict:
    """Evolução do saldo em mútuo habitacional (SFH/SFI) com saldo indexado.

    NÃO presume nada: `indexador` (variação mensal do índice do saldo, decimal —
    TR/poupança/IPCA, série do conector Radar Apogeu) e `prestacoes` (valores
    efetivamente pagos, da conta gráfica ou do contrato/PES) vêm do documento.
    Comprimentos iguais, uma competência por posição.

    ordem:
      corrige_antes  — Súmula 450/STJ: atualiza o saldo, depois incide juros e
                       amortiza (regra do SFH).
      amortiza_antes — contrafactual para contratos fora do SFH ou para réplica.
    juros_impagos:
      apartado    — cenário revisado: juros não cobertos pela prestação vão a uma
                    conta apartada, só com correção pelo mesmo índice, sem novos
                    juros (TRF4 AC 5002846-95; STJ REsp 1.476.395/RS).
      incorporado — cenário do credor: juros impagos somam ao saldo e rendem juros
                    (é o anatocismo a demonstrar).

    Saída: linhas (competência a competência), saldo_final, conta_apartada
    (saldo corrigido dos juros impagos), amortizacao_negativa (resumo).
    """
    if ordem not in ORDENS_SFH:
        raise ValueError(f"ordem {ordem!r} inválida — use {ORDENS_SFH}")
    if juros_impagos not in IMPAGOS_SFH:
        raise ValueError(f"juros_impagos {juros_impagos!r} inválido — use {IMPAGOS_SFH}")
    if pv <= 0:
        raise ValueError(f"valor presente inválido: pv={pv}")
    if r < 0:
        raise ValueError("taxa negativa")
    if not indexador or not prestacoes:
        raise ValueError("tabela_sfh exige a série do indexador e as prestações do documento "
                         "(lacuna bloqueante — regra 0)")
    if len(indexador) != len(prestacoes):
        raise ValueError(f"indexador ({len(indexador)}) e prestações ({len(prestacoes)}) "
                         "precisam ter a mesma quantidade de competências")
    if any(p < 0 for p in prestacoes):
        raise ValueError("prestação negativa")
    saldo, apartada, linhas = pv, 0.0, []
    for k, (idx, prest) in enumerate(zip(indexador, prestacoes), 1):
        saldo_ini = saldo
        if ordem == "corrige_antes":
            saldo_corr = saldo * (1.0 + idx)
            juros = saldo_corr * r
            amort = prest - juros
            novo = saldo_corr - amort
        else:
            juros = saldo * r
            amort = prest - juros
            novo = (saldo - amort) * (1.0 + idx)
        impago = -amort if amort < 0 else 0.0
        apartada = apartada * (1.0 + idx)
        if impago > 0:
            if juros_impagos == "apartado":
                novo -= impago          # o saldo não absorve os juros impagos
                apartada += impago
            # incorporado: `novo` já contém o impago (amort negativa somou ao saldo)
        if novo < 0:
            novo = 0.0
        linhas.append({"n": k, "saldo_inicial": saldo_ini, "indexador": idx,
                       "saldo_corrigido": saldo_corr if ordem == "corrige_antes" else None,
                       "prestacao": prest, "juros": juros, "amortizacao": amort,
                       "juros_impagos": impago, "conta_apartada": apartada,
                       "saldo_final": novo})
        saldo = novo
    return {"ordem": ordem, "juros_impagos": juros_impagos, "linhas": linhas,
            "saldo_final": saldo, "conta_apartada": apartada,
            "amortizacao_negativa": amortizacao_negativa(linhas)}


def comparar_sfh(pv: float, r: float, indexador: list[float], prestacoes: list[float],
                 ordem: str = "corrige_antes") -> dict:
    """Credor (juros impagos incorporados) × revisado (conta apartada). A diferença
    entre `saldo_final + conta_apartada` dos dois cenários é exatamente o juro
    sobre juros impagos — o número que o laudo chama de anatocismo."""
    credor = tabela_sfh(pv, r, indexador, prestacoes, ordem, "incorporado")
    rev = tabela_sfh(pv, r, indexador, prestacoes, ordem, "apartado")
    divida_credor = credor["saldo_final"] + credor["conta_apartada"]
    divida_rev = rev["saldo_final"] + rev["conta_apartada"]
    return {"credor": credor, "revisado": rev,
            "divida_credor": divida_credor, "divida_revisada": divida_rev,
            "anatocismo": divida_credor - divida_rev,
            "favoravel": divida_credor > divida_rev,
            "ocorre_amortizacao_negativa": rev["amortizacao_negativa"]["ocorre"]}


# ─────────────────────────────────────────────────────────────────────
# 6. CENÁRIOS E DECOTE
# ─────────────────────────────────────────────────────────────────────

SISTEMAS = {"price": tabela_price, "sac": tabela_sac, "tabelado": tabela_tabelada}


@dataclass
class Cenario:
    sistema: str
    pv: float
    r: float
    n: int = 0
    antecipado: bool = False
    percentuais: list = field(default_factory=list)
    linhas: list = field(default_factory=list)

    def __post_init__(self):
        s = self.sistema.strip().lower()
        if s not in SISTEMAS:
            raise ValueError(f"sistema desconhecido: {self.sistema!r}. "
                             f"Use 'price', 'sac' ou 'tabelado'")
        self.sistema = s                       # normalizado: "SAC" e "sac" são o mesmo cenário
        if s == "tabelado":
            if not self.percentuais:
                raise ValueError("sistema tabelado exige percentuais extraídos do instrumento")
            self.linhas = tabela_tabelada(self.pv, self.r, self.percentuais)
            self.n = len(self.percentuais)
        elif s == "price":
            self.linhas = tabela_price(self.pv, self.r, self.n, self.antecipado)
        else:
            self.linhas = tabela_sac(self.pv, self.r, self.n)

    @property
    def total_pago(self): return sum(l["prestacao"] for l in self.linhas)
    @property
    def total_juros(self): return sum(l["juros"] for l in self.linhas)
    @property
    def saldo_final(self): return self.linhas[-1]["saldo_final"]


NOTA_REVISADO_MAIS_CARO = ("cenário revisado é mais caro que o contratado — reportar em "
                           "ressalvas, não esconder")


def comparar(contratado: Cenario, revisado: Cenario) -> dict:
    """Confronta prestação a prestação o cenário contratado com o revisado.

    `favoravel` é False quando a taxa revisada é MAIOR que a contratada (excesso
    total negativo): o resultado sai com `nota` e deve ir para as ressalvas do
    relatório — o mesmo tratamento de `conta_corrente`. Nunca sai sem sinalização.
    """
    sa, sb = contratado.sistema.strip().lower(), revisado.sistema.strip().lower()
    if sa != sb:
        raise ValueError("cenários devem usar o mesmo sistema de amortização")
    if contratado.n != revisado.n:
        raise ValueError("cenários devem ter o mesmo prazo")
    dif = [{"n": a["n"],
            "prestacao_contratada": a["prestacao"],
            "prestacao_revisada": b["prestacao"],
            "excesso": a["prestacao"] - b["prestacao"],
            "saldo_contratado": a["saldo_inicial"],
            "saldo_revisado": b["saldo_inicial"],
            "divergencia_saldo": a["saldo_inicial"] - b["saldo_inicial"]}
           for a, b in zip(contratado.linhas, revisado.linhas)]
    acc, total = [], 0.0
    for d in dif:
        total += d["excesso"]
        acc.append(total)
    favoravel = total > 0
    return {"linhas": dif, "excesso_acumulado": acc,
            "excesso_total": total,
            "favoravel": favoravel,
            "nota": None if favoravel else NOTA_REVISADO_MAIS_CARO,
            "plotar": "prestacao" if sa in ("sac", "tabelado") else "saldo",
            "saldos_coincidem": all(abs(d["divergencia_saldo"]) < 0.01 for d in dif)}


NOTA_DECOTE = ("impacto_nominal já contém os juros sobre o encargo ao longo do prazo; NÃO "
               "corrigir monetariamente o impacto_nominal como se fosse valor presente — para "
               "atualizar_debito use as diferenças parcela a parcela (diferencas_parcela) em "
               "suas datas")


def decotar_encargo_financiado(pv: float, r: float, n: int, encargo: float,
                               sistema: str = "price") -> dict:
    """Decote de tarifa/comissão que integrou o principal financiado.

    O VALOR PRESENTE do impacto é o próprio encargo, por construção: a diferença
    entre as duas séries de parcelas (PV com e sem o encargo), descontada à taxa do
    contrato, é exatamente `encargo` — vale para Price e para SAC. A soma NOMINAL
    das diferenças de parcela (`impacto_nominal`) é maior porque já contém os juros
    que o encargo rendeu ao longo do prazo.

    Por isso `impacto_nominal` NÃO é valor presente e NÃO pode ser corrigido
    monetariamente como se fosse. Para atualizar_debito, usar `diferencas_parcela`
    (uma por competência) em suas respectivas datas de vencimento.

    Devolve: {"valor_presente": encargo, "impacto_nominal": soma das diferenças,
              "diferencas_parcela": [dif_1, ..., dif_n], "razao": nominal/encargo,
              "valor_nominal": encargo (compatibilidade), "nota": NOTA_DECOTE}
    Cronograma tabelado não tem PMT fechada — `sistema="tabelado"` é ValueError.
    """
    s = sistema.strip().lower()
    if s not in ("price", "sac"):
        raise ValueError(f"decote exige Price ou SAC — sistema {sistema!r} não admitido "
                         "(cronograma tabelado não tem prestação fechada para recompor)")
    if encargo <= 0:
        raise ValueError("encargo deve ser positivo")
    if encargo >= pv:
        raise ValueError("encargo maior que o principal — verificar escala")
    com = Cenario(s, pv, r, n)
    sem = Cenario(s, pv - encargo, r, n)
    difs = [a["prestacao"] - b["prestacao"] for a, b in zip(com.linhas, sem.linhas)]
    impacto = sum(difs)
    return {"valor_presente": encargo,
            "impacto_nominal": impacto,
            "diferencas_parcela": difs,
            "razao": impacto / encargo,
            "valor_nominal": encargo,
            "nota": NOTA_DECOTE}


# `brl` vem de comum.py (Decimal, ROUND_HALF_UP) — resultado idêntico ao da versão local
# que existia aqui, agora numa única fonte para todos os motores.


# ─────────────────────────────────────────────────────────────────────
# 7. AUTOTESTE
# ─────────────────────────────────────────────────────────────────────

def _testes() -> tuple[int, int]:
    ok = fail = 0
    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond: ok += 1; print(f"  PASS  {nome} {extra}")
        else:    fail += 1; print(f"  FAIL  {nome} {extra}")

    P, n = 1926440.74, 61
    rc = normalizar_taxa(2.85, "am_efetiva")
    rr = normalizar_taxa(1.47, "am_efetiva")

    chk("normalizacao am", abs(rc - 0.0285) < 1e-12)
    chk("aa_nominal != aa_efetiva",
        abs(normalizar_taxa(34.20, "aa_nominal") - normalizar_taxa(34.20, "aa_efetiva")) > 1e-4,
        f"({normalizar_taxa(34.20,'aa_nominal')*100:.4f}% vs {normalizar_taxa(34.20,'aa_efetiva')*100:.4f}% a.m.)")

    for u in ("am_efetiva", "aa_efetiva"):
        try: normalizar_taxa(-1, u); chk(f"guarda taxa negativa {u}", False)
        except ValueError: chk(f"guarda taxa negativa {u}", True)
    try: normalizar_taxa(0.0285, "am_efetiva"); chk("aceita 0.0285 como 0,0285%", True, "(escala e responsabilidade do operador)")
    except ValueError: chk("escala", False)

    chk("price r=0 nao explode", abs(pmt_price(1200, 0.0, 12) - 100) < 1e-9)
    try: pmt_price(1000, 0.02, 0); chk("guarda n=0", False)
    except ValueError: chk("guarda n=0", True)

    tp = tabela_price(P, rc, n)
    chk("price fecha em zero", abs(tp[-1]["saldo_final"]) < 1e-9, f"(saldo={tp[-1]['saldo_final']:.10f})")
    chk("price soma amortizacao = PV", abs(sum(l["amortizacao"] for l in tp) - P) < 1e-6)

    ts = tabela_sac(P, rc, n)
    chk("sac fecha em zero", abs(ts[-1]["saldo_final"]) < 1e-9)
    chk("sac prestacao decrescente", all(ts[i]["prestacao"] > ts[i+1]["prestacao"] for i in range(n-1)))
    chk("sac soma amortizacao = PV", abs(sum(l["amortizacao"] for l in ts) - P) < 1e-6)

    cmp_price = comparar(Cenario("price", P, rc, n), Cenario("price", P, rr, n))
    chk("price: saldos divergem", not cmp_price["saldos_coincidem"])
    chk("price: plota saldo", cmp_price["plotar"] == "saldo")
    chk("price: excesso constante",
        abs(cmp_price["linhas"][0]["excesso"] - cmp_price["linhas"][n-2]["excesso"]) < 1e-6)

    cmp_sac = comparar(Cenario("sac", P, rc, n), Cenario("sac", P, rr, n))
    chk("sac: saldos coincidem", cmp_sac["saldos_coincidem"])
    chk("sac: plota prestacao", cmp_sac["plotar"] == "prestacao")
    chk("sac: excesso decrescente",
        all(cmp_sac["linhas"][i]["excesso"] > cmp_sac["linhas"][i+1]["excesso"] for i in range(n-1)))

    d = decotar_encargo_financiado(P, rc, n, P * 0.0275)
    chk("decote: impacto_nominal > valor_presente (juros sobre o encargo)", d["razao"] > 1.5,
        f"(VP R$ {brl(d['valor_presente'])} -> nominal R$ {brl(d['impacto_nominal'])}, {d['razao']:.2f}x)")

    chk("antecipado < postecipado", pmt_price(P, rc, n, True) < pmt_price(P, rc, n, False))
    chk("carencia eleva PV", aplicar_carencia(P, rc, 3) > P)

    p1 = prazo_em_periodos(date(2024,3,25), date(2029,4,27), "meses_civis")
    p2 = prazo_em_periodos(date(2024,3,25), date(2029,4,27), "dias_corridos")
    chk("convencoes de prazo divergem", abs(p1 - p2) > 0.5, f"({p1:.2f} vs {p2:.2f} periodos)")

    chk("brl formata pt-BR", brl(1926440.74) == "1.926.440,74", f"-> {brl(1926440.74)}")

    # --- cronograma tabelado (sistemas de percentual variável, ex.: SPV) ---
    pct = [1.71, 1.72, 1.72, 1.73] + [2.0] * 115 + [100.0]
    ct = tabela_tabelada(1_415_330.57, 0.0025, pct)
    chk("tabelado: uma linha por percentual", len(ct) == 120)
    chk("tabelado: fecha o saldo na ultima", abs(ct[-1]["saldo_final"]) < 0.01)
    chk("tabelado: aplica o percentual do instrumento",
        abs(ct[0]["amortizacao"] - 1_415_330.57 * 0.0171) < 0.01)
    cen_t = Cenario("tabelado", 1_415_330.57, 0.0025, percentuais=pct)
    chk("tabelado: Cenario infere n dos percentuais", cen_t.n == 120)
    _lacuna = False
    try:
        Cenario("tabelado", 1000.0, 0.01)
    except ValueError:
        _lacuna = True
    chk("tabelado sem percentuais e lacuna bloqueante", _lacuna)
    _an = amortizacao_negativa(tabela_tabelada(100_000.0, 0.05, [0.5] * 9 + [100.0]))
    chk("tabelado NAO e amortizacao negativa (amortizacao lenta, >= 0)", not _an["ocorre"])
    _an_p = amortizacao_negativa(tabela_price(1000.0, 0.02, 12))
    chk("price regular: amortizacao < juros no inicio NAO e negativa (v1.2.0 acusava)", not _an_p["ocorre"])

    # ── item 11 (v1.3.0): tabela_sfh — fixture calculada a mao, independente do motor ──
    # PV 1.000, 1% a.m., indexador 2%/mes, prestacao 5 (abaixo dos juros): forca negativa.
    # Mes 1: saldo_corr 1.020,00; juros 10,20; amort -5,20.
    #   apartado:    saldo 1.020,00; apartada 5,20
    #   incorporado: saldo 1.025,20
    # Mes 2 apartado: corr 1.040,40; juros 10,404; amort -5,404; saldo 1.040,40;
    #   apartada 5,20*1,02 + 5,404 = 10,708
    # Mes 2 incorporado: corr 1.045,704; juros 10,45704; amort -5,45704; saldo 1.051,16104
    # anatocismo = (1.051,16104) - (1.040,40 + 10,708) = 0,05304
    sfh_ap = tabela_sfh(1000.0, 0.01, [0.02, 0.02], [5.0, 5.0])
    chk("sfh apartado: saldo mes 1 = 1.020,00 (Sumula 450: corrige antes)",
        abs(sfh_ap["linhas"][0]["saldo_final"] - 1020.0) < 1e-9)
    chk("sfh apartado: juros mes 1 = 10,20 sobre o saldo corrigido",
        abs(sfh_ap["linhas"][0]["juros"] - 10.2) < 1e-9)
    chk("sfh apartado: conta apartada mes 2 = 10,708",
        abs(sfh_ap["conta_apartada"] - 10.708) < 1e-9, f"(= {sfh_ap['conta_apartada']:.6f})")
    chk("sfh apartado: saldo mes 2 = 1.040,40", abs(sfh_ap["saldo_final"] - 1040.4) < 1e-9)
    chk("sfh: detecta amortizacao negativa nas 2 competencias",
        sfh_ap["amortizacao_negativa"]["ocorre"] and sfh_ap["amortizacao_negativa"]["quantidade"] == 2)
    sfh_inc = tabela_sfh(1000.0, 0.01, [0.02, 0.02], [5.0, 5.0], juros_impagos="incorporado")
    chk("sfh incorporado: saldo mes 2 = 1.051,16104",
        abs(sfh_inc["saldo_final"] - 1051.16104) < 1e-9, f"(= {sfh_inc['saldo_final']:.6f})")
    cmp_sfh = comparar_sfh(1000.0, 0.01, [0.02, 0.02], [5.0, 5.0])
    chk("comparar_sfh: anatocismo = 0,05304 (juros sobre juros impagos)",
        abs(cmp_sfh["anatocismo"] - 0.05304) < 1e-9, f"(= {cmp_sfh['anatocismo']:.6f})")
    # sem amortizacao negativa os cenarios coincidem
    cmp_ok = comparar_sfh(1000.0, 0.01, [0.02, 0.02], [20.0, 20.0])
    chk("comparar_sfh: prestacao que cobre os juros -> anatocismo zero",
        abs(cmp_ok["anatocismo"]) < 1e-9 and not cmp_ok["ocorre_amortizacao_negativa"])
    # ordem amortiza_antes: mes 1 com prestacao 20 -> (1000 - 10) * 1,02 = 1.009,80
    sfh_am = tabela_sfh(1000.0, 0.01, [0.02], [20.0], ordem="amortiza_antes")
    chk("sfh amortiza_antes: saldo = 1.009,80 (contrafactual)",
        abs(sfh_am["saldo_final"] - 1009.8) < 1e-9)
    chk("sfh corrige_antes: saldo = 1.010,20 > amortiza_antes",
        abs(tabela_sfh(1000.0, 0.01, [0.02], [20.0])["saldo_final"] - 1010.2) < 1e-9)
    for args, nome in (((1000.0, 0.01, [], [5.0]), "sem indexador"),
                       ((1000.0, 0.01, [0.02], [5.0, 5.0]), "comprimentos diferentes")):
        try:
            tabela_sfh(*args); chk(f"sfh guarda {nome}", False)
        except ValueError:
            chk(f"sfh guarda {nome} e lacuna bloqueante", True)

    # ── item 9: Price antecipado (annuity-due) sem balao na ultima ──
    # PV 1.000, 2% a.m., n=12: PMT postecipada 94,5596 / 1,02 = 92,7055
    ta = tabela_price(1000.0, 0.02, 12, antecipado=True)
    chk("price antecipado: PMT = 92,7055", abs(ta[0]["prestacao"] - 92.7055) < 5e-5,
        f"({ta[0]['prestacao']:.4f})")
    chk("price antecipado: 1a linha em t0 sem juros, saldo = PV - PMT",
        ta[0]["juros"] == 0.0 and ta[0]["amortizacao"] == ta[0]["prestacao"]
        and abs(ta[0]["saldo_final"] - (1000.0 - 92.7055)) < 5e-5)
    chk("price antecipado: 2a linha cobra juros sobre o saldo reduzido",
        abs(ta[1]["juros"] - (1000.0 - 92.7055) * 0.02) < 5e-6)
    chk("price antecipado: ultima prestacao entre 92,70 e 92,71 (sem balao)",
        92.70 < ta[-1]["prestacao"] < 92.71, f"({ta[-1]['prestacao']:.4f})")
    chk("price antecipado: fecha em zero", abs(ta[-1]["saldo_final"]) < 0.005)
    chk("price antecipado: soma amortizacao = PV", abs(sum(l["amortizacao"] for l in ta) - 1000.0) < 1e-6)
    chk("price antecipado: 12 linhas", len(ta) == 12)
    chk("price postecipado nao mudou: 1a linha cobra juros",
        abs(tabela_price(1000.0, 0.02, 12)[0]["juros"] - 20.0) < 1e-12)

    # ── item 10: limite de entrada por unidade ──
    # (1 + 4)^(1/12) - 1 = 0,1435298 (14,353% a.m.)
    chk("400% a.a. efetiva (rotativo) -> 14,353% a.m.",
        abs(normalizar_taxa(400, "aa_efetiva") - 0.14352984) < 1e-7,
        f"({normalizar_taxa(400, 'aa_efetiva'):.7f})")
    chk("150% a.a. efetiva (cheque especial) aceita",
        abs(normalizar_taxa(150, "aa_efetiva") - (2.5 ** (1 / 12) - 1)) < 1e-12)
    chk("400% a.a. nominal -> 33,33% a.m.", abs(normalizar_taxa(400, "aa_nominal") - 4 / 12) < 1e-12)
    for _v, _u in ((150, "am_efetiva"), (2500, "aa_efetiva"), (2001, "aa_nominal")):
        try:
            normalizar_taxa(_v, _u); chk(f"normalizar_taxa({_v}, {_u}) levanta", False)
        except ValueError:
            chk(f"normalizar_taxa({_v}, {_u}) levanta", True)

    # ── item 11: sistema normalizado ──
    cA, cB = Cenario("SAC", 1000.0, 0.02, 12), Cenario("sac", 1000.0, 0.02, 12)
    chk("Cenario('SAC') e Cenario('sac') equivalem", cA.sistema == "sac" and cA.linhas == cB.linhas)
    cmp_mix = comparar(cA, Cenario(" Sac ", 1000.0, 0.01, 12))
    chk("comparar com 'SAC' x ' Sac ' plota prestacao", cmp_mix["plotar"] == "prestacao")
    chk("Cenario('Price') plota saldo",
        comparar(Cenario("Price", 1000.0, 0.02, 12), Cenario("PRICE", 1000.0, 0.01, 12))["plotar"] == "saldo")

    # ── item 12: revisado mais caro nao sai sem sinalizacao ──
    cmp_inv = comparar(Cenario("price", P, rr, n), Cenario("price", P, rc, n))
    chk("revisado mais caro: excesso_total < 0, favoravel False e nota",
        cmp_inv["excesso_total"] < 0 and cmp_inv["favoravel"] is False
        and cmp_inv["nota"] == NOTA_REVISADO_MAIS_CARO)
    chk("revisado mais barato: favoravel True e nota None",
        cmp_price["favoravel"] is True and cmp_price["nota"] is None)

    # ── item 13: decote — valor presente = encargo; nominal = 48 x diferenca de PMT ──
    # PMT(50.000; 2%; 48) = 1.630,0918  PMT(53.000) = 1.727,8973  dif = 97,8055  x48 = 4.694,6643
    d2 = decotar_encargo_financiado(50_000.0, 0.02, 48, 3_000.0)
    chk("decote: valor_presente = encargo = 3.000,00", d2["valor_presente"] == 3000.0)
    chk("decote: impacto_nominal = 4.694,6643", abs(d2["impacto_nominal"] - 4694.6643) < 1e-4,
        f"({d2['impacto_nominal']:.4f})")
    chk("decote: impacto_nominal == 48 x (PMT 53.000 - PMT 50.000)",
        abs(d2["impacto_nominal"] - 48 * (pmt_price(53_000.0, 0.02, 48) - pmt_price(50_000.0, 0.02, 48))) < 1e-6)
    chk("decote: 48 diferencas de parcela, constantes no Price",
        len(d2["diferencas_parcela"]) == 48
        and max(d2["diferencas_parcela"]) - min(d2["diferencas_parcela"]) < 1e-6)
    chk("decote: VP das diferencas a 2% a.m. = encargo (prova da construcao)",
        abs(sum(x / (1.02 ** k) for k, x in enumerate(d2["diferencas_parcela"], 1)) - 3000.0) < 1e-6)
    chk("decote: nota alerta contra corrigir o nominal", "NÃO corrigir" in d2["nota"] and d2["nota"] == NOTA_DECOTE)
    chk("decote: chaves antigas enganosas removidas", "impacto_recomposto" not in d2 and "subestimacao" not in d2)
    d3 = decotar_encargo_financiado(50_000.0, 0.02, 48, 3_000.0, sistema="SAC")
    chk("decote SAC: VP das diferencas = encargo",
        abs(sum(x / (1.02 ** k) for k, x in enumerate(d3["diferencas_parcela"], 1)) - 3000.0) < 1e-6)
    try:
        decotar_encargo_financiado(50_000.0, 0.02, 48, 3_000.0, sistema="tabelado")
        chk("decote tabelado e recusado", False)
    except ValueError as e:
        chk("decote tabelado e recusado", "decote exige Price ou SAC" in str(e))

    # ── item 14: meses civis com regra de fim de mes ──
    chk("31/01/2024 -> 29/02/2024 = 1 mes", prazo_em_periodos(date(2024, 1, 31), date(2024, 2, 29)) == 1.0)
    chk("31/01/2024 -> 28/02/2024 = 0 (28 nao e o ultimo dia de fev bissexto)",
        prazo_em_periodos(date(2024, 1, 31), date(2024, 2, 28)) == 0.0)
    chk("30/01/2024 -> 29/02/2024 = 1", prazo_em_periodos(date(2024, 1, 30), date(2024, 2, 29)) == 1.0)
    chk("31/01/2024 -> 01/03/2024 = 1", prazo_em_periodos(date(2024, 1, 31), date(2024, 3, 1)) == 1.0)
    chk("31/01/2023 -> 28/02/2023 = 1 (ano nao bissexto)", prazo_em_periodos(date(2023, 1, 31), date(2023, 2, 28)) == 1.0)
    chk("25/03/2024 -> 27/04/2029 = 61 (inalterado)", p1 == 61.0)

    # ── item 15: brl de comum ──
    chk("brl HALF_UP via comum", brl(0.125) == "0,13" and brl(1234.565) == "1.234,57" and brl(-1500) == "-1.500,00")

    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("calculo", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    print("Autoteste — motores/calculo.py v1.3.0\n")
    raise SystemExit(1 if autoteste()["falharam"] else 0)
