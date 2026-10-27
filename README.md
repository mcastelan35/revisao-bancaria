# Revisão bancária — Claude para Advogados

Plugin desenvolvido por **Marcos Vilas Boas** — [fale comigo](https://www.instagram.com/advvilasboas/) (Instagram @advvilasboas).

Plugin que faz do Claude um assistente de revisão de contratos bancários, para advogados e
contadores. Ele lê o documento (contrato, cédula, extrato, fatura ou memória de cálculo do
banco), busca a taxa média oficial do BACEN pelo conector **Radar Apogeu**, aplica 40 regras
jurídicas, recalcula o que for preciso e entrega laudo e planilha. Cobre quatro frentes:

- **Contratos** — financiamento, consignado, capital de giro, cédulas e leasing: Price/SAC,
  pós-fixados (CDI, Selic, TR, IPCA) com reconstrução dia útil a dia útil e auditoria do CET,
  auditoria da memória de cálculo do credor.
- **Cartão de crédito** — faturas, teto de 100% da Lei 14.690/2023, bola de neve da dívida.
- **Financiamento habitacional e imobiliário (SFH/SFI)** — saldo indexado, amortização negativa,
  capitalização vedada e checklist da consolidação da propriedade e dos leilões.
- **Conta corrente, cheque especial e conta garantida** — saldo diário, método hamburguês,
  imputação do art. 354 do CC, três cenários de recomposição e encontro de contas.

Três princípios guiam o plugin:

- **O Claude raciocina, os motores calculam.** Nenhum número do laudo é digitado pelo Claude:
  prestação, saldo, razão de taxa e excesso saem de programas Python testados.
- **Nada é presumido.** Dado que não está no documento nem foi informado por você vira lacuna
  declarada, e a análise para e pergunta.
- **Você controla o fluxo.** Cada etapa termina num ponto de aprovação (gate); nada avança sem o
  seu ok.

## As três skills

| Skill | Quando entra | O que faz |
|---|---|---|
| `triagem` | "Essa taxa de 3,2% ao mês do consignado de 2023 é abusiva?", sem documento | Uma consulta ao conector, a taxa contratada dividida pela média do BACEN e o enquadramento: faixa de mercado, zona de abusividade ou fortemente abusiva |
| `revisao-bancaria` | Você envia contrato, extrato, faturas ou memória de cálculo | A análise completa, em etapas com aprovação |
| `configurar` | Logo depois de instalar | Registra quem assina (OAB ou CRC), oferece a identidade visual do escritório, confere o Python e testa o conector |

## Como uma revisão acontece

1. **A pergunta inicial.** "O que você espera desta análise?", com botões. A resposta define o
   caminho: contrato, cartão, financiamento habitacional, conta corrente ou contrato e conta
   juntos (encontro de contas). Aqui também se contam os documentos: dois contratos geram dois
   laudos.
2. **Quem assina.** O Claude confirma o operador gravado ou, na primeira vez, pergunta.
3. **As etapas do caminho escolhido**, cada uma terminando num gate. Num contrato comum:

| Etapa | O que faz | O que você aprova |
|---|---|---|
| L0 — recepção | Identifica o tipo de contrato, extrai taxa, datas e valores, situa o contrato nas mudanças de regra no tempo e já compara a taxa com a média do BACEN | Os dados extraídos e a comparação |
| L1 — cláusulas | Classifica cada cláusula; reconhece a comissão de permanência disfarçada pela função dela, não pelo nome | O mapa de cláusulas |
| L2 — conformidade | O motor de regras escolhe as regras que valem para o caso, e cada cláusula recebe um semáforo | O painel de achados, mostrado no chat antes de gerar qualquer arquivo |
| L3 — cálculo | Confere a memória de cálculo do banco, recalcula, simula cenários e apura o que foi pago a mais | Os números |
| L4 — entrega | Gera laudo, panorama e planilha | O formato da entrega |

Os outros caminhos trocam o miolo:

- **Cartão:** a análise das faturas substitui as etapas L1 a L3.
- **Financiamento habitacional (SFH/SFI):** ganha a etapa L2b, o checklist da consolidação da
  propriedade e dos leilões.
- **Conta corrente:** tem etapas próprias, de C0 a C6 — inventário dos lançamentos, saldo dia a
  dia, conformidade, três cenários de recomposição, exibição de documentos e encontro de contas.

Há ainda a **auditoria rápida**, que entrega só o semáforo (L0 a L2) num turno.

## As análises

| Área | Regras | O que verifica |
|---|---|---|
| Juros remuneratórios | R15–R17 | Taxa acima de 1,5 vez a média do BACEN (zona de abusividade) ou de 2 vezes (fortemente abusiva); taxa não comprovada, quando a média a substitui (Súmula 530); teto de 12% ao ano nas cédulas rural, comercial e industrial |
| Capitalização | R18–R20, R30 | Pactuação expressa, cédulas e capitalização dos juros de mora |
| Comissão de permanência | R01–R03 | Cumulação com outros encargos, teto e cobrança disfarçada sob outro nome |
| Tarifas e serviços | R04–R12, R29, R32, R33 | TAC e TEC depois de 2008, cadastro, avaliação, registro, serviços de terceiros, correspondente bancário, comissão flat, honorários extrajudiciais e encargo que o devedor não consegue calcular |
| Seguro e IOF | R13, R14, R25 | Venda casada do seguro prestamista; o que for lícito entra nas ressalvas |
| Atraso | R21, R22, R31 | Juros de mora acima de 1% ao mês, multa acima de 2% em relação de consumo e multa sobre base que já inclui juros |
| Devolução do que foi pago a mais | R26, R27 | Em dobro para pagamentos depois de 30/03/2021 (Tema 929); simples antes disso |
| Cartão | R23, R24 | Teto de 100% para os juros do rotativo a partir de 03/01/2024; cartão consignado (RMC/RCC) |
| Financiamento habitacional | R34–R40 | Capitalização vedada, juros não pagos incorporados ao saldo, ordem de correção e amortização (Súmula 450), CES, PES e TR, notificação por edital e purga da mora |
| Prova | R28 | Cabe ao banco provar que a assinatura é autêntica |

A razão entre a taxa contratada e a média do BACEN aparece em toda análise de juros, em
qualquer caminho. Além das regras, duas conferências próprias:

- **Memória de cálculo do banco**, em seis conferências: percentuais uniformes, base da multa,
  desconto das parcelas futuras, índice contra a série oficial, saldo contra as amortizações
  informadas e método anunciado contra o método praticado.
- **Contratos atrelados a CDI, Selic, TR ou IPCA:** o saldo é reconstruído dia útil a dia útil e
  o CET (custo efetivo total) é conferido.

Cada achado sai com duas marcações:

- **Semáforo:** vermelho (ilícito), amarelo (zona cinzenta) ou verde (lícito).
- **Prioridade de ataque:** T1 é tese objetiva e prioritária; T2 depende de prova ou tem
  incerteza; as regras sobre cobranças lícitas não têm prioridade.

Regras suspensas, como a dos juros abusivos enquanto o Tema 1378/STJ estiver pendente, ou sem
precedente consolidado não concluem: aparecem como alerta, e a decisão é do advogado.

## As entregas

| Entrega | O que é | Para quem |
|---|---|---|
| Painel no chat | Semáforo das cláusulas com a prioridade de ataque, antes de qualquer arquivo | Você, para aprovar |
| Laudo PREMIUM | Laudo pericial em A4 com memória de cálculo, achados com fundamento, ressalvas (o que favorece o banco) e lacunas | O processo e o assistente técnico |
| PANORAMA | Duas a três páginas com veredito, indicadores, gráficos comparativos e recomendação | Reunião com o cliente |
| PLANILHA (Excel) | Painel na primeira aba, memória de cálculo, metodologia e lacunas | Conferência independente e anexo |
| PDF | O laudo e o panorama já convertidos, ao lado de cada HTML, quando o computador tem Chrome, Edge, Chromium ou Brave; sem navegador, o HTML abre e se salva como PDF | Juntar aos autos e enviar ao cliente |
| Resumo para a petição | Os achados organizados para a sua skill de peticionamento | A redação da inicial |
| Agenda de pesquisa | Pedidos de pesquisa de jurisprudência (JusIA), num arquivo interno que nunca entra no laudo | Uso do escritório |

- **Assinatura:** o laudo sai em nome de quem foi configurado. Laudo pericial é assinado por
  contador com CRC; parecer técnico, por advogado com OAB.
- **Identidade visual (opcional):** na `configurar`, o plugin importa de uma skill de layout do
  seu escritório as cores, as fontes, o logo, a linha do cabeçalho e o rodapé, e aplica tudo ao
  laudo, ao panorama e à planilha. Sem isso, sai o visual padrão. O semáforo (vermelho, verde e
  âmbar) nunca muda com a marca.
- **Sem excesso:** quando não há o que cobrar, o veredito diz isso: "revisão contratual inviável
  — atacar a composição do débito".
- **Conta corrente:** sai no mesmo padrão dos contratos (laudo, panorama, planilha e PDF), com a
  reconciliação do extrato, os três cenários lado a lado e o encontro de contas. O resultado é uma
  faixa entre os cenários, não um número fechado, e serve para pedir perícia contábil.

## Instalação

O plugin funciona em dois lugares: no **Claude Code** (terminal, aba **Code** do app Claude,
VS Code ou JetBrains) e no **claude.ai** (chat e Cowork). Nos dois, ele precisa do conector
**Radar Apogeu**, que é a fonte das taxas do BACEN.

### Antes de começar

| Precisa de | Para quê | Como conferir |
|---|---|---|
| Assinatura do conector **Radar Apogeu** | Taxas médias, séries e correção do indébito: sem ele a revisão não roda | Ver o passo 1 abaixo |
| Claude Code com **login pela conta claude.ai** (Pro, Max, Team ou Enterprise) | É por esse login que o conector do claude.ai chega ao Claude Code. Login só com chave de API não traz o conector | `/status` mostra a conta. Para trocar, use `/login` |
| **git** | O Claude Code baixa o plugin do GitHub com o git | `git --version` no terminal |
| **Python 3.10+** ou **uv** | Os motores de cálculo são programas Python | Não precisa instalar antes: no primeiro uso, a skill `configurar` confere e, se faltar, oferece instalar o uv, sem pedir administrador |
| **Chrome, Edge, Chromium ou Brave** (opcional) | O PDF do laudo e do panorama sai pronto; sem navegador, o HTML abre no navegador e se salva como PDF | O plugin o encontra sozinho; para indicar um específico, defina `REVISAO_BANCARIA_NAVEGADOR` com o caminho do executável |

### No Claude Code — passo a passo

**1. Ative o conector no claude.ai.** Em [claude.ai › Personalizar › Conectores](https://claude.ai/customize/connectors),
adicione o **Radar Apogeu** e configure a chave de acesso **no próprio conector**. Nunca cole a
chave no chat: ela é pessoal e acompanha a assinatura. Nos planos Team e Enterprise, só o
administrador adiciona conectores.

Depois, numa sessão do Claude Code, rode `/mcp`: o conector deve aparecer como
`claude.ai Radar Apogeu`. Se ele não aparecer, veja [Problemas comuns](#problemas-comuns).

**2. Adicione o marketplace do plugin** (uma vez por computador):

```
/plugin marketplace add mcastelan35/revisao-bancaria
```

A resposta é `Successfully added marketplace: revisao-bancaria`.

**3. Instale o plugin:**

```
/plugin install revisao-bancaria@revisao-bancaria
```

O comando abre a ficha do plugin. Escolha **Install for you (user scope)**: o plugin fica
disponível em qualquer pasta deste computador. Se aparecer `Run /reload-plugins to apply`, rode
`/reload-plugins` (ou abra uma sessão nova).

**4. Confira a instalação.** Digite `/` e procure as três skills, que vêm com o prefixo do plugin:

- `/revisao-bancaria:revisao-bancaria`
- `/revisao-bancaria:triagem`
- `/revisao-bancaria:configurar`

A instalação também aparece na aba **Installed** do `/plugin` e, fora da sessão, no comando
`claude plugin list`.

**5. Configure.** Rode `/revisao-bancaria:configurar` (ou diga "configura a revisão bancária").
Veja o que ela faz em [Primeiro uso](#primeiro-uso).

#### Pelo terminal, sem abrir uma sessão

Os mesmos passos 2 e 3, no PowerShell, no Prompt de Comando ou no terminal do Mac e do Linux:

```
claude plugin marketplace add mcastelan35/revisao-bancaria
claude plugin install revisao-bancaria@revisao-bancaria
```

O plugin carrega na próxima sessão do Claude Code. Para instalar só para um projeto, acrescente
`--scope project` (vale para todos que trabalham no repositório) ou `--scope local` (só para você,
só nesse repositório).

#### No app desktop e no VS Code

- **Aba Code do app Claude:** adicione o marketplace uma vez pelo terminal
  (`claude plugin marketplace add mcastelan35/revisao-bancaria`). Depois, clique no **+** ao lado
  da caixa de mensagem, em **Add plugins** (ou **Plugins › Browse plugins**), escolha
  `revisao-bancaria` e o escopo.
- **VS Code:** digite `/plugins` para abrir **Manage plugins**. Na aba **Marketplaces**,
  adicione `mcastelan35/revisao-bancaria`. Na aba **Plugins**, procure `revisao-bancaria` e
  clique em **Install**.
- **JetBrains:** use os comandos do terminal do próprio IDE.

O terminal, o app desktop e o VS Code no mesmo computador compartilham a instalação: o plugin
instalado para o usuário num deles aparece nos outros.

#### Atualizar

Para marketplaces de terceiros, a atualização automática vem **desligada**. Há três jeitos de
atualizar:

- **Automático:** em `/plugin`, aba **Marketplaces**, selecione `revisao-bancaria` e clique em
  **Enable auto-update**. A partir daí, cada sessão nova já traz a última versão.
- **Pelo terminal:** `claude plugin update revisao-bancaria@revisao-bancaria`.
- **Pelo painel:** em `/plugin`, aba **Installed**, abra `revisao-bancaria` e clique em **Update now**.

A sessão que estava aberta continua com a versão antiga até você rodar `/reload-plugins`. As
novidades de cada versão estão no [CHANGELOG](CHANGELOG.md) e nas
[releases](https://github.com/mcastelan35/revisao-bancaria/releases).

#### Desativar ou remover

Para desligar sem desinstalar, use `claude plugin disable revisao-bancaria@revisao-bancaria` (e
`enable` para religar). Para desinstalar, use
`claude plugin uninstall revisao-bancaria@revisao-bancaria`. Pelo painel, a aba **Installed** do
`/plugin` faz o mesmo.

#### Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `/mcp` não lista `claude.ai Radar Apogeu` | Claude Code logado por chave de API, conector não adicionado no claude.ai ou conectores do claude.ai desligados | Rode `/login` e entre com a conta claude.ai que tem o conector. Confira o passo 1. Veja se a variável `ENABLE_CLAUDEAI_MCP_SERVERS` está como `false` |
| O conector aparece, mas a consulta falha por autenticação | Chave do conector expirada ou não configurada | Reconecte o conector em [claude.ai › Personalizar › Conectores](https://claude.ai/customize/connectors) |
| `/plugin isn't available in this environment` | Sessão não interativa (`claude -p`) | Instale pelo terminal, com os comandos `claude plugin` |
| O marketplace não é adicionado | git ausente ou sem acesso ao GitHub | Instale o git e tente de novo. Atrás de proxy, confira o acesso a `github.com` |
| As skills não aparecem depois de instalar | Plugin pendente de recarga | Rode `/reload-plugins` ou abra uma sessão nova. Os erros de carga aparecem na aba **Errors** do `/plugin` |
| A sessão é na nuvem (claude.ai/code) | Sessões na nuvem não carregam os plugins instalados no seu computador | Use o Claude Code local ou o claude.ai com o arquivo `.plugin` |

### No claude.ai (chat e Cowork)

Baixe o arquivo `revisao-bancaria-<versão>.plugin` da
[última release](https://github.com/mcastelan35/revisao-bancaria/releases/latest) (ou gere com
`python ferramentas/empacotar_plugin.py`) e envie em **Personalizar › Plugins**. O conector Radar
Apogeu é ativado no mesmo lugar do passo 1.

Plugins ligados na sua conta claude.ai também chegam ao Claude Code do mesmo login, com o nome
`revisao-bancaria@synced`. Se você usar os dois caminhos, deixe só uma cópia ativa no Claude Code
(aba **Installed** do `/plugin`), para não carregar duas versões ao mesmo tempo.

### Primeiro uso

Diga **"configura a revisão bancária"** (ou rode `/revisao-bancaria:configurar`). O Claude confere
o Python, roda o autoteste dos motores, pergunta quem assina os laudos — advogado com OAB ou
contador com CRC —, oferece a identidade visual do escritório (se houver uma skill de layout na
sua sessão) e confirma o conector com uma chamada.

## Como pedir

| Você diz ou envia | O que acontece |
|---|---|
| "a taxa de 3,2% ao mês do consignado INSS de março de 2023 é abusiva?" | **triagem**: uma consulta ao conector, razão contra a média, limiares e próximo passo |
| contrato, CCB, cédula ou proposta | revisão do **contrato** (L0 a L4) |
| extratos de conta corrente | revisão da **conta** (C0 a C6) |
| faturas do cartão | caminho do **cartão** |
| contrato habitacional, consolidação ou leilão | caminho **SFH/SFI** |
| memória de cálculo de uma execução | auditoria da **memória do credor** antes de recalcular |
| "gera o laudo" ao fim da análise | PREMIUM, PANORAMA, planilha e os PDFs, em nome de quem foi configurado e com a identidade visual do escritório, se houver |

## O que tem no repositório

| Pasta ou arquivo | Papel |
|---|---|
| `.claude-plugin/` | Manifestos do plugin: o que o comando de instalação lê |
| `skills/revisao-bancaria/SKILL.md` | O roteiro da análise: ordem das etapas e regras de conduta |
| `skills/revisao-bancaria/camadas/` | Uma instrução para cada etapa |
| `skills/revisao-bancaria/dados/regras-bancarias.json` | A base jurídica: 40 regras, 10 marcos temporais, 23 súmulas, 24 séries do BACEN e as pendências de jurisprudência |
| `skills/revisao-bancaria/motores/` | Os programas de cálculo, o motor de regras e o gerador dos laudos (com a identidade visual e o PDF) |
| `skills/revisao-bancaria/revisao.py` | O comando que o Claude usa para acionar os motores |
| `skills/revisao-bancaria/referencia/` | Como consultar o conector, o formato dos dados do laudo e a pesquisa de base |
| `skills/triagem/`, `skills/configurar/` | As duas skills auxiliares |
| `tests/`, `.github/workflows/` | A suíte de testes, que roda a cada envio ao GitHub |
| `ferramentas/` | O verificador de consistência e o gerador do arquivo `.plugin` para o claude.ai |
| [ARCHITECTURE.md](ARCHITECTURE.md), [CHANGELOG.md](CHANGELOG.md), [CONECTOR.md](CONECTOR.md) | Mapa técnico, histórico de versões e uso do conector sem o plugin |

Antes do primeiro cálculo de cada conversa, os motores fazem um autoteste; se algo falha, a
análise para.

## Linha de comando

Os motores ficam em `skills/revisao-bancaria/motores/` (Python 3.10+, só biblioteca padrão; a
planilha usa `openpyxl`). O Claude os chama pela linha de comando, que também serve para conferir
à mão:

```bash
python skills/revisao-bancaria/revisao.py autoteste
python skills/revisao-bancaria/revisao.py regras --tipo consumo_pf --regime consumerista --data-contrato 2022-05-10 --formato resumo
python skills/revisao-bancaria/revisao.py razao --contratada-pct 3.2 --media-pct 1.75
python skills/revisao-bancaria/revisao.py serie --buscar "cheque especial"
```

Subcomandos: `autoteste`, `regras`, `regra`, `sumula`, `marcos`, `serie`, `razao`, `comparar`,
`gerar`, `operador` e `tema` — detalhes em [ARCHITECTURE.md](ARCHITECTURE.md). O `gerar` converte
os HTML em PDF sozinho quando acha um navegador Chromium (`--pdf nao` desliga).

## Testes e manutenção

```bash
uv run --no-project --python 3.12 --with pytest --with openpyxl pytest   # suíte completa
python ferramentas/verificar_consistencia.py                             # documentos × JSON × motores × manifestos
python ferramentas/empacotar_plugin.py                                   # dist/revisao-bancaria-<versão>.plugin
```

O GitHub Actions roda a suíte a cada envio, no Windows e no Linux. A versão é uma só — manifestos,
`SKILL.md`, `regras-bancarias.json`, `motores/__init__.py`, CHANGELOG e ARCHITECTURE — e a
consistência falha se divergirem. Quem já instalou só recebe código novo quando a versão sobe.

## Privacidade e limites

- Contratos, extratos e faturas são lidos na sua sessão do Claude e não entram neste repositório
  (o `.gitignore` bloqueia PDFs, planilhas, HTML e payloads). Ao conector vão apenas códigos de
  série, datas e, na correção do indébito, valores e datas de pagamento — nunca nome, CPF ou o
  documento.
- A identidade de quem assina e a identidade visual do escritório (`operador.json` e `tema.json`)
  ficam na pasta de dados do plugin, fora do código, e nunca vêm pré-preenchidas.
- A razão contratada/média é aritmética; a tese de juros abusivos depende do Tema 1378/STJ,
  pendente. Regras suspensas ou sem precedente consolidado não concluem: a decisão é do advogado.
- Jurisprudência só do acervo do plugin, com ementa integral; o que não estiver lá vai para
  pesquisa (JusIA). A rota CONTA é **beta** enquanto o repertório jurisprudencial dela estiver em
  esqueleto.
- Os valores da rota CONTA são faixa, não ponto, e instruem a perícia contábil.
- Todo entregável é sujeito a revisão por advogado(a) ou contador(a) responsável.

---

Desenvolvido por **Marcos Vilas Boas** — Claude para Advogados. Dúvidas, sugestões e contato:
[instagram.com/advvilasboas](https://www.instagram.com/advvilasboas/).
