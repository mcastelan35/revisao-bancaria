"""
pdf.py — PDF dos entregáveis HTML, convertido por um navegador Chromium já instalado

O `gerar` entrega o HTML e, quando acha Chrome, Edge, Chromium ou Brave, converte cada HTML em
PDF ao lado dele (mesmo nome, `.pdf`), em modo headless e sem o cabeçalho e o rodapé do
navegador. Sem navegador NADA falha: o HTML segue entregue e o JSON do `gerar` diz como fechar o
PDF à mão. Só biblioteca padrão.

Busca do navegador, nesta ordem:
  1. variável de ambiente REVISAO_BANCARIA_NAVEGADOR (caminho do executável ou nome no PATH);
  2. `shutil.which` para chrome, google-chrome, google-chrome-stable, chromium,
     chromium-browser, msedge, microsoft-edge e brave;
  3. caminhos padrão do Windows (Program Files, Program Files (x86), %LOCALAPPDATA%: Chrome e
     Edge) e do macOS (/Applications).

Cada conversão usa um `--user-data-dir` temporário, para não colidir com o navegador que o
usuário já tenha aberto, e confere o resultado: o arquivo existe, começa com `%PDF` e tem as
páginas contadas (`/Type /Page`). O Edge, em algumas instalações, devolve o controle antes de
gravar o arquivo; por isso, depois que o processo sai, espera-se o PDF aparecer por inteiro.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ENV_NAVEGADOR = "REVISAO_BANCARIA_NAVEGADOR"
EXECUTAVEIS = ("chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
               "msedge", "microsoft-edge", "brave")
TIMEOUT = 60                         # segundos por arquivo: navegador mais espera do PDF
INTERVALO = 0.25                     # segundos entre uma conferência e outra do arquivo
PAGINAS_PANORAMA = 3                 # o PANORAMA é de duas a três páginas
MOTIVO_SEM_NAVEGADOR = "nenhum navegador Chromium encontrado — abra o HTML e salve como PDF"
RE_PAGINA = re.compile(rb"/Type\s*/Page(?!s)")


class ConversaoErro(RuntimeError):
    """O PDF de UM arquivo não saiu (o `converter_todos` a transforma em aviso)."""


# ─────────────────────────────────────────────────────────────────────
# busca do navegador
# ─────────────────────────────────────────────────────────────────────

def caminhos_padrao(plataforma: str | None = None, ambiente=None) -> list[Path]:
    """Onde Chrome e Edge costumam estar no Windows e no macOS (lista vazia nos demais sistemas,
    que dependem do PATH). `plataforma` e `ambiente` existem para os testes."""
    plataforma = plataforma or sys.platform
    env = os.environ if ambiente is None else ambiente
    if plataforma == "win32":
        bases = [env.get(v) for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
        relativos = (Path("Google/Chrome/Application/chrome.exe"),
                     Path("Microsoft/Edge/Application/msedge.exe"))
        return [Path(base) / rel for rel in relativos for base in bases if base]
    if plataforma == "darwin":
        return [Path("/Applications") / app for app in (
            "Google Chrome.app/Contents/MacOS/Google Chrome",
            "Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "Chromium.app/Contents/MacOS/Chromium",
            "Brave Browser.app/Contents/MacOS/Brave Browser")]
    return []


def achar_navegador() -> str | None:
    """O executável do primeiro Chromium encontrado, ou None."""
    indicado = (os.environ.get(ENV_NAVEGADOR) or "").strip()
    if indicado:
        if Path(indicado).is_file():
            return indicado
        achado = shutil.which(indicado)
        if achado:
            return achado
    for nome in EXECUTAVEIS:
        achado = shutil.which(nome)
        if achado:
            return achado
    for caminho in caminhos_padrao():
        if caminho.is_file():
            return str(caminho)
    return None


# ─────────────────────────────────────────────────────────────────────
# conversão
# ─────────────────────────────────────────────────────────────────────

def contar_paginas(pdf: Path) -> int:
    """Páginas de um PDF pelo número de objetos `/Type /Page` (o `/Type /Pages` não conta)."""
    return len(RE_PAGINA.findall(Path(pdf).read_bytes()))


def _termina_em_eof(arquivo: Path) -> bool:
    with arquivo.open("rb") as f:
        f.seek(max(0, arquivo.stat().st_size - 64))
        return f.read().rstrip().endswith(b"%%EOF")


def _ultima_linha(relato) -> str:
    """A última linha que o navegador escreveu (ajuda a explicar a falha); '' se não há."""
    try:
        relato.seek(0)
        linhas = [l.strip() for l in relato.read().decode("utf-8", "replace").splitlines() if l.strip()]
    except (OSError, ValueError):
        return ""
    return linhas[-1][:200] if linhas else ""


def _apagar_perfil(perfil: Path) -> None:
    """Apaga o perfil temporário do navegador. O Edge solta os arquivos alguns instantes depois de
    gravar o PDF: tenta de novo por uns segundos e desiste sem erro (sobra um perfil pequeno)."""
    for _ in range(12):
        shutil.rmtree(perfil, ignore_errors=True)
        if not perfil.exists():
            return
        time.sleep(INTERVALO)


def _esperar_pdf(destino: Path, codigo: int, limite: float) -> None:
    """Espera o PDF existir por inteiro: termina em %%EOF ou parou de crescer entre duas
    conferências. Navegador que saiu com erro e não deixou arquivo falha sem esperar."""
    anterior = -1
    while True:
        if destino.is_file():
            tamanho = destino.stat().st_size
            if tamanho > 0 and (tamanho == anterior or _termina_em_eof(destino)):
                return
            anterior = tamanho
        elif codigo != 0:
            raise ConversaoErro(f"o navegador saiu com código {codigo} sem gerar o PDF")
        if time.monotonic() >= limite:
            raise ConversaoErro(f"o PDF não ficou pronto em {TIMEOUT} s")
        time.sleep(INTERVALO)


def converter(html, navegador: str | None = None, destino=None) -> dict:
    """Converte um HTML em PDF e devolve `{"arquivo": <caminho do PDF>, "paginas": <int>}`.

    `destino` padrão: o mesmo caminho do HTML com `.pdf`. Levanta ConversaoErro se não há
    navegador, se ele não termina em TIMEOUT segundos ou se o arquivo gerado não é um PDF."""
    html = Path(html).resolve()
    destino = Path(destino).resolve() if destino else html.with_suffix(".pdf")
    navegador = navegador or achar_navegador()
    if not navegador:
        raise ConversaoErro(MOTIVO_SEM_NAVEGADOR)
    limite = time.monotonic() + TIMEOUT
    try:
        destino.unlink(missing_ok=True)                  # PDF velho não pode passar por novo
    except OSError as erro:
        raise ConversaoErro(f"não foi possível substituir {destino.name} (está aberto em outro "
                            f"programa?): {erro.strerror or erro}") from None
    perfil = Path(tempfile.mkdtemp(prefix="revisao-bancaria-pdf-"))
    try:
        with tempfile.TemporaryFile() as relato:
            comando = [str(navegador), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                       f"--user-data-dir={perfil}", f"--print-to-pdf={destino}", html.as_uri()]
            try:
                # A saída vai para arquivo, não para pipe: os processos-filho do Chromium herdam o pipe
                # e, depois de um timeout, o `run` ficaria esperando por eles.
                processo = subprocess.run(comando, stdout=relato, stderr=subprocess.STDOUT, timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                raise ConversaoErro(f"o navegador não terminou em {TIMEOUT} s") from None
            except OSError as erro:
                raise ConversaoErro(f"não foi possível executar o navegador {navegador}: "
                                    f"{erro.strerror or erro}") from None
            try:
                _esperar_pdf(destino, processo.returncode, limite)
            except ConversaoErro as erro:
                detalhe = _ultima_linha(relato)
                raise ConversaoErro(f"{erro} ({detalhe})" if detalhe else str(erro)) from None
    finally:
        _apagar_perfil(perfil)
    if not destino.read_bytes().startswith(b"%PDF"):
        destino.unlink(missing_ok=True)
        raise ConversaoErro(f"o arquivo gerado para {html.name} não é um PDF")
    return {"arquivo": str(destino), "paginas": contar_paginas(destino)}


def converter_todos(arquivos, modo: str = "auto") -> dict:
    """O bloco `pdf` do JSON do `gerar`, para os `.html` de `arquivos` (o resto é ignorado).

    modo "nao": não tenta. "auto" e "sim": tentam; a diferença (sem navegador, "sim" é erro de
    saída) é de quem chama. Sem navegador: `{"gerado": False, "motivo": ...}`. Com navegador:
    `{"gerado": True, "arquivos": [...], "paginas": {<pdf>: n}}`, mais `avisos` quando algum
    arquivo não converteu ou o PANORAMA passou de três páginas. Nunca levanta por falha de
    conversão."""
    htmls = [Path(a) for a in arquivos if Path(a).suffix.lower() == ".html"]
    if modo == "nao":
        return {"gerado": False, "motivo": "desligado por --pdf nao"}
    if not htmls:
        return {"gerado": False, "motivo": "nenhum HTML entre os arquivos gerados"}
    navegador = achar_navegador()
    if not navegador:
        return {"gerado": False, "motivo": MOTIVO_SEM_NAVEGADOR}
    feitos, paginas, avisos = [], {}, []
    for html in htmls:
        try:
            resultado = converter(html, navegador)
        except (ConversaoErro, OSError) as erro:
            avisos.append(f"PDF de {html.name} não gerado: {erro}")
            continue
        nome = Path(resultado["arquivo"]).name
        feitos.append(resultado["arquivo"])
        paginas[nome] = resultado["paginas"]
        if html.name.startswith("panorama") and resultado["paginas"] > PAGINAS_PANORAMA:
            avisos.append(f"{nome}: panorama passou de {PAGINAS_PANORAMA} páginas "
                          f"({resultado['paginas']}) — enxugar o texto ou as seções")
    saida: dict = {"gerado": bool(feitos)}
    if feitos:
        saida.update(arquivos=feitos, paginas=paginas)
    else:
        saida["motivo"] = "a conversão falhou em todos os arquivos"
    if avisos:
        saida["avisos"] = avisos
    return saida
