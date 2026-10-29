"""Identidade visual (`motores/tema.py`) e o que o renderizador faz com ela: esquema fechado,
logo, gravação na pasta de configuração, HTML sem tema idêntico ao de antes (byte a byte) e
cores do semáforo que nunca mudam.

Nenhum nome, OAB ou logo real: só o que o plugin traz de exemplo. Nada escreve fora de `tmp_path`."""
import base64
import hashlib
import json

import pytest

from conftest import PNG_1X1 as PNG
from motores import relatorios, tema

# SHA-256 do HTML que o plugin gerava ANTES de existir tema, para o payload sintético de
# `relatorios._payload_demo()`, e das constantes do chassi. Se uma mudança de visual for
# intencional, imprima os novos valores com `hashlib.sha256(texto.encode("utf-8")).hexdigest()`.
HASH_PREMIUM = "4306f2c09491c7bfb09c631601acf2cdc4815b6b688ea61d2562f2607f1ad96b"   # v6.1: contagem inteira sem casas (antes "1,00")
HASH_PANORAMA = "4df54aba3b2df5d832d298666d95fc92997dcf7207b3aa18e54b8f59d339ce1b"
HASH_CSS = "a5684966a91115ef03a2d294a1fe1b250e14cf00c5363b308d060bc125829c8e"
HASH_FONTES = "6d55a7d1da49168d2a5f3297e76733c3a1ebec35ed591bd50d261d119d4eb2a5"

SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10"/></svg>'
URL = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Lato:wght@300;400&display=swap"
AZUL = {"nome": "Identidade do escritório", "skill_origem": "skill-de-layout-exemplo",
        "cores": {"tinta": "#12263F", "destaque": "#0A5C8A", "destaque_claro": "#BCE0F5", "fundo_destaque": "#EEF6FB"},
        "fontes": {"titulo": "Playfair Display", "texto": "Lato"}, "fontes_url": URL,
        "cabecalho_linha": "Rua Exemplo, 100 — Cidade-UF", "rodape": "Uso restrito do escritório"}


def sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


@pytest.fixture
def payload():
    return relatorios._payload_demo()


@pytest.fixture(autouse=True)
def ambiente_limpo(monkeypatch):
    for var in ("REVISAO_BANCARIA_CONFIG_DIR", "CLAUDE_PLUGIN_DATA"):
        monkeypatch.delenv(var, raising=False)


def logo(tmp_path, nome="logo.png", conteudo=PNG):
    arquivo = tmp_path / nome
    arquivo.write_bytes(conteudo if isinstance(conteudo, bytes) else conteudo.encode("utf-8"))
    return arquivo


# ── sem tema, nada muda ───────────────────────────────────────────────

def test_html_sem_tema_e_o_de_antes_byte_a_byte(payload):
    premium, panorama = relatorios.render_premium(payload), relatorios.render_panorama(payload)
    assert sha(premium) == HASH_PREMIUM and sha(panorama) == HASH_PANORAMA
    assert sha(relatorios.CSS) == HASH_CSS and sha(relatorios.FONTES) == HASH_FONTES
    assert relatorios.render_premium(payload, tema=None) == premium
    assert relatorios.render_panorama(payload, None) == panorama


def test_tema_padrao_e_tema_vazio_desenham_o_mesmo_html_de_antes(payload):
    premium, panorama = relatorios.render_premium(payload), relatorios.render_panorama(payload)
    for igual_ao_padrao in (tema.PADRAO, {}, {"cores": dict(tema.PADRAO["cores"])}, {"nome": "Só o nome"}):
        assert relatorios.render_premium(payload, igual_ao_padrao) == premium
        assert relatorios.render_panorama(payload, igual_ao_padrao) == panorama


def test_padrao_descreve_o_visual_atual_e_e_idempotente():
    assert tema.validar(tema.PADRAO) == (tema.PADRAO, [])
    assert tema.PADRAO["cores"] == {"tinta": "#1A1714", "destaque": "#B08A4E", "destaque_claro": "#EDE0B8",
                                    "fundo_destaque": "#FAF7EF"}
    for chave, cor in (("ink", "#1A1714"), ("gold", "#B08A4E"), ("glt", "#EDE0B8"), ("gpale", "#FAF7EF")):
        assert f"--{chave}:{cor}" in relatorios.CSS
    assert tema.FONTES_URL_PADRAO in relatorios.FONTES.replace("&amp;", "&")
    assert tema.PADRAO["rodape"] == "Documento confidencial"
    novo, avisos = tema.validar(AZUL)
    assert tema.validar(novo) == (novo, avisos)


