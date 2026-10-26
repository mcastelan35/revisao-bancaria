"""Motor de regras (`motores/regras.py`): corte temporal, grupos, regras desligadas, regime,
`regime_por_marco`, pendências, filtro de categorias, formatos, razão e integridade do JSON.

As datas dos marcos são fixadas aqui, à mão, como gabarito independente do JSON: se alguém mudar
um marco por engano, estes testes acusam."""
import copy
import json
from datetime import date, datetime, timedelta
from itertools import product

import pytest

from motores import regras
from motores.regras import avaliar

DADOS = regras.carregar_dados()
HOJE = "2026-10-26"
TIPOS = [t["id"] for t in DADOS["tipos_contrato"]["tipos"]]
REGIMES = ("consumerista", "civil_empresarial")
TOTAL = len(DADOS["regras"])

# Marcos legais (gabarito): id → data
MARCOS = {"MT01": "2000-03-31", "MT02": "2008-04-30", "MT03": "2011-02-25", "MT04": "2017-09-01",
          "MT05": "2021-03-30", "MT06": "2024-01-03", "MT07": "1991-03-11", "MT08": "1990-12-05",
          "MT09": "1997-11-20", "MT10": "2017-07-11"}


def dia(iso, deslocamento=0):
    return (date.fromisoformat(iso) + timedelta(days=deslocamento)).isoformat()


def rodar(tipo="consumo_pf", regime="consumerista", contrato="2019-05-02", **kw):
    kw.setdefault("hoje", HOJE)
    return avaliar(tipo, regime, contrato, **kw)


def achar(saida, rid):
    """('aplicaveis' | 'confirmar' | 'nao_aplicaveis', item) — ou (None, None)."""
    for lista in ("aplicaveis", "confirmar", "nao_aplicaveis"):
        for item in saida[lista]:
            if item["id"] == rid:
                return lista, item
    return None, None


def destino(saida, rid):
    return achar(saida, rid)[0]


def adulterar(mutacao):
    copia = copy.deepcopy(DADOS)
    mutacao(copia)
    return copia


# ── integridade do JSON ───────────────────────────────────────────────

def test_json_real_e_integro():
    assert regras.validar_dados() == []
    assert regras.validar_dados(DADOS) == []


def test_marcos_do_json_batem_com_o_gabarito_legal():
    assert {m["id"]: m["data"] for m in DADOS["marcos_temporais"]["marcos"]} == MARCOS


def _tipo(copia, tid):
    return next(t for t in copia["tipos_contrato"]["tipos"] if t["id"] == tid)


ADULTERACOES = [
    ("grupo todos com tipo a mais", lambda d: d["tipos_contrato"]["grupos"]["todos"].append("novo"), "grupos.todos"),
    ("grupo todos_sfn sem derivar", lambda d: d["tipos_contrato"]["grupos"]["todos_sfn"].append("imobiliario_fora_sfi"),
     "grupos.todos_sfn"),
    ("grupo todos_sem_lei_especifica incompleto",
     lambda d: d["tipos_contrato"]["grupos"]["todos_sem_lei_especifica"].pop(), "grupos.todos_sem_lei_especifica"),
    ("tipo muda credor_sfn e o grupo não acompanha",
     lambda d: _tipo(d, "sfh").__setitem__("credor_sfn", False), "grupos.todos_sfn"),
    ("tag que não é tipo nem grupo", lambda d: d["regras"][0]["tipo_contrato"].append("pj"), "'pj'"),
    ("marco inexistente no corte", lambda d: d["regras"][0]["corte_temporal"].__setitem__("marco", "MT99"), "MT99"),
    ("posição inválida", lambda d: d["regras"][0]["corte_temporal"].__setitem__("posicao", "depois"), "depois"),
    ("marco sem posição", lambda d: d["regras"][0]["corte_temporal"].__setitem__("posicao", None), "R01"),
    ("base de marco inválida", lambda d: d["marcos_temporais"]["marcos"][0].__setitem__("base", "pagamentos"),
     "pagamentos"),
    ("regras_afetadas sobrando", lambda d: d["marcos_temporais"]["marcos"][0]["regras_afetadas"].append("R01"),
     "MT01.regras_afetadas"),
    ("regras_afetadas faltando", lambda d: d["marcos_temporais"]["marcos"][3]["regras_afetadas"].remove("R03"),
     "MT04.regras_afetadas"),
    ("regras_afetadas de marco sem regra", lambda d: d["marcos_temporais"]["marcos"][6]["regras_afetadas"].append("R01"),
     "MT07.regras_afetadas"),
    ("regime_por_marco cita marco inexistente",
     lambda d: d["regras"][2]["regime_por_marco"].__setitem__("anterior_a_MT98", {}), "MT98"),
    ("regras_desligadas cita regra inexistente",
     lambda d: _tipo(d, "sfh")["regras_desligadas"].append("R99"), "regras_desligadas"),
    ("regras_sem_cdc cita regra inexistente",
     lambda d: _tipo(d, "empresarial_pj")["regras_sem_cdc"].append("R98"), "regras_sem_cdc"),
    ("regras_especificas cita regra inexistente",
     lambda d: _tipo(d, "sfi")["regras_especificas"].append("R97"), "regras_especificas"),
    ("pendência cita regra inexistente",
     lambda d: d["pendencias_jurisprudenciais"]["temas"][0]["regras_afetadas"].append("R96"), "R96"),
    ("id de regra duplicado", lambda d: d["regras"][1].__setitem__("id", "R01"), "duplicado: R01"),
    ("id de tipo duplicado", lambda d: d["tipos_contrato"]["tipos"][1].__setitem__("id", "consumo_pf"),
     "duplicado: consumo_pf"),
]


@pytest.mark.parametrize("nome,mutacao,trecho", ADULTERACOES, ids=[a[0] for a in ADULTERACOES])
def test_validar_dados_acusa_json_adulterado(nome, mutacao, trecho):
    problemas = regras.validar_dados(adulterar(mutacao))
    assert problemas, nome
    assert any(trecho in p for p in problemas), problemas


