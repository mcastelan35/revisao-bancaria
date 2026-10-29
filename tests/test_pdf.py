"""PDF dos entregáveis (`motores/pdf.py`): busca do navegador, conversão com o navegador SIMULADO
(`subprocess.run` trocado por um falso que grava o PDF), os três modos do `gerar` e, quando há
Chrome, Edge, Chromium ou Brave instalado, uma conversão de verdade.

Os testes simulados não dependem de haver navegador na máquina e nada escreve fora de `tmp_path`."""
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from motores import pdf, relatorios

MOTIVO = "nenhum navegador Chromium encontrado — abra o HTML e salve como PDF"


def pdf_falso(paginas: int = 1) -> bytes:
    objetos = "".join(f"{n + 2} 0 obj << /Type /Page /Parent 1 0 R >> endobj\n" for n in range(paginas))
    return (f"%PDF-1.4\n1 0 obj << /Type /Pages /Count {paginas} >> endobj\n{objetos}%%EOF\n").encode("ascii")


class Navegador:
    """Faz o papel do `subprocess.run`: grava o PDF que o navegador gravaria e anota as chamadas.
    `paginas` pode ser um número ou um dict {nome do pdf: páginas}; `codigo` é o do processo."""

    def __init__(self, paginas=1, codigo=0, grava=True, conteudo=None, falha=None, relato=None):
        self.paginas, self.codigo, self.grava, self.conteudo, self.falha = paginas, codigo, grava, conteudo, falha
        self.relato = relato                              # o que o navegador escreveria na saída
        self.chamadas, self.perfil_existia, self.perfis = [], [], []

    def __call__(self, comando, **kwargs):
        self.chamadas.append((list(comando), kwargs))
        destino = Path(next(a.split("=", 1)[1] for a in comando if a.startswith("--print-to-pdf=")))
        perfil = Path(next(a.split("=", 1)[1] for a in comando if a.startswith("--user-data-dir=")))
        self.perfil_existia.append(perfil.is_dir())
        self.perfis.append(perfil)
        if self.relato and kwargs.get("stdout") not in (None, subprocess.PIPE):
            kwargs["stdout"].write(self.relato)
        if self.falha:
            raise self.falha
        paginas = self.paginas.get(destino.name, 1) if isinstance(self.paginas, dict) else self.paginas
        if self.grava:
            destino.write_bytes(self.conteudo if self.conteudo is not None else pdf_falso(paginas))
        return subprocess.CompletedProcess(comando, self.codigo, b"", b"")


@pytest.fixture
def rapido(monkeypatch):
    """Espera curta: o teste que depende do prazo não demora o prazo real."""
    monkeypatch.setattr(pdf, "TIMEOUT", 0.6)
    monkeypatch.setattr(pdf, "INTERVALO", 0.02)


@pytest.fixture
def htmls(tmp_path):
    pasta = tmp_path / "saida"
    pasta.mkdir()
    nomes = ("laudo-premium-x.html", "panorama-estrategico-x.html")
    for nome in nomes:
        (pasta / nome).write_text("<html><body>x</body></html>", encoding="utf-8")
    (pasta / "planilha-x.xlsx").write_bytes(b"PK")
    (pasta / "INTERNO-agenda-pesquisa-x.md").write_text("# x", encoding="utf-8")
    return pasta


def arquivos(pasta):
    return [pasta / n for n in ("laudo-premium-x.html", "INTERNO-agenda-pesquisa-x.md",
                                "panorama-estrategico-x.html", "planilha-x.xlsx")]


# ── busca do navegador ────────────────────────────────────────────────

