---
name: configurar
description: "Configura o plugin de revisao bancaria: identifica quem assina os laudos (advogado com OAB ou contador com CRC, nome, entidade, cidade e skill de peticionamento), confere o Python e o openpyxl, roda o autoteste dos motores e confirma o conector Radar Apogeu, fonte das taxas do BACEN. Use logo depois de instalar o plugin, quando a revisao pedir a identificacao do operador, ou quando o usuario disser 'configura a revisao bancaria', 'muda o nome do laudo', 'trocar OAB', 'trocar CRC', 'o plugin de revisao nao funciona'."
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - Bash(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - PowerShell(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - Bash(uv run --no-project --python 3.12 --with openpyxl python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - PowerShell(uv run --no-project --python 3.12 --with openpyxl python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
---

# Configuração — revisão bancária

Objetivo: numa conversa só, o usuário sai com o ambiente conferido, o operador gravado e o
conector confirmado. Linguagem simples, uma etapa por vez, perguntas com botões quando a sessão
tiver (`AskUserQuestion`).

**Comando base** (`<rb>`): `python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"`
— no Windows, `python` no lugar de `python3`.

## 1. Python

Os motores exigem Python 3.10 ou mais novo, só com a biblioteca padrão; a planilha XLSX exige
também o `openpyxl`. Confira `python3 --version` (no Windows, `python --version` ou
`py -3 --version`).

- Sem Python adequado: ofereça o **uv** (instalador oficial da astral.sh, não pede
  administrador) e só rode depois da confirmação — Windows (PowerShell):
  `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`;
  Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`. Logo após instalar, o uv ainda
  não está no PATH da sessão: use o caminho completo (`~/.local/bin/uv`; no Windows
  `& "$env:USERPROFILE\.local\bin\uv.exe"`). O comando base passa a ser
  `uv run --no-project --python 3.12 --with openpyxl python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"`.

## 2. Autoteste

`<rb> autoteste`. Resuma em uma linha. Falha → mostre a linha do módulo que falhou e pare:
análise com motor quebrado não sai. `relatorios` PULADO quer dizer `openpyxl` ausente: o laudo
HTML sai, a planilha não. Ofereça instalar (`python3 -m pip install --user openpyxl`, com
confirmação) ou usar o comando base com uv, que traz o `openpyxl` sem instalar nada no sistema.

## 3. Operador — quem assina os laudos

`<rb> operador mostrar --config-dir "${CLAUDE_PLUGIN_DATA}"`.

- Já configurado: mostre nome, registro e entidade e pergunte se mantém.
- Código 3 (não configurado) ou pedido de troca: pergunte
  1. **tipo** — `advogado` (OAB) ou `contador` (CRC). Explique que o tipo muda o entregável:
     laudo pericial para o contraditório é assinado por contador com CRC; parecer técnico que
     instrui peça é assinado por advogado com OAB;
  2. **nome**, **registro** (OAB/UF 00.000 ou CRC/UF 000000/O), **entidade** (sociedade ou
     escritório, se houver) e **cidade** da assinatura (Cidade-UF);
  3. **skill de peticionamento** que recebe o briefing ao fim da análise (opcional). Se houver
     skills de petição instaladas na sessão, ofereça-as pelo nome; nunca invente.

  Grave: `<rb> operador salvar --tipo … --nome "…" --registro "…" --entidade "…" --cidade "…" --skill-peticao "…" --config-dir "${CLAUDE_PLUGIN_DATA}"`.
  Mostre os `avisos` (registro fora do padrão OAB/CRC). Os dados ficam na pasta de dados do
  plugin, fora do código: sobrevivem a atualizações e nunca entram no repositório.

Nunca preencha nome, OAB ou CRC por conta própria nem reaproveite os de outra pessoa.

## 4. Conector Radar Apogeu

A revisão depende do conector: é a fonte única das taxas e índices do BACEN.

- Se as ferramentas do conector estão na sessão (`consultar_taxa_bacen`, `status_conta`), faça
  **uma** chamada a `status_conta` e mostre o plano e o uso de chamadas do mês — chamada é a
  unidade de quota. Nenhuma outra chamada de teste.
- Se não estão: oriente a adicionar o conector Radar Apogeu em **Configurações → Conectores**,
  com a chave de acesso configurada **no próprio conector** — nunca colada no chat — e a abrir
  uma conversa nova depois.

## 5. Fechamento

Resumo em até cinco linhas: Python, autoteste, operador, conector, e como começar —
"envie o contrato, o extrato ou as faturas" (skill `revisao-bancaria`) ou "essa taxa é
abusiva?" (skill `triagem`).
