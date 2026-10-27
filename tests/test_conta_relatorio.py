"""Ramo CONTA do renderizador, de ponta a ponta: o bloco `conta` montado pelo
`conta_corrente.bloco_payload` a partir das saídas do motor (CSV -> reconciliação -> trinca ->
encontro de contas) passa pela validação e sai nos três formatos com os números do motor.

Extrato fictício, de quatro competências, sem nenhum dado de caso."""
import json
from datetime import date

import pytest

from motores import conta_corrente as cc
from motores import relatorios
from motores.relatorios import ADVERTENCIA_CONTA, ROTULOS_CENARIOS, brl, brl_rs, validar, validar_detalhado

LINHAS = ["2021-02-01;SAQUE;D;1.000,00;MOVIMENTO;;;-1.000,00",
          "2021-02-28;JUROS COBRADOS;D;90,00;ENCARGO;juros;;-1.090,00",
          "2021-03-31;JUROS COBRADOS;D;95,00;ENCARGO;juros;;-1.185,00",
          "2021-04-30;JUROS COBRADOS;D;100,00;ENCARGO;juros;;-1.285,00",
          "2021-05-31;JUROS COBRADOS;D;105,00;ENCARGO;juros;;-1.390,00"]
COMPETENCIAS = ("2021-02", "2021-03", "2021-04", "2021-05")
SERIES = [{"serie": "Taxa média de juros — modalidade fictícia", "codigo": "000000",
           "procedencia": "SGS/BACEN, via conector (valor oficial congelado)", "periodo": "02/2021 a 05/2021"}]
INICIO = date(2021, 2, 1)


def apurar(linhas=LINHAS, taxa_contratada=0.08, media=0.03):
    """O que a C1, a C4 e a C6 fazem com o motor, na ordem."""
    lancs = cc.carregar_csv(cc.CSV_CABECALHO + "\n" + "\n".join(linhas))
    reconciliacao = cc.reconciliar(lancs, 0.0, data_inicial=INICIO)
    trinca = cc.rodar_trinca(lancs, 0.0, taxa_contratada, {c: media for c in COMPETENCIAS}, data_inicial=INICIO)
    return reconciliacao, trinca


def payload_de(reconciliacao, trinca, lider="C1_TAXA_MEDIA", **extra):
    escolhido = next(c for c in trinca if c["cenario"] == lider)
    encontro = cc.encontro_de_contas(escolhido) if not escolhido.get("omitido") else {}
    p = relatorios._payload_demo_conta()
    p["conta"] = cc.bloco_payload(reconciliacao, trinca, lider, encontro, SERIES, **extra)
    return p


@pytest.fixture
def motor():
    return apurar()


def test_o_extrato_de_teste_fecha_e_a_trinca_tem_os_tres_estados(motor):
    reconciliacao, trinca = motor
    assert reconciliacao["veredito"] == "CONFORME" and reconciliacao["pontos_conferidos"] == 5
    c1, c2, c3 = trinca
    assert c1["favoravel"] is True and c1["excesso_final"] > 0
    assert c3["favoravel"] is False                                  # juros mantidos, nada a expurgar: excesso zero
    assert [c["cenario"] for c in trinca] == list(ROTULOS_CENARIOS)  # os rótulos cobrem a trinca do motor


def test_bloco_do_motor_passa_na_validacao_e_o_encontro_fecha(motor):
    p = payload_de(*motor)
    enc = p["conta"]["encontro"]
    assert abs(enc["base_repeticao_simples"] + enc["base_repeticao_dobro"] - enc["excesso_final"]) <= 0.01
    assert enc["base_repeticao_simples"] > 0 and enc["base_repeticao_dobro"] > 0     # o corte de 2021-03 reparte
    assert validar(p) == [] and json.loads(json.dumps(p["conta"])) == p["conta"]