def test_caminhos_padrao_do_windows():
    env = {"ProgramFiles": r"C:\PF", "ProgramFiles(x86)": r"C:\PF86", "LOCALAPPDATA": r"C:\Local"}
    caminhos = pdf.caminhos_padrao("win32", env)
    assert [c.parts[-4:] for c in caminhos] == [
        ("Google", "Chrome", "Application", "chrome.exe")] * 3 + [("Microsoft", "Edge", "Application", "msedge.exe")] * 3
    bases = (r"C:\PF86", r"C:\PF", r"C:\Local")                 # a mais longa primeiro: C:\PF86 começa com C:\PF
    assert [next(b for b in bases if str(c).startswith(b)) for c in caminhos[:3]] == [r"C:\PF", r"C:\PF86", r"C:\Local"]
    assert len(pdf.caminhos_padrao("win32", {"LOCALAPPDATA": r"C:\Local"})) == 2        # só o que existe no ambiente
    assert pdf.caminhos_padrao("win32", {}) == []


def test_caminhos_padrao_do_macos_e_do_linux():
    mac = [str(c) for c in pdf.caminhos_padrao("darwin")]
    assert any("Google Chrome.app" in c for c in mac) and any("Microsoft Edge.app" in c for c in mac)
    assert all(Path(c).parts[1] == "Applications" for c in mac)
    assert pdf.caminhos_padrao("linux") == []


def test_navegador_da_variavel_de_ambiente_vence(monkeypatch, tmp_path):
    falso = tmp_path / "meu-navegador"
    falso.write_text("", encoding="utf-8")
    monkeypatch.setenv(pdf.ENV_NAVEGADOR, str(falso))
    monkeypatch.setattr(pdf.shutil, "which", lambda nome: f"/usr/bin/{nome}")
    assert pdf.achar_navegador() == str(falso)


def test_variavel_de_ambiente_pode_ser_um_nome_do_path(monkeypatch):
    monkeypatch.setenv(pdf.ENV_NAVEGADOR, "meu-chrome")
    monkeypatch.setattr(pdf.shutil, "which", lambda nome: "/opt/bin/meu-chrome" if nome == "meu-chrome" else None)
    assert pdf.achar_navegador() == "/opt/bin/meu-chrome"


def test_variavel_invalida_cai_para_a_busca_normal(monkeypatch, tmp_path):
    monkeypatch.setenv(pdf.ENV_NAVEGADOR, str(tmp_path / "nao-existe"))
    monkeypatch.setattr(pdf.shutil, "which", lambda nome: "/usr/bin/chromium" if nome == "chromium" else None)
    assert pdf.achar_navegador() == "/usr/bin/chromium"


def test_which_segue_a_ordem_da_lista(monkeypatch):
    monkeypatch.delenv(pdf.ENV_NAVEGADOR, raising=False)
    assert pdf.EXECUTAVEIS == ("chrome", "google-chrome", "google-chrome-stable", "chromium",
                               "chromium-browser", "msedge", "microsoft-edge", "brave")
    presentes = {"brave", "msedge", "google-chrome"}
    monkeypatch.setattr(pdf.shutil, "which", lambda nome: f"/bin/{nome}" if nome in presentes else None)
    assert pdf.achar_navegador() == "/bin/google-chrome"
    presentes.discard("google-chrome")
    assert pdf.achar_navegador() == "/bin/msedge"


def test_cai_nos_caminhos_padrao_e_sem_nada_devolve_none(monkeypatch, tmp_path):
    monkeypatch.delenv(pdf.ENV_NAVEGADOR, raising=False)
    monkeypatch.setattr(pdf.shutil, "which", lambda nome: None)
    instalado = tmp_path / "Application" / "chrome.exe"
    instalado.parent.mkdir()
    instalado.write_text("", encoding="utf-8")
    monkeypatch.setattr(pdf, "caminhos_padrao", lambda: [tmp_path / "x" / "chrome.exe", instalado])
    assert pdf.achar_navegador() == str(instalado)
    monkeypatch.setattr(pdf, "caminhos_padrao", lambda: [tmp_path / "x" / "chrome.exe"])
    assert pdf.achar_navegador() is None


# ── conversão de um arquivo ───────────────────────────────────────────

