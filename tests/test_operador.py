"""Identidade de quem assina o laudo (`motores/operador.py`): pasta de configuração por
precedência, gravação e leitura, chave desconhecida e avisos de registro.

Nenhum nome, OAB ou CRC real: só os placeholders do plugin. Nada escreve na pasta real do usuário."""
import json
import sys
from datetime import datetime
from pathlib import Path

import pytest

from motores import operador

NOME, ENTIDADE, CIDADE = "Fulana de Tal", "Escritório Exemplo", "Cidade-UF"
OAB, CRC = "OAB/UF 00.000", "CRC/UF 000000/O"


@pytest.fixture(autouse=True)
def ambiente_limpo(monkeypatch, tmp_path):
    """Sem variáveis do ambiente real; HOME e LOCALAPPDATA/XDG apontam para uma casa de mentira."""
    for var in ("REVISAO_BANCARIA_CONFIG_DIR", "CLAUDE_PLUGIN_DATA", "LOCALAPPDATA", "XDG_CONFIG_HOME"):
        monkeypatch.delenv(var, raising=False)
    casa = tmp_path / "casa"
    casa.mkdir()
    monkeypatch.setenv("HOME", str(casa))
    monkeypatch.setenv("USERPROFILE", str(casa))
    return casa


# ── pasta de configuração ─────────────────────────────────────────────

def test_config_dir_explicito_vence_tudo(monkeypatch, tmp_path):
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(tmp_path / "env1"))
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "env2"))
    assert operador.pasta_config(str(tmp_path / "arg")) == tmp_path / "arg"
    assert operador.pasta_config(tmp_path / "arg") == tmp_path / "arg"


def test_variavel_do_revisao_vence_a_do_plugin(monkeypatch, tmp_path):
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(tmp_path / "env1"))
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "env2"))
    assert operador.pasta_config() == tmp_path / "env1"
    assert operador.pasta_config("") == tmp_path / "env1"          # argumento vazio não conta


def test_variavel_do_plugin_quando_e_a_unica(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "dados-do-plugin"))
    assert operador.pasta_config() == tmp_path / "dados-do-plugin"
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", "   ")        # só espaços: vazio
    assert operador.pasta_config() == tmp_path / "dados-do-plugin"


@pytest.mark.parametrize("literal", ["${CLAUDE_PLUGIN_DATA}", "${CLAUDE_PLUGIN_DATA}/dados", "x${VAR}y"])
def test_variavel_nao_substituida_conta_como_vazia(monkeypatch, tmp_path, literal):
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", literal)
    assert operador.pasta_config() == operador._pasta_padrao()
    assert "${" not in str(operador.pasta_config())
    assert operador.pasta_config(literal) == operador._pasta_padrao()
    # com a variável do projeto válida, a literal do plugin é só ignorada
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(tmp_path / "valida"))
    assert operador.pasta_config(literal) == tmp_path / "valida"


def test_literal_no_argumento_cai_para_a_variavel_seguinte(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "dados-do-plugin"))
    assert operador.pasta_config("${CLAUDE_PLUGIN_DATA}") == tmp_path / "dados-do-plugin"


def test_padrao_no_windows(monkeypatch, tmp_path, ambiente_limpo):
    monkeypatch.setattr(sys, "platform", "win32")
    assert operador.pasta_config() == ambiente_limpo / "AppData" / "Local" / "RevisaoBancaria"
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))
    assert operador.pasta_config() == tmp_path / "local" / "RevisaoBancaria"
    monkeypatch.setenv("LOCALAPPDATA", "${LOCALAPPDATA}")
    assert operador.pasta_config() == ambiente_limpo / "AppData" / "Local" / "RevisaoBancaria"


def test_padrao_no_macos(monkeypatch, ambiente_limpo):
    monkeypatch.setattr(sys, "platform", "darwin")
    assert operador.pasta_config() == ambiente_limpo / "Library" / "Application Support" / "RevisaoBancaria"