def test_validar_dados_nao_altera_o_json_em_cache():
    antes = json.dumps(DADOS, sort_keys=True)
    regras.validar_dados(adulterar(lambda d: d["regras"].pop()))
    assert json.dumps(regras.carregar_dados(), sort_keys=True) == antes


# ── datas, relação e posição ──────────────────────────────────────────

@pytest.mark.parametrize("data,esperado", [("2017-08-31", "anterior"), ("2017-09-01", "igual"),
                                           ("2017-09-02", "posterior")])
def test_relacao_na_fronteira(data, esperado):
    assert regras.relacao(data, "2017-09-01") == esperado
    assert regras.relacao(date.fromisoformat(data), date(2017, 9, 1)) == esperado


@pytest.mark.parametrize("posicao,anterior,igual,posterior", [
    ("anterior", True, False, False), ("anterior_ou_igual", True, True, False),
    ("posterior", False, False, True)])
def test_posicao_atende(posicao, anterior, igual, posterior):
    assert [regras.posicao_atende(posicao, r) for r in ("anterior", "igual", "posterior")] == [
        anterior, igual, posterior]


def test_posicao_desconhecida_levanta():
    with pytest.raises(ValueError, match="posição inválida"):
        regras.posicao_atende("depois", "igual")


def test_data_invalida_levanta():
    with pytest.raises(ValueError, match="AAAA-MM-DD"):
        rodar(contrato="02/05/2019")
    with pytest.raises(ValueError):
        regras.relacao("2017-09-01", None)


def test_datas_como_date_texto_ou_datetime_dao_o_mesmo():
    texto = rodar("sfh", contrato="2010-01-01", data_consolidacao="2020-01-01")
    assert rodar("sfh", contrato=date(2010, 1, 1), data_consolidacao=date(2020, 1, 1)) == texto
    assert rodar("sfh", contrato=datetime(2010, 1, 1, 15, 30), data_consolidacao=datetime(2020, 1, 1)) == texto
    assert texto["entrada"]["data_contrato"] == "2010-01-01" and texto["entrada"]["data_consolidacao"] == "2020-01-01"


@pytest.mark.parametrize("vazia", ["", "   ", None])
def test_data_vazia_e_data_ausente(vazia):
    assert rodar(contrato=vazia) == rodar(contrato=None)
    assert rodar("sfh", contrato="2010-01-01", data_consolidacao=vazia)["entrada"]["data_consolidacao"] is None


# ── marcos ────────────────────────────────────────────────────────────

def test_resolver_marcos_sem_datas():
    marcos = regras.resolver_marcos()
    assert list(marcos) == list(MARCOS)
    assert all(m["contrato"] is None for m in marcos.values())
    assert marcos["MT10"]["consolidacao"] is None


def test_resolver_marcos_traz_data_base_evento_e_notas():
    marcos = regras.resolver_marcos("2019-05-02")
    assert marcos["MT04"]["contrato"] == "posterior" and marcos["MT05"]["contrato"] == "anterior"
    assert marcos["MT02"] == {"data": "2008-04-30", "base": "contrato", "evento": marcos["MT02"]["evento"],
                              "contrato": "posterior"}
    assert marcos["MT05"]["nota"] == ("corte por pagamento: reparte a apuração (cada pagamento antes ou "
                                      "depois do marco), não exclui a regra")
    assert marcos["MT06"]["nota"] == "corte pela data da operação de rotativo/parcelamento, não pela data do contrato"
    assert "nota" not in marcos["MT04"] and "consolidacao" not in marcos["MT04"]


def test_resolver_marcos_com_consolidacao():
    marcos = regras.resolver_marcos("2010-01-01", date(2020, 1, 1))
    assert marcos["MT10"]["contrato"] == "anterior" and marcos["MT10"]["consolidacao"] == "posterior"
    assert marcos["MT10"]["base"] == "contrato_ou_consolidacao"


# ── fronteiras do corte por contrato ──────────────────────────────────

@pytest.mark.parametrize("rid,marco,posicao,igual_aplica", [
    ("R01", "MT04", "anterior", False), ("R05", "MT02", "anterior_ou_igual", True),
    ("R04", "MT02", "posterior", False), ("R10", "MT03", "posterior", False),
    ("R18", "MT01", "posterior", False)])
def test_fronteira_data_igual_ao_marco(rid, marco, posicao, igual_aplica):
    assert DADOS["regras"][int(rid[1:]) - 1]["corte_temporal"] == {
        "aplica_se": DADOS["regras"][int(rid[1:]) - 1]["corte_temporal"]["aplica_se"],
        "marco": marco, "posicao": posicao}
    eva = lambda iso: destino(rodar(contrato=iso), rid) == "aplicaveis"            # noqa: E731
    antes, igual, depois = (eva(dia(MARCOS[marco], d)) for d in (-1, 0, 1))
    esperado = {"anterior": (True, False, False), "anterior_ou_igual": (True, True, False),
                "posterior": (False, False, True)}[posicao]
    assert (antes, igual, depois) == esperado
    assert igual is igual_aplica


def test_motivo_do_corte_por_contrato():
    saida = rodar(contrato="2017-09-01")
    assert achar(saida, "R01")[1]["motivo"] == "MT04 (01/09/2017): contrato igual ao marco — a regra exige anterior"
    assert achar(rodar(contrato="2019-05-02"), "R05")[1]["motivo"] == (
        "MT02 (30/04/2008): contrato posterior ao marco — a regra exige anterior_ou_igual")
    assert achar(rodar(contrato="1999-01-01"), "R18")[1]["motivo"] == (
        "MT01 (31/03/2000): contrato anterior ao marco — a regra exige posterior")


def test_sem_data_do_contrato_a_regra_vai_a_confirmar_com_motivo():
    saida = rodar(contrato=None)
    lista, item = achar(saida, "R01")
    assert lista == "confirmar" and item["motivo"] == "data do contrato ausente — corte MT04 (01/09/2017)"
    assert item["conclusiva"] is True and item["id"] == "R01"
    assert achar(saida, "R10")[1]["motivo"] == "data do contrato ausente — corte MT03 (25/02/2011)"
    assert [i["id"] for i in saida["confirmar"]] == ["R01", "R02", "R04", "R05", "R06", "R07", "R10", "R13", "R18"]


