"""
relatorios.py — camada de saída do plugin `revisao-bancaria`

MUDANÇA DE ARQUITETURA (v4, 08/2026)
------------------------------------
Antes: seis templates HTML/XLSX que EMBUTIAM a lógica de cálculo em `<script>` e
eram editados à mão trocando as constantes `P`, `rC`, `rR`, `n`. Isso amarrava o
relatório a Price/SAC com comparação contratado-versus-revisado e quebrava em
contrato atípico, em contrato cujo saldo confere e em operação pós-fixada.

Agora: DOIS entregáveis, renderizados a partir de um PAYLOAD.
  · PREMIUM   — laudo pericial completo, A4 retrato, para instrução processual.
  · PANORAMA  — panorâmica estratégica de 2 a 3 páginas, para reunião com o cliente.
  · PLANILHA  — XLSX único, dashboard na primeira aba, A4 retrato.

O template não calcula mais nada. Todo número vem do payload, produzido pelas
camadas L0-L3 com `calculo.py` e `cet.py`. Isso mantém a regra 12
(cálculo só pelo motor) e torna possível cobrir qualquer sistema de amortização.

USO
---
    python3 revisao.py gerar payload.json --saida <pasta de saída>
    python3 revisao.py autoteste --modulo relatorios

Ver `referencia/payload-schema.md` para o contrato de dados.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .comum import (brl as _brl_comum, brl_rs as _brl_rs_comum, pct as _pct_comum,
                    rodar_autoteste, saida_utf8)

# openpyxl é opcional no import e obrigatório só quando a planilha é pedida. `gerar()`
# confere ANTES de escrever qualquer arquivo, para não deixar HTML pela metade.
try:
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.properties import PageSetupProperties
except ImportError:                                            # pragma: no cover
    openpyxl = None
    Alignment = Border = Font = PatternFill = Side = None
    get_column_letter = PageSetupProperties = None

#: Sem `openpyxl` a planilha não sai (o HTML sim) e o autoteste pula só as asserções dela.
PLANILHA_DISPONIVEL = openpyxl is not None

# ─────────────────────────────────────────────────────────────────────
# FORMATAÇÃO — delega a comum.py (Decimal, ROUND_HALF_UP); aqui só o `None` -> "—"
# ─────────────────────────────────────────────────────────────────────

def brl(v, casas: int = 2) -> str:
    """'1234.565' -> '1.234,57'; None -> '—'. Mesma saída de comum.brl."""
    if v is None:
        return "—"
    return _brl_comum(v, casas)


def brl_rs(v, casas: int = 2) -> str:
    """'R$ 1.234,57'; None -> '—'."""
    if v is None:
        return "—"
    return _brl_rs_comum(v, casas)


def pct(v, casas: int = 4) -> str:
    """Percentual já em PONTOS PERCENTUAIS (18.3737 -> '18,3737%'), como comum.pct.
    Difere de comum.pct só no default de casas (4, taxa a.a. sai com 4) e no None -> '—'."""
    if v is None:
        return "—"
    return _pct_comum(v, casas)


def taxa_aa_pct(v):
    """`conferencia.cenarios[*].taxa_aa` é esperada em pontos percentuais (18,3737).
    O `cet.py` devolve fração (0,183737): se 0 < v < 1, trata como fração e converte.
    `validar_detalhado()` avisa quando a conversão acontece."""
    if v is None:
        return None
    v = float(v)
    return v * 100 if 0 < v < 1 else v


def _taxa_parece_fracao(v) -> bool:
    try:
        return v is not None and 0 < float(v) < 1
    except (TypeError, ValueError):
        return False


def esc(t) -> str:
    if t is None:
        return ""
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# Espelha EXATAMENTE "Valores admitidos em resultado" do referencia/payload-schema.md.
CORES = {"Conforme": "grn", "Lícito": "grn", "Revisão inviável": "grn",
         "Ilícito": "red", "Ilícito parcial": "red", "Divergência": "red", "Contradição": "red",
         "Excesso": "red", "Prejudicial": "red", "Não discriminado": "red", "Base de cálculo": "red",
         "Lacuna": "amb", "A demonstrar": "amb", "A verificar": "amb",
         "Excessivo": "amb", "Inconsistência": "amb"}
RESULTADOS_ADMITIDOS = set(CORES)
PRO_BANCO = {r for r, c in CORES.items() if c == "grn"}          # exigem `ressalvas`
PENDENTES = {"A verificar", "A demonstrar", "Lacuna"}             # sinalizados no laudo
VEREDITOS = {"CONFORME", "DIVERGENTE"}
NATUREZAS_CENARIOS = {"conferencia", "recomposicao"}

# Textos condicionais à natureza dos cenários (schema: `conferencia.natureza_cenarios`).
# "conferencia" (default) é a rota pós-fixada/CET: os cenários só dimensionam o diferencial.
# "recomposicao" é a rota Price/SAC: os cenários SÃO a recomposição do saldo.
TEXTOS_CENARIOS = {
    "conferencia": {
        "conforme": ("O saldo apurado pela instituição credora é aritmeticamente correto quando "
                     "aferido pela metodologia efetivamente pactuada."),
        "nota": ("Os cenários acima não constituem proposta de recomposição do saldo. Medem o "
                 "diferencial entre o custo informado e o custo praticado, para fins de "
                 "dimensionamento."),
    },
    "recomposicao": {
        "conforme": ("O saldo apurado pela instituição credora é aritmeticamente correto quando "
                     "aferido pelos parâmetros contratados (taxa, sistema de amortização e prazo)."),
        "nota": ("Os cenários acima recompõem o saldo sob a taxa revisada e constituem a base da "
                 "repetição: a diferença entre o saldo cobrado e o recomposto é o indébito a "
                 "restituir."),
    },
}

_CHARS_ABA_INVALIDOS = '/\\?*[]:'


def nome_aba(nome) -> str:
    """Nome de aba válido no Excel: sem `/ \\ ? * [ ] :`, máximo 31 caracteres."""
    s = "".join("-" if ch in _CHARS_ABA_INVALIDOS else ch for ch in str(nome or "Aba"))
    return (s.strip() or "Aba")[:31]

# ─────────────────────────────────────────────────────────────────────
# CHASSI CSS — imutável, compartilhado pelos dois entregáveis
# ─────────────────────────────────────────────────────────────────────

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#1A1714;--gold:#B08A4E;--glt:#EDE0B8;--gpale:#FAF7EF;--mid:#4A4A4A;
--mut:#8A8175;--rule:#DDD6C8;--red:#A62B2B;--rbg:#FCF3F3;--grn:#2F6B45;--gbg:#F2F8F4;
--amb:#8A6A1F;--abg:#FDF8EC}
html,body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
@page{size:A4 portrait;margin:14mm 0}
.doc{font-family:'DM Sans',-apple-system,Segoe UI,sans-serif;font-size:9pt;color:var(--ink);
width:210mm;margin:0 auto;padding:0 18mm 0 24mm;border-left:6px solid var(--gold)}
.hdr{display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:10px;
border-bottom:2px solid var(--gold);margin-bottom:16px;break-after:avoid}
.marca{font-family:'Space Grotesk',sans-serif;font-size:19pt;font-weight:600;letter-spacing:-.4px}
.marca span{color:var(--gold)}
.hdr-ref{text-align:right;font-size:7.5pt;color:var(--mut);line-height:1.6}
.hdr-ref strong{display:block;color:var(--ink);font-size:8.5pt;letter-spacing:.5px}
h1{font-family:'Space Grotesk',sans-serif;font-size:16pt;font-weight:600;line-height:1.25;
margin-bottom:6px;break-after:avoid}
.sub{font-size:8.5pt;color:var(--mid);line-height:1.6;margin-bottom:14px;text-align:justify}
.faixa{font-family:'Space Grotesk',sans-serif;font-size:8pt;font-weight:600;letter-spacing:.09em;
text-transform:uppercase;color:#7A5F10;background:var(--gpale);border-bottom:1px solid var(--gold);
padding:5px 9px;margin:16px 0 8px;break-after:avoid}
p{font-size:9pt;line-height:1.62;text-align:justify;margin-bottom:7px;orphans:3;widows:3}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin:12px 0}
.kpi{background:var(--gpale);border:1px solid var(--glt);border-radius:3px;padding:8px 6px;text-align:center}
.kpi .lab{font-size:6.5pt;letter-spacing:.05em;text-transform:uppercase;color:var(--mut);margin-bottom:2px}
.kpi .n{font-family:'Space Grotesk',sans-serif;font-size:14pt;font-weight:600;font-variant-numeric:tabular-nums}
.kpi .s{font-size:6.5pt;color:var(--mut);margin-top:1px}
.red{color:var(--red)}.grn{color:var(--grn)}.amb{color:var(--amb)}
table{width:100%;border-collapse:collapse;font-size:8pt;font-variant-numeric:tabular-nums;margin:8px 0}
thead{display:table-header-group}
th{background:var(--ink);color:#F2EFE9;padding:5px 7px;font-family:'Space Grotesk',sans-serif;
font-size:7pt;font-weight:500;letter-spacing:.04em;text-transform:uppercase;text-align:left}
td{border:1px solid var(--rule);padding:4px 7px;vertical-align:top}
td.n,th.n{text-align:right}td.c,th.c{text-align:center}
tbody tr:nth-child(even) td{background:#FAF9F6}
tfoot td{background:var(--gpale);border-top:2px solid var(--gold);font-weight:600}
tr{break-inside:avoid}
.cx{padding:7px 11px;margin:8px 0;font-size:8pt;line-height:1.6;text-align:justify;
border-radius:0 3px 3px 0;break-inside:avoid}
.cx.ok{background:var(--gbg);border-left:3px solid var(--grn)}
.cx.al{background:var(--rbg);border-left:3px solid var(--red)}
.cx.nt{background:var(--gpale);border-left:3px solid var(--gold)}
.cx b{color:inherit}
.cx.ok b{color:var(--grn)}.cx.al b{color:var(--red)}
.prompt{background:#F6F4EF;border-left:3px solid var(--gold);padding:6px 9px;margin:5px 0;
font-family:'JetBrains Mono',Consolas,monospace;font-size:6.8pt;line-height:1.45;white-space:pre-wrap}
.barra{height:14px;background:#EFECE4;border-radius:2px;overflow:hidden;margin:2px 0}
.barra i{display:block;height:100%}
.sig{margin-top:26px;break-inside:avoid;text-align:center}
.sig .ln{width:230px;margin:0 auto 4px;border-top:1px solid var(--ink)}
.sig .nm{font-family:'Space Grotesk',sans-serif;font-size:9pt;font-weight:500}
.sig .rg{font-size:8pt;color:var(--mut)}
.rod{margin-top:20px;padding-top:8px;border-top:1px solid var(--rule);display:flex;
justify-content:space-between;font-family:'Space Grotesk',sans-serif;font-size:7pt;
color:var(--mut);letter-spacing:.06em;break-inside:avoid}
"""

