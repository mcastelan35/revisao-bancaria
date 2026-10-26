# L0 — Intake e datação do contrato

Camada do plugin `revisao-bancaria`. Responsável por receber o contrato, classificar o tipo, extrair dados-chave e resolver os marcos temporais que determinam qual regime jurídico se aplica.

## Entrada

O usuário pode fornecer o contrato de 3 formas (perguntar com botões — `AskUserQuestion` no Claude Code, tap no claude.ai — se não for óbvio):
- Enviar PDF/documento (texto selecionável ou imagem)
- Digitar os dados manualmente
- Enviar múltiplos contratos em sequência

## Extração de PDF

Se PDF com texto selecionável: extrair diretamente. Se PDF imagem: tentar OCR. Se falhar ou se o contrato for protegido: solicitar os dados-chave manualmente ao usuário — nunca travar o fluxo por causa de extração.

## Classificação do tipo de contrato

Classificar usando os 10 tipos do `dados/regras-bancarias.json` → `tipos_contrato`:

| Tipo | Identificadores no contrato | Regras desbloqueadas |
|---|---|---|
| `consumo_pf` | CPF, pessoa física, financiamento PF, crédito pessoal, consignado | Todas as consumeristas |
| `empresarial_pj` | CNPJ, razão social, capital de giro, fomento | Apenas CC/02 + especiais (gate PJ obrigatório) |
| `cedula_rural` | "Cédula de Crédito Rural", DL 167/67, CPR | R17 (12% a.a.) + R20 (capitalização) |
| `cedula_comercial` | "Cédula de Crédito Comercial", Lei 6.840/80 | R17 + R20 |
| `cedula_industrial` | "Cédula de Crédito Industrial", DL 413/69 | R17 + R20 |
| `cartao_credito` | Cartão de crédito, fatura, rotativo, anuidade | R23 (teto 100%) |
| `cartao_consignado` | RMC, RCC, margem consignável, cartão consignado | R24 (alto litígio) |
| `sfh` | Lei 4.380/64, SFH, FGTS/SBPE, CEF/EMGEA, apólice SH/SFH, FCVS, PES/CP, CES, hipoteca | R34, R36, R37, R38, R39, R40 — **R15, R18, R19 desligadas** |
| `sfi` | Lei 9.514/97, alienação fiduciária, consolidação da propriedade, arts. 26/27, leilão extrajudicial | R35, R36, R37, R39, R40 — **R15, R18, R19 desligadas** |
| `imobiliario_fora_sfi` | Construtora/loteadora como credora, promessa de compra e venda, sem banco | R35, R39, R40 — **R15, R18 desligadas** |

**Teste de entrada dos tipos habitacionais.** A classificação decide tudo: a data de
assinatura e a cobertura do FCVS definem se o CDC incide (MT07 — REsp 2.174.331/SP: só
contratos posteriores a 11/03/1991 e sem FCVS), e a data do contrato E a da consolidação
decidem a R40 (MT10). Um mesmo imóvel pode ter contrato SFH antigo refinanciado em SFI —
nesse caso são dois instrumentos (R0-b), um laudo cada.

## Dados-chave a extrair (perguntar o que faltar)

**Obrigatórios — a análise NÃO prossegue sem estes dados:**
- Data do contrato (determina regime jurídico)
- Valor financiado / valor do crédito
- Prazo (número de parcelas)
- **Taxa de juros contratada (mensal E anual) — BLOQUEANTE, ver abaixo**
- Nome e CPF/CNPJ do contratante
- Nome e CNPJ da instituição financeira

**Obrigatórios adicionais nos tipos `sfh` / `sfi` / `imobiliario_fora_sfi`** (campo
`campos_extras_obrigatorios` do tipo no JSON; faltando, a análise não entra na L2):
- Índice de correção do saldo (TR, poupança, IPCA) e o plano de reajuste da prestação
  (PES/CP, categoria profissional, prefixado) — sem isso `tabela_sfh` não roda
- Cláusula de capitalização e sua periodicidade (mensal/anual/silente) — base da R34/R35
- Cláusula expressa de CES e se o CES foi cobrado (R38, só `sfh`)
- Cobertura do FCVS (R38/MT07/MT08, só `sfh`)
- Conta gráfica integral desde a primeira prestação (não só o saldo atual): sem ela, R34 e
  R36 saem `A verificar` e dependem de perícia, que o TRF4 costuma indeferir quando os
  documentos "bastam" — dizer isso no gate
- Data da consolidação da propriedade ou do leilão, endereços e e-mail do contrato, e as
  certidões de notificação do cartório — alimentam a `L2b`

### Taxa de juros — regra de extração obrigatória

