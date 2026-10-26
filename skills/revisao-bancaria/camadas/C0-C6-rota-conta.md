# C0-C6 — Rota CONTA (conta corrente, cheque especial e conta garantida)

Camada do plugin `revisao-bancaria`. Revisão da movimentação de conta a
partir de extratos. Motor único: `motores/conta_corrente.py` — rodar
`<rb> autoteste` antes da primeira apuração da sessão; se o autoteste falhar, parar e
reportar. Uso numa sessão Python: `from motores import conta_corrente as cc` (com a pasta da
skill no `sys.path`).

**Divisão de responsabilidade (inegociável):** o Claude extrai e classifica (C1, com gate
de aprovação); o motor calcula e **confere a extração** pela reconciliação contra o saldo
impresso no extrato. Nenhum número do entregável nasce fora do motor. Nenhum lançamento
entra no motor sem passar pelo inventário aprovado.

---

## C0 — Intake e qualificação do regime

1. Receber os documentos: extratos (obrigatórios, período contínuo), contrato de abertura
   de conta / termo de adesão ao limite / cédula de conta garantida (se houver), e
   qualquer aditivo de taxa. Registrar o que NÃO veio — a ausência do instrumento é
   informação (alimenta a tese da Súmula 530 e o pedido de exibição na C5).

2. Fixar com o usuário, via gate: período de apuração, **saldo inicial e a data em que ele
   vale** (o saldo de abertura do primeiro extrato e o dia dessa abertura — nunca presumir
   zero; a data entra no motor como `data_inicial`, senão a janela começa no primeiro
   lançamento e o SMD do primeiro mês sai sobre menos dias), titular, banco, agência/conta,
   modalidade (cheque especial PF, cheque especial PJ, conta garantida) e a taxa
   contratada quando comprovada (instrumento ou extrato), com unidade declarada.

3. **Qualificação do regime — prejudicial (regra de conduta 18).** Definir
   `regime = consumerista | civil-empresarial` antes de calcular ou fundamentar qualquer
   coisa. PJ com conta garantida/capital de giro é relação de insumo por regra;
   vulnerabilidade não se presume e exige elementos concretos (porte, faturamento,
   sofisticação, dependência do crédito) — perguntar via gate. Sem CDC caem a inversão do
   art. 6º, VIII, o art. 51, o art. 39, I, e a repetição em dobro.

### Gate C0 → C1
Ficha de intake apresentada e aprovada. Sem saldo inicial e sua data confirmados, não prossegue.

---

## C1 — Extração e inventário de lançamentos

1. Extrair os lançamentos dos PDFs para o **CSV canônico** do motor:
   `data;historico;natureza;valor;classe;rubrica;contrato_ref;saldo_informado`
   Sempre que o extrato imprimir o saldo após o lançamento, preencher `saldo_informado` —
   é o que dá poder à reconciliação. Datas ISO (yyyy-mm-dd); valores em pt-BR estrito: o
   motor **recusa** `1.500` (milhar ou 1,5?) e `1,234.56` (en-US) — escrever `1500,00` ou
   `1.500,00`. Número ambíguo na extração é lacuna, não palpite (regra 0).

2. Classificar cada lançamento:
   - `classe`: ENCARGO (juros, IOF, tarifas, seguros, CP, mora, multa), MOVIMENTO
     (depósitos, saques, TED/PIX, pagamentos, cheques), ESTORNO (com a rubrica do
     encargo estornado — o pareamento evita crédito em dobro no expurgo).
   - `rubrica` (obrigatória em ENCARGO/ESTORNO): juros | iof | tarifa | seguro | cp |
     mora | multa | outro. Aplicar a detecção de CP disfarçada da regra R03
     (12 termos suspeitos em `regras-bancarias.json`, dentro da própria R03) — encargo de
     inadimplência com nome criativo classifica pela **natureza**, não pelo nome.
   - `contrato_ref`: débito identificável como parcela/encargo de contrato externo
     (ex.: "PARC CCB 123") recebe o identificador — alimenta o nexo cruzado (C5).

3. **Rodar a reconciliação — guarda da extração:** `carregar_csv` + `reconciliar(lancs,
   saldo_inicial, data_inicial=<data do saldo inicial>)`. Lançamentos do mesmo dia são
   conferidos pelo fechamento do dia (a ordem intradia do extrato pode diferir da do CSV).
   Veredito DIVERGENTE aponta exatamente onde o saldo recomputado
   descolou do impresso: lançamento perdido, duplicado ou com valor errado na extração.
   Corrigir e rodar de novo. `competencias_sem_lancamento` não vazio = extrato faltante =
   **lacuna bloqueante**: pedir o período ao usuário. A análise NÃO avança com veredito
   DIVERGENTE — este é o `conferir_fator` da rota CONTA.

