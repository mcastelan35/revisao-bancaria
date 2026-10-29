"""Autoteste de cada motor (contagens exatas, sem falhas), o pacote `motores` sem hacks de
caminho e o que é comum aos motores (`comum`, `relatorios.main`)."""
import importlib
import json
import re
import subprocess
import sys

import pytest

from conftest import SKILL
from motores import VERSAO, comum, relatorios

CONTAGENS = {"comum": 17, "calculo": 77, "cet": 97, "cartao": 53, "conta_corrente": 67}
MODULOS = ("comum", "calculo", "cet", "cartao", "conta_corrente", "relatorios", "regras")


def _mudo(capsys):
    """verbose=False não imprime nada, nem em stdout nem em stderr."""
    saida = capsys.readouterr()
    assert saida.out == "" and saida.err == ""


@pytest.mark.parametrize("nome,esperado", sorted(CONTAGENS.items()))
def test_autoteste_do_motor_tem_a_contagem_exata(nome, esperado, capsys):
    modulo = importlib.import_module(f"motores.{nome}")
    assert modulo.autoteste(verbose=False) == {
        "modulo": nome, "passaram": esperado, "falharam": 0, "pulados": 0}
    _mudo(capsys)


def test_autoteste_do_motor_de_regras(capsys):
    from motores import regras
    r = regras.autoteste(verbose=False)
    assert r["modulo"] == "regras" and r["falharam"] == 0 and r["pulados"] == 0 and r["passaram"] >= 40
    _mudo(capsys)


def test_autoteste_do_renderizador_com_planilha(capsys):
    pytest.importorskip("openpyxl")
    assert relatorios.PLANILHA_DISPONIVEL is True
    assert relatorios.autoteste(verbose=False) == {
        "modulo": "relatorios", "passaram": 110, "falharam": 0, "pulados": 0}
    _mudo(capsys)


def test_autoteste_do_renderizador_pula_so_a_planilha(monkeypatch, capsys):
    """Simula a ausência do openpyxl: o HTML continua testado e nada falha."""
    monkeypatch.setattr(relatorios, "PLANILHA_DISPONIVEL", False)
    r = relatorios.autoteste(verbose=False)
    assert (r["falharam"], r["pulados"], r["passaram"]) == (0, 13, 97)
    _mudo(capsys)


def test_autoteste_do_renderizador_pula_a_planilha_se_o_modulo_some_depois_do_import(monkeypatch, capsys):
    monkeypatch.setattr(relatorios, "openpyxl", None)
    r = relatorios.autoteste(verbose=False)
    assert (r["falharam"], r["pulados"], r["passaram"]) == (0, 13, 97)
    _mudo(capsys)


def test_renderizador_importa_e_testa_sem_openpyxl_de_verdade():
    """Processo à parte com o openpyxl bloqueado: o módulo importa e o autoteste não quebra."""
    codigo = (
        "import sys, json; sys.modules['openpyxl'] = None; sys.path.insert(0, sys.argv[1]);"
        "from motores import relatorios;"
        "print(json.dumps([relatorios.PLANILHA_DISPONIVEL, relatorios.autoteste(verbose=False)]))")
    p = subprocess.run([sys.executable, "-c", codigo, str(SKILL)], capture_output=True,
                       text=True, encoding="utf-8", timeout=120)
    assert p.returncode == 0, p.stderr
    disponivel, resultado = json.loads(p.stdout)
    assert disponivel is False
    assert resultado["falharam"] == 0 and resultado["pulados"] == 13 and resultado["passaram"] == 97


def test_autoteste_verbose_true_imprime_as_linhas(capsys):
    comum.autoteste()
    saida = capsys.readouterr().out
    assert "PASS  brl HALF_UP" in saida and "17 passaram · 0 falharam" in saida


@pytest.mark.parametrize("nome", MODULOS)
def test_modulo_roda_como_pacote_de_dentro_da_skill(nome):
    """`python -m motores.<modulo>` (de skills/revisao-bancaria/): imprime o autoteste e sai com 0."""
    args = ["--autoteste"] if nome == "relatorios" else []
    p = subprocess.run([sys.executable, "-m", f"motores.{nome}", *args], cwd=SKILL,
                       capture_output=True, text=True, encoding="utf-8", timeout=180)
    assert p.returncode == 0, p.stdout[-500:] + p.stderr[-500:]
    assert re.search(r"\d+ passaram · 0 falharam", p.stdout)


def test_motores_sem_hack_de_caminho_nem_import_absoluto():
    for arq in sorted((SKILL / "motores").glob("*.py")):
        texto = arq.read_text(encoding="utf-8")
        assert "sys.path" not in texto, arq.name
        assert "importlib.util" not in texto and "carregar_motores" not in texto, arq.name
        assert not re.search(r"^\s*from comum import", texto, re.M), arq.name


def test_versao_do_pacote_esta_na_forma_que_o_verificador_le():
    init = (SKILL / "motores" / "__init__.py").read_text(encoding="utf-8")
    achado = re.search(r'^VERSAO\s*=\s*"([^"]+)"', init, re.M)
    assert achado and achado.group(1) == VERSAO


# ── comum ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("valor,casas,esperado", [
    (0.125, 2, 0.13), (2.675, 2, 2.68), (-0.125, 2, -0.13), (1 / 3, 4, 0.3333),
    (1.00005, 4, 1.0001), (2, 2, 2.0)])
def test_arredondar_e_half_up_em_decimal(valor, casas, esperado):
    assert comum.arredondar(valor, casas) == esperado


def test_rodar_autoteste_monta_o_dicionario_e_suprime_a_saida(capsys):
    def testes():
        print("ruído")
        print("ruído de erro", file=sys.stderr)
        return 3, 1, 2

    assert comum.rodar_autoteste("x", testes, verbose=False) == {
        "modulo": "x", "passaram": 3, "falharam": 1, "pulados": 2}
    assert capsys.readouterr().out == ""
    assert comum.rodar_autoteste("x", lambda: (4, 0), verbose=True)["pulados"] == 0


# ── relatorios.main ───────────────────────────────────────────────────

def test_parse_formatos():
    assert relatorios.parse_formatos(None) is None and relatorios.parse_formatos("") is None
    assert relatorios.parse_formatos("premium, planilha ,") == {"premium", "planilha"}


def test_relatorios_main_gera_a_partir_do_payload(tmp_path, capsys):
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps(relatorios._payload_demo(), ensure_ascii=False), encoding="utf-8")
    assert relatorios.main([str(payload), "--saida", str(tmp_path / "saida"), "--formatos", "premium"]) == 0
    impresso = capsys.readouterr().out.splitlines()
    assert any(l.endswith("laudo-premium-demo.html") for l in impresso)
    assert (tmp_path / "saida" / "laudo-premium-demo.html").is_file()
    assert not (tmp_path / "saida" / "panorama-estrategico-demo.html").exists()


@pytest.mark.parametrize("argv", [[], ["payload.json"], ["--saida", "x"]])
def test_relatorios_main_exige_payload_e_saida(argv):
    with pytest.raises(SystemExit) as saida:
        relatorios.main(argv)
    assert saida.value.code == 2


def test_relatorios_main_autoteste(capsys):
    assert relatorios.main(["--autoteste"]) == 0
    assert "passaram · 0 falharam" in capsys.readouterr().out