def test_padrao_no_linux(monkeypatch, tmp_path, ambiente_limpo):
    monkeypatch.setattr(sys, "platform", "linux")
    assert operador.pasta_config() == ambiente_limpo / ".config" / "revisao-bancaria"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    assert operador.pasta_config() == tmp_path / "xdg" / "revisao-bancaria"


def test_padrao_do_sistema_atual_e_absoluto_e_nao_e_a_do_plugin(ambiente_limpo):
    pasta = operador.pasta_config()
    assert pasta.is_absolute() and ambiente_limpo in pasta.parents
    assert pasta.name in ("RevisaoBancaria", "revisao-bancaria")


def test_til_no_argumento_expande_para_a_casa(ambiente_limpo):
    assert operador.pasta_config("~/dados-rb") == ambiente_limpo / "dados-rb"


# ── gravar e ler ──────────────────────────────────────────────────────

def test_ler_sem_arquivo_devolve_none(tmp_path):
    assert operador.ler(tmp_path / "nada") is None


def test_salvar_e_ler(tmp_path):
    pasta = tmp_path / "um" / "dois"                       # a pasta é criada, inclusive as intermediárias
    arquivo, avisos = operador.salvar(
        {"tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE,
         "skill_peticao": "peticoes-exemplo"}, pasta)
    assert arquivo == pasta / "operador.json" and arquivo.is_file() and avisos == []
    lido = operador.ler(pasta)
    assert {k: lido[k] for k in lido if k != "atualizado_em"} == {
        "tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE,
        "skill_peticao": "peticoes-exemplo"}
    assert isinstance(datetime.fromisoformat(lido["atualizado_em"]), datetime)


def test_arquivo_e_utf8_com_indent_2(tmp_path):
    arquivo, _ = operador.salvar({"tipo": "contador", "nome": "Fulana de Tal", "entidade": "Escritório Exemplo Ltda"},
                                 tmp_path)
    bruto = arquivo.read_bytes()
    assert "Escritório Exemplo Ltda".encode("utf-8") in bruto and b"\\u" not in bruto
    texto = bruto.decode("utf-8")
    assert texto.startswith('{\n  "tipo": "contador",\n  "nome": "Fulana de Tal"')
    assert json.loads(texto)["tipo"] == "contador"


def test_salvar_usa_a_pasta_do_ambiente(monkeypatch, tmp_path):
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(tmp_path / "cfg"))
    arquivo, _ = operador.salvar({"tipo": "advogado", "nome": NOME})
    assert arquivo == tmp_path / "cfg" / "operador.json" and operador.ler()["nome"] == NOME


def test_chaves_em_branco_sao_aceitas(tmp_path):
    operador.salvar({"tipo": "advogado", "nome": "", "registro": "", "entidade": "", "cidade": "",
                     "skill_peticao": ""}, tmp_path)
    assert operador.ler(tmp_path)["nome"] == ""


def test_salvar_de_novo_substitui_o_conteudo(tmp_path):
    operador.salvar({"tipo": "advogado", "nome": NOME, "registro": OAB}, tmp_path)
    operador.salvar({"tipo": "contador", "nome": "Beltrano de Tal"}, tmp_path)
    lido = operador.ler(tmp_path)
    assert lido["tipo"] == "contador" and lido["nome"] == "Beltrano de Tal" and "registro" not in lido


def test_salvar_aceita_o_que_ler_devolveu(tmp_path):
    operador.salvar({"tipo": "advogado", "nome": NOME}, tmp_path)
    operador.salvar(operador.ler(tmp_path), tmp_path)             # atualizado_em volta e é reescrito
    assert operador.ler(tmp_path)["nome"] == NOME


def test_chave_desconhecida_e_erro_e_nada_e_gravado(tmp_path):
    with pytest.raises(ValueError, match="cpf"):
        operador.salvar({"tipo": "advogado", "nome": NOME, "cpf": "000.000.000-00"}, tmp_path)
    assert not (tmp_path / "operador.json").exists()