def test_os_numeros_do_motor_chegam_aos_tres_formatos(motor, tmp_path):
    reconciliacao, trinca = motor
    p = payload_de(*motor)
    enc = p["conta"]["encontro"]
    arquivos = relatorios.gerar(p, tmp_path, formatos={"premium", "panorama"})
    premium = (tmp_path / "laudo-premium-demo-conta.html").read_text(encoding="utf-8")
    panorama = (tmp_path / "panorama-estrategico-demo-conta.html").read_text(encoding="utf-8")
    assert len(arquivos) == 3
    for valor in (trinca[0]["excesso_final"], enc["base_repeticao_simples"], enc["base_repeticao_dobro"],
                  trinca[2]["excesso_final"]):
        assert brl(valor) in premium, valor
    assert brl_rs(trinca[0]["excesso_final"]) in panorama and "5 pontos de conferência" in premium
    assert "01/02/2021 a 31/05/2021" in premium and "03/2021" in premium and ADVERTENCIA_CONTA in premium


def test_planilha_traz_os_numeros_do_motor(motor, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    reconciliacao, trinca = motor
    p = payload_de(*motor)
    x = relatorios.render_planilha(p, tmp_path / "conta.xlsx")
    ws = openpyxl.load_workbook(x)["Dashboard"]
    numeros = {c.value for linha in ws.iter_rows() for c in linha if isinstance(c.value, float)}
    assert trinca[0]["excesso_final"] in numeros and p["conta"]["encontro"]["base_repeticao_dobro"] in numeros
    assert reconciliacao["pontos_conferidos"] in {c.value for linha in ws.iter_rows() for c in linha}


def test_cenario_sem_excesso_do_motor_exige_ressalva(motor):
    p = payload_de(*motor)
    assert p["conta"]["cenarios"][2]["favoravel"] is False and p["ressalvas"]
    p.pop("ressalvas")
    erros = validar(p)
    assert any("conta.cenarios[2].favoravel=false exige `ressalvas`" in e for e in erros)
    p["ressalvas"] = ["O cenário C3 não apura excesso: os juros cobrados são mantidos nele."]
    assert validar(p) == []
    assert "Desfavorável" in relatorios.render_premium(p)


def test_extracao_adulterada_e_recusada_antes_de_virar_laudo():
    linhas = list(LINHAS)
    linhas[2] = "2021-03-31;JUROS COBRADOS;D;95,00;ENCARGO;juros;;-1.200,00"       # saldo impresso não bate
    reconciliacao, trinca = apurar(linhas)
    assert reconciliacao["veredito"] == "DIVERGENTE"
    erros = validar(payload_de(reconciliacao, trinca))
    assert any("conta.reconciliacao.veredito (DIVERGENTE" in e and "lacuna bloqueante" in e for e in erros)
    assert any("conta.reconciliacao.divergencias" in e for e in erros)       # as duas travas apontam o defeito


def test_competencia_sem_lancamento_e_recusada():
    reconciliacao, trinca = apurar([l for l in LINHAS if "2021-04" not in l])
    assert reconciliacao["competencias_sem_lancamento"] == ["2021-04"]
    assert any("competencias_sem_lancamento" in e and "extrato faltante" in e
               for e in validar(payload_de(reconciliacao, trinca)))


def test_lider_omitido_pelo_motor_e_recusado_mas_o_bloco_e_montado():
    reconciliacao, trinca = apurar(taxa_contratada=None)
    assert trinca[1]["omitido"] is True
    p = payload_de(reconciliacao, trinca, lider="C2_CAP_MENSAL")
    assert p["conta"]["cenarios"][1] == {"cenario": "C2_CAP_MENSAL", "omitido": True, "motivo": trinca[1]["motivo"]}
    assert any("foi omitido e não pode ser o líder" in e for e in validar(p))
    p["conta"]["cenario_lider"] = "C1_TAXA_MEDIA"
    p["conta"]["encontro"] = cc.encontro_de_contas(trinca[0])
    assert validar(p) == []                                              # com o líder certo, o cenário omitido segue declarado
    html = relatorios.render_premium(p)
    assert "Omitido." in html and trinca[1]["motivo"].split(": ", 1)[1] in html


def test_cenario_desfavoravel_do_motor_e_reportado_nao_escondido():
    reconciliacao, trinca = apurar(taxa_contratada=0.02, media=0.15)     # média acima da contratada
    assert trinca[0]["favoravel"] is False and trinca[0]["excesso_final"] < 0
    p = payload_de(reconciliacao, trinca)
    assert validar(p) == []                                              # há ressalvas no payload de teste
    premium, panorama = relatorios.render_premium(p), relatorios.render_panorama(p)
    assert "Desfavorável" in premium and '<div class="cx ok"><b>Veredito.</b>' in panorama
    assert "(negativo)" in panorama                                      # a barra do cenário não vira largura negativa
    p.pop("ressalvas")
    assert any("favoravel=false exige `ressalvas`" in e for e in validar(p))


def test_correcao_do_conector_e_opcional_e_so_numero_valido():
    reconciliacao, trinca = apurar()
    sem = payload_de(reconciliacao, trinca)
    assert "correcao" not in sem["conta"] and "Correção do indébito" not in relatorios.render_premium(sem)
    com = payload_de(reconciliacao, trinca, correcao={"valor_corrigido": 1234.5, "data_final": "2024-06-28",
                                                      "indice": "IPCA + taxa legal", "hash": "abc123"})
    assert validar(com) == [] and "R$ 1.234,50" in relatorios.render_premium(com)
    com["conta"]["correcao"]["valor_corrigido"] = "1.234,50"
    assert any("conta.correcao.valor_corrigido" in e for e in validar(com))


def test_series_vazia_e_aviso_nao_erro(motor):
    p = payload_de(*motor)
    p["conta"]["series"] = []
    v = validar_detalhado(p)
    assert v["erros"] == [] and any("conta.series vazia" in a for a in v["avisos"])
    assert "Nenhuma série externa foi declarada" in relatorios.render_premium(p)


def test_reconciliacao_sem_pontos_conferidos_avisa():
    reconciliacao, trinca = apurar([l.rsplit(";", 1)[0] + ";" for l in LINHAS])       # sem saldo_informado
    assert reconciliacao["veredito"] == "CONFORME" and reconciliacao["pontos_conferidos"] == 0
    v = validar_detalhado(payload_de(reconciliacao, trinca))
    assert v["erros"] == [] and any("pontos_conferidos=0" in a for a in v["avisos"])


def test_so_o_laudo_e_a_planilha_dispensam_o_panorama_no_ramo_conta(motor, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    p = payload_de(*motor)
    p.pop("panorama")
    assert validar(p, {"premium", "planilha"}) == [] and "panorama" in validar(p)
    arquivos = relatorios.gerar(p, tmp_path, formatos={"premium", "planilha"})
    assert sorted(a.suffix for a in arquivos) == [".html", ".md", ".xlsx"]
    assert openpyxl.load_workbook(tmp_path / "planilha-demo-conta.xlsx").sheetnames[0] == "Dashboard"


def test_conta_com_panorama_do_instrumento_no_payload_ainda_gera(motor):
    """Payload convertido do ramo instrumento, com `selo` e `barras` sobrando: o ramo conta os ignora."""
    p = payload_de(*motor)
    p["panorama"].update(selo="Texto do selo antigo.", barras=[{"rotulo": "x", "valor": 1.0}])
    html = relatorios.render_panorama(p)
    rodados = sum(1 for c in p["conta"]["cenarios"] if not c.get("omitido"))
    assert "Texto do selo antigo." in html and ">x —" not in html and html.count('class="barra"') == rodados == 3
    p["panorama"]["barras"] = "não é lista"
    assert validar(p) == []


def test_a_trinca_do_payload_demo_usa_os_rotulos_do_dicionario():
    html = relatorios.render_premium(relatorios._payload_demo_conta())
    assert all(rotulo in html for rotulo in ROTULOS_CENARIOS.values())
    assert relatorios.rotulo_cenario("C9_FUTURO") == "C9_FUTURO"


def test_conta_com_tema_sai_com_a_identidade_do_escritorio(motor, tmp_path):
    p = payload_de(*motor)
    tema = {"cores": {"destaque": "#0A5C8A", "fundo_destaque": "#EEF6FB"}, "rodape": "Uso restrito do escritório"}
    relatorios.gerar(p, tmp_path, formatos={"premium", "panorama"}, tema=tema)
    for nome in ("laudo-premium-demo-conta.html", "panorama-estrategico-demo-conta.html"):
        html = (tmp_path / nome).read_text(encoding="utf-8")
        assert "--gold:#0A5C8A" in html and "Uso restrito do escritório" in html and ADVERTENCIA_CONTA in html