FONTES = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600'
          '&family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400'
          '&display=swap" rel="stylesheet">')


def _cabecalho(p, titulo_doc):
    m = p["marca"]
    return f"""  <div class="hdr">
    <div class="marca">{esc(m['nome'])}<span>.</span></div>
    <div class="hdr-ref"><strong>{esc(titulo_doc)}</strong>
      {esc(p['identificacao'].get('referencia', ''))}<br>{esc(p['emissao'])}</div>
  </div>"""


def _assinatura(p):
    a = p["assinatura"]
    ent = f'<div class="rg">{esc(a["entidade"])}</div>' if a.get("entidade") else ""
    return f"""  <div class="sig">
    <div class="ln"></div>
    <div class="nm">{esc(a['nome'])}</div>
    <div class="rg">{esc(a['registro'])}</div>
    {ent}
    <div class="rg">{esc(a['cidade'])}, {esc(p['emissao'])}</div>
  </div>"""


def _rodape(p):
    return (f'  <div class="rod"><span>{esc(p["marca"]["nome"])} — '
            f'{esc(p["identificacao"].get("referencia",""))}</span>'
            f'<span>Documento confidencial</span></div>')


def _tabela_conferencia(p):
    c = p["conferencia"]
    linhas = ""
    for l in c["cenarios"]:
        d = l.get("diferenca")
        cls = "" if d is None else ("grn" if abs(float(d)) < float(c.get("limiar_conforme", 1e9)) else "red")
        linhas += (f'<tr><td>{esc(l["premissa"])}</td><td class="c">{pct(taxa_aa_pct(l.get("taxa_aa")), 4)}</td>'
                   f'<td class="n">{brl(l["saldo"])}</td>'
                   f'<td class="n {cls}">{brl(d)}</td></tr>')
    return (f'<table><thead><tr><th>Premissa de evolução do débito</th><th class="c">Taxa</th>'
            f'<th class="n">Saldo em {esc(c["data_base"])}</th><th class="n">Diferença</th></tr></thead>'
            f'<tbody>{linhas}</tbody></table>')


def _tabela_achados(p, resumida=False):
    ach = p["achados"]
    if resumida:
        ach = [a for a in ach if a.get("tier") in ("T1", None) or a["resultado"] in
               PRO_BANCO][:7] or ach[:7]
    linhas = ""
    for a in ach:
        cls = CORES.get(a["resultado"], "")
        det = f'<br>{esc(a["detalhe"])}' if (a.get("detalhe") and not resumida) else ""
        fund = (f'<td>{esc(a.get("fundamento",""))}</td>') if not resumida else ""
        tier = (f'<td class="c">{esc(a.get("tier","—"))}</td>') if not resumida else ""
        linhas += (f'<tr><td class="c">{esc(a.get("id",""))}</td>'
                   f'<td><b>{esc(a["titulo"])}</b>{det}</td>{fund}'
                   f'<td class="c {cls}">{esc(a["resultado"])}</td>{tier}</tr>')
    cabs = ('<th class="c">Id.</th><th>Achado</th>' +
            ('' if resumida else '<th>Fundamento</th>') +
            '<th class="c">Resultado</th>' +
            ('' if resumida else '<th class="c">Tier</th>'))
    return f'<table><thead><tr>{cabs}</tr></thead><tbody>{linhas}</tbody></table>'


# ─────────────────────────────────────────────────────────────────────
# ENTREGÁVEL 1 — PREMIUM (laudo pericial completo)
# ─────────────────────────────────────────────────────────────────────

def _frase_diferenca(diferenca) -> str:
    """Sinal de `conferencia.diferenca` = apurado pela credora − recalculado.
    Positivo: a credora cobra a mais; negativo: o recalculado supera o apurado."""
    d = float(diferenca)
    if d >= 0:
        return f"O saldo apurado pela credora excede o recalculado em {brl_rs(abs(d))}"
    return f"O saldo recalculado excede o apurado pela credora em {brl_rs(abs(d))}"


