"""comum.py — utilitários compartilhados pelos motores da skill revisao-bancaria.

Existe para que os motores não carreguem quatro versões de `brl()` com arredondamento
diferente: laudo que mistura fontes diverge no centavo, e divergência de centavo em perícia é
munição para a parte contrária. Tudo o que é formatação, parse numérico, competência e guarda
de escala vive aqui e é importado pelos motores.

Uso dentro de um motor (pacote `motores`, import relativo):

    from .comum import brl, brl_rs, parse_num_ptbr, competencia, guard_taxa

Autoteste: `python -m motores.comum` (de dentro de `skills/revisao-bancaria/`) ou
`python3 revisao.py autoteste --modulo comum`.
"""
from __future__ import annotations

import calendar
import io
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

# ─────────────────────────────────────────────────────────────────────
# Constantes jurídicas compartilhadas (uma fonte, não quatro)
# ─────────────────────────────────────────────────────────────────────

CORTE_TEMA_929 = date(2021, 3, 30)      # MT05 — modulação da repetição em dobro (EAREsp 676.608/RS)
MARCO_TETO_CARTAO = date(2024, 1, 3)    # MT06 — teto de 100% no rotativo (Lei 14.690/2023; Res. CMN 5.112/2023)

# ─────────────────────────────────────────────────────────────────────
# Formatação pt-BR
# ─────────────────────────────────────────────────────────────────────

_CENT = Decimal("0.01")


def _dec(v) -> Decimal:
    if isinstance(v, Decimal):
        return v
    return Decimal(str(v))


def brl(v, casas: int = 2) -> str:
    """'1234.565' -> '1.234,57' (Decimal, ROUND_HALF_UP — o mesmo em todos os motores).
    Sem prefixo; use `brl_rs` para 'R$ 1.234,57'."""
    q = Decimal(1).scaleb(-casas)
    d = _dec(v).quantize(q, rounding=ROUND_HALF_UP)
    neg = d < 0
    inteiro, _, frac = f"{abs(d):f}".partition(".")
    inteiro = f"{int(inteiro):,}".replace(",", ".")
    s = f"{inteiro},{frac.ljust(casas, '0')}" if casas else inteiro
    return f"-{s}" if neg else s


def brl_rs(v, casas: int = 2) -> str:
    """'R$ 1.234,57' (negativo: 'R$ -1.234,57')."""
    return f"R$ {brl(v, casas)}"


def pct(v, casas: int = 2) -> str:
    """Percentual já em pontos percentuais: pct(12.3456) -> '12,35%'."""
    return f"{brl(v, casas)}%"


def arredondar(v, casas: int = 2) -> float:
    """Arredonda em Decimal, ROUND_HALF_UP, e devolve float (saída JSON): 0.125 -> 0.13
    (`round(0.125, 2)` daria 0.12). Só para exibição — nunca no meio de um cálculo."""
    return float(_dec(v).quantize(Decimal(1).scaleb(-casas), rounding=ROUND_HALF_UP))


def pt(s: str) -> str:
    """Troca o ponto decimal de uma f-string por vírgula: pt(f'{x:.4f}') -> '0,8500'.
    Só para números SEM separador de milhar — para moeda use brl()."""
    return s.replace(".", ",")


# ─────────────────────────────────────────────────────────────────────
# Parse numérico pt-BR — estrito por desenho
# ─────────────────────────────────────────────────────────────────────

_RE_NUM = re.compile(r"^[+-]?[\d.,]+$")


def parse_num_ptbr(s: str) -> float:
    """Converte texto numérico do CSV canônico (pt-BR) em float, recusando ambiguidade.

    Aceita:  '1.234,56'  '1234,56'  '1234.56'  '1500'  '1.234.567,89'  '-12,5'  'R$ 1.234,56'
    Recusa:  '1.500'     (um ponto e três dígitos: milhar ou 1,5? — exigir '1500' ou '1.500,00')
             '1,234.56'  (formato en-US: a vírgula antes do ponto não é pt-BR)
             ''          (vazio)

    A recusa é deliberada (regra 0): número ambíguo na extração vira lacuna, não palpite.
    """
    t = s.strip().replace("R$", "").replace(" ", "")
    if t == "":
        raise ValueError("número vazio")
    if not _RE_NUM.match(t):
        raise ValueError(f"número inválido: {s!r}")
    tem_v, tem_p = "," in t, "." in t
    if tem_v and tem_p:
        if t.rfind(",") < t.rfind("."):
            raise ValueError(f"número em formato en-US ({s!r}) — o CSV canônico é pt-BR: use '1.234,56'")
        return float(t.replace(".", "").replace(",", "."))
    if tem_v:
        if t.count(",") > 1:
            raise ValueError(f"número com mais de uma vírgula: {s!r}")
        return float(t.replace(",", "."))
    if tem_p:
        partes = t.lstrip("+-").split(".")
        if len(partes) == 2 and len(partes[1]) == 3:
            raise ValueError(
                f"número ambíguo ({s!r}): um ponto seguido de três dígitos pode ser milhar ou "
                f"decimal — escreva '{partes[0]}{partes[1]},00' ou '{partes[0]},{partes[1]}'")
        if len(partes) > 2:
            if all(len(p) == 3 for p in partes[1:]):
                return float(t.replace(".", ""))       # '1.234.567' — só milhar
            raise ValueError(f"número inválido: {s!r}")
        return float(t)                                # '1234.56' — decimal com ponto, aceito
    return float(t)


