"""
tema.py — identidade visual dos entregáveis (cores, fontes, logo, cabeçalho e rodapé)

Guardada em `tema.json`, na MESMA pasta de configuração do operador (`operador.pasta_config`),
fora do pacote: sobrevive a atualizações do plugin e nunca entra no repositório. Sem `tema.json`
os entregáveis saem com o tema padrão (`PADRAO`) e o HTML é o mesmo, byte a byte, de antes de o
tema existir. O módulo só guarda, valida e deriva valores; quem desenha é `relatorios.py`.

Esquema fechado — chave desconhecida é ValueError, como no operador:

  nome, skill_origem   texto. `skill_origem` é a skill de layout de onde o tema foi importado;
                       só registro, o código Python nunca chama skill
  cores                tinta, destaque, destaque_claro, fundo_destaque — só `#RRGGBB`. Viram
                       --ink, --gold, --glt e --gpale do CSS e as cores equivalentes da
                       planilha. As cores do semáforo (vermelho, verde, âmbar) NÃO são
                       configuráveis: o significado jurídico não muda com a marca
  fontes               titulo, texto, mono — nome de família (letras, números, espaço e hífen),
                       sempre acrescido do fallback que o CSS já tem
  fontes_url           opcional; só `https://fonts.googleapis.com/css2?...`. Sem ela, o link do
                       Google das fontes padrão cobre apenas as famílias padrão que o tema
                       ainda usa; fonte do tema sem link depende de estar instalada
  logo                 PNG, JPG ou SVG de até 300 KB, embutido no cabeçalho como data URI.
                       `salvar` copia o arquivo para a pasta de configuração (o caminho original
                       pode mudar de lugar numa atualização da skill de origem)
  cabecalho_linha      texto curto sob a marca; rodape: substitui "Documento confidencial"

Todo texto do tema passa por `esc()` no renderizador e nada do tema entra cru no CSS fora das
variáveis validadas aqui (cor `#RRGGBB`, nome de família restrito).
"""

from __future__ import annotations

import base64
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from .operador import pasta_config

NOME_ARQUIVO = "tema.json"
PREFIXO_LOGO = "tema-logo"                  # tema-logo.png | .jpg | .jpeg | .svg, ao lado do tema.json
CHAVES = ("nome", "skill_origem", "cores", "fontes", "fontes_url", "logo", "cabecalho_linha", "rodape")
CHAVES_CORES = ("tinta", "destaque", "destaque_claro", "fundo_destaque")
CHAVES_FONTES = ("titulo", "texto", "mono")
TIPOS_LOGO = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}
LOGO_MAX_BYTES = 300 * 1024
LIMITE_TEXTO = {"nome": 80, "skill_origem": 80, "cabecalho_linha": 200, "rodape": 120}
NOME_SEM_NOME = "Personalizado"
RODAPE_PADRAO = "Documento confidencial"
CONTRASTE_MINIMO = 4.5                      # WCAG AA para texto corrido

RE_COR = re.compile(r"#[0-9A-Fa-f]{6}")
RE_FONTE = re.compile(r"[A-Za-z0-9 \-]{1,40}")
RE_FONTES_URL = re.compile(r"https://fonts\.googleapis\.com/css2\?[\w:;,=&+@.%\-]+")
# `<script` ou atributo de evento (`onload=`, `onclick =`); o `(?<![\w:-])` evita casar o meio de
# um nome de atributo legítimo, como `patternContentUnits=`.
RE_SVG_ATIVO = re.compile(r"<script|(?<![\w:-])on\w+\s*=", re.I)

#: Famílias do link padrão do Google, na ordem em que o link as lista (e que o HTML sem tema usa).
FAMILIAS_PADRAO = {"DM Sans": "DM+Sans:wght@300;400;500;600",
                   "Space Grotesk": "Space+Grotesk:wght@400;500;600",
                   "JetBrains Mono": "JetBrains+Mono:wght@400"}
FONTES_URL_PADRAO = ("https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600"
                     "&family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400"
                     "&display=swap")
COR_TEXTO_FAIXA_PADRAO = "#7A5F10"          # texto das faixas de seção no CSS padrão (destaque escurecido)

#: O tema atual do plugin, descrito em dados. `validar(PADRAO)` o devolve sem alteração e o
#: renderizador o desenha igual ao HTML sem tema.
PADRAO = {
    "nome": "Padrão do plugin",
    "cores": {"tinta": "#1A1714", "destaque": "#B08A4E", "destaque_claro": "#EDE0B8",
              "fundo_destaque": "#FAF7EF"},
    "fontes": {"titulo": "Space Grotesk", "texto": "DM Sans", "mono": "JetBrains Mono"},
    "fontes_url": FONTES_URL_PADRAO,
    "rodape": RODAPE_PADRAO,
}