### Gate C1 → C2
Apresentar o inventário (totais por classe/rubrica, nº de lançamentos, período coberto,
veredito da reconciliação com os pontos conferidos) e a amostra dos ENCARGOs
classificados. Perguntar: "Alguma classificação errada? Algum encargo que não reconhece?"

---

## C2 — Apuração: saldo diário, SMD e perfil da conta

1. `recompor_saldo_diario` + `perfil_conta`: % de dias devedores, maior saldo devedor e
   data. Conta que "roda no vermelho" o tempo todo é o retrato que abre o entregável.

2. `smd_hamburgues` por competência. Convenção padrão `dias_corridos`, declarada na
   metodologia; `dias_devedores` disponível quando o laudo adversário usar essa base
   (impugnação comparável exige mesma régua). Taxa-dia padrão `linear_mes` (taxa mensal ÷
   dias do mês — a única que reproduz exatamente a taxa contratual sobre o SMD em qualquer
   mês); `linear_30` e `exponencial_30` existem só para reproduzir a régua de laudo adverso
   e, quando usadas, a metodologia declara a diferença (3,1% em mês de 31 dias; 29,57 em vez
   de 30,00).

3. **Consulta BACEN — uma chamada.** Identificar a série da modalidade com `<rb> serie`
   (cheque especial PF / cheque especial PJ / conta garantida — mapeamento local, sem quota)
   e trazer o vetor mensal do período inteiro numa única `consultar_taxa_bacen({ codigo,
   data_inicial (dia 1º), data_final })`; a identidade da série volta na própria resposta. Registrar `procedencia` e `ponta`. O vetor
   alimenta o cenário C1_TAXA_MEDIA — competência faltante o motor bloqueia sozinho.

4. Calcular a razão taxa contratada / taxa média (quando a contratada é comprovada) e
   classificar pelos limiares 1,5x / 2,0x, com o alerta permanente do Tema 1378
   (regra crítica da SKILL.md).

### Gate C2 → C3
Painel inline no chat (widget visual quando a sessão tiver a ferramenta; senão tabela
markdown — regra de conduta 10): KPIs (SMD médio, % dias devedores, juros cobrados no
período, razão contratada/média), gráfico do saldo diário, tabela de competências.

---

## C3 — Conformidade da conta

Rodar o motor de regras com o regime qualificado na C0 e o tipo do titular (`consumo_pf` ou
`empresarial_pj`):

```bash
<rb> regras --tipo consumo_pf|empresarial_pj --regime <C0> [--data-contrato <instrumento de abertura/limite, se exibido>]     --categorias tarifas,seguro_prestamista,comissao_de_permanencia,juros_remuneratorios,capitalizacao,juros_moratorios,multa_contratual,iof,repeticao_indebito
```

e aplicar às rubricas inventariadas as regras que ele devolver (tarifas, seguros, CP e
disfarce, mora, multa, IOF), com os cortes temporais já resolvidos. Sem o instrumento, as
regras com corte pela data do contrato voltam em `confirmar` ("data do contrato ausente") —
são pontos a confirmar pela exibição (C5), nunca presunção de data. Somam-se os pontos
próprios da rota:

1. **Capitalização diária × pactuação.** Verificar no instrumento (quando exibido) se a
   capitalização em periodicidade inferior à mensal foi pactuada de forma expressa e
   clara. Sem instrumento, registrar como ponto a confirmar via exibição (C5) — a
   consequência quantitativa é o cenário C2_CAP_MENSAL.

2. **Taxa não comprovada.** Sem instrumento e sem taxa aferível no extrato, aplicar a
   R16 (Súmula 530 — taxa média): consequência quantitativa é o cenário C1_TAXA_MEDIA.

3. **Encargos sem lastro.** Tarifa, seguro ou título de capitalização debitados sem
   pactuação/autorização identificável: marcar a rubrica como expurgável (alimenta
   `rubricas_sem_lastro` da trinca). Distinguir do que é lícito — regra de conduta 8
   (encargos lícitos existem e vão em ressalvas).

### Gate C3 → C4
Relatório de conformidade com semáforo e tier, como na L2. Perguntar quais teses
perseguir e, em consequência, quais rubricas entram no expurgo.

---

## C4 — Recomposição: a trinca de cenários