def render_premium(p: dict) -> str:
    i, c = p["identificacao"], p["conferencia"]
    veredito = c["veredito"]
    textos = TEXTOS_CENARIOS.get(c.get("natureza_cenarios") or "conferencia",
                                 TEXTOS_CENARIOS["conferencia"])
    cx_saldo = (f'<div class="cx ok"><b>Conclusão parcial.</b> {textos["conforme"]} '
                f'A divergência é de {pct(abs(float(c["diferenca_pct"])),2)} do montante.</div>'
                if veredito == "CONFORME" else
                f'<div class="cx al"><b>Divergência apurada.</b> {_frase_diferenca(c["diferenca"])}, '
                f'equivalentes a {pct(abs(float(c["diferenca_pct"])),2)} do montante.</div>')
    nota_cenarios = f'<div class="cx nt">{textos["nota"]}</div>'

    premissas = ""
    if p.get("premissas"):
        premissas = (f'<div class="faixa">Premissas declaradas</div>'
                     f'<div class="cx nt">Afirmadas pelo operador e não comprovadas documentalmente — '
                     f'os achados que delas dependem estão classificados como A verificar.</div>'
                     + "".join(f"<p>{esc(t)}</p>" for t in p["premissas"]))

    ident = "".join(
        f'<tr><td>{esc(k)}</td><td>{esc(v)}</td><td class="c">{esc(o)}</td></tr>'
        for k, v, o in i["campos"])

    kpis = "".join(
        f'<div class="kpi"><div class="lab">{esc(k["lab"])}</div>'
        f'<div class="n {k.get("cor","")}">{esc(k["val"])}</div>'
        f'<div class="s">{esc(k.get("sub",""))}</div></div>' for k in p["kpis"])

    metodo = "".join(f"<p>{esc(t)}</p>" for t in p["metodologia"])
    lacunas = "".join(f"<p>{esc(t)}</p>" for t in p.get("lacunas", [])) or \
        "<p>Não foram identificadas lacunas documentais que impeçam conclusão sobre os pontos examinados.</p>"
    ressalvas = "".join(f'<div class="cx ok"><b>Ressalva de imparcialidade.</b> {esc(t)}</div>'
                        for t in p.get("ressalvas", []))
    conclusao = "".join(f"<p>{esc(t)}</p>" for t in p["conclusao"])
    # A agenda de pesquisa NAO entra no laudo. Documento pericial destina-se aos autos e
    # nao pode expor roteiro de pesquisa nao executada nem admitir tese sem lastro. Os
    # enunciados de `agenda_jusia` saem em arquivo apartado, de uso interno.
    pendentes = [a for a in p.get("achados", [])
                 if a.get("resultado") in PENDENTES or a.get("pesquisa_pendente")]
    bloco_prompts = (f'<div class="cx nt">Os achados classificados como pendentes de '
                     f'verificação — {esc(", ".join(a["id"] for a in pendentes))} — dependem de '
                     f'elementos não constantes do acervo examinado ou de qualificação jurídica '
                     f'que extrapola o objeto desta auditoria, e por isso não comportam conclusão '
                     f'definitiva neste laudo.</div>' if pendentes else "")

    memoria = ""
    if p.get("memoria"):
        m = p["memoria"]
        linhas = "".join("<tr>" + "".join(
            f'<td class="{"n" if isinstance(v,(int,float)) and not isinstance(v,bool) else "c"}">'
            f'{brl(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else esc(v)}</td>'
            for v in row) + "</tr>" for row in m["linhas"])
        memoria = (f'<div class="faixa">{esc(m["titulo"])}</div><p>{esc(m.get("nota",""))}</p>'
                   f'<table><thead><tr>' +
                   "".join(f'<th class="c">{esc(h)}</th>' for h in m["colunas"]) +
                   f'</tr></thead><tbody>{linhas}</tbody></table>')

    docs = "".join(f'<tr><td>{esc(d[0])}</td><td class="c">{esc(d[1])}</td><td>{esc(d[2])}</td></tr>'
                   for d in p.get("documentos", []))
    bloco_docs = (f'<div class="faixa">Documentos examinados</div><table><thead><tr>'
                  f'<th>Documento</th><th class="c">Emissão</th><th>Origem</th></tr></thead>'
                  f'<tbody>{docs}</tbody></table>' if docs else "")

    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>{esc(p['titulo'])}</title>{FONTES}<style>{CSS}</style></head><body><div class="doc">
{_cabecalho(p, p['tipo_doc'])}
  <h1>{esc(p['titulo'])}</h1>
  <div class="sub">{esc(p['subtitulo'])}</div>
  <div class="kpis">{kpis}</div>

  <div class="faixa">1 — Objeto e delimitação</div>
  {"".join(f"<p>{esc(t)}</p>" for t in p["objeto"])}

{bloco_docs}

  <div class="faixa">2 — Metodologia</div>
  {metodo}
  <div class="cx nt">Nenhum dado foi presumido. Toda informação empregada foi extraída dos
  documentos examinados ou de série oficial do Banco Central do Brasil. As lacunas que impedem
  conclusão estão declaradas em seção própria, e os achados correspondentes foram classificados
  como pendentes de verificação.</div>

  <div class="faixa">3 — Conferência do saldo devedor — veredito {esc(veredito)}</div>
  {cx_saldo}
  {_tabela_conferencia(p)}
  {nota_cenarios}

  <div class="faixa">4 — Quadro de achados</div>
  {_tabela_achados(p)}
  {ressalvas}

{memoria}

{premissas}

  <div class="faixa">5 — Lacunas documentais declaradas</div>
  {lacunas}

{bloco_prompts}

  <div class="faixa">6 — Conclusão</div>
  {conclusao}

{_assinatura(p)}
{_rodape(p)}
</div></body></html>"""


# ─────────────────────────────────────────────────────────────────────
# ENTREGÁVEL 2 — PANORAMA (panorâmica estratégica executiva)
# ─────────────────────────────────────────────────────────────────────

def render_panorama(p: dict) -> str:
    c = p["conferencia"]
    kpis = "".join(
        f'<div class="kpi"><div class="lab">{esc(k["lab"])}</div>'
        f'<div class="n {k.get("cor","")}">{esc(k["val"])}</div>'
        f'<div class="s">{esc(k.get("sub",""))}</div></div>' for k in p["kpis"])

    selo = ("ok" if c["veredito"] == "CONFORME" else "al")
    txt_selo = (p["panorama"]["selo"] if p.get("panorama", {}).get("selo") else
                ("O saldo cobrado confere com a metodologia do contrato."
                 if c["veredito"] == "CONFORME" else
                 "O saldo cobrado diverge da metodologia do contrato."))

    barras = ""
    if p.get("panorama", {}).get("barras"):
        # Valor negativo (ex.: saldo credor) não vira largura negativa: barra vazia + rótulo.
        mx = max([float(b["valor"]) for b in p["panorama"]["barras"]] + [0.0]) or 1
        for b in p["panorama"]["barras"]:
            v = float(b["valor"])
            w = max(0.0, v / mx * 100)
            neg = " (negativo)" if v < 0 else ""
            barras += (f'<div style="font-size:7.5pt;color:var(--mut);margin-top:5px">'
                       f'{esc(b["rotulo"])} — <b style="color:var(--ink)">{brl_rs(v)}</b>{neg}</div>'
                       f'<div class="barra"><i style="width:{w:.1f}%;background:{esc(b.get("cor","#B08A4E"))}"></i></div>')

    secoes = "".join(
        f'<div class="faixa">{esc(s["titulo"])}</div>' + "".join(f"<p>{esc(t)}</p>" for t in s["paragrafos"])
        for s in p["panorama"]["secoes"])

    pend = "".join(f"<p>{esc(t)}</p>" for t in p.get("lacunas", []))
    bloco_pend = (f'<div class="cx al"><b>Pendências que condicionam as conclusões.</b> '
                  f'{esc(" ".join(p.get("lacunas", [])))}</div>' if pend else "")

    reco = "".join(f"<p>{esc(t)}</p>" for t in p["panorama"].get("recomendacao", []))

    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>Panorâmica estratégica — {esc(p['identificacao'].get('referencia',''))}</title>
{FONTES}<style>{CSS}</style></head><body><div class="doc">
{_cabecalho(p, 'Panorâmica estratégica')}
  <h1>{esc(p['panorama']['titulo'])}</h1>
  <div class="sub">{esc(p['panorama']['subtitulo'])}</div>
  <div class="kpis">{kpis}</div>
  <div class="cx {selo}"><b>Veredito.</b> {esc(txt_selo)}</div>

  <div class="faixa">O que foi verificado</div>
  {"".join(f"<p>{esc(t)}</p>" for t in p['panorama']['verificado'])}
  {barras}

{secoes}

  <div class="faixa">Semáforo de conformidade</div>
  {_tabela_achados(p, resumida=True)}

  <div class="faixa">Recomendação</div>
  {reco}
  {bloco_pend}

{_assinatura(p)}
{_rodape(p)}
</div></body></html>"""


# ─────────────────────────────────────────────────────────────────────
# ENTREGÁVEL 3 — PLANILHA XLSX
# ─────────────────────────────────────────────────────────────────────

XLSX_AMB, XLSX_ABG = "FF8A6A1F", "FFFDF8EC"      # âmbar — mesmo par do CSS (--amb/--abg)