# ── grupos de tipo ────────────────────────────────────────────────────

def test_grupo_todos_vale_para_qualquer_tipo():
    for tid in TIPOS:
        saida = rodar(tid, "consumerista", "2019-05-02", data_consolidacao="2019-05-02")
        desligadas = _tipo(DADOS, tid).get("regras_desligadas", [])
        if "R28" not in desligadas:
            assert destino(saida, "R28") == "aplicaveis", tid


def test_grupo_todos_sem_lei_especifica():
    for tid in DADOS["tipos_contrato"]["grupos"]["todos_sem_lei_especifica"]:
        assert destino(rodar(tid), "R21") in ("aplicaveis", "confirmar"), tid
    for tid in ("cedula_rural", "cedula_comercial", "cedula_industrial", "sfh", "sfi", "imobiliario_fora_sfi"):
        lista, item = achar(rodar(tid), "R21")
        assert lista == "nao_aplicaveis" and item["motivo"] == f"tipo_contrato todos_sem_lei_especifica não inclui {tid}"


def test_grupo_todos_sfn_exclui_credor_fora_do_sfn():
    # a R18 também está em regras_desligadas do tipo: tira-se de lá para isolar o efeito do grupo
    copia = adulterar(lambda d: _tipo(d, "imobiliario_fora_sfi").__setitem__(
        "regras_desligadas", [r for r in _tipo(d, "imobiliario_fora_sfi")["regras_desligadas"] if r != "R18"]))
    lista, item = achar(avaliar("imobiliario_fora_sfi", "consumerista", "2019-01-01", hoje=HOJE, dados=copia), "R18")
    assert lista == "nao_aplicaveis" and item["motivo"] == "tipo_contrato todos_sfn não inclui imobiliario_fora_sfi"
    assert destino(rodar("sfi", contrato="2019-01-01"), "R18") == "nao_aplicaveis"      # desligada no SFI
    for tid in ("consumo_pf", "empresarial_pj", "cedula_rural", "cartao_credito"):
        assert destino(rodar(tid, contrato="2019-01-01"), "R18") == "aplicaveis", tid


def test_tags_de_tipo_simples_e_lista():
    lista, item = achar(rodar("consumo_pf"), "R17")
    assert lista == "nao_aplicaveis" and item["motivo"] == (
        "tipo_contrato cedula_rural, cedula_comercial, cedula_industrial não inclui consumo_pf")
    assert destino(rodar("cedula_rural"), "R17") == "aplicaveis"
    assert destino(rodar("sfh"), "R34") == "aplicaveis" and destino(rodar("sfi"), "R34") == "nao_aplicaveis"
    assert destino(rodar("cartao_consignado"), "R24") == "aplicaveis"


# ── regras desligadas e superadas ─────────────────────────────────────

@pytest.mark.parametrize("tid", [t["id"] for t in DADOS["tipos_contrato"]["tipos"] if t.get("regras_desligadas")])
def test_regras_desligadas_do_tipo(tid):
    desligadas = _tipo(DADOS, tid)["regras_desligadas"]
    assert desligadas
    for regime in REGIMES:
        saida = rodar(tid, regime, "2019-05-02", data_consolidacao="2019-05-02")
        for rid in desligadas:
            lista, item = achar(saida, rid)
            assert lista == "nao_aplicaveis", (tid, rid)
            assert item["motivo"] == f"desligada no tipo {tid} (regras_desligadas)"


def test_habitacionais_desligam_a_r15():
    for tid in ("sfh", "sfi", "imobiliario_fora_sfi"):
        assert "R15" in _tipo(DADOS, tid)["regras_desligadas"]
        assert destino(rodar(tid), "R15") == "nao_aplicaveis"
    assert destino(rodar("consumo_pf"), "R15") == "aplicaveis"


def test_regra_superada_nao_se_aplica():
    copia = adulterar(lambda d: d["regras"][3].__setitem__("status", "superada"))        # R04
    lista, item = achar(avaliar("consumo_pf", "consumerista", "2019-05-02", hoje=HOJE, dados=copia), "R04")
    assert lista == "nao_aplicaveis" and item["motivo"] == "regra superada"


# ── regime ────────────────────────────────────────────────────────────

def test_regime_r15_resolve_tier_e_consequencia():
    bloco = DADOS["regras"][14]["regime"]
    cons = achar(rodar(regime="consumerista"), "R15")[1]
    civ = achar(rodar(regime="civil_empresarial"), "R15")[1]
    assert (cons["tier"], civ["tier"]) == ("T1", "T2")
    assert cons["consequencia"] == bloco["consumerista"]["consequencia"]
    assert civ["consequencia"] == bloco["civil_empresarial"]["consequencia"]
    assert cons["tier"] == bloco["consumerista"]["tier"] and cons["consequencia"] != civ["consequencia"]


def test_regime_com_aplica_false_exclui():
    copia = adulterar(lambda d: d["regras"][14]["regime"]["civil_empresarial"].__setitem__("aplica", False))
    lista, item = achar(avaliar("consumo_pf", "civil_empresarial", "2019-05-02", hoje=HOJE, dados=copia), "R15")
    assert lista == "nao_aplicaveis" and item["motivo"] == "não se aplica no regime civil_empresarial"
    assert destino(avaliar("consumo_pf", "consumerista", "2019-05-02", hoje=HOJE, dados=copia), "R15") == "aplicaveis"


def test_consumo_pf_civil_empresarial_exclui_regra_so_consumerista():
    saida = rodar("consumo_pf", "civil_empresarial")
    for rid in ("R04", "R06", "R22", "R26"):
        lista, item = achar(saida, rid)
        assert lista == "nao_aplicaveis" and item["motivo"] == "regra consumerista — regime civil-empresarial", rid
    assert destino(saida, "R28") == "aplicaveis"          # tags ['todos']: não é só consumerista


