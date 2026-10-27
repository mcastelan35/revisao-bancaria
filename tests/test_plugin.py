"""Coerência do pacote do plugin: manifestos, versões, skills, consistência, empacotador e sigilo."""

import importlib.util
import json
import re
import subprocess
import sys

import pytest

from conftest import RAIZ, SKILL

SKILLS = ("revisao-bancaria", "triagem", "configurar")
CLI = '"${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"'


def _ler(rel: str) -> str:
    return (RAIZ / rel).read_text(encoding="utf-8")


def _frontmatter(texto: str) -> str:
    assert texto.startswith("---\n")
    return texto.split("---", 2)[1]


def _modulo(caminho):
    spec = importlib.util.spec_from_file_location(caminho.stem, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_versao_unica_em_todos_os_lugares():
    from motores import VERSAO

    plugin = json.loads(_ler(".claude-plugin/plugin.json"))
    mercado = json.loads(_ler(".claude-plugin/marketplace.json"))
    [entrada] = mercado["plugins"]
    regras = json.loads(_ler("skills/revisao-bancaria/dados/regras-bancarias.json"))
    skill = re.search(r'^\s*version:\s*"([^"]+)"', _ler("skills/revisao-bancaria/SKILL.md"), re.M).group(1)
    changelog = re.search(r"^## v(\d+\.\d+\.\d+)", _ler("CHANGELOG.md"), re.M).group(1)
    arquitetura = re.search(r"Versão do pacote:\s*\*\*v(\d+\.\d+\.\d+)", _ler("ARCHITECTURE.md")).group(1)
    versoes = {plugin["version"], mercado["metadata"]["version"], entrada["version"], regras["versao"],
               regras["notas_de_versao"][-1]["versao"], skill, changelog, arquitetura, VERSAO}
    assert versoes == {VERSAO}, versoes


def test_manifestos_descrevem_o_mesmo_plugin():
    plugin = json.loads(_ler(".claude-plugin/plugin.json"))
    [entrada] = json.loads(_ler(".claude-plugin/marketplace.json"))["plugins"]
    assert plugin["name"] == entrada["name"] == "revisao-bancaria"
    assert entrada["source"] == "./"
    assert entrada["category"] == "legal"


@pytest.mark.parametrize("skill", SKILLS)
def test_skills_tem_cabecalho_valido(skill):
    cabecalho = _frontmatter(_ler(f"skills/{skill}/SKILL.md"))
    assert re.search(rf"^name: {skill}$", cabecalho, re.M)
    descricao = re.search(r'^description: "(.*)"$', cabecalho, re.M).group(1)
    assert 80 <= len(descricao) <= 1000          # limite de upload do claude.ai é 1024
    permissoes = re.findall(r"^\s+- (?:Bash|PowerShell)\((.*)\)$", cabecalho, re.M)
    assert permissoes and all(CLI in p for p in permissoes)


def test_skills_usam_o_comando_base_da_cli():
    assert (SKILL / "revisao.py").is_file()
    for skill in SKILLS:
        assert CLI in _ler(f"skills/{skill}/SKILL.md")


def test_verificacao_de_consistencia_passa():
    r = subprocess.run([sys.executable, "-X", "utf8", str(RAIZ / "ferramentas" / "verificar_consistencia.py")],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout[-3000:] + r.stderr[-2000:]


def test_empacotador_confere_versoes_e_filtra_arquivos(tmp_path):
    emp = _modulo(RAIZ / "ferramentas" / "empacotar_plugin.py")
    assert len(set(emp.versoes().values())) == 1
    lixo = [tmp_path / "__pycache__" / "x.pyc", tmp_path / "laudo.pdf", tmp_path / "extrato.csv",
            tmp_path / "planilha.xlsx", tmp_path / "operador.json", tmp_path / "tema.json",
            tmp_path / "tema-logo.png"]
    for arq in lixo:
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text("x", encoding="utf-8")
        assert not emp.entra(arq), arq
    bom = tmp_path / "SKILL.md"
    bom.write_text("x", encoding="utf-8")
    assert emp.entra(bom)


def test_gitignore_protege_documentos_de_clientes():
    regras = _ler(".gitignore").splitlines()
    for padrao in ("*.pdf", "*.csv", "*.xlsx", "*.docx", "operador.json", "tema.json", "INTERNO-*.md",
                   "ferramentas/identidades-locais.txt", "dist/"):
        assert padrao in regras, padrao


# Processo de cliente costuma tramitar na Justiça Estadual (segmento J = 8 no número CNJ). Número
# estadual em arquivo versionado é, até prova em contrário, dado de caso real. A exceção é o
# precedente público de TJ do repertório jurisprudencial: admitido só dentro dele, como
# `classe_numero` (ou no link permanente) de uma entrada com fonte pública (Jusbrasil ou portal
# oficial do tribunal) ou citado na ementa integral dessa entrada (texto do tribunal). Em observação ou qualquer outro
# texto, recusado.
CNJ_ESTADUAL = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.8\.\d{2}\.\d{4}\b")
REPERTORIO = SKILL / "referencia" / "repertorio-jurisprudencial.md"
IGNORADAS = (".git", "__pycache__", "dist", ".pesquisa", ".venv")


def _precedentes_estaduais_do_repertorio() -> set[str]:
    from motores import jurisprudencia
    _, entradas, _ =jurisprudencia._parse(REPERTORIO.read_text(encoding="utf-8"))
    fontes = [e for e in entradas if jurisprudencia.fonte_valida(e.get("url", ""), e.get("tribunal", ""))]
    return ({m.group(0) for e in fontes if e.get("tribunal") not in jurisprudencia.SUPERIORES
             for m in CNJ_ESTADUAL.finditer(e.get("classe_numero", ""))}
            | {m.group(0) for e in fontes for m in CNJ_ESTADUAL.finditer(e.get("ementa", ""))})


def test_nenhum_numero_de_processo_estadual_nos_arquivos_versionados():
    admitidos = _precedentes_estaduais_do_repertorio()
    suspeitos = []
    for arq in RAIZ.rglob("*"):
        if not arq.is_file() or any(p in arq.parts for p in IGNORADAS):
            continue
        if arq.suffix not in (".md", ".py", ".json", ".yml", ".txt"):
            continue
        texto = arq.read_text(encoding="utf-8", errors="ignore")
        if arq == REPERTORIO:
            for linha in texto.splitlines():
                for m in CNJ_ESTADUAL.finditer(linha):
                    if m.group(0) not in admitidos or not linha.startswith(
                            ("### ", "- classe_numero:", "- url:", ">")):
                        suspeitos.append(f"{arq.relative_to(RAIZ).as_posix()}: {m.group(0)}")
            continue
        for m in CNJ_ESTADUAL.finditer(texto):
            suspeitos.append(f"{arq.relative_to(RAIZ).as_posix()}: {m.group(0)}")
    assert not suspeitos, suspeitos