def render_planilha(p: dict, destino: Path) -> Path:
    if openpyxl is None:
        raise ImportError("openpyxl não está instalado e a planilha foi pedida — "
                          "instale (`pip install openpyxl`) ou gere sem `planilha` em --formatos.")

    GOLD, GPALE, GLT = "FFB8952E", "FFFAF7EF", "FFEDE0B8"
    INK, MUT, RED, GRN = "FF1A1A1A", "FF888888", "FFA62B2B", "FF2F6B45"
    RBG, GBG = "FFFCF3F3", "FFF2F8F4"
    AMB, ABG = XLSX_AMB, XLSX_ABG
    # Mesma classificação do HTML (CORES): verde / vermelho / âmbar; fora da lista, sem cor.
    PALETA = {"grn": (GBG, GRN), "red": (RBG, RED), "amb": (ABG, AMB)}
    thin = Side("thin", color="FFD9D9D9")
    BD = Border(thin, thin, thin, thin)
    M = "#,##0.00"

    def F(sz=9, b=False, c=INK):
        return Font(name="Calibri", size=sz, bold=b, color=c)

    def fill(c):
        return PatternFill("solid", fgColor=c)

    CE = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LE = Alignment(horizontal="left", vertical="center", wrap_text=True)
    RI = Alignment(horizontal="right", vertical="center")

    wb = openpyxl.Workbook()

    def setup(ws, cols, fit_h=0, titles=None):
        ws.sheet_view.showGridLines = False
        ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
        ws.page_setup.orientation = "portrait"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = fit_h
        ws.page_margins.left = ws.page_margins.right = 0.4
        ws.page_margins.top = ws.page_margins.bottom = 0.5
        ws.oddFooter.left.text = f"{p['marca']['nome']} — {p['identificacao'].get('referencia','')}"
        ws.oddFooter.left.size = 8
        ws.oddFooter.left.color = "888888"
        ws.oddFooter.right.text = "Página &P de &N"
        ws.oddFooter.right.size = 8
        ws.oddFooter.right.color = "888888"
        if titles:
            ws.print_title_rows = titles
        for k, w in enumerate(cols, 1):
            ws.column_dimensions[get_column_letter(k)].width = w

    def faixa(ws, r, txt, ncols):
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
        c = ws.cell(r, 1, txt)
        c.font = F(9, True, "FF7A5F10")
        c.fill = fill(GPALE)
        c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        for j in range(1, ncols + 1):
            ws.cell(r, j).border = Border(bottom=Side("thin", color=GOLD))
        ws.row_dimensions[r].height = 18
        return r + 1

    def cab(ws, r, cols):
        for j, t in enumerate(cols, 1):
            c = ws.cell(r, j, t)
            c.font = F(8, True, "FFE8E7E2")
            c.fill = fill(INK)
            c.alignment = CE
            c.border = BD
        ws.row_dimensions[r].height = 24
        return r + 1

    # ---- aba 1: dashboard
    ws = wb.active
    ws.title = "Dashboard"
    setup(ws, [2.5, 30, 15, 15, 2.5, 24, 15, 15], fit_h=1)
    ws.merge_cells("B2:H2")
    c = ws["B2"]
    c.value = p["titulo"].upper()
    c.font = F(14, True)
    c.alignment = LE
    ws.row_dimensions[2].height = 24
    ws.merge_cells("B3:H3")
    c = ws["B3"]
    c.value = p["subtitulo"]
    c.font = F(8, False, MUT)
    c.alignment = LE

    pos = [(2, 4), (6, 8), (2, 4), (6, 8)]
    for k, kp in enumerate(p["kpis"][:4]):
        c1, c2 = pos[k]
        lin = 5 if k < 2 else 8
        ws.merge_cells(start_row=lin, start_column=c1, end_row=lin, end_column=c2)
        a = ws.cell(lin, c1, kp["lab"].upper())
        a.font = F(7, True, MUT)
        a.alignment = CE
        ws.merge_cells(start_row=lin + 1, start_column=c1, end_row=lin + 1, end_column=c2)
        b = ws.cell(lin + 1, c1, kp["val"])
        cor = {"red": RED, "grn": GRN, "amb": AMB}.get(kp.get("cor"), INK)
        b.font = F(16, True, cor)
        b.alignment = CE
        for rr in (lin, lin + 1):
            for cc in range(c1, c2 + 1):
                ws.cell(rr, cc).fill = fill(GPALE)
        ws.row_dimensions[lin].height = 14
        ws.row_dimensions[lin + 1].height = 26

    r = 11
    r = faixa(ws, r, "IDENTIFICAÇÃO DA OPERAÇÃO", 8)
    campos = p["identificacao"]["campos"]
    meio = (len(campos) + 1) // 2
    for k in range(meio):
        for col, idx in ((2, k), (6, k + meio)):
            if idx < len(campos):
                ws.cell(r, col, campos[idx][0]).font = F(8, False, MUT)
                ws.cell(r, col).alignment = LE
                ws.merge_cells(start_row=r, start_column=col + 1, end_row=r, end_column=col + 2)
                ws.cell(r, col + 1, str(campos[idx][1])).font = F(8, True)
                ws.cell(r, col + 1).alignment = LE
        ws.row_dimensions[r].height = 14
        r += 1

    r += 1
    r = faixa(ws, r, f"CONFERÊNCIA DO SALDO — VEREDITO {p['conferencia']['veredito']}", 8)
    r = cab(ws, r, ["", "Premissa de evolução do débito", "Taxa a.a.", "Saldo (R$)", "", "Diferença (R$)", "", ""])
    for l in p["conferencia"]["cenarios"]:
        ws.cell(r, 2, l["premissa"]).font = F(8)
        ws.cell(r, 2).alignment = LE
        taxa = taxa_aa_pct(l.get("taxa_aa"))
        ws.cell(r, 3, (taxa if taxa is not None else "—")).alignment = CE
        ws.cell(r, 3).font = F(8)
        if taxa is not None:
            ws.cell(r, 3).number_format = '0.0000"%"'
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
        cv = ws.cell(r, 4, float(l["saldo"]))
        cv.number_format = M
        cv.font = F(9, True)
        cv.alignment = RI
        ws.merge_cells(start_row=r, start_column=6, end_row=r, end_column=8)
        cd = ws.cell(r, 6, float(l["diferenca"]) if l.get("diferenca") is not None else "—")
        if l.get("diferenca") is not None:
            cd.number_format = M
        cd.font = F(9, True)
        cd.alignment = RI
        for j in range(2, 9):
            ws.cell(r, j).border = BD
        ws.row_dimensions[r].height = 15
        r += 1

    r += 1
    r = faixa(ws, r, "SÍNTESE DOS ACHADOS", 8)
    for a in p["achados"]:
        bg, cor = PALETA.get(CORES.get(a["resultado"], ""), (None, INK))
        ws.cell(r, 2, a["resultado"]).font = F(8, True, cor)
        ws.cell(r, 2).alignment = LE
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8)
        ws.cell(r, 3, a["titulo"]).font = F(8)
        ws.cell(r, 3).alignment = LE
        for j in range(2, 9):
            if bg:
                ws.cell(r, j).fill = fill(bg)
            ws.cell(r, j).border = BD
        ws.row_dimensions[r].height = 14
        r += 1

    # ---- abas de memória
    for m in p.get("abas", []):
        ws = wb.create_sheet(nome_aba(m["nome"]))
        setup(ws, m.get("larguras", [14] * len(m["colunas"])), titles="1:3")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(m["colunas"]))
        c = ws.cell(1, 1, m["titulo"])
        c.font = F(12, True)
        c.alignment = LE
        ws.row_dimensions[1].height = 20
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(m["colunas"]))
        c = ws.cell(2, 1, m.get("nota", ""))
        c.font = F(8, False, MUT)
        c.alignment = LE
        rr = cab(ws, 3, m["colunas"])
        for k, row in enumerate(m["linhas"]):
            for j, v in enumerate(row, 1):
                cel = ws.cell(rr, j, v)
                cel.border = BD
                cel.font = F(8)
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    cel.number_format = M
                    cel.alignment = RI
                else:
                    cel.alignment = CE if j <= 2 else LE
                if k % 2 == 1:
                    cel.fill = fill("FFF7F6F3")
            ws.row_dimensions[rr].height = 12
            rr += 1
        if m.get("totais"):
            for j, v in enumerate(m["totais"], 1):
                cel = ws.cell(rr, j, v)
                cel.fill = fill(GLT)
                cel.font = F(9, True)
                cel.border = Border(thin, thin, Side("medium", color=GOLD), thin)
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    cel.number_format = M
                    cel.alignment = RI
        ws.freeze_panes = "A4"

    # ---- aba metodologia e lacunas
    ws = wb.create_sheet("Metodologia e fontes")
    setup(ws, [2.5, 30, 62], fit_h=1)
    ws.merge_cells("B2:C2")
    ws["B2"].value = "METODOLOGIA, FONTES E LACUNAS DECLARADAS"
    ws["B2"].font = F(12, True)
    r = 4
    r = faixa(ws, r, "PARÂMETROS", 3)
    for k, t in enumerate(p["metodologia"], 1):
        ws.cell(r, 2, f"Parâmetro {k}").font = F(8, True)
        ws.cell(r, 2).alignment = LE
        ws.cell(r, 3, t).font = F(8, False, "FF4A4A4A")
        ws.cell(r, 3).alignment = LE
        for j in (2, 3):
            ws.cell(r, j).border = BD
        ws.row_dimensions[r].height = 26
        r += 1
    if p.get("premissas"):
        r += 1
        r = faixa(ws, r, "PREMISSAS DECLARADAS", 3)
        intro = ("Afirmadas pelo operador e não comprovadas documentalmente — os achados que "
                 "delas dependem estão classificados como A verificar.")
        for k, t in enumerate([intro] + list(p["premissas"])):
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
            ws.cell(r, 2, t).font = F(8, k == 0, "FF4A4A4A")
            ws.cell(r, 2).alignment = LE
            for j in (2, 3):
                ws.cell(r, j).fill = fill(ABG)
                ws.cell(r, j).border = BD
            ws.row_dimensions[r].height = 16
            r += 1
    r += 1
    r = faixa(ws, r, "LACUNAS DECLARADAS", 3)
    for t in p.get("lacunas", []) or ["Nenhuma lacuna bloqueante identificada."]:
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        ws.cell(r, 2, t).font = F(8, False, "FF4A4A4A")
        ws.cell(r, 2).alignment = LE
        for j in (2, 3):
            ws.cell(r, j).fill = fill(RBG)
            ws.cell(r, j).border = BD
        ws.row_dimensions[r].height = 16
        r += 1
    r += 2
    a = p["assinatura"]
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    ws.cell(r, 2, f"Responsável técnico: {a['nome']} — {a['registro']}").font = F(9, True)
    ws.cell(r, 2).alignment = LE

    destino.parent.mkdir(parents=True, exist_ok=True)
    wb.save(destino)
    return destino