def test_empresarial_pj_civil_empresarial_confirma_o_que_esta_fora_de_regras_sem_cdc():
    sem_cdc = _tipo(DADOS, "empresarial_pj")["regras_sem_cdc"]
    saida = rodar("empresarial_pj", "civil_empresarial", dia(MARCOS["MT04"], -1))
    for rid in ("R11", "R12", "R14", "R16", "R28", "R29", "R30", "R31", "R32", "R33"):
        assert rid not in sem_cdc
        lista, item = achar(saida, rid)
        assert lista == "confirmar", rid
        assert item["motivo"] == "fora de regras_sem_cdc: confirmar que a tese não depende do CDC (regra de conduta 18)"
    for rid in ("R01", "R02", "R03", "R18", "R19", "R21", "R25"):
        assert destino(saida, rid) == "aplicaveis", rid
    assert destino(saida, "R15") == "aplicaveis"           # tem bloco regime: não vai a confirmar
    assert destino(saida, "R04") == "nao_aplicaveis"       # consumo_pf: não casa fora do consumerista


def test_empresarial_pj_consumerista_cdc_mitigado_casa_as_regras_consumo_pf():
    saida = rodar("empresarial_pj", "consumerista", "2019-05-02")
    for rid in ("R04", "R06", "R09", "R22", "R26"):
        assert destino(saida, rid) == "aplicaveis", rid
    assert achar(saida, "R11")[0] == "aplicaveis"          # em regime consumerista nada vai a confirmar pela regra 18
    assert not any("regra de conduta 18" in i["motivo"] for i in saida["confirmar"])


def test_repeticao_consumerista_fora_de_consumo_pf_e_pj_vai_a_confirmar():
    for tid in ("cartao_credito", "cartao_consignado", "sfh", "sfi", "cedula_rural", "imobiliario_fora_sfi"):
        saida = rodar(tid, "consumerista", "2019-05-02")
        for rid in ("R26", "R27"):
            lista, item = achar(saida, rid)
            assert lista == "confirmar", (tid, rid)
            assert item["motivo"] == f"repetição segue o regime (regra de conduta 9): confirmar a relação de consumo no tipo {tid}"
        civ = rodar(tid, "civil_empresarial", "2019-05-02")
        assert destino(civ, "R26") == "nao_aplicaveis", tid
    assert destino(rodar("consumo_pf"), "R26") == "aplicaveis"


def test_regime_aceita_alias_e_recusa_outros():
    assert rodar(regime="civil-empresarial")["entrada"]["regime"] == "civil_empresarial"
    assert rodar(regime="civil-empresarial")["aplicaveis"] == rodar(regime="civil_empresarial")["aplicaveis"]
    for ruim in ("civil", "empresarial", "", None, "Consumerista"):
        with pytest.raises(ValueError, match="regime inválido"):
            rodar(regime=ruim)


def test_tipo_invalido_lista_os_validos():
    with pytest.raises(ValueError) as erro:
        rodar("pessoa_fisica")
    assert all(t in str(erro.value) for t in TIPOS)


# ── corte por pagamento e por operação ────────────────────────────────

@pytest.mark.parametrize("contrato", [None, "1995-01-01", "2021-03-30", "2025-01-01"])
def test_corte_por_pagamento_nunca_exclui_pela_data_do_contrato(contrato):
    for rid, posicao in (("R26", "posterior"), ("R27", "anterior_ou_igual")):
        lista, item = achar(rodar(contrato=contrato), rid)
        assert lista == "aplicaveis"
        assert item["corte"] == {"marco": "MT05", "data": "2021-03-30", "base": "pagamento", "posicao": posicao}


@pytest.mark.parametrize("contrato", [None, "2015-01-01", "2024-01-03", "2025-01-01"])
def test_corte_por_operacao_nunca_exclui_pela_data_do_contrato(contrato):
    lista, item = achar(rodar("cartao_credito", contrato=contrato), "R23")
    assert lista == "aplicaveis"
    assert item["corte"] == {"marco": "MT06", "data": "2024-01-03", "base": "operacao", "posicao": "posterior"}


# ── corte por contrato ou consolidação (MT10) ─────────────────────────

def r40(contrato, consolidacao, tipo="sfh"):
    return achar(rodar(tipo, "consumerista", contrato, data_consolidacao=consolidacao), "R40")


def test_mt10_sem_uma_das_datas_vai_a_confirmar():
    for contrato, consolidacao in ((None, None), ("2010-01-01", None), (None, "2010-01-01")):
        lista, item = r40(contrato, consolidacao)
        assert lista == "confirmar" and item["motivo"] == "datar contrato e consolidação (MT10)"


@pytest.mark.parametrize("contrato,consolidacao,esperado", [
    ("2010-01-01", "2015-01-01", ("aplicaveis", "contrato e consolidação atendem ao marco")),
    ("2010-01-01", "2020-01-01", ("aplicaveis", "só o contrato atende ao marco — critério temporal divergente (ver pendências)")),
    ("2020-01-01", "2015-01-01", ("aplicaveis", "só a consolidação atende ao marco — critério temporal divergente (ver pendências)")),
    ("2020-01-01", "2021-01-01", ("nao_aplicaveis", "MT10: contrato e consolidação fora do marco")),
    ("2017-07-10", "2017-07-10", ("aplicaveis", "contrato e consolidação atendem ao marco")),
    ("2017-07-11", "2017-07-11", ("nao_aplicaveis", "MT10: contrato e consolidação fora do marco"))])
def test_mt10_os_quatro_casos_e_a_fronteira(contrato, consolidacao, esperado):
    lista, item = r40(contrato, consolidacao)
    assert lista == esperado[0]
    if lista == "aplicaveis":
        assert item["corte"]["leitura"] == esperado[1]
        assert item["corte"]["marco"] == "MT10" and item["corte"]["base"] == "contrato_ou_consolidacao"
    else:
        assert item["motivo"] == esperado[1]