# ── esquema fechado ───────────────────────────────────────────────────

def test_normaliza_completa_com_o_padrao_e_aceita_so_o_que_veio():
    normal, avisos = tema.validar({"nome": "  Meu   tema ", "cores": {"destaque": " #0a5c8a "}})
    assert normal == {"nome": "Meu tema", "cores": {**tema.PADRAO["cores"], "destaque": "#0A5C8A"},
                      "fontes": tema.PADRAO["fontes"]}
    assert avisos == []
    assert tema.validar({})[0]["nome"] == "Personalizado"
    assert tema.validar({"logo": None, "rodape": "", "fontes_url": None, "cabecalho_linha": "  "})[0].keys() \
        == {"nome", "cores", "fontes"}


@pytest.mark.parametrize("dados,trecho", [
    ({"cor": "#000000"}, "chave desconhecida no tema: cor"),
    ({"cores": {"texto": "#000000"}}, "chave desconhecida em cores: texto"),
    ({"fontes": {"corpo": "Lato"}}, "chave desconhecida em fontes: corpo"),
    ({"cores": {"tinta": "preto"}}, "cores.tinta"),
    ({"cores": {"tinta": "#FFF"}}, "cores.tinta"),
    ({"cores": {"destaque": "#GG0000"}}, "cores.destaque"),
    ({"cores": {"destaque": 255}}, "cores.destaque"),
    ({"cores": ["#000000"]}, "cores deve ser um objeto"),
    ({"fontes": {"titulo": "Arial';}</style><script>"}}, "fontes.titulo"),
    ({"fontes": {"texto": "x" * 41}}, "fontes.texto"),
    ({"fontes": {"mono": "Fira_Code"}}, "fontes.mono"),
    ({"fontes_url": "http://fonts.googleapis.com/css2?family=Lato"}, "fontes_url"),
    ({"fontes_url": "https://exemplo.com/css2?family=Lato"}, "fontes_url"),
    ({"fontes_url": "https://fonts.googleapis.com/css?family=Lato"}, "fontes_url"),
    ({"fontes_url": "https://fonts.googleapis.com/css2?family=Lato\" onload=\"x"}, "fontes_url"),
    ({"nome": 7}, "nome deve ser texto"),
    ({"nome": "x" * 81}, "nome com 81 caracteres"),
    ({"rodape": "x" * 121}, "rodape com 121 caracteres"),
    ({"cabecalho_linha": ["a"]}, "cabecalho_linha deve ser texto"),
])
def test_esquema_recusa(dados, trecho):
    with pytest.raises(ValueError, match=trecho):
        tema.validar(dados)


def test_tema_que_nao_e_objeto_e_recusado():
    for ruim in ([], "azul", 3, None):
        with pytest.raises(ValueError, match="objeto JSON"):
            tema.validar(ruim)


def test_atualizado_em_e_aceito_para_regravar_o_que_foi_lido():
    assert "atualizado_em" not in tema.validar({"atualizado_em": "2026-10-27T10:00:00"})[0]


# ── avisos ────────────────────────────────────────────────────────────

def test_fonte_do_tema_sem_url_avisa():
    avisos = tema.validar({"fontes": {"titulo": "Playfair Display", "texto": "Lato"}})[1]
    assert len(avisos) == 1 and "Lato, Playfair Display" in avisos[0] and "fontes_url" in avisos[0]
    assert tema.validar({"fontes": {"titulo": "Playfair Display"}, "fontes_url": URL})[1] == []
    assert tema.validar({"fontes": {"titulo": "DM Sans", "texto": "Space Grotesk"}})[1] == []


def test_tinta_que_nao_contrasta_avisa():
    avisos = tema.validar({"cores": {"tinta": "#CCCCCC"}})[1]
    assert len(avisos) == 2 and "papel branco" in avisos[0] and "fundo_destaque" in avisos[1]
    assert tema.validar({"cores": {"tinta": "#12263F"}})[1] == []
    assert tema.contraste("#000000", "#FFFFFF") == pytest.approx(21.0)
    assert tema.contraste("#FFFFFF", "#FFFFFF") == pytest.approx(1.0)


