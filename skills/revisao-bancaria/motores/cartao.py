"""
cartao.py — análise de faturas de cartão de crédito
Versão 1.1.0 · 2026-09-20 · complementa calculo.py

Cartão de crédito não é série de prestações. Não use Price nem SAC aqui.
A dívida rola de fatura em fatura com encargos variáveis por competência, e a
única fonte probatória disponível costuma ser a própria fatura — raramente há
instrumento contratual. A fatura é obrigada a informar a taxa de juros; é dela
que a taxa deve ser extraída, nunca estimada.

REGRA INEGOCIÁVEL — PROIBIÇÃO DE PRESUNÇÃO
    Nenhuma função deste módulo aceita valor ausente. Campo faltante levanta
    DadoAusente com o nome do campo e a competência. Não há default, não há
    interpolação, não há estimativa. Origem admissível de dado: (a) extraído do
    documento, (b) informado pelo usuário. Não existe terceira origem.

Formatação pt-BR, competências e marco do teto vêm de comum.py.

Executar `python3 revisao.py autoteste --modulo cartao` roda a suíte de autoteste embutida.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date

from .comum import brl as _brl_comum, fim_do_mes, MARCO_TETO_CARTAO, rodar_autoteste, saida_utf8

# ─────────────────────────────────────────────────────────────────────
# Marco legal
# ─────────────────────────────────────────────────────────────────────

#: Lei 14.690/2023, art. 28, §1º + Resolução CMN 5.112/2023.
#: Teto de 100% do valor original da dívida sobre juros e demais encargos
#: financeiros no rotativo e no parcelamento de fatura. IOF fica de fora.
#: Aplica-se às OPERAÇÕES posteriores ao marco, independentemente da data de
#: assinatura do contrato de cartão. Cada competência de rotativo é uma
#: operação (R23): o teto alcança as competências a partir do marco mesmo
#: quando a dívida começou antes dele.
VIGENCIA_TETO_14690 = MARCO_TETO_CARTAO   # date(2024, 1, 3) — fonte única em comum.py


def teto_aplicavel(data_operacao: date) -> bool:
    if not isinstance(data_operacao, date):
        raise DadoAusente("data_operacao", None, "necessária para aferir o marco MT06")
    return data_operacao >= VIGENCIA_TETO_14690


def competencia_no_teto(comp: str) -> bool:
    """A competência entra no cômputo do teto quando seu último dia é >= marco
    (2024-01 entra: contém 03/01/2024; 2023-12 não)."""
    ano, mes = _parse_comp(comp)
    return fim_do_mes(date(ano, mes, 1)) >= VIGENCIA_TETO_14690


# ─────────────────────────────────────────────────────────────────────
# Erros
# ─────────────────────────────────────────────────────────────────────

class DadoAusente(Exception):
    """Levantado sempre que falta dado. Nunca substituir por estimativa."""

    def __init__(self, campo: str, competencia: str | None, motivo: str = ""):
        self.campo, self.competencia, self.motivo = campo, competencia, motivo
        onde = f" na competência {competencia}" if competencia else ""
        extra = f" — {motivo}" if motivo else ""
        super().__init__(
            f"Dado ausente: '{campo}'{onde}{extra}. "
            f"Solicitar ao usuário o documento ou a informação. Presunção é vedada."
        )


def exigir(valor, campo: str, competencia: str | None = None, motivo: str = ""):
    if valor is None:
        raise DadoAusente(campo, competencia, motivo)
    return valor


# ─────────────────────────────────────────────────────────────────────
# Competências
# ─────────────────────────────────────────────────────────────────────

def _parse_comp(c: str) -> tuple[int, int]:
    try:
        a, m = c.split("-")
        ano, mes = int(a), int(m)
    except Exception:
        raise ValueError(f"competência fora do formato AAAA-MM: {c!r}")
    if not 1 <= mes <= 12:
        raise ValueError(f"mês inválido em {c!r}")
    return ano, mes


def _ordinal(c: str) -> int:
    a, m = _parse_comp(c)
    return a * 12 + (m - 1)


def _de_ordinal(o: int) -> str:
    return f"{o // 12:04d}-{o % 12 + 1:02d}"


def competencias_faltantes(comps: list[str]) -> list[str]:
    if not comps:
        return []
    ords = sorted(_ordinal(c) for c in comps)
    presentes = set(ords)
    return [_de_ordinal(o) for o in range(ords[0], ords[-1] + 1) if o not in presentes]


def _ordenadas(faturas: list["Fatura"], contexto: str = "faturas") -> list["Fatura"]:
    """Ordena por competência e recusa série vazia ou competência duplicada
    (duas faturas do mesmo mês = extração repetida ou competência errada:
    regra 0, conferir antes de somar)."""
    if not faturas:
        raise DadoAusente(contexto, None, "nenhuma fatura recebida")
    vistas: set[str] = set()
    for f in faturas:
        if f.competencia in vistas:
            raise ValueError(
                f"competência duplicada na série: {f.competencia} — extração repetida ou "
                f"competência errada; conferir as faturas antes de prosseguir (regra 0)")
        vistas.add(f.competencia)
    return sorted(faturas, key=lambda f: _ordinal(f.competencia))


# ─────────────────────────────────────────────────────────────────────
# Fatura
# ─────────────────────────────────────────────────────────────────────

#: Tolerância da conferência aritmética da fatura (centavos de arredondamento).
TOLERANCIA_FATURA = 0.05


@dataclass
class Fatura:
    """Uma competência de fatura. Todos os campos vêm da fatura ou do usuário.

    Semântica dos campos (é a que `detectar_candidatos`, `entrou_no_rotativo`
    e `evolucao_divida` já usam):
      saldo_anterior — saldo que ENTROU nesta competência, já líquido do
                       pagamento da fatura anterior (= total anterior − pagamento anterior)
      compras        — compras/lançamentos do período
      encargos       — juros do rotativo + demais encargos financeiros, SEM IOF.
                       O IOF é apartado porque a Res. CMN 5.112 o exclui do teto.
      iof            — IOF do período
      total_fatura   — total desta fatura
      pagamento      — pagamento efetuado CONTRA esta fatura (após o fechamento);
                       o saldo rolado para a próxima é total_fatura − pagamento
      taxa_informada_am — taxa de juros do rotativo impressa na fatura, em % a.m.
                       A fatura é obrigada a informá-la. Se estiver ilegível, é
                       lacuna, não é caso de estimar pela média BACEN.

    Regra 0 — consistência aritmética: |total_fatura − (saldo_anterior + compras +
    encargos + iof)| deve ficar dentro de TOLERANCIA_FATURA; divergência é extração
    inconsistente (encargos com vírgula deslocada, campo trocado) e levanta
    ValueError com a competência e a diferença. O pagamento não entra na
    identidade porque, nesta semântica, é posterior ao total.
    """
    competencia: str
    saldo_anterior: float
    compras: float
    pagamento: float
    encargos: float
    iof: float
    total_fatura: float
    taxa_informada_am: float | None = None

    def __post_init__(self):
        _parse_comp(self.competencia)
        for nome in ("saldo_anterior", "compras", "pagamento", "encargos", "iof", "total_fatura"):
            exigir(getattr(self, nome), nome, self.competencia)
            if getattr(self, nome) < 0:
                raise ValueError(f"{nome} negativo em {self.competencia}")
        esperado = self.saldo_anterior + self.compras + self.encargos + self.iof
        dif = self.total_fatura - esperado
        if abs(dif) > TOLERANCIA_FATURA:
            raise ValueError(
                f"regra 0: extração inconsistente, conferir a fatura — competência "
                f"{self.competencia}: total_fatura {self.total_fatura:.2f} difere de "
                f"saldo_anterior + compras + encargos + iof = {esperado:.2f} "
                f"(diferença {dif:+.2f}; tolerância {TOLERANCIA_FATURA:.2f})")

    @property
    def entrou_no_rotativo(self) -> bool:
        """Pagamento inferior ao total da fatura anterior implica rolagem."""
        return self.pagamento < self.total_fatura


# ─────────────────────────────────────────────────────────────────────
# Segmentação da série
# ─────────────────────────────────────────────────────────────────────

def segmentar_serie(faturas: list[Fatura]) -> dict:
    """Divide a série em trechos contínuos e reporta as competências faltantes.

    Decisão de projeto: buraco na série NÃO interrompe o trabalho e NÃO é
    interpolado. Analisa-se cada trecho contínuo, marca-se o corte e lista-se
    o que falta para fechar a análise.
    """
    ordenadas = _ordenadas(faturas)          # vazio → DadoAusente; duplicada → ValueError
    faltantes = competencias_faltantes([f.competencia for f in ordenadas])

    trechos, atual = [], [ordenadas[0]]
    for ant, prox in zip(ordenadas, ordenadas[1:]):
        if _ordinal(prox.competencia) - _ordinal(ant.competencia) == 1:
            atual.append(prox)
        else:
            trechos.append(atual)
            atual = [prox]
    trechos.append(atual)

    return {
        "trechos": trechos,
        "qtd_trechos": len(trechos),
        "competencias_faltantes": faltantes,
        "serie_completa": len(faltantes) == 0,
        "cobertura": f"{ordenadas[0].competencia} a {ordenadas[-1].competencia}",
        "alerta_documentos": (
            f"Série descontínua. Faltam {len(faltantes)} competência(s): "
            f"{', '.join(faltantes)}. A análise abrange apenas os {len(trechos)} trecho(s) "
            f"contínuo(s); solicitar as faturas faltantes para fechar o período."
        ) if faltantes else None,
    }


# ─────────────────────────────────────────────────────────────────────
# Detecção de eventos — apenas CANDIDATOS
# ─────────────────────────────────────────────────────────────────────

def detectar_candidatos(faturas: list[Fatura], tolerancia: float = 0.02) -> list[dict]:
    """Sinaliza competências que PODEM conter parcelamento ou renegociação.

    Nunca classifica. A saída é lista de candidatos para confirmação do usuário.
    Heurística: descontinuidade entre o saldo anterior declarado e o saldo
    esperado pela aritmética da fatura precedente.
    """
    out = []
    ordenadas = _ordenadas(faturas)
    for ant, atual in zip(ordenadas, ordenadas[1:]):
        if _ordinal(atual.competencia) - _ordinal(ant.competencia) != 1:
            continue
        esperado = ant.total_fatura - ant.pagamento
        divergencia = atual.saldo_anterior - esperado
        base = max(abs(esperado), 1.0)
        if abs(divergencia) / base > tolerancia:
            out.append({
                "competencia": atual.competencia,
                "saldo_esperado": esperado,
                "saldo_declarado": atual.saldo_anterior,
                "divergencia": divergencia,
                "divergencia_pct": divergencia / base * 100,
                "hipoteses": (["parcelamento de fatura", "renegociação", "portabilidade", "estorno"]
                              if divergencia < 0 else
                              ["encargo lançado fora do campo de encargos", "compra retroativa", "estorno revertido"]),
                "status": "CANDIDATO — requer confirmação do usuário",
                "acao": "Perguntar ao usuário o que ocorreu nesta competência antes de classificar.",
            })
    return out


# ─────────────────────────────────────────────────────────────────────
# Evolução da dívida — a bola de neve
# ─────────────────────────────────────────────────────────────────────

def evolucao_divida(faturas: list[Fatura]) -> dict:
    """Reconstrói a formação da dívida: onde começou e como cresceu.

    Devolve, por competência, o acumulado de encargos e a participação deles no
    saldo — que é a leitura mais eloquente para o cliente.
    Série vazia levanta DadoAusente; competência duplicada, ValueError.
    """
    ordenadas = _ordenadas(faturas)
    origem = next((f.competencia for f in ordenadas if f.entrou_no_rotativo), None)

    acumulado = acumulado_iof = 0.0
    linhas = []
    for f in ordenadas:
        acumulado += f.encargos
        acumulado_iof += f.iof
        saldo = f.total_fatura - f.pagamento
        linhas.append({
            "competencia": f.competencia,
            "saldo_anterior": f.saldo_anterior,
            "compras": f.compras,
            "pagamento": f.pagamento,
            "encargos": f.encargos,
            "iof": f.iof,
            "total_fatura": f.total_fatura,
            "saldo_rolado": saldo,
            "encargos_acumulados": acumulado,
            "participacao_encargos_no_saldo": (acumulado / saldo * 100) if saldo > 0 else None,
            "taxa_informada_am": f.taxa_informada_am,
        })

    primeira, ultima = ordenadas[0], ordenadas[-1]
    saldo_final = ultima.total_fatura - ultima.pagamento
    taxas = [f.taxa_informada_am for f in ordenadas if f.taxa_informada_am is not None]

    return {
        "linhas": linhas,
        "origem_rotativo": origem,
        "competencias": len(ordenadas),
        "encargos_totais": acumulado,
        "iof_total": acumulado_iof,
        "saldo_inicial": primeira.saldo_anterior,
        "saldo_final": saldo_final,
        "crescimento_absoluto": saldo_final - primeira.saldo_anterior,
        "multiplicador": (saldo_final / primeira.saldo_anterior) if primeira.saldo_anterior > 0 else None,
        "taxa_min_am": min(taxas) if taxas else None,
        "taxa_max_am": max(taxas) if taxas else None,
        "competencias_sem_taxa": [f.competencia for f in ordenadas if f.taxa_informada_am is None],
    }


# ─────────────────────────────────────────────────────────────────────
# Teto da Lei 14.690
# ─────────────────────────────────────────────────────────────────────

RESSALVA_NOVAS_DIVIDAS = (
    "admissível apurado sobre valor original único; compras novas roladas constituem "
    "dívida própria com teto próprio (Res. CMN 5.112/2023, art. 2º, §1º) — informar "
    "`novas_dividas` quando houver")


def teto_lei_14690(valor_original: float, faturas: list[Fatura],
                   data_operacao: date | None = None,
                   novas_dividas: list[tuple[str, float]] | None = None) -> dict:
    """Aplica o teto de 100% do valor original sobre juros e encargos.

    valor_original: definido em gate com o usuário logo após o envio das
        faturas. Não é inferido — a Res. CMN 5.112 define o conceito, mas a
        identificação do saldo que entrou no rotativo depende de confirmação.
    IOF não entra no cômputo.

    Marco (MT06, R23): só competências cujo último dia é >= 03/01/2024 entram
        no cômputo (cada competência de rotativo é uma operação). As anteriores
        saem em `competencias_excluidas_pre_marco` com `nota`. Se a série é
        inteiramente pré-marco, `aplicavel: False`. `data_operacao` anterior ao
        marco NÃO afasta o teto das competências posteriores — só é registrada.

    novas_dividas: [(competência, valor)] — dívidas novas constituídas (compras
        roladas) ao longo da série. O admissível na competência C é a soma dos
        valores originais constituídos até C (valor_original + novas com
        competência <= C). Sem o parâmetro, o resultado leva `ressalva`.
    """
    exigir(valor_original, "valor_original_divida", None,
           "fixar em gate com o usuário após o envio das faturas")
    if valor_original <= 0:
        raise ValueError("valor_original_divida deve ser positivo")
    ordenadas = _ordenadas(faturas)          # vazio → DadoAusente; duplicada → ValueError

    novas: list[tuple[int, str, float]] = []
    for comp_n, valor_n in (novas_dividas or []):
        _parse_comp(comp_n)
        exigir(valor_n, "nova_divida.valor", comp_n)
        if valor_n <= 0:
            raise ValueError(f"nova dívida em {comp_n} deve ser positiva")
        novas.append((_ordinal(comp_n), comp_n, float(valor_n)))

    def teto_em(comp: str) -> float:
        o = _ordinal(comp)
        return valor_original + sum(v for on, _, v in novas if on <= o)

    excluidas = [f.competencia for f in ordenadas if not competencia_no_teto(f.competencia)]
    no_teto = [f for f in ordenadas if competencia_no_teto(f.competencia)]
    nota_marco = (
        f"Competências anteriores ao marco de {VIGENCIA_TETO_14690.isoformat()} (MT06) "
        f"não entram no cômputo do teto: {', '.join(excluidas)}. O teto não retroage; "
        f"cada competência de rotativo posterior é operação própria (R23)."
    ) if excluidas else None
    nota_operacao = (
        f"data_operacao {data_operacao.isoformat()} é anterior ao marco; o teto alcança "
        f"apenas as competências a partir de {VIGENCIA_TETO_14690.isoformat()} (R23: cada "
        f"competência de rotativo é uma operação)."
    ) if data_operacao is not None and not teto_aplicavel(data_operacao) else None
    ressalva = None if novas_dividas is not None else RESSALVA_NOVAS_DIVIDAS

    if not no_teto:
        origem = (f"Operação em {data_operacao.isoformat()} e " if data_operacao else "") + \
                 f"série {ordenadas[0].competencia} a {ordenadas[-1].competencia}"
        return {"aplicavel": False,
                "motivo": f"{origem} anterior a {VIGENCIA_TETO_14690.isoformat()} "
                          f"(marco MT06). O teto não retroage.",
                "competencias_excluidas_pre_marco": excluidas, "nota": nota_marco,
                "ressalva": ressalva,
                "linhas": [], "encargos_cobrados_total": 0.0,
                "encargos_admissiveis_total": 0.0, "excesso_total": 0.0}

    acum_permitido = acum_cobrado = acum_excesso = 0.0
    linhas, estouro = [], None

    for f in no_teto:
        teto_c = teto_em(f.competencia)
        admissivel = max(0.0, teto_c - acum_permitido)
        permitido = min(f.encargos, admissivel)
        excesso = f.encargos - permitido
        acum_cobrado += f.encargos
        acum_permitido += permitido
        acum_excesso += excesso
        if excesso > 0 and estouro is None:
            estouro = f.competencia
        linhas.append({
            "competencia": f.competencia,
            "teto_da_competencia": teto_c,
            "encargos_cobrados": f.encargos,
            "encargos_admissiveis": permitido,
            "excesso": excesso,
            "excesso_acumulado": acum_excesso,
            "cobrado_acumulado": acum_cobrado,
            "margem_restante_do_teto": max(0.0, teto_c - acum_permitido),
            "iof_apartado": f.iof,
        })

    teto_final = teto_em(no_teto[-1].competencia)
    return {
        "aplicavel": True,
        "valor_original": valor_original,
        "teto": teto_final,
        "novas_dividas": [(c, v) for _, c, v in sorted(novas)],
        "encargos_cobrados_total": acum_cobrado,
        "encargos_admissiveis_total": acum_permitido,
        "excesso_total": acum_excesso,
        "competencia_estouro": estouro,
        "percentual_cobrado_sobre_original": acum_cobrado / teto_final * 100,
        "competencias_excluidas_pre_marco": excluidas,
        "nota": " ".join(n for n in (nota_marco, nota_operacao) if n) or None,
        "ressalva": ressalva,
        "linhas": linhas,
        "fundamento": "Lei 14.690/2023, art. 28 + Resolução CMN 5.112/2023 (marco MT06, regra R23)",
    }


METODO_EXCESSO_POR_TAXA = "nominal por competência, sem efeito composto — critério de menor excesso"


def excesso_por_taxa(faturas: list[Fatura], taxa_teto_am: float) -> dict:
    """Excesso apurado por taxa, para quando a discussão for a taxa e não o teto.

    taxa_teto_am em % a.m. — vem da média BACEN da competência ou de limite
    judicial. Base de incidência: saldo_anterior da própria fatura.

    Método: NOMINAL por competência, sem efeito composto — o excesso de cada mês
    é encargos − saldo_anterior × taxa, somado sem recompor o saldo revisado
    (que reduziria a base dos meses seguintes e ampliaria o excesso). É o
    critério de menor excesso; a recomposição composta, se cabível, é cenário
    à parte e deve ser declarada como tal.
    """
    exigir(taxa_teto_am, "taxa_teto_am", None, "informar a taxa de referência")
    r = taxa_teto_am / 100.0
    acum = 0.0
    linhas = []
    for f in _ordenadas(faturas):
        admissivel = f.saldo_anterior * r
        exc = max(0.0, f.encargos - admissivel)
        acum += exc
        linhas.append({"competencia": f.competencia, "base": f.saldo_anterior,
                       "encargos_cobrados": f.encargos, "encargos_admissiveis": admissivel,
                       "excesso": exc, "excesso_acumulado": acum,
                       "taxa_efetiva_apurada_am": (f.encargos / f.saldo_anterior * 100)
                       if f.saldo_anterior > 0 else None})
    return {"taxa_teto_am": taxa_teto_am, "excesso_total": acum, "linhas": linhas,
            "metodo": METODO_EXCESSO_POR_TAXA}


# ─────────────────────────────────────────────────────────────────────
# Gráfico — excesso por competência e acumulado
# ─────────────────────────────────────────────────────────────────────

def svg_excesso(linhas: list[dict], largura: int = 640, altura: int = 240) -> str:
    """Barras = excesso da competência. Linha = excesso acumulado.

    Paleta do chassi canônico: tinta #16150F, ouro #A8842C, régua #EDEAE0.
    Sem legenda embutida — o figcaption do template cuida disso.
    """
    if not linhas:
        raise DadoAusente("linhas", None, "nada a plotar")
    n = len(linhas)
    plot_h, base_y, pad_r = altura - 40, altura - 40, 20
    plot_w = largura - pad_r

    maxb = max((l["excesso"] for l in linhas), default=0.0) or 1.0
    maxa = max((l["excesso_acumulado"] for l in linhas), default=0.0) or 1.0
    passo = plot_w / n
    lb = min(passo * 0.62, 26)

    barras, pontos = [], []
    for i, l in enumerate(linhas):
        x = i * passo + (passo - lb) / 2
        h = (l["excesso"] / maxb) * (plot_h * 0.78)
        if h > 0:
            barras.append(f'<rect x="{x:.1f}" y="{base_y-h:.1f}" width="{lb:.1f}" '
                          f'height="{h:.1f}" fill="#16150F" opacity="0.82"/>')
        px = i * passo + passo / 2
        py = base_y - (l["excesso_acumulado"] / maxa) * (plot_h * 0.90)
        pontos.append(f"{px:.1f},{py:.1f}")

    grade = "".join(
        f'<line x1="0" y1="{base_y - plot_h*f:.1f}" x2="{plot_w}" y2="{base_y - plot_h*f:.1f}" '
        f'stroke="#EDEAE0" stroke-width="1"/>' for f in (0.25, 0.5, 0.75, 1.0)
    )
    rotulos = "".join(
        f'<text x="{i*passo+passo/2:.1f}" y="{altura-8}" font-family="JetBrains Mono" '
        f'font-size="6.5" fill="#9C978A" text-anchor="middle">{linhas[i]["competencia"][2:]}</text>'
        for i in range(n) if n <= 18 or i % max(1, n // 12) == 0
    )
    return (
        f'<svg viewBox="0 0 {largura} {altura}" width="100%" role="img" '
        f'aria-label="Excesso de encargos por competência e acumulado">'
        f'{grade}{"".join(barras)}'
        f'<polyline fill="none" stroke="#A8842C" stroke-width="1.8" points="{" ".join(pontos)}"/>'
        f'<line x1="0" y1="{base_y}" x2="{plot_w}" y2="{base_y}" stroke="#16150F" stroke-width="1"/>'
        f'{rotulos}</svg>'
    )


def brl(v: float) -> str:
    """'1.926.440,74' sem prefixo — delega a comum.brl (Decimal, ROUND_HALF_UP)."""
    return _brl_comum(v)


# ─────────────────────────────────────────────────────────────────────
# Autoteste
# ─────────────────────────────────────────────────────────────────────

def _amostra() -> list[Fatura]:
    """Série sintética apenas para autoteste — jamais usar como dado de caso."""
    dados = [
        # comp,     sant,    compras, pgto,   enc,    iof,   total,  taxa
        ("2024-02", 12000.0, 1800.0,  1500.0,  0.0,     0.0, 13800.0, 12.5),
        ("2024-03", 12300.0, 900.0,   1200.0, 1537.5,  92.3, 14829.8, 12.5),
        ("2024-04", 13629.8, 600.0,   1000.0, 1703.7, 102.2, 16035.7, 12.5),
        ("2024-05", 15035.7, 400.0,    800.0, 1879.5, 112.8, 17428.0, 12.5),
        ("2024-06", 16628.0, 300.0,    700.0, 2078.5, 124.7, 19131.2, 12.5),
        ("2024-07", 18431.2, 200.0,    600.0, 2303.9, 138.2, 21073.3, 12.5),
    ]
    return [Fatura(c, sa, cp, pg, en, io, tt, tx) for c, sa, cp, pg, en, io, tt, tx in dados]


def _fat(comp: str, sant: float, compras: float, pgto: float, enc: float, iof: float,
         taxa: float | None = None) -> Fatura:
    """Fatura aritmeticamente consistente (total = sant + compras + enc + iof) — só autoteste."""
    return Fatura(comp, sant, compras, pgto, enc, iof, sant + compras + enc + iof, taxa)


def _serie(comps: list[str], sant: float, enc: float, compras: float = 0.0,
           pgto: float = 0.0) -> list[Fatura]:
    """Série encadeada e consistente: saldo_anterior(k+1) = total(k) − pagamento(k)."""
    out = []
    for c in comps:
        f = _fat(c, sant, compras, pgto, enc, 0.0)
        out.append(f)
        sant = f.total_fatura - f.pagamento
    return out


def _testes() -> tuple[int, int]:
    ok = fail = 0
    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond: ok += 1; print(f"  PASS  {nome} {extra}")
        else:    fail += 1; print(f"  FAIL  {nome} {extra}")

    fs = _amostra()

    # proibição de presunção
    try:
        Fatura("2024-08", 100.0, 0.0, 0.0, None, 0.0, 100.0); chk("campo None e rejeitado", False)
    except DadoAusente as e:
        chk("campo None e rejeitado", True, f"({e.campo})")
    try:
        teto_lei_14690(None, fs); chk("valor_original None e rejeitado", False)
    except DadoAusente: chk("valor_original None e rejeitado", True)
    try:
        excesso_por_taxa(fs, None); chk("taxa None e rejeitada", False)
    except DadoAusente: chk("taxa None e rejeitada", True)

    # marco temporal
    chk("teto nao retroage", teto_aplicavel(date(2023, 12, 31)) is False)
    chk("teto vigente em 03/01/2024", teto_aplicavel(date(2024, 1, 3)) is True)
    # v1.1.0: data_operacao anterior ao marco NAO afasta o teto das competencias
    # posteriores (R23: cada competencia de rotativo e uma operacao). A serie fs
    # (2024-02..2024-07) e toda pos-marco → aplicavel True com nota.
    fora = teto_lei_14690(12000.0, fs, data_operacao=date(2023, 6, 1))
    chk("operacao anterior com serie pos-marco aplica as competencias posteriores",
        fora["aplicavel"] is True and "2023-06-01" in fora["nota"]
        and fora["competencias_excluidas_pre_marco"] == [])
    pre = [_fat("2023-06", 1000.0, 0.0, 0.0, 100.0, 0.0), _fat("2023-07", 1100.0, 0.0, 0.0, 100.0, 0.0)]
    fora2 = teto_lei_14690(1000.0, pre, data_operacao=date(2023, 6, 1))
    chk("serie inteiramente pre-marco nao aplica",
        fora2["aplicavel"] is False and fora2["competencias_excluidas_pre_marco"] == ["2023-06", "2023-07"]
        and fora2["excesso_total"] == 0.0)

    # segmentacao
    seg = segmentar_serie(fs)
    chk("serie continua sem falta", seg["serie_completa"] and seg["qtd_trechos"] == 1)
    buraco = [f for f in fs if f.competencia != "2024-04"]
    seg2 = segmentar_serie(buraco)
    chk("buraco detectado sem interpolar",
        seg2["competencias_faltantes"] == ["2024-04"] and seg2["qtd_trechos"] == 2,
        f"({seg2['qtd_trechos']} trechos)")
    chk("alerta de documentos emitido", seg2["alerta_documentos"] is not None)

    # candidatos — a fatura alterada precisa ser internamente consistente (regra 0,
    # v1.1.0); o candidato vem do saldo_anterior 9.000 ≠ 16.035,7 − 1.000 esperado
    alterada = list(fs)
    alterada[3] = Fatura("2024-05", 9000.0, 400.0, 800.0, 1879.5, 112.8, 11392.3, 12.5)
    cands = detectar_candidatos(alterada)
    chk("candidato sinalizado", len(cands) >= 1 and cands[0]["status"].startswith("CANDIDATO"))
    chk("candidato nao classifica", all("hipoteses" in c for c in cands))
    chk("serie coerente sem candidato", len(detectar_candidatos(fs)) == 0)

    # evolucao
    ev = evolucao_divida(fs)
    chk("origem do rotativo identificada", ev["origem_rotativo"] == "2024-02", f"({ev['origem_rotativo']})")
    chk("encargos acumulados somam", abs(ev["encargos_totais"] - sum(f.encargos for f in fs)) < 1e-6,
        f"(R$ {brl(ev['encargos_totais'])})")
    chk("multiplicador calculado", ev["multiplicador"] > 1,
        f"({ev['multiplicador']:.2f}x em {ev['competencias']} competencias)")
    chk("iof apartado dos encargos", ev["iof_total"] > 0 and ev["iof_total"] not in (ev["encargos_totais"],))
    chk("competencias sem taxa listadas", ev["competencias_sem_taxa"] == [])

    # teto — ramo em que o teto ainda NAO foi atingido
    folga = teto_lei_14690(12000.0, fs, data_operacao=date(2024, 2, 1))
    chk("teto igual ao valor original", folga["teto"] == 12000.0)
    chk("dentro do teto nao gera excesso",
        folga["excesso_total"] == 0 and folga["competencia_estouro"] is None,
        f"(cobrado {folga['percentual_cobrado_sobre_original']:.1f}% do original)")
    chk("margem restante decresce",
        folga["linhas"][-1]["margem_restante_do_teto"] < folga["linhas"][0]["margem_restante_do_teto"])

    # teto — ramo em que o teto e ESTOURADO
    t = teto_lei_14690(6000.0, fs, data_operacao=date(2024, 2, 1))
    chk("excesso apurado", t["excesso_total"] > 0, f"(R$ {brl(t['excesso_total'])})")
    chk("competencia de estouro identificada", t["competencia_estouro"] is not None,
        f"({t['competencia_estouro']})")
    chk("admissiveis nunca superam o teto", t["encargos_admissiveis_total"] <= t["teto"] + 1e-9)
    chk("cobrado = admissivel + excesso",
        abs(t["encargos_cobrados_total"] - t["encargos_admissiveis_total"] - t["excesso_total"]) < 1e-6)
    chk("acumulado monotono", all(t["linhas"][i]["excesso_acumulado"] <= t["linhas"][i+1]["excesso_acumulado"]
                                  for i in range(len(t["linhas"]) - 1)))

    # excesso por taxa
    ex = excesso_por_taxa(fs, 1.47)
    chk("excesso por taxa apurado", ex["excesso_total"] > 0, f"(R$ {brl(ex['excesso_total'])})")

    # grafico
    svg = svg_excesso(t["linhas"])
    chk("svg gerado", svg.startswith("<svg") and svg.endswith("</svg>"))
    chk("svg tem barras e linha", "<rect" in svg and "<polyline" in svg)
    try:
        svg_excesso([]); chk("svg vazio e rejeitado", False)
    except DadoAusente: chk("svg vazio e rejeitado", True)

    chk("brl pt-BR", brl(1926440.74) == "1.926.440,74")
    chk("brl delega a comum.brl (HALF_UP, sem prefixo)", brl(0.125) == "0,13" and brl(-1500) == "-1.500,00")

    # ═════════════════════════════════════════════════════════════════
    # Regressoes v1.1.0 — valores fixos conferidos a mao
    # ═════════════════════════════════════════════════════════════════

    # (11) teto pre-marco: 2023-10..2024-02, encargos 300/mes, original 1.000
    # so 2024-01 e 2024-02 entram: cobrado 600 (< 1.000 → excesso 0)
    s11 = _serie(["2023-10", "2023-11", "2023-12", "2024-01", "2024-02"], 1000.0, 300.0)
    t11 = teto_lei_14690(1000.0, s11)
    chk("teto pre-marco: cobrado_total = 600 (so 2024-01 e 2024-02), excesso 0",
        t11["aplicavel"] is True and abs(t11["encargos_cobrados_total"] - 600.0) < 1e-9
        and t11["excesso_total"] == 0.0 and [l["competencia"] for l in t11["linhas"]] == ["2024-01", "2024-02"],
        f"(cobrado {t11['encargos_cobrados_total']:.2f})")
    chk("teto pre-marco: excluidas = ['2023-10','2023-11','2023-12'] com nota",
        t11["competencias_excluidas_pre_marco"] == ["2023-10", "2023-11", "2023-12"]
        and t11["nota"] is not None and "2023-12" in t11["nota"])
    t11b = teto_lei_14690(1000.0, s11, data_operacao=date(2023, 10, 5))
    chk("data_operacao pre-marco com serie que atravessa o marco: mesmas 2 competencias",
        t11b["aplicavel"] is True and abs(t11b["encargos_cobrados_total"] - 600.0) < 1e-9
        and "2023-10-05" in t11b["nota"])
    chk("competencia_no_teto: 2023-12 fora, 2024-01 dentro",
        competencia_no_teto("2023-12") is False and competencia_no_teto("2024-01") is True)

    # (12) novas dividas: original 1.000 + ('2024-03', 500); encargos 400/mes 2024-01..04
    # admissivel 1.000 ate 2024-02, 1.500 de 2024-03; cobrado 1.600 → excesso 100 em 2024-04
    s12 = _serie(["2024-01", "2024-02", "2024-03", "2024-04"], 1000.0, 400.0)
    t12 = teto_lei_14690(1000.0, s12, novas_dividas=[("2024-03", 500.0)])
    chk("novas dividas: teto por competencia [1000, 1000, 1500, 1500]",
        [l["teto_da_competencia"] for l in t12["linhas"]] == [1000.0, 1000.0, 1500.0, 1500.0])
    chk("novas dividas: excesso acumulado em 2024-04 = 1.600 − 1.500 = 100",
        abs(t12["linhas"][-1]["excesso_acumulado"] - 100.0) < 1e-9
        and abs(t12["excesso_total"] - 100.0) < 1e-9 and t12["competencia_estouro"] == "2024-04"
        and abs(t12["encargos_admissiveis_total"] - 1500.0) < 1e-9 and t12["teto"] == 1500.0,
        f"(excesso {t12['excesso_total']:.2f})")
    chk("novas dividas informadas: sem ressalva", t12["ressalva"] is None)
    t12b = teto_lei_14690(1000.0, s12)
    chk("sem novas_dividas: comportamento anterior (excesso 600) + ressalva",
        abs(t12b["excesso_total"] - 600.0) < 1e-9 and t12b["ressalva"] is not None
        and "novas_dividas" in t12b["ressalva"] and "5.112/2023" in t12b["ressalva"],
        f"(excesso {t12b['excesso_total']:.2f})")

    # (13) consistencia aritmetica: encargos 15.375 num total 14.829,80
    try:
        Fatura("2024-03", 12300.0, 900.0, 1200.0, 15375.0, 92.3, 14829.8, 12.5)
        chk("fatura inconsistente (encargos 15.375) e rejeitada", False)
    except ValueError as e:
        chk("fatura inconsistente (encargos 15.375) e rejeitada com competencia e diferenca",
            "2024-03" in str(e) and "regra 0" in str(e) and "-13837.50" in str(e), f"[{str(e)[:70]}...]")
    chk("diferenca de 0,04 fica na tolerancia",
        Fatura("2024-03", 12300.0, 900.0, 1200.0, 1537.5, 92.3, 14829.84, 12.5).total_fatura == 14829.84)
    chk("amostra inteira e consistente", len(_amostra()) == 6)

    # (14) competencia duplicada
    for nome, fn in (("segmentar_serie", segmentar_serie), ("evolucao_divida", evolucao_divida),
                     ("teto_lei_14690", lambda x: teto_lei_14690(1000.0, x)),
                     ("excesso_por_taxa", lambda x: excesso_por_taxa(x, 1.47)),
                     ("detectar_candidatos", detectar_candidatos)):
        try:
            fn(fs + [fs[1]]); chk(f"{nome}: competencia duplicada e rejeitada", False)
        except ValueError as e:
            chk(f"{nome}: competencia duplicada e rejeitada", "2024-03" in str(e))

    # (15) serie vazia
    for nome, fn in (("evolucao_divida([])", lambda: evolucao_divida([])),
                     ("teto_lei_14690(x, [])", lambda: teto_lei_14690(1000.0, [])),
                     ("segmentar_serie([])", lambda: segmentar_serie([]))):
        try:
            fn(); chk(f"{nome} levanta DadoAusente", False)
        except DadoAusente as e:
            chk(f"{nome} levanta DadoAusente", e.campo == "faturas")

    # (16) excesso_por_taxa: metodo declarado, aritmetica nominal inalterada
    e16 = excesso_por_taxa([_fat("2024-01", 1000.0, 0.0, 0.0, 50.0, 0.0),
                            _fat("2024-02", 1050.0, 0.0, 0.0, 50.0, 0.0)], 3.0)
    # jan: 50 − 1000 × 3% = 20; fev: 50 − 1050 × 3% = 18,50 (base = saldo_anterior nominal) → 38,50
    chk("excesso_por_taxa nominal: 20,00 + 18,50 = 38,50", abs(e16["excesso_total"] - 38.5) < 1e-9,
        f"({e16['excesso_total']:.2f})")
    chk("excesso_por_taxa declara o metodo",
        e16["metodo"] == "nominal por competência, sem efeito composto — critério de menor excesso"
        and ex["metodo"] == METODO_EXCESSO_POR_TAXA)

    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("cartao", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    print("Autoteste — motores/cartao.py v1.1.0\n")
    raise SystemExit(1 if autoteste()["falharam"] else 0)