def test_mt10_vale_para_sfi_e_imobiliario_mas_nao_para_consumo_pf():
    assert r40("2010-01-01", "2015-01-01", "sfi")[0] == "aplicaveis"
    assert r40("2010-01-01", "2015-01-01", "imobiliario_fora_sfi")[0] == "aplicaveis"
    assert r40("2010-01-01", "2015-01-01", "consumo_pf")[0] == "nao_aplicaveis"


# ── R03: regime_por_marco ─────────────────────────────────────────────

def test_r03_antes_do_mt04():
    item = achar(rodar(contrato=dia(MARCOS["MT04"], -1)), "R03")[1]
    leitura = DADOS["regras"][2]["regime_por_marco"]["anterior_a_MT04"]
    assert item["consequencia"] == leitura["consequencia"]
    assert item["fundamentacao_marco"] == leitura["fundamentacao"]
    assert "alerta" not in item and item["exige_pesquisa"] is False
    assert "leitura_por_marco_pendente" not in item


@pytest.mark.parametrize("contrato", ["2017-09-01", "2017-09-02", "2024-05-05"])
def test_r03_no_dia_do_mt04_ou_depois(contrato):
    item = achar(rodar(contrato=contrato), "R03")[1]
    leitura = DADOS["regras"][2]["regime_por_marco"]["posterior_a_MT04"]
    assert item["consequencia"] == leitura["consequencia"] and item["alerta"] == leitura["alerta"]
    assert item["fundamentacao_marco"] == leitura["fundamentacao"]
    assert item["exige_pesquisa"] is True and item["conclusiva"] is True
    assert item["alerta"].startswith("NÃO citar Súmula 294, 296 ou 472")


def test_r03_sem_data_usa_a_consequencia_geral_e_marca_a_pendencia():
    item = achar(rodar(contrato=None), "R03")[1]
    assert item["consequencia"] == DADOS["regras"][2]["consequencia"]
    assert item["leitura_por_marco_pendente"] is True
    assert "fundamentacao_marco" not in item and "alerta" not in item


def test_r03_traz_os_termos_suspeitos_e_o_alerta_da_leitura_se_concatena_ao_da_regra():
    item = achar(rodar(), "R03")[1]
    assert item["termos_suspeitos"] == DADOS["regras"][2]["padroes_deteccao"]["termos_suspeitos"]
    copia = adulterar(lambda d: d["regras"][2].__setitem__("alerta", "Alerta da regra."))
    junto = achar(avaliar("consumo_pf", "consumerista", "2019-05-02", hoje=HOJE, dados=copia), "R03")[1]
    assert junto["alerta"].startswith("Alerta da regra. NÃO citar Súmula 294")


# ── status, conclusiva, pendências ────────────────────────────────────

def test_regras_suspensas_e_sem_precedente_nao_concluem():
    saida = rodar("consumo_pf", "consumerista", "2019-05-02")
    for rid in ("R15", "R30", "R31", "R32", "R33"):
        item = achar(saida, rid)[1]
        assert item["conclusiva"] is False and item["exige_pesquisa"] is True, rid
    assert saida["resumo"]["nao_conclusivas"] == ["R15", "R30", "R31", "R32", "R33"]
    assert achar(saida, "R28")[1]["conclusiva"] is True and achar(saida, "R28")[1]["exige_pesquisa"] is False
    assert achar(rodar("cartao_consignado"), "R24")[1]["conclusiva"] is False
    assert achar(rodar("sfh", contrato="2000-01-01", data_consolidacao="2000-01-01"), "R40")[1]["conclusiva"] is False


def test_nao_conclusivas_inclui_as_regras_a_confirmar():
    # empresarial_pj civil-empresarial: R30–R33 (sem precedente) vão a confirmar, R15 (suspensa) aplica
    pj = rodar("empresarial_pj", "civil_empresarial", dia(MARCOS["MT04"], -1))
    assert [destino(pj, r) for r in ("R15", "R30", "R31", "R32", "R33")] == ["aplicaveis"] + ["confirmar"] * 4
    assert pj["resumo"]["nao_conclusivas"] == ["R15", "R30", "R31", "R32", "R33"]
    # sfh sem as datas: a R40 (sem precedente) vai a confirmar e continua listada como não conclusiva
    sfh = rodar("sfh", contrato=None)
    assert destino(sfh, "R40") == "confirmar" and "R40" in sfh["resumo"]["nao_conclusivas"]
    # regra não aplicável não entra na lista
    assert "R40" not in rodar("consumo_pf")["resumo"]["nao_conclusivas"]


def _tema(regra_id):
    return next(t for t in DADOS["pendencias_jurisprudenciais"]["temas"] if regra_id in t["regras_afetadas"])


def test_pendencia_no_ultimo_dia_da_validade_nao_vence_e_no_seguinte_vence():
    tema = _tema("R15")
    limite = date.fromisoformat(tema["verificado_em"]) + timedelta(days=DADOS["pendencias_jurisprudenciais"]["validade_dias"])
    no_limite, apos = rodar(hoje=limite), rodar(hoje=limite + timedelta(days=1))
    assert achar(no_limite, "R15")[1]["pendencias"][0]["vencida"] is False
    assert achar(no_limite, "R15")[1]["alertas_vencidos"] == [] and "R15" not in no_limite["resumo"]["com_alerta_vencido"]
    assert achar(apos, "R15")[1]["pendencias"][0]["vencida"] is True
    assert "R15" in apos["resumo"]["com_alerta_vencido"]


def test_alerta_vencido_usa_o_modelo_do_json():
    tema = _tema("R15")
    verificado = date.fromisoformat(tema["verificado_em"])
    item = achar(rodar(hoje=verificado + timedelta(days=200)), "R15")[1]
    assert item["alertas_vencidos"] == [
        "STATUS POSSIVELMENTE DESATUALIZADO: a pendência do Tema 1378/STJ foi conferida pela última vez em "
        f"{verificado:%d/%m/%Y}. Validar via pesquisa-jurisprudencial-jusia antes de citar ou de emitir conclusão."]
    assert item["pendencias"] == [{"tema": tema["tema"], "status": tema["status"],
                                   "verificado_em": tema["verificado_em"], "vencida": True}]