A taxa contratada é o dado mais importante da análise. Sem ela, a comparação com a média BACEN não pode ser feita — e essa comparação é o ouro do módulo. A skill DEVE obter a taxa antes de prosseguir. Nunca gerar relatório com "taxa pendente".

Ordem de tentativa para encontrar a taxa:
1. Extrair do corpo do contrato (campo "taxa de juros", "encargos financeiros", CET, ou equivalente)
2. Se o contrato remeter a documento complementar (Proposta de Utilização, Planilha CET, Aditivo), **perguntar ao usuário**: "O contrato remete a taxa de juros a um documento complementar (Proposta de Utilização / Planilha CET). Você tem esse documento? Se sim, envie. Se não, informe a taxa manualmente — ela consta no app do banco, no extrato da operação ou no boleto de pagamento."
3. Se o usuário não tiver nenhum documento, pedir a taxa digitada: "Informe a taxa de juros da operação (mensal e/ou anual). Essa informação consta no extrato, no app do banco ou na central de atendimento."
4. Só se o usuário confirmar que não consegue obter a taxa de nenhuma forma, registrar como "taxa não informada" e aplicar a regra R16 (Súmula 530 — taxa incomprovável → média BACEN como substitutiva).

**Nunca aceitar "pendente" e seguir com relatório parcial.** Ou a taxa é obtida, ou a Súmula 530 é aplicada.

**Importantes (perguntar se não encontrar):**
- Sistema de amortização (Price, SAC, etc.)
- Valor da parcela
- Número do contrato
- Encargos listados (TAC, TEC, tarifa de cadastro, seguro, avaliação, registro, IOF, comissão de correspondente, serviços de terceiros — extrair nome exato e valor de cada um)

**Para contratos PJ (gate obrigatório):**
- Perguntar: "A empresa contratante é vulnerável nesta relação? (porte, faturamento, sofisticação financeira, dependência do crédito)"
- Se SIM → **não basta o sim**. Pedir os elementos concretos e gravá-los em `premissas`:
  faturamento anual, número de empregados, existência de assessoria financeira ou contábil
  própria, destinação do crédito (custeio essencial ou investimento discricionário), e se a
  empresa negociou ou apenas aderiu a instrumento de formulário. Vulnerabilidade de PJ **não se
  presume** e o STJ exige demonstração concreta; sem os elementos, os achados que dependem do
  CDC ficam classificados como `A verificar`, jamais como `Ilícito`, e o laudo declara a
  premissa como afirmada e não comprovada.
- Se NÃO → registrar `cdc_mitigado: false` → aplicar apenas CC/02 e legislação especial. A
  razão contratada/média continua sendo apurada e exibida (R15 dispara em qualquer tipo de
  contrato desde a v5.1); o que muda é a consequência, lida do bloco
  `regime.civil_empresarial` da R15 — sem inversão do ônus, sem art. 51 do CDC, sem dobro

Sinal de alerta a registrar, sem valorar: volume de crédito tomado. Empresa que contratou
várias operações de porte junto à mesma instituição enfrenta contra-argumento óbvio de
sofisticação, e a credora vai levantá-lo. Melhor endereçar na fundamentação do que ser
surpreendido.

### Taxa composta — indexador mais spread

Quando a remuneração for pós-fixada (`CDI + x% a.m.`, `Selic + x`, `TR + x`), a taxa contratada
para fins de comparação com a média BACEN é a **soma composta** do indexador na data da
contratação com o spread: `(1 + i_indexador) × (1 + spread) − 1`. Não comparar o spread isolado
contra a média da modalidade — o erro subestima a taxa em várias vezes e faz operação cara
parecer barata.

Obter o indexador na data pela série diária correspondente (**12** para CDI, **11** para Selic
fator diário, **226** para TR) e converter para a mesma base da série da modalidade, que é
mensal. A série 4390 é a Selic acumulada no mês: serve ao `atualizar_debito`, não a esta
composição. Registrar as duas parcelas
separadamente na ficha de intake, para que a comparação seja auditável.

## Resolução de marcos temporais

`<rb> marcos --data-contrato AAAA-MM-DD [--data-consolidacao AAAA-MM-DD]` devolve a posição do
contrato em cada marco de `marcos_temporais`, com a `base` do corte (contrato, pagamento,
operação ou contrato e consolidação). Não resolver à mão. O que cada marco decide:

| Marco | Data | Pergunta resolvida |
|---|---|---|
| MT01 | 31/03/2000 | Capitalização infraanual permitida? |
| MT02 | 30/04/2008 | TAC/TEC vedadas? Tarifa de cadastro autorizada? |
| MT03 | 25/02/2011 | Comissão de correspondente vedada? |
| MT04 | 01/09/2017 | Comissão de permanência extinta? |
| MT05 | 30/03/2021 | Repetição em dobro? |
| MT06 | 03/01/2024 | Teto de 100% no rotativo do cartão? |
| MT07 | 11/03/1991 | CDC incide no contrato habitacional? (só se posterior e sem FCVS) |
| MT08 | 05/12/1990 | Segundo financiamento com FCVS admite quitação do saldo residual? |
| MT09 | 20/11/1997 | Contrato sob a Lei 9.514 (SFI)? |
| MT10 | 11/07/2017 | Purga da mora até a arrematação (anterior) ou só até a consolidação (posterior)? Datar contrato E consolidação |

Registrar na ficha o objeto que o `<rb> marcos` devolve (`{ MT01: "posterior", … }`).

## Saída (gate para L1)

### Comparação imediata com BACEN (executar ANTES do gate)

Este é o dado mais importante da análise. Se a taxa de juros contratada estiver disponível no contrato:

1. Identificar a série da modalidade com `<rb> serie --buscar "<modalidade>"` (mapeamento
   `series_bacen_por_modalidade`, sem gastar quota). Modalidade ambígua (PF × PJ, consignado
   público × privado × INSS) se pergunta ao usuário; `listar_series_bacen` só se o mapeamento
   não cobrir o caso
2. Consultar a taxa média **já na janela completa do contrato** — data de assinatura até o
   vencimento, que o intake conhece — e extrair daí o ponto da data do contrato. Uma consulta
   só: a L2 e a L3 reaproveitam este mesmo resultado em vez de reconsultar a série. Ver
   `referencia/bacen-consulta.md`; em série mensal, `data_inicial` no **dia 1º**
3. Calcular a razão com `<rb> razao --contratada-pct <taxa> --unidade-contratada
   am_efetiva|aa_efetiva|aa_nominal --media-pct <média do mês> --tipo <tipo>` — a unidade é a
   da cláusula, nunca inferida; a média da série de modalidade já é % a.m.
4. Classificar pelo que o comando devolve: < 1,5x (lícita) / 1,5x–2,0x (zona de abusividade) /
   ≥ 2,0x (fortemente abusiva), com os limiares em % a.m.
5. Incluir o resultado NA FICHA DE INTAKE como o dado mais visível

Se a taxa NÃO estiver no contrato (CCB-quadro, Proposta separada), registrar como pendente e MOSTRAR os limiares: "limiar 1,5x = X% a.a. / limiar 2,0x = Y% a.a."

Apresentar ficha de intake ao usuário com a comparação BACEN em destaque:

```
┌─────────────────────────────────────────┐
│ FICHA DE INTAKE                         │
├─────────────────────────────────────────┤
│ Tipo: [classificação]                   │
│ Contratante: [nome — CPF/CNPJ]         │
│ Instituição: [nome — CNPJ]             │
│ Contrato: [número — data]              │
│ Valor: [R$ X] — Prazo: [N parcelas]    │
│ Taxa: [X% a.m. (Y% a.a.)]             │
│ Sistema: [Price/SAC/outro]              │
│ CDC aplicável: [sim/não/mitigado]       │
│ Marcos: MT01=post MT02=post ...         │
│ Encargos identificados: [lista]         │
│                                         │
│ ═══ COMPARAÇÃO BACEN (imediata) ═══     │
│ Série: [código — nome]                  │
│ Média na data: [X% a.a.]               │
│ Razão: [N,Nx] → [lícita/zona/abusiva]  │
│ Limiar 1,5x: [Y% a.a.]                │
│ Limiar 2,0x: [Z% a.a.]                │
└─────────────────────────────────────────┘
```

**Tipos habitacionais: a comparação BACEN sai da ficha.** Em `sfh`, `sfi` e
`imobiliario_fora_sfi` não consultar a série da modalidade para a R15 (STJ REsp 2.166.103/SP
e TRF4 AC 5010159-78 rejeitam limitar juros no SFH; a tese não existe). A chamada ao conector
nesses tipos é outra: `consultar_indice` da série diária/mensal do índice do saldo (TR 226,
poupança, IPCA) para alimentar `tabela_sfh`. O bloco "COMPARAÇÃO BACEN" da ficha é substituído
por "ÍNDICE DO SALDO: série, janela, ponta, procedência".

Quando a razão ficar abaixo de 1,5x, dizer isso **no próprio gate**, sem esperar a L3:
"a tese de juros abusivos não se sustenta neste contrato; o esforço deve ir para a composição
do débito". Poupa o operador de aprovar camadas inteiras rumo a um resultado que já se sabe
nulo, e é o tipo de contestação que o operador contratou a skill para receber.

Perguntar: "Os dados estão corretos? O tipo de contrato está certo?"

Só prosseguir para L1 após aprovação explícita.