def test_converter_monta_o_comando_e_devolve_arquivo_e_paginas(monkeypatch, htmls):
    navegador = Navegador(paginas=4)
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    html = htmls / "laudo-premium-x.html"
    resultado = pdf.converter(html, "/opt/chrome")
    assert resultado == {"arquivo": str((htmls / "laudo-premium-x.pdf").resolve()), "paginas": 4}
    (comando, kwargs), = navegador.chamadas
    assert comando[0] == "/opt/chrome" and comando[-1] == html.resolve().as_uri()
    assert comando[1:4] == ["--headless=new", "--disable-gpu", "--no-pdf-header-footer"]
    assert f"--print-to-pdf={(htmls / 'laudo-premium-x.pdf').resolve()}" in comando
    perfil = next(a.split("=", 1)[1] for a in comando if a.startswith("--user-data-dir="))
    assert Path(perfil).parent != htmls and navegador.perfil_existia == [True]
    assert not Path(perfil).exists()                       # o perfil temporário não fica para trás
    assert kwargs["timeout"] == 60 and not kwargs.get("shell")


def test_converter_destino_explicito_e_nome_do_html_com_espaco_e_acento(monkeypatch, tmp_path):
    pasta = tmp_path / "pasta com espaço"
    pasta.mkdir()
    html = pasta / "laudo ação.html"
    html.write_text("x", encoding="utf-8")
    navegador = Navegador()
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    pdf.converter(html, "/opt/chrome", destino=tmp_path / "outro.pdf")
    assert (tmp_path / "outro.pdf").is_file() and navegador.chamadas[0][0][-1].startswith("file:///")
    assert " " not in navegador.chamadas[0][0][-1] and "%20" in navegador.chamadas[0][0][-1]


def test_converter_conta_paginas_sem_contar_o_no_pages(tmp_path):
    arquivo = tmp_path / "x.pdf"
    arquivo.write_bytes(pdf_falso(3))
    assert pdf.contar_paginas(arquivo) == 3
    arquivo.write_bytes(b"%PDF-1.7 /Type /Pages /Count 9 /Type/Page /Type  /Page /Type\n/Page")
    assert pdf.contar_paginas(arquivo) == 3


def test_converter_sem_navegador_levanta(monkeypatch, htmls):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: None)
    with pytest.raises(pdf.ConversaoErro, match=MOTIVO):
        pdf.converter(htmls / "laudo-premium-x.html")


def test_converter_busca_o_navegador_quando_nao_e_dado(monkeypatch, htmls):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/achado/chrome")
    navegador = Navegador()
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    pdf.converter(htmls / "laudo-premium-x.html")
    assert navegador.chamadas[0][0][0] == "/achado/chrome"


def test_pdf_velho_nao_passa_por_novo(monkeypatch, htmls, rapido):
    velho = htmls / "laudo-premium-x.pdf"
    velho.write_bytes(pdf_falso(7))
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(grava=False))
    with pytest.raises(pdf.ConversaoErro):
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    assert not velho.exists()


def test_navegador_que_sai_com_erro_e_sem_pdf_falha_sem_esperar(monkeypatch, htmls):
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(codigo=1, grava=False))
    with pytest.raises(pdf.ConversaoErro, match="saiu com código 1 sem gerar o PDF") as erro:
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    assert "(" not in str(erro.value)                      # sem relato do navegador, sem parênteses


def test_a_falha_traz_a_ultima_linha_que_o_navegador_escreveu(monkeypatch, htmls):
    relato = b"[1:1] ruido\r\n[1:1] ERROR: Running as root without --no-sandbox is not supported\r\n\r\n"
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(codigo=1, grava=False, relato=relato))
    with pytest.raises(pdf.ConversaoErro,
                       match=r"sem gerar o PDF \(\[1:1\] ERROR: Running as root without --no-sandbox is not supported\)"):
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")


def test_a_saida_do_navegador_vai_para_arquivo_nao_para_pipe(monkeypatch, htmls):
    """Pipe herdado pelos processos-filho do Chromium trava o `run` depois de um timeout."""
    navegador = Navegador()
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    kwargs = navegador.chamadas[0][1]
    assert "capture_output" not in kwargs and kwargs["stdout"] != subprocess.PIPE
    assert kwargs["stderr"] == subprocess.STDOUT