def test_hoje_aceita_data_ou_texto_e_aparece_na_saida():
    assert rodar(hoje="2026-12-31")["hoje"] == "2026-12-31"
    assert rodar(hoje=date(2026, 12, 31))["hoje"] == "2026-12-31"
    assert avaliar("consumo_pf", "consumerista")["hoje"] == date.today().isoformat()


def test_hoje_padrao_e_o_dia_da_chamada(monkeypatch):
    class Dia(date):
        @classmethod
        def today(cls):
            return cls(2031, 3, 4)

    monkeypatch.setattr(regras, "date", Dia)
    saida = avaliar("consumo_pf", "consumerista", "2019-05-02")
    assert saida["hoje"] == "2031-03-04"
    assert achar(saida, "R15")[1]["pendencias"][0]["vencida"] is True       # 2031 está bem além dos 90 dias


def test_pendencias_por_regra():
    saida = rodar("cartao_consignado")
    r24 = achar(saida, "R24")[1]
    assert [p["tema"] for p in r24["pendencias"]] == ["Tema 1328/STJ", "Tema 1414/STJ"]
    assert achar(rodar(), "R28")[1]["pendencias"] == []
    r26 = achar(rodar(), "R26")[1]
    assert [p["tema"] for p in r26["pendencias"]] == ["Tema 929/STJ"]
    sfh = achar(rodar("sfh", contrato="2000-01-01", data_consolidacao="2000-01-01"), "R40")[1]
    assert sfh["pendencias"][0]["tema"].startswith("Purga da mora")


def test_alertas_vencidos_so_das_regras_que_entram_no_caso():
    longe = date.fromisoformat(HOJE) + timedelta(days=400)
    saida = rodar("cartao_consignado", "civil_empresarial", hoje=longe)
    assert destino(saida, "R26") == "nao_aplicaveis"
    assert saida["resumo"]["com_alerta_vencido"] == ["R15", "R24"]
    assert len(achar(saida, "R24")[1]["alertas_vencidos"]) == 2
    # a regra a confirmar também carrega o alerta: o operador decide com a pendência à vista
    assert "R26" in rodar("cartao_consignado", "consumerista", hoje=longe)["resumo"]["com_alerta_vencido"]


# ── categorias ────────────────────────────────────────────────────────

def test_categorias_filtram_e_contam_as_omitidas():
    saida = rodar(categorias=["tarifas", "iof"])
    ids = {i["id"] for k in ("aplicaveis", "confirmar", "nao_aplicaveis") for i in saida[k]}
    assert ids == {r["id"] for r in DADOS["regras"] if r["categoria"] in ("tarifas", "iof")}
    assert saida["resumo"]["omitidas_por_categoria"] == TOTAL - len(ids)
    assert saida["entrada"]["categorias"] == ["tarifas", "iof"]
    assert (saida["resumo"]["aplicaveis"] + saida["resumo"]["confirmar"] + saida["resumo"]["nao_aplicaveis"]
            + saida["resumo"]["omitidas_por_categoria"]) == TOTAL


def test_categorias_como_texto_separado_por_virgula():
    assert rodar(categorias="tarifas, iof")["entrada"]["categorias"] == ["tarifas", "iof"]
    assert rodar(categorias="tarifas, iof")["resumo"] == rodar(categorias=["tarifas", "iof"])["resumo"]


def test_sem_categorias_nada_e_omitido():
    saida = rodar()
    assert saida["entrada"]["categorias"] is None and saida["resumo"]["omitidas_por_categoria"] == 0


def test_categoria_exclui_antes_de_qualquer_outro_passo():
    saida = rodar("sfh", categorias=["tarifas"])        # R15 está desligada no sfh, mas é de outra categoria
    assert achar(saida, "R15") == (None, None)


# ── formatos ──────────────────────────────────────────────────────────

CHAVES_PADRAO = {"id", "categoria", "nome", "status", "tier", "resultado_se_positivo", "consequencia", "teste",
                 "conclusiva", "exige_pesquisa", "pendencias", "alertas_vencidos"}


def test_formato_padrao_traz_os_campos_do_item():
    item = achar(rodar(), "R28")[1]
    assert CHAVES_PADRAO <= set(item) and "alerta" not in item or item["alerta"]
    assert set(item["teste"]) == {"logica", "campos_necessarios"}
    r15 = achar(rodar(), "R15")[1]
    assert set(r15["teste"]) == {"logica", "campos_necessarios", "requer_consulta_bacen", "parametros"}
    assert r15["teste"]["parametros"] == {"limiar_zona_cinzenta": 1.5, "limiar_forte": 2.0}
    assert r15["alerta"].startswith("TEMA 1378/STJ")
    assert "descricao" not in r15 and "fundamentacao" not in r15 and "regime" not in r15


def test_formato_padrao_carrega_os_blocos_especificos():
    assert achar(rodar("cartao_credito", contrato="2024-02-01"), "R23")[1]["implementacao"]["modulo"] == "motores/cartao.py"
    assert achar(rodar("sfh"), "R34")[1]["resultado_se_sem_conta_grafica"] == "a_verificar"
    assert achar(rodar("sfh"), "R36")[1]["resultado_se_sem_conta_grafica"] == "a_verificar"
    assert achar(rodar("sfh", contrato="2000-01-01", data_consolidacao="2000-01-01"), "R39")[1]["teste"]["requer_sub_skill"]
    assert "implementacao" not in achar(rodar(), "R28")[1]


def test_formato_resumo():
    saida = rodar(formato="resumo")
    assert set(achar(saida, "R28")[1]) == {"id", "categoria", "nome", "tier", "status", "conclusiva"}
    assert set(achar(saida, "R26")[1]) == {"id", "categoria", "nome", "tier", "status", "conclusiva", "corte"}
    confirmar = achar(rodar(contrato=None, formato="resumo"), "R01")[1]
    assert set(confirmar) == {"id", "categoria", "nome", "tier", "status", "conclusiva", "motivo"}
    vencido = achar(rodar(hoje="2030-01-01", formato="resumo"), "R15")[1]
    assert vencido["alertas_vencidos"] and "pendencias" not in vencido and "consequencia" not in vencido