# ─────────────────────────────────────────────────────────────────────
# ORQUESTRAÇÃO
# ─────────────────────────────────────────────────────────────────────

OBRIGATORIOS = ["marca", "titulo", "subtitulo", "tipo_doc", "emissao", "identificacao",
                "kpis", "objeto", "metodologia", "conferencia", "achados", "conclusao",
                "assinatura", "panorama"]


def validar_detalhado(p: dict, formatos: set[str] | None = None) -> dict:
    """Validação ESTRUTURAL: tudo o que o render lê com `[...]` é exigido aqui, para que um
    payload aprovado nunca dê KeyError em `render_*`. Devolve `{"erros": [...], "avisos": [...]}`.
    `erros` recusa a geração; `avisos` não recusam (vão ao stderr em `gerar()`).

    Sub-chaves só são inspecionadas quando o bloco pai existe e é do tipo certo — o bloco
    ausente já consta em `erros` pelo nome, sem ruído de sub-chaves."""
    formatos = formatos or {"premium", "panorama", "planilha"}
    erros: list[str] = []
    avisos: list[str] = []
    if not isinstance(p, dict):
        return {"erros": ["payload não é um objeto JSON"], "avisos": []}

    exigidos = [k for k in OBRIGATORIOS if k != "panorama" or "panorama" in formatos]
    erros += [k for k in exigidos if k not in p]

    def bloco(nome, tipo=dict):
        """Devolve o bloco se presente e do tipo esperado; registra erro de tipo se não for."""
        v = p.get(nome)
        if v is None:
            return None
        if not isinstance(v, tipo):
            erros.append(f"{nome} (esperado {tipo.__name__})")
            return None
        return v

    def chaves(obj, prefixo, nomes):
        for k in nomes:
            if k not in obj:
                erros.append(f"{prefixo}.{k}")

    for nome in ("objeto", "metodologia", "conclusao"):
        bloco(nome, list)

    m = bloco("marca")
    if m is not None and not m.get("nome"):
        erros.append("marca.nome")

    i = bloco("identificacao")
    if i is not None:
        if not i.get("slug"):
            erros.append("identificacao.slug")
        campos = i.get("campos")
        if not isinstance(campos, list):
            erros.append("identificacao.campos (lista de [rótulo, valor, origem])")
        else:
            for k, c in enumerate(campos):
                if not isinstance(c, (list, tuple)) or len(c) != 3:
                    erros.append(f"identificacao.campos[{k}] (esperado [rótulo, valor, origem])")

    kp = bloco("kpis", list)
    if kp is not None:
        if len(kp) != 4:
            avisos.append(f"kpis: {len(kp)} itens — o dashboard da planilha usa exatamente 4")
        for k, item in enumerate(kp):
            if not isinstance(item, dict) or "lab" not in item or "val" not in item:
                erros.append(f"kpis[{k}] (lab/val)")

    c = bloco("conferencia")
    if c is not None:
        chaves(c, "conferencia", ("veredito", "data_base", "diferenca_pct"))
        ver = c.get("veredito")
        if "veredito" in c and ver not in VEREDITOS:
            erros.append(f"conferencia.veredito ({ver!r} — esperado CONFORME ou DIVERGENTE)")
        if ver == "DIVERGENTE" and c.get("diferenca") is None:
            erros.append("conferencia.diferenca (obrigatório quando o veredito é DIVERGENTE)")
        nat = c.get("natureza_cenarios")
        if nat is not None and nat not in NATUREZAS_CENARIOS:
            erros.append(f"conferencia.natureza_cenarios ({nat!r} — esperado conferencia ou recomposicao)")
        cen = c.get("cenarios")
        if not isinstance(cen, list):
            erros.append("conferencia.cenarios (lista)")
        else:
            for k, l in enumerate(cen):
                if not isinstance(l, dict) or "premissa" not in l or "saldo" not in l:
                    erros.append(f"conferencia.cenarios[{k}] (premissa/saldo)")
                    continue
                t = l.get("taxa_aa")
                if _taxa_parece_fracao(t):
                    avisos.append(f"conferencia.cenarios[{k}].taxa_aa={t} parece fração; "
                                  f"convertida para % ({pct(taxa_aa_pct(t), 4)})")

    ach = bloco("achados", list)
    if ach is not None:
        for k, a in enumerate(ach):
            if not isinstance(a, dict):
                erros.append(f"achados[{k}] (esperado objeto)")
                continue
            chaves(a, f"achados[{k}]", ("id", "tier", "resultado", "titulo", "detalhe", "fundamento"))
            r = a.get("resultado")
            if "resultado" in a and r not in RESULTADOS_ADMITIDOS:
                avisos.append(f"achados[{k}].resultado={r!r} fora da lista admitida — renderiza sem cor")
        if any(isinstance(a, dict) and a.get("resultado") in PRO_BANCO for a in ach) \
                and not p.get("ressalvas"):
            avisos.append("há achado pró-banco sem ressalva — `ressalvas` é obrigatório nesse caso")

    a = bloco("assinatura")
    if a is not None:
        chaves(a, "assinatura", ("nome", "registro", "entidade", "cidade"))

    mem = bloco("memoria")
    if mem is not None:
        chaves(mem, "memoria", ("titulo", "colunas", "linhas"))

    abas = bloco("abas", list)
    if abas is not None:
        for k, ab in enumerate(abas):
            if not isinstance(ab, dict):
                erros.append(f"abas[{k}] (esperado objeto)")
                continue
            chaves(ab, f"abas[{k}]", ("nome", "titulo", "colunas", "linhas"))

    if "panorama" in formatos:
        pan = bloco("panorama")
        if pan is not None:
            chaves(pan, "panorama", ("titulo", "subtitulo", "selo", "verificado", "barras",
                                     "secoes", "recomendacao"))
            for nome in ("verificado", "secoes", "recomendacao"):
                if nome in pan and not isinstance(pan[nome], list):
                    erros.append(f"panorama.{nome} (lista)")
            for k, s in enumerate(pan.get("secoes") or []):
                if not isinstance(s, dict) or "titulo" not in s or "paragrafos" not in s:
                    erros.append(f"panorama.secoes[{k}] (titulo/paragrafos)")
            for k, b in enumerate(pan.get("barras") or []):
                if not isinstance(b, dict) or "rotulo" not in b or "valor" not in b:
                    erros.append(f"panorama.barras[{k}] (rotulo/valor)")

    return {"erros": erros, "avisos": avisos}


def validar(p: dict, formatos: set[str] | None = None) -> list[str]:
    """Mantém o contrato antigo (lista de erros; vazia = válido). Para os avisos, usar
    `validar_detalhado()`."""
    return validar_detalhado(p, formatos)["erros"]