# ─────────────────────────────────────────────────────────────────────
# cor: luminância, contraste e derivados
# ─────────────────────────────────────────────────────────────────────

def _rgb(cor: str) -> tuple[int, int, int]:
    return int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16)


def luminancia(cor: str) -> float:
    """Luminância relativa (WCAG) de `#RRGGBB`."""
    def canal(v: int) -> float:
        v = v / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(v) for v in _rgb(cor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a: str, b: str) -> float:
    """Razão de contraste (1 a 21) entre duas cores `#RRGGBB`."""
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def cor_texto_destaque(destaque: str, fundo: str) -> str:
    """Cor do texto das faixas de seção: o `destaque` escurecido até ler bem sobre o `fundo`.
    Com o destaque e o fundo padrão devolve a cor que o CSS padrão sempre usou (#7A5F10)."""
    if (destaque.upper(), fundo.upper()) == (PADRAO["cores"]["destaque"], PADRAO["cores"]["fundo_destaque"]):
        return COR_TEXTO_FAIXA_PADRAO
    r, g, b = _rgb(destaque)
    for fator in (0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0):
        cor = "#%02X%02X%02X" % (round(r * fator), round(g * fator), round(b * fator))
        if contraste(cor, fundo) >= CONTRASTE_MINIMO:
            return cor
    return "#000000"


def argb(cor: str) -> str:
    """`#RRGGBB` -> `FFRRGGBB`, o formato de cor do openpyxl."""
    return "FF" + cor.lstrip("#").upper()


# ─────────────────────────────────────────────────────────────────────
# validação
# ─────────────────────────────────────────────────────────────────────

def _texto(dados: dict, chave: str) -> str:
    valor = dados.get(chave)
    if valor is None:
        return ""
    if not isinstance(valor, str):
        raise ValueError(f"{chave} deve ser texto (recebido: {type(valor).__name__})")
    valor = " ".join(valor.split())                       # quebras de linha e espaços repetidos
    if len(valor) > LIMITE_TEXTO[chave]:
        raise ValueError(f"{chave} com {len(valor)} caracteres: o limite é {LIMITE_TEXTO[chave]}")
    return valor


def _bloco(dados: dict, chave: str, aceitas: tuple[str, ...]) -> dict:
    bloco = dados.get(chave)
    if bloco is None:
        return {}
    if not isinstance(bloco, dict):
        raise ValueError(f"{chave} deve ser um objeto com {', '.join(aceitas)}")
    desconhecidas = sorted(str(k) for k in bloco if k not in aceitas)
    if desconhecidas:
        raise ValueError(f"chave desconhecida em {chave}: {', '.join(desconhecidas)}. "
                         f"Aceitas: {', '.join(aceitas)}")
    return bloco


def _cores(dados: dict) -> dict:
    dadas, cores = _bloco(dados, "cores", CHAVES_CORES), {}
    for chave in CHAVES_CORES:
        valor = dadas.get(chave)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            cores[chave] = PADRAO["cores"][chave]
        elif isinstance(valor, str) and RE_COR.fullmatch(valor.strip()):
            cores[chave] = valor.strip().upper()
        else:
            raise ValueError(f"cores.{chave}: {valor!r} não é uma cor no formato #RRGGBB")
    return cores


def _fontes(dados: dict) -> dict:
    dadas, fontes = _bloco(dados, "fontes", CHAVES_FONTES), {}
    for chave in CHAVES_FONTES:
        valor = dadas.get(chave)
        if valor is None or (isinstance(valor, str) and not valor.strip()):
            fontes[chave] = PADRAO["fontes"][chave]
        elif isinstance(valor, str) and RE_FONTE.fullmatch(valor.strip()):
            fontes[chave] = valor.strip()
        else:
            raise ValueError(f"fontes.{chave}: {valor!r} não é um nome de família válido "
                             "(até 40 letras, números, espaços ou hífens)")
    return fontes


def _fontes_url(dados: dict) -> str:
    valor = dados.get("fontes_url")
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return ""
    if not isinstance(valor, str) or not RE_FONTES_URL.fullmatch(valor.strip()):
        raise ValueError(f"fontes_url: {valor!r} não é um link https://fonts.googleapis.com/css2?...")
    return valor.strip()