def test_texto_das_faixas_e_o_destaque_escurecido_e_legivel():
    assert tema.cor_texto_destaque("#B08A4E", "#FAF7EF") == "#7A5F10"                # o do plugin
    for destaque, fundo in (("#0A5C8A", "#EEF6FB"), ("#F2A900", "#FFF8E5"), ("#E0E0E0", "#FFFFFF")):
        cor = tema.cor_texto_destaque(destaque, fundo)
        assert tema.contraste(cor, fundo) >= tema.CONTRASTE_MINIMO
    assert tema.argb("#0a5c8a") == "FF0A5C8A"


# ── logo ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("nome,tipo", [("a.png", "image/png"), ("a.JPG", "image/jpeg"),
                                       ("a.jpeg", "image/jpeg"), ("a.svg", "image/svg+xml")])
def test_logo_aceito_vira_data_uri(tmp_path, nome, tipo):
    conteudo = SVG if nome.endswith("svg") else PNG
    normal, _ = tema.validar({"logo": str(logo(tmp_path, nome, conteudo))})
    uri = tema.logo_data_uri(normal)
    assert uri.startswith(f"data:{tipo};base64,")
    assert base64.b64decode(uri.split(",", 1)[1]) == (SVG.encode("utf-8") if nome.endswith("svg") else PNG)


def test_logo_que_some_entre_a_validacao_e_o_desenho_e_valueerror(tmp_path):
    arquivo = logo(tmp_path)
    normal, _ = tema.validar({"logo": str(arquivo)})
    arquivo.unlink()
    with pytest.raises(ValueError, match="não foi possível ler o logo"):
        tema.logo_data_uri(normal)


def test_logo_relativo_e_resolvido_pela_base(tmp_path):
    logo(tmp_path, "marca.png")
    assert tema.validar({"logo": "marca.png"}, base=tmp_path)[0]["logo"] == str((tmp_path / "marca.png").resolve())


@pytest.mark.parametrize("nome,conteudo,trecho", [
    ("a.gif", PNG, "extensão .gif não aceita"),
    ("a.webp", PNG, "extensão .webp não aceita"),
    ("a", PNG, "extensão \\(nenhuma\\)"),
    ("vazio.png", b"", "está vazio"),
    ("a.svg", b"\xff\xfe<\x00s\x00v\x00g\x00", "UTF-8"),
])
def test_logo_recusado(tmp_path, nome, conteudo, trecho):
    with pytest.raises(ValueError, match=trecho):
        tema.validar({"logo": str(logo(tmp_path, nome, conteudo))})


def test_logo_ausente_e_recusado(tmp_path):
    with pytest.raises(ValueError, match="logo não encontrado"):
        tema.validar({"logo": str(tmp_path / "nao-existe.png")})
    with pytest.raises(ValueError, match="logo deve ser o caminho"):
        tema.validar({"logo": 5})


def test_logo_limite_de_300_kb(tmp_path):
    assert tema.LOGO_MAX_BYTES == 300 * 1024
    tema.validar({"logo": str(logo(tmp_path, "no-limite.png", b"0" * tema.LOGO_MAX_BYTES))})
    with pytest.raises(ValueError, match="o limite é 300 KB"):
        tema.validar({"logo": str(logo(tmp_path, "grande.png", b"0" * (tema.LOGO_MAX_BYTES + 1)))})


@pytest.mark.parametrize("svg", [
    '<svg><script>alert(1)</script></svg>', '<svg><SCRIPT src="x"/></svg>',
    '<svg onload="alert(1)"/>', '<svg ONLOAD = "x"/>', "<svg><a onclick='x()'/></svg>",
    '<svg xmlns="http://www.w3.org/2000/svg"onload="x()"/>', '<svg/onload=alert(1)>'])
def test_svg_com_script_ou_evento_e_recusado(tmp_path, svg):
    with pytest.raises(ValueError, match="conteúdo ativo"):
        tema.validar({"logo": str(logo(tmp_path, "a.svg", svg))})


@pytest.mark.parametrize("svg", [
    SVG, '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" patternContentUnits="userSpaceOnUse"/>',
    '<svg xmlns:xlink="http://www.w3.org/1999/xlink"><title>Conteúdo e ação</title></svg>'])
def test_svg_simples_nao_e_confundido_com_evento(tmp_path, svg):
    assert tema.validar({"logo": str(logo(tmp_path, "a.svg", svg))})[0]["logo"].endswith("a.svg")