def render_agenda(p: dict) -> str:
    """Agenda de pesquisa — arquivo APARTADO, uso interno, nunca anexado aos autos."""
    i = p["identificacao"]
    itens = "\n\n".join(f"### {n}\n\n{t}" for n, t in enumerate(p.get("agenda_jusia", []), 1))
    return (f"# Agenda de validação jurisprudencial — USO INTERNO\n\n"
            f"> **Não juntar aos autos.** Este arquivo registra pesquisa ainda não executada e "
            f"não integra o laudo pericial. Destina-se exclusivamente à preparação da peça.\n\n"
            f"**Referência:** {i.get('referencia','—')}  \n"
            f"**Instrumento:** {p.get('titulo','—')}  \n"
            f"**Emissão:** {p.get('emissao','—')}\n\n"
            f"Executar na skill `pesquisa-jurisprudencial-jusia` antes da redação. "
            f"Descartar julgados adversos ou de duplo gume antes de levar à peça.\n\n"
            f"---\n\n{itens}\n")


def gerar(payload: dict, saida: Path, slug: str = None,
          formatos: set[str] | None = None) -> list[Path]:
    """formatos: subconjunto de {"premium","panorama","planilha"}. None = todos.

    A validação é condicional ao que foi pedido no gate de entrega: exigir `panorama`
    quando só o laudo foi solicitado é incoerência entre o gate e o validador.
    """
    formatos = formatos or {"premium", "panorama", "planilha"}
    v = validar_detalhado(payload, formatos)
    if v["erros"]:
        raise ValueError("payload incompleto — campos ausentes ou inválidos: " + ", ".join(v["erros"]))
    for a in v["avisos"]:
        print(f"  aviso: {a}", file=sys.stderr)
    # Dependência conferida ANTES de qualquer escrita: sem openpyxl, nada sai pela metade.
    if "planilha" in formatos and openpyxl is None:
        raise ImportError("openpyxl não está instalado e a planilha foi pedida — nenhum arquivo "
                          "foi gerado. Instale (`pip install openpyxl`) ou gere sem `planilha` "
                          "em --formatos.")
    slug = slug or payload["identificacao"].get("slug", "analise")
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    out = []
    if "premium" in formatos:
        f1 = saida / f"laudo-premium-{slug}.html"
        f1.write_text(render_premium(payload), encoding="utf-8")
        out.append(f1)
    if payload.get("agenda_jusia"):
        fa = saida / f"INTERNO-agenda-pesquisa-{slug}.md"
        fa.write_text(render_agenda(payload), encoding="utf-8")
        out.append(fa)
    if "panorama" in formatos:
        f2 = saida / f"panorama-estrategico-{slug}.html"
        f2.write_text(render_panorama(payload), encoding="utf-8")
        out.append(f2)
    if "planilha" in formatos:
        out.append(render_planilha(payload, saida / f"planilha-{slug}.xlsx"))
    return out


def _payload_demo() -> dict:
    return {
        "marca": {"nome": "Escritório Exemplo"},
        "tipo_doc": "Laudo pericial contábil",
        "titulo": "Auditoria de saldo devedor e de custo efetivo",
        "subtitulo": "Contrato de demonstração — payload sintético do autoteste.",
        "emissao": "17 de agosto de 2026",
        "identificacao": {"referencia": "DEMO-0001", "slug": "demo", "campos": [
            ("Emitente", "Empresa Demonstração Ltda.", "instrumento"),
            ("Credora", "Instituição Demonstração", "instrumento"),
            ("Valor do título", "R$ 1.000.000,00", "instrumento"),
            ("Encargos", "CDI + 3,041596% a.a.", "instrumento"),
        ]},
        "kpis": [{"lab": "Custo efetivo real", "val": "18,3737%", "cor": "red", "sub": "ao ano"},
                 {"lab": "CET declarado", "val": "6,6600%", "sub": "razão 2,76x"},
                 {"lab": "Divergência do saldo", "val": "0,15%", "cor": "grn", "sub": "confere"},
                 {"lab": "Exigido / vencido", "val": "30,1x", "cor": "red", "sub": "purgação"}],
        "objeto": ["Payload sintético para autoteste do renderizador."],
        "documentos": [("Instrumento de demonstração", "17/07/2025", "credor")],
        "metodologia": ["Reconstrução dia útil a dia útil com série 12 do SGS/BACEN.",
                        "Convenção dias úteis sobre 252, encargos do dia do vencimento acumulados antes da amortização."],
        "conferencia": {"veredito": "CONFORME", "data_base": "10/04/2026",
                        "diferenca": 2357.74, "diferenca_pct": 0.15, "limiar_conforme": 10000,
                        "cenarios": [
                            {"premissa": "Apurado pela credora", "taxa_aa": None, "saldo": 1547563.74, "diferenca": None},
                            {"premissa": "Recalculado pela metodologia pactuada", "taxa_aa": 18.3737, "saldo": 1545206.00, "diferenca": 2357.74},
                            {"premissa": "Ao CET declarado no anexo", "taxa_aa": 6.66, "saldo": 1431200.01, "diferenca": 116363.73}]},
        "achados": [
            {"id": "A1", "tier": "T1", "resultado": "Ilícito", "titulo": "CET declarado incompatível com o custo praticado",
             "detalhe": "6,66% a.a. contra 18,3737% a.a.", "fundamento": "Res. CMN 4.881/2020."},
            {"id": "A2", "tier": "—", "resultado": "Conforme", "titulo": "Saldo confere com a metodologia pactuada",
             "detalhe": "Divergência de 0,15%.", "fundamento": "Reconstrução com série oficial."}],
        "ressalvas": ["O montante exigido não excede a hipótese de vencimento antecipado integral."],
        "lacunas": ["Contrato de limite de crédito não apresentado."],
        "agenda_jusia": ["Pesquisar consequência do CET em desacordo com a Res. CMN 4.881/2020 em contrato empresarial."],
        "memoria": {"titulo": "Memória de apuração (extrato)", "nota": "Demonstração.",
                    "colunas": ["#", "Data", "Saldo (R$)"],
                    "linhas": [[1, "18/07/2025", 1000949.24], [2, "21/07/2025", 1001899.38]]},
        "abas": [{"nome": "Apuração diária", "titulo": "APURAÇÃO DIÁRIA", "nota": "Demonstração.",
                  "colunas": ["#", "Data", "Saldo (R$)"], "larguras": [7, 14, 18],
                  "linhas": [[1, "18/07/2025", 1000949.24], [2, "21/07/2025", 1001899.38]],
                  "totais": ["TOTAIS", "—", 1001899.38]}],
        "conclusao": ["O saldo confere; o vício está na informação de custo."],
        "assinatura": {"nome": "Nome do Responsável", "registro": "CRC/PR 000000/O",
                       "entidade": "Escritório Exemplo Ltda", "cidade": "Cidade-UF"},
        "panorama": {"titulo": "Panorâmica estratégica da operação",
                     "subtitulo": "Síntese para reunião com o cliente.",
                     "selo": "O saldo cobrado confere com a metodologia do contrato.",
                     "verificado": ["Auditamos o instrumento e os documentos do credor."],
                     "barras": [{"rotulo": "Cobrado", "valor": 1547563.74, "cor": "#A62B2B"},
                                {"rotulo": "Ao CET declarado", "valor": 1431200.01, "cor": "#2a78d6"}],
                     "secoes": [{"titulo": "Onde estão os problemas",
                                 "paragrafos": ["O custo informado é 2,76 vezes menor que o praticado."]}],
                     "recomendacao": ["Atacar o vício de informação, não o quantum do saldo."]},
    }