def test_formato_completo():
    item = achar(rodar(formato="completo"), "R15")[1]
    padrao = achar(rodar(), "R15")[1]
    assert set(padrao) < set(item)
    assert item["descricao"] == DADOS["regras"][14]["descricao"]
    assert item["fundamentacao"] == DADOS["regras"][14]["fundamentacao"]
    assert item["regime"] == DADOS["regras"][14]["regime"]
    r03 = achar(rodar(formato="completo"), "R03")[1]
    assert r03["regime_por_marco"] == DADOS["regras"][2]["regime_por_marco"]
    assert r03["observacao_metodologica"] == DADOS["regras"][2]["observacao_metodologica"]
    assert "regime" not in achar(rodar(formato="completo"), "R28")[1]


def test_nao_aplicaveis_sao_iguais_em_todos_os_formatos():
    visto = {f: rodar(formato=f)["nao_aplicaveis"] for f in ("resumo", "padrao", "completo")}
    assert visto["resumo"] == visto["padrao"] == visto["completo"]
    assert all(set(i) == {"id", "nome", "motivo"} for i in visto["padrao"])


def test_formato_invalido():
    with pytest.raises(ValueError, match="formato inválido"):
        rodar(formato="longo")


# ── saída: forma e invariantes ────────────────────────────────────────

def test_forma_da_saida():
    saida = rodar("sfh", contrato="2000-01-01", data_consolidacao="2010-01-01")
    assert list(saida) == ["versao_regras", "hoje", "entrada", "tipo", "marcos", "aplicaveis", "confirmar",
                           "nao_aplicaveis", "resumo"]
    assert saida["versao_regras"] == DADOS["versao"] == "6.0.0"
    assert saida["entrada"] == {"tipo": "sfh", "regime": "consumerista", "data_contrato": "2000-01-01",
                                "data_consolidacao": "2010-01-01", "categorias": None}
    sfh = _tipo(DADOS, "sfh")
    assert saida["tipo"] == {"id": "sfh", "nome": sfh["nome"], "cdc_aplicavel": sfh["cdc_aplicavel"],
                             "regras_desligadas": sfh["regras_desligadas"],
                             "campos_extras_obrigatorios": sfh["campos_extras_obrigatorios"]}
    assert "gate_obrigatorio" not in saida["tipo"]
    assert rodar("empresarial_pj")["tipo"]["gate_obrigatorio"] == _tipo(DADOS, "empresarial_pj")["gate_obrigatorio"]
    assert set(rodar("consumo_pf")["tipo"]) == {"id", "nome", "cdc_aplicavel"}
    assert saida["marcos"] == regras.resolver_marcos("2000-01-01", "2010-01-01")


@pytest.mark.parametrize("tipo,regime", list(product(TIPOS, REGIMES)))
@pytest.mark.parametrize("datas", [(None, None), ("2005-06-15", "2010-01-01"), ("2023-05-01", "2024-06-01")])
def test_toda_regra_cai_em_exatamente_um_destino(tipo, regime, datas):
    saida = rodar(tipo, regime, datas[0], data_consolidacao=datas[1])
    vistos = [i["id"] for k in ("aplicaveis", "confirmar", "nao_aplicaveis") for i in saida[k]]
    assert sorted(vistos) == sorted(r["id"] for r in DADOS["regras"])
    assert len(set(vistos)) == TOTAL
    assert [i["id"] for i in saida["aplicaveis"]] == sorted(i["id"] for i in saida["aplicaveis"])
    json.dumps(saida, ensure_ascii=False)                  # serializável
    for item in saida["confirmar"]:
        assert item["motivo"]


def test_saida_nao_compartilha_estado_com_o_json_em_cache():
    antes = json.dumps(DADOS, sort_keys=True)
    saida = rodar("sfh", contrato="2000-01-01", data_consolidacao="2010-01-01", formato="completo")
    for item in saida["aplicaveis"]:
        item["teste"]["campos_necessarios"].append("x")
        item["pendencias"].append("y")
        item.pop("fundamentacao", None)
    saida["tipo"]["regras_desligadas"].append("R99")
    assert json.dumps(regras.carregar_dados(), sort_keys=True) == antes
    assert rodar() == rodar()


# ── consultas: regra, súmula, séries ──────────────────────────────────

def test_regra_integral():
    r = regras.regra("R15")
    assert r == DADOS["regras"][14] and r is not DADOS["regras"][14]
    assert regras.regra("r03")["id"] == "R03"
    assert [regras.regra(i)["id"] for i in ("R01", "R40")] == ["R01", "R40"]
    with pytest.raises(KeyError, match="R99"):
        regras.regra("R99")


def test_sumula():
    assert regras.sumula(530)["texto"].startswith("Nos contratos bancários, na impossibilidade")
    assert regras.sumula("541")["numero"] == 541
    assert regras.sumula(450)["numero"] == 450
    with pytest.raises(KeyError, match="1"):
        regras.sumula(1)
    with pytest.raises(ValueError):
        regras.sumula("abc")


def test_series_sem_filtro_e_por_modalidade():
    mapa = DADOS["series_bacen_por_modalidade"]["mapeamento"]
    assert regras.series() == mapa and regras.series() is not mapa
    assert regras.series(modalidade="cartao_rotativo") == [
        {"modalidade": "cartao_rotativo", "serie": 25477, "nome": "Cartão de crédito rotativo — PF", "unidade": "% a.m."}]
    assert regras.series(modalidade="cartao") == []                 # igualdade exata, não substring
    assert regras.series(modalidade="Cartao_Rotativo") == []


@pytest.mark.parametrize("busca", ["cartão", "CARTAO", "Cartão", "cartao"])
def test_series_busca_sem_acento_e_sem_caixa(busca):
    achadas = regras.series(buscar=busca)
    assert {s["modalidade"] for s in achadas} == {"cartao_rotativo", "cartao_parcelado", "cartao_rotativo_pj",
                                                  "cartao_parcelado_pj"}