def _conferir_svg(caminho: Path) -> None:
    try:
        texto = caminho.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        raise ValueError(f"logo {caminho.name!r}: o SVG deve estar em UTF-8") from None
    achado = RE_SVG_ATIVO.search(texto)
    if achado:
        raise ValueError(f"logo {caminho.name!r}: SVG com conteúdo ativo ({achado.group(0).strip()!r}) "
                         "é recusado — exporte o logo como SVG simples, sem script nem evento")


def _logo(valor, base) -> str:
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return ""
    if not isinstance(valor, str):
        raise ValueError("logo deve ser o caminho de um arquivo PNG, JPG ou SVG")
    caminho = Path(valor.strip()).expanduser()
    if not caminho.is_absolute():
        caminho = (Path(base).expanduser() if base else Path.cwd()) / caminho
    extensao = caminho.suffix.lower()
    if extensao not in TIPOS_LOGO:
        raise ValueError(f"logo {caminho.name!r}: extensão {extensao or '(nenhuma)'} não aceita — "
                         "use PNG, JPG ou SVG")
    if not caminho.is_file():
        raise ValueError(f"logo não encontrado: {caminho}")
    tamanho = caminho.stat().st_size
    if tamanho == 0:
        raise ValueError(f"logo {caminho.name!r} está vazio")
    if tamanho > LOGO_MAX_BYTES:
        raise ValueError(f"logo {caminho.name!r} com {tamanho / 1024:.0f} KB: o limite é "
                         f"{LOGO_MAX_BYTES // 1024} KB — reduza a imagem")
    if extensao == ".svg":
        _conferir_svg(caminho)
    return str(caminho.resolve())


def validar(dados: dict, base=None) -> tuple[dict, list[str]]:
    """Valida o tema e devolve (dados normalizados, avisos). Erro de esquema é ValueError.

    Normaliza: textos sem espaços repetidos, cores em maiúsculas, `cores` e `fontes` completas
    (o que faltou vem de `PADRAO`) e `logo` como caminho absoluto. `base` é a pasta que resolve
    um `logo` relativo (padrão: a pasta atual). Idempotente: `validar(validar(d)[0])[0]` é igual.

    Avisos (não recusam): fonte do tema sem `fontes_url` e tinta que não contrasta com o papel
    ou com o fundo de destaque (tabelas e textos ficariam ilegíveis)."""
    if not isinstance(dados, dict):
        raise ValueError("o tema deve ser um objeto JSON")
    desconhecidas = sorted(str(k) for k in dados if k not in CHAVES and k != "atualizado_em")
    if desconhecidas:
        raise ValueError(f"chave desconhecida no tema: {', '.join(desconhecidas)}. "
                         f"Aceitas: {', '.join(CHAVES)}")
    tema: dict = {"nome": _texto(dados, "nome") or NOME_SEM_NOME}
    if _texto(dados, "skill_origem"):
        tema["skill_origem"] = _texto(dados, "skill_origem")
    tema["cores"] = _cores(dados)
    tema["fontes"] = _fontes(dados)
    for chave, valor in (("fontes_url", _fontes_url(dados)), ("logo", _logo(dados.get("logo"), base)),
                         ("cabecalho_linha", _texto(dados, "cabecalho_linha")),
                         ("rodape", _texto(dados, "rodape"))):
        if valor:
            tema[chave] = valor

    avisos: list[str] = []
    fora = sorted({f for f in tema["fontes"].values() if f not in FAMILIAS_PADRAO})
    if fora and "fontes_url" not in tema:
        avisos.append(f"fonte(s) {', '.join(fora)} sem fontes_url: o navegador só as usa se estiverem "
                      "instaladas no computador de quem abrir o arquivo; senão entra a fonte de reserva")
    cores = tema["cores"]
    if contraste(cores["tinta"], "#FFFFFF") < CONTRASTE_MINIMO:
        avisos.append(f"tinta {cores['tinta']} contrasta pouco com o papel branco "
                      f"(razão {contraste(cores['tinta'], '#FFFFFF'):.1f}): textos e cabeçalhos "
                      "de tabela ficam difíceis de ler")
    if contraste(cores["tinta"], cores["fundo_destaque"]) < CONTRASTE_MINIMO:
        avisos.append(f"tinta {cores['tinta']} contrasta pouco com fundo_destaque {cores['fundo_destaque']} "
                      f"(razão {contraste(cores['tinta'], cores['fundo_destaque']):.1f}): indicadores e "
                      "caixas ficam difíceis de ler")
    return tema, avisos


# ─────────────────────────────────────────────────────────────────────
# derivados para o renderizador
# ─────────────────────────────────────────────────────────────────────