def _autoteste() -> tuple[int, int, int]:
    import tempfile
    ok = fail = pulados = 0
    # a planilha só é testada se o openpyxl está instalado (o módulo é lido agora, não no import)
    planilha = PLANILHA_DISPONIVEL and globals()["openpyxl"] is not None

    def chk(nome, cond, extra=""):
        nonlocal ok, fail
        if cond:
            ok += 1
            print(f"  PASS  {nome} {extra}")
        else:
            fail += 1
            print(f"  FAIL  {nome} {extra}")

    def pula(*nomes):
        """Asserções que dependem do openpyxl: contadas como puladas, nunca como falha."""
        nonlocal pulados
        for nome in nomes:
            pulados += 1
            print(f"  SKIP  {nome} (openpyxl ausente)")

    p = _payload_demo()
    chk("payload demo e valido", validar(p) == [])
    chk("payload incompleto e recusado", validar({"marca": {}}) != [])

    h1 = render_premium(p)
    chk("premium sem placeholder residual", "{" not in h1.split("<style>")[0])
    chk("premium traz o veredito", "CONFORME" in h1)
    chk("premium traz lacunas declaradas", "Lacunas documentais" in h1)
    chk("premium traz ressalva de imparcialidade", "Ressalva de imparcialidade" in h1)
    chk("premium assina com o registro do payload", "CRC/PR 000000/O" in h1)

    h2 = render_panorama(p)
    chk("panorama renderiza", "Panorâmica estratégica" in h2)
    chk("panorama e mais curto que o premium", len(h2) < len(h1),
        f"({len(h2)} vs {len(h1)} bytes)")
    chk("panorama traz recomendacao", "Recomendação" in h2)

    p2 = json.loads(json.dumps(p))
    p2["conferencia"]["veredito"] = "DIVERGENTE"
    p2["conferencia"]["diferenca_pct"] = 8.2
    chk("veredito DIVERGENTE troca a caixa", "Divergência apurada" in render_premium(p2))

    chk("laudo NAO carrega prompt de pesquisa",
        "Agenda de validação" not in h1 and "Modo E." not in h1)
    chk("laudo sinaliza achados pendentes sem expor roteiro",
        "pendentes de verificação" in h1 or not any(
            a.get("resultado") in ("A verificar", "A demonstrar", "Lacuna")
            for a in p.get("achados", [])))

    with tempfile.TemporaryDirectory() as td:
        # Sem openpyxl a planilha não pode ser pedida: gera só o HTML e a agenda.
        arqs = gerar(p, Path(td), "demo", None if planilha else {"premium", "panorama"})
        xlsx = [a for a in arqs if a.suffix == ".xlsx"]
        agenda = [a for a in arqs if a.name.startswith("INTERNO-agenda")]
        chk("gera os 3 entregaveis mais a agenda apartada",
            len(arqs) == (4 if planilha else 3))
        chk("agenda sai em arquivo apartado marcado como interno", len(agenda) == 1)
        chk("agenda avisa para nao juntar aos autos",
            "Não juntar aos autos" in agenda[0].read_text(encoding="utf-8"))
        if planilha:
            chk("planilha criada", xlsx and xlsx[0].stat().st_size > 4000)
            import openpyxl
            wb = openpyxl.load_workbook(xlsx[0])
            chk("dashboard e a primeira aba", wb.sheetnames[0] == "Dashboard")
            chk("planilha em A4 retrato ajustado a largura",
                all(w.page_setup.orientation == "portrait" and w.page_setup.fitToWidth == 1
                    for w in wb))
            chk("aba de metodologia presente", "Metodologia e fontes" in wb.sheetnames)
        else:
            pula("planilha criada", "dashboard e a primeira aba",
                 "planilha em A4 retrato ajustado a largura", "aba de metodologia presente")

    p3 = json.loads(json.dumps(p)); p3.pop("panorama")
    try:
        validar_ok = not validar(p3, {"premium", "planilha"})
    except Exception:
        validar_ok = False
    chk("payload sem panorama passa quando o gate pediu so o laudo", validar_ok)
    chk("payload sem panorama reprova quando o panorama foi pedido",
        "panorama" in validar(p3, {"premium", "panorama"}))

    # ------------------------------------------------------------------ v4.1
    clone = lambda d: json.loads(json.dumps(d))  # noqa: E731

    # 1 — CORES espelha exatamente o schema; resultado estranho avisa, não recusa
    esperado = {**{r: "grn" for r in ("Conforme", "Lícito", "Revisão inviável")},
                **{r: "red" for r in ("Ilícito", "Ilícito parcial", "Divergência", "Contradição",
                                      "Excesso", "Prejudicial", "Não discriminado", "Base de cálculo")},
                **{r: "amb" for r in ("Lacuna", "A demonstrar", "A verificar", "Excessivo",
                                      "Inconsistência")}}
    chk("CORES cobre exatamente os 16 resultados do schema",
        CORES == esperado and RESULTADOS_ADMITIDOS == set(esperado))
    px = clone(p)
    px["achados"].append({"id": "A3", "tier": "T2", "resultado": "A verificar",
                          "titulo": "Encargo dependente de documento ausente",
                          "detalhe": "", "fundamento": ""})
    px["achados"].append({"id": "A4", "tier": "T3", "resultado": "Inventado",
                          "titulo": "Classificação errada da L2", "detalhe": "", "fundamento": ""})
    vx = validar_detalhado(px)
    chk("resultado fora da lista gera aviso, nao erro",
        vx["erros"] == [] and any("fora da lista" in a for a in vx["avisos"]))

    # 2 — premissas declaradas
    px["premissas"] = ["A data de liberação do crédito foi a informada pelo cliente."]
    hx = render_premium(px)
    chk("premium com premissas traz secao e texto",
        "Premissas declaradas" in hx and
        "Afirmadas pelo operador e não comprovadas documentalmente" in hx)
    chk("premissas ficam antes das lacunas",
        hx.index("Premissas declaradas") < hx.index("Lacunas documentais"))
    chk("premium sem premissas nao traz o titulo da secao", "Premissas declaradas" not in h1)

    # 6/7 — taxa_aa em fração; nome de aba inválido — tudo na mesma planilha
    px["conferencia"]["cenarios"][1]["taxa_aa"] = 0.183737
    px["abas"][0]["nome"] = "Apuração/2025"
    if planilha:
        with tempfile.TemporaryDirectory() as td:
            try:
                x = render_planilha(px, Path(td) / "x.xlsx")
                wb = openpyxl.load_workbook(x)
            except Exception as e:  # noqa: BLE001
                wb = None
                chk("planilha com aba 'Apuração/2025' nao levanta", False, repr(e))
            if wb is not None:
                chk("aba 'Apuração/2025' vira 'Apuração-2025'", "Apuração-2025" in wb.sheetnames)
                ws = wb["Dashboard"]
                fills, taxas = {}, []
                for row in ws.iter_rows(min_col=2, max_col=3):
                    if row[0].value in ("A verificar", "Ilícito", "Conforme", "Inventado"):
                        fills[row[0].value] = row[0].fill.fgColor.rgb if row[0].fill.fill_type else None
                    if isinstance(row[1].value, float):
                        taxas.append(row[1].value)
                chk("XLSX: 'A verificar' recebe fill ambar", fills.get("A verificar") == XLSX_ABG)
                chk("XLSX: verde e vermelho preservados; fora da lista sem fill",
                    fills.get("Conforme") == "FFF2F8F4" and fills.get("Ilícito") == "FFFCF3F3"
                    and fills.get("Inventado") is None)
                chk("XLSX: taxa_aa em fracao vira 18,3737 pontos percentuais",
                    any(abs(t - 18.3737) < 1e-9 for t in taxas))
                wm = wb["Metodologia e fontes"]
                chk("XLSX: metodologia traz PREMISSAS DECLARADAS",
                    any(c.value == "PREMISSAS DECLARADAS" for r in wm.iter_rows() for c in r))
    else:
        pula("aba 'Apuração/2025' vira 'Apuração-2025'", "XLSX: 'A verificar' recebe fill ambar",
             "XLSX: verde e vermelho preservados; fora da lista sem fill",
             "XLSX: taxa_aa em fracao vira 18,3737 pontos percentuais",
             "XLSX: metodologia traz PREMISSAS DECLARADAS")
    chk("taxa_aa em fracao renderiza 18,3737% no premium", "18,3737%" in render_premium(px))
    chk("taxa_aa em fracao gera aviso de conversao",
        any("parece fração" in a for a in validar_detalhado(px)["avisos"]))
    chk("taxa_aa em pontos percentuais nao e alterada",
        taxa_aa_pct(18.3737) == 18.3737 and taxa_aa_pct(None) is None and taxa_aa_pct(0) == 0)
    chk("nome_aba sanitiza e trunca",
        nome_aba("Apuração/2025") == "Apuração-2025" and len(nome_aba("x" * 40)) == 31
        and nome_aba("a:b?c*d[e]f\\g") == "a-b-c-d-e-f-g")

    # 3 — validação estrutural: o que passava e quebrava no render agora é recusado
    def recusa(nome, mut, fmts=None, chave=None):
        q = clone(p)
        mut(q)
        e = validar(q, fmts)
        chk(f"validar recusa {nome}",
            e != [] and (chave is None or any(chave in x for x in e)), str(e)[:70])

    def _div(q):
        q["conferencia"]["veredito"] = "DIVERGENTE"
        q["conferencia"].pop("diferenca")
    recusa("payload sem marca.nome", lambda q: q.__setitem__("marca", {}), chave="marca.nome")
    recusa("payload sem identificacao.campos", lambda q: q["identificacao"].pop("campos"),
           chave="identificacao.campos")
    recusa("DIVERGENTE sem diferenca", _div, chave="conferencia.diferenca")
    recusa("panorama pedido sem panorama.titulo", lambda q: q["panorama"].pop("titulo"),
           {"premium", "panorama"}, "panorama.titulo")
    recusa("veredito fora de CONFORME/DIVERGENTE",
           lambda q: q["conferencia"].__setitem__("veredito", "OK"), chave="conferencia.veredito")
    recusa("achado sem fundamento", lambda q: q["achados"][0].pop("fundamento"), chave="achados[0].fundamento")
    recusa("assinatura sem entidade", lambda q: q["assinatura"].pop("entidade"), chave="assinatura.entidade")
    recusa("campos com 2 elementos",
           lambda q: q["identificacao"]["campos"].append(["Só rótulo", "valor"]), chave="campos[4]")
    recusa("natureza_cenarios invalida",
           lambda q: q["conferencia"].__setitem__("natureza_cenarios", "x"), chave="natureza_cenarios")
    q = clone(p); q["panorama"].pop("titulo")
    chk("panorama sem titulo passa quando o panorama nao foi pedido", validar(q, {"premium"}) == [])
    q = clone(p); q["kpis"] = q["kpis"][:3]
    vq = validar_detalhado(q)
    chk("kpis != 4 gera aviso, nao erro", vq["erros"] == [] and any("kpis" in a for a in vq["avisos"]))
    q = clone(p); q.pop("ressalvas")
    vq = validar_detalhado(q)
    chk("achado pro-banco sem ressalva gera aviso",
        vq["erros"] == [] and any("pró-banco sem ressalva" in a for a in vq["avisos"]))
    chk("validar() segue devolvendo lista; validar_detalhado() devolve erros/avisos",
        isinstance(validar(p), list) and set(validar_detalhado(p)) == {"erros", "avisos"}
        and validar_detalhado(p) == {"erros": [], "avisos": []})

    # 4 — nenhum dado real de operador no módulo (montado por concatenação para não se autoacusar)
    # Registro real de operador (OAB/CRC com número) não pode estar no módulo; os placeholders
    # "OAB/UF 00.000" e "CRC/UF 000000" são admitidos. Nomes reais de escritório e cidade são
    # conferidos por ferramentas/verificar_consistencia.py com a lista local, fora do repositório.
    import re
    fonte = open(__file__, encoding="utf-8").read()
    registros = re.findall(r"(?:OAB|CRC)/[A-Z]{2}\s*\d[\d.]*", fonte)
    reais = [r for r in registros if "/UF" not in r and re.sub(r"\D", "", r).strip("0")]
    chk("modulo nao contem OAB ou CRC reais", not reais, str(reais))

    # 5 — formatação delega a comum; diferença negativa com frase e sinal certos
    chk("brl/brl_rs delegam a comum (HALF_UP, None -> —)",
        brl(1234.565) == "1.234,57" and brl(None) == "—" and brl_rs(-1500) == "R$ -1.500,00")
    chk("pct em pontos percentuais como comum.pct",
        pct(18.3737) == "18,3737%" and pct(0.15, 2) == "0,15%" and pct(None) == "—")
    q = clone(p); q["conferencia"].update(veredito="DIVERGENTE", diferenca=-5000.0, diferenca_pct=-0.32)
    hq = render_premium(q)
    chk("diferenca negativa: valor absoluto e frase invertida",
        "O saldo recalculado excede o apurado pela credora em R$ 5.000,00" in hq and "R$ -" not in hq)
    q["conferencia"].update(diferenca=2357.74, diferenca_pct=0.15)
    chk("diferenca positiva: credora excede o recalculado",
        "O saldo apurado pela credora excede o recalculado em R$ 2.357,74" in render_premium(q))

    # 8 — barras do panorama com valor negativo
    q = clone(p); q["panorama"]["barras"].append({"rotulo": "Saldo credor", "valor": -1000.0})
    hq = render_panorama(q)
    chk("barra negativa: largura 0 e rotulo (negativo)",
        "(negativo)" in hq and "width:-" not in hq and "width:0.0%" in hq)
    q["panorama"]["barras"] = [{"rotulo": "Só negativa", "valor": -10.0}]
    chk("todas as barras negativas nao viram largura positiva", "width:0.0%" in render_panorama(q))

    # 9 — natureza dos cenários
    q = clone(p); q["conferencia"]["natureza_cenarios"] = "recomposicao"
    hq = render_premium(q)
    chk("natureza recomposicao troca a nota dos cenarios",
        "não constituem proposta de recomposição" not in hq and "constituem a base da repetição" in hq
        and "metodologia efetivamente pactuada" not in hq)
    chk("natureza default mantem a nota de conferencia",
        "não constituem proposta de recomposição" in h1 and "metodologia efetivamente pactuada" in h1)

    # 10 — openpyxl ausente: ImportError antes de escrever qualquer arquivo
    g = globals()
    orig = g["openpyxl"]
    g["openpyxl"] = None
    try:
        with tempfile.TemporaryDirectory() as td:
            try:
                gerar(p, Path(td), "demo")
                levantou = False
            except ImportError:
                levantou = True
            chk("sem openpyxl e planilha pedida: ImportError e diretorio vazio",
                levantou and os.listdir(td) == [])
        with tempfile.TemporaryDirectory() as td:
            arqs = gerar(p, Path(td), "demo", {"premium", "panorama"})
            chk("sem openpyxl e so HTML pedido: gera normalmente", len(arqs) == 3)
    finally:
        g["openpyxl"] = orig

    print(f"\n  {ok} passaram · {fail} falharam" + (f" · {pulados} pulados" if pulados else ""))
    return ok, fail, pulados