def test_navegador_que_sai_com_zero_e_nao_entrega_o_pdf_no_prazo(monkeypatch, htmls, rapido):
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(grava=False))
    with pytest.raises(pdf.ConversaoErro, match="não ficou pronto"):
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")


def test_navegador_que_devolve_o_controle_antes_de_gravar(monkeypatch, htmls):
    """O Edge, em algumas instalações, sai antes de gravar: o PDF aparece depois e é esperado."""
    destino = (htmls / "laudo-premium-x.pdf").resolve()

    def sai_logo(comando, **kwargs):
        threading.Timer(0.5, lambda: destino.write_bytes(pdf_falso(2))).start()
        return subprocess.CompletedProcess(comando, 0, b"", b"")

    monkeypatch.setattr(pdf.subprocess, "run", sai_logo)
    assert pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")["paginas"] == 2


def test_arquivo_ainda_vazio_nao_conta_como_pronto(monkeypatch, htmls):
    destino = (htmls / "laudo-premium-x.pdf").resolve()

    def sai_logo(comando, **kwargs):
        threading.Timer(0.2, destino.touch).start()                  # o arquivo nasce vazio...
        threading.Timer(0.7, lambda: destino.write_bytes(pdf_falso(3))).start()      # ...e se completa depois
        return subprocess.CompletedProcess(comando, 0, b"", b"")

    monkeypatch.setattr(pdf.subprocess, "run", sai_logo)
    assert pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")["paginas"] == 3


def test_arquivo_que_nao_e_pdf_e_recusado_e_apagado(monkeypatch, htmls):
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(conteudo=b"<html>erro do navegador</html>"))
    with pytest.raises(pdf.ConversaoErro, match="não é um PDF"):
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    assert not (htmls / "laudo-premium-x.pdf").exists()


def test_timeout_e_erro_de_execucao_viram_conversao_erro(monkeypatch, htmls):
    html = htmls / "laudo-premium-x.html"
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(falha=subprocess.TimeoutExpired("chrome", 60)))
    with pytest.raises(pdf.ConversaoErro, match="não terminou em 60 s"):
        pdf.converter(html, "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(falha=FileNotFoundError(2, "No such file")))
    with pytest.raises(pdf.ConversaoErro, match="não foi possível executar o navegador"):
        pdf.converter(html, "/opt/chrome")


def test_perfil_temporario_some_ate_quando_a_conversao_falha(monkeypatch, htmls):
    navegador = Navegador(codigo=1, grava=False)
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    with pytest.raises(pdf.ConversaoErro):
        pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    assert navegador.perfil_existia == [True] and not navegador.perfis[0].exists()


def test_perfil_preso_pelo_navegador_e_apagado_na_nova_tentativa(monkeypatch, tmp_path, rapido):
    """O Edge solta os arquivos do perfil alguns instantes depois de gravar o PDF."""
    perfil = tmp_path / "perfil"
    perfil.mkdir()
    real, chamadas = pdf.shutil.rmtree, []

    def preso_duas_vezes(caminho, **kwargs):
        chamadas.append(caminho)
        if len(chamadas) > 2:
            real(caminho, **kwargs)

    monkeypatch.setattr(pdf.shutil, "rmtree", preso_duas_vezes)
    pdf._apagar_perfil(perfil)
    assert len(chamadas) == 3 and not perfil.exists()
    perfil.mkdir()
    chamadas.clear()
    monkeypatch.setattr(pdf.shutil, "rmtree", lambda caminho, **kwargs: chamadas.append(caminho))
    pdf._apagar_perfil(perfil)                                   # nunca solta: desiste sem erro
    assert len(chamadas) == 12 and perfil.exists()


def test_perfil_temporario_e_diferente_a_cada_conversao(monkeypatch, htmls):
    navegador = Navegador()
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    pdf.converter(htmls / "laudo-premium-x.html", "/opt/chrome")
    pdf.converter(htmls / "panorama-estrategico-x.html", "/opt/chrome")
    perfis = [next(a for a in c[0] if a.startswith("--user-data-dir=")) for c in navegador.chamadas]
    assert perfis[0] != perfis[1]


# ── converter_todos: o bloco `pdf` do JSON ────────────────────────────

def test_modo_nao_nao_tenta(monkeypatch, htmls):
    monkeypatch.setattr(pdf.subprocess, "run", lambda *a, **k: pytest.fail("não devia chamar o navegador"))
    monkeypatch.setattr(pdf, "achar_navegador", lambda: pytest.fail("não devia nem procurar"))
    assert pdf.converter_todos(arquivos(htmls), "nao") == {"gerado": False, "motivo": "desligado por --pdf nao"}


@pytest.mark.parametrize("modo", ["auto", "sim"])
def test_sem_navegador_o_html_segue_e_o_json_diz_como_fechar_o_pdf(monkeypatch, htmls, modo):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: None)
    assert pdf.converter_todos(arquivos(htmls), modo) == {"gerado": False, "motivo": MOTIVO}


