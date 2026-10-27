#!/usr/bin/env python3
"""Empacota o plugin revisao-bancaria para o claude.ai (o repositório já é plugin e marketplace).

    python ferramentas/empacotar_plugin.py

Gera `dist/revisao-bancaria-<versão>.plugin`, o arquivo que se envia em claude.ai › Personalizar ›
Plugins (e que aparece também no Claude Code do mesmo usuário). Antes de empacotar, confere se a
versão é a mesma em todos os lugares; se não for, rode `python ferramentas/verificar_consistencia.py`.

Quem já instalou só recebe código novo quando a versão muda: suba a versão (manifestos, SKILL.md,
regras-bancarias.json, motores/__init__.py, CHANGELOG e ARCHITECTURE) a cada publicação.

Instalação pelo GitHub, no Claude Code:
    /plugin marketplace add mcastelan35/revisao-bancaria
    /plugin install revisao-bancaria@revisao-bancaria
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOME = "revisao-bancaria"

# Entram no .plugin; testes, ferramentas e configuração local ficam de fora.
ARQUIVOS = [".claude-plugin", "skills", "README.md", "CONECTOR.md", "CHANGELOG.md"]
IGNORAR_PARTES = {"__pycache__", ".pytest_cache"}
IGNORAR_SUFIXOS = {".pyc", ".pdf", ".csv", ".xlsx", ".xls", ".docx", ".html"}


def versoes() -> dict[str, str | None]:
    plugin = json.loads((RAIZ / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    mercado = json.loads((RAIZ / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    skill = RAIZ / "skills" / NOME
    regras = json.loads((skill / "dados" / "regras-bancarias.json").read_text(encoding="utf-8"))
    m_skill = re.search(r'^\s*version:\s*"([^"]+)"', (skill / "SKILL.md").read_text(encoding="utf-8"), re.M)
    m_init = re.search(r'^VERSAO\s*=\s*"([^"]+)"', (skill / "motores" / "__init__.py").read_text(encoding="utf-8"), re.M)
    return {
        "plugin.json": plugin.get("version"),
        "marketplace.json": mercado["plugins"][0].get("version"),
        "SKILL.md": m_skill.group(1) if m_skill else None,
        "regras-bancarias.json": regras.get("versao"),
        "motores/__init__.py": m_init.group(1) if m_init else None,
    }


def entra(arq: Path) -> bool:
    if not arq.is_file() or IGNORAR_PARTES & set(arq.parts):
        return False
    if arq.suffix.lower() in IGNORAR_SUFIXOS or arq.name in ("operador.json", "tema.json"):
        return False
    if arq.name.startswith("tema-logo."):                    # logo copiado do tema, na pasta de dados
        return False
    return True


def main() -> int:
    v = versoes()
    if len(set(v.values())) != 1 or None in v.values():
        print(f"✗ versões divergentes: {v}\n  Rode python ferramentas/verificar_consistencia.py e alinhe antes de publicar.")
        return 1
    versao = v["plugin.json"]
    saida = RAIZ / "dist" / f"{NOME}-{versao}.plugin"
    saida.parent.mkdir(exist_ok=True)
    if saida.exists():
        print(f"⚠ dist/{saida.name} já existia e foi substituído: se o código mudou desde a última "
              "publicação, suba a versão — quem já instalou só recebe a versão nova.")
    n = 0
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for item in ARQUIVOS:
            caminho = RAIZ / item
            for arq in [caminho] if caminho.is_file() else sorted(caminho.rglob("*")):
                if entra(arq):
                    z.write(arq, arq.relative_to(RAIZ).as_posix())
                    n += 1
    print(f"✓ {saida.relative_to(RAIZ).as_posix()} — {n} arquivos, {saida.stat().st_size / 1e3:.0f} KB, "
          f"versão {versao}, para enviar em claude.ai › Personalizar › Plugins")
    return 0


if __name__ == "__main__":
    for _f in (sys.stdout, sys.stderr):
        try:
            _f.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    sys.exit(main())
