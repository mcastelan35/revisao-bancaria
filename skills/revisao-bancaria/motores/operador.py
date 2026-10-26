"""
operador.py — identidade de quem assina o laudo (advogado com OAB ou contador com CRC)

Guardada em `operador.json`, FORA do pacote: sobrevive a atualizações do plugin e nunca entra
no repositório. Nenhum nome, registro ou entidade vem pré-preenchido em arquivo do plugin
(regra de conduta 26); o `gerar` da linha de comando preenche `marca` e `assinatura` do payload
a partir daqui quando o payload não as traz.

Pasta de configuração, por precedência:
  1. argumento `config_dir` (não vazio);
  2. variável de ambiente REVISAO_BANCARIA_CONFIG_DIR;
  3. variável de ambiente CLAUDE_PLUGIN_DATA (pasta de dados do plugin no Claude Code);
  4. padrão do sistema — Windows: %LOCALAPPDATA%\\RevisaoBancaria; macOS:
     ~/Library/Application Support/RevisaoBancaria; demais:
     ${XDG_CONFIG_HOME:-~/.config}/revisao-bancaria.
Valor que contenha `${` (variável que o ambiente não substituiu) conta como vazio.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

NOME_ARQUIVO = "operador.json"
TIPOS = ("advogado", "contador")
CHAVES = ("tipo", "nome", "registro", "entidade", "cidade", "skill_peticao")
CHAVES_ASSINATURA = ("nome", "registro", "entidade", "cidade")
PREFIXO_REGISTRO = {"advogado": "OAB/", "contador": "CRC/"}
EXEMPLO_REGISTRO = {"advogado": "OAB/UF 00.000", "contador": "CRC/UF 000000/O"}


def _limpo(valor) -> str:
    """Texto sem espaços nas pontas; vazio se ausente ou com variável não substituída (`${`)."""
    texto = "" if valor is None else str(valor).strip()
    return "" if "${" in texto else texto


def _pasta_padrao() -> Path:
    casa = Path.home()
    if sys.platform == "win32":
        base = _limpo(os.environ.get("LOCALAPPDATA"))
        return (Path(base) if base else casa / "AppData" / "Local") / "RevisaoBancaria"
    if sys.platform == "darwin":
        return casa / "Library" / "Application Support" / "RevisaoBancaria"
    xdg = _limpo(os.environ.get("XDG_CONFIG_HOME"))
    return (Path(xdg) if xdg else casa / ".config") / "revisao-bancaria"


def pasta_config(config_dir=None) -> Path:
    """Pasta onde fica o `operador.json` (ver a precedência no cabeçalho do módulo)."""
    for candidato in (config_dir, os.environ.get("REVISAO_BANCARIA_CONFIG_DIR"),
                      os.environ.get("CLAUDE_PLUGIN_DATA")):
        valor = _limpo(candidato)
        if valor:
            return Path(valor).expanduser()
    return _pasta_padrao()


def ler(config_dir=None) -> dict | None:
    """O operador gravado, ou None se ainda não foi configurado."""
    arquivo = pasta_config(config_dir) / NOME_ARQUIVO
    if not arquivo.is_file():
        return None
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as erro:
        raise ValueError(f"{arquivo} não é um JSON válido: {erro}") from None
    if not isinstance(dados, dict):
        raise ValueError(f"{arquivo} deve conter um objeto JSON")
    return dados


def salvar(dados: dict, config_dir=None) -> tuple[Path, list[str]]:
    """Grava o operador (UTF-8, indent 2) e devolve (arquivo, avisos).

    Chaves aceitas: tipo ('advogado' | 'contador', obrigatória), nome, registro, entidade,
    cidade, skill_peticao. Chave desconhecida é ValueError. Registro fora do padrão
    (OAB/ para advogado, CRC/ para contador) gera aviso, não erro."""
    desconhecidas = sorted(k for k in dados if k not in CHAVES and k != "atualizado_em")
    if desconhecidas:
        raise ValueError(f"chave desconhecida no operador: {', '.join(desconhecidas)}. "
                         f"Aceitas: {', '.join(CHAVES)}")
    tipo = dados.get("tipo")
    if tipo not in TIPOS:
        raise ValueError(f"tipo obrigatório: 'advogado' ou 'contador' (recebido: {tipo!r})")
    gravar = {k: dados[k] for k in CHAVES if k in dados}
    gravar["atualizado_em"] = datetime.now().isoformat(timespec="seconds")

    avisos: list[str] = []
    registro = _limpo(gravar.get("registro"))
    prefixo = PREFIXO_REGISTRO[tipo]
    if registro and not registro.startswith(prefixo):
        avisos.append(f"registro {registro!r} fora do padrão: o de {tipo} começa com {prefixo!r} "
                      f"(ex.: {EXEMPLO_REGISTRO[tipo]})")

    pasta = pasta_config(config_dir)
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / NOME_ARQUIVO
    arquivo.write_text(json.dumps(gravar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
                       newline="\n")                               # LF também no Windows
    return arquivo, avisos


def assinatura(op: dict | None) -> dict:
    """Bloco `assinatura` do payload: nome, registro, entidade e cidade ('' se ausentes)."""
    op = op or {}
    return {k: str(op.get(k) or "") for k in CHAVES_ASSINATURA}


def marca_nome(op: dict | None) -> str:
    """Nome da marca do cabeçalho: a `entidade`, se houver; senão o `nome`."""
    a = assinatura(op)
    return a["entidade"] if a["entidade"].strip() else a["nome"]