# ─────────────────────────────────────────────────────────────────────
# Competências
# ─────────────────────────────────────────────────────────────────────

def competencia(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def fim_do_mes(d: date) -> date:
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])


def dias_no_mes(comp: str) -> int:
    y, m = (int(x) for x in comp.split("-"))
    return calendar.monthrange(y, m)[1]


def competencias_entre(ini: date, fim: date) -> list[str]:
    out, y, m = [], ini.year, ini.month
    while (y, m) <= (fim.year, fim.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def proximo_dia_util_civil(d: date) -> date:
    """Próximo dia de segunda a sexta (sem feriados — quem sabe de feriado é a série SGS)."""
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d


# ─────────────────────────────────────────────────────────────────────
# Guarda de escala de taxa
# ─────────────────────────────────────────────────────────────────────

def guard_taxa(valor: float, contexto: str = "taxa", max_fracao_am: float = 0.5) -> float:
    """Taxa mensal em FRAÇÃO decimal (0,03 = 3% a.m.). Valor acima de `max_fracao_am`
    (50% a.m.) foi quase certamente digitado em pontos percentuais — parar, não adivinhar."""
    v = float(valor)
    if v < 0:
        raise ValueError(f"{contexto}: taxa negativa ({v})")
    if v > max_fracao_am:
        raise ValueError(
            f"{contexto}: {v} não parece fração decimal mensal (limite {max_fracao_am}). "
            f"Se a taxa é {v}% a.m., informe {v / 100}. Regra 0: não adivinhar a escala.")
    return v


# ─────────────────────────────────────────────────────────────────────
# Autoteste
# ─────────────────────────────────────────────────────────────────────

def saida_utf8() -> None:
    """Põe stdout e stderr em UTF-8. No Windows, console e pipes usam cp1252 e quebram em '−'
    ou '→'; chamado só pelos blocos `__main__` e pela linha de comando, nunca pelas funções."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):   # fluxo substituído (pytest, redirecionamento)
            pass


def rodar_autoteste(modulo: str, testes, verbose: bool = True) -> dict:
    """Executa `testes()` e monta o resultado uniforme do `autoteste()` de cada motor:
    `{"modulo", "passaram", "falharam", "pulados"}`.

    `testes` devolve `(passaram, falharam)` ou `(passaram, falharam, pulados)`.
    `verbose=False` suprime tudo o que o autoteste imprimir (stdout e stderr)."""
    if verbose:
        resultado = testes()
    else:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            resultado = testes()
    passaram, falharam, *resto = resultado
    return {"modulo": modulo, "passaram": passaram, "falharam": falharam,
            "pulados": resto[0] if resto else 0}


def _testes() -> tuple[int, int]:
    ok = fail = 0

    def chk(nome, cond):
        nonlocal ok, fail
        ok += bool(cond); fail += (not cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {nome}")

    chk("brl HALF_UP", brl(0.125) == "0,13" and brl(1234.565) == "1.234,57")
    chk("brl negativo", brl(-1500) == "-1.500,00" and brl_rs(-1500) == "R$ -1.500,00")
    chk("brl Decimal", brl(Decimal("3166077.58")) == "3.166.077,58")
    chk("pct", pct(12.3456) == "12,35%")
    chk("pt", pt(f"{0.85:.4f}") == "0,8500")
    chk("parse pt-BR", parse_num_ptbr("1.234,56") == 1234.56 and parse_num_ptbr("R$ 1.500,00") == 1500.0)
    chk("parse inteiro/decimal ponto", parse_num_ptbr("1500") == 1500.0 and parse_num_ptbr("1234.56") == 1234.56)
    chk("parse só milhar", parse_num_ptbr("1.234.567") == 1234567.0)
    for amb in ("1.500", "1,234.56", "", "abc"):
        try:
            parse_num_ptbr(amb); chk(f"parse recusa {amb!r}", False)
        except ValueError:
            chk(f"parse recusa {amb!r}", True)
    chk("competencias_entre", competencias_entre(date(2023, 11, 5), date(2024, 2, 1)) ==
        ["2023-11", "2023-12", "2024-01", "2024-02"])
    chk("fim_do_mes bissexto", fim_do_mes(date(2024, 2, 10)) == date(2024, 2, 29) and dias_no_mes("2024-02") == 29)
    chk("proximo_dia_util_civil", proximo_dia_util_civil(date(2025, 8, 16)) == date(2025, 8, 18))
    chk("guard_taxa aceita 0,08", guard_taxa(0.08) == 0.08)
    try:
        guard_taxa(7.9); chk("guard_taxa recusa 7,9", False)
    except ValueError:
        chk("guard_taxa recusa 7,9", True)
    print(f"\n  {ok} passaram · {fail} falharam")
    return ok, fail


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada."""
    return rodar_autoteste("comum", _testes, verbose)


if __name__ == "__main__":
    saida_utf8()
    raise SystemExit(1 if autoteste()["falharam"] else 0)