# ── gravar, ler, remover ──────────────────────────────────────────────

def test_ler_sem_arquivo_devolve_none(tmp_path):
    assert tema.ler(tmp_path) is None and tema.carregar(tmp_path) == (None, [])
    assert tema.remover(tmp_path / "nada") is False


def test_salvar_e_ler_na_pasta_do_operador(tmp_path):
    arquivo, avisos = tema.salvar(AZUL, tmp_path / "cfg")
    assert arquivo == tmp_path / "cfg" / "tema.json" and avisos == []
    bruto = arquivo.read_bytes()
    assert b"\r\n" not in bruto and "Rua Exemplo, 100 — Cidade-UF".encode("utf-8") in bruto and b"\\u" not in bruto
    lido = tema.ler(tmp_path / "cfg")
    assert {k: v for k, v in lido.items() if k != "atualizado_em"} == tema.validar(AZUL)[0]
    assert tema.carregar(tmp_path / "cfg")[0] == tema.validar(AZUL)[0]


def test_salvar_usa_a_mesma_pasta_do_operador(monkeypatch, tmp_path):
    monkeypatch.setenv("REVISAO_BANCARIA_CONFIG_DIR", str(tmp_path / "env"))
    assert tema.salvar({"nome": "x"})[0] == tmp_path / "env" / "tema.json"
    monkeypatch.delenv("REVISAO_BANCARIA_CONFIG_DIR")
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "dados"))
    assert tema.salvar({"nome": "x"})[0] == tmp_path / "dados" / "tema.json"