def test_series_busca_em_modalidade_e_em_nome():
    assert [s["serie"] for s in regras.series(buscar="cheque especial")] == [25463, 25446]
    assert {s["serie"] for s in regras.series(buscar="veículo")} == {25471, 25447, 25450, 25474}
    assert {s["modalidade"] for s in regras.series(buscar="capital_giro")} >= {"capital_giro_ate_365"}
    assert regras.series(buscar="inexistente") == []
    assert len(regras.series(modalidade="cartao_rotativo", buscar="pj")) == 0


# ── razão contratada / média ──────────────────────────────────────────

@pytest.mark.parametrize("contratada,media,classificacao,razao,texto", [
    (1.0, 2.0, "licita", 0.5, "0,50x"),
    (2.99, 2.0, "licita", 1.495, "1,50x"),
    (3.00, 2.0, "zona_cinzenta", 1.5, "1,50x"),
    (0.03, 0.02, "zona_cinzenta", 1.5, "1,50x"),
    (3.9999, 2.0, "zona_cinzenta", 2.0, "2,00x"),
    (4.00, 2.0, "ilicita", 2.0, "2,00x"),
    (0.06, 0.03, "ilicita", 2.0, "2,00x"),
    (4.74, 3.0, "zona_cinzenta", 1.58, "1,58x"),
    (10.0, 2.0, "ilicita", 5.0, "5,00x"),
    (0.0, 2.0, "licita", 0.0, "0,00x")])
def test_razao_em_cada_faixa_e_exatamente_nos_limiares(contratada, media, classificacao, razao, texto):
    r = regras.classificar_razao(contratada, media)
    assert r["classificacao"] == classificacao
    assert r["razao"] == razao and r["razao_txt"] == texto
    assert r["contratada_am"] == contratada and r["media_am"] == media


def test_razao_limiares_e_rotulos():
    r = regras.classificar_razao(2.99, 1.85)
    assert r["limiares_am"] == {"zona_cinzenta": 2.775, "forte": 3.7}
    assert regras.classificar_razao(1, 2)["rotulo"] == "dentro da faixa de mercado"
    assert regras.classificar_razao(3, 2)["rotulo"] == "zona de abusividade"
    assert regras.classificar_razao(4, 2)["rotulo"] == "fortemente abusiva"
    assert set(r) == {"razao", "razao_txt", "classificacao", "rotulo", "limiares_am", "contratada_am", "media_am"}


def test_razao_arredonda_half_up_na_exibicao_e_nao_no_calculo():
    # média 2,000025: zona 3,0000375 → 3,0000; forte 4,00005 → 4,0001 (HALF_UP; float/round daria 4,0)
    r = regras.classificar_razao(3.0, 2.000025)
    assert r["limiares_am"] == {"zona_cinzenta": 3.0, "forte": 4.0001}
    assert regras.classificar_razao(3.000037, 2.000025)["classificacao"] == "licita"      # < 3,0000375
    assert regras.classificar_razao(3.000038, 2.000025)["classificacao"] == "zona_cinzenta"
    assert regras.classificar_razao(1.0, 3.0)["razao"] == 0.3333 and regras.classificar_razao(2.0, 3.0)["razao"] == 0.6667
    assert regras.classificar_razao(1.005, 1.0)["razao_txt"] == "1,01x"                   # HALF_UP, não 1,00


def test_razao_nao_cai_em_erro_de_float():
    # em float, 0.03 / 0.02 = 1.4999999999999998 em algumas combinações; em Decimal é exatamente 1,5
    for c, m in ((0.03, 0.02), (0.45, 0.30), (1.275, 0.85), (2.25, 1.5), (0.0105, 0.007)):
        assert regras.classificar_razao(c, m)["classificacao"] == "zona_cinzenta", (c, m)
        assert regras.classificar_razao(c, m)["razao"] == 1.5


def test_razao_le_os_limiares_da_r15():
    copia = adulterar(lambda d: d["regras"][14]["teste"]["parametros"].update(limiar_zona_cinzenta=1.2, limiar_forte=1.8))
    assert regras.classificar_razao(2.4, 2.0, copia)["classificacao"] == "zona_cinzenta"
    assert regras.classificar_razao(3.6, 2.0, copia)["classificacao"] == "ilicita"
    assert regras.classificar_razao(2.39, 2.0, copia)["classificacao"] == "licita"
    assert regras.classificar_razao(2.4, 2.0)["classificacao"] == "licita"              # JSON real: 1,2x < 1,5x
    assert regras.classificar_razao(2.4, 2.0)["limiares_am"] == {"zona_cinzenta": 3.0, "forte": 4.0}
    assert regras.classificar_razao(2.4, 2.0, copia)["limiares_am"] == {"zona_cinzenta": 2.4, "forte": 3.6}


@pytest.mark.parametrize("contratada,media", [(2.0, 0), (2.0, -1.0), (-0.01, 2.0)])
def test_razao_recusa_media_nao_positiva_e_contratada_negativa(contratada, media):
    with pytest.raises(ValueError):
        regras.classificar_razao(contratada, media)


# ── dados: caminho padrão, cache e arquivo próprio ────────────────────

def test_carregar_dados_cache_por_caminho_e_recarrega_se_o_arquivo_muda(tmp_path):
    assert regras.carregar_dados() is regras.carregar_dados(regras.CAMINHO_PADRAO)
    arq = tmp_path / "outro.json"
    arq.write_text(json.dumps({"versao": "x", "regras": []}), encoding="utf-8")
    primeira = regras.carregar_dados(arq)
    assert regras.carregar_dados(arq) is primeira and primeira["versao"] == "x"
    arq.write_text(json.dumps({"versao": "yy", "regras": []}), encoding="utf-8")
    assert regras.carregar_dados(arq)["versao"] == "yy"


def test_caminho_padrao_aponta_para_o_json_da_skill():
    assert regras.CAMINHO_PADRAO.name == "regras-bancarias.json"
    assert regras.CAMINHO_PADRAO.parent.name == "dados" and regras.CAMINHO_PADRAO.is_file()