def test_so_html_e_convertido_e_o_json_traz_arquivos_e_paginas(monkeypatch, htmls):
    navegador = Navegador(paginas={"laudo-premium-x.pdf": 5, "panorama-estrategico-x.pdf": 3})
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", navegador)
    r = pdf.converter_todos(arquivos(htmls), "auto")
    assert r == {"gerado": True,
                 "arquivos": [str((htmls / "laudo-premium-x.pdf").resolve()),
                              str((htmls / "panorama-estrategico-x.pdf").resolve())],
                 "paginas": {"laudo-premium-x.pdf": 5, "panorama-estrategico-x.pdf": 3}}
    assert len(navegador.chamadas) == 2 and not list(htmls.glob("*.xlsx.pdf")) and not list(htmls.glob("INTERNO*.pdf"))


@pytest.mark.parametrize("paginas,avisa", [(3, False), (4, True), (9, True)])
def test_panorama_com_mais_de_tres_paginas_gera_aviso(monkeypatch, htmls, paginas, avisa):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(paginas={"panorama-estrategico-x.pdf": paginas,
                                                                    "laudo-premium-x.pdf": 9}))
    r = pdf.converter_todos(arquivos(htmls))
    if avisa:
        assert len(r["avisos"]) == 1 and "panorama passou de 3 páginas" in r["avisos"][0]
        assert "panorama-estrategico-x.pdf" in r["avisos"][0] and f"({paginas})" in r["avisos"][0]
    else:
        assert "avisos" not in r                     # o premium é longo por natureza: sem limite


def test_falha_de_um_arquivo_e_aviso_nao_excecao(monkeypatch, htmls):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    chamadas = []

    def so_o_primeiro(comando, **kwargs):
        chamadas.append(comando)
        if len(chamadas) == 2:
            return subprocess.CompletedProcess(comando, 1, b"", b"")
        return Navegador()(comando, **kwargs)

    monkeypatch.setattr(pdf.subprocess, "run", so_o_primeiro)
    r = pdf.converter_todos(arquivos(htmls))
    assert r["gerado"] is True and list(r["paginas"]) == ["laudo-premium-x.pdf"]
    assert r["avisos"] == ["PDF de panorama-estrategico-x.html não gerado: o navegador saiu com código 1 sem gerar o PDF"]


def test_falha_em_todos_os_arquivos(monkeypatch, htmls):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(codigo=1, grava=False))
    r = pdf.converter_todos(arquivos(htmls), "sim")
    assert r["gerado"] is False and r["motivo"] == "a conversão falhou em todos os arquivos"
    assert len(r["avisos"]) == 2 and "arquivos" not in r