def autoteste(verbose: bool = True) -> dict:
    """Roda o autoteste embutido e devolve as contagens; `verbose=False` não imprime nada.
    Sem openpyxl, só as asserções da planilha são puladas (`pulados`); o HTML é testado."""
    return rodar_autoteste("relatorios", _autoteste, verbose)


# ─────────────────────────────────────────────────────────────────────
# LINHA DE COMANDO
# ─────────────────────────────────────────────────────────────────────

FORMATOS = ("premium", "panorama", "planilha")


def parse_formatos(texto: str | None) -> set[str] | None:
    """'premium,planilha' -> {'premium', 'planilha'}. Vazio ou None -> None (todos os formatos).
    Nome fora de FORMATOS é ValueError: um erro de digitação não pode virar zero arquivos."""
    if not texto:
        return None
    pedidos = {f.strip() for f in texto.split(",") if f.strip()}
    desconhecidos = sorted(pedidos - set(FORMATOS))
    if desconhecidos:
        raise ValueError(f"formato desconhecido: {', '.join(desconhecidos)}. "
                         f"Use um ou mais de: {', '.join(FORMATOS)}")
    return pedidos or None


def main(argv: list[str] | None = None) -> int:
    """`python -m motores.relatorios PAYLOAD.json --saida DIR [--formatos premium,panorama,planilha]`
    ou `python -m motores.relatorios --autoteste`. A linha de comando `revisao.py gerar` reaproveita
    `parse_formatos()` e `gerar()` e acrescenta a identidade do operador ao payload."""
    ap = argparse.ArgumentParser(
        prog="python -m motores.relatorios",
        description="Renderiza o laudo (PREMIUM, PANORAMA e planilha) a partir do payload JSON.")
    ap.add_argument("payload", nargs="?", help="payload.json (contrato em referencia/payload-schema.md)")
    ap.add_argument("--saida", help="pasta de saída dos arquivos (obrigatório)")
    ap.add_argument("--formatos", help="subconjunto de premium,panorama,planilha, separado por "
                                       "vírgula (padrão: todos)")
    ap.add_argument("--autoteste", action="store_true", help="roda o autoteste do módulo")
    args = ap.parse_args(argv)
    if args.autoteste:
        print("\n  motores/relatorios.py — autoteste\n")
        return 1 if autoteste()["falharam"] else 0
    if not args.payload or not args.saida:
        ap.error("informe o payload e --saida (obrigatório)")
    try:
        formatos = parse_formatos(args.formatos)
    except ValueError as erro:
        ap.error(str(erro))
    payload = json.loads(Path(args.payload).read_text(encoding="utf-8-sig"))
    for f in gerar(payload, Path(args.saida), formatos=formatos):
        print(f)
    return 0


if __name__ == "__main__":
    saida_utf8()
    raise SystemExit(main())
