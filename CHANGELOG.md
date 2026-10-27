# CHANGELOG

## [Não lançado]

Entregáveis padronizados: a rota CONTA ganha o renderizador, o laudo ganha a identidade visual do
escritório e o `gerar` passa a entregar o PDF. **Nenhum cálculo, tese, súmula, tier, limiar ou
regra mudou**. O HTML sem tema só difere do anterior na contagem inteira da memória, que sai sem
casas ("1", não "1,00"). A versão do pacote segue 6.0.0.

### Ramo CONTA no renderizador

- Payload com `ramo: "conta"` (o padrão segue `"instrumento"`): o bloco `conferencia` dá lugar ao
  bloco `conta` — reconciliação do extrato, trinca de cenários, líder, encontro de contas, séries
  consultadas e, opcionalmente, a correção do conector. Especificação em
  `referencia/payload-schema.md`, "Ramo CONTA" (substitui a seção "Ramo CONTA — pendente").
- `conta_corrente.bloco_payload(reconciliacao, trinca, cenario_lider, encontro, series, correcao)`
  monta o bloco a partir das saídas dos motores, sem número digitado.
- PREMIUM com a seção 3 "Reconciliação do extrato e recomposição da conta" e a advertência fixa da
  regra de conduta 20; PANORAMA com selo do cenário líder (o CONFORME do extrato não vira "sem
  excesso"), barras dos cenários não omitidos e a mesma advertência; PLANILHA com reconciliação,
  trinca e encontro no Dashboard e as séries na aba de metodologia. Rótulos amigáveis dos cenários
  em `ROTULOS_CENARIOS`.
- Validação do ramo: reconciliação DIVERGENTE ou competência sem lançamento é erro (lacuna
  bloqueante da C1), líder inexistente ou omitido, simples + dobro que não fecha com o excesso
  final (tolerância de 0,01) e cenário desfavorável sem `ressalvas`.
- C6: o entregável passa a sair por `<rb> gerar`; o fallback em HTML manual com o CSS de
  `html-pdf-impressao-segura` foi removido, e a regra de conduta 14 não tem mais exceção de rota.

- Cenário omitido por falta de taxa leva motivo legível no laudo ("nenhuma taxa comprovada nos
  documentos para este cenário"), não a mensagem interna do motor.

### Identidade visual do escritório

- `motores/tema.py`: `tema.json` na mesma pasta do `operador.json`, com esquema fechado — cores
  (`tinta`, `destaque`, `destaque_claro`, `fundo_destaque`), fontes (`titulo`, `texto`, `mono`),
  `fontes_url` do Google Fonts, `logo` (PNG, JPG ou SVG de até 300 KB, embutido no cabeçalho e
  copiado para a pasta de dados), `cabecalho_linha` e `rodape`. As cores do semáforo não são
  configuráveis. `render_premium`, `render_panorama`, `render_planilha` e `gerar` aceitam `tema=`.
- `revisao.py tema mostrar|salvar --arquivo|remover`; o `gerar` lê o tema da pasta de configuração
  (`--sem-tema` força o padrão) e informa `"tema"` no JSON. `operador salvar --skill-layout`
  registra a skill de layout escolhida (só registro).
- `configurar`: nova etapa "Identidade visual", que importa o tema de uma skill de layout do
  escritório quando houver uma na sessão.

### PDF pelo `gerar`

- `motores/pdf.py`: converte cada HTML gerado em PDF, ao lado dele, com Chrome, Edge, Chromium ou
  Brave instalado (`REVISAO_BANCARIA_NAVEGADOR` indica um), em headless e com perfil temporário.
  Sem navegador o HTML segue e o JSON traz `"pdf": {"gerado": false, "motivo": …}`; com navegador
  traz `arquivos` e `paginas`, e avisa quando o PANORAMA passa de três páginas.
- `gerar --pdf auto|sim|nao` (padrão `auto`; `sim` sem PDF sai com código 1).
- L4, passo 5: a paginação passa a ser conferida pelas `paginas` do JSON do `gerar`.

### Testes

Novos `tests/test_tema.py`, `tests/test_pdf.py` (navegador simulado e, havendo navegador, uma
conversão de verdade) e `tests/test_conta_relatorio.py` (do motor ao laudo); o autoteste do
renderizador e o do motor da conta cobrem o ramo CONTA e o bloco do payload.

## v6.0.0 — 26/10/2026 — Plugin `revisao-bancaria`

A skill `revisao-contratos-bancarios` vira o plugin `revisao-bancaria`, no padrão dos demais
plugins do autor: o repositório é plugin e marketplace ao mesmo tempo, instalável no Claude
Code e no claude.ai. **Nenhuma tese, súmula, tier, status, limiar ou consequência mudou** — as
mudanças são de estrutura, de economia de tokens e de quota, de alinhamento com o conector e de
sigilo.

### Estrutura

- `skills/revisao-bancaria/`: orquestrador (`SKILL.md`), `camadas/` (as antigas sub-skills de
  `skills/` e a análise de faturas de cartão), `referencia/` (protocolo do conector, schema do
  payload, pesquisa, repertório CONTA, teste do catálogo), `dados/regras-bancarias.json`,
  `motores/` (pacote Python) e `revisao.py` (linha de comando).
- Motores renomeados e importáveis como pacote: `motor-calculo.py` → `motores/calculo.py`,
  `motor-cet.py` → `motores/cet.py`, `motor-cartao.py` → `motores/cartao.py`,
  `motor-conta-corrente.py` → `motores/conta_corrente.py`, `gerar-relatorios.py` →
  `motores/relatorios.py`. `carregar_motores.py` aposentado. Autoteste uniforme
  (`autoteste()` em cada módulo); o do renderizador roda sem `openpyxl`, pulando só a planilha.
- Skills novas: `triagem` (taxa contratada × média BACEN sem documento, com uma chamada ao
  conector) e `configurar` (operador, ambiente e conector).
- `ferramentas/verificar_consistencia.py` (antes `reference/verificar-consistencia.py`) passa a
  conferir também os manifestos do plugin e os nomes antigos no JSON; `ferramentas/empacotar_plugin.py`
  gera o `.plugin` para o claude.ai. Suíte `pytest` em `tests/` (355 testes: motores, motor de
  regras, operador, linha de comando e pacote) e GitHub Actions em Windows e Linux, inclusive no
  Python 3.10 e sem `openpyxl`.

### Motor de regras determinístico (pendência 3 da v5.x)

- `motores/regras.py` e `revisao.py regras`: recebe tipo, regime, datas e categorias e devolve
  `aplicaveis`, `confirmar` e `nao_aplicaveis` com motivo; corte temporal pela base certa
  (contrato, pagamento, operação, contrato e consolidação); consequência e tier por regime
  (R15) e por marco (R03); regras desligadas; `conclusiva`; pendências e alertas vencidos
  calculados na data da análise.
- Antes, L1, L2 e C3 mandavam carregar o JSON inteiro (105 KB) e interpretar à mão a cada
  análise; agora o agente recebe só as regras do caso.
- JSON: `base` em cada marco temporal, `nota_base`, `tipos_contrato.grupos` derivado dos tipos
  e `credor_sfn: false` em `imobiliario_fora_sfi`.
- Regra de conduta 28: aplicabilidade sai do motor; `confirmar` é pergunta ao operador.

### Linha de comando `revisao.py`

`autoteste` (resumo compacto), `regras`, `regra`, `sumula`, `marcos`, `serie`, `razao`
(aritmética decimal, limiares lidos da R15, recusa nos tipos habitacionais), `comparar`
(Price/SAC contratado × revisado), `gerar` (renderizador, com marca e assinatura do operador) e
`operador`.

### Operador (L-1)

- Gravado em `${CLAUDE_PLUGIN_DATA}/operador.json` — a pasta de dados do plugin, que sobrevive a
  atualizações. Antes ficava em `config/operador.json` dentro da pasta da skill, que se perde a
  cada atualização do pacote.
- `revisao.py gerar` preenche `marca` e `assinatura` a partir do operador quando o payload não
  as traz: identidade não é mais copiada à mão para o payload.

### Conector Radar Apogeu

- O código da série sai do mapeamento local (`revisao.py serie`) e a identidade da série volta
  na própria resposta de `consultar_taxa_bacen`: `listar_series_bacen` sai do caminho normal.
  Caso típico: de duas para uma chamada de dado.
- `atualizar_debito`: documentados `regra: civil_lei_14905` (`juros_desde`,
  `indice_correcao_anterior`), `pro_rata_die`, `art_523`, multa e honorários. O regime de
  correção do indébito é escolha do operador no gate da L3/C6, declarada na metodologia.
- Catálogo reconferido em 26/10/2026: 48 séries no conector; as 24 do mapeamento conferem em
  código, nome e unidade. Documentadas as séries de índice do saldo (7811, 196, 195, 25), de
  correção (7478, 7447, 190, 13522, 1178, 29543) e as anuais 207xx, impróprias à razão.

### Corrigido

- `payload-schema.md`: a advertência do fallback CONTA apontava a regra de conduta 21 (agenda
  de pesquisa); a certa é a 20 (faixa de valores e perícia).
- `--formatos` com nome desconhecido gerava zero arquivos em silêncio; agora é erro com a lista
  dos formatos válidos.
- R34 e R36 apontavam `requer_motor` para o nome antigo do motor; agora
  `motores/calculo.py::comparar_sfh` e `::tabela_sfh`.

### Sigilo — repositório público

- Retirados do pacote: número de processo e instituição de um caso real que constavam do
  CHANGELOG, identificadores de caso nos exemplos do schema do payload, o nome de terceiro no
  repertório CONTA, a referência ao escritório do autor no gate pós-entrega, nomes internos do
  código do conector (repositório, tabelas e arquivos) e os nomes e o fragmento de OAB do
  operador original que o autoteste do renderizador guardava — a conferência passa a ser por
  padrão de OAB/CRC no módulo e, para nomes, pela lista local da verificação de consistência,
  fora do repositório.
- Teste que barra número de processo da Justiça Estadual em qualquer arquivo versionado.
- `.gitignore` bloqueia PDFs, planilhas, HTML, payloads e a configuração do operador.

## v5.2 — 09/10/2026 — Ramo SFH/SFI e correção da amortização negativa

Origem: pesquisa jurisprudencial pelo conector Jusbrasil (21 buscas, 30 inteiros teores em
STJ e TRF4, 2016–2026) para mapear abusividades em SFH e SFI. Conclusão que motivou a versão:
a lógica central da rota INSTRUMENTO (duodécuplo + Súmula 539 validam capitalização; razão
1,5x da média BACEN como tese de juros) está invertida para contratos habitacionais e, aplicada
neles, produz laudo contra o cliente. As frentes que ainda rendem são documentais: conta
gráfica (amortização negativa) e certidões do procedimento de consolidação.

### Corrigido — motor (defeito que produzia achado falso em silêncio)

**motor-calculo.py** (v1.3.0; 64 → 77 asserções)
- `amortizacao_negativa()` testava `amortizacao < juros` — situação NORMAL do início de qualquer
  Price — e acusava amortização negativa onde não há. Critério correto: `amortizacao < 0`
  (prestação não cobre os juros; TRF4 AC 5002846-95; STJ REsp 1.476.395/RS). O docstring
  também afirmava que cronograma tabelado produz saldo crescente: impossível, a amortização
  tabelada é `saldo × pct ≥ 0` (amortização lenta, não negativa). Teste anterior passava por
  testar o motor contra ele mesmo — o padrão que a v5.1 já havia apontado nos outros motores.
- Novo `tabela_sfh(pv, r, indexador[], prestacoes[], ordem, juros_impagos)`: saldo indexado
  competência a competência, correção ANTES da amortização (Súmula 450; `amortiza_antes` só
  como contrafactual), juros impagos em conta apartada só com correção (cenário revisado) ou
  incorporados ao saldo (cenário do credor). Nada é presumido: série do índice e prestações
  vêm do documento/conector; comprimentos diferentes ou lista vazia são lacuna bloqueante.
- Novo `comparar_sfh()`: credor × revisado; `anatocismo` = diferença das dívidas totais
  (saldo + conta apartada), que é exatamente o juro sobre juros impagos.
- Fixture calculada à mão (PV 1.000, 1% a.m., índice 2%, prestação 5, duas competências):
  apartada 10,708; saldo incorporado 1.051,16104; anatocismo 0,05304. Sem amortização
  negativa os dois cenários coincidem (anatocismo zero).

### Adicionado — motor de regras (v5.2)

- Tipos `sfh`, `sfi`, `imobiliario_fora_sfi` com `regras_desligadas` (R15; R18/R19) e
  `campos_extras_obrigatorios` (índice do saldo, plano de reajuste, periodicidade da
  capitalização, CES, FCVS, conta gráfica integral, data da consolidação, certidões).
- R34 SFH — capitalização em qualquer periodicidade; Price por si não prova (REsp 2.168.394/SP,
  REsp 2.103.041/DF); prova pela conta gráfica em `comparar_sfh`. T1.
- R35 SFI e fora do SFN — capitalização inferior à anual vedada mesmo pactuada
  (REsp 2.086.650/MG, 07/02/2025; AgInt AREsp 2.738.974/MG; AgInt EDcl AREsp 3.050.638/SE).
  T1, com alerta: recepção no TRF4 não localizada no acervo.
- R36 Amortização negativa — conta apartada (TRF4 AC 5002846-95; REsp 1.476.395/RS, que também
  fixa que a amortização negativa NÃO afasta a mora). T2.
- R37 Súmula 450 — ordem correção/amortização consolidada contra o mutuário; registrada para
  ir em ressalvas e calibrar `ordem='corrige_antes'`.
- R38 CES sem cláusula expressa (REsp 2.166.103/SP; REsp 2.174.331/SP); TR válida (Súmula 454,
  REsp 969.129/MG repetitivo); repetição simples salvo má-fé. T2, alerta de prescrição.
- R39 Notificação por edital sem esgotar diligências; ciência do leilão não supre
  (REsp 2.107.242/ES, 17/08/2026; REsp 2.218.731/PE); contrários registrados (REsp 1.977.553/SP
  — prejuízo concreto; REsp 1.698.322/RJ; TRF4 AC 5000201-87). T1.
- R40 Purga até a arrematação em contratos/consolidações anteriores à Lei 13.465/2017 —
  `sem_precedente_consolidado`: STJ diverge sobre o critério temporal (REsp 2.187.505/SP ×
  REsp 2.005.064/GO), TRF4 hostil.
- MT07 CDC 11/03/1991 (REsp 2.174.331/SP: só posteriores e sem FCVS); MT08 FCVS 05/12/1990
  (TRF4 AC 5018577-45); MT09 Lei 9.514 20/11/1997; MT10 Lei 13.465 11/07/2017.
- Categorias `habitacional_sfh_sfi` e `procedimento_expropriatorio`; Súmulas 450 e 454.
- Pendências: critério temporal da purga; recepção do REsp 2.086.650 no TRF4 (verificado_em
  09/10/2026).

### Adicionado — sub-skills e orquestrador

- `skills/L2b-procedimento-expropriatorio.md`: checklist documental de 9 itens com semáforo
  (diligências antes do edital, prazo de purga, recusa × frustração, averbação, comunicação
  dos leilões, prazo de 30 dias, piso do 2º leilão, purga tardia, prejuízo concreto no DL 70/66),
  com o bloco contrário obrigatório em `ressalvas`.
- R0: opção "financiamento habitacional ou imobiliário" como ramo próprio da rota INSTRUMENTO,
  com a explicação de por que a leitura do SFN não serve.
- L0: três tipos novos na classificação, campos extras obrigatórios, MT07–MT10, e a ficha
  troca o bloco "COMPARAÇÃO BACEN" por "ÍNDICE DO SALDO" (`consultar_indice`) nesses tipos.
- L2: passo 0 (remover `regras_desligadas` antes do filtro; carregar L2b) e seis perguntas de
  gate interno para R34–R40.
- SKILL.md: descrição com os gatilhos habitacionais; regra de conduta 27; linha do ramo na
  tabela de rotas; exceção explícita na regra crítica de juros.

### Não feito nesta versão (ver ARCHITECTURE → Pendências 7 e 8)

- Identificação completa (relator, órgão, data de julgamento) dos 15 precedentes novos: o
  acervo devolveu só ementa e data-base; estão marcados `[CONFERIR]` e a regra de conduta 3
  impede citá-los em peça até que o operador complete no portal do tribunal.
- Ramo `sfh` no `gerar-relatorios.py` e no `payload-schema.md`: o laudo SFH/SFI sai pela rota
  `recomposicao` com a conta apartada declarada em texto na metodologia.
- Fixture real de conta gráfica da CEF para congelar a convenção de arredondamento.

## v5.1 — 20/09/2026 — Auditoria de consistência e correção dos motores

Sessão de auditoria completa do pacote (documentação, motor de regras, cinco motores Python,
renderizador e protocolo do conector). Os cinco autotestes passavam — e escondiam seis bugs de
cálculo que produziam número errado sem avisar, porque testavam o motor contra ele mesmo. A
documentação havia descolado do código em quinze pontos. Nenhum comportamento jurídico novo
foi introduzido sem registro abaixo.

### Corrigido — motores (defeitos que produziam número errado em silêncio)

**motor-conta-corrente.py** (v1.1.0; 34 → 63 asserções)
- ESTORNO de juros/mora entrava como crédito ao capital enquanto o ENCARGO pareado era
  expurgado: crédito em dobro contra o banco (saque 1.000, juros 100, estorno 100 → excesso
  +70,10 em vez de −35,33). Agora simétrico ao ENCARGO.
- `_parse_num("1.500")` devolvia 1,5 e `"1,234.56"` devolvia 1,23456 sem erro. Parse pt-BR
  estrito em `comum.parse_num_ptbr`: ambiguidade é lacuna, não palpite (regra 0).
- Janela de apuração começava no primeiro lançamento: saldo inicial em 01/01 com primeiro
  lançamento em 15/01 apurava SMD e juros de janeiro sobre 17 dias. Novo parâmetro
  `data_inicial` (data do saldo informado), propagado por `reconciliar`, `recompor_cenario`
  e `rodar_trinca`; a C0 passa a exigir a data do saldo inicial.
- Lançamentos fora de ordem cronológica eram silenciosamente descartados — ordenação estável
  em todas as entradas.
- Convenção de taxa-dia: `linear_30` cobrava 3,1% em mês de 31 dias e `exponencial_30`
  rendia 29,57 em vez de 30,00. Nova convenção padrão `linear_mes` (taxa ÷ dias do mês), a
  única que reproduz a taxa contratual sobre o SMD; as outras duas ficam para régua de laudo
  adverso, com a diferença declarada. Fixtures de maio recalibradas (30,90 → 29,90 em
  linear_mes; a variante linear_30 mantém 30,90).
- `encontro_de_contas` excluía incrementos negativos das bases (simples + dobro não fechava
  com o excesso final) e datava a competência do corte no fim do mês (juros de 05/03/2021 caíam
  no dobro). Agora as bases fecham e a competência que contém 30/03/2021 vai inteira na base
  simples (menor excesso, declarado na `nota`).
- Taxa em pontos percentuais (7,9) era aceita como fração: `guard_taxa` recusa.
- Reconciliação com lançamentos intradia reordenados gerava divergências falsas — conferência
  pelo fechamento do dia.

**motor-cet.py** (97 asserções, eram 57)
- Três descartes silenciosos de pagamento: na data-base (loop semiaberto), no mesmo dia
  (dicionário sobrescrevia) e em dia não útil (fora da série). Agora: agregação por data,
  pagamento na data-base abatido no fim sem encargo do dia, dia não útil deslocado ao próximo
  dia útil com `pagamentos_deslocados` na saída, fora do período ou acima do saldo → erro.
- `cobertura()` exigia série até a data-base, mas a reconstrução só usa pontos anteriores —
  todo caso "até hoje" falhava (o SGS publica em D+1). Ponta necessária = último dia útil
  antes da data-base; `verificar_ponta_da_serie` devolve `ponta_necessaria`.
- CET-01 comparava custo ex-post (indexador realizado) com CET ex-ante (Res. CMN 4.881/2020:
  indexador da contratação) — todo pós-fixado assinado antes da alta da Selic saía "Ilícito
  T1" por construção. Agora `auditar_cet` recebe `indexador_aa_na_contratacao` e `spread_aa`,
  compara o declarado com o CET esperado ex-ante (tolerância 5%); sem esses dados o achado é
  `A verificar`, nunca `Ilícito`.
- Memória: termo cruzado do spread omitido (R$ 18,53 sem rubrica em R$ 1M/ano) —
  `enc_spr = saldo × (1+i) × (f−1)`; toda linha fecha saldo_anterior + encargos − amortização.
- `f"R$ {x:,.2f}"` en-US vazava para o laudo ("R$ 3,166,077.58") — `brl_rs` de `comum`.
- `conferir_fator` com tolerância relativa e `casas_conector` (fator do conector com menos
  casas não gera falso "não confere"); `conferir_saldo(apurado=0)` e custo zero viram lacuna.

**motor-calculo.py** (v1.2.0; 64 asserções, eram 29)
- `tabela_price(antecipado=True)` usava PMT antecipado em mecânica postecipada: balão de +27%
  na última parcela (leasing saía errado). Primeira parcela em t0, sem juros.
- `normalizar_taxa` rejeitava 150% a.a. (cheque especial) e 400% a.a. (rotativo) — limite por
  unidade (100 para a.m., 2.000 para a.a.).
- `decotar_encargo_financiado` dizia "recompõe o valor presente" e devolvia a soma nominal das
  diferenças de parcela (cujo VP é o próprio encargo). Devolve `valor_presente` e
  `impacto_nominal` com nota para não corrigir monetariamente o nominal; `tabelado` → erro.
- `comparar` sem `.lower()` em `sistema`; cenário revisado mais caro saía sem sinal —
  `favoravel` e `nota`. `prazo_em_periodos` com regra de fim de mês (31/01 → 29/02 = 1).

**motor-cartao.py** (v1.1.0; 53 asserções, eram 30)
- Teto da Lei 14.690 somava competências anteriores a 03/01/2024 — só as posteriores entram;
  as demais saem em `competencias_excluidas_pre_marco`.
- `valor_original` único para toda a série subestimava o admissível (compras novas roladas
  constituem dívida própria com teto próprio — Res. CMN 5.112/2023, art. 2º, §1º): novo
  parâmetro `novas_dividas`; sem ele, `ressalva` obrigatória.
- Fatura cujo total não fecha (encargos com OCR ×10) passava — consistência aritmética com
  tolerância R$ 0,05; competência duplicada e série vazia agora são erro.
- `excesso_por_taxa` declara `metodo` (nominal, sem efeito composto — menor excesso).

**gerar-relatorios.py** (60 asserções, eram 22)
- `Revisão inviável` prometido em verde e ausente de `CORES` (saía sem cor); XLSX pintava
  `A verificar`/`Lacuna` de vermelho — paleta única espelhando o schema.
- `premissas` documentado e nunca renderizado — seção "Premissas declaradas" no PREMIUM e
  na aba de metodologia.
- `validar()` aprovava payload que depois dava KeyError (marca.nome, identificacao.campos,
  diferenca em DIVERGENTE, panorama.*) — nova `validar_detalhado()` estrutural com erros e
  avisos (kpis ≠ 4, achado pró-banco sem ressalva, resultado fora da lista, taxa_aa em fração).
- Payload demo e schema carregavam o nome do escritório, a OAB e a cidade do operador original — placeholders
  neutros; o autoteste falha se voltarem.
- `conferencia.natureza_cenarios` (`conferencia` | `recomposicao`) para o texto fixo da tabela
  de cenários, que era só da rota CET; diferença negativa com frase certa; nome de aba
  sanitizado; barra negativa no panorama; `openpyxl` conferido antes de escrever qualquer
  arquivo.

### Acrescentado

- `reference/comum.py` — `brl`/`brl_rs`/`pct`/`pt` únicos (Decimal HALF_UP), parse pt-BR
  estrito, competências, `guard_taxa`, constantes `CORTE_TEMA_929` e `MARCO_TETO_CARTAO`.
  Os quatro `brl()` divergentes (o laudo arredondava diferente conforme a fonte) foram
  substituídos.
- `reference/carregar_motores.py` — importa os motores (nomes com hífen) com registro em
  `sys.modules`, o que os `@dataclass` exigem.
- `reference/verificar-consistencia.py` — autoteste documental: versão única (SKILL.md, JSON,
  CHANGELOG, ARCHITECTURE), contagens em prosa contra o JSON, tiers, `regras_afetadas`
  derivado do `corte_temporal`, `CORES` = lista do schema, identidade pré-preenchida,
  `description` ≤ 1.000 caracteres, regras de conduta sem repetição e referências cruzadas
  válidas, arquivos referenciados existentes, 4390 nunca como diária, pendências vencidas.
- `regras-bancarias.json` v5.1: R15 com `tipo_contrato: [todos]` e bloco `regime`
  (consumerista T1 / civil-empresarial T2 com consequência própria) — restrita a consumo_pf,
  nunca disparava para PJ na L2, contradizendo a regra crítica e a C2; R16 com
  `requer_consulta_bacen`; `marcos_temporais[*].regras_afetadas` regenerado do
  `corte_temporal` (MT01 apontava seguro em vez de capitalização; MT05 apontava R25/IOF em
  vez de R26/R27); bloco `pendencias_jurisprudenciais` com `verificado_em` (26/08/2026) e
  `validade_dias` 90 — o motor passa a saber que está velho; nota 5.0 retroativa (R30–R33
  entraram sem nota).

### Alterado — documentação

- SKILL.md reescrito como **orquestrador** (505 → ~230 linhas, ~12 mil → ~5 mil tokens por
  acionamento): não repete mais L0–L4, que já viviam nas sub-skills e haviam divergido
  (gate pós-L4 apontava skills diferentes em três arquivos). Regras de conduta renumeradas
  0–26 sem repetição (havia 19, 20 e 21 duplicadas e a regra "0" depois da 11); referências
  cruzadas nas sub-skills atualizadas.
- Versão única em todo o pacote (SKILL.md dizia 4.6, CHANGELOG 5.0, JSON 5.0 com notas até
  1.5.1, ARCHITECTURE 4.6/1.5.1). Contagens "29 regras" → 33 em todos os arquivos; tiers em
  ARCHITECTURE 15/7 → 16/11/6; asserções de autoteste atualizadas.
- L0: "4390 para Selic" como série diária corrigido para 11 (4390 é a Selic mensal).
- L2: regras `sem_precedente_consolidado` não concluem; verificação de validade das
  pendências; reaproveita a consulta BACEN da L0 em vez de reconsultar (também na L3).
- L3: pagamentos e CET ex-ante documentados; decote com dois números; ponta até o dia útil
  anterior (também em bacen-consulta.md e INSTRUCOES-CONECTOR.md).
- L-1: pergunta tipo/nome/registro (OAB ou CRC)/entidade/cidade/skill de peticionamento;
  persistência em `config/operador.json`.
- Ferramentas de interface neutras com fallback (widget quando houver; senão tabela markdown),
  diretório de saída por sessão, skill de peticionamento configurável em vez de nome fixo.
- R0: ramo cartão declara que `analise-faturas-cartao.md` substitui L1–L3; rota CONTA marcada
  **beta** enquanto o repertório estiver em ESQUELETO (o R0 avisa ao confirmar a rota).
- `description` reduzida de 1.006 para menos de 1.000 caracteres (limite de upload 1.024).

### Pendente (lote 3)

Ramo `conta` no renderizador; repertório CONTA via JusIA; cartão como terceira rota (F0–F3);
motor de regras determinístico; regressão com caso real; conferir status dos temas 1378, 929,
1328 e 1414 e atualizar `verificado_em`.

## v5.0 — 26/08/2026

Sessão de auditoria de uma execução bancária real com duas cédulas (caso de cliente — identificação omitida). Os
defeitos abaixo foram encontrados em uso real, não em revisão de gabinete.

### Corrigido — defeitos que produziam erro material

**Prompt de pesquisa saía dentro do laudo.** `render_premium` imprimia `agenda_jusia` como
seção do documento pericial. Documento destinado aos autos não pode carregar roteiro de
pesquisa não executada: entrega a estratégia à parte contrária e admite por escrito que as
teses estão sem lastro. A agenda passa a sair em `INTERNO-agenda-pesquisa-<slug>.md`, com
advertência de não juntar aos autos; o laudo apenas nomeia os achados pendentes de verificação.

**A skill mandava consolidar múltiplos contratos num relatório único.** O chassi é
mono-instrumento — `conferencia` tem um veredito, `memoria` é singular. Numa execução em que o
saldo de uma operação confere e o da outra diverge, o laudo consolidado atestava conformidade
de planilha não conferida naqueles termos. Novo gate R0-b: N instrumentos, N payloads, N
laudos, cada um com veredito próprio, achados renumerados e bloco de advertência de conexão.

**R03 acendia vermelho e apontava para o vazio.** Detectava comissão de permanência disfarçada
em qualquer data, mas mandava aplicar R01 e R02, cujo corte temporal para em 01/09/2017. Ganhou
`regime_por_marco`, com consequência própria pós-MT04 ancorada no art. 884 do CC e na
capitalização da mora, e alerta expresso para não citar as Súmulas 294, 296 e 472 em contrato
posterior ao marco.

**`dias_uteis()` tinha convenção implícita.** Semiaberta à direita, correta para reconstruir
saldo e errada para auditar fator declarado em intervalo fechado — produzia dois números para a
mesma grandeza. Acrescentados `dias_uteis_fechado()` e `auditar_fator_declarado()`, que apura
nas duas convenções, adota a de menor excesso e declara a descartada.

**Validação exigia `panorama` mesmo quando o gate pedia só o laudo.** `gerar()` e `validar()`
passam a receber `formatos`; CLI ganhou `--formatos`.

### Acrescentado

- **R30** capitalização de juros moratórios; **R31** multa sobre base que inclui juros;
  **R32** honorários extrajudiciais cumulados com judiciais; **R33** encargo com base
  indeterminável. As quatro com status `sem_precedente_consolidado`, que obriga pesquisa antes
  da peça em vez de sumir do quadro.
- **L3 — auditoria da memória do credor**, com seis conferências, a executar antes dos cenários
  contrafactuais. Em execução ajuizada é onde está o resultado útil.
- **L3 — veredito `revisão contratual inviável`** quando a razão fica abaixo de 1,5x, a
  capitalização está pactuada e a prestação reproduz a taxa.
- **L0 — taxa composta** por indexador mais spread, apurada como soma composta e não pelo
  spread isolado.
- **L0 — gate PJ endurecido**: vulnerabilidade afirmada sem elementos concretos mantém os
  achados dependentes do CDC como `A verificar`.
- **Critério de menor excesso** como regra geral, com a leitura descartada declarada na
  metodologia.
- Formatação numérica pt-BR no schema do payload.

### Testes

`motor-calculo.py` 29, `motor-cet.py` 57 (eram 49), `gerar-relatorios.py` 22 (eram 17). As
asserções novas travam as regressões desta sessão: laudo sem prompt, agenda apartada com
advertência, validação condicional ao gate e divergência entre as duas convenções de janela.

## v4.6 — 22/08/2026 — Rota CONTA implementada; correções da auditoria

A rota que a v4.5 descrevia passa a existir. Entram `skills/R0-gate-roteamento.md`,
`skills/C0-C6-rota-conta.md`, `reference/motor-conta-corrente.py` (autoteste com 34
asserções: saldo diário, reconciliação contra o saldo impresso do extrato como guarda
da extração, SMD hamburguês em duas bases, trinca de cenários com condição de
aplicabilidade, imputação do art. 354, expurgo com pareamento de estorno, nexo cruzado
e encontro de contas com o corte do Tema 929) e
`reference/repertorio-jurisprudencial-contas.md` (ESQUELETO: 7 teses com prompts JusIA
prontos — nada citável até a validação com inteiro teor).

Decisões de projeto: motor puro — a extração de PDF é da camada C1, com gate de
aprovação, e a reconciliação valida a extração (divergência ou competência faltante é
lacuna bloqueante); trinca = taxa média BACEN / capitalização mensal / taxa contratada
limpa de cumulações; convenções declaradas (hamburguês, linear_30/exponencial_30,
capitalizacao mensal|nenhuma).

Correções da auditoria de 22/08: ARCHITECTURE.md regenerado do estado real (estava duas
gerações atrás — descrevia assets/ e seis templates aposentados na v4.0); sumário da L4
na SKILL.md alinhado à regra 14 ("6 formatos" → payload → PREMIUM/PANORAMA/planilha);
contagem de regras na L2 (28 → 29); caminho dos termos de CP disfarçada explicitado
(dentro da R03); nota das 12 categorias na L1 (10 de cláusula + 2 de regra); "5
camadas" → "L0 a L4" nos modos; regra 21 com o fallback do entregável CONTA declarado.

Pendências: ramo CONTA no payload do gerar-relatorios.py; preenchimento do repertório
via JusIA; regressão com extrato real.

## v4.5 — 18/08/2026 — Conector com leitura em lote; skill aproveitando

O conector ganhou duas capacidades que a skill pedia, e a skill passou a usá-las. Nenhuma muda
regra de negócio; as duas cortam quota do aluno.

**Leitura multi-série** — `consultar_taxa_bacen` aceita `codigos: [...]` (até 6): a série da
modalidade e o indexador diário vêm numa chamada, cada um com estatísticas, `fator_acumulado`,
`procedencia` e `ponta`. Uma série que falhe na fonte entra como `erro` no lote sem derrubar as
outras. `pontos: "completos"` é recusado com `codigos` (a série diária inteira de várias
estouraria a resposta) — para ela, `codigo` sozinho. O orçamento do caso típico caiu de **4 para
2 chamadas** de dado (mais o `atualizar_debito`).

**Restituição parcela a parcela** — `atualizar_debito` aceita `valores: [{ valor, data_inicial,
rotulo }]`: cada pagamento indevido é corrigido da sua data-base, sob o mesmo regime de
`segmentos`, e a série é buscada **uma vez só**. 48 parcelas custavam 48 chamadas (ou 1 com
data-base única, pericialmente errada) — agora **1**. Devolve `resumo_geral` e a memória de cada
valor. A L3 passa a montar a repetição de indébito do Tema 929 por esse caminho.

**Procedência mais honesta** — `fonte_indisponivel` separa timeout do SGS de ausência de
publicação (`sem_dado`): a skill não declara mais lacuna por causa de uma falha de rede.
`capturado_em_min` revela a captura mais antiga do cache na janela, que o `atualizado_em` por
série (um `max`) mascarava.

**Alterado na skill**
- SKILL.md (orçamento e tabela de tools), `reference/bacen-consulta.md` (seções 2 e 4, orçamento,
  sinais de procedência), `skills/L3-analise-quantitativa.md` (indébito via `valores`) e
  `INSTRUCOES-CONECTOR.md` (itens 4 e 10) alinhados às duas capacidades.

**Do lado do conector** (mesma leva): `codigos` em
`consultar_taxa_bacen`, `valores` em `atualizar_debito`, `fonte_indisponivel`/`capturado_em_min`
em `procedencia`, e o handshake anunciando as duas capacidades de lote. Suíte: 179 testes.

## v4.4.1 — 18/08/2026 — Fechamento da auditoria adversarial

Correções que saíram da auditoria cruzada skill × conector, depois que a v4.4 já estava escrita.
Nenhuma muda regra de negócio.

**Corrigido — o contrato do conector mudou de novo, e a skill descrevia o anterior**
- `consultar_indice` e `atualizar_debito` deixaram de emitir `structuredContent` no conector: a
  resposta inteira vem como JSON no texto, para não transmitir série e memória de cálculo em
  dobro. A skill ainda mandava procurar payload estruturado nessas duas
  (`reference/bacen-consulta.md`, `SKILL.md`). Alinhado nas três superfícies.
- `carregar_de_consultar_taxa_bacen` agora aceita o **envelope MCP cru**
  (`{content:[{type:'text',text:…}], structuredContent:{…}}`), que é o que um agente passa
  naturalmente. Antes só aceitava o payload já desempacotado e levantava "resposta sem pontos".

**Corrigido — guarda que prometia mais do que entregava**
- `cobertura()` compara só as pontas da série: uma série com buraco no MIOLO passava como
  "cobertura integral". A docstring agora diz isso com todas as letras e aponta para
  `conferir_fator()`, que é quem detecta lacuna interna. Ganhou o parâmetro opcional
  `pontos_esperados` (o `pontos_total` do conector) que fecha a brecha quando disponível.

**Quota**
- A L0 passa a consultar a **janela completa** do contrato de uma vez e extrair dela o ponto da
  data de assinatura, em vez de consultar a data e depois a L3 consultar o período. A L2 já
  reaproveitava desde a v4.4; agora as três camadas dividem uma consulta só.

**Higiene**
- As instruções de metadata já superadas saíram do `regras-bancarias.json` (v1.5.1) e vieram para
  cá. Aquele arquivo é o único que a skill carrega como dado estruturado, e um prefixo
  `[SUPERADO]` protege um leitor humano, não um agente que faz grep.
- Limitação declarada: TR e poupança publicam período de referência (`dataFim`), e os adaptadores
  carregam só `data`/`valor`. Em reconstrução indexada a essas séries, a convenção de ancoragem
  vai declarada na metodologia.
- Autoteste do `motor-cet.py`: 44 → 49 asserções.

**Instruções de metadata aposentadas** (histórico — eram verdadeiras contra o conector de julho,
são falsas contra o atual):
- [1.3.0] Disciplina de metadata do conector (testes ao vivo). Não confiar nos campos nome/unidade do payload do conector (consultar_taxa_bacen devolve null; listar_series_bacen usa catálogo hardcoded desatualizado). Validar identidade pelo cabeçalho serie.nome de consultar_indice. Superado em 1.4.0/1.4.1 pela reconstrução do catálogo com séries mensais corretas.
- [1.3.0] IDENTIDADE: validar a série pelo cabeçalho serie.nome/unidade de consultar_indice. 226 = TR (diária), NÃO CDI — confirmado contra a fonte oficial (portal de dados abertos do BCB/SGS). Aliasing 11≡12 (Selic ≡ CDI) é bug interno do conector.
- [1.3.0] DRIFT: o espelho do catálogo na skill é ilustrativo, não autoritativo. Descobrir séries em runtime via listar_series_bacen e probar antes de usar; regressão em teste-contrato-bacen.md.
- [1.3.0] Mapeamento de séries mantido como intenção validada; em runtime, probar cada série e, se não responder, buscar equivalente por modalidade na resposta viva do conector.
- [1.4.0] Reconstrução do mapeamento modalidade->série SGS contra o Portal de Dados Abertos do BCB. Os códigos anteriores apontavam para modalidades erradas (cartão rotativo->25497 que é imobiliário; cheque especial->20715 que é PJ total; consignado INSS/privado trocados; etc.).
- [1.4.0] Todas as séries do mapeamento passam a ser MENSAIS (% a.m.) da faixa 254xx — razão contratada/média calculada na mesma base, sem conversão anual->mensal.
- [1.4.0] Corrigido no conector em conjunto: séries renomeadas para a verdade e 17 séries mensais corretas adicionadas com histórico.

## v4.4 — 18/08/2026 — Skill e conector como um conjunto

**Motivo.** A skill tratava o conector como algo a detectar, auditar e desconfiar. Isso fazia
sentido contra a versão do conector de julho; contra a atual, virou puro custo. Auditoria do
caso típico (financiamento de veículo PF pós-fixado em CDI, com restituição corrigida) mediu
**16 chamadas ao conector, 12 delas sem trazer dado nenhum** — sondagem de disponibilidade,
probes de identidade, teste de não-aliasing, reconsulta da mesma série em três camadas. Chamada
de ferramenta é a unidade de quota do plano do aluno.

Pior que o custo: o caminho eleito como primário para série diária estava **errado**. A
`consultar_taxa_bacen` recorta o texto em 60 pontos e o adaptador da skill parseava justamente
esse texto. Numa série de CDI de 48 meses (~1.000 pontos), a reconstrução carregava 60 e seguia —
e as duas guardas da skill, `cobertura()` e `verificar_ponta_da_serie()`, **passavam**, porque o
recorte preserva o primeiro e o último ponto.

Esta versão foi desenvolvida junto com uma leva de correções no conector; as duas metades se
pressupõem.

**Premissa nova, declarada**
- O conector Radar Apogeu está na sessão, **ativo e validado**. A skill é distribuída junto com
  ele, sob a mesma assinatura. Não há detecção, não há teste de disponibilidade, não há caminho
  paralelo.
- Fim da contradição interna: `bacen-consulta.md` dizia "a skill funciona com ou sem o conector"
  e "nunca abortar por ausência do conector" a três parágrafos de "conector ausente: parar e
  avisar". A SKILL.md dizia a terceira coisa. Agora é uma coisa só.

**Correção — série truncada em silêncio**
- `carregar_de_consultar_taxa_bacen` passa a **recusar** resposta recortada em vez de carregá-la
  pela metade: detecta o marcador de omissão e confere `pontos_total` contra o que parseou.
  Aceita também o payload estruturado, não só texto.
- A L3 manda chamar a tool com `pontos: "completos"` para série diária.
- `conferir_fator` é reenquadrado como a guarda que **de fato** pega o problema, e sua assinatura
  muda para `conferir_fator(serie, fator_conector, inicio=None, fim=None)`: a janela é **fechada**
  nas duas pontas, como a do conector. Antes ela comparava o produtório local semiaberto
  `[inicio, fim)` contra o fator fechado do conector — divergência de um dia em todo contrato
  cuja data-base caísse em dia útil publicado. A assinatura antiga falha alto, com mensagem.
- Novo helper `janela_fechada()`. `dias_uteis()` segue semiaberto: é a convenção do CDI para a
  reconstrução financeira, e a distinção agora está escrita.

**Removido — o que virou alarme falso ou custo**
- Teste de disponibilidade `listar_series_bacen({ filtro: "CDI" })`. Devolvia 2 de 31 séries,
  nenhuma útil ao caso.
- Probe de identidade por `consultar_indice(codigo).serie.nome`. O caminho nem existia — o nome
  está em `cabecalho.serie.nome` — e, para as séries 254xx, devolvia identidade *pior* que a tool
  que deveria auditar.
- Teste de não-aliasing 11×12. Selic e CDI publicam fator diário muito próximo: é o mercado, não
  defeito do conector.
- Os dois espelhos do código do conector que a skill carregava (catálogo e tools). Espelhos que
  derivavam e não eram autoritativos em runtime; o segundo descrevia uma "v2.0.0" que nunca
  esteve em produção. A descoberta agora é `listar_series_bacen`.
- Avisos de metadata obsoletos: "consultar_taxa_bacen devolve nome/unidade como null",
  "listar_series_bacen serve catálogo hardcoded desatualizado", "226 vem rotulada CDI",
  "consultar_indice vai ao vivo, sem cache". Todos falsos contra o conector atual.

**Alterado**
- `reference/bacen-consulta.md` reescrito como **protocolo**: o que o cache garante, as quatro
  chamadas, o orçamento, as verificações que restam e a tabela de sinais de erro.
- Seção do conector na SKILL.md e regra 12-A reescritas nos mesmos termos.
- `reference/teste-contrato-bacen.md` rebaixado de pré-requisito de laudo para **alarme de
  drift**: roda na atualização do conector, não em toda análise, e numa chamada só.
- L2 e L3 alinhadas, com instrução explícita de **reaproveitar** série já consultada na sessão.
- ARCHITECTURE.md deixa de descrever o conector como opcional e as taxas como "ao vivo".
- `regras-bancarias.json` → v1.5.0: nota que **supera** a disciplina de metadata da 1.3.0/1.4.0.
- Contagens corrigidas: 29 regras (eram 28 no texto), 24 séries mapeadas (eram 16).

**Orçamento de chamadas — o resultado**

| | antes | agora |
|---|---|---|
| Sondagem e probes | 12 | 0 |
| Dado | 4 | 3 |
| Correção do indébito | 1 | 1 |
| **Total do caso típico** | **16** | **4** |

**Do lado do conector** (mesma leva)
- Cache visível ao cliente: `listar_series_bacen` anexa a cobertura de cada série;
  `consultar_taxa_bacen` declara `procedencia`, `ponta` e `fator_acumulado`.
- Recorte de texto passa a se declarar, e `pontos: "completos"` desliga o recorte.
- `atualizar_debito` busca de borda a borda de competência — `data_inicial` no meio do mês não
  zera mais a correção — e expõe `resumo.calculo_interrompido`.
- Timeout do SGS deixa de virar "nenhum dado encontrado".
- Identidade única de série entre as três visões do conector, travada por teste.
- As instruções do servidor ganham o bloco de índices e cache.

- Autoteste do `motor-cet.py`: 25 → 44 asserções, incluindo regressão do recorte de texto, da
  contagem divergente de pontos e da janela fechada do `conferir_fator`.

## v4.3 — 17/08/2026 — Conector como fonte única

**Motivo.** A v4.2 havia documentado um "caminho 0" que lia o cache do BACEN direto na base
de dados do conector. Dois defeitos: (a) essa skill é distribuída a usuários que
têm o conector instalado, e nenhum deles tem acesso àquela base — o caminho não existia para
o destinatário; (b) pior, a documentação embutia o identificador do projeto e os nomes das
tabelas internas dentro de um artefato distribuído a terceiros.

**Removido**
- Seção "Caminho 0" de `bacen-consulta.md` e a linha correspondente na tabela da SKILL.md.
- Toda referência a projeto, tabelas ou infraestrutura interna nos arquivos distribuídos.
  Varredura confirma zero ocorrências fora do CHANGELOG histórico.

**Alterado**
- O adaptador de leitura direta do banco → `carregar_de_linhas()`: adaptador genérico para série já
  tabulada, sem referência a infraestrutura, com aviso explícito de que **não é caminho de
  obtenção de dado** — a fonte continua sendo o conector.
- `verificar_defasagem_cache()` → `verificar_ponta_da_serie()`: reenquadrado como guarda de
  ponta de série devolvida pelo conector, que é o problema real (o SGS publica com atraso e
  feriado encurta o período), e não como diagnóstico de cache alheio.
- **O conector deixa de ser acelerador e passa a ser pré-requisito declarado.** Ausente da
  sessão, a skill para e orienta a ativação, em vez de trocar de fonte em silêncio — mudar a
  fonte sem declarar quebra a reprodutibilidade do laudo em contraditório.
- `web_fetch` rebaixado de "fallback" a **contingência declarada**, admissível só quando o
  conector está presente mas indisponível, e sempre registrado na metodologia do entregável.
- Regra 12-A reescrita nesses termos; L3 alinhada.

**Verificação**
- Reconstrução de 184 dias úteis de CDI conferida contra três fontes independentes —
  produtório local, `fator_acumulado` do conector e cálculo direto sobre o cache — com
  resultado idêntico (fator 1,10659021).

## v4.1 — 17/08/2026 — Uso correto do conector BACEN

**Motivo.** Auditoria ao vivo revelou que a skill tinha o conector Radar Apogeu na sessão e
não o usava: a série diária do CDI foi puxada por `curl` direto na `api.bcb.gov.br`,
ignorando o cache persistente e dispensando a conferência de fator. A `bacen-consulta.md`
documentava o conector apenas para taxa média de mercado — série diária de indexador, que é
o insumo do caminho pós-fixado da v4.0, não estava documentada em lugar nenhum.

**Adicionado**
- `motor-cet.py`: `carregar_de_consultar_taxa_bacen()` (parseia o texto do cache),
  `carregar_de_consultar_indice()` (consome o JSON, aceita dict ou string) e
  `conferir_fator()` (cruza o produtório local contra o `fator_acumulado` do conector).
  7 asserções novas, total de 32.
- `bacen-consulta.md`: seção de série diária de indexador, com ordem de preferência entre as
  tools, conferência obrigatória de fator e registro do erro a não repetir.
- `teste-contrato-bacen.md`: contrato de drift das séries diárias 12, 11 e 226.
- Regra 12-A na SKILL.md: indexador vem do conector, não de `curl`.

**Alterado**
- Resolução de dependência BACEN da SKILL.md reescrita em tabela por necessidade, com o
  teste de disponibilidade explícito (`listar_series_bacen({filtro:"CDI"})`, que lê catálogo
  interno e não bate em API externa).
- L2 e L3 alinhadas: `consultar_taxa_bacen` identificado como o caminho de cache, e L3 ganhou
  o procedimento de operação pós-fixada em quatro passos.
- Formato de datas documentado: tools do conector usam `yyyy-MM-dd`; a API pública do SGS
  usa `DD/MM/AAAA`. Trocar devolve série vazia, que é lacuna bloqueante.

**Verificado ao vivo**
- `consultar_indice(12)` para 18/07/2025 a 09/04/2026: 184 pontos, fator 1,10659021,
  variação 10,65902144% — confere com a reconstrução independente do caso em produção.

## v4.0 — 17/08/2026 — Refatoração da camada de saída

**Motivo.** Em produção, os seis templates falharam simultaneamente num contrato real: sistema
de amortização atípico (percentual do saldo fixado pelo instrumento), operação pós-fixada em CDI
e saldo que **conferia** com a apuração do credor. Os três modelos HTML embutiam a lógica de
cálculo no `<script>` a partir de `P`, `rC`, `rR` e `n`, e todos pressupunham comparação
Price/SAC contratado-versus-revisado com excesso a decotar. Nenhum servia.

**Adicionado**
- `reference/motor-cet.py` — custo efetivo real e auditoria do CET declarado. Reconstrução dia
  útil a dia útil de operação pós-fixada com série do SGS, cobertura da série como lacuna
  bloqueante, confronto com a Res. CMN 4.881/2020, cenários contrafactuais, `conferir_saldo()`
  com veredito CONFORME/DIVERGENTE, auditoria da taxa de mora praticada e detecção de acréscimo
  sem rubrica em projeção diária. 25 asserções.
- `reference/gerar-relatorios.py` — renderizador único dos dois entregáveis e da planilha, a
  partir de payload. Valida o payload antes de renderizar. 17 asserções.
- `reference/payload-schema.md` — contrato de dados entre a L3 e a saída.
- `motor-calculo.py`: sistema `tabelado` (cronograma de percentuais extraído do instrumento,
  cobre SPV e congêneres sem arbitrar sistema) e `amortizacao_negativa()`. 6 asserções novas,
  total de 29.

**Alterado**
- Regra 14 deixa de ser "template com dados trocados" e passa a ser "payload renderizado".
- Seis formatos reduzidos a **PREMIUM** (laudo pericial) e **PANORAMA** (executivo), mais a
  planilha única com dashboard na primeira aba e impressão em A4 retrato.
- L-1 ganha gate de tipo de responsável: advogado com OAB ou contador com CRC. O tipo passa a
  determinar o cabeçalho e o formato do entregável, não apenas a linha de assinatura.
- L4 passa a exigir validação de paginação em PDF antes de `present_files`.
- Payload passa a exigir `conferencia.veredito`, `ressalvas` e `lacunas`.

**Aposentado**
- `assets/templates-html/` e `assets/templates-xlsx/` movidos para `assets/_aposentados/`, com
  `LEIA-ME.md` explicando o motivo. Não usar para entregável novo.

# CHANGELOG — revisao-contratos-bancarios

## 1.4.2 — 15/08/2026

Correção do catálogo levada ao **código-fonte do conector** (permanente).

- O conector recriava o catálogo a partir do código a cada inicialização, então a
  correção só no banco seria revertida. Corrigido na fonte: catálogo reconstruído com os
  códigos mensais corretos (254xx) — isso também conserta o `listar_series_bacen` (que lê
  esse catálogo). `226` reetiquetado TR; exemplo da tool `consultar_taxa_bacen`
  atualizado; teste de contrato do catálogo ajustado.
- Espelho ilustrativo do catálogo na skill sincronizado com a fonte.

---

## 1.4.1 — 15/08/2026

Reconstrução do catálogo de séries de crédito do BACEN — o mapeamento
modalidade→código estava **sistematicamente errado**, apontando para séries de
outra modalidade. Corrigido contra a fonte oficial e no conector em conjunto.

### Corrigido (crítico)

- **Mapeamento modalidade→série SGS reconstruído** contra o Portal de Dados
  Abertos do BCB. Os códigos anteriores apontavam para a modalidade errada — o
  mais grave: **cartão rotativo estava mapeado em 25497, que na verdade é
  financiamento imobiliário** (1,12%/mês); o real é **25477** (15,13%/mês).
  Comparar um cartão (~15%/mês) contra 1,12%/mês inflava a razão ~12× e fazia
  todo cartão parecer "fortemente abusivo", sempre. Outros: cheque especial
  estava em 20715 (PJ total anual); consignado INSS/privado trocados;
  imobiliário↔rural trocados.

- **Todas as séries de modalidade agora são mensais (% a.m.)** da faixa 254xx —
  a razão contratada/média sai na mesma base, sem conversão anual→mensal.

- **`reference/bacen-consulta.md`** e **`regras-bancarias.json` (motor 1.4.0)**
  atualizados com os códigos corretos e verificados.

### Feito em conjunto no conector

- 17 séries mensais corretas adicionadas com histórico completo, direto do SGS: 25463/25464/25471/25474/25477/25478/25496
  (PF) e 25438/25441/25442/25443/25445/25446/25447/25450/25455/25456 (PJ).
- Séries mal rotuladas renomeadas para a verdade (25466/25468 consignados
  destrocados; 25494/25495→rural; 25497/25498→imobiliário; 20714-20720
  agregados anuais).
- `descricao` da série 226 corrigida (dizia "CDI", é TR); unidade das séries de
  crédito anuais 207xx corrigida para % a.a.

---

## 1.4.0 — 15/08/2026

Blindagem do caminho-ouro (razão contratado × média BACEN) contra a metadata do
conector, após testes ao vivo. O tratamento é a mesma tese de sempre — recusar
número que o dado não sustenta — agora aplicada à própria confiabilidade do
conector.

### Corrigido

- **Série 226 reetiquetada de CDI para TR.** `reference/bacen-consulta.md` dizia
  "226 = CDI acumulado no mês"; a fonte oficial (portal de dados abertos do BCB /
  SGS) confirma **226 = TR (Taxa Referencial, diária)**. Usar 226 como CDI mensal
  (~1%) produzia número grosseiramente errado. Removida de qualquer papel de
  CDI/crédito; CDI mensal, quando necessário, vem de série verificada pelo
  cabeçalho.

- **Unidade das séries de crédito blindada.** O conector devolve 207xx/25xxx
  rotuladas `% a.m.` ao vivo, mas são **% a.a.** (o `regras-bancarias.json` já as
  declarava corretamente). Seguir o rótulo encolhia a razão contratado/média em
  **~12×** e fazia todo contrato virar "lícito". Regra nova: **nunca confiar no
  campo `unidade` do conector** para essas séries — sempre converter anual→mensal
  e rodar **assert de sanidade** (*média de crédito > 10 nunca é % a.m.*).

### Adicionado

- **Disciplina de metadata** em `reference/bacen-consulta.md`: unidade, identidade
  (validar pelo cabeçalho `serie.nome`/`unidade` de `consultar_indice`) e drift.

- **`reference/teste-contrato-bacen.md`** — teste de contrato que **falha
  automaticamente** quando existência, nome, unidade ou periodicidade de uma
  série muda no conector (pegaria 25442 ausente, 20716 `% a.m.`, 226 CDI e o
  aliasing 11≡12). Converte vigilância humana em regressão.

- **Delegação opcional da correção do indébito ao `atualizar_debito`** (hash
  pericial no demonstrativo), sob gate de identidade da série + `data_inicial` no
  dia 1º da competência + assert de correção não-nula. Price/SAC e teto do cartão
  seguem nos motores locais.

### Alterado

- **Espelho do catálogo do conector marcado ILUSTRATIVO, não autoritativo.** Passa a
  ser snapshot; a existência/identidade de série vem de descoberta em runtime via
  `listar_series_bacen` + probe, não do arquivo embarcado (que já defasou —
  25442 sumiu do conector ao vivo).

- **Motor de regras em 1.3.0** (`regras-bancarias.json`): nota da disciplina de
  metadata no mapeamento de séries; o mapeamento passa a ser "intenção validada",
  probada em runtime.

### Bug-report ao conector (metadata das séries)

Encaminhado ao time do conector para correção na origem: (1) 226 = TR, não CDI;
(2) unidade `% a.a.` nas séries 207xx/25xxx; (3) reconciliar aliasing 11≡12;
(4) expor `taxa_mensal_equivalente` e mapa modalidade→código. Até a correção na
origem, a conversão defensiva + o teste de contrato blindam a skill.

---

## 1.3.0 — 23/07/2026

Ramo de cartão de crédito e proibição absoluta de presunção.

### Adicionado

- **Regra de conduta 0 — proibição de presunção.** Prevalece sobre todas as
  demais. Só há duas origens admissíveis de dado: extraído do documento ou
  informado pelo usuário. Não existe terceira. Dado ausente é lacuna bloqueante,
  não premissa de trabalho. Vale para financiamento e para cartão.

- **`reference/motor-cartao.py`** — motor próprio de faturas, com 30 autotestes.
  `teto_lei_14690()` aplica o teto de 100% do valor original sobre juros e
  encargos, com IOF apartado, devolvendo excesso por competência, excesso
  acumulado, competência de estouro e margem restante. `evolucao_divida()`
  reconstrói a bola de neve: origem do rotativo, encargos acumulados,
  participação dos encargos no saldo e multiplicador. `excesso_por_taxa()`
  quantifica pela taxa quando a discussão não for o teto. `segmentar_serie()`
  divide a série em trechos contínuos e lista as competências faltantes.
  `detectar_candidatos()` sinaliza possíveis parcelamentos e renegociações sem
  classificá-los. `svg_excesso()` emite o gráfico de barras por competência com
  linha de acumulado, no padrão do chassi canônico.

- **`reference/analise-faturas-cartao.md`** — regras de negócio do ramo: a
  fatura como fonte probatória e única fonte da taxa, gate de abertura
  obrigatório, sequência de trabalho e a ordem de valor do que o relatório
  precisa mostrar.

- **Regra de conduta 15 — cartão é ramo próprio.** Sem Price, sem SAC, sem
  estimar taxa pela média BACEN quando ela deveria constar da fatura.

### Alterado

- **R23 ganhou implementação quantitativa.** Era regra qualitativa sem número:
  mandava limitar a 100% sem função que calculasse o teto, o excesso e a
  competência de estouro. Agora aponta para `teto_lei_14690()` e registra que o
  valor original da dívida é fixado em gate com o usuário, nunca inferido.

- **Seção 03 do chassi canônico reestruturada.** Deixou de ser "Premissas e
  limitações" e passou a ser "Origem dos dados e lacunas", com duas listas —
  informado pelo usuário e extraído do documento, cada linha com a origem — mais
  a lista de lacunas pendentes. A categoria "premissa do analista" foi
  eliminada, porque violava a regra 0.

- Motor de regras em 1.2.0.

### Comportamentos fixados nesta versão

- Série de faturas descontínua é analisada por trechos, com pedido nominal das
  competências faltantes. Interpolação é vedada.
- Parcelamento e renegociação são sinalizados como candidatos com hipóteses
  possíveis, e só rotulados após confirmação do usuário.
- O teto de 100% não retroage: operações anteriores a 03/01/2024 recebem
  `aplicavel: False` com o motivo. O marco é a data da operação de rotativo ou
  parcelamento, não a data de assinatura do contrato de cartão.
- IOF nunca entra no cômputo do teto.

### Pendente para a v1.4.0

- Conversão dos modelos 1, 2 e 3 para o chassi canônico.
- Variante de relatório específica para cartão, consumindo `svg_excesso()`.
- Gate de regime jurídico com efeito no motor: em relação empresarial, as regras
  de repetição em dobro fundadas no CDC devem ser desabilitadas por
  classificação, não por lembrete textual.
- Correção monetária e juros sobre os valores de restituição.

---

## 1.2.0 — 23/07/2026

Versão preparada para distribuição na Claude Academy. Remove toda identidade
pré-preenchida, substitui o motor de cálculo e fixa o padrão visual dos relatórios.

### Adicionado

- **`reference/motor-calculo.py`** — núcleo determinístico de cálculo, executável.
  Price e SAC completos, normalização de taxa por unidade declarada
  (`am_efetiva` / `aa_efetiva` / `aa_nominal`), guarda para taxa zero e domínio,
  parcela de ajuste fechando o saldo em zero exato, convenção de prazo
  parametrizada (`meses_civis` / `dias_30_360` / `dias_corridos`), carência,
  parcela antecipada e `decotar_encargo_financiado()`.
  Suíte embutida com 23 casos: `python3 reference/motor-calculo.py`.

- **Camada L-1 — Identificação do operador.** Na primeira execução em cada
  ambiente, a skill pergunta nome, OAB e cidade e persiste em `operador.*`.
  Nas execuções seguintes apenas confirma em uma linha. Sem dados informados,
  a assinatura sai em branco com a pendência sinalizada — nunca substituída
  por nome de terceiro.

- **Regra R29 — comissão flat.** Ilícita quando ausente demonstração de
  contraprestação de serviço autônomo, distinto da própria intermediação
  financeira já remunerada pelos juros. Ônus de demonstração da instituição.
  Tier T1. Consequência com recomposição de valor presente quando financiada.

- **`assets/templates-html/modelo-0-canonico.html`** — chassi canônico do padrão
  visual financeiro: hierarquia numerada, réguas no lugar de cartões, numeral
  tabular, acento cromático único reservado a variação negativa, bloco de
  premissas antes de qualquer valor e nota metodológica com fórmulas abertas.

- `CHANGELOG.md` e seção de arquitetura da v1.2.0 em `ARCHITECTURE.md`.

### Corrigido

- **Identidade literalizada nos templates.** Nome e OAB do autor original
  estavam gravados nos três modelos HTML. Todos passaram a consumir
  `{{OPERADOR_NOME}}`, `{{OPERADOR_OAB}}` e `{{OPERADOR_CIDADE}}`.
  Defeito bloqueante para distribuição.

- **SAC ausente do motor.** A L3 declarava suporte a Price e SAC e fornecia
  apenas a fórmula do Price. Metade do escopo estava sem implementação.

- **Gráfico errado em contratos SAC.** Mantidos principal e prazo, a amortização
  é `PV/n` em qualquer taxa e o saldo devedor coincide nos dois cenários — duas
  curvas sobrepostas. `comparar()` agora devolve o campo `plotar`, que resolve a
  ramificação: `saldo` em Price, `prestacao` em SAC.

- **Decote de encargo financiado subestimado.** A regra anterior devolvia o valor
  nominal, ignorando que o encargo incorporado ao principal rende juros por todo
  o prazo. Em caso real de comissão flat, R$ 52.977,12 nominais correspondiam a
  R$ 112.333,03 de impacto efetivo.

- **Taxa sem unidade declarada.** A mesma cláusula anual admitia leitura nominal
  ou efetiva, com divergência de R$ 325.937,86 no total pago de um contrato de
  61 parcelas. A unidade agora é parâmetro obrigatório, lida da cláusula e
  registrada nas premissas do relatório.

- **Divisão por zero com taxa nula** e ausência de validação de domínio na
  entrada de taxa e prazo.

- **Arredondamento sem parcela de ajuste**, que deixava resíduo no saldo final.

- **Códigos de série BACEN inválidos.** `21371` e `21372` não respondem no SGS e
  penduravam a conexão até o timeout. Substituídos por `20722` (capital de giro
  até 365 dias) e `20723` (acima de 365 dias), com `25442` acrescentada para a
  base mensal e `20724` para o rotativo. A série agregada `20717` foi mantida,
  porém marcada como imprópria para aferição de abusividade. Todas as entradas
  passaram a declarar `unidade`.

- **Fallback de consulta BACEN inoperante.** A instrução mandava montar a URL da
  API por edição de caminho, o que o ambiente rejeita. O fallback correto é
  `web_search`, depois `web_fetch` no link retornado, e só então perguntar a
  taxa ao usuário.

- **Espelho das tools do conector, v2.0.0** — probe de existência da série antes da
  consulta pesada, retry com timeout escalonado e backoff, cache com TTL
  diferenciado, truncamento do `structuredContent`, tolerância a vírgula
  decimal, validação real de data e intervalo, e erros com código legível por
  máquina.

### Pendente para a v1.3.0

- Conversão dos modelos 1, 2 e 3 para o chassi canônico. Estão funcionais e
  tokenizados, mas ainda no padrão visual anterior.
- Gate de regime jurídico com efeito no motor: em relação empresarial, as regras
  de repetição em dobro fundadas no CDC devem ser desabilitadas por
  classificação, não por lembrete textual.
- Correção monetária e juros sobre os valores de restituição, hoje apurados em
  termos nominais.

---

## 1.0.0

Versão inicial. Cinco camadas com gates, motor de 28 regras em 12 categorias,
consulta BACEN ao vivo, três modelos HTML e três modelos XLSX.
