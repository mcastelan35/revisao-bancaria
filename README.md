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
| `configurar` | Logo depois de instalar | Registra quem assina (OAB ou CRC), confere o Python e testa o conector |

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
| Resumo para a petição | Os achados organizados para a sua skill de peticionamento | A redação da inicial |
| Agenda de pesquisa | Pedidos de pesquisa de jurisprudência (JusIA), num arquivo interno que nunca entra no laudo | Uso do escritório |

- **Assinatura:** o laudo sai em nome de quem foi configurado. Laudo pericial é assinado por
  contador com CRC; parecer técnico, por advogado com OAB.
- **Sem excesso:** quando não há o que cobrar, o veredito diz isso: "revisão contratual inviável
  — atacar a composição do débito".
- **Conta corrente:** o resultado é uma faixa entre três cenários, não um número fechado, e serve
  para pedir perícia contábil.

## Instalação

No Claude Code (aba **Code** do app Claude, terminal ou IDE):

```
/plugin marketplace add mcastelan35/revisao-bancaria
/plugin install revisao-bancaria@revisao-bancaria
```

No claude.ai, baixe o arquivo `revisao-bancaria-<versão>.plugin` da
[última release](https://github.com/mcastelan35/revisao-bancaria/releases/latest) (ou gere com
`python ferramentas/empacotar_plugin.py`) e envie em **Personalizar › Plugins**.

### Pré-requisito: o conector Radar Apogeu

O plugin trabalha **sempre** com o conector: ele é a fonte única das taxas médias por modalidade,
das séries de indexador e da correção do indébito, servidas de um cache persistente que torna o
laudo reproduzível por terceiro. Sem ele, a revisão não roda.

1. Adicione o conector **Radar Apogeu** em **Configurações › Conectores**.
2. Configure a chave de acesso **no próprio conector** — nunca cole a chave no chat. A chave é
   pessoal e acompanha a assinatura.
3. Abra uma conversa nova.

### Primeiro uso

Diga **"configura a revisão bancária"** (ou rode `/revisao-bancaria:configurar`). O Claude confere
o Python, roda o autoteste dos motores, pergunta quem assina os laudos — advogado com OAB ou
contador com CRC — e confirma o conector com uma chamada.

## Como pedir

| Você diz ou envia | O que acontece |
|---|---|
| "a taxa de 3,2% ao mês do consignado INSS de março de 2023 é abusiva?" | **triagem**: uma consulta ao conector, razão contra a média, limiares e próximo passo |
| contrato, CCB, cédula ou proposta | revisão do **contrato** (L0 a L4) |
| extratos de conta corrente | revisão da **conta** (C0 a C6) |
| faturas do cartão | caminho do **cartão** |
| contrato habitacional, consolidação ou leilão | caminho **SFH/SFI** |
| memória de cálculo de uma execução | auditoria da **memória do credor** antes de recalcular |
| "gera o laudo" ao fim da análise | PREMIUM, PANORAMA e planilha, em nome de quem foi configurado |

## O que tem no repositório

| Pasta ou arquivo | Papel |
|---|---|
| `.claude-plugin/` | Manifestos do plugin: o que o comando de instalação lê |
| `skills/revisao-bancaria/SKILL.md` | O roteiro da análise: ordem das etapas e regras de conduta |
| `skills/revisao-bancaria/camadas/` | Uma instrução para cada etapa |
| `skills/revisao-bancaria/dados/regras-bancarias.json` | A base jurídica: 40 regras, 10 marcos temporais, 23 súmulas, 24 séries do BACEN e as pendências de jurisprudência |
| `skills/revisao-bancaria/motores/` | Os programas de cálculo, o motor de regras e o gerador dos laudos |
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
`gerar` e `operador` — detalhes em [ARCHITECTURE.md](ARCHITECTURE.md).

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
- A identidade de quem assina fica na pasta de dados do plugin, fora do código, e nunca vem
  pré-preenchida.
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