1. `rodar_trinca(lancs, saldo_inicial, taxa_contratada, taxa_media_vetor,
   rubricas_sem_lastro)`. Os três cenários saem com **condição de aplicabilidade
   declarada** (regra de conduta 20 — a rota CONTA entrega faixa, não ponto):

   | Cenário | Recompõe | Aplicável quando |
   |---|---|---|
   | C1_TAXA_MEDIA | juros pela taxa média BACEN, cap. mensal, expurga sem-lastro | taxa abusiva ou não comprovada (S. 530) |
   | C2_CAP_MENSAL | juros pela taxa contratada, cap. mensal, expurga sem-lastro | taxa hígida, capitalização diária não pactuada |
   | C3_TAXA_LIMPA | mantém juros cobrados, expurga só encargos sem lastro | juros e capitalização válidos |

2. Cenário sem insumo o motor omite com motivo — nunca estimar. Cenário desfavorável
   (`favoravel: false`, ex.: taxa média acima da contratada) é **reportado, não
   escondido**: vai em `ressalvas` do payload — é o que dá credibilidade ao laudo.

3. A imputação do art. 354 do CC está no motor (créditos quitam juros antes do capital);
   com capitalização mensal ela é absorvida pelo saldo único, e a variante
   `capitalizacao="nenhuma"` fica disponível para tese de ausência total de pactuação.
   ESTORNO de juros/mora é tratado simetricamente ao ENCARGO pareado: quando o motor
   recompõe os juros, o estorno abate `juros_cobrados` e não entra como crédito ao capital
   (evita crédito em dobro contra o banco — o erro que derruba o laudo em perícia).

### Gate C4 → C5
Painel dos três cenários lado a lado: excesso final, série por competência, condição de
aplicabilidade. O usuário escolhe o cenário-líder do entregável (os demais permanecem
como faixa).

---

## C5 — Nexo cruzado e exibição de documentos

1. `nexo_cruzado(lancs)`: débitos vinculados a contratos externos, totalizados por
   contrato e período. Em rota AMBAS, é a ponte para o encontro de contas com a rota
   INSTRUMENTO. Em rota CONTA isolada, é registro — o motor não expurga parcela de
   contrato que não foi analisado (regra 0: nunca presumir a ilicitude do instrumento
   que não se leu).

2. **Exibição.** Inventariar os documentos que faltam e que a instituição detém
   (instrumento de abertura/limite, aditivos de taxa, extratos de períodos faltantes) e
   montar o requerimento de exibição para o briefing da peça (arts. 396-404 do CPC).
   Achado dependente de documento ausente é classificado `A verificar`, jamais `Ilícito`.

### Gate C5 → C6
Confirmar a lista de lacunas e o requerimento de exibição.

---

## C6 — Encontro de contas e saída

1. `encontro_de_contas(cenario_lider)`: excesso final, base de repetição simples
   (competências até a que contém 30/03/2021, inteira — critério de menor excesso, declarado
   na `nota`) e base do dobro (posteriores — modulação do Tema 929, condicionada ao regime
   consumerista qualificado na C0). Incrementos negativos entram nas bases: simples + dobro
   fecha com o excesso final.

2. **Correção do indébito → conector, uma chamada.** A série
   `indebito_por_competencia` do cenário vai inteira ao
   `atualizar_debito({ valores: [...], segmentos, data_final })` — cada competência
   corrigida da sua data-base, memória linha a linha e hash de auditoria.

3. **Entregável.** Gate de formato como na L4 (Premium / Panorâmica / os dois / só
   planilha). Enquanto o renderizador (`motores/relatorios.py`) não tiver o ramo CONTA no payload
   (pendência declarada no CHANGELOG), o entregável HTML sai pelo padrão visual
   financeiro com o CSS canônico de `html-pdf-impressao-segura`, contendo
   obrigatoriamente: metodologia (convenções declaradas: hamburguês, base de dias,
   linear_30/exponencial_30, capitalização), veredito da reconciliação com pontos
   conferidos, procedência das séries, trinca com condições, ressalvas e lacunas, e a
   advertência da regra de conduta 20: os valores instruem a perícia e dependem de
   confirmação pericial — o briefing para peça inclui requerimento expresso de prova
   pericial contábil.

4. **Fundamentação jurídica** apenas via `referencia/repertorio-jurisprudencial-contas.md`
   (regra de conduta 3: ementa na íntegra, padrão sanduíche, identificação completa ao
   final). Entrada `[PENDENTE]`/`[CONFERIR]` não se cita — validar antes via
   `pesquisa-jurisprudencial-jusia`. **Enquanto o repertório estiver em ESQUELETO, a rota
   CONTA é beta**: o R0 avisa isso ao escolher a rota, e o entregável declara na metodologia
   que a fundamentação jurídica se limita ao `regras-bancarias.json`.

### Gate pós-entrega
Encerrar / analisar contrato vinculado (rota AMBAS) / gerar petição (briefing para a skill de
peticionamento configurada na L-1) / outro formato.