@pytest.mark.parametrize("dados", [{}, {"nome": NOME}, {"tipo": ""}, {"tipo": "juiz"}, {"tipo": None},
                                   {"tipo": "Advogado"}])
def test_tipo_e_obrigatorio_e_so_advogado_ou_contador(tmp_path, dados):
    with pytest.raises(ValueError, match="tipo"):
        operador.salvar(dados, tmp_path)
    assert not (tmp_path / "operador.json").exists()


def test_ler_arquivo_invalido_levanta(tmp_path):
    (tmp_path / "operador.json").write_text("{ não é json", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON válido"):
        operador.ler(tmp_path)
    (tmp_path / "operador.json").write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(ValueError, match="objeto"):
        operador.ler(tmp_path)


def test_ler_aceita_arquivo_com_bom(tmp_path):
    (tmp_path / "operador.json").write_bytes(b"\xef\xbb\xbf" + json.dumps({"tipo": "advogado"}).encode("utf-8"))
    assert operador.ler(tmp_path) == {"tipo": "advogado"}


# ── avisos de registro ────────────────────────────────────────────────

@pytest.mark.parametrize("tipo,registro,avisa", [
    ("advogado", OAB, False), ("advogado", "OAB/UF 12.345", False), ("advogado", "12345", True),
    ("advogado", CRC, True), ("advogado", "oab/uf 00.000", True), ("advogado", "", False),
    ("contador", CRC, False), ("contador", "CRC/UF 123456/O", False), ("contador", OAB, True),
    ("contador", "123456", True), ("contador", "", False)])
def test_aviso_de_registro_fora_do_padrao(tmp_path, tipo, registro, avisa):
    arquivo, avisos = operador.salvar({"tipo": tipo, "registro": registro}, tmp_path)
    assert bool(avisos) is avisa and len(avisos) == int(avisa)
    assert arquivo.is_file()                                       # aviso não impede a gravação
    if avisa:
        prefixo = "OAB/" if tipo == "advogado" else "CRC/"
        assert prefixo in avisos[0] and tipo in avisos[0]


def test_sem_registro_nao_ha_aviso(tmp_path):
    assert operador.salvar({"tipo": "advogado", "nome": NOME}, tmp_path)[1] == []


# ── assinatura e marca ────────────────────────────────────────────────

def test_assinatura_tem_as_quatro_chaves():
    op = {"tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE,
          "skill_peticao": "x", "atualizado_em": "2026-10-26T10:00:00"}
    assert operador.assinatura(op) == {"nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE}
    assert operador.assinatura({"tipo": "contador", "nome": NOME}) == {
        "nome": NOME, "registro": "", "entidade": "", "cidade": ""}
    assert operador.assinatura({}) == {"nome": "", "registro": "", "entidade": "", "cidade": ""}
    assert operador.assinatura({"nome": None})["nome"] == ""


def test_marca_nome_prefere_a_entidade():
    assert operador.marca_nome({"nome": NOME, "entidade": ENTIDADE}) == ENTIDADE
    assert operador.marca_nome({"nome": NOME, "entidade": ""}) == NOME
    assert operador.marca_nome({"nome": NOME}) == NOME
    assert operador.marca_nome({"nome": NOME, "entidade": "   "}) == NOME
    assert operador.marca_nome({}) == "" and operador.marca_nome({"entidade": ENTIDADE}) == ENTIDADE


def test_modulo_sem_identidade_real():
    texto = Path(operador.__file__).read_text(encoding="utf-8")
    import re
    assert not re.search(r"OAB/[A-Z]{2}\s*\d{1,3}\.\d{3}", texto.replace("OAB/UF 00.000", ""))
    assert not re.search(r"CRC/[A-Z]{2}\s*\d{6}", texto.replace("CRC/UF 000000/O", ""))