def test_sem_html_nao_ha_o_que_converter(monkeypatch, htmls):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: pytest.fail("não devia procurar"))
    r = pdf.converter_todos([htmls / "planilha-x.xlsx"], "sim")
    assert r == {"gerado": False, "motivo": "nenhum HTML entre os arquivos gerados"}


# ── `gerar` na linha de comando ───────────────────────────────────────

def _payload(tmp_path):
    arquivo = tmp_path / "payload.json"
    arquivo.write_text(json.dumps(relatorios._payload_demo(), ensure_ascii=False), encoding="utf-8")
    return arquivo


def _gerar(tmp_path, capsys, *extra):
    import revisao
    codigo = revisao.main(["gerar", str(_payload(tmp_path)), "--saida", str(tmp_path / "s"),
                           "--formatos", "premium,panorama", "--config-dir", str(tmp_path / "cfg"), *extra])
    saida = capsys.readouterr()
    return codigo, (json.loads(saida.out) if saida.out else None), saida.err


def test_gerar_pdf_auto_sem_navegador_entrega_o_html(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: None)
    codigo, saida, _ = _gerar(tmp_path, capsys)                  # o padrão é auto
    assert codigo == 0 and saida["pdf"] == {"gerado": False, "motivo": MOTIVO}
    assert (tmp_path / "s" / "laudo-premium-demo.html").is_file() and not list((tmp_path / "s").glob("*.pdf"))


def test_gerar_pdf_sim_sem_navegador_e_erro_com_codigo_1(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: None)
    codigo, saida, erro = _gerar(tmp_path, capsys, "--pdf", "sim")
    assert codigo == 1 and saida["pdf"]["motivo"] == MOTIVO       # o HTML e o JSON saem mesmo assim
    assert "--pdf sim" in erro and MOTIVO in erro
    assert (tmp_path / "s" / "panorama-estrategico-demo.html").is_file()


def test_gerar_pdf_nao_nao_tenta(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: pytest.fail("não devia procurar"))
    codigo, saida, _ = _gerar(tmp_path, capsys, "--pdf", "nao")
    assert codigo == 0 and saida["pdf"] == {"gerado": False, "motivo": "desligado por --pdf nao"}


def test_gerar_pdf_com_navegador_simulado(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(paginas={"laudo-premium-demo.pdf": 2,
                                                                    "panorama-estrategico-demo.pdf": 4}))
    codigo, saida, _ = _gerar(tmp_path, capsys, "--pdf", "sim")
    assert codigo == 0
    assert [os.path.basename(a) for a in saida["arquivos"]] == [
        "laudo-premium-demo.html", "INTERNO-agenda-pesquisa-demo.md", "panorama-estrategico-demo.html"]
    assert saida["pdf"]["gerado"] is True and saida["pdf"]["paginas"] == {
        "laudo-premium-demo.pdf": 2, "panorama-estrategico-demo.pdf": 4}
    assert [os.path.basename(a) for a in saida["pdf"]["arquivos"]] == ["laudo-premium-demo.pdf",
                                                                      "panorama-estrategico-demo.pdf"]
    assert "panorama passou de 3 páginas" in saida["pdf"]["avisos"][0]


