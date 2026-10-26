"""verificar_consistencia.py — autoteste documental do plugin revisao-bancaria.

Os motores têm autoteste; a documentação não tinha, e foi ela que descolou ao longo das versões
(contagem de regras, versão, tiers, cores do schema, OAB literal em exemplo, regra de conduta
duplicada, caminho de arquivo que não existe mais). Este script FALHA quando manifestos,
SKILL.md, camadas, referências, JSON e renderizador contam histórias diferentes.

    python ferramentas/verificar_consistencia.py          # exit 0 = consistente

FALHA (exit 1): divergência que produz instrução errada ao agente ou dado errado no laudo.
AVISO (exit 0): coisa a olhar (pendência jurisprudencial vencida, etc.).

Nomes reais que nunca podem aparecer na skill vão em `ferramentas/identidades-locais.txt`
(um por linha, fora do repositório); os padrões genéricos de OAB/CRC valem sempre.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "skills" / "revisao-bancaria"
NOME = "revisao-bancaria"
SKILLS_DO_PLUGIN = ("revisao-bancaria", "triagem", "configurar")
COMANDO_CLI = '"${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"'
# Caminhos e nomes da skill v5 (pacote `revisao-contratos-bancarios`) que não podem voltar.
NOMES_ANTIGOS = ("reference/", "carregar_motores", "gerar-relatorios", "verificar-consistencia",
                 "motor-calculo", "motor-cet", "motor-cartao", "motor-conta-corrente",
                 "revisao-contratos-bancarios", "config/operador.json")

FALHAS: list[str] = []
AVISOS: list[str] = []


def falha(msg): FALHAS.append(msg); print(f"  FAIL  {msg}")
def ok(msg): print(f"  PASS  {msg}")
def aviso(msg): AVISOS.append(msg); print(f"  WARN  {msg}")


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


def rel(caminho: Path) -> str:
    return caminho.relative_to(RAIZ).as_posix()


def docs_da_skill() -> list[Path]:
    """Markdown que o agente lê: SKILL.md das três skills, camadas e referências."""
    out = [RAIZ / "skills" / s / "SKILL.md" for s in SKILLS_DO_PLUGIN]
    for pasta in ("camadas", "referencia"):
        out += sorted((SKILL / pasta).glob("*.md"))
    return out


def docs_com_contagens() -> list[Path]:
    return docs_da_skill() + [RAIZ / "ARCHITECTURE.md", RAIZ / "README.md"]


def frontmatter(texto: str) -> str:
    partes = texto.split("---", 2)
    return partes[1] if len(partes) >= 3 and texto.startswith("---") else ""


def main() -> int:
    plugin = json.loads(ler(RAIZ / ".claude-plugin" / "plugin.json"))
    mercado = json.loads(ler(RAIZ / ".claude-plugin" / "marketplace.json"))
    skill = ler(SKILL / "SKILL.md")
    arch = ler(RAIZ / "ARCHITECTURE.md")
    changelog = ler(RAIZ / "CHANGELOG.md")
    regras = json.loads(ler(SKILL / "dados" / "regras-bancarias.json"))

    # ── 1. versão única ─────────────────────────────────────────────
    def achar(padrao, texto):
        m = re.search(padrao, texto, re.M)
        return m.group(1) if m else None

    versoes = {
        "plugin.json": plugin.get("version"),
        "marketplace.json (metadata)": mercado.get("metadata", {}).get("version"),
        "marketplace.json (plugin)": (mercado.get("plugins") or [{}])[0].get("version"),
        "SKILL.md": achar(r'^\s*version:\s*"([^"]+)"', skill),
        "regras-bancarias.json": regras.get("versao"),
        "motores/__init__.py": achar(r'^VERSAO\s*=\s*"([^"]+)"', ler(SKILL / "motores" / "__init__.py")),
        "CHANGELOG.md": achar(r"^## v?(\d+\.\d+(?:\.\d+)?)", changelog),
        "ARCHITECTURE.md": achar(r"Versão do pacote:\s*\*?\*?v?(\d+\.\d+(?:\.\d+)?)", arch),
    }
    if None not in versoes.values() and len(set(versoes.values())) == 1:
        ok(f"versão única: {versoes['plugin.json']}")
    else:
        falha(f"versões divergentes: {versoes}")
    ultima_nota = regras["notas_de_versao"][-1]["versao"] if regras.get("notas_de_versao") else None
    if ultima_nota == regras.get("versao"):
        ok("última nota_de_versao do JSON = versao do JSON")
    else:
        falha(f"JSON versao {regras.get('versao')} sem nota_de_versao correspondente (última: {ultima_nota})")

    # ── 2. manifestos e skills do plugin ────────────────────────────
    [entrada] = mercado["plugins"]
    if plugin["name"] == entrada["name"] == NOME and entrada.get("source") == "./":
        ok("plugin.json e marketplace.json descrevem o mesmo plugin (source ./)")
    else:
        falha("nome ou source divergente entre plugin.json e marketplace.json")
    pastas = sorted(p.name for p in (RAIZ / "skills").iterdir() if (p / "SKILL.md").exists())
    if pastas == sorted(SKILLS_DO_PLUGIN):
        ok(f"skills do plugin: {', '.join(pastas)}")
    else:
        falha(f"skills encontradas {pastas} ≠ esperadas {sorted(SKILLS_DO_PLUGIN)}")
    for s in SKILLS_DO_PLUGIN:
        cab = frontmatter(ler(RAIZ / "skills" / s / "SKILL.md"))
        nome = achar(r'^name:\s*"?([\w-]+)"?\s*$', cab)
        desc = re.search(r'^description:\s*"(.*?)"\s*$', cab, re.M | re.S)
        if nome != s:
            falha(f"skills/{s}/SKILL.md: name '{nome}' ≠ pasta '{s}'")
        if not desc or not (80 <= len(desc.group(1)) <= 1000):
            falha(f"skills/{s}/SKILL.md: description ausente ou fora de 80–1000 caracteres "
                  f"({len(desc.group(1)) if desc else 0})")
        for linha in re.findall(r"^\s+- (?:Bash|PowerShell)\((.*)\)$", cab, re.M):
            if COMANDO_CLI not in linha:
                falha(f"skills/{s}/SKILL.md: allowed-tools fora do comando base: {linha}")
    ok("frontmatter das skills: name = pasta, description de 80 a 1000 caracteres, allowed-tools no comando base")
    if (SKILL / "revisao.py").exists():
        ok("linha de comando skills/revisao-bancaria/revisao.py existe")
    else:
        falha("skills/revisao-bancaria/revisao.py não existe")

    # ── 3. contagens do JSON vs prosa ───────────────────────────────
    r03 = next(r for r in regras["regras"] if r["id"] == "R03")
    esperado = {
        "regras": (len(regras["regras"]), r"\b(\d+)\s+regras\b(?!\s+de\s+conduta)"),
        "marcos": (len(regras["marcos_temporais"]["marcos"]), r"\b(\d+)\s+marcos\b"),
        "categorias": (len(regras["categorias"]), r"\b(\d+)\s+categorias\b"),
        "súmulas": (len(regras["sumulas_consolidadas"]["sumulas"]), r"\b(\d+)\s+súmulas\b"),
        "séries": (len(regras["series_bacen_por_modalidade"]["mapeamento"]), r"\b(\d+)\s+séries\b"),
        "tipos": (len(regras["tipos_contrato"]["tipos"]), r"\b(\d+)\s+tipos\b"),
        "termos": (len(r03["padroes_deteccao"]["termos_suspeitos"]), r"\b(\d+)\s+termos\b"),
    }
    textos = docs_com_contagens()
    textos += [RAIZ / ".claude-plugin" / "plugin.json", RAIZ / ".claude-plugin" / "marketplace.json"]
    for caminho in textos:
        txt = ler(caminho)
        for rotulo, (n, pad) in esperado.items():
            for m in re.finditer(pad, txt):
                ctx = txt[max(0, m.start() - 25):m.start()].lower()
                if any(h in ctx for h in ("eram ", "era ", "de ", "antes", "v4", "v5.0", "5.0")):
                    continue
                if int(m.group(1)) != n:
                    falha(f"{rel(caminho)}: diz '{m.group(0)}', o JSON tem {n}")
    ok("contagens em prosa conferidas contra o JSON (" +
       ", ".join(f"{k} {v[0]}" for k, v in esperado.items()) + ")")

    tiers = [r.get("tier") for r in regras["regras"]]
    trio = (tiers.count("T1"), tiers.count("T2"), tiers.count(None))
    m_t = re.search(r"\((\d+) T1, (\d+) T2, (\d+) sem tier\)", arch)
    if m_t and tuple(map(int, m_t.groups())) == trio:
        ok(f"tiers em ARCHITECTURE = ({trio[0]} T1, {trio[1]} T2, {trio[2]} sem tier)")
    else:
        falha(f"ARCHITECTURE tiers {m_t.groups() if m_t else None} ≠ JSON {trio}")

    # ── 4. integridade do JSON (derivações) ─────────────────────────
    ids = [r["id"] for r in regras["regras"]]
    if len(ids) != len(set(ids)):
        falha("ids de regra duplicados")
    por_marco: dict[str, set] = {}
    for r in regras["regras"]:
        mk = (r.get("corte_temporal") or {}).get("marco")
        if mk:
            por_marco.setdefault(mk, set()).add(r["id"])
        for k in (r.get("regime_por_marco") or {}):
            mm = re.search(r"MT\d+", k)
            if mm:
                por_marco.setdefault(mm.group(0), set()).add(r["id"])
    bases = {"contrato", "pagamento", "operacao", "contrato_ou_consolidacao"}
    for m in regras["marcos_temporais"]["marcos"]:
        if set(m["regras_afetadas"]) != por_marco.get(m["id"], set()):
            falha(f"{m['id']}.regras_afetadas {m['regras_afetadas']} ≠ derivado {sorted(por_marco.get(m['id'], set()))}")
        if m.get("base") not in bases:
            falha(f"{m['id']}.base inválida: {m.get('base')!r}")
    tipos = regras["tipos_contrato"]["tipos"]
    grupos = regras["tipos_contrato"].get("grupos", {})
    derivados = {
        "todos": [t["id"] for t in tipos],
        "todos_sfn": [t["id"] for t in tipos if t.get("credor_sfn", True)],
        "todos_sem_lei_especifica": [t["id"] for t in tipos if not t.get("legislacao_especifica")],
    }
    for g, lista in derivados.items():
        if grupos.get(g) != lista:
            falha(f"tipos_contrato.grupos.{g} {grupos.get(g)} ≠ derivado {lista}")
    validos = set(derivados["todos"]) | set(derivados)
    for r in regras["regras"]:
        for tag in r["tipo_contrato"]:
            if tag not in validos:
                falha(f"{r['id']}: tipo_contrato '{tag}' não é tipo nem grupo")
    ok("marcos (base e regras_afetadas), grupos de tipo e tags de tipo_contrato coerentes")

    # ── 5. CORES do renderizador = lista do payload-schema ──────────
    schema = ler(SKILL / "referencia" / "payload-schema.md")
    sec = re.search(r"## Valores admitidos em `resultado`\n\n(.*?)\n\n", schema, re.S)
    vals_schema = {v for v in re.findall(r"`([^`]+)`", sec.group(1))
                   if not any(c in v for c in "()_.")} if sec else set()
    try:
        sys.path.insert(0, str(SKILL))
        from motores import relatorios  # noqa: PLC0415
        vals_cores = set(relatorios.CORES)
        if vals_schema and vals_schema == vals_cores:
            ok(f"CORES do renderizador = {len(vals_cores)} valores do schema")
        else:
            falha(f"CORES ≠ schema: só no schema {sorted(vals_schema - vals_cores)}; só em CORES {sorted(vals_cores - vals_schema)}")
    except Exception as e:  # pragma: no cover
        falha(f"não foi possível carregar motores.relatorios: {e}")

    # ── 6. identidade pré-preenchida ────────────────────────────────
    proibidos = [r"OAB/[A-Z]{2}\s*\d{1,3}\.\d{3}", r"CRC/[A-Z]{2}\s*\d{6}"]
    locais = RAIZ / "ferramentas" / "identidades-locais.txt"
    if locais.exists():
        proibidos += [re.escape(l.strip()) for l in ler(locais).splitlines()
                      if l.strip() and not l.lstrip().startswith("#")]
    varridos = [p for p in sorted((RAIZ / "skills").rglob("*"))
                if p.is_file() and p.suffix in (".md", ".py", ".json") and "__pycache__" not in p.parts]
    varridos += sorted((RAIZ / "tests").rglob("*.py")) if (RAIZ / "tests").exists() else []
    for caminho in varridos:
        txt = ler(caminho)
        for pad in proibidos:
            for m in re.finditer(pad, txt, re.I):
                achado = m.group(0)
                # placeholders admitidos: "OAB/UF 00.000", "CRC/UF 000000/O" e registros só com zeros
                if "/UF" in achado.upper() or not re.sub(r"\D", "", achado).strip("0") and re.search(r"\d", achado):
                    continue
                falha(f"{rel(caminho)}: identidade pré-preenchida '{achado}' (regra de conduta 26)")
    ok(f"nenhuma identidade de operador pré-preenchida nos arquivos da skill e dos testes "
       f"({len(varridos)} arquivos{', lista local aplicada' if locais.exists() else ''})")

    # ── 7. regras de conduta numeradas e referências cruzadas ───────
    sec_rc = re.search(r"## Regras de conduta(.*?)\n## ", skill, re.S)
    nums = [int(x) for x in re.findall(r"^(\d+)\. \*\*", sec_rc.group(1), re.M)] if sec_rc else []
    if nums and nums == list(range(0, len(nums))):
        ok(f"regras de conduta 0..{nums[-1]} sem repetição")
    else:
        falha(f"regras de conduta com numeração irregular: {nums}")
    max_rc = nums[-1] if nums else -1
    for caminho in docs_com_contagens():
        for m in re.finditer(r"[Rr]egras? de conduta (\d+)", ler(caminho)):
            if int(m.group(1)) > max_rc:
                falha(f"{rel(caminho)}: referência à regra de conduta {m.group(1)}, que não existe (máx. {max_rc})")
    ok("referências cruzadas a regras de conduta apontam para regras existentes")

    # ── 8. arquivos citados existem; caminhos antigos não voltam ────
    for caminho in docs_da_skill() + [RAIZ / "ARCHITECTURE.md", RAIZ / "README.md"]:
        txt = ler(caminho)
        for m in re.finditer(r"`((?:camadas|referencia|motores|dados)/[\w\-\.]+\.(?:md|py|json))", txt):
            if not (SKILL / m.group(1)).exists():
                falha(f"{rel(caminho)}: cita {m.group(1)}, que não existe na skill")
        for m in re.finditer(r"`((?:ferramentas|tests|skills)/[\w\-\./]+\.(?:md|py|json|yml))", txt):
            if not (RAIZ / m.group(1)).exists():
                falha(f"{rel(caminho)}: cita {m.group(1)}, que não existe no repositório")
        for antigo in NOMES_ANTIGOS:
            if antigo in txt:
                falha(f"{rel(caminho)}: caminho ou nome do pacote antigo '{antigo}'")
    # No JSON, as notas de versão são histórico e citam os nomes antigos; o resto é instrução viva.
    vivo = json.dumps({k: v for k, v in regras.items() if k != "notas_de_versao"}, ensure_ascii=False)
    for antigo in (*NOMES_ANTIGOS, "skills/L", "skills/C0"):
        if antigo in vivo:
            falha(f"dados/regras-bancarias.json: caminho ou nome do pacote antigo '{antigo}' fora das notas de versão")
    ok("arquivos citados existem e não há caminho do pacote antigo nos documentos nem no JSON")

    # ── 9. séries: 4390 nunca descrita como diária ──────────────────
    for caminho in docs_da_skill():
        for m in re.finditer(r"di[áa]ri[ao][^\n.]{0,80}4390|4390[^\n.]{0,40}di[áa]ri", ler(caminho)):
            if "não" in m.group(0) or "acumulada" in m.group(0):
                continue
            falha(f"{rel(caminho)}: 4390 (Selic mensal) descrita como diária: '{m.group(0)[:70]}'")
    ok("4390 não aparece como série diária")

    # ── 10. pendências jurisprudenciais vencidas (aviso) ────────────
    pend = regras.get("pendencias_jurisprudenciais", {})
    hoje = date.today()
    vencidas = 0
    for t in pend.get("temas", []):
        dias = (hoje - date.fromisoformat(t["verificado_em"])).days
        if dias > pend.get("validade_dias", 90):
            vencidas += 1
            aviso(f"{t['tema']} conferido há {dias} dias (validade {pend.get('validade_dias')}) — validar via JusIA e publicar nova versão")
    if not vencidas:
        ok("pendências jurisprudenciais dentro da validade")

    print(f"\n  {len(FALHAS)} falha(s) · {len(AVISOS)} aviso(s)")
    return 1 if FALHAS else 0


if __name__ == "__main__":
    for _f in (sys.stdout, sys.stderr):
        try:
            _f.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    raise SystemExit(main())
