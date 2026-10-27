"""Configuração comum dos testes: põe a skill no sys.path e expõe `RAIZ` e `SKILL`.

Os testes importam `motores` direto (`from motores import regras`) e chamam a linha de comando
por subprocesso; nenhum toca a pasta real do operador nem a rede."""
import base64
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILL = RAIZ / "skills" / "revisao-bancaria"

#: PNG de 1x1 pixel: o logo mínimo dos testes de tema (nenhum logo real entra no repositório).
PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")

if str(SKILL) not in sys.path:
    sys.path.insert(0, str(SKILL))
