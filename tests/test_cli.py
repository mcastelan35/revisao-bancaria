"""Linha de comando `revisao.py`, chamada por subprocesso (como o Claude a chama): cada
subcomando, os códigos de saída (0, 1, 2 e 3) e o preenchimento do operador no `gerar`.

Todo teste que toca o operador passa REVISAO_BANCARIA_CONFIG_DIR apontando para `tmp_path`:
nada escreve na pasta real do usuário."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import PNG_1X1, SKILL
from motores import operador, relatorios

REVISAO = SKILL / "revisao.py"
NOME, ENTIDADE, CIDADE, OAB = "Fulana de Tal", "Escritório Exemplo", "Cidade-UF", "OAB/UF 00.000"


class Resultado:
    def __init__(self, p):
        self.codigo, self.out, self.err = p.returncode, p.stdout, p.stderr

    def json(self):
        return json.loads(self.out)


@pytest.fixture
def cli(tmp_path):
    """Roda `revisao.py` a partir de `tmp_path` (qualquer pasta serve) com a configuração isolada."""
    config = tmp_path / "config-do-operador"

    def rodar(*args, env=None, cwd=None, config_dir=True):
        ambiente = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_PLUGIN_DATA", "PYTHONUTF8")}
        ambiente["PYTHONIOENCODING"] = "cp1252"       # o console do Windows: o CLI tem que se virar
        if config_dir:
            ambiente["REVISAO_BANCARIA_CONFIG_DIR"] = str(config)
        ambiente.update(env or {})
        if args and args[0] == "gerar" and "--pdf" not in args:
            args = (*args, "--pdf", "nao")           # o PDF tem testes próprios (test_pdf.py): aqui, sem navegador
        p = subprocess.run([sys.executable, str(REVISAO), *map(str, args)], capture_output=True, text=True,
                           encoding="utf-8", env=ambiente, cwd=str(cwd or tmp_path), timeout=300)
        return Resultado(p)

    rodar.config = config
    return rodar


def salvar_operador(cli, **extra):
    campos = {"tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE, **extra}
    args = []
    for chave, valor in campos.items():
        args += [f"--{chave.replace('_', '-')}", valor]
    r = cli("operador", "salvar", *args)
    assert r.codigo == 0, r.err
    return r.json()


def escrever_payload(caminho, **mudancas):
    payload = relatorios._payload_demo()
    for chave, valor in mudancas.items():
        if valor is None:
            payload.pop(chave, None)
        else:
            payload[chave] = valor
    caminho.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return caminho


# ── básico ────────────────────────────────────────────────────────────

def test_version(cli):
    r = cli("--version")
    assert r.codigo == 0 and r.out.strip() == "revisao-bancaria 6.0.0"


def test_sem_subcomando_ou_subcomando_desconhecido(cli):
    assert cli().codigo == 2
    assert cli("inexistente").codigo == 2
    assert cli("--help").codigo == 0


def test_funciona_de_qualquer_pasta_e_importa_motores_do_proprio_diretorio(cli, tmp_path):
    (tmp_path / "motores").mkdir()                       # uma pasta "motores" falsa na pasta de trabalho
    (tmp_path / "motores" / "__init__.py").write_text("raise RuntimeError('pasta errada')\n", encoding="utf-8")
    r = cli("marcos", "--data-contrato", "2019-05-02", cwd=tmp_path)
    assert r.codigo == 0, r.err
    assert r.json()["MT04"]["contrato"] == "posterior"


def test_saida_em_utf8_mesmo_com_console_cp1252(cli):
    r = cli("regra", "R15")
    assert r.codigo == 0 and "Juros remuneratórios abusivos — acima de 1,5x a média BACEN" in r.out
    assert "\\u" not in r.out                            # ensure_ascii=False


# ── autoteste ─────────────────────────────────────────────────────────

def test_autoteste_compacto(cli):
    r = cli("autoteste")
    linhas = r.out.splitlines()
    assert r.codigo == 0, r.out + r.err
    assert [l.split()[1] for l in linhas[:-1]] == ["comum", "calculo", "cet", "cartao", "conta_corrente",
                                                    "relatorios", "regras", "jurisprudencia"]
    for linha in linhas[:-1]:
        assert linha.split()[0] in ("OK", "PULADO") and "FALHOU" not in linha
    assert "  OK      calculo          77 passaram" in linhas
    assert linhas[-1].startswith("total: ") and " 0 falharam" in linhas[-1] and "PASS" not in r.out
    if any(l.startswith("  PULADO  relatorios") for l in linhas):
        assert "openpyxl ausente — 13 asserções da planilha puladas (HTML testado)" in r.out
        assert linhas[-1].endswith("13 pulados")
    else:
        assert "  OK      relatorios       110 passaram" in linhas and linhas[-1].endswith("0 pulados")


def test_autoteste_de_um_modulo(cli):
    r = cli("autoteste", "--modulo", "comum")
    assert r.codigo == 0 and r.out.splitlines() == [
        "  OK      comum            17 passaram", "total: 17 passaram · 0 falharam · 0 pulados"]


def test_autoteste_verbose_mostra_as_linhas_pass(cli):
    r = cli("autoteste", "--modulo", "comum", "--verbose")
    assert r.codigo == 0 and "PASS  guard_taxa recusa 7,9" in r.out
    assert "  OK      comum            17 passaram" in r.out and "17 passaram · 0 falharam" in r.out


def test_autoteste_modulo_invalido(cli):
    assert cli("autoteste", "--modulo", "nada").codigo == 2


def test_autoteste_sai_com_1_quando_um_modulo_falha(tmp_path):
    """Falha injetada num processo à parte: a CLI mostra FALHOU e devolve 1."""
    codigo = (
        "import sys; sys.path.insert(0, sys.argv[1]);"
        "import revisao; from motores import comum;"
        "comum.autoteste = lambda verbose=True: {'modulo': 'comum', 'passaram': 16, 'falharam': 1, 'pulados': 0};"
        "sys.exit(revisao.main(['autoteste', '--modulo', 'comum']))")
    p = subprocess.run([sys.executable, "-c", codigo, str(SKILL)], capture_output=True, text=True,
                       encoding="utf-8", timeout=120)
    assert p.returncode == 1
    assert "  FALHOU  comum            16 passaram · 1 falharam" in p.stdout
    assert "total: 16 passaram · 1 falharam · 0 pulados" in p.stdout


# ── regras, regra, sumula, marcos, serie ──────────────────────────────

def test_regras_resumo(cli):
    r = cli("regras", "--tipo", "consumo_pf", "--regime", "consumerista", "--data-contrato", "2019-05-02",
            "--formato", "resumo", "--hoje", "2026-10-26")
    assert r.codigo == 0, r.err
    saida = r.json()
    assert saida["entrada"] == {"tipo": "consumo_pf", "regime": "consumerista", "data_contrato": "2019-05-02",
                                "data_consolidacao": None, "categorias": None}
    assert saida["hoje"] == "2026-10-26" and saida["versao_regras"] == "6.0.0"
    assert [i["id"] for i in saida["aplicaveis"]][:3] == ["R03", "R04", "R06"]
    assert set(saida["aplicaveis"][0]) == {"id", "categoria", "nome", "tier", "status", "conclusiva"}
    assert saida["resumo"]["nao_conclusivas"] == ["R15", "R30", "R31", "R32", "R33"]


def test_regras_padrao_e_o_formato_padrao(cli):
    r = cli("regras", "--tipo", "consumo_pf", "--regime", "civil-empresarial", "--data-contrato", "2017-09-01",
            "--categorias", "juros_remuneratorios, comissao_de_permanencia", "--hoje", "2026-10-26")
    assert r.codigo == 0, r.err
    saida = r.json()
    assert saida["entrada"]["regime"] == "civil_empresarial"
    assert saida["entrada"]["categorias"] == ["juros_remuneratorios", "comissao_de_permanencia"]
    r15 = next(i for i in saida["aplicaveis"] if i["id"] == "R15")
    assert r15["tier"] == "T2" and "consequencia" in r15 and "pendencias" in r15
    assert saida["resumo"]["omitidas_por_categoria"] == 40 - len(saida["aplicaveis"]) - len(saida["nao_aplicaveis"]) \
        - len(saida["confirmar"])


def test_regras_sem_data_manda_para_confirmar(cli):
    saida = cli("regras", "--tipo", "consumo_pf", "--regime", "consumerista", "--formato", "resumo").json()
    assert "data do contrato ausente — corte MT04 (01/09/2017)" in [i["motivo"] for i in saida["confirmar"]]


def test_regras_sfh_com_consolidacao(cli):
    saida = cli("regras", "--tipo", "sfh", "--regime", "consumerista", "--data-contrato", "2010-01-01",
                "--data-consolidacao", "2020-01-01", "--formato", "resumo").json()
    r40 = next(i for i in saida["aplicaveis"] if i["id"] == "R40")
    assert r40["corte"]["leitura"].startswith("só o contrato atende")
    assert {"id": "R15"} .items() <= next(i for i in saida["nao_aplicaveis"] if i["id"] == "R15").items()


@pytest.mark.parametrize("args", [
    ["--tipo", "inexistente", "--regime", "consumerista"],
    ["--tipo", "consumo_pf", "--regime", "outro"],
    ["--tipo", "consumo_pf", "--regime", "consumerista", "--data-contrato", "02/05/2019"],
    ["--tipo", "consumo_pf", "--regime", "consumerista", "--formato", "longo"],
    ["--tipo", "consumo_pf", "--regime", "consumerista", "--hoje", "ontem"]])
def test_regras_erro_de_entrada_sai_com_2(cli, args):
    r = cli("regras", *args)
    assert r.codigo == 2 and r.out == "" and r.err.startswith("erro: ")


def test_regras_exige_tipo_e_regime(cli):
    assert cli("regras", "--tipo", "consumo_pf").codigo == 2
    assert cli("regras", "--regime", "consumerista").codigo == 2


def test_regra_devolve_lista_com_o_texto_integral(cli):
    r = cli("regra", "R15", "R16")
    assert r.codigo == 0
    regras_ = r.json()
    assert [x["id"] for x in regras_] == ["R15", "R16"] and "fundamentacao" in regras_[0] and "regime" in regras_[0]


def test_regra_inexistente_sai_com_2_sem_aspas_de_keyerror(cli):
    r = cli("regra", "R99")
    assert r.codigo == 2 and r.err.strip() == "erro: regra 'R99' não existe (válidas: R01 a R40)"


def test_sumula(cli):
    r = cli("sumula", "530", "541")
    assert r.codigo == 0 and [s["numero"] for s in r.json()] == [530, 541]
    assert "taxa média de mercado" in r.json()[0]["texto"]
    assert cli("sumula", "1").codigo == 2 and cli("sumula", "abc").codigo == 2


def test_marcos(cli):
    r = cli("marcos", "--data-contrato", "2010-01-01", "--data-consolidacao", "2020-01-01")
    assert r.codigo == 0
    marcos = r.json()
    assert marcos["MT10"]["contrato"] == "anterior" and marcos["MT10"]["consolidacao"] == "posterior"
    assert marcos["MT05"]["base"] == "pagamento" and "nota" in marcos["MT05"]
    assert all(m["contrato"] is None for m in cli("marcos").json().values())
    assert cli("marcos", "--data-contrato", "x").codigo == 2


def test_serie(cli):
    todas = cli("serie").json()
    assert len(todas) == 24 and todas[0]["modalidade"] == "credito_pessoal_nao_consignado"
    assert [s["serie"] for s in cli("serie", "--buscar", "cheque especial").json()] == [25463, 25446]
    assert [s["serie"] for s in cli("serie", "--modalidade", "aquisicao_veiculo_pf").json()] == [25471]
    assert cli("serie", "--buscar", "CARTÃO ROTATIVO").json() == []
    assert cli("serie", "--buscar", "veículo").json() != []
    assert cli("serie", "--modalidade", "x", "--buscar", "y").codigo == 2          # exclusivos


# ── razao ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("contratada,media,classificacao,razao", [
    ("2.99", "2.00", "licita", 1.495), ("3.00", "2.00", "zona_cinzenta", 1.5), ("3.99", "2.00", "zona_cinzenta", 1.995),
    ("4.00", "2.00", "ilicita", 2.0), ("0.03", "0.02", "zona_cinzenta", 1.5),
    ("7.05", "4.7", "zona_cinzenta", 1.5), ("14.1", "9.4", "zona_cinzenta", 1.5)])
def test_razao_am_efetiva_exata_nos_limiares(cli, contratada, media, classificacao, razao):
    r = cli("razao", "--contratada-pct", contratada, "--media-pct", media)
    assert r.codigo == 0, r.err
    saida = r.json()
    assert saida["classificacao"] == classificacao and saida["razao"] == pytest.approx(razao, abs=5e-5)
    assert saida["unidade_contratada_informada"] == "am_efetiva" and saida["contratada_informada"] == float(contratada)


def test_razao_saida_completa(cli):
    saida = cli("razao", "--contratada-pct", "4.74", "--media-pct", "3.0").json()
    assert saida == {"razao": 1.58, "razao_txt": "1,58x", "classificacao": "zona_cinzenta",
                     "rotulo": "zona de abusividade", "limiares_am": {"zona_cinzenta": 4.5, "forte": 6.0},
                     "contratada_am": 4.74, "media_am": 3.0, "unidade_contratada_informada": "am_efetiva",
                     "contratada_informada": 4.74}


def test_razao_converte_a_unidade_da_contratada(cli):
    ef = cli("razao", "--contratada-pct", "40.10", "--unidade-contratada", "aa_efetiva", "--media-pct", "2").json()
    nom = cli("razao", "--contratada-pct", "34.20", "--unidade-contratada", "aa_nominal", "--media-pct", "2").json()
    assert ef["contratada_am"] == pytest.approx(2.8497352, abs=1e-6) and ef["unidade_contratada_informada"] == "aa_efetiva"
    assert nom["contratada_am"] == pytest.approx(2.85, abs=1e-9)
    assert ef["classificacao"] == nom["classificacao"] == "licita"


def test_razao_recusa_tipos_habitacionais(cli):
    for tipo in ("sfh", "sfi", "imobiliario_fora_sfi"):
        r = cli("razao", "--contratada-pct", "3", "--media-pct", "2", "--tipo", tipo)
        assert r.codigo == 2 and r.out == ""
        assert r.err.strip() == (f"erro: R15 desligada no tipo {tipo}: a razão contratada/média BACEN não é tese "
                                 "nos tipos habitacionais (regra de conduta 27)")


def test_razao_com_tipo_que_aceita_a_r15(cli):
    for tipo in ("consumo_pf", "empresarial_pj", "cartao_credito", "cedula_rural"):
        assert cli("razao", "--contratada-pct", "3", "--media-pct", "2", "--tipo", tipo).codigo == 0, tipo
    r = cli("razao", "--contratada-pct", "3", "--media-pct", "2", "--tipo", "xyz")
    assert r.codigo == 2 and "tipo de contrato inválido" in r.err


@pytest.mark.parametrize("args", [
    ["--contratada-pct", "3", "--media-pct", "0"], ["--contratada-pct", "3", "--media-pct", "-1"],
    ["--contratada-pct", "-3", "--media-pct", "2"], ["--contratada-pct", "150", "--media-pct", "2"],
    ["--contratada-pct", "3", "--media-pct", "nan"], ["--contratada-pct", "abc", "--media-pct", "2"],
    ["--contratada-pct", "3"], ["--media-pct", "2"],
    ["--contratada-pct", "3", "--media-pct", "2", "--unidade-contratada", "mensal"]])
def test_razao_entrada_invalida_sai_com_2(cli, args):
    assert cli("razao", *args).codigo == 2


# ── comparar ──────────────────────────────────────────────────────────

def test_comparar_price(cli):
    r = cli("comparar", "--sistema", "price", "--pv", "50000", "--n", "48", "--taxa-contratada-pct", "2.99",
            "--taxa-revisada-pct", "1.85")
    assert r.codigo == 0, r.err
    saida = r.json()
    assert list(saida) == ["sistema", "pv", "n", "taxa_contratada_am", "taxa_revisada_am",
                           "prestacao_contratada_primeira", "prestacao_revisada_primeira",
                           "prestacao_contratada_ultima", "prestacao_revisada_ultima", "total_pago_contratado",
                           "total_pago_revisado", "total_juros_contratado", "total_juros_revisado",
                           "excesso_total", "favoravel", "nota", "plotar", "saldos_coincidem"]
    assert saida["sistema"] == "price" and saida["pv"] == 50000.0 and saida["n"] == 48
    assert saida["taxa_contratada_am"] == pytest.approx(0.0299) and saida["taxa_revisada_am"] == pytest.approx(0.0185)
    assert saida["prestacao_contratada_primeira"] == 1975.24 and saida["prestacao_revisada_primeira"] == 1580.74
    assert saida["total_pago_contratado"] - saida["total_pago_revisado"] == pytest.approx(saida["excesso_total"], abs=0.02)
    assert saida["total_juros_contratado"] == pytest.approx(saida["total_pago_contratado"] - 50000, abs=0.02)
    assert saida["favoravel"] is True and saida["nota"] is None
    assert saida["plotar"] == "saldo" and saida["saldos_coincidem"] is False and "linhas" not in saida


def test_comparar_sac_com_tabela(cli):
    r = cli("comparar", "--sistema", "sac", "--pv", "3000", "--n", "3", "--taxa-contratada-pct", "3",
            "--taxa-revisada-pct", "1", "--tabela")
    saida = r.json()
    assert r.codigo == 0 and saida["plotar"] == "prestacao" and saida["saldos_coincidem"] is True
    assert saida["excesso_total"] == 120.0 and saida["prestacao_contratada_ultima"] == 1030.0
    assert [l["n"] for l in saida["linhas"]] == [1, 2, 3]
    assert saida["linhas"][0] == {"n": 1, "prestacao_contratada": 1090.0, "prestacao_revisada": 1030.0,
                                  "excesso": 60.0, "saldo_contratado": 3000.0, "saldo_revisado": 3000.0,
                                  "divergencia_saldo": 0.0}


def test_comparar_tabela_arredonda_a_2_casas_so_na_saida(cli):
    saida = cli("comparar", "--sistema", "price", "--pv", "1000", "--n", "5", "--taxa-contratada-pct", "2.99",
                "--taxa-revisada-pct", "1.85", "--tabela").json()
    assert [l["n"] for l in saida["linhas"]] == [1, 2, 3, 4, 5]
    for linha in saida["linhas"]:
        for chave, valor in linha.items():
            if chave != "n":
                assert round(valor, 2) == valor, (chave, valor)
    # a taxa não é monetária: sai inteira, sem arredondar
    assert saida["taxa_contratada_am"] == 2.99 / 100.0


def test_comparar_unidade_anual(cli):
    nominal = cli("comparar", "--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "36",
                  "--taxa-revisada-pct", "12", "--unidade", "aa_nominal").json()
    assert nominal["taxa_contratada_am"] == pytest.approx(0.03) and nominal["taxa_revisada_am"] == pytest.approx(0.01)
    efetiva = cli("comparar", "--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "36",
                  "--taxa-revisada-pct", "12", "--unidade", "aa_efetiva").json()
    assert efetiva["taxa_contratada_am"] == pytest.approx(1.36 ** (1 / 12) - 1)


def test_comparar_revisado_mais_caro_sai_sinalizado(cli):
    saida = cli("comparar", "--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "1",
                "--taxa-revisada-pct", "2").json()
    assert saida["favoravel"] is False and saida["excesso_total"] < 0
    assert saida["nota"] == "cenário revisado é mais caro que o contratado — reportar em ressalvas, não esconder"


@pytest.mark.parametrize("args", [
    ["--sistema", "price", "--pv", "1000", "--n", "0", "--taxa-contratada-pct", "1", "--taxa-revisada-pct", "2"],
    ["--sistema", "price", "--pv", "0", "--n", "12", "--taxa-contratada-pct", "1", "--taxa-revisada-pct", "2"],
    ["--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "-1", "--taxa-revisada-pct", "2"],
    ["--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "150", "--taxa-revisada-pct", "2"],
    ["--sistema", "tabelado", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "1", "--taxa-revisada-pct", "2"],
    ["--sistema", "price", "--pv", "1000", "--n", "12", "--taxa-contratada-pct", "1"]])
def test_comparar_entrada_invalida_sai_com_2(cli, args):
    assert cli("comparar", *args).codigo == 2


# ── operador ──────────────────────────────────────────────────────────

def test_operador_mostrar_sem_configuracao_sai_com_3(cli):
    r = cli("operador", "mostrar")
    assert r.codigo == 3
    assert r.json() == {"pasta": str(cli.config), "operador": None}


def test_operador_salvar_e_mostrar(cli):
    salvo = salvar_operador(cli, skill_peticao="peticoes-exemplo")
    assert salvo["arquivo"] == str(cli.config / "operador.json") and salvo["avisos"] == []
    assert {k: v for k, v in salvo["operador"].items() if k != "atualizado_em"} == {
        "tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE,
        "skill_peticao": "peticoes-exemplo"}
    r = cli("operador", "mostrar")
    assert r.codigo == 0 and r.json()["operador"] == salvo["operador"] and r.json()["pasta"] == str(cli.config)
    assert (cli.config / "operador.json").is_file()


def test_operador_salvar_so_o_que_foi_passado(cli):
    r = cli("operador", "salvar", "--tipo", "contador", "--nome", NOME)
    assert r.codigo == 0
    assert set(r.json()["operador"]) == {"tipo", "nome", "atualizado_em"}


def test_operador_salvar_avisa_registro_fora_do_padrao(cli):
    r = cli("operador", "salvar", "--tipo", "contador", "--nome", NOME, "--registro", OAB)
    assert r.codigo == 0 and len(r.json()["avisos"]) == 1 and "CRC/" in r.json()["avisos"][0]


@pytest.mark.parametrize("args", [["--tipo", "juiz"], [], ["--nome", NOME]])
def test_operador_salvar_exige_tipo_valido(cli, args):
    assert cli("operador", "salvar", *args).codigo == 2
    assert not (cli.config / "operador.json").exists()


def test_operador_config_dir_vence_a_variavel_de_ambiente(cli, tmp_path):
    outra = tmp_path / "outra"
    r = cli("operador", "salvar", "--tipo", "advogado", "--nome", NOME, "--config-dir", outra)
    assert r.codigo == 0 and (outra / "operador.json").is_file() and not (cli.config / "operador.json").exists()
    assert cli("operador", "mostrar", "--config-dir", outra).json()["operador"]["nome"] == NOME
    assert cli("operador", "mostrar").codigo == 3


def test_operador_variavel_literal_do_plugin_e_ignorada(cli, tmp_path):
    """`${CLAUDE_PLUGIN_DATA}` que o ambiente não substituiu não pode virar uma pasta chamada assim."""
    r = cli("operador", "mostrar", "--config-dir", "${CLAUDE_PLUGIN_DATA}", config_dir=False,
            env={"REVISAO_BANCARIA_CONFIG_DIR": str(tmp_path / "valida")})
    assert r.json()["pasta"] == str(tmp_path / "valida")
    assert not (tmp_path / "${CLAUDE_PLUGIN_DATA}").exists()


def test_operador_json_corrompido_sai_com_2(cli):
    cli.config.mkdir(parents=True)
    (cli.config / "operador.json").write_text("{ quebrado", encoding="utf-8")
    r = cli("operador", "mostrar")
    assert r.codigo == 2 and "JSON válido" in r.err


# ── gerar ─────────────────────────────────────────────────────────────

def test_gerar_preenche_marca_e_assinatura_a_partir_do_operador(cli, tmp_path):
    salvar_operador(cli)
    payload = escrever_payload(tmp_path / "payload.json", assinatura=None, marca={})
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 0, r.err
    saida = r.json()
    assert saida["operador_aplicado"] is True
    nomes = sorted(os.path.basename(a) for a in saida["arquivos"])
    assert nomes == ["INTERNO-agenda-pesquisa-demo.md", "laudo-premium-demo.html"]
    html = (tmp_path / "saida" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert ENTIDADE in html and NOME in html and OAB in html and CIDADE in html


def test_gerar_marca_usa_o_nome_quando_nao_ha_entidade(cli, tmp_path):
    r = cli("operador", "salvar", "--tipo", "contador", "--nome", NOME, "--registro", "CRC/UF 000000/O")
    assert r.codigo == 0
    payload = escrever_payload(tmp_path / "payload.json", assinatura=None, marca=None)
    assert cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium").json()["operador_aplicado"]
    html = (tmp_path / "saida" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert NOME in html and "CRC/UF 000000/O" in html


def test_gerar_o_que_vem_no_payload_prevalece(cli, tmp_path):
    salvar_operador(cli, nome="Operador Gravado", entidade="Entidade Gravada")
    payload = escrever_payload(tmp_path / "payload.json")          # o demo já traz marca e assinatura
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 0 and r.json()["operador_aplicado"] is False
    html = (tmp_path / "saida" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert "Nome do Responsável" in html and "Operador Gravado" not in html and "Entidade Gravada" not in html


def test_gerar_preenche_so_o_que_falta(cli, tmp_path):
    salvar_operador(cli)
    payload = escrever_payload(tmp_path / "payload.json", assinatura=None)       # marca do payload fica
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.json()["operador_aplicado"] is True
    html = (tmp_path / "saida" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert NOME in html and OAB in html


def test_gerar_marca_sem_nome_e_preenchida_sem_perder_o_resto(cli, tmp_path):
    salvar_operador(cli)
    payload = escrever_payload(tmp_path / "payload.json", marca={"nome": "", "logo": "x.png"})
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 0 and r.json()["operador_aplicado"] is True


def test_gerar_monta_o_payload_do_renderizador(tmp_path, monkeypatch, capsys):
    """Em processo, com o renderizador trocado por um espião: o que `gerar` entrega a ele."""
    import revisao
    config = tmp_path / "cfg"
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(config))
    operador.salvar({"tipo": "advogado", "nome": NOME, "registro": OAB, "entidade": ENTIDADE,
                     "cidade": CIDADE, "skill_peticao": "x"}, config)
    recebido = {}

    def espiao(payload, saida, slug=None, formatos=None, tema=None):
        recebido.update(payload=payload, saida=saida, formatos=formatos, tema=tema)
        return [saida / "a.html"]

    monkeypatch.setattr(revisao.relatorios, "gerar", espiao)
    sem_nada = escrever_payload(tmp_path / "p1.json", assinatura=None, marca={"logo": "x.png"})
    assert revisao.main(["gerar", str(sem_nada), "--saida", str(tmp_path / "s"), "--formatos", "premium, planilha",
                         "--pdf", "nao"]) == 0
    assert recebido["payload"]["marca"] == {"logo": "x.png", "nome": ENTIDADE}
    assert recebido["payload"]["assinatura"] == {"nome": NOME, "registro": OAB, "entidade": ENTIDADE, "cidade": CIDADE}
    assert recebido["formatos"] == {"premium", "planilha"} and recebido["saida"] == tmp_path / "s"
    assert recebido["tema"] is None                                  # sem tema.json, o visual padrão
    assert json.loads(capsys.readouterr().out) == {
        "arquivos": [str(tmp_path / "s" / "a.html")], "operador_aplicado": True, "tema": "padrao",
        "pdf": {"gerado": False, "motivo": "desligado por --pdf nao"}}

    completo = escrever_payload(tmp_path / "p2.json")
    assert revisao.main(["gerar", str(completo), "--saida", str(tmp_path / "s"), "--pdf", "nao"]) == 0
    assert recebido["payload"]["marca"] == {"nome": "Escritório Exemplo"} and recebido["formatos"] is None
    assert recebido["payload"]["assinatura"]["nome"] == "Nome do Responsável"
    assert json.loads(capsys.readouterr().out)["operador_aplicado"] is False


def test_gerar_sem_operador_e_sem_identidade_dica_a_configuracao(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json", assinatura=None, marca={})
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 2 and r.out == ""
    assert "payload incompleto" in r.err and "assinatura" in r.err and "marca.nome" in r.err
    assert "configure o operador: revisao.py operador salvar --tipo" in r.err
    assert not (tmp_path / "saida").exists()                       # nada foi escrito


def test_gerar_sem_operador_mas_com_identidade_no_payload_funciona(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json")
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 0 and r.json()["operador_aplicado"] is False


def test_gerar_sem_a_dica_quando_o_erro_nao_e_de_identidade(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json", achados=None)
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium")
    assert r.codigo == 2 and "achados" in r.err and "configure o operador" not in r.err


def test_gerar_todos_os_formatos_e_formatos_escolhidos(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json")
    r = cli("gerar", payload, "--saida", tmp_path / "html", "--formatos", "premium,panorama")
    assert r.codigo == 0
    assert sorted(os.path.basename(a) for a in r.json()["arquivos"]) == [
        "INTERNO-agenda-pesquisa-demo.md", "laudo-premium-demo.html", "panorama-estrategico-demo.html"]
    pytest.importorskip("openpyxl")
    r = cli("gerar", payload, "--saida", tmp_path / "tudo")
    assert r.codigo == 0 and sorted(os.path.basename(a) for a in r.json()["arquivos"])[-1] == "planilha-demo.xlsx"
    assert len(r.json()["arquivos"]) == 4


def test_gerar_planilha_sem_openpyxl_recusa_antes_de_escrever(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json")
    bloqueio = tmp_path / "bloqueio"
    bloqueio.mkdir()
    (bloqueio / "sitecustomize.py").write_text("import sys; sys.modules['openpyxl'] = None\n", encoding="utf-8")
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium,planilha",
            env={"PYTHONPATH": str(bloqueio)})
    assert r.codigo == 2 and "openpyxl não está instalado" in r.err
    assert not (tmp_path / "saida").exists() or not list((tmp_path / "saida").iterdir())


def test_gerar_formato_desconhecido_sai_com_2_sem_escrever(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json")
    r = cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium,pdf")
    assert r.codigo == 2 and "pdf" in r.err and "premium, panorama, planilha" in r.err
    assert not (tmp_path / "saida").exists()


def test_gerar_payload_ilegivel_sai_com_2(cli, tmp_path):
    assert cli("gerar", tmp_path / "nao-existe.json", "--saida", tmp_path / "s").codigo == 2
    ruim = tmp_path / "ruim.json"
    ruim.write_text("{ quebrado", encoding="utf-8")
    r = cli("gerar", ruim, "--saida", tmp_path / "s")
    assert r.codigo == 2 and "JSON" in r.err
    lista = tmp_path / "lista.json"
    lista.write_text("[1]", encoding="utf-8")
    assert cli("gerar", lista, "--saida", tmp_path / "s").codigo == 2
    assert cli("gerar", ruim).codigo == 2                          # --saida é obrigatório


def test_gerar_aceita_payload_com_bom(cli, tmp_path):
    salvar_operador(cli)
    payload = escrever_payload(tmp_path / "payload.json", assinatura=None, marca={})
    payload.write_bytes(b"\xef\xbb\xbf" + payload.read_bytes())
    assert cli("gerar", payload, "--saida", tmp_path / "saida", "--formatos", "premium").codigo == 0


# ── skill_layout, tema e o JSON do gerar ──────────────────────────────

def escrever_tema(caminho, **mudancas):
    tema = {"nome": "Identidade do escritório", "skill_origem": "skill-de-layout-exemplo",
            "cores": {"tinta": "#12263F", "destaque": "#0A5C8A", "destaque_claro": "#BCE0F5",
                      "fundo_destaque": "#EEF6FB"},
            "fontes": {"titulo": "Playfair Display", "texto": "Lato"},
            "fontes_url": "https://fonts.googleapis.com/css2?family=Playfair+Display&family=Lato&display=swap",
            "cabecalho_linha": "Rua Exemplo, 100 — Cidade-UF", "rodape": "Uso restrito do escritório"}
    for chave, valor in mudancas.items():
        if valor is None:
            tema.pop(chave, None)
        else:
            tema[chave] = valor
    caminho.write_text(json.dumps(tema, ensure_ascii=False), encoding="utf-8")
    return caminho


def test_operador_salvar_registra_a_skill_de_layout(cli):
    salvo = salvar_operador(cli, skill_layout="skill-de-layout-exemplo")
    assert salvo["operador"]["skill_layout"] == "skill-de-layout-exemplo"
    assert cli("operador", "mostrar").json()["operador"]["skill_layout"] == "skill-de-layout-exemplo"
    assert "skill_layout" not in cli("operador", "salvar", "--tipo", "advogado").json()["operador"]


def test_tema_mostrar_sem_tema_usa_o_padrao_e_sai_com_0(cli):
    r = cli("tema", "mostrar")
    assert r.codigo == 0 and r.json() == {"pasta": str(cli.config), "tema": None, "em_uso": "padrao", "avisos": []}


def test_tema_salvar_mostrar_e_remover(cli, tmp_path):
    r = cli("tema", "salvar", "--arquivo", escrever_tema(tmp_path / "tema.json"))
    assert r.codigo == 0, r.err
    saida = r.json()
    assert saida["pasta"] == str(cli.config) and saida["arquivo"] == str(cli.config / "tema.json")
    assert saida["avisos"] == [] and saida["tema"]["cores"]["destaque"] == "#0A5C8A"
    assert saida["tema"]["fontes"] == {"titulo": "Playfair Display", "texto": "Lato", "mono": "JetBrains Mono"}
    mostrar = cli("tema", "mostrar").json()
    assert mostrar["em_uso"] == "Identidade do escritório" and mostrar["tema"] == saida["tema"]
    r = cli("tema", "remover")
    assert r.codigo == 0 and r.json() == {"pasta": str(cli.config), "removido": True}
    assert not (cli.config / "tema.json").exists() and cli("tema", "mostrar").json()["em_uso"] == "padrao"
    assert cli("tema", "remover").json()["removido"] is False


def test_tema_salvar_avisa_fonte_sem_link(cli, tmp_path):
    r = cli("tema", "salvar", "--arquivo", escrever_tema(tmp_path / "t.json", fontes_url=None))
    assert r.codigo == 0 and len(r.json()["avisos"]) == 1 and "fontes_url" in r.json()["avisos"][0]


def test_tema_salvar_logo_relativo_ao_arquivo_vira_copia_na_pasta(cli, tmp_path):
    (tmp_path / "layout").mkdir()
    (tmp_path / "layout" / "marca.png").write_bytes(PNG_1X1)
    arquivo = escrever_tema(tmp_path / "layout" / "tema.json", logo="marca.png")
    r = cli("tema", "salvar", "--arquivo", arquivo, cwd=tmp_path)         # cwd diferente da pasta do arquivo
    assert r.codigo == 0, r.err
    assert (cli.config / "tema-logo.png").read_bytes() == PNG_1X1
    assert json.loads((cli.config / "tema.json").read_text(encoding="utf-8"))["logo"] == "tema-logo.png"
    assert r.json()["tema"]["logo"] == str(cli.config / "tema-logo.png")
    assert cli("tema", "remover").json()["removido"] is True and not (cli.config / "tema-logo.png").exists()


@pytest.mark.parametrize("mudanca,trecho", [
    ({"cores": {"tinta": "preto"}}, "cores.tinta"),
    ({"cor": "x"}, "chave desconhecida no tema: cor"),
    ({"logo": "nao-existe.png"}, "logo não encontrado"),
    ({"fontes_url": "https://exemplo.com/css2?family=X"}, "fontes_url")])
def test_tema_salvar_invalido_sai_com_2_e_nao_grava(cli, tmp_path, mudanca, trecho):
    r = cli("tema", "salvar", "--arquivo", escrever_tema(tmp_path / "t.json", **mudanca))
    assert r.codigo == 2 and r.out == "" and r.err.startswith("erro: ") and trecho in r.err
    assert not cli.config.exists()


def test_tema_salvar_arquivo_ilegivel_ou_sem_argumento_sai_com_2(cli, tmp_path):
    assert cli("tema", "salvar", "--arquivo", tmp_path / "nao-existe.json").codigo == 2
    ruim = tmp_path / "ruim.json"
    ruim.write_text("{ quebrado", encoding="utf-8")
    r = cli("tema", "salvar", "--arquivo", ruim)
    assert r.codigo == 2 and "JSON" in r.err
    assert cli("tema", "salvar").codigo == 2 and cli("tema").codigo == 2


def test_tema_config_dir_vence_a_variavel_de_ambiente(cli, tmp_path):
    outra = tmp_path / "outra"
    assert cli("tema", "salvar", "--arquivo", escrever_tema(tmp_path / "t.json"), "--config-dir", outra).codigo == 0
    assert (outra / "tema.json").is_file() and not (cli.config / "tema.json").exists()
    assert cli("tema", "mostrar").json()["em_uso"] == "padrao"
    assert cli("tema", "mostrar", "--config-dir", outra).json()["em_uso"] == "Identidade do escritório"


def test_tema_fica_na_mesma_pasta_do_operador(cli, tmp_path):
    salvar_operador(cli)
    cli("tema", "salvar", "--arquivo", escrever_tema(tmp_path / "t.json"))
    assert sorted(p.name for p in cli.config.iterdir()) == ["operador.json", "tema.json"]


def test_gerar_usa_o_tema_gravado_e_informa_o_nome(cli, tmp_path):
    payload = escrever_payload(tmp_path / "payload.json")
    padrao = cli("gerar", payload, "--saida", tmp_path / "a", "--formatos", "premium")
    assert padrao.json()["tema"] == "padrao"
    assert padrao.json()["pdf"] == {"gerado": False, "motivo": "desligado por --pdf nao"}
    html_padrao = (tmp_path / "a" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert "--gold:#B08A4E" in html_padrao and "Documento confidencial" in html_padrao

    (tmp_path / "layout").mkdir()
    (tmp_path / "layout" / "marca.png").write_bytes(PNG_1X1)
    arquivo = escrever_tema(tmp_path / "layout" / "tema.json", logo="marca.png")
    assert cli("tema", "salvar", "--arquivo", arquivo).codigo == 0
    com = cli("gerar", payload, "--saida", tmp_path / "b", "--formatos", "premium,panorama")
    assert com.codigo == 0 and com.json()["tema"] == "Identidade do escritório"
    for nome in ("laudo-premium-demo.html", "panorama-estrategico-demo.html"):
        html = (tmp_path / "b" / nome).read_text(encoding="utf-8")
        assert "--gold:#0A5C8A" in html and "Uso restrito do escritório" in html and "'Playfair Display'" in html
        assert 'src="data:image/png;base64,' in html and "Documento confidencial" not in html

    sem = cli("gerar", payload, "--saida", tmp_path / "c", "--formatos", "premium", "--sem-tema")
    assert sem.json()["tema"] == "padrao"
    assert (tmp_path / "c" / "laudo-premium-demo.html").read_text(encoding="utf-8") == html_padrao


def test_gerar_com_tema_quebrado_recusa_dizendo_como_sair_e_sem_tema_contorna(cli, tmp_path):
    (tmp_path / "layout").mkdir()
    (tmp_path / "layout" / "marca.png").write_bytes(PNG_1X1)
    arquivo = escrever_tema(tmp_path / "layout" / "tema.json", logo="marca.png")
    assert cli("tema", "salvar", "--arquivo", arquivo).codigo == 0
    (cli.config / "tema-logo.png").unlink()                                # o logo copiado sumiu
    payload = escrever_payload(tmp_path / "payload.json")
    r = cli("gerar", payload, "--saida", tmp_path / "s", "--formatos", "premium")
    assert r.codigo == 2 and r.out == "" and "logo não encontrado" in r.err
    assert "tema salvar" in r.err and "tema remover" in r.err and "--sem-tema" in r.err
    assert not (tmp_path / "s").exists()                                   # nada foi escrito
    assert cli("gerar", payload, "--saida", tmp_path / "s", "--formatos", "premium", "--sem-tema").codigo == 0
    (cli.config / "tema.json").write_text("{ quebrado", encoding="utf-8")
    r = cli("gerar", payload, "--saida", tmp_path / "s2", "--formatos", "premium")
    assert r.codigo == 2 and "JSON válido" in r.err and "--sem-tema" in r.err
    assert cli("gerar", payload, "--saida", tmp_path / "s2", "--formatos", "premium", "--sem-tema").codigo == 0


def test_gerar_ramo_conta_pela_linha_de_comando(cli, tmp_path):
    payload = tmp_path / "conta.json"
    payload.write_text(json.dumps(relatorios._payload_demo_conta(), ensure_ascii=False), encoding="utf-8")
    r = cli("gerar", payload, "--saida", tmp_path / "s", "--formatos", "premium,panorama")
    assert r.codigo == 0, r.err
    assert sorted(os.path.basename(a) for a in r.json()["arquivos"]) == [
        "INTERNO-agenda-pesquisa-demo-conta.md", "laudo-premium-demo-conta.html",
        "panorama-estrategico-demo-conta.html"]
    html = (tmp_path / "s" / "laudo-premium-demo-conta.html").read_text(encoding="utf-8")
    assert "3 — Reconciliação do extrato e recomposição da conta" in html
    assert "Os valores apurados na conta corrente formam uma faixa entre cenários de recomposição" in html


def test_gerar_conta_com_extracao_nao_reconciliada_e_recusado_com_2(cli, tmp_path):
    ruim = relatorios._payload_demo_conta()
    ruim["conta"]["reconciliacao"]["veredito"] = "DIVERGENTE"
    payload = tmp_path / "conta.json"
    payload.write_text(json.dumps(ruim, ensure_ascii=False), encoding="utf-8")
    r = cli("gerar", payload, "--saida", tmp_path / "s")
    assert r.codigo == 2 and r.out == "" and "DIVERGENTE" in r.err and "lacuna bloqueante" in r.err
    assert not (tmp_path / "s").exists()


# ── jurisprudência e espelho ─────────────────────────────────────────

def test_jurisprudencia_validar_e_cobertura(cli):
    r = cli("jurisprudencia", "validar")
    assert r.codigo == 0, r.out + r.err
    assert r.json()["erros"] == []
    c = cli("jurisprudencia", "cobertura").json()
    assert {l["id"] for l in c["regras"]} >= {"R01", "R40"}


def test_jurisprudencia_consultar_recusa_lista_vazia(cli):
    r = cli("jurisprudencia", "consultar", "--regras", " , ")
    assert r.codigo == 2 and "ao menos uma regra" in r.err


def test_espelho_formato_neutro_e_skill_canonica(cli, tmp_path):
    achados = relatorios._payload_demo()["achados"]
    for a in achados:
        a["regras"] = ["R04"]
    payload = escrever_payload(tmp_path / "p.json", achados=achados)
    r = cli("espelho", payload, "--saida", tmp_path / "saida")
    assert r.codigo == 0, r.err
    saida = r.json()
    texto = Path(saida["arquivo"]).read_text(encoding="utf-8")
    assert Path(saida["arquivo"]).name.startswith("espelho-peticao-")
    assert "neutro" in texto and saida["skill_peticao"] is None
    salvar_operador(cli, skill_peticao="peticoes-escritorio")
    texto = Path(cli("espelho", payload, "--saida", tmp_path / "saida").json()["arquivo"]).read_text(encoding="utf-8")
    assert "`peticoes-escritorio`" in texto


def test_espelho_recusa_payload_sem_achados(cli, tmp_path):
    payload = escrever_payload(tmp_path / "p.json", achados=None)
    r = cli("espelho", payload, "--saida", tmp_path / "saida")
    assert r.codigo == 2 and "achados" in r.err
