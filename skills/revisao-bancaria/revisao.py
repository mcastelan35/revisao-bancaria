#!/usr/bin/env python3
"""
revisao.py — linha de comando única do plugin revisao-bancaria

Chamada de qualquer pasta, só com a biblioteca padrão (o `openpyxl` é exigido só pela planilha):

    python3 revisao.py autoteste [--modulo M] [--verbose]
    python3 revisao.py regras --tipo T --regime R [--data-contrato D] [--data-consolidacao D]
                       [--categorias a,b] [--hoje D] [--formato resumo|padrao|completo]
    python3 revisao.py regra R15 R16 · sumula 530 541 · marcos --data-contrato D
    python3 revisao.py serie [--modalidade M | --buscar TEXTO]
    python3 revisao.py razao --contratada-pct X --media-pct Y [--unidade-contratada U] [--tipo T]
    python3 revisao.py comparar --sistema price|sac --pv V --n N
                       --taxa-contratada-pct X --taxa-revisada-pct Y [--unidade U] [--tabela]
    python3 revisao.py gerar payload.json --saida DIR [--formatos premium,panorama,planilha]
    python3 revisao.py operador mostrar | salvar --tipo advogado|contador [--nome ...]

Saída em JSON (salvo `autoteste`). Códigos de saída: 0 ok · 1 autoteste com falha ·
2 erro de entrada · 3 operador não configurado.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from pathlib import Path

PASTA_SKILL = Path(__file__).resolve().parent
if str(PASTA_SKILL) not in sys.path:
    sys.path.insert(0, str(PASTA_SKILL))

from motores import VERSAO, calculo, operador, regras, relatorios  # noqa: E402
from motores.comum import arredondar, saida_utf8                    # noqa: E402

MODULOS_AUTOTESTE = ("comum", "calculo", "cet", "cartao", "conta_corrente", "relatorios", "regras")
DICA_OPERADOR = ("configure o operador: revisao.py operador salvar --tipo advogado|contador "
                 "--nome ... --registro ... --entidade ... --cidade ...")


def _imprimir(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _numero(texto: str) -> float:
    try:
        valor = float(texto)
    except ValueError:
        raise argparse.ArgumentTypeError(f"número inválido: {texto!r}") from None
    if not math.isfinite(valor):
        raise argparse.ArgumentTypeError(f"número inválido: {texto!r}")
    return valor


# ─────────────────────────────────────────────────────────────────────
# autoteste
# ─────────────────────────────────────────────────────────────────────

def _linha_autoteste(r: dict) -> str:
    passaram, falharam, pulados = r["passaram"], r["falharam"], r["pulados"]
    if falharam:
        status = "FALHOU"
        detalhe = f"{passaram} passaram · {falharam} falharam" + (f" · {pulados} pulados" if pulados else "")
    elif pulados:
        status = "PULADO"
        detalhe = (f"openpyxl ausente — {pulados} asserções da planilha puladas (HTML testado)"
                   if r["modulo"] == "relatorios" else f"{passaram} passaram · {pulados} pulados")
    else:
        status, detalhe = "OK", f"{passaram} passaram"
    return f"  {status:<6}  {r['modulo']:<16} {detalhe}"


def cmd_autoteste(args) -> int:
    nomes = MODULOS_AUTOTESTE if args.modulo == "todos" else (args.modulo,)
    resultados = []
    for nome in nomes:
        modulo = importlib.import_module(f"motores.{nome}")
        if args.verbose:
            print(f"\n══ {nome} ══")
        resultados.append(modulo.autoteste(verbose=args.verbose))
    if args.verbose:
        print()
    for r in resultados:
        print(_linha_autoteste(r))
    soma = {k: sum(r[k] for r in resultados) for k in ("passaram", "falharam", "pulados")}
    print(f"total: {soma['passaram']} passaram · {soma['falharam']} falharam · {soma['pulados']} pulados")
    return 1 if soma["falharam"] else 0


# ─────────────────────────────────────────────────────────────────────
# regras, regra, sumula, marcos, serie
# ─────────────────────────────────────────────────────────────────────

def cmd_regras(args) -> int:
    categorias = None
    if args.categorias is not None:
        categorias = [c.strip() for c in args.categorias.split(",") if c.strip()] or None
    _imprimir(regras.avaliar(args.tipo, args.regime, args.data_contrato,
                             data_consolidacao=args.data_consolidacao, categorias=categorias,
                             hoje=args.hoje, formato=args.formato))
    return 0


def cmd_regra(args) -> int:
    _imprimir([regras.regra(i) for i in args.ids])
    return 0


def cmd_sumula(args) -> int:
    _imprimir([regras.sumula(n) for n in args.numeros])
    return 0


def cmd_marcos(args) -> int:
    _imprimir(regras.resolver_marcos(args.data_contrato, args.data_consolidacao))
    return 0


def cmd_serie(args) -> int:
    _imprimir(regras.series(modalidade=args.modalidade, buscar=args.buscar))
    return 0


# ─────────────────────────────────────────────────────────────────────
# razao, comparar
# ─────────────────────────────────────────────────────────────────────

def cmd_razao(args) -> int:
    if args.tipo:
        tipo = regras.tipo_contrato(args.tipo)
        if "R15" in tipo.get("regras_desligadas", []):
            raise ValueError(f"R15 desligada no tipo {args.tipo}: a razão contratada/média BACEN "
                             "não é tese nos tipos habitacionais (regra de conduta 27)")
    # normalizar_taxa devolve fração; ×100 em float deixa ruído (0,23 → 0,23000000000000004) que
    # empurraria uma razão exatamente no limiar para o lado errado — 10 casas bastam.
    contratada_am = arredondar(calculo.normalizar_taxa(args.contratada_pct, args.unidade_contratada) * 100, 10)
    saida = regras.classificar_razao(contratada_am, args.media_pct)
    saida["unidade_contratada_informada"] = args.unidade_contratada
    saida["contratada_informada"] = args.contratada_pct
    _imprimir(saida)
    return 0


def cmd_comparar(args) -> int:
    r_contratada = calculo.normalizar_taxa(args.taxa_contratada_pct, args.unidade)
    r_revisada = calculo.normalizar_taxa(args.taxa_revisada_pct, args.unidade)
    contratado = calculo.Cenario(args.sistema, args.pv, r_contratada, args.n)
    revisado = calculo.Cenario(args.sistema, args.pv, r_revisada, args.n)
    cmp = calculo.comparar(contratado, revisado)
    saida = {
        "sistema": contratado.sistema,
        "pv": arredondar(args.pv),
        "n": args.n,
        "taxa_contratada_am": r_contratada,
        "taxa_revisada_am": r_revisada,
        "prestacao_contratada_primeira": arredondar(contratado.linhas[0]["prestacao"]),
        "prestacao_revisada_primeira": arredondar(revisado.linhas[0]["prestacao"]),
        "prestacao_contratada_ultima": arredondar(contratado.linhas[-1]["prestacao"]),
        "prestacao_revisada_ultima": arredondar(revisado.linhas[-1]["prestacao"]),
        "total_pago_contratado": arredondar(contratado.total_pago),
        "total_pago_revisado": arredondar(revisado.total_pago),
        "total_juros_contratado": arredondar(contratado.total_juros),
        "total_juros_revisado": arredondar(revisado.total_juros),
        "excesso_total": arredondar(cmp["excesso_total"]),
        "favoravel": cmp["favoravel"],
        "nota": cmp["nota"],
        "plotar": cmp["plotar"],
        "saldos_coincidem": cmp["saldos_coincidem"],
    }
    if args.tabela:
        saida["linhas"] = [{k: (v if k == "n" else arredondar(v)) for k, v in linha.items()}
                           for linha in cmp["linhas"]]
    _imprimir(saida)
    return 0


# ─────────────────────────────────────────────────────────────────────
# gerar, operador
# ─────────────────────────────────────────────────────────────────────

def _sem_identidade(payload: dict) -> bool:
    marca = payload.get("marca")
    nome = marca.get("nome") if isinstance(marca, dict) else None
    return "assinatura" not in payload or not nome


def cmd_gerar(args) -> int:
    caminho = Path(args.payload)
    try:
        payload = json.loads(caminho.read_text(encoding="utf-8-sig"))
    except OSError as erro:
        raise ValueError(f"não foi possível ler o payload {caminho}: {erro.strerror or erro}") from None
    except ValueError as erro:                       # JSON malformado ou texto que não é UTF-8
        raise ValueError(f"payload {caminho} não é um JSON UTF-8 válido: {erro}") from None
    if not isinstance(payload, dict):
        raise ValueError(f"payload {caminho} deve ser um objeto JSON")

    op = operador.ler(args.config_dir)
    aplicado = False
    if op is not None:
        if "assinatura" not in payload:
            payload["assinatura"] = operador.assinatura(op)
            aplicado = True
        marca = payload.get("marca")
        nome_marca = operador.marca_nome(op)
        if nome_marca and (marca is None or (isinstance(marca, dict) and not marca.get("nome"))):
            payload["marca"] = {**(marca or {}), "nome": nome_marca}
            aplicado = True
    try:
        arquivos = relatorios.gerar(payload, Path(args.saida),
                                    formatos=relatorios.parse_formatos(args.formatos))
    except ValueError as erro:
        if op is None and _sem_identidade(payload):
            raise ValueError(f"{erro} — {DICA_OPERADOR}") from None
        raise
    _imprimir({"arquivos": [str(a) for a in arquivos], "operador_aplicado": aplicado})
    return 0


def cmd_operador_mostrar(args) -> int:
    op = operador.ler(args.config_dir)
    _imprimir({"pasta": str(operador.pasta_config(args.config_dir)), "operador": op})
    return 0 if op is not None else 3


def cmd_operador_salvar(args) -> int:
    dados = {"tipo": args.tipo}
    for chave in ("nome", "registro", "entidade", "cidade", "skill_peticao"):
        valor = getattr(args, chave)
        if valor is not None:
            dados[chave] = valor
    arquivo, avisos = operador.salvar(dados, args.config_dir)
    _imprimir({"arquivo": str(arquivo), "avisos": avisos, "operador": operador.ler(args.config_dir)})
    return 0


# ─────────────────────────────────────────────────────────────────────
# argparse
# ─────────────────────────────────────────────────────────────────────

def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="revisao.py", description="Linha de comando do plugin revisao-bancaria.",
        epilog="Saída em JSON (salvo `autoteste`). Códigos: 0 ok · 1 autoteste com falha · "
               "2 erro de entrada · 3 operador não configurado.")
    ap.add_argument("--version", action="version", version=f"revisao-bancaria {VERSAO}")
    sub = ap.add_subparsers(dest="comando", required=True, metavar="COMANDO")

    p = sub.add_parser("autoteste", help="autoteste dos motores, uma linha por módulo")
    p.add_argument("--modulo", choices=(*MODULOS_AUTOTESTE, "todos"), default="todos")
    p.add_argument("--verbose", action="store_true", help="mostra as linhas PASS/FAIL de cada módulo")
    p.set_defaults(func=cmd_autoteste)

    p = sub.add_parser("regras", help="regras aplicáveis ao caso, com corte temporal e regime resolvidos")
    p.add_argument("--tipo", required=True, help="id do tipo de contrato (consumo_pf, empresarial_pj, sfh, ...)")
    p.add_argument("--regime", required=True, help="consumerista | civil_empresarial (aceita civil-empresarial)")
    p.add_argument("--data-contrato", help="AAAA-MM-DD")
    p.add_argument("--data-consolidacao", help="AAAA-MM-DD (SFH/SFI com consolidação)")
    p.add_argument("--categorias", help="categorias separadas por vírgula; as demais regras são só contadas")
    p.add_argument("--hoje", help="AAAA-MM-DD, data da análise (padrão: hoje)")
    p.add_argument("--formato", default="padrao", help="resumo | padrao | completo (padrão: padrao)")
    p.set_defaults(func=cmd_regras)

    p = sub.add_parser("regra", help="regra integral (fundamentação)")
    p.add_argument("ids", nargs="+", metavar="ID", help="R01 ... R40")
    p.set_defaults(func=cmd_regra)

    p = sub.add_parser("sumula", help="texto integral de súmula do acervo")
    p.add_argument("numeros", nargs="+", metavar="N", type=int)
    p.set_defaults(func=cmd_sumula)

    p = sub.add_parser("marcos", help="posição do contrato nos marcos temporais MT01-MT10")
    p.add_argument("--data-contrato", help="AAAA-MM-DD")
    p.add_argument("--data-consolidacao", help="AAAA-MM-DD")
    p.set_defaults(func=cmd_marcos)

    p = sub.add_parser("serie", help="série SGS/BACEN por modalidade, sem gastar quota do conector")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--modalidade", help="id exato da modalidade (cartao_rotativo, ...)")
    g.add_argument("--buscar", help="texto, sem acento e sem caixa, em modalidade e nome")
    p.set_defaults(func=cmd_serie)

    p = sub.add_parser("razao", help="razão taxa contratada / média BACEN e limiares da R15")
    p.add_argument("--contratada-pct", required=True, type=_numero)
    p.add_argument("--unidade-contratada", choices=calculo.UNIDADES, default="am_efetiva")
    p.add_argument("--media-pct", required=True, type=_numero, help="média BACEN da modalidade, % a.m.")
    p.add_argument("--tipo", help="se informado, recusa os tipos em que a R15 está desligada")
    p.set_defaults(func=cmd_razao)

    p = sub.add_parser("comparar", help="Price/SAC contratado × revisado")
    p.add_argument("--sistema", required=True, choices=("price", "sac"))
    p.add_argument("--pv", required=True, type=_numero)
    p.add_argument("--n", required=True, type=int)
    p.add_argument("--taxa-contratada-pct", required=True, type=_numero)
    p.add_argument("--taxa-revisada-pct", required=True, type=_numero)
    p.add_argument("--unidade", choices=calculo.UNIDADES, default="am_efetiva")
    p.add_argument("--tabela", action="store_true", help="inclui as linhas parcela a parcela")
    p.set_defaults(func=cmd_comparar)

    p = sub.add_parser("gerar", help="entregáveis a partir do payload, com a identidade do operador")
    p.add_argument("payload")
    p.add_argument("--saida", required=True, help="pasta de saída")
    p.add_argument("--formatos", help="premium,panorama,planilha (padrão: todos)")
    p.add_argument("--config-dir", help="pasta do operador.json")
    p.set_defaults(func=cmd_gerar)

    p = sub.add_parser("operador", help="identidade de quem assina os laudos")
    acao = p.add_subparsers(dest="acao", required=True, metavar="AÇÃO")
    m = acao.add_parser("mostrar", help="mostra o operador gravado (código 3 se não houver)")
    m.add_argument("--config-dir")
    m.set_defaults(func=cmd_operador_mostrar)
    s = acao.add_parser("salvar", help="grava o operador")
    s.add_argument("--tipo", required=True, help="advogado | contador")
    for opcao in ("nome", "registro", "entidade", "cidade", "skill-peticao"):
        s.add_argument(f"--{opcao}")
    s.add_argument("--config-dir")
    s.set_defaults(func=cmd_operador_salvar)
    return ap


def main(argv: list[str] | None = None) -> int:
    saida_utf8()
    args = _parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, KeyError, ImportError) as erro:
        mensagem = erro.args[0] if isinstance(erro, KeyError) and erro.args else str(erro)
        print(f"erro: {mensagem}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