def test_tema_invalido_nao_grava_nada(tmp_path):
    with pytest.raises(ValueError):
        tema.salvar({"cores": {"tinta": "preto"}}, tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_salvar_copia_o_logo_para_a_pasta_e_guarda_so_o_nome(tmp_path):
    assets = tmp_path / "skill-de-layout" / "assets"
    assets.mkdir(parents=True)
    origem = logo(assets, "logo-original.PNG")
    cfg = tmp_path / "cfg"
    arquivo, _ = tema.salvar({**AZUL, "logo": str(origem)}, cfg)
    assert json.loads(arquivo.read_text(encoding="utf-8"))["logo"] == "tema-logo.png"
    assert (cfg / "tema-logo.png").read_bytes() == PNG
    origem.unlink()                                       # a skill de origem mudou de lugar: o tema segue de pé
    lido = tema.ler(cfg)
    assert lido["logo"] == str(cfg / "tema-logo.png")
    assert tema.logo_data_uri(tema.carregar(cfg)[0]).startswith("data:image/png;base64,")


def test_salvar_logo_relativo_usa_a_base_e_trocar_de_formato_apaga_o_antigo(tmp_path):
    cfg = tmp_path / "cfg"
    logo(tmp_path, "marca.png")
    tema.salvar({"logo": "marca.png"}, cfg, base=tmp_path)
    assert (cfg / "tema-logo.png").is_file()
    logo(tmp_path, "marca.svg", SVG)
    tema.salvar({"logo": "marca.svg"}, cfg, base=tmp_path)
    assert (cfg / "tema-logo.svg").is_file() and not (cfg / "tema-logo.png").exists()
    tema.salvar({"nome": "sem logo"}, cfg)
    assert not any(cfg.glob("tema-logo.*")) and "logo" not in tema.ler(cfg)


def test_salvar_aceita_o_que_ler_devolveu(tmp_path):
    cfg = tmp_path / "cfg"
    tema.salvar({**AZUL, "logo": str(logo(tmp_path))}, cfg)
    tema.salvar(tema.ler(cfg), cfg)                       # logo volta absoluto, atualizado_em é descartado
    assert (cfg / "tema-logo.png").read_bytes() == PNG
    assert tema.carregar(cfg)[0]["nome"] == AZUL["nome"]


def test_remover_apaga_tema_e_logo_e_so_eles(tmp_path):
    cfg = tmp_path / "cfg"
    tema.salvar({"logo": str(logo(tmp_path))}, cfg)
    (cfg / "operador.json").write_text("{}", encoding="utf-8")
    (cfg / "logo.png").write_bytes(PNG)                   # arquivo do usuário, não do tema
    assert tema.remover(cfg) is True
    assert sorted(p.name for p in cfg.iterdir()) == ["logo.png", "operador.json"]
    assert tema.remover(cfg) is False and tema.ler(cfg) is None


def test_ler_arquivo_invalido_levanta(tmp_path):
    (tmp_path / "tema.json").write_text("{ quebrado", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON válido"):
        tema.ler(tmp_path)
    (tmp_path / "tema.json").write_text("[1]", encoding="utf-8")
    with pytest.raises(ValueError, match="objeto"):
        tema.ler(tmp_path)


def test_ler_aceita_bom_e_tema_gravado_com_logo_que_sumiu_falha_ao_carregar(tmp_path):
    (tmp_path / "tema.json").write_bytes(b"\xef\xbb\xbf" + json.dumps({"nome": "x", "logo": "tema-logo.png"}).encode())
    assert tema.ler(tmp_path)["logo"] == str(tmp_path / "tema-logo.png")
    with pytest.raises(ValueError, match="logo não encontrado"):
        tema.carregar(tmp_path)


# ── HTML com tema ─────────────────────────────────────────────────────

def test_cores_e_fontes_do_tema_entram_no_css_e_o_semaforo_nao_muda(payload):
    for html in (relatorios.render_premium(payload, AZUL), relatorios.render_panorama(payload, AZUL)):
        assert "--ink:#12263F;--gold:#0A5C8A;--glt:#BCE0F5;--gpale:#EEF6FB;" in html
        assert "--red:#A62B2B" in html and "--rbg:#FCF3F3" in html and "--grn:#2F6B45" in html
        assert "--gbg:#F2F8F4" in html and "--amb:#8A6A1F" in html and "--abg:#FDF8EC" in html
        for antigo in ("#1A1714", "#B08A4E", "#EDE0B8", "#FAF7EF", "#7A5F10", "DM Sans", "Space Grotesk"):
            assert antigo not in html, antigo
        assert ".doc{font-family:'Lato',-apple-system,Segoe UI,sans-serif" in html
        assert "h1{font-family:'Playfair Display',sans-serif" in html
        assert "'JetBrains Mono',Consolas,monospace" in html          # mono não foi trocada
        assert "color:" + tema.cor_texto_destaque("#0A5C8A", "#EEF6FB") in html


def test_trocar_as_familias_nao_encadeia(payload):
    """texto='Space Grotesk' e titulo='Playfair Display': a troca de uma não pode contaminar a outra."""
    html = relatorios.render_premium(payload, {"fontes": {"texto": "Space Grotesk", "titulo": "Playfair Display"},
                                               "fontes_url": URL})
    assert ".doc{font-family:'Space Grotesk',-apple-system,Segoe UI,sans-serif" in html
    assert "h1{font-family:'Playfair Display',sans-serif" in html and "'DM Sans'" not in html


def test_link_de_fontes_segue_o_que_o_tema_usa(payload):
    padrao = relatorios.render_premium(payload)
    assert relatorios.FONTES in padrao
    com_url = relatorios.render_premium(payload, AZUL)
    assert relatorios.FONTES not in com_url and "family=Playfair+Display:wght@500;600&amp;family=Lato" in com_url
    assert 'rel="preconnect" href="https://fonts.gstatic.com" crossorigin' in com_url
    # fonte própria sem fontes_url: nenhum link do Google das fontes padrão para ela
    sem_url = relatorios.render_premium(payload, {"fontes": {"titulo": "Playfair Display", "texto": "Lato",
                                                             "mono": "Courier Prime"}})
    assert "fonts.googleapis.com" not in sem_url and "family=" not in sem_url
    # só a de título é do tema: o link cobre as outras duas famílias padrão, e só elas
    parcial = relatorios.render_premium(payload, {"fontes": {"titulo": "Playfair Display"}})
    assert "family=DM+Sans" in parcial and "family=JetBrains+Mono" in parcial and "Space+Grotesk" not in parcial
    # só as cores mudam: o link padrão, inteiro
    so_cores = relatorios.render_premium(payload, {"cores": {"destaque": "#0A5C8A"}})
    assert relatorios.FONTES in so_cores


def test_cabecalho_e_rodape_do_tema(payload, tmp_path):
    html = relatorios.render_premium(payload, {**AZUL, "logo": str(logo(tmp_path))})
    assert html.index('<img class="logo" src="data:image/png;base64,') < html.index('<div class="marca">')
    assert '<div class="linha">Rua Exemplo, 100 — Cidade-UF</div>' in html
    assert ".logo{display:block;max-height:14mm" in html and "Uso restrito do escritório" in html
    assert "Documento confidencial" not in html and 'alt=""' in html
    sem = relatorios.render_premium(payload, {"cores": {"destaque": "#0A5C8A"}})
    assert 'class="logo"' not in sem and 'class="linha"' not in sem and ".logo{" not in sem
    assert "Documento confidencial" in sem


def test_textos_do_tema_passam_por_esc(payload):
    html = relatorios.render_panorama(payload, {"cabecalho_linha": "A & B <i>x</i>", "rodape": "<script>x</script>"})
    assert "A &amp; B &lt;i&gt;x&lt;/i&gt;" in html and "&lt;script&gt;x&lt;/script&gt;" in html
    assert "<script>" not in html and "<i>x</i>" not in html


def test_logo_so_do_tema_nao_do_payload(payload, tmp_path):
    """`marca.logo` do payload, que ninguém lê, não vira imagem: o logo é do tema."""
    payload["marca"]["logo"] = str(logo(tmp_path))
    assert "<img" not in relatorios.render_premium(payload)


def test_barras_sem_cor_usam_o_destaque_do_tema(payload):
    payload["panorama"]["barras"] = [{"rotulo": "Sem cor", "valor": 10}, {"rotulo": "Com cor", "valor": 5, "cor": "#2a78d6"}]
    com_tema = relatorios.render_panorama(payload, AZUL)
    assert "background:#0A5C8A" in com_tema and "background:#2a78d6" in com_tema
    assert "background:#B08A4E" in relatorios.render_panorama(payload)


def test_tema_invalido_recusa_antes_de_escrever(payload, tmp_path):
    with pytest.raises(ValueError, match="cores.tinta"):
        relatorios.gerar(payload, tmp_path / "saida", formatos={"premium"}, tema={"cores": {"tinta": "x"}})
    assert not (tmp_path / "saida").exists()


def test_gerar_com_tema_escreve_o_html_do_tema(payload, tmp_path, capsys):
    arquivos = relatorios.gerar(payload, tmp_path / "saida", formatos={"premium", "panorama"},
                                tema={"fontes": {"titulo": "Playfair Display"}})
    html = (tmp_path / "saida" / "laudo-premium-demo.html").read_text(encoding="utf-8")
    assert "'Playfair Display'" in html and len(arquivos) == 3
    assert "aviso: tema: fonte(s) Playfair Display sem fontes_url" in capsys.readouterr().err


# ── planilha ──────────────────────────────────────────────────────────

def _celula(ws, texto):
    return next(c for linha in ws.iter_rows() for c in linha if c.value == texto)


def test_planilha_usa_cores_do_tema_nas_faixas_e_cabecalhos(payload, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    relatorios.render_planilha(payload, tmp_path / "azul.xlsx", AZUL)
    ws = openpyxl.load_workbook(tmp_path / "azul.xlsx")["Dashboard"]
    faixa, cab = _celula(ws, "IDENTIFICAÇÃO DA OPERAÇÃO"), _celula(ws, "Premissa de evolução do débito")
    assert faixa.fill.fgColor.rgb == "FFEEF6FB" and cab.fill.fgColor.rgb == "FF12263F"
    assert faixa.font.color.rgb == tema.argb(tema.cor_texto_destaque("#0A5C8A", "#EEF6FB"))
    assert faixa.border.bottom.color.rgb == "FF0A5C8A"
    # as cores do semáforo da planilha não são do tema
    achado = _celula(ws, "Ilícito")
    assert achado.fill.fgColor.rgb == "FFFCF3F3" and achado.font.color.rgb == "FFA62B2B"


def test_planilha_sem_tema_ou_com_o_padrao_mantem_as_cores_de_antes(payload, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    for nome, tema_usado in (("sem", None), ("padrao", tema.PADRAO)):
        relatorios.render_planilha(payload, tmp_path / f"{nome}.xlsx", tema_usado)
        ws = openpyxl.load_workbook(tmp_path / f"{nome}.xlsx")["Dashboard"]
        faixa, cab = _celula(ws, "IDENTIFICAÇÃO DA OPERAÇÃO"), _celula(ws, "Premissa de evolução do débito")
        assert (faixa.fill.fgColor.rgb, faixa.font.color.rgb, cab.fill.fgColor.rgb) == (
            "FFFAF7EF", "FF7A5F10", "FF1A1A1A")
        assert faixa.border.bottom.color.rgb == "FFB8952E"