def test_gerar_pdf_sim_com_conversao_que_falha_e_codigo_1(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(pdf, "achar_navegador", lambda: "/opt/chrome")
    monkeypatch.setattr(pdf.subprocess, "run", Navegador(codigo=1, grava=False))
    codigo, saida, erro = _gerar(tmp_path, capsys, "--pdf", "sim")
    assert codigo == 1 and saida["pdf"]["gerado"] is False and "não gerado" in erro
    assert _gerar(tmp_path, capsys, "--pdf", "auto")[0] == 0        # em auto, a mesma falha é só aviso


def test_gerar_so_planilha_com_pdf_sim_nao_e_erro(monkeypatch, tmp_path, capsys):
    pytest.importorskip("openpyxl")
    monkeypatch.setattr(pdf, "achar_navegador", lambda: None)
    codigo, saida, _ = _gerar(tmp_path, capsys, "--pdf", "sim", "--formatos", "planilha")
    assert codigo == 0 and saida["pdf"]["motivo"] == "nenhum HTML entre os arquivos gerados"


def test_gerar_pdf_valor_invalido_sai_com_2(tmp_path, capsys):
    with pytest.raises(SystemExit) as saida:
        _gerar(tmp_path, capsys, "--pdf", "talvez")
    assert saida.value.code == 2


def navegador_de_mentira(tmp_path):
    """Executável de verdade (o `.cmd` no Windows, um script no resto) que grava um PDF no
    `--print-to-pdf=`: o `gerar` roda por subprocesso, como o Claude o chama."""
    script = tmp_path / "navegador_de_mentira.py"
    script.write_text(
        "import sys\n"
        "destino = next(a.split('=', 1)[1] for a in sys.argv if a.startswith('--print-to-pdf='))\n"
        "open(destino, 'wb').write(b'%PDF-1.4\\n1 0 obj << /Type /Pages >> endobj\\n"
        "2 0 obj << /Type /Page >> endobj\\n3 0 obj << /Type /Page >> endobj\\n%%EOF\\n')\n", encoding="utf-8")
    if os.name == "nt":
        lancador = tmp_path / "navegador-de-mentira.cmd"
        lancador.write_text(f'@echo off\r\n"{sys.executable}" "{script}" %*\r\n', encoding="utf-8")
    else:
        lancador = tmp_path / "navegador-de-mentira.sh"
        lancador.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"\n', encoding="utf-8")
        lancador.chmod(0o755)
    return lancador


def test_gerar_por_subprocesso_acha_o_navegador_pela_variavel_de_ambiente(tmp_path):
    ambiente = {**os.environ, pdf.ENV_NAVEGADOR: str(navegador_de_mentira(tmp_path)),
                "PYTHONIOENCODING": "utf-8"}
    ambiente.pop("CLAUDE_PLUGIN_DATA", None)
    p = subprocess.run([sys.executable, str(Path(pdf.__file__).parent.parent / "revisao.py"), "gerar",
                        str(_payload(tmp_path)), "--saida", str(tmp_path / "s"), "--formatos", "premium,panorama",
                        "--config-dir", str(tmp_path / "cfg"), "--pdf", "sim"],
                       capture_output=True, text=True, encoding="utf-8", env=ambiente, timeout=120)
    assert p.returncode == 0, p.stderr
    saida = json.loads(p.stdout)
    assert saida["pdf"]["gerado"] is True and saida["pdf"]["paginas"] == {
        "laudo-premium-demo.pdf": 2, "panorama-estrategico-demo.pdf": 2}
    assert (tmp_path / "s" / "laudo-premium-demo.pdf").read_bytes().startswith(b"%PDF")


# ── navegador de verdade ──────────────────────────────────────────────

@pytest.mark.skipif(pdf.achar_navegador() is None, reason="nenhum navegador Chromium instalado")
def test_conversao_real_com_o_navegador_instalado(tmp_path):
    arquivos_gerados = relatorios.gerar(relatorios._payload_demo(), tmp_path, formatos={"premium", "panorama"})
    r = pdf.converter_todos(arquivos_gerados, "sim")
    if not r["gerado"] and "sandbox" in json.dumps(r, ensure_ascii=False).lower():
        pytest.skip(f"o navegador não roda neste ambiente sem --no-sandbox: {r}")      # runner restrito, não bug
    assert r["gerado"] is True, r
    assert sorted(r["paginas"]) == ["laudo-premium-demo.pdf", "panorama-estrategico-demo.pdf"]
    for arquivo in r["arquivos"]:
        dados = Path(arquivo).read_bytes()
        assert dados.startswith(b"%PDF") and dados.rstrip().endswith(b"%%EOF")
        assert pdf.contar_paginas(Path(arquivo)) == r["paginas"][Path(arquivo).name] >= 1
    assert 1 <= r["paginas"]["panorama-estrategico-demo.pdf"] <= pdf.PAGINAS_PANORAMA and "avisos" not in r