def url_fontes(tema: dict) -> str | None:
    """CSS de fontes a carregar: o `fontes_url` do tema; sem ele, o link do Google só com as
    famílias PADRÃO que o tema ainda usa (None se não usa nenhuma). `tema` já validado."""
    if tema.get("fontes_url"):
        return tema["fontes_url"]
    usadas = set(tema["fontes"].values())
    partes = [f"family={consulta}" for nome, consulta in FAMILIAS_PADRAO.items() if nome in usadas]
    return ("https://fonts.googleapis.com/css2?" + "&".join(partes) + "&display=swap") if partes else None


def logo_data_uri(tema: dict) -> str | None:
    """O logo como `data:<tipo>;base64,...`, lido do arquivo no momento da renderização."""
    if not tema.get("logo"):
        return None
    caminho = Path(tema["logo"])
    try:
        conteudo = caminho.read_bytes()
    except OSError as erro:
        raise ValueError(f"não foi possível ler o logo {caminho}: {erro.strerror or erro}") from None
    return f"data:{TIPOS_LOGO[caminho.suffix.lower()]};base64," + base64.b64encode(conteudo).decode("ascii")


def nome_do_tema(tema: dict | None) -> str:
    """O rótulo que a linha de comando informa: o nome do tema ou "padrao"."""
    return "padrao" if tema is None else (tema.get("nome") or NOME_SEM_NOME)


# ─────────────────────────────────────────────────────────────────────
# arquivo na pasta de configuração
# ─────────────────────────────────────────────────────────────────────

def ler(config_dir=None) -> dict | None:
    """O tema gravado, ou None se não há `tema.json`. O logo, guardado pelo nome do arquivo ao
    lado do tema.json, volta como caminho absoluto. Não valida: use `validar` ou `carregar`."""
    arquivo = pasta_config(config_dir) / NOME_ARQUIVO
    if not arquivo.is_file():
        return None
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as erro:
        raise ValueError(f"{arquivo} não é um JSON válido: {erro}") from None
    if not isinstance(dados, dict):
        raise ValueError(f"{arquivo} deve conter um objeto JSON")
    logo = dados.get("logo")
    if isinstance(logo, str) and logo.strip():
        caminho = Path(logo.strip()).expanduser()
        dados["logo"] = str(caminho if caminho.is_absolute() else arquivo.parent / caminho)
    return dados


def carregar(config_dir=None) -> tuple[dict | None, list[str]]:
    """`ler` + `validar`: (tema normalizado, avisos), ou (None, []) sem tema gravado. Tema
    gravado e inválido (logo que sumiu, por exemplo) é ValueError."""
    dados = ler(config_dir)
    return (None, []) if dados is None else validar(dados)


def salvar(dados: dict, config_dir=None, base=None) -> tuple[Path, list[str]]:
    """Valida e grava o tema (UTF-8, indent 2); devolve (arquivo, avisos). Tema inválido não
    grava nada. O logo é copiado para `tema-logo.<ext>` ao lado do `tema.json`, e o `tema.json`
    guarda só esse nome. `base` resolve um `logo` relativo no `dados` (padrão: a pasta atual)."""
    tema, avisos = validar(dados, base)
    pasta = pasta_config(config_dir)
    pasta.mkdir(parents=True, exist_ok=True)
    gravar = dict(tema)
    mantido = None
    if tema.get("logo"):
        origem = Path(tema["logo"])
        mantido = pasta / f"{PREFIXO_LOGO}{origem.suffix.lower()}"
        if origem.resolve() != mantido.resolve():
            shutil.copyfile(origem, mantido)
        gravar["logo"] = mantido.name
    for antigo in pasta.glob(f"{PREFIXO_LOGO}.*"):                 # logo de uma gravação anterior
        if antigo.suffix.lower() in TIPOS_LOGO and antigo != mantido:
            antigo.unlink()
    gravar["atualizado_em"] = datetime.now().isoformat(timespec="seconds")
    arquivo = pasta / NOME_ARQUIVO
    arquivo.write_text(json.dumps(gravar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
                       newline="\n")                               # LF também no Windows
    return arquivo, avisos


def remover(config_dir=None) -> bool:
    """Apaga o `tema.json` e o logo copiado; True se havia algo. Volta ao tema padrão."""
    pasta = pasta_config(config_dir)
    removido = False
    alvos = [pasta / NOME_ARQUIVO, *(p for p in pasta.glob(f"{PREFIXO_LOGO}.*")
                                      if p.suffix.lower() in TIPOS_LOGO)]
    for alvo in alvos:
        if alvo.is_file():
            alvo.unlink()
            removido = True
    return removido
