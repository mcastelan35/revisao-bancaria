# Repertório jurisprudencial validado

Base das petições iniciais: para cada regra do motor (R01…) ou tese própria (PJ-VULN…), os
julgados que a peça pode citar. Cada entrada traz a ementa na íntegra, copiada do inteiro teor
lido no conector Jusbrasil (no TJPR, também do portal do tribunal), a identificação completa e a
url canônica de acesso.

**Não leia este arquivo inteiro.** Peça só os julgados das regras do caso:

- `<rb> jurisprudencia consultar --regras R04,R13` devolve os julgados citáveis de cada regra;
- `<rb> jurisprudencia cobertura` mostra quantos julgados cada regra tem e quais regras T1 ainda
  estão sem precedente superior;
- `<rb> jurisprudencia validar` confere o formato (roda também no autoteste e no CI);
- `<rb> espelho payload.json --saida DIR` monta o espelho da petição inicial a partir do laudo e
  deste repertório.

## Critérios de entrada

1. **Fonte:** o conector Jusbrasil (busca e inteiro teor) ou, para acórdão do TJPR, o portal de
   jurisprudência do próprio tribunal, com o link permanente do acórdão (o inteiro teor das
   Câmaras Cíveis no Jusbrasil vem sem ementa). Julgado que não foi aberto no inteiro teor não
   entra. A ementa é copiada palavra por palavra, sem resumo nem grifo; só se corrigem erro de
   digitação e defeito de extração (palavras emendadas, acento faltando, espaço antes de vírgula).
2. **STJ e STF:** entram os favoráveis à tese (`FAV`) e, quando o tribunal fixa o limite da tese,
   um adverso (`ADV`), que vira ressalva ou argumento contrário previsto na peça.
3. **Tribunais locais (TJ, TRF):** só favoráveis. O TJPR vem primeiro; outro tribunal entra quando
   o TJPR não tem julgado favorável alinhado à tese.
4. **Alinhamento:** o ponto decidido é a própria tese (voto e dispositivo, não só a ementa).
5. **Validade:** cada entrada vale por um ano desde `verificado_em`. Vencida ou marcada
   `CONFERIR`, sai da consulta com aviso até ser revalidada.
6. **Sigilo:** só a ementa e a identificação do julgado. Nenhum nome de parte ou advogado e nenhum
   dado de cliente do escritório.

## Formato de uma entrada

```
## R04 — TAC vedada em contratos pós-30/04/2008

Tese: <a tese como o autor a sustenta na inicial>

### STJ · REsp 0.000.000/UF
- regras: R04, R06
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 0.000.000/UF
- orgao: Segunda Seção
- relator: Min. Nome
- julgamento: AAAA-MM-DD
- publicacao: AAAA-MM-DD
- precedente_qualificado: Tema 000/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/0000000000  (TJPR: https://portal.tjpr.jus.br/jurisprudencia/j/…)
- verificado_em: AAAA-MM-DD
- status: VERIFICADO
- uso_na_peca: <o que o julgado prova na petição>
- observacao: <limite, distinção ou modulação; "—" se nada>

ementa:
> <ementa na íntegra, uma ou mais linhas>
```

Um julgado que sirva a mais de uma regra aparece uma vez, sob a primeira, com todas em `regras`.

## R01 — Comissão de permanência — cumulação vedada

Tese: A comissão de permanência, quando validamente pactuada, só pode incidir de forma isolada no período de inadimplência: sua cobrança exclui a exigibilidade dos juros remuneratórios, dos juros moratórios, da multa contratual e da correção monetária, e o excesso cobrado em cumulação é decotado e restituído.

### STJ · REsp 1.058.114/RS
- regras: R01, R02
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.058.114/RS
- orgao: Segunda Seção
- relator: Min. Nancy Andrighi (p/ acórdão Min. João Otávio de Noronha)
- julgamento: 2009-08-12
- publicacao: 2010-11-16
- precedente_qualificado: Tema 52/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106304712
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case repetitivo: a comissão de permanência é válida só se limitada à soma dos encargos remuneratórios e moratórios do contrato, e os excessos pactuados na cláusula são decotados (base da Súmula 472/STJ, que exclui a cumulação com juros remuneratórios, moratórios e multa).
- observacao: Para os efeitos do art. 543-C do CPC/1973 a cláusula de comissão de permanência foi considerada válida (vencida a relatora); a ementa fixa o teto (soma dos encargos) e o decote, e a vedação de cumulação vem da Súmula 472/STJ (2012), que deve ser citada em conjunto. O REsp 1.063.343/RS (Segunda Seção, mesma sessão, mesma tese do Tema 52) tem ementa praticamente idêntica e não foi listado em separado. Corte temporal: contratos anteriores a 01/09/2017 (Res. CMN 4.558/2017).

ementa:
> DIREITO COMERCIAL E BANCÁRIO. CONTRATOS BANCÁRIOS SUJEITOS AO CÓDIGO DE DEFESA DO CONSUMIDOR. PRINCÍPIO DA BOA-FÉ OBJETIVA. COMISSÃO DE PERMANÊNCIA. VALIDADE DA CLÁUSULA. VERBAS INTEGRANTES. DECOTE DOS EXCESSOS. PRINCÍPIO DA CONSERVAÇÃO DOS NEGÓCIOS JURÍDICOS. ARTIGOS 139 E 140 DO CÓDIGO CIVIL ALEMÃO. ARTIGO 170 DO CÓDIGO CIVIL BRASILEIRO.
> 1. O princípio da boa-fé objetiva se aplica a todos os partícipes da relação obrigacional, inclusive daquela originada de relação de consumo. No que diz respeito ao devedor, a expectativa é a de que cumpra, no vencimento, a sua prestação.
> 2. Nos contratos bancários sujeitos ao Código de Defesa do Consumidor, é válida a cláusula que institui comissão de permanência para viger após o vencimento da dívida.
> 3. A importância cobrada a título de comissão de permanência não poderá ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato, ou seja: a) juros remuneratórios à taxa média de mercado, não podendo ultrapassar o percentual contratado para o período de normalidade da operação; b) juros moratórios até o limite de 12% ao ano; e c) multa contratual limitada a 2% do valor da prestação, nos termos do art. 52, § 1º, do CDC.
> 4. Constatada abusividade dos encargos pactuados na cláusula de comissão de permanência, deverá o juiz decotá-los, preservando, tanto quanto possível, a vontade das partes manifestada na celebração do contrato, em homenagem ao princípio da conservação dos negócios jurídicos consagrado nos arts. 139 e 140 do Código Civil alemão e reproduzido no art. 170 do Código Civil brasileiro.
> 5. A decretação de nulidade de cláusula contratual é medida excepcional, somente adotada se impossível o seu aproveitamento.
> 6. Recurso especial conhecido e parcialmente provido.

### STJ · AgInt no AREsp 1.800.828/RS
- regras: R01, R02
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 1.800.828/RS
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2023-09-18
- publicacao: 2023-09-20
- precedente_qualificado: Súmula 472/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2108095091
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão de Turma (2023) que, enfrentando o mérito, reafirma que a comissão de permanência não pode ser cumulada com outros encargos, inclusive os moratórios, e que a repetição do indébito dispensa prova do erro (Súmula 322/STJ).
- observacao: Publicação pela data do Jusbrasil (o texto traz a sessão virtual de 12 a 18/09/2023 e a data de 19/09/2023, sem DJe). Ação civil pública de associação de consumidores (interesses individuais homogêneos); a conclusão sobre a efetiva cumulação no caso foi mantida por Súmulas 5 e 7/STJ, mas a tese (item 4 da ementa) é afirmada no voto contra o banco, que sustentava só ser vedada a cumulação com correção e juros remuneratórios.

ementa:
> AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. CIVIL, PROCESSO CIVIL E CONSUMIDOR. AÇÃO CIVIL PÚBLICA. INTERESSES INDIVIDUAIS HOMOGÊNEOS. 1. VIOLAÇÃO DOS ARTS. 489 E 1.022 DO CPC . OMISSÃO E NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO CONFIGURAÇÃO. 2. LEGITIMIDADE ATIVA DAS ASSOCIAÇÕES. RECONHECIMENTO. AUTORIZAÇÃO ASSEMBLEAR. DESNECESSIDADE. 3. INTERESSE PROCESSUAL. NECESSIDADE DE INTERPRETAÇÃO DE CLÁUSULAS CONTRATUAIS E DO REEXAME DE FATOS E PROVAS DOS AUTOS. INCIDÊNCIA DAS SÚMULAS NºS 5 E 7 DO STJ. 4. COMISSÃO DE PERMANÊNCIA. IMPOSSIBILIDADE DE CUMULAÇÃO COM OUTROS ENCARGOS, INCLUSIVE MORATÓRIOS. 5. VIOLAÇÃO AOS PRINCÍPIOS DA ISONOMIA E DA LIVRE CONCORRÊNCIA. ALEGAÇÃO GENÉRICA. INCIDÊNCIA DA SÚMULA Nº 284 DO STF. 6. REPETIÇÃO DE INDÉBITO . CABIMENTO. COMPROVAÇÃO DE ERRO NO PAGAMENTO. DISPENSABILIDADE. 7. PUBLICAÇÃO DA SENTENÇA EM JORNAIS DE GRANDE CIRCULAÇÃO. VIOLAÇÃO A DISPOSITIVOS CONSTITUCIONAIS. IMPOSSIBILIDADE DE ANÁLISE DA MATÉRIA, SOB PENA DE USURPAÇÃO DA COMPETÊNCIA DO STF. AGRAVO INTERNO NÃO PROVIDO.
> 1. Inexistem os vícios elencados nos arts. 489 e 1.022 do CPC, sendo forçoso reconhecer que a pretensão recursal ostenta caráter nitidamente infringente, visando rediscutir matéria que já foi analisada.
> 2. Para a defesa coletiva, são legitimadas concorrentes as associações legalmente constituídas há pelo menos um ano e que incluam entre seus fins institucionais a defesa dos interesses e direitos protegidos por este código, dispensada a autorização assemblear.
> 3. Rever as conclusões quanto à efetiva cumulação da comissão de permanência com outros encargos demandaria, necessariamente, reexame do conjunto fático- probatório dos autos e do contrato firmado entre as partes, o que é vedado em razão dos óbices das Súmulas nºs 5 e 7 do STJ.
> 4. A cobrança de comissão de permanência, cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato, exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual (Súmula nº 472 /STJ .
> 5. A simples alegação genérica de violação de princípios, sem qualquer fundamento prático para reversão do julgado, atrai a incidência da Súmula nº 284 do STF, que dispõe: É inadmissível o recurso extraordinário, quando a deficiência na sua fundamentação não permitir a exata compreensão da controvérsia.
> 6. A compensação de valores e a repetição de indébito são cabíveis sempre que verificado o pagamento indevido, em repúdio ao enriquecimento ilícito de quem o receber, independentemente da comprovação do erro, nos termos da Súmula nº 322 do STJ.
> 7. É inadmissível, em recurso especial, a análise de suposta violação de dispositivos constitucionais, sob pena de se usurpar a competência do Supremo Tribunal Federal, nos termos do art. 102 da CF.
> 8. Agravo interno não provido.

### STJ · AgInt nos EDcl no REsp 2.031.717/PR
- regras: R01, R02
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt nos EDcl no REsp 2.031.717/PR
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2024-02-26
- publicacao: 2024-02-29
- precedente_qualificado: Súmula 472/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2548913848
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão recente de Turma que reafirma (item 2 da ementa) que a comissão de permanência só é admitida sem cumulação com correção monetária, juros remuneratórios, moratórios e multa, porque tem a mesma natureza desses encargos em conjunto (Súmulas 294 e 472), evitando dupla penalização; serve também a tomador pessoa jurídica (sem CDC).
- observacao: Resultado concreto desfavorável ao tomador (o TJPR reconheceu comissão pactuada e cobrada de forma isolada, e o STJ manteve por Súmulas 5 e 7); usar só pela tese do item 2. Tomador pessoa jurídica (crédito rotativo). DJe/STJ de 29/02/2024 conforme o texto.

ementa:
> AGRAVO INTERNO. EMBARGOS DE DECLARAÇÃO. RECURSO ESPECIAL. EMBARGOS À MONITÓRIA. CONTRATO DE ABERTURA DE CRÉDITO. REALIZAÇÃO DE PROVA PERICIAL. TAXA DE JUROS REMUNERATÓRIOS PRATICADAS PELO BANCO. AUSÊNCIA DE ABUSIVIDADE. CAPITALIZAÇÃO DOS JUROS. EXPRESSA PACTUAÇÃO. COMISSÃO DE PERMANÊNCIA. POSSIBILIDADE DE COBRANÇA. SÚMULA N. 472 DO STJ. ENCARGOS CONTRATUAIS PACTUADOS. REEXAME CONTRATUAL E FÁTICO DOS AUTOS. SÚMULAS N. 5 E 7 DO STJ.
> 1. Não cabe, em recurso especial, reexaminar matéria fático-probatória e interpretar cláusulas contratuais (Súmulas n. 5 e 7 /STJ).
> 2. A jurisprudência do STJ firmou o entendimento de que a comissão de permanência pode ser autorizada, de acordo com a Súmula n. 294 do STJ, desde que sem cumulação com correção monetária, com juros remuneratórios e moratórios e multa. Tal prática visa a evitar a ocorrência de dupla penalização, porque a comissão de permanência possui a mesma natureza desses encargos, conjuntamente, conforme estabelecido na Súmula n. 472 do STJ.
> 3. Agravo interno a que se nega provimento.

## R02 — Comissão de permanência — teto: soma dos encargos, limitada à taxa média BACEN

Tese: O valor da comissão de permanência tem como teto a soma dos encargos remuneratórios e moratórios previstos no contrato (juros remuneratórios à taxa média de mercado do BACEN, limitada à taxa contratada; juros de mora até 1% ao mês; multa de até 2%), e o que exceder esse teto é decotado e restituído.

Entradas STJ (repetitivo Tema 52, AgInt no AREsp 1.800.828/RS e AgInt nos EDcl no REsp 2.031.717/PR): constam sob R01, com `regras` incluindo R02.

### TJMT · Apelação Cível 0036624-88.2013.8.11.0041
- regras: R02
- posicao: FAV
- tribunal: TJMT
- classe_numero: Apelação Cível 0036624-88.2013.8.11.0041
- orgao: Segunda Câmara de Direito Privado
- relator: Des. Marilsen Andrade Addario
- julgamento: 2026-09-02
- publicacao: 2026-09-13
- precedente_qualificado: Tema 52/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mt/7319159282
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Aplicação direta do Tema 52 em segundo juízo de retratação (após decisão do STJ): a comissão de permanência fica isolada, limitada à soma de juros remuneratórios (taxa média, sem passar a contratada), juros de mora de 1% ao mês e multa de 2%, com exclusão da cobrança separada de juros moratórios, multa e correção monetária e restituição simples do excesso.
- observacao: Faltou no TJPR (os acórdãos favoráveis do TJPR que localizei não trazem a ementa no inteiro teor do conector; ver relatório). Cautela: a sentença havia excluído a comissão de permanência e mantido os encargos de mora; a retratação, por determinação do STJ (decisão monocrática, Súmulas 5 e 7), manteve a comissão isolada e dentro do teto, o que é menos favorável ao tomador que a sentença; citar apenas pela tese do teto e da vedação de cumulação. Contrato de 2012 (anterior a 01/09/2017). Ementa copiada sem o cabeçalho de identificação das partes que antecede o texto. Publicação pela data do Jusbrasil.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL - SEGUNDO JUÍZO DE RETRATAÇÃO - RECURSO DE APELAÇÃO - AÇÃO DE REVISÃO CONTRATUAL - CÉDULA DE CRÉDITO BANCÁRIO - COMISSÃO DE PERMANÊNCIA - ADEQUAÇÃO AOS PARÂMETROS DO STJ - TEMA REPETITIVO Nº 52 - CONSERVAÇÃO DOS NEGÓCIOS JURÍDICOS - REPETIÇÃO DE INDÉBITO NA FORMA SIMPLES - JUÍZO DE RETRATAÇÃO POSITIVO.
> I. Caso em exame
> 1. Trata-se de segundo Juízo de Retratação, instaurado com fundamento no art. 1.030, II, do Código de Processo Civil, em razão de decisão monocrática proferida no REsp nº 2.175.877/MT.
> II. Questão em discussão
> 2. A questão em discussão consiste em adequar o julgado aos parâmetros fixados pelo Superior Tribunal de Justiça no Tema Repetitivo nº 52, mantendo a comissão de permanência de forma isolada e excluindo os encargos excessivos, em observância ao princípio da conservação dos negócios jurídicos.
> III. Razões de decidir
> 3. O Tema Repetitivo nº 52 do STJ estabelece que a comissão de permanência é válida quando limitada à soma dos encargos remuneratórios e moratórios previstos no contrato, devendo incidir de forma isolada.
> 4. A cláusula contratual pode ser adequada aos parâmetros legais mediante decote dos encargos excessivos, preservando-se a vontade das partes em homenagem ao princípio da conservação dos negócios jurídicos.
> 5. A cobrança de comissão de permanência exclui a exigibilidade dos juros remuneratórios, moratórios e multa contratual cobrados separadamente, conforme Súmula 472 do STJ.
> 6. Eventual diferença cobrada indevidamente deve ser restituída na forma simples, independentemente da comprovação do erro no pagamento.
> IV. Dispositivo e tese
> 7. Juízo de retratação positivo. Reforma parcial do acórdão anteriormente proferido.
> Tese de julgamento: "1. A comissão de permanência deve ser mantida de forma isolada, limitada à soma dos encargos remuneratórios e moratórios previstos no contrato, excluindo-se a cobrança separada de outros encargos moratórios. 2. O princípio da conservação dos negócios jurídicos impõe a adequação de cláusulas contratuais aos parâmetros legais, ao invés de sua nulidade, quando possível o aproveitamento."

## R03 — Comissão de permanência disfarçada (encargo de inadimplência sob outro nome)

Tese: O encargo exclusivo da inadimplência que, sob outro nome ("juros remuneratórios para operações em atraso", "juros de inadimplência", "encargos de atraso"), reconstitui juros remuneratórios, juros moratórios e multa tem a natureza da comissão de permanência e, por isso, sofre a mesma vedação de cumulação (Súmula 472/STJ; Tema 52/STJ).

### STJ · AgInt no AREsp 2.780.818/SE
- regras: R03
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.780.818/SE
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2026-04-22
- publicacao: 2026-04-27
- precedente_qualificado: Súmula 472/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6795039903
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: A Terceira Turma mantém acórdão que tratou os "juros remuneratórios de inadimplência" do contrato (juros remuneratórios + mora de 1% + multa de 2%) como comissão de permanência camuflada e afirma que, firmada essa premissa, a vedação de cumulação com juros moratórios e multa está em linha com a Súmula 472/STJ e o Tema 52.
- observacao: O STJ não define critério próprio para reconhecer a "camuflagem": trata a qualificação do encargo como interpretação de cláusula (Súmula 5) e só afirma a vedação depois de "estabelecida a premissa fática". Não há tema repetitivo específico. Contrato de financiamento de veículo; o banco invocou a Res. CMN 4.558/2017 e os repetitivos, mas o acórdão não examina a resolução. Publicação pela data do Jusbrasil (sessão virtual de 14 a 22/04/2026).

ementa:
> PROCESSUAL CIVIL E BANCÁRIO. AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO. ENCARGOS DE INADIMPLÊNCIA. "COMISSÃO DE PERMANÊNCIA CAMUFLADA". CONCLUSÃO DO TRIBUNAL DE ORIGEM COM BASE NA ANÁLISE DE CLÁUSULAS CONTRATUAIS. IMPOSSIBILIDADE DE REVISÃO. INCIDÊNCIA DA SÚMULA 5/STJ. ACÓRDÃO RECORRIDO EM CONSONÂNCIA COM A JURISPRUDÊNCIA DO STJ. SÚMULA 83/STJ.
> 1. O Tribunal de origem, soberano na análise do conjunto fático-probatório e das cláusulas contratuais, concluiu que a cobrança de "juros remuneratórios de inadimplência" configurava, na realidade, comissão de permanência disfarçada, sendo indevida sua cumulação com outros encargos moratórios.
> 2. A pretensão de afastar a conclusão do acórdão recorrido, para reconhecer a legalidade da cobrança cumulativa dos encargos de inadimplência, demandaria, inevitavelmente, a reinterpretação das cláusulas do contrato firmado entre as partes, o que encontra óbice no enunciado da Súmula n. 5 do STJ.
> 3. Estabelecida a premissa fática de que o encargo cobrado se refere à comissão de permanência, o acórdão recorrido, ao vedar sua cumulação com juros moratórios e multa contratual, alinhou-se à jurisprudência pacífica desta Corte Superior, consolidada no enunciado da Súmula n. 472/STJ, o que atrai a incidência da Súmula n. 83/STJ como óbice ao conhecimento do recurso especial.
> Agravo interno improvido.

### STJ · REsp 2.094.237/SP
- regras: R03
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.094.237/SP
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2025-10-13
- publicacao: 2025-10-16
- precedente_qualificado: Tema 52/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6267882413
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: o STJ (Terceira Turma, 2025) reformou acórdão do TJSP que tratava como comissão de permanência disfarçada os juros remuneratórios previstos para a inadimplência, decidindo que, desde que o contrato não preveja comissão de permanência, é possível cumular juros remuneratórios, juros de mora e multa. A inicial deve, portanto, demonstrar no contrato os traços da substituição (rubrica própria e taxa diferenciada para o atraso, função de comissão), e não apenas a incidência de juros remuneratórios após o vencimento.
- observacao: A ementa registra o ponto de forma genérica ("A comissão de permanência é válida desde que não cumulada..."); a solução sobre a cumulação sem previsão de comissão consta no voto. Contrato de financiamento de veículo de 2011 (anterior a 01/09/2017). Fica em tensão com o AgInt no AREsp 2.780.818/SE (mesma Turma, 2026), que mantém a equiparação por Súmula 5. Publicação pela data do Jusbrasil (sessão virtual de 07 a 13/10/2025).

ementa:
> DIREITO BANCÁRIO. RECURSO ESPECIAL. CÉDULA DE CRÉDITO BANCÁRIO. COMISSÃO DE PERMANÊNCIA. CUMULAÇÃO DE ENCARGOS.
> I. CASO EM EXAME
> 1. Recurso especial interposto contra acórdão do Tribunal de Justiça do Estado de São Paulo que reformou sentença de primeiro grau, determinando a restituição de valores pagos a título de comissão de permanência cumulada com encargos moratórios em contrato de financiamento de veículo.
> II. QUESTÃO EM DISCUSSÃO
> 2. A questão em discussão consiste em saber se é possível a cumulação de comissão de permanência com juros remuneratórios, juros moratórios, multa contratual ou correção monetária em caso de inadimplemento contratual, conforme entendimento do REsp Repetitivo n. 1.058.114/RS.
> III. RAZÕES DE DECIDIR
> 3. A comissão de permanência é válida desde que não cumulada com outros encargos moratórios, conforme a Súmula n. 472 do STJ.
> 4. O contrato não prevê a cobrança cumulada de comissão de permanência com outros encargos de mora durante o período de inadimplência.
> 5. A sentença de primeiro grau deve ser restabelecida, pois não houve violação ao disposto no art. 52, § 1°, do CDC.
> IV. DISPOSITIVO
> 6. Resultado do Julgamento: Recurso provido para restabelecer a sentença de primeiro grau.

### TJMT · Apelação Cível 1028080-89.2024.8.11.0015
- regras: R03
- posicao: FAV
- tribunal: TJMT
- classe_numero: Apelação Cível 1028080-89.2024.8.11.0015
- orgao: Quarta Câmara de Direito Privado
- relator: Des. Serly Marcondes Alves
- julgamento: 2026-02-11
- publicacao: 2026-02-13
- precedente_qualificado: Súmula 472/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mt/5578970477
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Mantém sentença que reconheceu como comissão de permanência disfarçada a previsão de juros remuneratórios para o período de inadimplência cumulados com juros de mora e multa, por reunirem encargos remuneratórios e moratórios com o mesmo fato gerador (Súmula 472/STJ), e afastou a cumulação.
- observacao: Faltou no TJPR (ver relatório). O resultado prático é a exclusão da cumulação (a sentença afastou a incidência conjunta de juros remuneratórios, mora e multa na inadimplência). O voto transcreve a Súmula 472 de forma inexata; não citar o trecho do voto, só a ementa. A ementa confirma restituição em dobro, ponto não alinhado a esta tese e que não deve ser usado. Há acórdãos do próprio TJMT em sentido contrário (ver relatório). Publicação pela data do Jusbrasil.

ementa:
> DIREITO CIVIL E DO CONSUMIDOR. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO C/C INDENIZAÇÃO. CÉDULA DE CRÉDITO BANCÁRIO. JUROS REMUNERATÓRIOS INCIDENTES NA INADIMPLÊNCIA. CUMULAÇÃO COM JUROS DE MORA E MULTA. COMISSÃO DE PERMANÊNCIA DISFARÇADA. ABUSIVIDADE. SÚMULA 472/STJ. REPETIÇÃO DO INDÉBITO. TARIFA DE REGISTRO DE CONTRATO. TEMA 958/STJ.LEGALIDADE. SENTENÇA MANTIDA. RECURSO DESPROVIDO.
> I. CASO EM EXAME
> 1. Apelação cível interposta por cooperativa de crédito contra sentença proferida em ação revisional de contrato bancário c/c pedido de indenização, que reconheceu a nulidade de cláusula contratual por permitir a cobrança cumulativa de encargos no período de inadimplência, afastou a incidência conjunta de juros remuneratórios, juros de mora e multa contratual, condenou à repetição do indébito em dobro e determinou a apuração do débito em liquidação, mantendo hígida a cobrança da tarifa de registro de contrato.
> II. QUESTÃO EM DISCUSSÃO
> 1. Há duas questões em discussão: (i) definir se a incidência de juros remuneratórios no período de inadimplência, cumulados com juros de mora e multa contratual, configura comissão de permanência disfarçada e, portanto, prática abusiva; (ii) estabelecer se é válida a cobrança da tarifa de registro de contrato prevista na cédula de crédito bancário.
> III. RAZÕES DE DECIDIR
> 1. A relação jurídica possui natureza de consumo, sujeitando-se à incidência do Código de Defesa do Consumidor e ao controle judicial de cláusulas abusivas que imponham desvantagem exagerada ao consumidor.
> 1. A previsão contratual de juros remuneratórios incidentes após o vencimento, cumulados com juros de mora e multa, caracteriza a cobrança de comissão de permanência de forma disfarçada, por reunir encargos remuneratórios e moratórios com o mesmo fato gerador.
> 1. A cumulação de encargos remuneratórios e moratórios no período de inadimplência viola a jurisprudência consolidada do Superior Tribunal de Justiça, especialmente a Súmula 472/STJ.
> 1. A exclusão da cobrança cumulativa impõe a restituição, em dobro, dos valores pagos indevidamente, ressalvado o direito à compensação.
> 1. A tarifa de registro de contrato é válida quando prevista contratualmente e comprovada a efetiva prestação do serviço, nos termos do Tema 958 /STJ, inexistindo nos autos demonstração de abusividade ou onerosidade excessiva.
> 1. A sentença recorrida observa os princípios da boa-fé objetiva, do equilíbrio contratual e da função social do contrato, devendo ser integralmente mantida.
> IV. DISPOSITIVO E TESE
> 1. Recurso desprovido.
> Tese de julgamento: 1. A incidência de juros remuneratórios no período de inadimplência, cumulada com juros de mora e multa contratual, configura comissão de permanência disfarçada e é vedada pela Súmula 472/STJ. 1. É devida a repetição do indébito em dobro quando comprovada a cobrança indevida de encargos cumulativos no contrato bancário. 1. É válida a cobrança da tarifa de registro de contrato quando prevista no instrumento contratual e ausente prova de abusividade ou serviço não prestado.
> Dispositivos relevantes citados: CDC, arts. 6º, IV,e 51, IV; CPC, art. 85, § 11 . Jurisprudência relevante citada: STJ, Súmula 472; STJ, Tema 958 (REsp nº 1.578.553/SP); TJMT, Apelação Cível nº 1020794-84.2021.8.11.0041, Quarta Câmara de Direito Privado, j. 14.11.2025.

### TJMT · Apelação Cível 1000156-79.2023.8.11.0002
- regras: R03
- posicao: FAV
- tribunal: TJMT
- classe_numero: Apelação Cível 1000156-79.2023.8.11.0002
- orgao: Terceira Câmara de Direito Privado
- relator: Des. Antonia Siqueira Gonçalves
- julgamento: 2026-01-28
- publicacao: 2026-01-31
- precedente_qualificado: Súmula 472/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mt/5509930941
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Desprovê a apelação do banco e mantém a sentença que afastou os juros remuneratórios do período de inadimplência: ainda que a cláusula não mencione "comissão de permanência", a previsão de juros mensais, juros de mora e multa sobre o saldo devedor atualizado é a comissão de permanência sob outra roupagem, cuja cumulação é vedada.
- observacao: Faltou no TJPR (ver relatório). Aqui a consequência foi excluir os juros remuneratórios e manter mora e multa (diferente dos acórdãos do TJPR que li, que mantêm o encargo único isolado e afastam mora e multa); a petição deve pedir a consequência que mais convier ao contrato. Ementa com falhas de espaçamento do texto original, mantidas. O TJMT é dividido (ver relatório). Publicação pela data do Jusbrasil.

ementa:
> APELAÇÃO CÍVEL - AÇÃO DE BUSCA E APREENSÃO COMISSÃO DE PERMANÊNCIA DISFARÇADA - CUMULAÇÃO COM JUROS REMUNERATÓRIOS E OUTROS ENCARGOS - IMPOSSIBILIDADE - CUMULAÇÃO INDEVIDA - SENTENÇA MANTIDA - RECURSO DESPROVIDO. É possível a revisão de cláusulas pactuadas quando demonstrada a onerosidade excessiva ao consumidor, admitindo-se a relativização do princípio pacta sunt servanda a fim de estabelecer o equilíbrio contratual. A comissão de permanência constitui encargo incidente quando constituída a mora, apresentando o caráter múltiplo de atualizar e remunerar a moeda, não podendo haver a cumulação de multa com juros e comissão de permanência, o que não é permitido, por isso, merece ser mantida a sentença recorrida.

## R04 — TAC (tarifa de abertura de crédito) vedada em contratos posteriores a 30/04/2008

Tese: A tarifa de abertura de crédito (TAC), ou qualquer outra denominação para o mesmo fato gerador, não tem respaldo legal em contrato bancário de pessoa física celebrado a partir de 30/04/2008 (Res. CMN 3.518/2007 e Súmula 565/STJ), sendo indevida a cobrança e devida a restituição.

### STJ · REsp 1.251.331/RS
- regras: R04, R06
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.251.331/RS
- orgao: Segunda Seção
- relator: Min. Maria Isabel Gallotti
- julgamento: 2013-08-28
- publicacao: 2013-10-24
- precedente_qualificado: Tema 618/STJ (repetitivo); Súmula 565/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106302421
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case: desde 30/04/2008 a TAC e a TEC não têm mais respaldo legal para pessoa física (2ª tese), de modo que a cobrança em contrato posterior é ilegal.
- observacao: Publicação pela data do Jusbrasil (confere com o DJe de 24/10/2013 citado em acórdão do TJPR). O texto do Jusbrasil não traz o número do Tema: 618/STJ vem do briefing, e um acórdão do TJPR consultado cita estes repetitivos como "Tema 620"; conferir a numeração no site do STJ antes de citar. Limites que viram ressalva na peça: era válida a TAC/TEC em contratos até 30/04/2008 (ressalvado abuso em concreto); a Tarifa de Cadastro permanece válida no início do relacionamento (Súmula 566/STJ); a vedação é para pessoa física (TAC em contrato com pessoa jurídica é admitida, inclusive nos TJs).

ementa:
> CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. CONTRATO DE FINANCIAMENTO COM GARANTIA DE ALIENAÇÃO FIDUCIÁRIA.
> DIVERGÊNCIA. CAPITALIZAÇÃO DE JUROS. JUROS COMPOSTOS. MEDIDA PROVISÓRIA 2.170-36/2001. RECURSOS REPETITIVOS.
> CPC, ART. 543-C. TARIFAS ADMINISTRATIVAS PARA ABERTURA DE CRÉDITO (TAC), E EMISSÃO DE CARNÊ (TEC). EXPRESSA
> PREVISÃO CONTRATUAL. COBRANÇA. LEGITIMIDADE. PRECEDENTES. MÚTUO ACESSÓRIO PARA PAGAMENTO PARCELADO DO IMPOSTO
> SOBRE OPERAÇÕES FINANCEIRAS (IOF). POSSIBILIDADE. 1. "A capitalização dos juros em periodicidade inferior à
> anual deve vir pactuada de forma expressa e clara. A previsão no contrato bancário de taxa de juros anual
> superior ao duodécuplo da mensal é suficiente para permitir a cobrança da taxa efetiva anual contratada" (2a
> Seção, REsp 973.827/RS, julgado na forma do art. 543-C do CPC, acórdão de minha relatoria, DJe de 24.9.2012).
> 2. Nos termos dos arts. 4º e 9º da Lei 4.595/1964, recebida pela Constituição como lei complementar, compete
> ao Conselho Monetário Nacional dispor sobre taxa de juros e sobre a remuneração dos serviços bancários, e ao
> Banco Central do Brasil fazer cumprir as normas expedidas pelo CMN. 3. Ao tempo da Resolução CMN 2.303/1996, a
> orientação estatal quanto à cobrança de tarifas pelas instituições financeiras era essencialmente não
> intervencionista, vale dizer, "a regulamentação facultava às instituições financeiras a cobrança pela
> prestação de quaisquer tipos de serviços, com exceção daqueles que a norma definia como básicos, desde que
> fossem efetivamente contratados e prestados ao cliente, assim como respeitassem os procedimentos voltados a
> assegurar a transparência da política de preços adotada pela instituição." 4. Com o início da vigência da
> Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços bancários prioritários para pessoas físicas
> ficou limitada às hipóteses taxativamente previstas em norma padronizadora expedida pelo Banco Central do
> Brasil. 5. A Tarifa de Abertura de Crédito (TAC) e a Tarifa de Emissão de Carnê (TEC) não foram previstas na
> Tabela anexa à Circular BACEN 3.371/2007 e atos normativos que a sucederam, de forma que não mais é válida sua
> pactuação em contratos posteriores a 30.4.2008. 6. A cobrança de tais tarifas (TAC e TEC) é permitida,
> portanto, se baseada em contratos celebrados até 30.4.2008, ressalvado abuso devidamente comprovado caso a
> caso, por meio da invocação de parâmetros objetivos de mercado e circunstâncias do caso concreto, não bastando
> a mera remissão a conceitos jurídicos abstratos ou à convicção subjetiva do magistrado. 7. Permanece legítima
> a estipulação da Tarifa de Cadastro, a qual remunera o serviço de "realização de pesquisa em serviços de
> proteção ao crédito, base de dados e informações cadastrais, e tratamento de dados e informações necessários
> ao inicio de relacionamento decorrente da abertura de conta de depósito à vista ou de poupança ou contratação
> de operação de crédito ou de arrendamento mercantil, não podendo ser cobrada cumulativamente" (Tabela anexa à
> vigente Resolução CMN 3.919/2010, com a redação dada pela Resolução 4.021/2011). 8. É lícito aos contratantes
> convencionar o pagamento do Imposto sobre Operações Financeiras e de Crédito (IOF) por meio financiamento
> acessório ao mútuo principal, sujeitando-o aos mesmos encargos contratuais. 9. Teses para os efeitos do art.
> 543-C do CPC: - 1a Tese: Nos contratos bancários celebrados até 30.4.2008 (fim da vigência da Resolução CMN
> 2.303/96) era válida a pactuação das tarifas de abertura de crédito (TAC) e de emissão de carnê (TEC), ou
> outra denominação para o mesmo fato gerador, ressalvado o exame de abusividade em cada caso concreto. - 2a
> Tese: Com a vigência da Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços bancários prioritários
> para pessoas físicas ficou limitada às hipóteses taxativamente previstas em norma padronizadora expedida pela
> autoridade monetária. Desde então, não mais tem respaldo legal a contratação da Tarifa de Emissão de Carnê
> (TEC) e da Tarifa de Abertura de Crédito (TAC), ou outra denominação para o mesmo fato gerador. Permanece
> válida a Tarifa de Cadastro expressamente tipificada em ato normativo padronizador da autoridade monetária, a
> qual somente pode ser cobrada no início do relacionamento entre o consumidor e a instituição financeira. - 3a
> Tese: Podem as partes convencionar o pagamento do Imposto sobre Operações Financeiras e de Crédito (IOF) por
> meio de financiamento acessório ao mútuo principal, sujeitando-o aos mesmos encargos contratuais. 10. Recurso
> especial parcialmente provido.

### TJPR · Recurso Inominado Cível 0003835-59.2023.8.16.0069
- regras: R04
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0003835-59.2023.8.16.0069
- orgao: 3ª Turma Recursal dos Juizados Especiais
- relator: Juiz Juan Daniel Pereira Sobreiro
- julgamento: 2024-04-05
- publicacao: 2024-04-09
- precedente_qualificado: Súmula 565/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/2336477935
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O TJPR declara inexigível e manda restituir a TAC cobrada em financiamento firmado após 30/04/2008, aplicando a Súmula 565/STJ.
- observacao: Turma Recursal (Juizado Especial), não Câmara Cível. A ementa mistura outros pontos (seguro e tarifa DOC/TED não contratados); o ponto da TAC é o descrito na ementa e no voto (contrato de 04/11/2020). Publicação pela data do Jusbrasil.

ementa:
> RECURSO INOMINADO. BANCÁRIO. DESCONTOS EM CONTA BANCÁRIA SOB A RUBRICA “BRADESCO VIDA E PREVIDÊNCIA” E
> “DOC/TED INTERNE”. AUSÊNCIA DE CONTRATAÇÃO. RESTITUIÇÃO DEVIDA. TARIFA DE ABERTURA DE CRÉDITO (TAC).
> INEXIGIBILIDADE DA COBRANÇA. CONTRATO FIRMADO APÓS 30.04.2008. INTELIGÊNCIA DA SÚMULA N. 565 DO SUPERIOR
> TRIBUNAL DE JUSTIÇA. INSURGÊNCIA ATINENTE AO DANO MORAL. MATÉRIA NÃO DISCUTIDA NO CASO CONCRETO, TAMPOUCO
> OBJETO DA SENTENÇA. NÃO CONHECIMENTO DO RECURSO NESSE PONTO. SENTENÇA MANTIDA. RECURSO CONHECIDO EM PARTE E,
> NA PARTE CONHECIDA, DESPROVIDO.

## R06 — TEC (tarifa de emissão de carnê/boleto) vedada em contratos posteriores a 30/04/2008

Tese: A tarifa de emissão de carnê ou boleto (TEC), ou outra denominação para o mesmo fato gerador, não tem respaldo legal em contrato bancário de pessoa física celebrado a partir de 30/04/2008 (Res. CMN 3.518/2007 e Súmula 565/STJ), sendo indevida a cobrança e devida a restituição.

### STJ · REsp 1.255.573/RS
- regras: R06, R04
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.255.573/RS
- orgao: Segunda Seção
- relator: Min. Maria Isabel Gallotti
- julgamento: 2013-08-28
- publicacao: 2013-10-24
- precedente_qualificado: Tema 619/STJ (repetitivo); Súmula 565/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106299943
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Repetitivo gêmeo do REsp 1.251.331/RS: a TEC e a TAC deixaram de ser pactuáveis em contratos posteriores a 30/04/2008, e a cobrança só é lícita nos contratos até essa data.
- observacao: Publicação pela data do Jusbrasil. O número do Tema (619) vem do briefing e não aparece no texto do Jusbrasil; conferir no site do STJ (ver observação do REsp 1.251.331/RS). Mesmos limites: validade até 30/04/2008, Tarifa de Cadastro lícita (Súmula 566/STJ), vedação voltada à pessoa física. A ementa também trata de comissão de permanência e financiamento do IOF.

ementa:
> CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. CONTRATO DE FINANCIAMENTO COM GARANTIA DE ALIENAÇÃO FIDUCIÁRIA.
> COMISSÃO DE PERMANÊNCIA. COMPENSAÇÃO/REPETIÇÃO SIMPLES DO INDÉBITO. RECURSOS REPETITIVOS. TARIFAS BANCÁRIAS.
> TAC E TEC. EXPRESSA PREVISÃO CONTRATUAL. COBRANÇA. LEGITIMIDADE. PRECEDENTES. FINANCIAMENTO DO IOF.
> POSSIBILIDADE. 1. A comissão de permanência não pode ser cumulada com quaisquer outros encargos remuneratórios
> ou moratórios (enunciados Súmulas 30, 294 e 472 do STJ). 2. Tratando-se de relação de consumo ou de contrato
> de adesão, a compensação/repetição simples do indébito independe da prova do erro (Enunciado 322 da Súmula do
> STJ). 3. Nos termos dos arts. 4º e 9º da Lei 4.595/1964, recebida pela Constituição como lei complementar,
> compete ao Conselho Monetário Nacional dispor sobre taxa de juros e sobre a remuneração dos serviços
> bancários, e ao Banco Central do Brasil fazer cumprir as normas expedidas pelo CMN. 4. Ao tempo da Resolução
> CMN 2.303/1996, a orientação estatal quanto à cobrança de tarifas pelas instituições financeiras era
> essencialmente não intervencionista, vale dizer, "a regulamentação facultava às instituições financeiras a
> cobrança pela prestação de quaisquer tipos de serviços, com exceção daqueles que a norma definia como básicos,
> desde que fossem efetivamente contratados e prestados ao cliente, assim como respeitassem os procedimentos
> voltados a assegurar a transparência da política de preços adotada pela instituição." 5. Com o início da
> vigência da Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços bancários prioritários para
> pessoas físicas ficou limitada às hipóteses taxativamente previstas em norma padronizadora expedida pelo Banco
> Central do Brasil. 6. A Tarifa de Abertura de Crédito (TAC) e a Tarifa de Emissão de Carnê (TEC) não foram
> previstas na Tabela anexa à Circular BACEN 3.371/2007 e atos normativos que a sucederam, de forma que não mais
> é válida sua pactuação em contratos posteriores a 30.4.2008. 7. A cobrança de tais tarifas (TAC e TEC) é
> permitida, portanto, se baseada em contratos celebrados até 30.4.2008, ressalvado abuso devidamente comprovado
> caso a caso, por meio da invocação de parâmetros objetivos de mercado e circunstâncias do caso concreto, não
> bastando a mera remissão a conceitos jurídicos abstratos ou à convicção subjetiva do magistrado. 8. Permanece
> legítima a estipulação da Tarifa de Cadastro, a qual remunera o serviço de "realização de pesquisa em serviços
> de proteção ao crédito, base de dados e informações cadastrais, e tratamento de dados e informações
> necessários ao inicio de relacionamento decorrente da abertura de conta de depósito à vista ou de poupança ou
> contratação de operação de crédito ou de arrendamento mercantil, não podendo ser cobrada cumulativamente"
> (Tabela anexa à vigente Resolução CMN 3.919/2010, com a redação dada pela Resolução 4.021/2011). 9. É lícito
> aos contratantes convencionar o pagamento do Imposto sobre Operações Financeiras e de Crédito (IOF) por meio
> financiamento acessório ao mútuo principal, sujeitando-o aos mesmos encargos contratuais. 10. Teses para os
> efeitos do art. 543-C do CPC: - 1a Tese: Nos contratos bancários celebrados até 30.4.2008 (fim da vigência da
> Resolução CMN 2.303/96) era válida a pactuação das tarifas de abertura de crédito (TAC) e de emissão de carnê
> (TEC), ou outra denominação para o mesmo fato gerador, ressalvado o exame de abusividade em cada caso
> concreto. - 2a Tese: Com a vigência da Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços
> bancários prioritários para pessoas físicas ficou limitada às hipóteses taxativamente previstas em norma
> padronizadora expedida pela autoridade monetária. Desde então, não mais tem respaldo legal a contratação da
> Tarifa de Emissão de Carnê (TEC) e da Tarifa de Abertura de Crédito (TAC), ou outra denominação para o mesmo
> fato gerador. Permanece válida a Tarifa de Cadastro expressamente tipificada em ato normativo padronizador da
> autoridade monetária, a qual somente pode ser cobrada no início do relacionamento entre o consumidor e a
> instituição financeira. - 3a Tese: Podem as partes convencionar o pagamento do Imposto sobre Operações
> Financeiras e de Crédito (IOF) por meio de financiamento acessório ao mútuo principal, sujeitando-o aos mesmos
> encargos contratuais. 11 . Recurso especial conhecido e parcialmente provido.

## R09 — Cláusula de ressarcimento de "serviços de terceiros" sem especificação do serviço

Tese: É abusiva a cláusula que transfere ao consumidor o ressarcimento de "serviços de terceiros" sem especificar o serviço efetivamente prestado, por violar o direito à informação adequada e impor desvantagem exagerada (CDC, arts. 6º, III, e 51, IV).

### STJ · REsp 1.578.553/SP
- regras: R09, R10, R29
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.578.553/SP
- orgao: Segunda Seção
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2018-11-28
- publicacao: 2018-12-06
- precedente_qualificado: Tema 958/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106314337
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Tese 2.1: abusiva a cláusula de ressarcimento de serviços de terceiros sem especificação do serviço (R09). Tese 2.2: abusivo o ressarcimento da comissão do correspondente bancário em contratos a partir de 25/02/2011 (R10). Base, por analogia, da tese 2.3.1 (cobrança por serviço não prestado) para a comissão flat (R29).
- observacao: Publicação pela data do Jusbrasil (DJe de 6/12/2018 também citado em acórdãos posteriores do STJ). Limite que vira ressalva na peça: tese 2.3 mantém válidas a tarifa de avaliação do bem e a despesa de registro do contrato, se efetivamente prestados e sem onerosidade excessiva; tese 2.2 considera válida a comissão do correspondente em contratos anteriores a 25/02/2011, ressalvada a onerosidade excessiva. Delimitação: contratos de consumo a partir de 30/04/2008. O julgado não trata expressamente de "comissão flat"; o uso em R29 é analógico.

ementa:
> RECURSO ESPECIAL REPETITIVO. TEMA 958/STJ. DIREITO BANCÁRIO. COBRANÇA POR SERVIÇOS DE TERCEIROS, REGISTRO DO
> CONTRATO E AVALIAÇÃO DO BEM. PREVALÊNCIA DAS NORMAS DO DIREITO DO CONSUMIDOR SOBRE A REGULAÇÃO BANCÁRIA.
> EXISTÊNCIA DE NORMA REGULAMENTAR VEDANDO A COBRANÇA A TÍTULO DE COMISSÃO DO CORRESPONDENTE BANCÁRIO. DISTINÇÃO
> ENTRE O CORRESPONDENTE E O TERCEIRO. DESCABIMENTO DA COBRANÇA POR SERVIÇOS NÃO EFETIVAMENTE PRESTADOS.
> POSSIBILIDADE DE CONTROLE DA ABUSIVIDADE DE TARIFAS E DESPESAS EM CADA CASO CONCRETO. 1. DELIMITAÇÃO DA
> CONTROVÉRSIA: Contratos bancários celebrados a partir de 30/04/2008, com instituições financeiras ou
> equiparadas, seja diretamente, seja por intermédio de correspondente bancário, no âmbito das relações de
> consumo. 2. TESES FIXADAS PARA OS FINS DO ART. 1.040 DO CPC/2015: 2.1. Abusividade da cláusula que prevê a
> cobrança de ressarcimento de serviços prestados por terceiros, sem a especificação do serviço a ser
> efetivamente prestado; 2.2. Abusividade da cláusula que prevê o ressarcimento pelo consumidor da comissão do
> correspondente bancário, em contratos celebrados a partir de 25/02/2011, data de entrada em vigor da Res.-CMN
> 3.954/2011, sendo válida a cláusula no período anterior a essa resolução, ressalvado o controle da onerosidade
> excessiva; 2.3. Validade da tarifa de avaliação do bem dado em garantia, bem como da cláusula que prevê o
> ressarcimento de despesa com o registro do contrato, ressalvadas a: 2.3.1. abusividade da cobrança por serviço
> não efetivamente prestado; e a 2.3.2. possibilidade de controle da onerosidade excessiva, em cada caso
> concreto. 3. CASO CONCRETO. 3.1. Aplicação da tese 2.2, declarando-se abusiva, por onerosidade excessiva, a
> cláusula relativa aos serviços de terceiros ("serviços prestados pela revenda"). 3.2. Aplicação da tese 2.3,
> mantendo-se hígidas a despesa de registro do contrato e a tarifa de avaliação do bem dado em garantia. 4.
> RECURSO ESPECIAL PARCIALMENTE PROVIDO.

### STJ · REsp 2.010.549/RO
- regras: R09
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.010.549/RO
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2025-10-20
- publicacao: 2025-10-23
- precedente_qualificado: Tema 958/STJ (aplicação)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/5901044925
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão recente de Turma que mantém a abusividade de tarifa de serviços de terceiros não discriminada em financiamento, reafirmando a tese 2.1 do Tema 958.
- observacao: Recurso conhecido em parte e desprovido. O mérito da tese é afirmado como razão de decidir (item 5 da ementa), mas o recurso esbarrou nas Súmulas 211 e 7/STJ (a ausência de discriminação no contrato é premissa fática do TJRO). Julgamento em sessão virtual de 14 a 20/10/2025; data de julgamento tomada do encerramento da sessão. Publicação pela data do Jusbrasil.

ementa:
> PROCESSUAL CIVIL. RECURSO ESPECIAL. VIOLAÇÃO DO ART. 1.022 DO CPC. INEXISTÊNCIA. AUSÊNCIA DE
> PREQUESTIONAMENTO. SÚMULA N. 211/STJ. SERVIÇO DE TERCEIROS NÃO DESCRIMINADO PELO BANCO NO CONTRATO DE
> FINANCIAMENTO. MODIFICAR AS CONCLUSÕES DO ACÓRDÃO RECORRIDO.SÚMULA N. 7/STJ. INCIDÊNCIA. I. Caso em exame 1.
> Recurso especial interposto contra acórdão do Tribunal de Justiça do Estado de Rondônia que reconheceu a
> abusividade na cobrança de tarifas por serviços de terceiros não discriminados em contratos de financiamento.
> 2. Embargos de declaração opostos pela instituição financeira foram rejeitados, mantendo-se integralmente o
> teor do acórdão embargado. II. Questão em discussão 3. A questão alegada pela recorrente consiste em saber se
> a cobrança de tarifas por serviços de terceiros em contratos de financiamento sem discriminação é abusiva.
> III. Razões de decidir 4. O acórdão recorrido decidiu, de forma fundamentada, acerca dos motivos que ensejaram
> o reconhecimento da abusividade da tarifa cobrada, não comportando acolhimento dos embargos de declaração. 5.
> A cobrança de tarifas por serviços de terceiros sem discriminação dos serviços prestados configura
> abusividade, conforme entendimento pacificado do STJ (Tema n. 958) 6. A alteração das conclusões das
> instâncias ordinárias demandaria o reexame do acervo fático-probatório dos autos, inviável em recurso especial
> em razão do óbice da Súmula n. 7/STJ. IV. Dispositivo Recurso especial parcialmente conhecido e, nessa parte,
> não provido.

### TJPR · Recurso Inominado Cível 0021827-52.2024.8.16.0019
- regras: R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0021827-52.2024.8.16.0019
- orgao: 3ª Turma Recursal dos Juizados Especiais
- relator: Juíza Letícia Zétola Portes
- julgamento: 2025-10-10
- publicacao: 2025-10-14
- precedente_qualificado: Tema 958/STJ (aplicação)
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/5089521995
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O TJPR declara abusiva a tarifa de "despesas com terceiros" lançada de forma genérica no contrato de financiamento de veículo e determina a restituição simples.
- observacao: Turma Recursal (Juizado Especial). Julgado por maioria (um voto vencido); o voto vencido não consta na ementa, e o ponto da tarifa de terceiros foi decidido a favor do consumidor. A ementa também trata de prescrição (aplica o prazo decenal do art. 205 do CC). Publicação pela data do Jusbrasil. Faltou acórdão de Câmara Cível do TJPR com ementa verificável (ver Relatório).

ementa:
> RECURSO INOMINADO. AÇÃO DE REPETIÇÃO DE INDÉBITO. CONTRATO DE FINANCIAMENTO DE VEÍCULO. SENTENÇA QUE
> RECONHECEU PRESCRIÇÃO TRIENAL. NULIDADE DECLARADA. PRAZO PRESCRICIONAL DECENAL (ART. 205 DO CC). ENTENDIMENTO
> CONSOLIDADO NESTA 3ª TURMA RECURSAL. TEORIA DA CAUSA MADURA. JULGAMENTO DO MÉRITO. TARIFA DE “DESPESAS COM
> TERCEIROS”. AUSÊNCIA DE DISCRIMINAÇÃO E DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DOS SERVIÇOS. ABUSIVIDADE
> CONFIGURADA. DEVOLUÇÃO DOS VALORES PAGOS. RECURSO CONHECIDO E PROVIDO. I. Caso em exame 1. Trata-se de recurso
> inominado interposto em face da sentença que extinguiu a ação de repetição de indébito, sob fundamento de
> prescrição trienal, em demanda ajuizada em face do Banco Daycoval S/A. O autor busca a restituição de valores
> cobrados a título de tarifa de “despesas com terceiros” em contrato de financiamento de veículo, alegando
> abusividade da cobrança. II. Questão em discussão 2. As questões em discussão consistem em: (i) saber se deve
> ser afastada a prescrição trienal reconhecida na sentença, aplicando-se o prazo decenal do art. 205 do Código
> Civil; e (ii) saber se a cobrança da tarifa de “despesas com terceiros” é abusiva, impondo a restituição dos
> valores pagos. III. Razões de decidir 3.1. A jurisprudência consolidada desta 3ª Turma Recursal afasta a
> prescrição trienal em ações revisionais e de repetição de indébito, aplicando o prazo decenal do art. 205 do
> CC, com termo inicial no vencimento da última parcela. 3.2. No caso, a última parcela venceu em 29/06/2021 e
> a ação foi ajuizada em 25/07/2024, dentro do prazo decenal, razão pela qual deve ser declarada a nulidade da
> sentença que reconheceu a prescrição. 3.3. Aplicando-se a teoria da causa madura (art. 1.013, § 3º, I, CPC),
> passa-se ao julgamento do mérito. 3.4. A cobrança da tarifa de “despesas com terceiros” é abusiva quando não
> há discriminação dos serviços nem comprovação da efetiva prestação, conforme entendimento do STJ (Tema 958) e
> precedentes desta Turma. 3.5. No caso concreto, o banco não comprovou a realização dos serviços nem apresentou
> documentos que justificassem a cobrança, limitando-se a previsão genérica no contrato. 3.6. Reconhecida a
> abusividade, impõe-se a restituição simples do valor pago, com correção monetária pelo IPCA desde o desembolso
> e juros de mora a partir da citação. IV. Dispositivo 4. Recurso conhecido e provido

## R10 — Comissão do correspondente bancário em contratos a partir de 25/02/2011

Tese: É abusiva a cláusula que transfere ao consumidor o ressarcimento da comissão do correspondente bancário em contratos celebrados a partir de 25/02/2011, data de vigência da Res. CMN 3.954/2011, devendo o valor ser restituído.

Sem entrada própria nesta onda. O julgado verificado para esta tese é o REsp 1.578.553/SP (tese 2.2), listado sob R09 com `regras: R09, R10, R29`. Nenhum acórdão de TJ passou na verificação (ver Relatório).

## R13 — Seguro prestamista — venda casada

Tese: A contratação de seguro prestamista (ou de proteção financeira) imposta pela instituição financeira, sem opção real de contratar ou de escolher outra seguradora, é venda casada (CDC, art. 39, I) e o valor cobrado deve ser restituído.

### STJ · REsp 1.639.259/SP
- regras: R13
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.639.259/SP
- orgao: Segunda Seção
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2018-12-12
- publicacao: 2018-12-17
- precedente_qualificado: Tema 972/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106312540
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case do Tema 972: tese 2.2 (consumidor não pode ser compelido a contratar seguro com a instituição ou seguradora por ela indicada) e, no caso concreto, declarada a venda casada do seguro de proteção financeira com restituição do indébito.
- observacao: Publicação pela data do Jusbrasil (outro julgado cita DJe 19/12/2018; conferir no DJe antes de citar a data). O paradigma gêmeo, REsp 1.639.320/SP (mesma sessão, Tema 972), aplicou ao caso concreto apenas a tese 2.3 (mora); por isso a entrada foi feita com o REsp 1.639.259/SP, que aplica a tese 2.2. Delimitação do repetitivo: contratos bancários celebrados a partir de 30/04/2008, com instituições financeiras ou equiparadas, inclusive via correspondente.

ementa:
> RECURSO ESPECIAL REPETITIVO. TEMA 972/STJ. DIREITO BANCÁRIO. DESPESA DE PRÉ-GRAVAME. VALIDADE NOS CONTRATOS CELEBRADOS ATÉ 25/02/2011. SEGURO DE PROTEÇÃO FINANCEIRA. VENDA CASADA. OCORRÊNCIA. RESTRIÇÃO À ESCOLHA DA SEGURADORA. ANALOGIA COM O ENTENDIMENTO DA SÚMULA 473/STJ. DESCARACTERIZAÇÃO DA MORA. NÃO OCORRÊNCIA. ENCARGOS ACESSÓRIOS. 1. DELIMITAÇÃO DA CONTROVÉRSIA: Contratos bancários celebrados a partir de 30/04/2008, com instituições financeiras ou equiparadas, seja diretamente, seja por intermédio de correspondente bancário, no âmbito das relações de consumo. 2. TESES FIXADAS PARA OS FINS DO ART. 1.040 DO CPC/2015: 2.1 - Abusividade da cláusula que prevê o ressarcimento pelo consumidor da despesa com o registro do pré-gravame, em contratos celebrados a partir de 25/02/2011, data de entrada em vigor da Res.-CMN 3.954/2011, sendo válida a cláusula pactuada no período anterior a essa resolução, ressalvado o controle da onerosidade excessiva . 2.2 - Nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada. 2.3 - A abusividade de encargos acessórios do contrato não descaracteriza a mora. 3. CASO CONCRETO. 3.1. Aplicação da tese 2.1 para declarar válida a cláusula referente ao ressarcimento da despesa com o registro do pré-gravame, condenando-se porém a instituição financeira a restituir o indébito em virtude da ausência de comprovação da efetiva prestação do serviço. 3.2. Aplicação da tese 2.2 para declarar a ocorrência de venda casada no que tange ao seguro de proteção financeira. 3.3. Validade da cláusula de ressarcimento de despesa com registro do contrato, nos termos da tese firmada no julgamento do Tema 958/STJ, tendo havido comprovação da prestação do serviço. 3.4. Ausência de interesse recursal no que tange à despesa com serviços prestados por terceiro. 4. RECURSO ESPECIAL PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, PARCIALMENTE PROVIDO.

### STJ · AREsp 3.047.092/MT
- regras: R13
- posicao: FAV
- tribunal: STJ
- classe_numero: AREsp 3.047.092/MT
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2026-05-25
- publicacao: 2026-05-29
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6797966743
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão recente da Terceira Turma que aplica o Tema 972 ao financiamento de veículo: a assinatura no contrato de adesão não afasta a abusividade, cabendo demonstrar que o consumidor pôde contratar sem o seguro ou escolher outra seguradora; restitui o valor do seguro.
- observacao: Superou as Súmulas 5 e 7 por tratar de revaloração jurídica de fatos incontroversos (seguro de empresa do mesmo conglomerado da financeira, contratação simultânea e eletrônica). Restituição na forma simples. Publicação pela data do Jusbrasil.

ementa:
> DIREITO DO CONSUMIDOR E PROCESSUAL CIVIL. AGRAVO EM RECURSO ESPECIAL. AÇÃO DECLARATÓRIA DE NULIDADE DE CLÁUSULA CONTRATUAL. SEGURO PRESTAMISTA. CONTRATO DE FINANCIAMENTO DE VEÍCULO. VENDA CASADA. TEMA 972/STJ. APLICAÇÃO. SÚMULAS 5 E 7/STJ. AFASTAMENTO. RECURSO ESPECIAL PROVIDO. 1. A controvérsia diz respeito à caracterização de venda casada na contratação de seguro prestamista vinculado a financiamento de veículo, à luz da tese fixada no Tema 972/STJ. 2. Nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada, conforme tese firmada no Tema 972/STJ, cuja incidência não é afastada pela mera assinatura do consumidor no instrumento contratual de adesão. 3. A ausência de demonstração de que ao consumidor foi ofertada a possibilidade de contratar o financiamento sem o seguro, ou de escolher livremente outra seguradora no mercado, configura a abusividade prevista no art. 39, I, do CDC. 4.Não incide a Súmula 7/STJ quando a controvérsia envolve a revaloração jurídica de fatos incontroversos para verificar a correta aplicação de tese fixada em recurso repetitivo. 5. Agravo conhecido para dar provimento ao recurso especial.

### STJ · REsp 2.015.976/PR
- regras: R13
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.015.976/PR
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2025-05-05
- publicacao: 2025-05-09
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6302170087
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Reconhecida a venda casada, os valores do seguro devem ser restituídos ao consumidor; o fato de o seguro ter dado cobertura durante o contrato não convalida a cláusula nula nem afasta a devolução.
- observacao: O tribunal de origem (TJPR) havia reconhecido a venda casada, mas negado a restituição por enriquecimento sem causa; o STJ reformou. Restituição com correção desde o desembolso e juros de mora desde a citação. Publicação pela data do Jusbrasil.

ementa:
> RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO. SEGURO. VENDA CASADA. ABUSIVIDADE. TEMA Nº 972/STJ. NULIDADE. CLÁUSULA. CONVALIDAÇÃO. IMPOSSIBILIDADE. DEVOLUÇÃO. VALOR INDEVIDAMENTE COBRADO. NECESSIDADE. SÚMULA Nº 568/stj. 1. De acordo com o entendimento consolidado no Tema nº 972/STJ, "nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada". 2. Na esteira da jurisprudência sedimentada no STJ, ainda que um ato nulo venha a produzir efeitos, o reconhecimento da sua nulidade os afasta, retroagindo à data em ele foi praticado e impedindo, ainda, que ele seja convalidado. Precedentes. 3. No caso, tendo sido reconhecida concretamente a venda casada, os valores indevidamente cobrados devem ser restituídos ao consumidor. 4. Recurso especial parcialmente conhecido e provido.

### STJ · REsp 2.160.528/SP
- regras: R13
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.160.528/SP
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2025-10-27
- publicacao: 2025-10-30
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6266581109
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Limite da tese: a mera contratação do seguro prestamista não configura, automaticamente, venda casada; é preciso demonstrar que a adesão foi condicionante para a obtenção do financiamento (a inicial deve alegar e provar a compulsão).
- observacao: Recurso não conhecido (Súmulas 5 e 7) porque o tribunal de origem afirmou facultatividade, proposta em apartado e ausência de condicionamento. Linha reiterada em outros acórdãos de 2025-2026 (ver relatório). O REsp 2.101.019/SP citado na pauta é decisão monocrática, não entrou (ver relatório).

ementa:
> RECURSO ESPECIAL. DIREITO DO CONSUMIDOR. AÇÃO REVISIONAL. CONTRATOS DE FINANCIAMENTO E REFINANCIAMENTO PARA AQUISIÇÃO DE VEÍCULO AUTOMOTOR. SEGURO PRESTAMISTA. ALEGAÇÃO DE VENDA CASADA. ART. 39, I, DO CDC. CIRCUNSTÂNCIA NÃO RECONHECIDA PELO TRIBUNAL DE ORIGEM. REVOLVIMENTO DO ACERVO PROBATÓRIO E INTERPRETAÇÃO DE CLÁUSULAS CONTRATUAIS. REVISÃO OBSTADA. SÚMULAS N. 5 E 7/STJ. 1. Nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada (Tema 972/STJ). 2. A mera contratação do seguro prestamista não configura, automaticamente, venda casada, vedada pelo art. 39, I, do CDC. É necessário que se demonstre que tal contratação foi condicionante para a obtenção do financiamento. 3. Hipótese em que o Tribunal de origem consignou que não restou comprovada a ocorrência de venda casada, que o recorrente teve a opção de não contratar o seguro prestamista e que o seguro não foi condicionante para a contratação do financiamento. 4. O acolhimento da pretensão recursal, no sentido de que houve venda casada na contratação de seguro prestamista, demandaria o reexame do acervo fático-probatório e a interpretação de cláusulas contratuais, providência incompatível com a via eleita, ante o óbice das Súmulas n. 5 e 7/STJ. Recurso especial não conhecido.

### TJPR · Recurso Inominado Cível 0002779-20.2025.8.16.0069
- regras: R13
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0002779-20.2025.8.16.0069
- orgao: 2ª Turma Recursal dos Juizados Especiais
- relator: Juiz Tiago Gagliano Pinto Alberto
- julgamento: 2025-12-02
- publicacao: 2025-12-05
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/5381835038
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Seguro prestamista pré-inserido no contrato de financiamento, sem comprovação documental de opção ou de liberdade de escolha da seguradora, é venda casada; a assinatura de documento apartado não prova a escolha quando o seguro já consta do instrumento principal.
- observacao: Julgado de Turma Recursal dos Juizados Especiais (não é Câmara Cível); o TJPR tem vários julgados favoráveis alinhados. A ementa traz o erro material "TEMA 972 STF" (o voto aplica o Tema 972/STJ); copiado como no original. Publicação pela data do Jusbrasil.

ementa:
> RECURSO INOMINADO. AÇÃO DECLARATÓRIA DE INEXISTÊNCIA DE DÉBITO. COBRANÇA DE TARIFAS EM CONTRATO DE FINANCIAMENTO DE VEÍCULO. SENTENÇA DE PARCIAL PROCEDÊNCIA. INSURGÊNCIA RECURSAL DO RÉU. PRELIMINAR IMPUGNAÇÃO AO VALOR DA CAUSA. AFASTADA. MÉRITO. ALEGAÇÃO DE REGULARIDADE DO SEGURO PRESTAMISTA, SEGURO DE ROUBO E FURTO E ASSISTÊNCIA IGS RESIDENCIAL, EM DA LIVRE ESCOLHA DO AUTOR EM OPTAR PELOS SERVIÇOS. SEM RAZÃO. TEMA 972 STF. TARIFAS INCLUÍDAS PREVIAMENTE NO CONTRATO. ABUSIVIDADE. VENDA CASADA. ART. 51, IV, CDC . RECURSO CONHECIDO E NÃO PROVIDO. SENTENÇA MANTIDA. 1. Em contratos de financiamento, a contratação de seguro prestamista só é válida se o consumidor puder escolher livremente a seguradora. Quando o contrato prevê automaticamente a inclusão do seguro ofertado pela instituição financeira, sem comprovação documental de opção ou liberdade de escolha, configura-se prática abusiva e venda casada, vedada pelo art. 39, I, do Código de Defesa do Consumidor . Aplicação direta da tese 2.2 do Tema 972 /STJ, segundo a qual o consumidor não pode ser compelido a contratar seguro com a própria instituição ou seguradora por ela indicada. 2. No caso concreto, não se vislumbra que o autor tenha tido opção real na contratação dos serviços de assistência e seguros, os quais foram impostos unilateralmente pelo réu, sem margem de escolha, o que caracteriza hipótese de venda casada e torna ilegítima a cobrança, nos termos do art. 51, IV, do CDC . 3. Precedentes desta C. Segunda Turma Recursal 0001942- 10.2023.8.16.0109; 0000834-32.2025.8.16.0090; 0007373- 14.2024.8.16.0069 .4. Recurso conhecido e não provido.

### TJPR · Recurso Inominado Cível 0000868-54.2025.8.16.0139
- regras: R13, R26
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0000868-54.2025.8.16.0139
- orgao: 2ª Turma Recursal dos Juizados Especiais
- relator: Juíza Vanessa de Souza Camargo
- julgamento: 2026-05-19
- publicacao: 2026-05-20
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/6194787080
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Venda casada reconhecida mesmo com a opção "SIM" assinalada no contrato (seguro previamente indicado e incorporado ao valor financiado, seguradora do mesmo grupo, propostas firmadas no mesmo dia); restituição em dobro das cobranças posteriores a 30/03/2021 por força do EAREsp 676.608/RS.
- observacao: Julgado de Turma Recursal dos Juizados Especiais. O marco de 30/03/2021 e a restituição em dobro estão no voto, não no texto da ementa. Publicação pela data do Jusbrasil.

ementa:
> RECURSOS INOMINADOS. DIREITO BANCÁRIO E DO CONSUMIDOR. CONTRATO DE FINANCIAMENTO DE VEÍCULO. TARIFA DE AVALIAÇÃO DO BEM. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO. COBRANÇA INDEVIDA. TARIFA DE REGISTRO DE CONTRATO. SERVIÇO COMPROVADAMENTE PRESTADO. COBRANÇA LEGÍTIMA. SEGURO PRESTAMISTA E SEGURO DE ACIDENTES PESSOAIS. CONTRATAÇÃO SEM OPÇÃO REAL DO CONSUMIDOR. CONFIGURAÇÃO DE VENDA CASADA. RESTITUIÇÃO EM DOBRO DOS VALORES. JUROS MORATÓRIOS. LIMITAÇÃO A 1% AO MÊS. SÚMULA 379 DO STJ. SENTENÇA PARCIALMENTE REFORMADA. RECURSO DA AUTORA CONHECIDO E PARCIALMENTE PROVIDO. RECURSO DA RÉ CONHECIDO E DESPROVIDO.

## R15 — Juros remuneratórios abusivos — taxa muito acima da média de mercado do BACEN

Tese: Em contrato de consumo, os juros remuneratórios são abusivos (CDC, art. 51, § 1º) quando a taxa contratada supera expressivamente a taxa média de mercado do BACEN para a mesma espécie de operação e o banco não justifica a diferença com circunstâncias concretas; a taxa deve ser revista para a média.

### STJ · REsp 1.061.530/RS
- regras: R15
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.061.530/RS
- orgao: Segunda Seção
- relator: Min. Nancy Andrighi
- julgamento: 2008-10-22
- publicacao: 2009-03-10
- precedente_qualificado: Temas 24, 25, 26, 27 e 28/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106329912
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Prova que o STJ admite a revisão das taxas de juros remuneratórios em contrato de consumo quando a abusividade, capaz de colocar o consumidor em desvantagem exagerada (CDC, art. 51, § 1º), fica cabalmente demonstrada no caso concreto (Tema 27), e que a abusividade dos encargos da normalidade descaracteriza a mora (Tema 28).
- observacao: LIMITE, a constar como ressalva na peça: o mesmo repetitivo fixa que as instituições financeiras não se sujeitam à Lei de Usura (Súmula 596/STF; Tema 24) e que juros acima de 12% ao ano, por si só, não indicam abusividade (Tema 25; mesmo teor da Súmula 382/STJ). No caso concreto o STJ manteve a taxa contratada. A proposta da relatora de teto de 2x a taxa média ficou vencida: a média é referencial, não limite (ver a entrada ADV REsp 2.009.614/SC). Os textos das Súmulas 382/STJ e 596/STF foram conferidos nos votos abertos, não como documento autônomo. Tema 1378/STJ pendente (ver Relatório). Publicação pela data do Jusbrasil.

ementa:
> DIREITO PROCESSUAL CIVIL E BANCÁRIO. RECURSO ESPECIAL. AÇÃO REVISIONAL DE CLÁUSULAS DE CONTRATO BANCÁRIO. INCIDENTE DE PROCESSO REPETITIVO. JUROS REMUNERATÓRIOS. CONFIGURAÇÃO DA MORA. JUROS MORATÓRIOS. INSCRIÇÃO/MANUTENÇÃO EM CADASTRO DE INADIMPLENTES. DISPOSIÇÕES DE OFÍCIO. DELIMITAÇÃO DO JULGAMENTO Constatada a multiplicidade de recursos com fundamento em idêntica questão de direito, foi instaurado o incidente de processo repetitivo referente aos contratos bancários subordinados ao Código de Defesa do Consumidor, nos termos da ADI n.º 2.591-1. Exceto: cédulas de crédito rural, industrial, bancária e comercial; contratos celebrados por cooperativas de crédito; contratos regidos pelo Sistema Financeiro de Habitação, bem como os de crédito consignado. Para os efeitos do § 7º do art. 543-C do CPC, a questão de direito idêntica, além de estar selecionada na decisão que instaurou o incidente de processo repetitivo, deve ter sido expressamente debatida no acórdão recorrido e nas razões do recurso especial, preenchendo todos os requisitos de admissibilidade. Neste julgamento, os requisitos específicos do incidente foram verificados quanto às seguintes questões: i) juros remuneratórios; ii) configuração da mora; iii) juros moratórios; iv) inscrição/manutenção em cadastro de inadimplentes e v) disposições de ofício. PRELIMINAR O Parecer do MPF opinou pela suspensão do recurso até o julgamento definitivo da ADI 2.316/DF. Preliminar rejeitada ante a presunção de constitucionalidade do art. 5º da MP n.º 1.963-17/00, reeditada sob o n.º 2.170-36/01. I - JULGAMENTO DAS QUESTÕES IDÊNTICAS QUE CARACTERIZAM A MULTIPLICIDADE. ORIENTAÇÃO 1 - JUROS REMUNERATÓRIOS a) As instituições financeiras não se sujeitam à limitação dos juros remuneratórios estipulada na Lei de Usura (Decreto 22.626/33), Súmula 596/STF; b) A estipulação de juros remuneratórios superiores a 12% ao ano, por si só, não indica abusividade; c) São inaplicáveis aos juros remuneratórios dos contratos de mútuo bancário as disposições do art. 591 c/c o art. 406 do CC/02; d) É admitida a revisão das taxas de juros remuneratórios em situações excepcionais, desde que caracterizada a relação de consumo e que a abusividade (capaz de colocar o consumidor em desvantagem exagerada - art. 51, § 1º, do CDC) fique cabalmente demonstrada, ante às peculiaridades do julgamento em concreto. ORIENTAÇÃO 2 - CONFIGURAÇÃO DA MORA a) O reconhecimento da abusividade nos encargos exigidos no período da normalidade contratual (juros remuneratórios e capitalização) descarateriza a mora; b) Não descaracteriza a mora o ajuizamento isolado de ação revisional, nem mesmo quando o reconhecimento de abusividade incidir sobre os encargos inerentes ao período de inadimplência contratual. ORIENTAÇÃO 3 - JUROS MORATÓRIOS Nos contratos bancários, não-regidos por legislação específica, os juros moratórios poderão ser convencionados até o limite de 1% ao mês. ORIENTAÇÃO 4 - INSCRIÇÃO/MANUTENÇÃO EM CADASTRO DE INADIMPLENTES a) A abstenção da inscrição/manutenção em cadastro de inadimplentes, requerida em antecipação de tutela e/ou medida cautelar, somente será deferida se, cumulativamente: i) a ação for fundada em questionamento integral ou parcial do débito; ii) houver demonstração de que a cobrança indevida se funda na aparência do bom direito e em jurisprudência consolidada do STF ou STJ; iii) houver depósito da parcela incontroversa ou for prestada a caução fixada conforme o prudente arbítrio do juiz; b) A inscrição/manutenção do nome do devedor em cadastro de inadimplentes decidida na sentença ou no acórdão observará o que for decidido no mérito do processo. Caracterizada a mora, correta a inscrição/manutenção. ORIENTAÇÃO 5 - DISPOSIÇÕES DE OFÍCIO É vedado aos juízes de primeiro e segundo graus de jurisdição julgar, com fundamento no art. 51 do CDC, sem pedido expresso, a abusividade de cláusulas nos contratos bancários. Vencidos quanto a esta matéria a Min. Relatora e o Min. Luis Felipe Salomão. II- JULGAMENTO DO RECURSO REPRESENTATIVO (REsp 1.061.530/RS) A menção a artigo de lei, sem a demonstração das razões de inconformidade, impõe o não-conhecimento do recurso especial, em razão da sua deficiente fundamentação. Incidência da Súmula 284/STF. O recurso especial não constitui via adequada para o exame de temas constitucionais, sob pena de usurpação da competência do STF. Devem ser decotadas as disposições de ofício realizadas pelo acórdão recorrido. Os juros remuneratórios contratados encontram-se no limite que esta Corte tem considerado razoável e, sob a ótica do Direito do Consumidor, não merecem ser revistos, porquanto não demonstrada a onerosidade excessiva na hipótese. Verificada a cobrança de encargo abusivo no período da normalidade contratual, resta descaracterizada a mora do devedor. Afastada a mora: i) é ilegal o envio de dados do consumidor para quaisquer cadastros de inadimplência; ii) deve o consumidor permanecer na posse do bem alienado fiduciariamente e iii) não se admite o protesto do título representativo da dívida. Não há qualquer vedação legal à efetivação de depósitos parciais, segundo o que a parte entende devido. Não se conhece do recurso quanto à comissão de permanência, pois deficiente o fundamento no tocante à alínea a do permissivo constitucional e também pelo fato de o dissídio jurisprudencial não ter sido comprovado, mediante a realização do cotejo entre os julgados tidos como divergentes. Vencidos quanto ao conhecimento do recurso a Min. Relatora e o Min. Carlos Fernando Mathias. Recurso especial parcialmente conhecido e, nesta parte, provido, para declarar a legalidade da cobrança dos juros remuneratórios, como pactuados, e ainda decotar do julgamento as disposições de ofício. Ônus sucumbenciais redistribuídos.

### STJ · REsp 2.199.537/RS
- regras: R15
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.199.537/RS
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2025-04-07
- publicacao: 2025-04-10
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6580726886
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Prova que o STJ chancela a limitação à taxa média quando a abusividade é fundamentada em circunstâncias concretas (taxa de 2 a 3 vezes a média em crédito de risco reduzido, banco que não comprova custo de captação, spread e risco de crédito), e não só na comparação aritmética com a média.
- observacao: O recurso do banco foi desprovido com apoio nas Súmulas 5, 7 e 83/STJ: o STJ não reexaminou os fatos, mas afirmou que a decisão de origem estava de acordo com sua jurisprudência por não se limitar ao cotejo com a média. A peça deve, por isso, narrar as peculiaridades concretas e imputar ao banco o ônus de justificar a taxa. Tema 1378/STJ pendente. Publicação pela data do Jusbrasil. Faltou julgado de TJ em R15 (ver Relatório).

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. REVISÃO DE CONTRATO BANCÁRIO. JUROS REMUNERATÓRIOS. ABUSIVIDADE. RECURSO DESPROVIDO. I. CASO EM EXAME 1. Recurso especial interposto contra acórdão do Tribunal de Justiça do Estado do Rio Grande do Sul que, em ação revisional de contrato de financiamento bancário, limitou os juros remuneratórios à taxa média de mercado divulgada pelo Bacen por considerar abusiva a taxa pactuada. II. QUESTÃO EM DISCUSSÃO 2. Há duas questões em discussão: (i) saber se a limitação dos juros remuneratórios à taxa média de mercado divulgada pelo Bacen, sem análise das peculiaridades do caso concreto, é válida; e (ii) saber se houve negativa de prestação jurisdicional e se cabe a análise da divergência jurisprudencial sobre a abusividade dos juros remuneratórios. III. RAZÕES DE DECIDIR 3. A Corte de origem analisou, de forma clara e objetiva, as questões que delimitam a controvérsia, afastando a alegada negativa de prestação jurisdicional. 4. A jurisprudência do STJ estabelece que a revisão das taxas de juros remuneratórios deve considerar a relação de consumo e a demonstração cabal de abusividade, não se limitando à comparação com a taxa média de mercado. 5. No caso concreto, a Corte de origem concluiu pela abusividade dos juros remuneratórios, considerando a falta de justificativa específica pela instituição financeira para a taxa praticada, adotando a jurisprudência do STJ. 6. A incidência das Súmulas n. 5, 7 e 83 do STJ impede o conhecimento do recurso especial pela divergência jurisprudencial sobre a mesma questão. IV. DISPOSITIVO E TESE 7. Recurso especial desprovido. Tese de julgamento: "1. A revisão das taxas de juros remuneratórios deve considerar a relação de consumo e a demonstração cabal de abusividade, não se limitando à comparação com a taxa média de mercado. 2. A negativa de prestação jurisdicional não se configura quando a corte de origem analisa, de forma clara e objetiva, as questões que delimitam a controvérsia". Dispositivos relevantes citados: CPC/2015, arts. 489, § 1º, III, IV e VI, e 1.022, parágrafo único, I e II; CC/2002, arts. 591 e 406; CDC, art. 51, § 1º. Jurisprudência relevante citada: STJ, REsp n. 1.061.530/RS, relatora Ministra Nancy Andrighi, Segunda Seção, julgado em 22/10/2008; STJ, AgInt no AREsp n. 2.007.281/PR, relatora Ministra Maria Isabel Gallotti, Quarta Turma, julgado em 12/9/2022; STJ, REsp n. 2.009.614/SC, relatora Ministra Nancy Andrighi, Terceira Turma, julgado em 27/9/2022.

### STJ · REsp 2.009.614/SC
- regras: R15
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.009.614/SC
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2022-09-27
- publicacao: 2022-09-30
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1660009005
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Fixa o LIMITE a antecipar na peça: o simples cotejo entre a taxa contratada e a média do BACEN, ou a aplicação de percentual aprioristicamente adotado pelo tribunal estadual (1,5x, 2x, 3x), não basta para reconhecer a abusividade; exige-se demonstração cabal das peculiaridades do caso (economia à época, custo de captação, risco, relacionamento com o banco, garantias).
- observacao: O STJ deu parcial provimento ao recurso do banco e devolveu os autos à origem. A ação foi ajuizada por pessoa jurídica e o acórdão também registra que a aplicabilidade do CDC é requisito para a revisão. Este é o parâmetro hoje aplicado pelas Turmas e é o ponto submetido ao Tema 1378/STJ. Os percentuais de 1,5x a 2x a média, citados na tese da inicial, são só referência histórica da jurisprudência, não critério adotado pelo STJ (ver ementa, item 5).

ementa:
> RECURSO ESPECIAL. CONTRATO DE MÚTUO BANCÁRIO. JUROS REMUNERATÓRIOS. REVISÃO. CARÁTER ABUSIVO. REQUISITOS. NECESSIDADE DE FUNDAMENTAÇÃO ADEQUADA. 1- Recurso especial interposto em 19/4/2022 e concluso ao gabinete em 4/7/2022. 2- O propósito recursal consiste em dizer se: a) a menção genérica às "circunstâncias da causa" não descritas na decisão, acompanhada ou não do simples cotejo entre a taxa de juros prevista no contrato e a média praticada no mercado, é suficiente para a revisão das taxas de juros remuneratórios pactuadas em contratos de mútuo bancário; e b) qual o incide a ser aplicado, na espécie, aos juros de mora. 3- A Segunda Seção, no julgamento REsp n. 1.061.530/RS, submetido ao rito dos recursos especiais repetitivos, fixou o entendimento de que "é admitida a revisão das taxas de juros remuneratórios em situações excepcionais, desde que caracterizada a relação de consumo e que a abusividade (capaz de colocar o consumidor em desvantagem exagerada - art. 51, § 1º, do CDC) fique cabalmente demonstrada, ante as peculiaridades do julgamento em concreto." 4- Deve-se observar os seguintes requisitos para a revisão das taxas de juros remuneratórios: a) a caracterização de relação de consumo; b) a presença de abusividade capaz de colocar o consumidor em desvantagem exagerada; e c) a demonstração cabal, com menção expressa às peculiaridades da hipótese concreta, da abusividade verificada, levando-se em consideração, entre outros fatores, a situação da economia na época da contratação, o custo da captação dos recursos, o risco envolvido na operação, o relacionamento mantido com o banco e as garantias ofertadas. 5- São insuficientes para fundamentar o caráter abusivo dos juros remuneratórios: a) a menção genérica às "circunstâncias da causa" - ou outra expressão equivalente; b) o simples cotejo entre a taxa de juros prevista no contrato e a média de mercado divulgada pelo BACEN e c) a aplicação de algum limite adotado, aprioristicamente, pelo próprio Tribunal estadual. 6- Na espécie, não se extrai do acórdão impugnado qualquer consideração acerca das peculiaridades da hipótese concreta, limitando-se a cotejar as taxas de juros pactuadas com as correspondentes taxas médias de mercado divulgadas pelo BACEN e a aplicar parâmetro abstrato para aferição do caráter abusivo dos juros, impondo-se, desse modo, o retorno dos autos às instâncias ordinárias para que aplique o direito à espécie a partir dos parâmetros delineados pela jurisprudência desta Corte Superior. 7- Recurso especial parcialmente provido.

### TJPR · Apelação Cível 0001169-30.2025.8.16.0194
- regras: R15, R26
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001169-30.2025.8.16.0194
- orgao: 14ª Câmara Cível
- relator: Des. Francisco Eduardo Gonzaga de Oliveira
- julgamento: 2026-04-13
- publicacao: 2026-04-14
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035688741/Ac%C3%B3rd%C3%A3o-0001169-30.2025.8.16.0194
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O TJPR limita à taxa média do BACEN os juros de empréstimo pessoal não consignado que superam em mais de duas vezes a média sem justificativa ligada ao perfil do consumidor, e manda devolver em dobro os pagamentos posteriores à modulação do EAREsp 676.608/RS.
- observacao: Apelação do banco desprovida. O critério do caso é o múltiplo da média (mais de duas vezes) somado à falta de justificativa concreta; a peça deve trazer a comparação com a série BACEN da mesma espécie e data. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E DO CONSUMIDOR. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. EMPRÉSTIMO PESSOAL NÃO CONSIGNADO. CÉDULA DE CRÉDITO BANCÁRIO. JUROS REMUNERATÓRIOS ABUSIVOS. REPETIÇÃO DE INDÉBITO EM DOBRO. RECURSO NÃO PROVIDO. I. CASO EM EXAME 1. Apelação Cível interposta por instituição financeira contra sentença que julgou procedente ação revisional de contrato bancário com pedido de repetição de indébito. A sentença determinou o recálculo da dívida com base na taxa média de mercado vigente à época da contratação, com devolução em dobro dos valores pagos indevidamente e fixação de honorários advocatícios sobre o valor da condenação.II. QUESTÃO EM DISCUSSÃO 2. Há duas questões em discussão: (i) definir se a taxa de juros remuneratórios contratada é abusiva, justificando sua limitação à taxa média de mercado; (ii) estabelecer se é devida a repetição do indébito em dobro nos moldes do art. 42, parágrafo único, do CDC, independentemente da comprovação de má-fé.III. RAZÕES DE DECIDIR 3.1. As instituições financeiras não estão sujeitas à limitação de juros da Lei de Usura, mas a cobrança de taxa manifestamente superior à média de mercado pode ser considerada abusiva quando não justificada por circunstâncias específicas do contrato.3.2. O Superior Tribunal de Justiça fixou entendimento de que a taxa média de mercado, divulgada pelo Banco Central, é parâmetro idôneo para aferição da abusividade dos juros, a ser analisada conforme as peculiaridades do caso concreto.3.3. As taxas de juros pactuadas ultrapassam em mais de duas vezes as taxas médias de mercado divulgadas pelo BACEN, revelando desequilíbrio contratual e abusividade, sobretudo diante da ausência de justificativa concreta relacionada ao perfil do consumidor. 3.4. A jurisprudência admite a limitação dos juros remuneratórios à taxa média de mercado quando houver evidente discrepância sem justificativa individualizada, conforme o REsp 1.061.530/RS (tema repetitivo) e decisões mais recentes do STJ. 3.5 A repetição em dobro dos valores pagos indevidamente é cabível quando demonstrada conduta contrária à boa-fé objetiva, sendo desnecessária a prova de má-fé, conforme entendimento consolidado pelo Superior Tribunal de Justiça. No caso, como os pagamentos indevidos ocorreram após a modulação dos efeitos da tese fixada em embargos de divergência, é aplicável a devolução em dobro independentemente de dolo.IV. DISPOSITIVO 4. Recurso conhecido e não provido.Dispositivos relevantes citados: CF/1988, art. 5º, XXXII; CDC, arts. 6º, V, 42, parágrafo único, e 51, §1º; CPC, arts. 85, §§ 2º e 11.Jurisprudência relevante citada: STJ, REsp 1.061.530/RS, Rel. Min. Nancy Andrighi, 2ª Seção, j. 25.11.2009; STJ, EAREsp 600.663/RS, Rel. Min. Maria Thereza de Assis Moura, Rel. p/ Acórdão Min. Herman Benjamin, Corte Especial, j. 21.10.2020, DJe 30.03.2021; STJ, AgInt no REsp 2.021.348/PR, Rel. Min. Maria Isabel Gallotti, 4ª T., j. 04.09.2023; TJPR, AC 0068456-36.2023.8.16.0014; TJPR, AC 0010026-82.2023.8.16.0017; TJPR, AC 0000514-68.2022.8.16.0160.

### TJPR · Apelação Cível 0010452-40.2025.8.16.0174
- regras: R15
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0010452-40.2025.8.16.0174
- orgao: 16ª Câmara Cível
- relator: Juiz Subst. 2º Grau Guilherme Frederico Hernandes Denz
- julgamento: 2026-06-22
- publicacao: 2026-06-22
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035381711/Ac%C3%B3rd%C3%A3o-0010452-40.2025.8.16.0174
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O TJPR mantém a limitação dos juros de empréstimo pessoal à taxa média do BACEN diante de discrepância significativa para a mesma espécie e período, com restituição do pago a maior e afastamento da mora.
- observacao: A taxa média é tratada como vetor relevante, não critério absoluto: a peça precisa mostrar a discrepância concreta. Repetição conforme a modulação do EAREsp 676.608/RS. Fonte: portal de jurisprudência do TJPR (comarca de União da Vitória).

ementa:
> DIREITO CIVIL E BANCÁRIO. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO DE EMPRÉSTIMO PESSOAL. JUROS REMUNERATÓRIOS. TAXA SUPERIOR À MÉDIA DE MERCADO. REPETIÇÃO DO INDÉBITO. RECURSO DESPROVIDO.I. CASO EM EXAME1. Apelação cível interposta contra sentença que julgou procedente ação revisional de contrato de empréstimo pessoal, reconhecendo a abusividade da taxa de juros remuneratórios pactuada, determinando sua limitação à taxa média de mercado divulgada pelo Banco Central do Brasil, bem como a restituição dos valores pagos a maior, afastando-se, ainda, os encargos moratórios.II. QUESTÃO EM DISCUSSÃO2. A questão em discussão consiste em: (i) saber se a simples estipulação de juros remuneratórios superiores à taxa média de mercado autoriza, no caso concreto, a revisão judicial das cláusulas contratuais; (ii) saber se é cabível a restituição dos valores pagos a maior, inclusive em dobro, diante do reconhecimento da abusividade; e (iii) saber se o reconhecimento da abusividade no período de normalidade contratual afasta a caracterização da mora do devedor.III. RAZÕES DE DECIDIR3. Embora as instituições financeiras não se submetam à limitação da Lei de Usura, admite-se a revisão dos juros remuneratórios em situações excepcionais, quando demonstrada abusividade capaz de colocar o consumidor em desvantagem exagerada, considerada a taxa média de mercado como relevante vetor de aferição, sem que se trate de critério absoluto.4. Constatada, no caso concreto, a discrepância significativa entre a taxa pactuada e a média de mercado para operações da mesma espécie e período, impõe-se a limitação dos juros remuneratórios aos parâmetros divulgados pelo Banco Central do Brasil.5. Reconhecida a abusividade no período de normalidade contratual, é devida a restituição dos valores pagos indevidamente, observada a modulação dos efeitos fixada pelo Superior Tribunal de Justiça quanto à aplicação da repetição em dobro, bem como o afastamento dos encargos moratórios.IV. DISPOSITIVO E TESE6. Recurso desprovido.Tese de julgamento:“1. A taxa média de mercado divulgada pelo Banco Central do Brasil constitui importante parâmetro para a aferição da abusividade dos juros remuneratórios, devendo ser analisadas as peculiaridades do caso concreto.”“2. Reconhecida a abusividade dos juros no período de normalidade contratual, é cabível a restituição dos valores pagos a maior, bem como o afastamento da mora do devedor.”Dispositivos relevantes citados:Código de Defesa do Consumidor, art. 42, parágrafo único.Código de Processo Civil, art. 487, I; art. 85, § 11.Jurisprudência relevante citada:STJ, Recurso Especial nº 1.061.530/RS, Rel. Ministra Nancy Andrighi, Segunda Seção, j. 22.10.2008.STJ, Agravo Interno no AREsp nº 2.150.980/RS, Rel. Ministra Nancy Andrighi, Terceira Turma, j. 09.11.2022.STJ, EAREsp nº 676.608/RS, Rel. Ministro Og Fernandes, Corte Especial, j. 21.10.2020.

## R17 — Cédulas comercial e industrial (e rural): juros limitados a 12% a.a. sem taxa fixada pelo CMN

Tese: Nas cédulas de crédito comercial e industrial (e rural), regidas por regramento próprio (DL 167/1967, DL 413/1969, Lei 6.840/1980), compete ao CMN fixar os juros; na omissão do CMN, os juros remuneratórios limitam-se a 12% a.a. (Decreto 22.626/1933), sem incidir a Súmula 596/STF, e o excedente é nulo.

### STJ · REsp 1.940.292/PR
- regras: R17
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.940.292/PR
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2022-05-03
- publicacao: 2022-05-27
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2107817550
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Precedente mais citado e mais recente da Terceira Turma: as cédulas rural, industrial e comercial têm regramento próprio e, na omissão do CMN, o teto é de 12% a.a., mesmo diante da liberdade de pactuação do MCR 6-3 (rural, recursos não controlados).
- observacao: O REsp existe e confere com a indicação (Terceira Turma, DJe 27/05/2022, que o texto do REsp 1.978.445 também cita). O caso concreto era de cédula de crédito RURAL; a extensão às cédulas comercial e industrial está no item 4 da ementa ("jurisprudência pacífica desta Corte") e na identidade do regime legal, não no objeto do julgamento. Maioria de 3 a 2 (vencidos os Mins. Ricardo Villas Bôas Cueva e Marco Aurélio Bellizze). O voto-vista vencido, do Min. Villas Bôas Cueva, entendeu que a livre pactuação prevista no MCR 6-3 (crédito rural com recursos não controlados) já cumpre o dever do CMN, de modo que não incidiria o teto; o MCR é norma de crédito rural, e o voto vencido não trata de cédula comercial ou industrial. A cédula rural tem onda própria.

ementa:
> CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. EMBARGOS À EXECUÇÃO. EMBARGOS DE DECLARAÇÃO. OMISSÃO, CONTRADIÇÃO, OBSCURIDADE OU ERRO DO ACÓRDÃO EMBARGADO. AUSÊNCIA. VIOLAÇÃO DO ART. 489, § 1º, DO CPC/2015 . NÃO OCORRÊNCIA. CÉDULA DE CRÉDITO RURAL. LIMITAÇÃO DOS JUROS REMUNERATÓRIOS. MANUAL DE CRÉDITO RURAL. OMISSÃO DO CONSELHO MONETÁRIO NACIONAL. OCORRÊNCIA. DECRETO Nº 22.626/1933. INCIDÊNCIA.
> 1. Embargos à execução opostos em 30/10/2018, dos quais foi extraído o presente recurso especial, interposto em 22/05/2020 e concluso ao gabinete em 30/04/2021.
> 2. O propósito recursal é decidir se, na hipótese de cédula de crédito rural, as taxas de juros remuneratórios devem obedecer ao limite de 12% ao ano, previsto no Decreto nº 22.626/1933, mesmo após a edição da Resolução nº 4.234/2013 do Conselho Monetário Nacional.
> 3. Não há ofensa aos arts. 489 e 1.022 do CPC/2015 quando o Tribunal de origem examina de forma fundamentada, a questão submetida à apreciação judicial na medida necessária para o deslinde da controvérsia, ainda que em sentido contrário à pretensão da parte. Precedentes.
> 4. Conforme a jurisprudência pacífica desta Corte, as cédulas de crédito rural, industrial e comercial se submetem a regramento próprio, que confere ao Conselho Monetário Nacional o dever de fixar os juros a serem praticados. Não havendo atuação do referido órgão, adota-se a limitação de 12% ao ano prevista no Decreto nº 22.626/1933. Precedentes.
> 5. O art. 5º do Decreto-Lei nº 167/1967, ao determinar que as taxas de juros remuneratórios devem obedecer ao limite fixado pelo CMN, sem ressalvas quanto à possibilidade de livre pactuação, tem por objetivo evitar a fixação de taxas abusivas por parte das instituições financeiras e, simultaneamente, permitir certa flexibilidade, uma vez que o limite pode ser constantemente alterado pelo CMN.
> 6. O CMN, por meio do item 1 do MCR 6-3, autorizou que as partes, em cédulas de crédito rural com recursos não controlados, pactuem livremente as taxas de juros, mas permaneceu omisso quanto à fixação de um limite, como determina o art. 5º do Decreto-Lei nº 167/1967, de modo que, não havendo limite estabelecido pelo CMN, as taxas acordadas entre as partes não podem ultrapassar o limite de 12% ao ano previsto no Decreto nº 22.626/1933.
> 7. Recurso especial conhecido e não provido.

### STJ · REsp 1.964.227/DF
- regras: R17
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.964.227/DF
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva (p/ acórdão Min. Moura Ribeiro)
- julgamento: 2022-09-27
- publicacao: 2022-09-30
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1660004982
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Julgado específico de nota/cédula de crédito COMERCIAL: o regime da Lei 6.840/1980 e do DL 413/1969 entrega ao CMN a fixação dos juros e, na falta dela, vale o teto de 12% a.a. da Lei de Usura; a cláusula acima do teto é nula de pleno direito (art. 11 do Decreto 22.626/1933) e a nulidade não convalesce com o tempo.
- observacao: Maioria de 3 a 1. O relator originário, Min. Villas Bôas Cueva, também reconhecia a nulidade da taxa acima de 12%, mas julgava prescrita a pretensão revisional; a divergência vencedora (Min. Moura Ribeiro) afastou a prescrição por se tratar de nulidade, razão pela qual a Turma negou provimento ao recurso do banco. O julgado trata de nota de crédito comercial. Publicação pela data do Jusbrasil. A ementa traz a grafia "Decerto" no item 3, copiada como está no texto do fetch.

ementa:
> CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL INTERPOSTO SOB A ÉGIDE DO NCPC . AÇÃO DECLARATÓRIA DE NULIDADE. NOTA DE CRÉDITO COMERCIAL. TAXA DE JUROS. LEI DE USURA . APLICABILIDADE. LIMITAÇÃO A 1% AO MÊS. RECURSO NÃO PROVIDO.
> 1. Aplica-se o NCPC a este recurso ante os termos do Enunciado Administrativo nº 3, aprovado pelo Plenário do STJ na sessão de 9/3/2016: Aos recursos interpostos com fundamento no CPC/2015 (relativos a decisões publicadas a partir de 18 de março de 2016) serão exigidos os requisitos de admissibilidade recursal na forma do novo CPC .
> 2. O negócio jurídico nulo não é suscetível de confirmação, nem convalesce pelo decurso do tempo. Ou seja, não decai, não caduca.
> 3. O art. 11 do Decerto nº 22.626/33 estipula que o contrato celebrado com infração desta lei é nulo de pleno direito, mormente quanto aos excessivos juros remuneratórios.
> 4. A Nota de Crédito Comercial objeto da demanda tem sua regulamentação prevista na Lei n. 6.840/1980 e Decreto-Lei n. 413/1969, conferindo ao Conselho Monetário Nacional a competência para a fixação dos juros a serem praticados. Na falta dessa estipulação, deve ser observada a limitação imposta na Lei de Usura, que veda a cobrança de juros em percentual superior a 12% ao ano, como verificado.
> 5. Recurso especial não provido.

### STJ · AgRg no REsp 784.935/CE
- regras: R17
- posicao: FAV
- tribunal: STJ
- classe_numero: AgRg no REsp 784.935/CE
- orgao: Quarta Turma
- relator: Min. Honildo Amaral de Mello Castro (Desembargador convocado do TJ/AP)
- julgamento: 2010-03-02
- publicacao: 2010-03-22
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/8562232
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Julgado específico de cédula de crédito INDUSTRIAL: na ausência de deliberação do CMN, os juros ficam sujeitos ao teto de 12% a.a., e a comissão de permanência não é admitida em caso de inadimplência.
- observacao: Unânime. Acórdão antigo (2010), escolhido porque é o que trata expressamente da cédula industrial; a tese segue reafirmada pelo STJ em julgados recentes sobre cédulas rurais, como o REsp 1.940.292/PR (2022), e a decisão citada no voto fixa que a cédula industrial tem, quanto aos juros, a mesma disciplina da rural (art. 5º da Lei 6.840/1980 c/c art. 5º do DL 413/1969). No fetch, a ementa grafa "AÇAO", "LIMITAÇAO" e "COMISSAO" sem cedilha ou til; aqui, corrigidos.

ementa:
> AGRAVO REGIMENTAL. RECURSO ESPECIAL. AÇÃO REVISIONAL. CÉDULA DE CRÉDITO INDUSTRIAL. JUROS REMUNERATÓRIOS. LIMITAÇÃO. POSSIBILIDADE. COMISSÃO DE PERMANÊNCIA. COBRANÇA. INADMISSIBILIDADE.
> 1. Segundo reiterada jurisprudência desta Corte, por ausência de deliberação do Conselho Monetário Nacional, a taxa de juros remuneratórios deve ficar sujeita ao limite de 12% ao ano, no caso de cédulas de crédito rural, industrial e comercial.
> 2. Nos casos de cédula de crédito rural, comercial e industrial, esta Corte não admite a cobrança de comissão de permanência em caso de inadimplência.
> 3. Agravo regimental a que se nega provimento.

### STJ · REsp 1.978.445/RS
- regras: R17
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.978.445/RS
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2022-10-25
- publicacao: 2022-10-28
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1674970359
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Limite da tese (ressalva obrigatória): o teto de 12% a.a. vale para as cédulas rural, industrial e comercial; na cédula de crédito BANCÁRIO (Lei 10.931/2004) não há esse teto, e o STJ examina a abusividade caso a caso, comparando com a taxa média de mercado do BACEN (REsp 1.061.530/RS), de modo que a mera aplicação do CDI não é abusiva.
- observacao: Maioria de 3 a 1 (vencido o Min. Moura Ribeiro). É o julgado que distingue os dois regimes: a ementa trata o 12% como regra das cédulas rural, industrial e comercial (itens 7 a 9) e, ao mesmo tempo, o repetitivo de juros (REsp 1.061.530/RS) como aplicável à cédula bancária. A petição deve identificar o título pela sua natureza (a "cédula de crédito bancário" não se confunde com a comercial ou industrial) antes de pedir o teto. Publicação pela data do Jusbrasil. A ementa foi copiada sem o cabeçalho de página "Superior Tribunal de Justiça" que o texto do fetch intercala no meio do item 8.

ementa:
> PROCESSUAL CIVIL. RECURSO ESPECIAL. EMBARGOS A EXECUÇÃO. ENCARGOS. CDI. CÉDULA DE CRÉDITO BANCÁRIO. CÉDULA DE CRÉDITO RURAL. ABUSIVIDADE. INOCORRÊNCIA.
> 1. Ação de embargos à execução.
> 2. Recurso especial interposto em: 06/07/2021. Concluso ao gabinete em: 20/01/2022.
> 3. O propósito recursal consiste em perquirir se é abusiva a aplicação dos Certificados de Depósito Interfinanceiro (CDI) como encargo de cédula de crédito bancário e de cédula de crédito rural, tendo em vista a disposição da Súmula nº 176 do STJ.
> 4. O art. 122 do Código Civil determina que são lícitas, em geral, todas as condições não contrárias à lei, à ordem pública ou aos bons costumes; entre as condições defesas se incluem as que privarem de todo efeito o negócio jurídico, ou o sujeitarem ao puro arbítrio de uma das partes.
> 5. É firme a jurisprudência deste STJ no sentido de que eventual abusividade deve ser verificada casuisticamente, em função do percentual fixado pela instituição financeira. Precedentes.
> 6. Em se tratando de cédula de crédito bancário, tem sido firme este STJ no sentido de que não há vedação à adoção da variação dos Certificados de Depósitos Interbancários - CDI como encargo financeiro em contratos bancários, devendo o abuso ser observado na hipótese, em cotejo com as taxas médias de mercado regularmente divulgadas pelo Banco Central do Brasil para as operações de mesma espécie.
> 7. As cédulas de crédito rural, industrial e comercial se submetem a regramento próprio, que confere ao Conselho Monetário Nacional o dever de fixar os juros a serem praticados. Não havendo atuação do referido órgão, adota-se a limitação de 12% ao ano, prevista no Decreto nº 22.626/1933. Precedentes.
> 8. O art. 5º do Decreto-Lei nº 167/1967, ao determinar que as taxas de juros remuneratórios devem obedecer ao limite fixado pelo CMN, sem ressalvas quanto à possibilidade de livre pactuação, tem por objetivo evitar a fixação de taxas abusivas por parte das instituições financeiras e, simultaneamente, permitir certa flexibilidade, uma vez que o limite pode ser constantemente alterado pelo CMN.
> 9. O CMN, por meio do item 1 do MCR 6-3, autorizou que as partes, em cédulas de crédito rural com recursos não controlados, pactuem livremente as taxas de juros, mas permaneceu omisso quanto à fixação de um limite, de modo que, não havendo limite estabelecido pelo CMN, as taxas acordadas entre as partes não podem ultrapassar o limite de 12% ao ano, conforme previsto no Decreto nº 22.626/1933.
> 10. A mera indexação da CDI em cédulas de crédito rural, não configura abusividade, haja vista que o consignado nesta Corte Superior é que a limitação deve ser de 12% ao ano.
> 11. Recurso especial provido.

### TJMG · Apelação Cível 0346144-21.2013.8.13.0145
- regras: R17
- posicao: FAV
- tribunal: TJMG
- classe_numero: Apelação Cível 0346144-21.2013.8.13.0145
- orgao: 17ª Câmara Cível
- relator: Des. Evandro Lopes da Costa Teixeira
- julgamento: 2023-03-23
- publicacao: 2023-03-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mg/1793581335
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Apelação da empresa tomadora de cédulas de crédito comercial provida em parte para limitar os juros remuneratórios a 12% a.a. (omissão do CMN), vedar a comissão de permanência e substituir o CDI pelo INPC.
- observacao: Faltou TJPR: os acórdãos do TJPR sobre o tema não puderam entrar porque o fetch devolve só o voto, sem a ementa (ver Relatório). O voto mantém a capitalização, por ser pactuada (Súmula 93/STJ), ressalva que a petição deve prever. Datas de julgamento e publicação pela data do Jusbrasil (o texto não traz a data da sessão). O número do processo foi montado a partir do título do Jusbrasil, no padrão CNJ.

ementa:
> APELAÇÃO CÍVEL - CÉDULA DE CRÉDITO COMERCIAL - JUROS REMUNERATÓRIOS - ABUSIVIDADE - FIXAÇÃO EM 12% AO ANO - CABIMENTO - COMISSÃO DE PERMANÊNCIA - INADMISSIBILIDADE - CDI (CERTIFICADO DE DEPÓSITO INTERBANCÁRIO) - ÍNDICE DE CORREÇÃO - AFASTAMENTO - SUBSTITUIÇÃO PELO INPC. - As cédulas de crédito rural, comercial e industrial acham-se submetidas a regramento próprio (Lei nº 6.840/80 e Decreto-Lei 413/69) que conferem ao Conselho Monetário Nacional o dever de fixar os juros a serem praticados. Diante da omissão desse órgão governamental, incide a limitação de 12% ao ano, prevista no Decreto n.º 22.626/33 (Lei da Usura) - Constatado que os juros remuneratórios foram estipulados em taxa superior ao limite legal de 12% ao ano, deve ser reconhecida sua abusividade. - Nas cédulas de crédito rural, comercial e industrial não se admite a cobrança de comissão de permanência. - Nos termos da súmula nº 176 do Superior Tribunal de Justiça, é nula a cláusula que prevê a aplicação do CDI (certificado de depósito interbancário), fornecido pela CETIP, como índice de correção monetária, devendo tal índice ser substituído pelo INPC.

## R19 — Capitalização de juros — vedada sem pactuação expressa

Tese: A capitalização de juros em periodicidade inferior à anual só é lícita se expressa e claramente pactuada; sem pactuação expressa (cláusula clara ou taxa anual superior ao duodécuplo da mensal) ou sem a juntada do contrato pelo banco, a cobrança é ilegal, devendo-se afastar a capitalização e restituir o indébito, mesmo em contrato posterior a 31/03/2000.

### STJ · REsp 973.827/RS
- regras: R19
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 973.827/RS
- orgao: Segunda Seção
- relator: Min. Luis Felipe Salomão (p/ acórdão Min. Maria Isabel Gallotti)
- julgamento: 2012-08-08
- publicacao: 2012-09-24
- precedente_qualificado: Temas 246 e 247/STJ (repetitivo); Súmulas 539 e 541/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106303358
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Prova que a capitalização em periodicidade inferior a um ano só é permitida se expressamente pactuada, e que a pactuação deve ser expressa e clara (primeira e segunda teses).
- observacao: LIMITE, a constar como ressalva na peça (Súmulas 539 e 541/STJ, que resumem este repetitivo): é lícita a capitalização mensal pactuada em contrato posterior a 31/03/2000 e a previsão de taxa anual superior ao duodécuplo da mensal basta como pactuação. O item 2 da ementa ainda afasta o argumento de que taxa efetiva e nominal, por si, caracterizam capitalização, de modo que a peça deve provar a capitalização concreta (juros incorporados ao saldo). Julgamento por maioria (vencidos o Min. Luis Felipe Salomão, relator originário, e os Mins. Paulo de Tarso Sanseverino e Nancy Andrighi). A proclamação da 2ª tese foi retificada no acórdão. Publicação pela data indicada em acórdãos posteriores (DJe 24/09/2012). Faltou julgado de TJ (ver Relatório).

ementa:
> CIVIL E PROCESSUAL. RECURSO ESPECIAL REPETITIVO. AÇÕES REVISIONAL E DE BUSCA E APREENSÃO CONVERTIDA EM DEPÓSITO. CONTRATO DE FINANCIAMENTO COM GARANTIA DE ALIENAÇÃO FIDUCIÁRIA. CAPITALIZAÇÃO DE JUROS. JUROS COMPOSTOS. DECRETO 22.626/1933 MEDIDA PROVISÓRIA 2.170-36/2001. COMISSÃO DE PERMANÊNCIA. MORA. CARACTERIZAÇÃO. 1. A capitalização de juros vedada pelo Decreto 22.626/1933 (Lei de Usura) em intervalo inferior a um ano e permitida pela Medida Provisória 2.170-36/2001, desde que expressamente pactuada, tem por pressuposto a circunstância de os juros devidos e já vencidos serem, periodicamente, incorporados ao valor principal. Os juros não pagos são incorporados ao capital e sobre eles passam a incidir novos juros. 2. Por outro lado, há os conceitos abstratos, de matemática financeira, de "taxa de juros simples" e "taxa de juros compostos", métodos usados na formação da taxa de juros contratada, prévios ao início do cumprimento do contrato. A mera circunstância de estar pactuada taxa efetiva e taxa nominal de juros não implica capitalização de juros, mas apenas processo de formação da taxa de juros pelo método composto, o que não é proibido pelo Decreto 22.626/1933. 3. Teses para os efeitos do art. 543-C do CPC: - "É permitida a capitalização de juros com periodicidade inferior a um ano em contratos celebrados após 31.3.2000, data da publicação da Medida Provisória n. 1.963-17/2000 (em vigor como MP 2.170-36/2001), desde que expressamente pactuada." - "A capitalização dos juros em periodicidade inferior à anual deve vir pactuada de forma expressa e clara. A previsão no contrato bancário de taxa de juros anual superior ao duodécuplo da mensal é suficiente para permitir a cobrança da taxa efetiva anual contratada". 4. Segundo o entendimento pacificado na 2a Seção, a comissão de permanência não pode ser cumulada com quaisquer outros encargos remuneratórios ou moratórios. 5. É lícita a cobrança dos encargos da mora quando caracterizado o estado de inadimplência, que decorre da falta de demonstração da abusividade das cláusulas contratuais questionadas. 6. Recurso especial conhecido em parte e, nessa extensão, provido.

### STJ · AgRg no AREsp 429.029/PR
- regras: R19
- posicao: FAV
- tribunal: STJ
- classe_numero: AgRg no AREsp 429.029/PR
- orgao: Segunda Seção
- relator: Min. Marco Buzzi
- julgamento: 2016-03-09
- publicacao: 2016-04-14
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/340013076
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Prova que, nos contratos bancários sujeitos ao CDC, a capitalização de juros não é automática: exige pactuação expressa e, se o contrato não foi juntado aos autos, é inviável presumir o ajuste do encargo.
- observacao: Julgado da Segunda Seção por maioria (vencidos os Mins. Maria Isabel Gallotti, Ricardo Villas Bôas Cueva, João Otávio de Noronha e Raul Araújo). A hipótese discutida é capitalização anual, em segunda fase de prestação de contas com pretensão revisional, e a ementa trata da capitalização em qualquer periodicidade como dependente de pactuação expressa. O acórdão foi republicado por incorreção na publicação do dia 14/04/2016 (data do texto do Jusbrasil). Faltou julgado de TJ (ver Relatório).

ementa:
> AGRAVO REGIMENTAL NO AGRAVO (ART. 544 DO CPC)- AÇÃO DE PRESTAÇÃO DE CONTAS - SEGUNDA FASE - REVISIONAL DE CONTRATO BANCÁRIO NÃO EXIBIDO - TRIBUNAL A QUO QUE AFIRMA SER NECESSÁRIA A EXPRESSA PACTUAÇÃO PARA A COBRANÇA DO ENCARGO CAPITALIZAÇÃO DE JUROS - IRRESIGNAÇÃO DA CASA BANCÁRIA - DECISÃO MONOCRÁTICA QUE NEGOU PROVIMENTO AO RECLAMO - ÓRGÃO COLEGIADO DA QUARTA TURMA AFETANDO O JULGAMENTO DO RECURSO DE AGRAVO REGIMENTAL À SEGUNDA SEÇÃO. Hipótese: Possibilidade de cobrança de capitalização anual de juros independentemente de expressa pactuação entre as partes 1. A despeito de a demanda ter se iniciado como ação de prestação de contas, o feito já está em sua segunda fase procedimental, na qual prepondera verdadeira pretensão revisional do contrato. Não tendo qualquer das partes promovido irresignação sobre esse ponto, inviável é a extinção da demanda, sob pena de violação ao princípio da non reformatio in pejus . 2. A capitalização de juros consiste na incorporação dos juros ao capital ao final de cada período de contagem. 3. O retrospecto histórico do ordenamento jurídico pátrio acerca da regência legal da capitalização de juros denota que desde tempos remotos é proibido contar juros sobre juros, permitida a acumulação de juros vencidos aos saldos líquidos em conta corrente de ano a ano. 4. Com a evolução, passou-se a admitir a cobrança de juros sobre juros em contratos outros, desde que houvesse lei especial regulatória, bem ainda, prévio ajuste do encargo. 5. Tendo em vista que nos contratos bancários é aplicável o Código de Defesa do Consumidor (súmula 297/STJ), a incidência da capitalização anual de juros não é automática, devendo ser expressamente pactuada, visto que, ante o princípio da boa-fé contratual e a hipossuficiência do consumidor, esse não pode ser cobrado por encargo sequer previsto contratualmente. 6. A jurisprudência consolidada nesta Corte Superior é no sentido de que a cobrança de juros capitalizados em periodicidade anual nos contratos de mútuo firmado com instituições financeiras é permitida quando houver expressa pactuação. Precedentes. 7. Na hipótese, não colacionado aos autos o contrato firmado entre as partes, inviável presumir o ajuste do encargo. 8. Agravo regimental desprovido.

### STJ · REsp 2.256.586/RS
- regras: R19
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.256.586/RS
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2026-05-04
- publicacao: 2026-05-07
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6795866244
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Prova que o STJ (2026) afasta a capitalização diária que o contrato prevê sem indicar a taxa diária, não bastando a menção às taxas efetivas mensal e anual, e que, afastado o encargo da normalidade, fica descaracterizada a mora; o voto também reafirma que, sem o contrato nos autos, é inviável presumir o ajuste de capitalização.
- observacao: Mérito enfrentado e recurso do consumidor provido (revaloração jurídica, sem reexame de fatos). DIVERGÊNCIA NA PRÓPRIA QUARTA TURMA: oito dias depois, no REsp 2.227.062/RS (Min. Maria Isabel Gallotti, 12/05/2026, entrada ADV abaixo), a mesma Turma validou a capitalização diária sem taxa diária quando as taxas efetivas mensal e anual constam do contrato. O voto aplica o REsp 1.826.463/SC (Segunda Seção, 14/10/2020), citado no próprio acórdão. Sirva a peça para contratos com capitalização diária ou sem pactuação clara. Publicação pela data do Jusbrasil.

ementa:
> RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. RECURSO ESPECIAL PROVIDO. I. CASO EM EXAME 1. Recurso especial interposto contra acórdão proferido em apelação nos autos de ação revisional de contrato bancário. 2. A controvérsia decorre de ação revisional de contrato bancário em que foi reconhecida a validade da capitalização de juros. O Tribunal a quo concluiu que a indicação contratual das taxas mensal e anual, sendo a anual superior ao duodécuplo da mensal, é suficiente para admitir capitalização inferior à anual, inclusive diária, não havendo abusividade e permanecendo hígida a mora. No recurso especial, alegou-se que a capitalização diária exige previsão expressa da periodicidade e indicação da taxa diária, não bastando as taxas mensal e anual. II. QUESTÃO EM DISCUSSÃO 3. A questão em discussão consiste em definir sobre a validade da capitalização diária. III. RAZÕES DE DECIDIR 4. Conforme a orientação do STJ, para que seja admitida a cobrança da capitalização diária, é necessária a previsão expressa de sua periodicidade e da taxa diária, não sendo suficiente a menção às taxas efetivas anual e mensal no contrato. O acórdão recorrido contrariou esse entendimento ao admitir a capitalização diária sem previsão contratual expressa. 5. Evidenciada a abusividade das cláusulas contratuais do período da normalidade, resta descaracterizada a mora do devedor, o que impede a busca e apreensão. IV. DISPOSITIVO E TESE 6. Recurso especial conhecido e provido. Tese de julgamento: "1. A capitalização diária de juros exige previsão expressa da periodicidade e indicação da taxa diária. 2. A abusividade dos encargos no período da normalidade contratual descaracteriza a mora". Dispositivos relevantes citados: CDC, arts. 6º, 46, 52. Jurisprudência relevante citada: STJ, REsp n. 973.827/RS, Relatora para o Acórdão Ministra Maria Isabel Gallotti, Segunda Seção, julgado em 8/8/2012, DJe 24/9/2012; REsp n. 1.826.463/SC, relator Ministro Paulo de Tarso Sanseverino, Segunda Seção, julgado em 14/10/2020; STJ, AgRg no AREsp n. 429.029/PR, relator Ministro Marco Buzzi, Segunda Seção, julgado em 9/3/2016; STJ, REsp n. 1.061.530/RS, relatora Ministra Nancy Andrighi, Segunda Seção, julgado em 22/10/2008.

### STJ · REsp 2.227.062/RS
- regras: R19
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.227.062/RS
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2026-05-12
- publicacao: 2026-05-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6621879161
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Fixa o LIMITE a antecipar na peça (Súmula 541/STJ): se o contrato é posterior a 31/03/2000 e traz expressamente a capitalização, ou taxas efetivas mensal e anual com a anual superior ao duodécuplo da mensal, a capitalização é lícita, e o consumidor não obtém a substituição por juros simples nem pela falta da taxa diária.
- observacao: Recurso do consumidor desprovido, por unanimidade. Contrato de prestações prefixadas, com capitalização diária expressa e taxas efetivas mensal e anual informadas. Diverge do REsp 2.256.586/RS, da mesma Turma, oito dias antes (ver acima). Registra a necessidade de compatibilizar o repetitivo REsp 973.827/RS com o REsp 1.826.463/SC (Segunda Seção). Publicação pela data do Jusbrasil. A peça deve distinguir o caso: contrato sem capitalização expressa, sem taxas informadas ou sem contrato juntado.

ementa:
> RECURSO ESPECIAL. AÇÃO REVISIONAL. CONTRATO DE PRESTAÇÕES PREFIXADAS. CAPITALIZAÇÃO DIÁRIA PREVISTA NO CONTRATO. AUSÊNCIA DE ESPECIFICAÇÃO DA TAXA DIÁRIA EQUIVALENTE ÀS TAXAS EFETIVAS MENSAL E ANUAL ESTIPULADAS NO CONTRATO NÃO JUSTIFICA A RESPECTIVA SUBSTITUIÇÃO POR TAXA DE JUROS SIMPLES. 1. Conforme assentado pela Segunda Seção, sob o rito dos recursos repetitivos, no julgamento do REsp. 973.827-RS: "É permitida a capitalização de juros com periodicidade inferior a um ano em contratos celebrados após 31.3.2000, data da publicação da Medida Provisória n. 1.963-17/2000 (em vigor como MP 2.170-36/2001), desde que expressamente pactuada", bem como "A capitalização dos juros em periodicidade inferior à anual deve vir pactuada de forma expressa e clara. A previsão no contrato bancário de taxa de juros anual superior ao duodécuplo da mensal é suficiente para permitir a cobrança da taxa efetiva anual contratada". 2. Necessidade de compatibilização do precedente firmado sob o rito dos recursos repetitivos no REsp 973.827-RS, também consolidado na Súmula 541/STJ, com o acórdão da Segunda Seção no REsp n. 1.826.463/SC, a propósito especificamente da capitalização diária de juros, no qual, apesar de afastada a taxa diária, igualmente foi mantida a estipulação contratual das taxas efetivas mensal e anual. 3. Como exposto no voto condutor do acórdão no REsp. 973.827-RS, o processo de formação da taxa de juros pode ser expresso por meio de juros simples ou de juros compostos, caso em que a mesma taxa efetiva anual será equivalente a determinada taxa mensal efetiva e também a uma taxa diária. Não há como desvincular a taxa efetiva de juros de seus equivalentes em diferentes medidas de tempo: anual, mensal ou diária. 4. A menção destacada à taxa diária somente seria útil ao consumidor caso se cuidasse de contrato de mútuo com prazo para pagamento inferior a um mês, ou, em contrato de maior duração, na hipótese de o devedor pretender antecipar em alguns dias (fração do mês) o pagamento das prestações. Somente nestes casos, teria utilidade a taxa diária, para calcular o valor dos juros a serem abatidos do saldo devedor, em decorrência de eventual antecipação pelo devedor em alguns dias do pagamento em relação à data de vencimento. 5. Não é essa, todavia, a pretensão deduzida nos nestes autos; não pretende o mutuário discutir o valor de juros a ser deduzido caso antecipasse em alguns dias (menos de um mês) o pagamento da dívida. O que se pretende, assim como no caso julgado sob o rito dos repetitivos, é alterar a taxa efetiva de juros contratada, para ler- se juros simples onde está escrito juros capitalizados, a fim de reduzir o valor da prestação e do saldo devedor, a fim de pagar menos juros do que o pactuado, obtendo condições que certamente não seriam conseguidas na negociação com a instituição financeira. 6. Tendo sido expressamente prevista no contrato, posterior à Medida Provisória nº 1.963-17/2000 (em vigor como Medida Provisória 2.170-26/2001), a capitalização diária de juros, assim como especificadas as taxas efetivas equivalentes em periodicidade mensal e anual, o valor do empréstimo, o número e valor das prestações prefixadas para toda a vigência contratual e o valor total da dívida assumida, não há ilegalidade na cobrança das prestações mensais de valor fixo nele estabelecidas, de modo a alcançar a quitação do valor total da dívida claramente especificado no contrato. 7. Recurso especial não provido.

### TJPR · Apelação Cível 0002664-98.2021.8.16.0049
- regras: R19
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002664-98.2021.8.16.0049
- orgao: 13ª Câmara Cível
- relator: Des. Naor Ribeiro de Macedo Neto
- julgamento: 2024-07-12
- publicacao: 2024-07-17
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000027978541/Ac%C3%B3rd%C3%A3o-0002664-98.2021.8.16.0049
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Sem a juntada dos contratos pelo banco, apesar da ordem de exibição, o TJPR afasta a capitalização por falta de pactuação expressa, limita os juros à média de mercado (Súmula 530/STJ) e descaracteriza a mora.
- observacao: Autora pessoa jurídica. A sentença foi anulada em parte (citra petita) e o tribunal julgou o mérito (CPC, art. 1.013, § 3º, III). Repetição simples. Fonte: portal de jurisprudência do TJPR (comarca de Astorga).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CONTRATOS BANCÁRIOS. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA DA AUTORA. CONSTATADA NULIDADE PARCIAL. SENTENÇA CITRA PETITA. PLEITO DE EXIBIÇÃO DE CONTRATOS. PROVA PERICIAL QUE NÃO PODE SER REALIZADA PELA AUSÊNCIA DA JUNTADA DE VÁRIOS CONTRATOS INICIALMENTE REQUERIDOS. ALERTA EFETIVADO QUANTO À INCIDÊNCIA DO ARTIGO 400 DO CPC, NO CASO DE NÃO CUMPRIMENTO DA ORDEM PELO BANCO. MAGISTRADO, ENTRETANTO, QUE NÃO ADMITE COMO VERDADEIROS OS FATOS ALEGADOS, INOBSTANTE A INVERSÃO DO ÔNUS DA PROVA, E ANALISA, TÃO-SOMENTE, A AVENÇA COLACIONADA INICIALMENTE PELA DEMANDANTE. VÍCIO CONSTATADO. JUÍZO QUE VIOLOU OS PRINCÍPIOS DA CONGRUÊNCIA E DA INAFASTABILIDADE DA JURISDIÇÃO (CF, ART. 5º, INCISO XXXV). NULIDADE PARCIAL DA SENTENÇA RECONHECIDA. APLICABILIDADE DO ART. 1.013, §3º, III, DO CPC. EXAME DO MÉRITO DA AÇÃO: 1) JUROS REMUNERATÓRIOS. LIMITAÇÃO À MÉDIA DE MERCADO DIVULGADA PELO BACEN. CONTRATOS FIRMADOS ENTRE AS PARTES NÃO JUNTADOS AOS AUTOS. INCIDÊNCIA DA SÚMULA 530 DO SUPERIOR TRIBUNAL DE JUSTIÇA. 2) CAPITALIZAÇÃO DE JUROS. EXPRESSA PACTUAÇÃO NÃO DEMONSTRADA. ILEGALIDADE. 3) AFASTADAS AS TARIFAS COBRADAS DIANTE DA AUSÊNCIA PACTUAÇÃO EXPRESSA. 4) DESCARACTERIZAÇÃO DA MORA. NECESSIDADE. ABUSIVIDADE NOS ENCARGOS EXIGIDOS NO PERÍODO DA NORMALIDADE CONTRATUAL. 5) REPETIÇÃO DO INDÉBITO NA MODALIDADE SIMPLES, COM CORREÇÃO MONETÁRIA PELA MÉDIA DO INPC/IGP-DI DESDE CADA DESCONTO INDEVIDO ATÉ A CITAÇÃO, MOMENTO EM QUE A CORREÇÃO E OS JUROS DE MORA SERÃO ABARCADOS PELA TAXA SELIC. 6) DANOS MORAIS QUE NÃO SE APERFEIÇOAM NA FORMA IN RE IPSA. 7) PROCEDÊNCIA PARCIAL DOS PEDIDOS AUTORAIS. 8) REDISTRIBUIÇÃO DO ÔNUS DE SUCUMBÊNCIA.RECURSO PROVIDO, para decretar a nulidade parcial da sentença citra petita, e exame, desde logo, do mérito da ação.

### TJPR · Apelação Cível 0012097-79.2022.8.16.0021
- regras: R19
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0012097-79.2022.8.16.0021
- orgao: 13ª Câmara Cível
- relator: Des.ª Rosana Andriguetto de Carvalho
- julgamento: 2024-03-15
- publicacao: 2024-03-18
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000026680261/Ac%C3%B3rd%C3%A3o-0012097-79.2022.8.16.0021
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Em cheque especial sem pactuação expressa, o TJPR exclui a capitalização de juros e as tarifas sem previsão contratual.
- observacao: Correntista pessoa jurídica e credora cooperativa de crédito. A alegação do banco de que havia previsão expressa não foi conhecida (inovação recursal); o ponto decidido é a ausência de pactuação expressa. Fonte: portal de jurisprudência do TJPR (comarca de Cascavel).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CONTRATO DE ABERTURA DE CONTA CORRENTE - CHEQUE ESPECIAL. SENTENÇA DE PROCEDÊNCIA.RECURSO DA INSTITUIÇÃO FINANCEIRA RÉ. ALEGADA PREVISÃO EXPRESSA DE CAPITALIZAÇÃO DE JUROS. NÃO CONHECIMENTO NESTE ASPECTO. INOVAÇÃO RECURSAL. RELATIVIZAÇÃO DO PRINCÍPIO DA PACTA SUNT SERVANDA EM RAZÃO DA FUNÇÃO SOCIAL DO CONTRATO DE ADESÃO E ONEROSIDADE EXCESSIVA. POSSIBILIDADE DE REVISÃO DO CONTRATO EM DISCUSSÃO. ALEGAÇÃO DE INOCORRÊNCIA DE CAPITALIZAÇÃO DE JUROS. NÃO VERIFICAÇÃO. AUSÊNCIA DE PACTUAÇÃO EXPRESSA. IMPOSSIBILIDADE DE COBRANÇA. ENTENDIMENTO CONSOLIDADO DO STJ. EXCLUSÃO DEVIDA. TARIFAS BANCÁRIAS. AUSÊNCIA DE PREVISÃO CONTRATUAL QUANTO À POSSIBILIDADE DE COBRANÇA, AINDA QUE GENÉRICA. CIRCUNSTÂNCIA QUE IMPEDE A COBRANÇA DE QUALQUER VALOR A ESTE TÍTULO, ANTE A AUSÊNCIA DE AUTORIZAÇÃO EXPRESSA DO CLIENTE. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS FIXADOS. RECURSO DA PARTE RÉ PARCIALMENTE CONHECIDO E, NA EXTENSÃO CONHECIDA, NÃO PROVIDO.

## R23 — Rotativo e parcelamento da fatura — teto de 100% de juros e encargos (Lei 14.690/2023, art. 28; Res. CMN 5.112/2023)

Tese: Nas operações de crédito rotativo e de parcelamento de fatura de cartão de crédito realizadas a partir de 03/01/2024, o total cobrado a título de juros e encargos financeiros não pode exceder o valor original da dívida (excluído o IOF), devendo o saldo ser recalculado e o excesso restituído ou abatido.

### TJPR · Recurso Inominado Cível 0009187-95.2025.8.16.0014
- regras: R23
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0009187-95.2025.8.16.0014
- orgao: 5ª Turma Recursal dos Juizados Especiais
- relator: Juíza Fernanda de Quadros Jorgensen Geronasso
- julgamento: 2026-02-13
- publicacao: 2026-02-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/5607799669
- verificado_em: 2026-10-27
- status: CONFERIR
- uso_na_peca: Turma Recursal do TJPR reconhece a regularidade do parcelamento automático, mas determina que os encargos sejam recalculados sobre o valor original da dívida, observado o limite do art. 28, § 1º, da Lei 14.690/2023, em vez de se limitar a taxa fixa.
- observacao: Julgado de Turma Recursal (Juizados), não de Câmara Cível. Publicação pela data do Jusbrasil. ATENÇÃO: o voto e o dispositivo aplicam o limite de 100% do valor original (R$ 771,38), mas o item 14 da ementa ("tese de julgamento") escreve que o limite "restringe o total cobrado ao dobro do valor original da dívida"; citar na peça com base no art. 28, § 1º, e no voto, não nessa frase da tese. O mesmo julgado ressalva que o parcelamento automático (Res. BACEN 4.549/2017) é regular, o que o banco usará em contraponto. A ementa transcreve ementas de outros dois julgados (TJPR e TJMT), com números de processo.

ementa:
> RECURSO INOMINADO. CARTÃO DE CRÉDITO. PARCELAMENTO AUTOMÁTICO DO SALDO DEVEDOR. REGULARIDADE DO PROCEDIMENTO NOS TERMOS DA RESOLUÇÃO BACEN Nº 4.549/2017. LIMITAÇÃO DE JUROS E ENCARGOS. APLICAÇÃO DO ART. 28, § 1º, DA LEI Nº 14.690/2023. RECURSO CONHECIDO E PARCIALMENTE PROVIDO. I. CASO EM EXAME 1. Ação de obrigação de fazer em que a autora buscou a revisão dos juros e encargos decorrentes de parcelamento automático de fatura de cartão de crédito. 2. Sentença de procedência, reconhecendo a regularidade do parcelamento automático, mas limitando a taxa de juros aplicada. 3. Recurso inominado interposto pela instituição financeira, sustentando a legitimidade da cobrança realizada e pugnando pela manutenção dos encargos. II. QUESTÕES EM DISCUSSÃO 4. Há duas questões em discussão: (i) saber se o parcelamento automático realizado após a inadimplência segue a disciplina prevista na Resolução BACEN nº 4.549/2017; (ii) saber se os encargos aplicados excederam o limite legal previsto no art. 28, § 1º, da Lei nº 14.690/2023. III. RAZÕES DE DECIDIR 5. Nos termos da Resolução BACEN nº 4.549/2017, o saldo devedor decorrente do crédito rotativo pode ser mantido até o vencimento da fatura subsequente, sendo permitido o parcelamento automático quando persistente a inadimplência por ao menos dois ciclos. 6. As faturas juntadas comprovam que houve informação adequada ao consumidor e utilização do crédito rotativo por mais de um período, legitimando o parcelamento automático. 7. A jurisprudência das Turmas Recursais reconhece a regularidade do procedimento quando demonstrado o uso do rotativo por dois meses consecutivos e a ausência de falha na prestação do serviço, conforme precedente: “RECURSO INOMINADO. BANCÁRIO. PARCELAMENTO AUTOMÁTICO DE FATURA DE CARTÃO DE CRÉDITO. REGULARIDADE. INDICAÇÃO CLARA AO CONSUMIDOR (...) RECURSO CONHECIDO E PROVIDO.” (TJPR, 5ª Turma Recursal, 0001098-39.2022.8.16.0192, j. 14.04.2025). 8. Quanto aos encargos, a Lei nº 14.690/2023 estabeleceu limite máximo de cobrança, dispondo em seu art. 28, § 1º, que os juros e encargos não podem superar o valor original da dívida. 9. A sentença de origem, embora tenha reconhecido a abusividade, aplicou critério inadequado ao limitar taxa fixa, quando a lei, na verdade, estabelece limite sobre o montante total da dívida. 10. A orientação jurisprudencial tem aplicado o limite de 100% do valor original da dívida em casos de parcelamento automático, reconhecendo a abusividade quando ultrapassado, a exemplo de: “O total de encargos, incluindo juros e tarifas, está limitado a 100% do valor original da dívida (...) Agravo interno parcialmente provido.” (TJMT, RN 10164974920248110002, j. 08.08.2025). 11. Assim, impõe-se a adequação da sentença para determinar a revisão dos encargos, tomando-se como base o valor original da dívida (R$ 771,38), observando-se o limite previsto no art. 28, § 1º, da Lei nº 14.690/2023. 12. Mantém-se, no mais, os demais termos da sentença, inclusive a multa fixada para eventual descumprimento, por não se mostrar excessiva. IV. DISPOSITIVO E TESE 13. Recurso conhecido e parcialmente provido, para reformar parcialmente a sentença apenas quanto ao critério de limitação dos encargos, devendo a requerida revisar o cálculo considerando o valor original da dívida e a limitação imposta pela Lei nº 14.690/2023. 14. Tese de julgamento: A limitação dos juros e encargos incidentes sobre parcelamento automático de fatura de cartão de crédito deve observar o art. 28, § 1º, da Lei nº 14.690/2023, que restringe o total cobrado ao dobro do valor original da dívida, sem imposição de taxa fixa, preservada a regularidade do parcelamento automático previsto na Resolução BACEN nº 4.549/2017.

### TJSP · Apelação Cível 1023130-28.2025.8.26.0001
- regras: R23
- posicao: FAV
- tribunal: TJSP
- classe_numero: Apelação Cível 1023130-28.2025.8.26.0001
- orgao: Núcleo 4.0 – T. VII (DP2)
- relator: Des. Fabiana Calil Canfour de Almeida
- julgamento: 2026-05-06
- publicacao: 2026-05-06
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-sp/5972997904
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Apelação provida em parte para declarar inexigíveis os encargos que excedam o art. 28, § 1º, da Lei 14.690/2023 e determinar o recálculo do débito (rotativo e parcelamento automático) de modo que juros e encargos não passem de 100% da dívida consolidada em 21/12/2023, com amparo na Res. CMN 5.112/2023.
- observacao: Complemento ao TJPR (o TJPR tem acórdão favorável apenas em Turma Recursal; ver relatório). Publicação pela data do Jusbrasil. O acórdão preserva os encargos contratuais até 21/12/2023 e aplica o teto a partir daí (recálculo em cumprimento de sentença); mantém a regularidade do parcelamento automático, a negativação (mora confessada desde 07/2023) e afasta o dano moral, ressalvas a antecipar na peça. Ementa em texto corrido, sem divisão em itens, como no original.

ementa:
> APELAÇÃO CÍVEL. DIREITO DO CONSUMIDOR. AÇÃO REVISIONAL DE CONTRATO DE CARTÃO DE CRÉDITO CUMULADA COM INDENIZAÇÃO POR DANOS MORAIS. SENTENÇA DE IMPROCEDÊNCIA. Parcelamento automático do saldo devedor da fatura de cartão de crédito inadimplida pela parte autora. Regularidade, nos termos da resolução CMN Nº 4.549/2017. Dever de informação observado. Ausência de vício de consentimento. Revisão dos encargos, todavia, cabível no caso concreto. Evolução do débito de R$ 10.019,49, em julho de 2023, para R$ 231.708,98, em fevereiro de 2025. Distorção patrimonial manifesta. Aplicação do artigo 28, § 1º, da lei nº 14.690/2023. Limitação legal de caráter cogente à cobrança de juros e encargos financeiros incidentes sobre o crédito rotativo e o parcelamento do saldo devedor. Resolução CMN nº 5.112/2023. Necessidade de recálculo do débito, em cumprimento de sentença, de modo que o total exigido a título de juros e encargos financeiros não ultrapasse 100% do valor da dívida consolidada em 21/12/2023. Negativação legítima. Inadimplemento confessado desde julho de 2023. Subsistência de dívida principal legítima, decorrente de despesas efetivamente realizadas e não adimplidas pela consumidora. Exercício regular de direito. Pendência de ação revisional que, por si só, não descaracteriza a mora nem obsta a inscrição do nome da devedora em cadastros restritivos. Cancelamento da negativação inviável. Danos morais não configurados. Sucumbência recíproca. Rateio das custas e despesas processuais na proporção de 50% para cada parte. Honorários advocatícios de sucumbência mantidos em 10% sobre o valor atualizado da causa. Inviabilidade de majoração recursal, à luz do tema 1059 do STJ. RECURSO PARCIALMENTE PROVIDO.

### STJ · AREsp 3.191.218/MT
- regras: R23
- posicao: ADV
- tribunal: STJ
- classe_numero: AREsp 3.191.218/MT
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2026-06-15
- publicacao: 2026-06-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6799368646
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva a antecipar: a Terceira Turma do STJ já registrou, em ementa, que a Lei 14.690/2023 não cria teto imediato e universal para o cartão e não alcança contratos anteriores à sua entrada em vigor; a peça deve invocar apenas operações posteriores a 03/01/2024 (Res. CMN 5.112, art. 2º-D).
- observacao: Posição ADV de alcance limitado: acórdão de agravo em REsp (ação monitória, contrato anterior à lei) que mantém a conclusão do TJMT; o voto reproduz o fundamento do tribunal de origem ("a norma não estabelece um teto generalizado... mecanismo de autorregulação") sem examinar a Res. CMN 5.112/2023, que o CMN editou em 21/12/2023, nem o seu art. 2º-D. Não é precedente qualificado. Publicação pela data do Jusbrasil. Não tratar como superação do teto; usar apenas como alerta do limite temporal e do ônus de demonstrar que a operação é posterior a 03/01/2024.

ementa:
> CIVIL. PROCESSUAL CIVIL. AGRAVO EM RECURSO ESPECIAL. AÇÃO MONITÓRIA. CONTRATOS BANCÁRIOS. CARTÃO DE CRÉDITO E CRÉDITO PESSOAL. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO OCORRÊNCIA. GRATUIDADE DA JUSTIÇA. AUSÊNCIA DE INTERESSE RECURSAL. VENCIMENTO ANTECIPADO DA DÍVIDA. PREVISÃO CONTRATUAL. REEXAME FÁTICO. SÚMULAS 5 E 7/STJ. JUROS REMUNERATÓRIOS. ABUSIVIDADE. ÔNUS DA PROVA. SÚMULA 596/STF. TEMA 27/STJ. LEI N. 14.690/2023. INAPLICABILIDADE AUTOMÁTICA. HONORÁRIOS RECURSAIS. MAJORAÇÃO. 1. Não configura negativa de prestação jurisdicional o acórdão que aprecia, de forma fundamentada, as questões controvertidas, ainda que de modo contrário aos interesses da parte recorrente. 2. Ausente o interesse recursal quando o benefício da gratuidade da justiça já foi concedido na instância de origem para fins de processamento do apelo. 3. Mantida a conclusão do Tribunal de origem sobre a validade do vencimento antecipado das parcelas vincendas diante do inadimplemento, por haver previsão contratual expressa e por demandar sua revisão o reexame de fatos e cláusulas contratuais - óbice das Súmulas n. 5 e 7/STJ. 4. As instituições financeiras não se sujeitam ao limite de juros da Lei de Usura, e a revisão das taxas remuneratórias exige demonstração cabal de abusividade em cotejo com a taxa média de mercado, nos termos da Súmula n. 596/STF e do Tema n. 27/STJ. 5. A Lei n. 14.690/2023 não institui teto imediato e universal de encargos para cartão de crédito, dependendo de implementação de mecanismos de autorregulação pelos emissores e de aprovação pelo Banco Central, sem aplicação retroativa sobre contratos anteriores já vigentes quando de sua entrada em vigor. 6. Agravo conhecido para negar provimento ao recurso especial.

## R24 — Cartão de crédito consignado com RMC/RCC em benefício previdenciário — nulidade/conversão em empréstimo consignado por falta de informação

Tese: A contratação de cartão de crédito consignado com reserva de margem consignável por consumidor que pretendia empréstimo consignado comum, sem informação clara sobre a natureza do produto e sobre a amortização, caracteriza falha no dever de informação e vício de consentimento, devendo o contrato ser anulado ou convertido em empréstimo consignado (juros pela taxa média do BACEN), com restituição do que foi pago a maior e indenização por danos morais.

### TJRS · Apelação Cível 5004183-61.2022.8.21.0077
- regras: R24
- posicao: FAV
- tribunal: TJRS
- classe_numero: Apelação Cível 5004183-61.2022.8.21.0077
- orgao: 17ª Câmara Cível
- relator: Des. Vanise Rohrig Monte Aço
- julgamento: 2025-12-18
- publicacao: 2025-12-18
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-rs/5980568334
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Reconhece falha no dever de informação na contratação de cartão RMC por quem queria empréstimo consignado e determina a conversão em empréstimo pessoal consignado (valor sacado como capital, taxa média BACEN do consignado INSS na data da contratação, descontos imputados na amortização, restituição simples do excedente).
- observacao: Faltou no TJPR (não há acórdão favorável de TJPR com ementa íntegra no fetch; ver relatório). Publicação pela data do Jusbrasil (sessão virtual de 17 a 18/12/2025). O acórdão NEGA dano moral e a repetição em dobro (restituição simples); o voto invoca, por precedente citado, o IRDR nº 28 do TJRS. Tema 1414/STJ (conversão como consequência da invalidação) segue pendente; a peça deve apresentar a conversão como pedido principal ou alternativo, ciente do risco de sobrestamento.

ementa:
> DIREITO CIVIL. APELAÇÃO CÍVEL. CARTÃO DE CRÉDITO CONSIGNADO. FALHA NO DEVER DE INFORMAÇÃO. CONVERSÃO EM EMPRÉSTIMO CONSIGNADO. DANOS MORAIS NÃO CONFIGURADOS. RECURSO PARCIALMENTE PROVIDO. I. CASO EM EXAME: 1. Apelação cível interposta contra sentença que julgou improcedentes os pedidos formulados em ação declaratória de nulidade de negócio jurídico c/c repetição de indébito e indenização por danos morais, na qual o autor alegou ter sido ludibriado ao contratar cartão de crédito com reserva de margem consignável (RMC), quando pretendia um empréstimo consignado tradicional. II. QUESTÃO EM DISCUSSÃO: 1. Há três questões em discussão: (i) a existência de falha no dever de informação na contratação do cartão de crédito consignado; (ii) a possibilidade de conversão do contrato para a modalidade de empréstimo consignado; (iii) a configuração de danos morais indenizáveis. III. RAZÕES DE DECIDIR: 1. A relação jurídica estabelecida entre as partes é de consumo, atraindo a incidência do CDC e seus princípios protetivos, com destaque para o direito à informação adequada e clara sobre produtos e serviços, conforme o art. 6º, III, do CDC. 2. O cartão de crédito com RMC é um produto financeiro substancialmente mais complexo e oneroso que o empréstimo consignado tradicional, pois o desconto mensal em folha corresponde ao pagamento mínimo da fatura, destinando-se majoritariamente a cobrir encargos do rotativo, com pouca ou nenhuma amortização do principal. 3. A narrativa do apelante, de que buscava um empréstimo e não um cartão de crédito, é verossímil, especialmente considerando que não utilizou o cartão em nenhuma operação comercial além do saque inicial, o que evidencia sua real intenção de contratar um empréstimo. 4. A instituição financeira não comprovou ter prestado informações claras e destacadas sobre a natureza do produto contratado, seu mecanismo de funcionamento, a incidência dos juros do rotativo e a ausência de prazo fixo para liquidação da dívida. 5. A solução jurídica mais adequada é a conversão do contrato de cartão de crédito RMC em empréstimo pessoal consignado, considerando como capital principal o valor efetivamente sacado, com incidência de juros remuneratórios à taxa média de mercado para operações de crédito pessoal consignado para aposentados do INSS. 6. Os valores já descontados do benefício previdenciário devem ser imputados para amortização da dívida recalculada, quitando-se primeiro os juros e depois o principal. 7. O pedido de indenização por danos morais não merece acolhimento, pois não há elementos que comprovem abalo extraordinário aos direitos da personalidade do apelante, limitando-se a situação a um inadimplemento contratual que se resolve na esfera patrimonial. IV. DISPOSITIVO E TESE: 1. Recurso parcialmente provido para declarar a abusividade da contratação na modalidade de cartão de crédito com RMC, determinar sua conversão em contrato de empréstimo pessoal consignado e estabelecer a redistribuição dos ônus sucumbenciais em 30% para o autor e 70% para o banco réu. Tese de julgamento: 1. A contratação de cartão de crédito consignado, quando o consumidor pretendia empréstimo consignado tradicional, configura falha no dever de informação e justifica a conversão do contrato para a modalidade pretendida, sem que isso, por si só, caracterize dano moral indenizável. ___________ Dispositivos relevantes citados: CDC, arts. 2º, 3º, 6º, III, 39, IV, 46; CC, art. 422. Jurisprudência relevante citada: TJRS, Apelação Cível, Nº 52166878120248210001, Décima Sétima Câmara Cível, Rel. Eugênio Couto Terra, j. 01-08-2025.

### TJMT · Apelação Cível 1019215-19.2024.8.11.0002
- regras: R24
- posicao: FAV
- tribunal: TJMT
- classe_numero: Apelação Cível 1019215-19.2024.8.11.0002
- orgao: Quarta Câmara de Direito Privado
- relator: Des. Serly Marcondes Alves
- julgamento: 2025-11-19
- publicacao: 2025-11-20
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mt/5326671619
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Reforma sentença de improcedência para declarar o vício de consentimento por falha no dever de informação (cartão não entregue, valor creditado por TED, contrato sem número de parcelas), converter o RMC em empréstimo consignado convencional pela taxa média BACEN da época e restituir de forma simples o pago a maior.
- observacao: Faltou no TJPR. Publicação pela data do Jusbrasil (julgamento em sessão de 19/11/2025). O texto do Jusbrasil junta palavras (ex.: "tratar-sede", "interessena"); aqui, separadas. O acórdão não trata de dano moral na tese (pedido não acolhido) e determina restituição simples, não em dobro. Mesma ressalva do Tema 1414/STJ.

ementa:
> EMENTA DIREITO DO CONSUMIDOR E BANCÁRIO. APELAÇÃO CÍVEL. CARTÃO DE CRÉDITO CONSIGNADO COM RESERVA DE MARGEM CONSIGNÁVEL (RMC). VÍCIO DE CONSENTIMENTO. FALHA NO DEVER DE INFORMAÇÃO. CONVERSÃO DO CONTRATO PARA EMPRÉSTIMO CONSIGNADO CONVENCIONAL. RESTITUIÇÃO SIMPLES DOS VALORES PAGOS A MAIOR. RECURSO PROVIDO. I. CASO EM EXAME 1. Recurso de apelação interposto contra sentença que julgou improcedentes os pedidos formulados na ação revisional de contrato cumulada com repetição do indébito e indenização por danos morais. A apelante sustenta ter sido induzida a erro ao celebrar contrato de cartão de crédito consignado com reserva de margem consignável (RMC), acreditando tratar-se de empréstimo consignado convencional, e pleiteia a revisão contratual, a restituição de valores pagos a maior e o reconhecimento do vício de consentimento. II. QUESTÃO EM DISCUSSÃO 1. Há duas questões centrais em discussão: (i) definir se houve vício de consentimento decorrente de falha no dever de informação na contratação do cartão de crédito consignado com RMC; (ii) determinar se é cabível a conversão da modalidade contratual para empréstimo consignado convencional, com restituição dos valores pagos indevidamente e limitação da taxa de juros à média de mercado. III. RAZÕES DE DECIDIR 1. O princípio da dialeticidade recursal não é violado quando as razões de apelação impugnam os fundamentos da sentença, ainda que repitam argumentos da inicial, desde que demonstrado o interesse na reforma do julgado (STJ, AgInt no AREsp 976.892/GO). 1. O cartão de crédito consignado com RMC constitui modalidade híbrida de crédito, cuja amortização ocorre por meio do desconto mínimo em folha, diferindo do empréstimo consignado tradicional, em que as parcelas amortizam integralmente o saldo devedor. 1. O dever de informação, previsto nos arts. 6º, III, e 46 do Código de Defesa do Consumidor, impõe ao fornecedor o ônus de prestar informações claras, precisas e ostensivas sobre o produto ou serviço oferecido, especialmente em operações financeiras complexas. 1. A ausência de entrega do cartão físico, a disponibilização do valor contratado por TED e a inexistência de informações claras no contrato quanto ao número de parcelas e encargos configuram falha no dever de informação, apta a caracterizar vício de consentimento. 1. A conversão do contrato de cartão de crédito consignado com RMC em empréstimo consignado convencional preserva o negócio jurídico e corrige o desvirtuamento da contratação, conforme o princípio da conservação dos contratos (CC, art. 170). 1. Os juros remuneratórios devem ser recalculados conforme a taxa média de mercado para empréstimos consignados, divulgada pelo Banco Central à época da contratação. 1. A restituição dos valores pagos a maior deve ocorrer de forma simples, pois não se comprovou má-fé da instituição financeira, conforme entendimento do STJ (AgInt no AREsp 1.110.103/DF). 1. A cumulação da Taxa Selic com o INPC é indevida, devendo incidir apenas a Taxa Selic para atualização dos valores a restituir. IV. DISPOSITIVO E TESE 1. Recurso provido. Tese de julgamento: 1. A contratação de cartão de crédito consignado, quando o consumidor acredita estar firmando empréstimo consignado tradicional, caracteriza vício de consentimento por falha no dever de informação. 1. A operação deve ser convertida em contrato de empréstimo consignado convencional, aplicando-se a taxa média de mercado para essa modalidade à época da contratação. 1. É devida a restituição simples dos valores pagos a maior, em razão da ausência de comprovação de má-fé da instituição financeira. 1. A atualização monetária deve observar exclusivamente a Taxa Selic, afastada a cumulação com o INPC. Dispositivos relevantes citados: CC, art. 170; CDC, arts. 6º, III, 39, III e V, 42, e 46. Jurisprudência relevante citada: STJ, AgInt no AREsp 976.892/GO, Rel. Min. Raul Araújo, Quarta Turma, DJe 29/08/2017; STJ, AgInt no REsp 1.823.145/SP, Rel. Min. Marco Buzzi, Quarta Turma, DJe 11/10/2019; STJ, AgInt no AREsp 1.110.103/DF, Rel. Min. Maria Isabel Gallotti, Quarta Turma, DJe 19/04/2018; TJMT, N.U 1025321-96.2021.8.11.0003, Rel. Des. Guiomar Teodoro Borges, j. 26/07/2023; TJMT, N.U 1031920-29.2024.8.11.0041, Rel. Des. Rubens de Oliveira Santos Filho, j. 30/04/2025.

## R26 — Repetição do indébito em dobro — boa-fé objetiva, sem exigir má-fé

Tese: A repetição em dobro (CDC, art. 42, parágrafo único) independe de má-fé e cabe quando a cobrança indevida contraria a boa-fé objetiva, para os pagamentos posteriores a 30/03/2021 (modulação do EAREsp 676.608/RS).

### STJ · EAREsp 676.608/RS
- regras: R26
- posicao: FAV
- tribunal: STJ
- classe_numero: EAREsp 676.608/RS
- orgao: Corte Especial
- relator: Min. Og Fernandes
- julgamento: 2020-10-21
- publicacao: 2021-03-30
- precedente_qualificado: não (embargos de divergência da Corte Especial; o Tema 929/STJ, repetitivo sobre o mesmo ponto, ficou pendente — ver relatório)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1205685304
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Fixa a tese de que a restituição em dobro independe do elemento volitivo do fornecedor e cabe quando a cobrança indevida contraria a boa-fé objetiva, e traz a modulação (contratos de consumo privados: só para pagamentos após a publicação do acórdão, 30/03/2021).
- observacao: Modulação confirmada no texto: aplica-se "apenas a partir da publicação do presente acórdão" às cobranças em contratos de consumo que não envolvam serviço público; a modulação vale só para a primeira tese. Mesma tese, mesma modulação e mesma data nos EREsp 1.413.542/RS, EAREsp 600.663/RS e outros (a redação da ementa difere: a do EAREsp 676.608/RS é a do voto do relator Og Fernandes; o STJ costuma citar Min. Herman Benjamin como relator para o acórdão da tese nesses embargos, o que a cópia aberta não registra). Os cabeçalhos de página "Superior Tribunal de Justiça" que o PDF inseriu no meio do texto foram retirados da ementa abaixo. Publicação conforme DJe indicado nos acórdãos posteriores.

ementa:
> EMBARGOS DE DIVERGÊNCIA EM AGRAVO EM RECURSO ESPECIAL. CIVIL. PROCESSUAL CIVIL. TELEFONIA FIXA. COBRANÇA INDEVIDA. AÇÃO DE REPETIÇÃO DE INDÉBITO DE TARIFAS. 1) RESTITUIÇÃO EM DOBRO DO INDÉBITO (PARÁGRAFO ÚNICO DO ARTIGO 42 DO CDC). DESINFLUÊNCIA DA NATUREZA DO ELEMENTO VOLITIVO DO FORNECEDOR QUE REALIZOU A COBRANÇA INDEVIDA. DOBRA CABÍVEL QUANDO A REFERIDA COBRANÇA CONSUBSTANCIAR CONDUTA CONTRÁRIA À BOA-FÉ OBJETIVA. 2) APLICAÇÃO DO PRAZO PRESCRICIONAL DECENAL DO CÓDIGO CIVIL (ART. 205 DO CÓDIGO CIVIL). APLICAÇÃO ANALÓGICA DA SÚMULA 412 /STJ. 3) MODULAÇÃO PARCIAL DOS EFEITOS DA DECISÃO. CONHECIMENTO E PROVIMENTO INTEGRAL DO RECURSO. 1. Trata-se de embargos de divergência interpostos contra acórdão em que se discute o lapso prescricional cabível aos casos de repetição de indébito por cobrança indevida de valores referentes a serviços não contratados, promovida por empresa de telefonia. Discute-se, ainda, acerca da necessidade de comprovação da má-fé pelo consumidor para aplicação do art. 42, parágrafo único, do Código de Defesa do Consumidor . 2. Na configuração da divergência do presente caso, temos, de um lado, o acórdão embargado da Terceira Turma concluindo que a norma do art. 42 do Código de Defesa do Consumidor pressupõe a demonstração de que a cobrança indevida decorreu de má-fé do credor fornecedor do serviço, enquanto os acórdãos-paradigmas da Primeira Seção afirmam que a repetição em dobro prescinde de má-fé, bastando a culpa. Ilustrando o posicionamento da Primeira Seção: EREsp 1.155.827/SP, Rel. Min. Humberto Martins, Primeira Seção, DJe 30/6/2011. Para exemplificar o posicionamento da Segunda Seção, vide: EREsp 1.127.721/RS, Rel. Min. Antônio Carlos Ferreira, Rel. p/ Acórdão Min. Marco Buzzi, Segunda Seção, DJe 13/3/2013. 3. Quanto ao citado parágrafo único do art. 42 do CDC, abstrai-se que a cobrança indevida será devolvida em dobro, "salvo hipótese de engano justificável". Em outras palavras, se não houver justificativa para a cobrança indevida, a repetição do indébito será em dobro. A divergência aqui constatada diz respeito ao caráter volitivo, a saber: se a ação que acarretou cobrança indevida deve ser voluntária (dolo/má-fé) e/ou involuntária (por culpa). 4. O próprio dispositivo legal caracteriza a conduta como engano e somente exclui a devolução em dobro se ele for justificável. Ou seja, a conduta base para a repetição de indébito é a ocorrência de engano, e a lei, rígida na imposição da boa-fé objetiva do fornecedor do produto ou do serviço, somente exclui a devolução dobrada se a conduta (engano) for justificável (não decorrente de culpa ou dolo do fornecedor). 5. Exigir a má-fé do fornecedor de produto ou de serviço equivale a impor a ocorrência de ação dolosa de prejudicar o consumidor como requisito da devolução em dobro, o que não se coaduna com o preceito legal. Nesse ponto, a construção realizada pela Segunda Seção em seus precedentes, ao invocar a má-fé do fornecedor como fundamento para a afastar a duplicação da repetição do indébito, não me convence, pois atribui requisito não previsto em lei. 6. A tese da exclusividade do dolo inviabiliza, por exemplo, a devolução em dobro de pacotes de serviços, no caso de telefonia, jamais solicitados pelo consumidor e sobre o qual o fornecedor do serviço invoque qualquer "justificativa do seu engano". Isso porque o requisito subjetivo da má-fé é prova substancialmente difícil de produzir. Exigir que o consumidor prove dolo ou má-fé do fornecedor é imputar-lhe prova diabólica, padrão probatório que vai de encontro às próprias filosofia e ratio do CDC . 7. Não vislumbro distinção para os casos em que o indébito provém de contratos que não envolvam fornecimento de serviços públicos, de forma que também deve prevalecer para todas as hipóteses a tese, que defendi acima, de que tanto a conduta dolosa quanto culposa do fornecedor de serviços dá azo à devolução em dobro do indébito, de acordo com o art. 42 do CDC . Nessas modalidades contratuais, também deve prevalecer o critério dúplice do dolo/culpa. Assim, tanto a conduta dolosa quanto a culposa do fornecedor de serviços dão substrato à devolução em dobro do indébito, à luz do art. 42 do CDC . 8. A Primeira Seção, no julgamento do REsp 1.113.403/RJ, de relatoria do Ministro Teori Albino Zavascki (DJe 15/9/2009), submetido ao regime dos recursos repetitivos do art. 543-C do Código de Processo Civil e da Resolução STJ 8/2008, firmou o entendimento de que, ante a ausência de disposição específica acerca do prazo prescricional aplicável à prática comercial indevida de cobrança excessiva, é de rigor a incidência das normas gerais relativas à prescrição insculpidas no Código Civil na ação de repetição de indébito de tarifas de água e esgoto. Assim, tem-se prazo vintenário, na forma estabelecida no art. 177 do Código Civil de 1916, ou decenal, de acordo com o previsto no art. 205 do Código Civil de 2002 . Diante da mesma conjuntura, não há razões para adotar solução diversa nos casos de repetição de indébito dos serviços de telefonia. 9. A tese adotada no âmbito do acórdão recorrido, de que a pretensão de repetição de indébito por cobrança indevida de valores referentes a serviços não contratados, promovida por empresa de telefonia, configuraria enriquecimento sem causa e, portanto, estaria abrangida pelo prazo fixado no art. 206, § 3º, IV, do Código Civil, não parece ser a melhor. A pretensão de enriquecimento sem causa (ação in rem verso) possui como requisitos: enriquecimento de alguém; empobrecimento correspondente de outrem; relação de causalidade entre ambos; ausência de causa jurídica; inexistência de ação específica. Trata-se, portanto, de ação subsidiária que depende da inexistência de causa jurídica. A discussão acerca da cobrança indevida de valores constantes de relação contratual e eventual repetição de indébito não se enquadra na hipótese do art. 206, § 3º, IV, do Código Civil, seja porque a causa jurídica, em princípio, existe (relação contratual prévia em que se debate a legitimidade da cobrança), seja porque a ação de repetição de indébito é ação específica. Doutrina. 10. Na hipótese aqui tratada, a jurisprudência da Segunda Seção, relativa a contratos privados, seguia compreensão que, com o presente julgamento, passa a ser superada, em consonância com a dominante da Primeira Seção, o que faz sobressair a necessidade de privilegiar os princípios da segurança jurídica e da proteção da confiança dos jurisdicionados. 11. Assim, proponho modular os efeitos da presente decisão para que o entendimento aqui fixado seja empregado aos indébitos de natureza contratual não pública pagos após a data da publicação do acórdão. 12. Embargos de divergência conhecidos e providos integralmente, para impor a devolução em dobro do indébito. 13. Fixação das seguintes teses. Primeira tese: A restituição em dobro do indébito (parágrafo único do artigo 42 do CDC) independe da natureza do elemento volitivo do fornecedor que realizou a cobrança indevida, revelando-se cabível quando a referida cobrança consubstanciar conduta contrária à boa-fé objetiva. Segunda tese: A ação de repetição de indébito por cobrança de valores referentes a serviços não contratados promovida por empresa de telefonia deve seguir a norma geral do prazo prescricional decenal, consoante previsto no artigo 205 do Código Civil, a exemplo do que decidido e sumulado no que diz respeito ao lapso prescricional para repetição de tarifas de água e esgoto (Súmula 412 /STJ). Modulação dos efeitos: Modulam-se os efeitos da presente decisão - somente com relação à primeira tese - para que o entendimento aqui fixado quanto à restituição em dobro do indébito seja aplicado apenas a partir da publicação do presente acórdão. A modulação incide unicamente em relação às cobranças indevidas em contratos de consumo que não envolvam prestação de serviços públicos pelo Estado ou por concessionárias, as quais apenas serão atingidas pelo novo entendimento quando pagas após a data da publicação do acórdão.

### STJ · AREsp 3.194.853/PE
- regras: R26
- posicao: FAV
- tribunal: STJ
- classe_numero: AREsp 3.194.853/PE
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2026-06-15
- publicacao: 2026-06-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6799384670
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão recente da Terceira Turma, em contrato bancário (empréstimo consignado), mantendo a repetição em dobro sem exigir má-fé, porque a cobrança sem base contratual válida viola a boa-fé objetiva e não é engano justificável.
- observacao: Caso de consignado fraudulento (assinatura falsa) com idoso, não de tarifa ou seguro; o voto não examina a data dos descontos em relação ao marco de 30/03/2021 (reproduz a ementa do EAREsp 1.501.756/SC, que reafirma a modulação). Na peça, conferir os meses dos pagamentos. Publicação pela data do Jusbrasil.

ementa:
> PROCESSUAL CIVIL. CONSUMIDOR. AGRAVO EM RECURSO ESPECIAL. CONTRATO BANCÁRIO. EMPRÉSTIMO CONSIGNADO. FRAUDE. ASSINATURA FALSA. RESPONSABILIDADE OBJETIVA. REPETIÇÃO EM DOBRO. DANO MORAL. QUANTUM INDENIZATÓRIO. AGRAVOS CONHECIDOS PARA NEGAR PROVIMENTO AOS RECURSOS ESPECIAIS. RECURSO DE SABEMI SEGURADORA S.A. 1. Mantida a repetição em dobro dos valores indevidamente descontados, pois a cobrança indevida com violação da boa-fé objetiva dispensa a comprovação de má-fé do fornecedor, conforme orientação da Corte Especial firmada nos EREsp 1.413.542/RS. 2. Mantida a condenação por danos morais, cujo valor não se revela irrisório nem exorbitante diante da gravidade da fraude e da condição de idoso da vítima, afastando a intervenção excepcional desta Corte. 3. Agravo conhecido para negar provimento ao recurso especial. RECURSO DE BANCO PAN S.A. 1. Inexiste negativa de prestação jurisdicional quando o acórdão recorrido enfrenta os pontos necessários à resolução da lide e apresenta fundamentação suficiente para o desfecho da controvérsia, ainda que contrária aos interesses da parte. 2. Mantida a responsabilidade objetiva da instituição financeira pelos danos decorrentes de fraude contratual praticada por terceiro, diante do reconhecimento da falha na segurança do serviço. 3. Agravo conhecido para negar provimento ao recurso especial.

### STJ · AgInt no AREsp 1.777.647/DF
- regras: R26
- posicao: ADV
- tribunal: STJ
- classe_numero: AgInt no AREsp 1.777.647/DF
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2021-10-11
- publicacao: 2021-11-17
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2107693092
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Limite temporal da tese: em contratos bancários, cobrança indevida anterior a 30/03/2021 sem prova de má-fé é restituída de forma simples; a peça deve delimitar o pedido de dobro aos pagamentos posteriores ao marco (ou provar a má-fé dos anteriores).
- observacao: Aplicação da modulação do EREsp 1.413.542/RS e EAREsp 676.608/RS a contrato bancário. Publicação pela data do Jusbrasil.

ementa:
> AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. DIALETICIDADE. IMPUGNAÇÃO DA DECISÃO AGRAVADA. OCORRÊNCIA. REVISÃO DE FATOS. DESNECESSIDADE. CONSUMIDOR. DEVOLUÇÃO EM DOBRO DE COBRANÇA INDEVIDA ANTERIOR A 30/03/2021 E RELATIVA A CONTRATO PRIVADO. MÁ-FÉ. NECESSIDADE. AGRAVO INTERNO A QUE SE NEGA PROVIMENTO. 1. Em virtude da impugnação do fundamento da decisão de inadmissibilidade do recurso especial, é devido o conhecimento do agravo em recurso especial. 2. No caso dos autos, é prescindível o reexame fático-probatório, não incidindo o óbice da Súmula 7 /STJ, pois todas as circunstâncias necessárias ao conhecimento do recurso especial foram delineadas no acórdão recorrido. 3. Segundo tese fixada pela Corte Especial, "a repetição em dobro, prevista no parágrafo único do art. 42 do CDC, é cabível quando a cobrança indevida consubstanciar conduta contrária à boa-fé objetiva, ou seja, deve ocorrer independentemente da natureza do elemento volitivo" (EREsp 1.413.542/RS, Rel. Ministra MARIA THEREZA DE ASSIS MOURA, Rel. p/ acórdão Ministro HERMAN BENJAMIN, CORTE ESPECIAL, julgado em 21/10/2020, DJe de 30/03/2021). 4. Esse entendimento, todavia, por modulação de efeitos também aprovada na mesma decisão, somente é aplicável a cobranças não decorrentes de prestação de serviço público realizadas após a data da publicação do acórdão em que fixado o precedente. 5. Caso concreto no qual a cobrança indevida de débito exclusivamente privado (contratos bancários) foi realizada sem comprovação de má-fé e anteriormente à publicação do precedente, motivo pelo qual, em observância à modulação de efeitos, não foi aplicada a tese naquele fixada, sendo confirmada a devolução simples dos valores cobrados. 6. Agravo interno a que se nega provimento.

### TJPR · Recurso Inominado Cível 0009693-37.2024.8.16.0069
- regras: R26
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0009693-37.2024.8.16.0069
- orgao: 2ª Turma Recursal dos Juizados Especiais
- relator: Juíza Vanessa de Souza Camargo
- julgamento: 2026-05-12
- publicacao: 2026-05-12
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-pr/6090410478
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Em financiamento de veículo, aplica o EAREsp 676.608/RS e a modulação: tarifa de avaliação sem prova do serviço e seguro com venda casada devolvidos de forma simples até 30/03/2021 e em dobro depois, sem exigir má-fé.
- observacao: Julgado de Turma Recursal dos Juizados Especiais. O voto cita o marco como "[31/03/2021]" na transcrição da modulação, mas o DJe do EAREsp é 30/03/2021; usar 30/03/2021. Data de publicação igual à do julgamento (data do Jusbrasil).

ementa:
> DIREITO DO CONSUMIDOR. RECURSOS INOMINADOS. REPETIÇÃO DE INDÉBITO. CONTRATO DE FINANCIAMENTO DE VEÍCULO. TARIFA DE AVALIAÇÃO DO BEM. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO. DOCUMENTOS UNILATERAIS INSUFICIENTES. COBRANÇA ABUSIVA. TARIFA DE REGISTRO DE CONTRATO. PREVISÃO CONTRATUAL. SERVIÇO COMPROVADO. ONEROSIDADE NÃO EVIDENCIADA. SEGURO PRESTAMISTA. CONTRATAÇÃO AUTOMÁTICA. AUSÊNCIA DE OPÇÃO REAL AO CONSUMIDOR QUANTO À ADESÃO E À ESCOLHA DA SEGURADORA. VENDA CASADA CONFIGURADA. RESTITUIÇÃO DOS VALORES DE FORMA SIMPLES E DOBRADA. ENTENDIMENTO DO STJ. RECURSO DO AUTOR CONHECIDO E PARCIALMENTE PROVIDO. RECURSO DA INSTITUIÇÃO FINANCEIRA CONHECIDO E DESPROVIDO.

## R28 — Impugnação da assinatura — ônus da instituição financeira

Tese: Impugnada pelo consumidor a autenticidade da assinatura do contrato bancário juntado pela instituição financeira, cabe a esta provar a autenticidade (CPC, arts. 6º, 369 e 429, II).

### STJ · REsp 1.846.649/MA
- regras: R28
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.846.649/MA
- orgao: Segunda Seção
- relator: Min. Marco Aurélio Bellizze
- julgamento: 2021-11-24
- publicacao: 2021-12-09
- precedente_qualificado: Tema 1061/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106310297
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case do Tema 1061: impugnada a assinatura do contrato bancário, o ônus de provar a autenticidade é da instituição financeira.
- observacao: A ementa cita "arts. 6º, 368 e 429, II", mas a tese aprovada no acórdão, reproduzida pelo próprio STJ e pelos tribunais, é "arts. 6º, 369 e 429, II"; na peça, citar o art. 369. Oriundo de IRDR do TJMA sobre empréstimo consignado; a tese vale para "contrato bancário" em geral.

ementa:
> RECURSO ESPECIAL. PROCESSUAL CIVIL. ACÓRDÃO PROFERIDO EM IRDR. CONTRATOS BANCÁRIOS. EMPRÉSTIMO CONSIGNADO. DOCUMENTO PARTICULAR. IMPUGNAÇÃO DA AUTENTICIDADE DA ASSINATURA. ÔNUS DA PROVA. RECURSO ESPECIAL PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, DESPROVIDO. 1. Para os fins do art. 1.036 do CPC/2015, a tese firmada é a seguinte: "Na hipótese em que o consumidor/autor impugnar a autenticidade da assinatura constante em contrato bancário juntado ao processo pela instituição financeira, caberá a esta o ônus de provar a sua autenticidade (CPC, arts. 6º, 368 e 429, II)." 2. Julgamento do caso concreto. 2.1. A negativa de prestação jurisdicional não foi demonstrada, pois deficiente sua fundamentação, já que o recorrente não especificou como o acórdão de origem teria se negado a enfrentar questões aduzidas pelas partes, tampouco discorreu sobre as matérias que entendeu por omissas. Aplicação analógica da Súmula 284/STF. 2.2. O acórdão recorrido imputou o ônus probatório à instituição financeira, conforme a tese acima firmada, o que impõe o desprovimento do recurso especial. 3. Recurso especial parcialmente conhecido e, nessa extensão, desprovido.

### STJ · AgInt no AREsp 2.097.250/PR
- regras: R28
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.097.250/PR
- orgao: Terceira Turma
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2023-04-03
- publicacao: 2023-04-27
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1922832316
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Reafirma o Tema 1061 em financiamento bancário (financeira que sustentava a dificuldade de provar a assinatura, inclusive no contrato eletrônico, perdeu): a impugnação do consumidor transfere à instituição financeira o ônus de provar a autenticidade.
- observacao: Decisão colegiada curta; o voto não esmiúça os fatos. A "data de julgamento" é a do encerramento da sessão virtual (28/03 a 03/04/2023). Publicação pela data do Jusbrasil.

ementa:
> AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. PROCESSUAL CIVIL. ACÓRDÃO RECORRIDO PROFERIDO EM CONSONÂNCIA COM PRECEDENTE DA SEGUNDA SEÇÃO. TEMA 1.061/STJ. CONTRATOS BANCÁRIOS. DOCUMENTO PARTICULAR. IMPUGNAÇÃO DA AUTENTICIDADE DA ASSINATURA. ÔNUS DA PROVA. CONSUMIDOR IMPUGNOU A AUTENTICIDADE. ÔNUS DA PROVA DA INSTITUIÇÃO FINANCEIRA. RAZÕES QUE NÃO INFIRMAM A DECISÃO AGRAVADA. AGRAVO INTERNO DESPROVIDO.

### STJ · AREsp 3.200.826/SC
- regras: R28
- posicao: ADV
- tribunal: STJ
- classe_numero: AREsp 3.200.826/SC
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2026-06-15
- publicacao: 2026-06-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6799384329
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Limite da tese: o ônus é da instituição financeira, mas ela pode cumpri-lo por qualquer meio idôneo; perícia grafotécnica não é obrigatória, e a conclusão das instâncias ordinárias sobre a suficiência das provas esbarra na Súmula 7. A inicial deve impugnar a assinatura de forma específica e requerer a perícia.
- observacao: Recurso da consumidora não conhecido; o acórdão cita julgados da Terceira Turma de 2025 na mesma linha (AREsp 2.952.820/MA, REsp 2.101.394/SP, AREsp 2.794.525/GO). Publicação pela data do Jusbrasil.

ementa:
> PROCESSUAL CIVIL E CONSUMIDOR. AGRAVO EM RECURSO ESPECIAL. CONTRATO BANCÁRIO. IMPUGNAÇÃO DE ASSINATURA. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. ARTS. 1.022 E 489 DO CPC. NÃO OCORRÊNCIA. ÔNUS DA PROVA DA AUTENTICIDADE. TEMA 1.061/STJ. COMPROVAÇÃO POR MEIOS IDÔNEOS DIVERSOS DA PERÍCIA GRAFOTÉCNICA. REEXAME FÁTICO-PROBATÓRIO. SÚMULA 7/STJ. 1. Agravo em recurso especial contra decisão que inadmitiu recurso especial em ação envolvendo contrato bancário, com impugnação de assinatura. 2. O objetivo recursal é decidir se (i) houve negativa de prestação jurisdicional; (ii) é indispensável perícia grafotécnica à luz do ônus probatório fixado no Tema 1.061/STJ; (iii) é possível modificar, em recurso especial, as premissas fáticas sobre a regularidade da contratação. 3. Não se configura negativa de prestação jurisdicional quando o acórdão enfrenta de modo suficiente as questões essenciais. 4. O ônus de provar a autenticidade da assinatura, quando impugnada, recai sobre a instituição financeira, podendo ser cumprido por qualquer meio idôneo, não se exigindo, necessariamente, perícia grafotécnica. 5. Formada a convicção pela instância ordinária com base no conjunto probatório, a revisão demanda reexame de fatos e provas, inviável em recurso especial, nos termos da Súmula 7/STJ. 6. Agravo conhecido para não conhecer do recurso especial.

### TJSP · Apelação Cível 1024731-89.2023.8.26.0405
- regras: R28
- posicao: FAV
- tribunal: TJSP
- classe_numero: Apelação Cível 1024731-89.2023.8.26.0405
- orgao: 20ª Câmara de Direito Privado
- relator: Des.ª Lidia Regina Rodrigues Monteiro Cabrini
- julgamento: 2025-04-09
- publicacao: 2025-04-09
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-sp/3398910362
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Impugnada a assinatura do empréstimo consignado, cabia ao banco provar a autenticidade (art. 429, II, CPC; Tema 1061); a perícia mostrou divergência das assinaturas, e o banco foi condenado (inexistência do contrato, restituição e dano moral).
- observacao: Faltou no TJPR: os acórdãos de Câmara Cível do TJPR que aplicam o Tema 1061 a favor do consumidor voltaram do fetch sem o texto da ementa e, pela regra de seleção, não entraram (ver relatório). Data de publicação igual à do julgamento (data do Jusbrasil).

ementa:
> DIREITO DO CONSUMIDOR. APELAÇÃO CÍVEL. EMPRÉSTIMO CONSIGNADO. IMPUGNAÇÃO DE AUTENTICIDADE DA ASSINATURA. ÔNUS DA PROVA DA INSTITUIÇÃO FINANCEIRA. PERÍCIA GRAFOTÉCNICA. FRAUDE COMPROVADA. INEXISTÊNCIA DE RELAÇÃO JURÍDICA. DANOS MORAIS. RESPONSABILIDADE OBJETIVA DO BANCO. RECURSO DESPROVIDO. I. Caso em exame Apelação interposta contra sentença que declarou a inexistência do contrato de empréstimo consignado e condenou a instituição financeira à restituição dos valores descontados indevidamente do benefício previdenciário da autora, com correção monetária e juros, além do pagamento de indenização por danos morais no valor de R$ 8.000,00. A sentença ainda determinou o pagamento de custas, despesas processuais e honorários advocatícios pela parte ré. A instituição financeira sustenta a regularidade da contratação e requer a improcedência total da ação, alegando inexistência de dever de indenizar. II. Questão em discussão A questão em discussão consiste em verificar a validade da contratação do empréstimo consignado impugnado, bem como a responsabilidade da instituição financeira pelos descontos indevidos e a consequente obrigação de indenizar por danos morais. III. Razões de decidir A relação jurídica em questão envolve prestação de serviços bancários, aplicando-se o Código de Defesa do Consumidor (Súmula 297 /STJ). Nos termos do art. 429, II, do CPC, cabia à instituição financeira a prova da autenticidade da assinatura do contrato impugnado. A perícia grafotécnica constatou a divergência das assinaturas, evidenciando a falsidade documental e a inexistência de relação jurídica válida. O entendimento consolidado pelo Tema 1.061 /STJ atribui à instituição financeira o ônus da prova quanto à autenticidade do contrato bancário impugnado. A instituição financeira responde objetivamente pelos danos causados por falha na segurança de suas operações, nos termos do art. 14 do CDC e da Súmula 479 do STJ. O dano moral, em casos de descontos indevidos sobre benefício previdenciário, verba de caráter alimentar, é presumido (dano "in re ipsa", não se exigindo comprovação do sofrimento pela parte prejudicada. O valor da indenização por danos morais fixado em R$ 8.000,00 mostra-se adequado, considerando a extensão do dano, a capacidade econômica das partes e o caráter pedagógico da condenação, ausente pedido de redução. Diante do improvimento do recurso, impõe-se a majoração dos honorários advocatícios recursais, nos termos do art. 85, § 11, do CPC . IV. Dispositivo e tese Recurso desprovido. Tese de julgamento: 1. A impugnação da autenticidade de assinatura contratual impõe à instituição financeira o ônus de comprovar sua validade, nos termos do art. 429, II, do CPC e do Tema 1.061 /STJ. 2. A falha na segurança dos serviços bancários configura responsabilidade objetiva da instituição financeira, nos termos do art. 14 do CDC . 3. O desconto indevido em benefício previdenciário caracteriza dano moral in re ipsa, sendo devida a reparação. Legislação relevante: CDC, art. 14; CPC, art. 429, II; CC, art. 406, § 1º e § 3º (redação dada pela Lei 14.905/2024). Jurisprudência relevante: STJ, Súmulas 297 e 479; STJ, Tema 1.061.

### TJPR · Apelação Cível 0000247-23.2024.8.16.0194
- regras: R28
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0000247-23.2024.8.16.0194
- orgao: 4ª Câmara Cível
- relator: Des.ª Astrid Maranhão de Carvalho Ruthes
- julgamento: 2026-06-29
- publicacao: 2026-06-30
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038150851/Ac%C3%B3rd%C3%A3o-0000247-23.2024.8.16.0194
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Impugnada a assinatura, cabe ao banco prová-la por prova técnica (Tema 1.061/STJ); sem ela, declara-se inexistente a relação jurídica e inexigível o débito. Assinatura eletrônica sem elementos mínimos de identificação e autenticação não valida o contrato.
- observacao: Embargos à execução de financiamento de veículo; o banco desistiu da perícia grafotécnica. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E DIREITO DO CONSUMIDOR. EMBARGOS À EXECUÇÃO. APELAÇÃO CÍVEL. AUTENTICIDADE DE ASSINATURA EM CONTRATO BANCÁRIO. ÔNUS DA PROVA INSTITUIÇÃO BANCÁRIA. NÃO SE DESINCUMBIU DO ÔNUS. TEMA REPETITIVO Nº 1.061, DO COLENDO SUPERIOR TRIBUNAL DE JUSTIÇA. NECESSIDADE DE REALIZAÇÃO DE PERÍCIA GRAFOTÉCNICA. RECURSO DE APELAÇÃO CONHECIDO E NÃO PROVIDO.
> I. CASO EM EXAME
> 1. Apelação cível interposta por instituição financeira em face da sentença que julga procedentes os embargos à execução, reconhecendo a inexistência da relação jurídica decorrente de contrato de financiamento de veículo, em razão da impugnação da autenticidade da assinatura constante no contrato e da ausência de comprovação por meio de prova técnica. A apelante busca a reforma da decisão para reconhecer a validade do contrato e o prosseguimento da execução.
> II. QUESTÃO EM DISCUSSÃO
> 2. A questão em discussão consiste em averiguar caso a instituição financeira comprovou a autenticidade da assinatura constante no contrato de financiamento, sendo a falsidade impugnada, para fins de validade da relação jurídica bancária e exigibilidade do débito objeto da execução.
> III. RAZÕES DE DECIDIR
> 3. A instituição financeira não comprovou a autenticidade da assinatura constante no contrato de financiamento, ônus que lhe competia conforme o Tema 1.061 do STJ.
> 4. A ausência de perícia grafotécnica, aliada à desistência da parte apelante em produzi-la, impossibilitou a comprovação da veracidade da assinatura.
> 5. A sentença aplicou corretamente a inversão do ônus da prova, reconhecendo a inexistência da relação jurídica e a inexigibilidade do débito executado.
> 6. A assinatura eletrônica apresentada não possui elementos técnicos mínimos de identificação e autenticação válidos, comprometendo a validade do contrato.
> 7. Diante da ausência de prova válida da contratação, a manutenção da sentença é medida que se impõe.
> IV. DISPOSITIVO E TESE
> 8. Recurso de apelação cível conhecida e não provido.
> Tese de julgamento: Impõe-se à instituição financeira o ônus de comprovar a autenticidade da assinatura constante em contrato bancário quando esta for impugnada pela parte contrária, sendo necessária prova técnica adequada para validar o negócio jurídico, sob pena de reconhecimento da inexistência da relação jurídica e da inexigibilidade do débito executado.

### TJPR · Apelação Cível 0013187-92.2022.8.16.0031
- regras: R28
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0013187-92.2022.8.16.0031
- orgao: 13ª Câmara Cível
- relator: Des.ª Rosana Andriguetto de Carvalho
- julgamento: 2025-08-01
- publicacao: 2025-08-01
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000033333791/Ac%C3%B3rd%C3%A3o-0013187-92.2022.8.16.0031
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O TJPR mantém a nulidade de empréstimo consignado cuja assinatura foi impugnada e o banco não provou (CPC, art. 429, II; Tema 1.061/STJ), com dano moral e multa por litigância de má-fé imposta ao banco.
- observacao: O banco deixou precluir a perícia grafotécnica. Devolução conforme a modulação do EAREsp 676.608/RS. Fonte: portal de jurisprudência do TJPR (comarca de Guarapuava).

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE INDENIZAÇÃO POR DANO MORAL E MATERIAL. CONTRATO DE EMPRÉSTIMO CONSIGNADO. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSO DO BANCO RÉU. PRETENSÃO DE RECONHECIMENTO DA REGULARIDADE DA CONTRATAÇÃO. NÃO OCORRÊNCIA. IMPUGNAÇÃO À AUTENTICIDADE DA ASSINATURA DO CONTRATO APRESENTADO. ÔNUS DO BANCO DE PROVAR A VERACIDADE. INTELIGÊNCIA DO ART. 429, II, DO CPC E DO TEMA 1.061 DO STJ. PRECLUSÃO QUANTO A SOLICITAÇÃO DE PERÍCIA GRAFOTÉCNICA. AUSÊNCIA DE PROVA HÁBIL QUANTO A AUTENTICIDADE DA ASSINATURA DA PARTE NO CONTRATO. NULIDADE DO CONTRATO MANTIDA. DEVOLUÇÃO DOS VALORES COBRADOS QUE DEVE SE DAR DE ACORDO COM A MODULAÇÃO DOS EFEITOS DO EARESP 676.608 DO STJ, SOB PENA DE REFORMATIO IN PEJUS. DANO MORAL CONFIGURADO. VALORES RECEBIDOS PELO AUTOR QUE FORAM DEPOSITADOS EM JUÍZO. IMPOSSIBILIDADE DE REDUÇÃO DO QUANTUM INDENIZATÓRIO. PRECEDENTES DESTA CORTE. TERMO INICIAL JUROS DE MORA. EVENTO DANOSO. SÚMULA Nº 54 DO STJ. FALHA NA PRESTAÇÃO DOS SERVIÇOS. PRETENSÃO DE AFASTAMENTO DA MULTA POR LITIGÂNCIA DE MÁ-FÉ. COMPORTAMENTO CONTRADITÓRIO DA INSTITUIÇÃO FINANCEIRA. MANUTENÇÃO DA CONDENAÇÃO EM MULTA POR LITIGÂNCIA DE MÁ-FÉ. ALTERAÇÃO DA VERDADE DOS FATOS E DEMANDA INFUNDADA. ARTIGO 80, INCISOS II E VI DO CPC. PREQUESTIONAMENTO DA MATÉRIA. EXPRESSA MENÇÃO DOS DISPOSITIVOS LEGAIS CONSIDERADOS VIOLADOS. DISPENSABILIDADE. PRECEDENTE DO STJ. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS FIXADOS. RECURSO DO BANCO RÉU CONHECIDO E NÃO PROVIDO.

## R29 — Comissão "flat" sem contraprestação de serviço autônomo

Tese: A comissão "flat" (percentual sobre o crédito a título de assessoria ou estruturação) é indevida quando não há contraprestação de serviço autônomo e efetivamente prestado, distinto da intermediação financeira já remunerada pelos juros, por abusividade (CDC, art. 51, IV) e ofensa à boa-fé e ao enriquecimento sem causa (CC, arts. 422 e 884).

Sem entrada verificada nesta onda. Base analógica: REsp 1.578.553/SP, tese 2.3.1, listado sob R09. Panorama e lacunas no Relatório.

## R34 — SFH: capitalização de juros vedada em qualquer periodicidade

Tese: Nos contratos do Sistema Financeiro da Habitação anteriores à Lei 11.977/2009 é vedada a capitalização de juros em qualquer periodicidade, ainda que pactuada (Decreto 22.626/1933, art. 4º; Súmula 121/STF); se a Tabela Price a produz, o excesso deve ser apurado por perícia e expurgado.

### STJ · REsp 1.070.297/PR
- regras: R34
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.070.297/PR
- orgao: Segunda Seção
- relator: Min. Luis Felipe Salomão
- julgamento: 2009-09-09
- publicacao: 2009-09-18
- precedente_qualificado: repetitivo (art. 543-C do CPC/1973); o número do Tema não consta do texto aberto
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106319445
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case: nos contratos do SFH é vedada a capitalização de juros em qualquer periodicidade.
- observacao: Traz o LIMITE na mesma tese: o STJ não afere se a Tabela Price capitaliza (Súmulas 5 e 7), então o anatocismo tem de ser provado nas instâncias ordinárias (perícia). CUIDADO com o fundamento: a vedação vem, no voto, da jurisprudência do STJ, da Súmula 121/STF e do art. 4º do Decreto 22.626/33; o art. 6º, "e", da Lei 4.380/64 foi lido neste mesmo julgado como NÃO limitando juros remuneratórios (tese 1.2). Não citar o art. 6º, "c" e "e", da Lei 4.380/64 como fundamento da vedação. O voto registra que a Lei 11.977/2009 (art. 15-A da Lei 4.380/64) passou a permitir a capitalização mensal no SFH; a tese vale para contratos anteriores. A publicação consta como DJe 18/09/2009 no cabeçalho do inteiro teor.

ementa:
> RECURSO ESPECIAL REPETITIVO. SISTEMA FINANCEIRO DA HABITAÇÃO. CAPITALIZAÇÃO DE JUROS VEDADA EM QUALQUER PERIODICIDADE. TABELA PRICE. ANATOCISMO. INCIDÊNCIA DAS SÚMULAS 5 E 7. ART. 6º, ALÍNEA E, DA LEI Nº 4.380/64. JUROS REMUNERATÓRIOS. AUSÊNCIA DE LIMITAÇÃO.
> 1. Para efeito do art. 543-C:
> 1.1. Nos contratos celebrados no âmbito do Sistema Financeiro da Habitação, é vedada a capitalização de juros em qualquer periodicidade. Não cabe ao STJ, todavia, aferir se há capitalização de juros com a utilização da Tabela Price, por força das Súmulas 5 e 7.
> 1.2. O art. 6º, alínea e, da Lei nº 4.380/64, não estabelece limitação dos juros remuneratórios.
> 2. Aplicação ao caso concreto:
> 2.1. Recurso especial parcialmente conhecido e, na extensão, provido, para afastar a limitação imposta pelo acórdão recorrido no tocante aos juros remuneratórios.

### STJ · REsp 2.168.394/SP
- regras: R34
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.168.394/SP
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2025-11-24
- publicacao: 2025-12-03
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/5901055192
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: a simples adoção da Tabela Price não prova anatocismo; a capitalização indevida depende de prova (taxa pactuada x aplicada) e o STJ não reexamina (Súmulas 5 e 7).
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Raul Araújo, Quarta Turma, sessão virtual de 18/11/2025 a 24/11/2025 (julgamento fixado em 24/11/2025, data de encerramento da sessão e do termo de julgamento), DJEN de 03/12/2025; votaram com o relator Gallotti, Antonio Carlos Ferreira, Buzzi e Noronha. O STJ reformou o TJSP, que havia afastado a Tabela Price "a priori" como anatocismo; o acórdão também mantém a exclusão do CES sem previsão contratual (sem relevância para R34) e aplica as Súmulas 450 e 454. Não serve como FAV: o resultado no ponto foi contrário ao mutuário.

ementa:
> DIREITO BANCÁRIO. RECURSO ESPECIAL. SISTEMA FINANCEIRO DA HABITAÇÃO. REVISÃO DE CONTRATO. TABELA PRICE. PARCIAL PROVIMENTO.
> 1. A jurisprudência do Superior Tribunal de Justiça é pacífica no sentido de que a mera utilização da Tabela Price como sistema de amortização não implica, por si só, capitalização de juros (anatocismo). A verificação de eventual capitalização indevida depende da análise da taxa de juros pactuada e da efetivamente aplicada, o que demandaria reexame de provas e do contrato, vedado pelas Súmulas 5 e 7/STJ.
> 2. A exclusão do Coeficiente de Equiparação Salarial (CES) foi correta, pois não havia previsão contratual expressa nem previsão legal à época da celebração do contrato, conforme entendimento consolidado do STJ.
> 3. A utilização da Taxa Referencial (TR) como indexador do saldo devedor é válida, conforme previsto na Lei 8.177/91 e na Súmula 454/STJ, não havendo sucumbência nesse ponto que justifique o interesse recursal do recorrente.
> 4. Recurso especial parcialmente provido, para reconhecer a legalidade da utilização da Tabela Price como sistema de amortização, restabelecendo o pactuado entre as partes nesse ponto.

### STJ · REsp 2.103.041/DF
- regras: R34
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.103.041/DF
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2026-04-13
- publicacao: 2026-04-16
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6614581061
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva da peça, com saída processual: a Tabela Price não gera juros sobre juros por si só, mas a existência de anatocismo é questão de fato e exige perícia contábil; indeferi-la é cerceamento de defesa.
- observacao: Dados antes [CONFERIR] agora conferidos: relatora Min. Maria Isabel Gallotti, Quarta Turma, sessão virtual de 07/04/2026 a 13/04/2026 (julgamento em 13/04/2026), unânime; votaram Antonio Carlos Ferreira, Luís Carlos Gambogi (Des. convocado TJMG), Noronha e Raul Araújo. Publicação pela data do Jusbrasil (16/04/2026). Recurso da construtora desprovido: o STJ manteve a anulação da sentença de improcedência liminar e o retorno para perícia. A ementa fala do SFH, mas o contrato do caso é de compra e venda com alienação fiduciária feita com construtora fora do SFN/SFH/SFI; no voto, a relatora cita o Tema 572/STJ e reafirma, com AgInt nos EDcl no REsp 2.060.160/RN, AgInt no REsp 1.905.596/PR e AgInt no AREsp 2.519.062/DF, que construtora fora do SFI não pode cobrar juros capitalizados (aproveitável na R35, mas esse ponto não está na ementa). Aqui há duas entradas ADV na R34 (acima do teto de 1 da regra de seleção) porque o pedido incluía conferir os dois REsp.

ementa:
> RECURSO ESPECIAL. TABELA PRICE. ANATOCISMO. PERÍCIA CONTÁBIL NECESSÁRIA. ANULAÇÃO DA SENTENÇA PARA REALIZAÇÃO DE PERÍCIA MANTIDA.
> 1. A utilização do Sistema Francês de Amortização, Tabela Price, para o cálculo das prestações não é ilegal e não enseja, por si só, a incidência de juros sobre juros.
> 2. Esta Corte, no julgamento de recurso submetido ao regime do art. 543-C do CPC/1973, assentou a impossibilidade de o STJ analisar a existência de capitalização de juros com a utilização da Tabela Price, em razão da incidência das Súmulas n. 5 e 7 do STJ (REsp n. 1.070.297/PR, Relator Ministro LUIS FELIPE SALOMÃO, SEGUNDA SEÇÃO, julgado em 9/9/2009, DJe 18/9/2009).
> 3. Em se verificando que matérias de fato ou eminentemente técnicas foram tratadas como exclusivamente de direito, reconhece- se o cerceamento, para que seja realizada a prova pericial. Decisão do Tribunal de origem em consonância com o entendimento do STJ.
> 4. Recurso especial conhecido e não provido.

## R35 — SFI e imobiliário fora do SFN: capitalização inferior à anual vedada

Tese: Nos contratos de compra e venda de imóvel com financiamento direto da construtora, incorporadora ou loteadora, ou no SFI (Lei 9.514/1997), a capitalização de juros em periodicidade inferior à anual é vedada mesmo se pactuada (Decreto 22.626/1933, art. 4º; Código Civil, art. 591); a MP 2.170-36/2001, a Súmula 539 e os Temas 246 e 247 do STJ não alcançam o SFI nem quem não integra o SFN.

### STJ · AgInt no AREsp 2.738.974/MG
- regras: R35
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.738.974/MG
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2025-04-28
- publicacao: 2025-05-06
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6580169537
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Contrato de compra e venda de imóvel com instituição fora do SFI não admite juros capitalizados em periodicidade inferior à anual.
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Raul Araújo, Quarta Turma, sessão virtual de 22/04/2025 a 28/04/2025 (julgamento em 28/04/2025), unânime; votaram Noronha, Gallotti, Antonio Carlos Ferreira e Buzzi. Publicação pela data do Jusbrasil. O relator reconsiderou decisão monocrática anterior que dera provimento ao recurso da incorporadora e negou provimento ao recurso especial dela, aplicando a Súmula 83/STJ; o acórdão de origem (TJMG, IRDR Tema 56) admitia só a capitalização anual. O voto transcreve a ementa do REsp 2.086.650/MG (Nancy Andrighi, 3ª Turma), que é o leading case da 3ª Turma, mas este não entra como entrada própria (ver Relatório).

ementa:
> CIVIL E PROCESSUAL CIVIL. AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. DECISÃO MONOCRÁTICA. RECONSIDERAÇÃO. AÇÃO REVISIONAL. PROMESSA DE COMPRA E VENDA DE IMÓVEL. SISTEMA DE FINANCIAMENTO IMOBILIÁRIO. CAPITALIZAÇÃO DE JUROS. PERIODICIDADE INFERIOR À ANUAL. INVIABILIDADE. CONSONÂNCIA DO ACÓRDÃO RECORRIDO COM A JURISPRUDÊNCIA DESTA CORTE. SÚMULA 83/STJ. AGRAVO INTERNO PROVIDO. AGRAVO EM RECURSO ESPECIAL CONHECIDO. RECURSO ESPECIAL DESPROVIDO.
> 1. Em se tratando de contrato de compra e venda de imóvel pactuado com instituição não integrante do Sistema Financeiro Imobiliário, não há que se falar na legalidade da cobrança de juros capitalizados em periodicidade inferior à anual. Precedentes.
> 2. O entendimento adotado no acórdão recorrido coincide com a jurisprudência assente desta Corte Superior, circunstância que atrai a incidência da Súmula 83/STJ.
> 3. Agravo interno provido para reconsiderar a decisão agravada e, em novo julgamento, conhecer do agravo para negar provimento ao recurso especial.

### STJ · AgInt nos EDcl no AREsp 3.050.638/SE
- regras: R35
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt nos EDcl no AREsp 3.050.638/SE
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2026-06-15
- publicacao: 2026-06-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6618178711
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: A capitalização mensal em promessa de compra e venda com construtora fora do SFN/SFI é vedada ainda que pactuada, por falta de autorização legal específica; a Tabela Price que a produz, apurada em perícia, autoriza a rescisão sem retenção.
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Raul Araújo, Quarta Turma, sessão virtual de 09/06/2026 a 15/06/2026 (julgamento em 15/06/2026), unânime; votaram Gallotti, Antonio Carlos Ferreira, Luís Carlos Gambogi (Des. convocado TJMG) e Noronha. Publicação pela data do Jusbrasil. A existência de pactuação expressa e a prova pericial ficaram fora do alcance do STJ (Súmulas 5 e 7); o ponto de direito é a vedação à construtora.

ementa:
> DIREITO DO CONSUMIDOR. AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. PROMESSA DE COMPRA E VENDA DE IMÓVEL. TABELA PRICE. CAPITALIZAÇÃO DE JUROS POR CONSTRUTORA NÃO INTEGRANTE DO SFN/SFI. SÚMULAS 83, 5 E 7/STJ. AGRAVO CONHECIDO E RECURSO ESPECIAL DESPROVIDO.
> 1. A jurisprudência do STJ veda a capitalização mensal de juros em contratos de promessa de compra e venda firmados com construtoras não integrantes do SFN/SFI, ainda que pactuada, por ausência de autorização legal específica.
> 2. O acórdão recorrido está em consonância com a orientação consolidada do STJ, incidindo a Súmula 83/STJ e preservando a rescisão contratual sem retenção, diante da índole abusiva constatada pericialmente.
> 3. A revisão da existência de pactuação expressa de capitalização mensal e a reapreciação das cláusulas contratuais e provas periciais esbarram nos óbices das Súmulas 5 e 7/STJ, inviáveis em recurso especial.
> 4. O agravo interno é conhecido após reconsideração nos termos do art. 259 do RISTJ, sem alteração do resultado quanto ao mérito do recurso especial.
> 5. Agravo interno conhecido para negar provimento ao recurso especial.

### TJSC · Apelação 5002346-56.2021.8.24.0033
- regras: R35
- posicao: FAV
- tribunal: TJSC
- classe_numero: Apelação 5002346-56.2021.8.24.0033
- orgao: Sétima Câmara de Direito Civil
- relator: Des. Carlos Roberto da Silva (nome conforme a citação do próprio acórdão na busca do Jusbrasil; o texto do fetch omite o relator)
- julgamento: 2025-05-29
- publicacao: 2025-05-29
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-sc/3944222624
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Incorporadora fora do SFI não pode cobrar juros capitalizados; a Tabela Price que capitaliza, constatada por perícia contábil, é nula e as parcelas são recalculadas na liquidação.
- observacao: Complementa os três acórdãos do TJPR desta tese: aqui a perícia constatou a capitalização e a sentença mandou recalcular as parcelas. Publicação pela data do Jusbrasil (29/05/2025). O texto do fetch também traz a ata da sessão virtual de 29/05/2025 (7ª Câmara de Direito Civil, unânime). Contrato de promessa de compra e venda de apartamento em construção com incorporadora (SPE), não com banco.

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE REVISÃO DE CONTRATO. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA DO AUTOR. PROMESSA DE COMPRA E VENDA DE APARTAMENTO EM CONSTRUÇÃO. TESE EXORDIAL DE CAPITALIZAÇÃO DE JUROS. DEFENDIDA A COBRANÇA ABUSIVA DE ENCARGOS FINANCEIROS. ACOLHIMENTO. RÉ NÃO INTEGRANTE DO SISTEMA FINANCEIRO IMOBILIÁRIO (SFI). IMPOSSIBILIDADE DE UTILIZAÇÃO DAS PRERROGATIVAS PREVISTAS NA LEI N. 9.514/1997. CAPITALIZAÇÃO DE JUROS CONSTATADA POR PERÍCIA CONTÁBIL. PRÁTICA ABUSIVA EVIDENCIADA. APURAÇÃO DO VALOR DE CADA PARCELA A SER FEITA EM FASE DE LIQUIDAÇÃO DE SENTENÇA. INVERSÃO DOS ÔNUS SUCUMBENCIAIS. "'[...] em se tratando de contratos de compra e venda de imóvel, somente é permitida a capitalização dos juros quando o financiamento for pactuado com entidade bancária que respeite as normas do Sistema Financeiro Imobiliário, não se enquadrando nessas hipóteses as construtoras de imóveis, as quais devem aplicar os juros na forma simples' (Apelação Cível n. 2014.065045-1, da Capital, rel. Des. Saul Steil, j. 16-12-2014)" (TJSC, Apelação n. 5004719-75.2020.8.24.0007, rel. Des., Quarta Câmara de Direito Civil, j. 3-4-2025). RECURSO CONHECIDO E PROVIDO.

### TJPR · Apelação Cível 0025314-12.2019.8.16.0017
- regras: R35
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0025314-12.2019.8.16.0017
- orgao: 19ª Câmara Cível
- relator: Juiz Subst. 2º Grau Osvaldo Canela Junior
- julgamento: 2024-02-26
- publicacao: 2024-02-26
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000024931151/Ac%C3%B3rd%C3%A3o-0025314-12.2019.8.16.0017
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: A loteadora não se equipara a instituição financeira e não pode capitalizar juros em periodicidade inferior à anual (MP 2.170-36/2001, art. 5º) no financiamento direto de imóvel; a perícia constatou a capitalização pela Tabela Price.
- observacao: Ação de resolução contratual por culpa da vendedora; o ponto da capitalização é o item 1 da ementa. Fonte: portal de jurisprudência do TJPR (comarca de Maringá).

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE RESOLUÇÃO CONTRATUAL. PROMESSA DE COMPRA E VENDA DE IMÓVEL. SENTENÇA DE PARCIAL PROCEDÊNCIA DOS PEDIDOS. FINANCIAMENTO FEITO DIRETAMENTE PELA LOTEADORA. PROVA PERICIAL CONTÁBIL. TABELA PRICE. UTILIZAÇÃO DE CAPITALIZAÇÃO MENSAL DE JUROS. VEDAÇÃO. CULPA EXCLUSIVA DA PROMITENTE VENDEDORA. IMPOSSIBILIDADE DE RETENÇÃO DA COMISSÃO DE CORRETAGEM E DA TAXA DE PUBLICIDADE. SÚMULA 543 DO STJ. RESTITUIÇÃO INTEGRAL DAS PARCELAS PAGAS PELOS PROMISSÁRIOS COMPRADORES. DECISÃO MANTIDA. RECURSO CONHECIDO E DESPROVIDO.1. As loteadoras não se equiparam às instituições financeiras, não se lhes estendendo a autorização para utilização da capitalização mensal de juros, a que se refere o artigo 5º da Medida Provisória 2.170-36, de 23 de agosto de 2001, nos contratos de financiamento imobiliário com periodicidade inferior a um ano.2. Em caso de resolução do contrato por culpa do promitente vendedor, a restituição das parcelas pagas pelo promissário comprador deve ser integral, o que abrange a comissão de corretagem e a taxa de publicidade.3. Recurso conhecido e desprovido.

### TJPR · Apelação Cível 0009749-25.2021.8.16.0021
- regras: R35
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0009749-25.2021.8.16.0021
- orgao: 20ª Câmara Cível
- relator: Des.ª Angela Khury
- julgamento: 2025-02-11
- publicacao: 2025-02-13
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000027374321/Ac%C3%B3rd%C3%A3o-0009749-25.2021.8.16.0021
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Em promessa de compra e venda de lote com financiamento da vendedora, o TJPR afirma a impossibilidade da capitalização mensal e reconhece, pela perícia, juros capitalizados sem previsão contratual.
- observacao: Favorável só na tese: o comprador estava em mora e havia saldo devedor, por isso não houve repetição nem descaracterização da mora, e a multa compensatória foi reduzida a 10%. Fonte: portal de jurisprudência do TJPR (comarca de Cascavel).

ementa:
> APELAÇÃO. AÇÃO REVISIONAL DE CONTRATO DE PROMESSA DE COMPRA E VENDA DE IMÓVEL. LOTEAMENTO “RESIDENCIAL SIENA”. APLICAÇÃO DO CÓDIGO DE DEFESA DO CONSUMIDOR. POSSIBILIDADE DE REVISÃO CONTRATUAL. CAPITALIZAÇÃO DE JUROS QUE DEPENDE DE PREVISÃO CONTRATUAL, QUALQUER QUE SEJA A SUA PERIODICIDADE. IMPOSSIBILIDADE DE CAPITALIZAÇÃO MENSAL DE JUROS NO CASO DE CONTRATO PARA AQUISIÇÃO DE IMÓVEL. ENTENDIMENTO DO STJ. PERÍCIA CONCLUIU QUE HOUVE JUROS CAPITALIZADOS SEM A EXPRESSA PREVISÃO CONTRATUAL. EXISTÊNCIA DE SALDO DEVEDOR. AUTOR QUE DESDE A PRIMEIRA PARCELA ATRASOU PAGAMENTOS. DEVIDA COMPENSAÇÃO DE VALORES ANTE O ATRASO NO PAGAMENTO DE PARCELAS. CÁLCULO DO PERITO NOS ESTRITOS TERMOS DO CONTRATO E QUE DEVE PREVALECER. EXISTÊNCIA DE SALDO DEVEDOR QUE IMPEDE A REPETIÇÃO DE VALORES E A DESCARACTERIZAÇÃO DA MORA. NECESSIDADE DE AJUIZAMENTO DA AÇÃO QUE JUSTIFICA A APLICAÇÃO DE MULTA COMPENSATÓRIA. AUTOR ESTEVE EM MORA DURANTE GRANDE PARTE DA RELAÇÃO CONTRATUAL. PENALIDADE QUE DEVE SER REDUZIDA EM OBSERVÂNCIA AOS PRINCÍPIOS DA PROPORCIONALIDADE E RAZOABILIDADE. INTELIGÊNCIA DO ART. 413 DO CÓDIGO CIVIL. REDUÇÃO DA MULTA CONTRATUAL DE 20% PARA 10% SOBRE O PREÇO TOTAL DO IMÓVEL, FACULTADA A COMPENSAÇÃO COM O SALDO DEVEDOR. IMPOSSIBILIDADE DE CONDENAÇÃO DO AUTOR ÀS PENAS DE LITIGÂNCIA DE MÁ-FÉ. ART. 80 DO CPC. MANUTENÇÃO NA PORCENTAGEM DOS HONORÁRIOS ADVOCATÍCIOS EM 10%. REDISTRIBUIÇÃO DO ÔNUS DE SUCUMBÊNCIA ANTE O PARCIAL PROVIMENTO DO APELO. SEM HONORÁRIOS RECURSAIS. APELAÇÃO PARCIALMENTE CONHECIDA E, NESTA EXTENSÃO, PARCIALMENTE PROVIDA. SENTENÇA REFORMADA EM PARTE.

### TJPR · Apelação Cível 0004484-37.2023.8.16.0194
- regras: R35
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0004484-37.2023.8.16.0194
- orgao: 20ª Câmara Cível
- relator: Des. Rosaldo Elias Pacagnan
- julgamento: 2024-11-12
- publicacao: 2024-11-12
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000028467661/Ac%C3%B3rd%C3%A3o-0004484-37.2023.8.16.0194
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Empresa que não integra o Sistema Financeiro Imobiliário não pode capitalizar juros; havendo indício de Tabela Price, a perícia contábil é indispensável e o julgamento sem ela é cerceamento de defesa (Tema 572/STJ).
- observacao: Sentença cassada para a perícia; o mérito não foi julgado. Serve à vedação e ao pedido de perícia em "Das provas". Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE REVISÃO CONTRATUAL C/C REPETIÇÃO DE INDÉBITO. NEGÓCIO PARTICULAR DE COMPRA E VENDA DE IMÓVEL URBANO. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA RECURSAL DOS AUTORES (PROMISSÁRIOS COMPRADORES). PRELIMINAR DE CERCEAMENTO DE DEFESA PELO JULGAMENTO ANTECIPADO DA LIDE SEM A PRODUÇÃO DE PROVA TÉCNICA. Acolhimento. Matéria de fato relevante acerca da cobrança de juros remuneratórios e sua capitalização. Autores que assinaram apenas proposta de compra em que não eram previstos juros. Instrumentos contratuais outros, elaborados pela empresa ré, que não foram assinados. Relação típica de consumo. Documentos emitidos pela promitente vendedora sobre os pagamentos feitos que sinalizam para aplicação da Tabela Price como método de amortização da dívida e eventual capitalização. Prova pericial contábil que foi especificamente requerida por ambas as partes. Empresa ré que não integra o Sistema Financeiro Imobiliário. Capitalização de juros vedada na espécie, o que justifica a realização de perícia para sua confirmação e/ou afastamento. Tema Repetitivo nº 572 do Superior Tribunal de Justiça. Cassação da sentença e retorno dos autos à origem para regular instrução probatória, com a realização da perícia e a prévia definição quanto a extensão da inversão do ônus da prova incidentemente decretada. Demais questões prejudicadas. RECURSO CONHECIDO E PROVIDO.

## R39 — Alienação fiduciária (Lei 9.514, art. 26) e DL 70/66: intimação por edital só após esgotada a notificação pessoal

Tese: A intimação do devedor fiduciante para purgar a mora só pode ser feita por edital depois de esgotadas as tentativas de intimação pessoal (Lei 9.514/1997, art. 26, §§ 3º, 3º-A e 4º; DL 70/66, art. 31); a ciência da data dos leilões não supre a ausência de notificação válida e o vício anula a consolidação da propriedade e os atos seguintes.

### STJ · REsp 2.107.242/ES
- regras: R39
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.107.242/ES
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2026-08-12
- publicacao: 2026-08-17
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7330500615
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: A ciência da data dos leilões não supre a notificação válida para purgar a mora; edital só depois de esgotadas as tentativas de localização; o STJ anulou os atos posteriores e abriu novo prazo para purgar.
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Ricardo Villas Bôas Cueva, Terceira Turma, sessão virtual de 06/08/2026 a 12/08/2026 (julgamento em 12/08/2026), unânime; votaram Moura Ribeiro, Daniela Teixeira, Nancy Andrighi e Humberto Martins. Publicação pela data do Jusbrasil (17/08/2026). Caso de financiamento imobiliário da CEF no SFI, com acórdão do TRF2 reformado. Recurso especial provido; honorários invertidos.

ementa:
> RECURSO ESPECIAL. ALIENAÇÃO FIDUCIÁRIA. NOTIFICAÇÃO. EDITAL. TENTATIVAS. ESGOTADAS. PURGAÇÃO DA MORA. INTIMAÇÃO. LEILÕES. INSUFICIENTE. NULIDADE.
> 1. A controvérsia dos autos diz respeito a saber: (i) se houve negativa de prestação jurisdicional e (ii) se a regularidade na intimação acerca dos leilões supre a ausência de notificação válida para a purgação da mora.
> 2. A jurisprudência do Superior Tribunal de Justiça entende que a intimação para purgação da mora apenas pode ser realizada por edital quando esgotadas as tentativas de localização do devedor. Precedentes.
> 3. A ciência da data da realização dos leilões não é suficiente para suprir a ausência de notificação válida para a purgação da mora.
> 4. Recurso especial provido.

### STJ · AgInt no AREsp 2.925.916/MG
- regras: R39
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.925.916/MG
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2026-03-30
- publicacao: 2026-04-08
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6804558103
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Com a Lei 13.465/2017, a intimação pessoal exige ao menos duas tentativas no endereço do contrato, depois hora certa se houver suspeita de ocultação, e só então edital; sem isso, anula-se a consolidação e os atos seguintes.
- observacao: Sessão virtual de 24/03/2026 a 30/03/2026, unânime; votaram Gallotti, Antonio Carlos Ferreira, Luís Carlos Gambogi (Des. convocado TJMG) e Noronha. Publicação: DJEN de 08/04/2026 (confere com a data do Jusbrasil e com a citação deste acórdão no REsp 2.107.242/ES). ATENÇÃO: o termo de julgamento traz a marca "SEGREDO DE JUSTIÇA"; a ementa não identifica partes, mas confirmar se a citação em peça pública é conveniente. A certidão de oficial de cartório tem fé pública, mas não dispensa as etapas legais para presumir o devedor em local incerto.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. AGRAVO INTERNO NO RECURSO ESPECIAL. ALIENAÇÃO FIDUCIÁRIA DE IMÓVEL. INTIMAÇÃO PARA PURGAÇÃO DA MORA. NOTIFICAÇÃO POR EDITAL. NECESSIDADE DE ESGOTAMENTO DAS TENTATIVAS DE INTIMAÇÃO PESSOAL. CONSOLIDAÇÃO DA PROPRIEDADE E LEILÕES SUBSEQUENTES. AGRAVO INTERNO DESPROVIDO.
> 1. O art. 26, §§ 3º e 3º-A, da Lei 9.514/1997 dispõe que a intimação do devedor fiduciante para purgação da mora deve ser realizada prioritariamente de forma pessoal (por oficial de registro ou pelo correio com aviso de recebimento), com, ao menos, duas tentativas no endereço por ele fornecido, admitindo-se posteriormente a intimação por hora certa, em caso de suspeita de ocultação, e apenas em último caso a intimação por edital, quando o devedor estiver em local ignorado, incerto ou inacessível.
> 2. A jurisprudência do STJ entende que a intimação por edital, para fins de purgação da mora em contrato de alienação fiduciária de bem imóvel regido pela Lei 9.514/1997, pressupõe o esgotamento de todas as possibilidades de intimação pessoal do devedor.
> 3. No caso concreto, houve apenas uma diligência no endereço residencial constante do contrato e correspondente ao imóvel dado em garantia, uma diligência em endereço distinto e outra que nem sequer foi realizada porque o endereço fornecido era inexistente, sem comprovação de envio de carta registrada com aviso de recebimento e sem realização de intimação por hora certa, de modo que não se configurou o esgotamento das tentativas de intimação pessoal exigido pela lei e pela jurisprudência.
> 4. Reconhecido o vício da intimação para purgação da mora, impõe-se a anulação da consolidação da propriedade do imóvel em nome do credor fiduciário e dos atos subsequentes, nos termos da orientação firmada pelo Superior Tribunal de Justiça.
> 5. Agravo interno a que se nega provimento.

### STJ · REsp 1.698.322/RJ
- regras: R39
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.698.322/RJ
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2026-04-13
- publicacao: 2026-04-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6615347726
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: no rito do DL 70/66, frustrada a notificação pessoal, o edital é válido para a purgação da mora (art. 31, § 2º); a nulidade exige demonstrar que a notificação pessoal não foi esgotada.
- observacao: Dados conferidos: relatora Min. Maria Isabel Gallotti, Quarta Turma, sessão virtual de 07/04/2026 a 13/04/2026, DJEN de 23/04/2026 (consta no inteiro teor); impedido o Min. Antonio Carlos Ferreira. O STJ deu provimento aos recursos da CEF, da seguradora e da adquirente para restabelecer a sentença, reconhecendo a regularidade da execução extrajudicial. Julgado do DL 70/66 (hipoteca), não da Lei 9.514; o ponto da notificação por edital aparece no voto e no item 2 da ementa. Há também EDcl rejeitados em 2026-06-11.

ementa:
> RECURSOS ESPECIAIS. CIVIL. CONTRATOS DE MÚTUO E SEGURO. SISTEMA FINANCEIRO DA HABITAÇÃO. PRETENSÃO PAGAMENTO INDENIZAÇÃO SECURITÁRIA. PRESCRIÇÃO ÂNUA. EXECUÇÃO EXTRAJUDICIAL. DECRETO- LEI N. 70/1966. NOTIFICAÇÃO POR EDITAL. VALIDADE.
> 1. Aplica-se à pretensão de pagamento de indenização securitária pactuada de forma adjeta ao contrato de mútuo vinculado ao Sistema Financeiro da Habitação o prazo prescricional de um ano previsto no artigo 206, § 1º, inciso II, alínea b, do Código Civil, contado da ciência da invalidez permanente do segurado. Precedentes.
> 2. No procedimento do Decreto-lei n. 70/1966, frustrada a notificação pessoal do devedor, é válida a notificação por edital para a purgação da mora, nos termos do seu artigo 31, § 2º. Precedentes.
> 3. Recursos especiais providos.

### STJ · REsp 2.218.731/PE
- regras: R39
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.218.731/PE
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2025-10-20
- publicacao: 2025-10-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6267299175
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: o STJ reafirma que o edital só é legítimo quando frustrada a notificação pessoal, mas não reexamina se as diligências foram esgotadas (Súmula 7); quem alega o vício precisa prová-lo nas instâncias ordinárias.
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Humberto Martins, Terceira Turma, sessão virtual de 14/10/2025 a 20/10/2025 (acórdão datado de 21/10/2025), unânime; votaram Villas Bôas Cueva, Moura Ribeiro, Daniela Teixeira e Nancy Andrighi. Publicação pela data do Jusbrasil (23/10/2025). NÃO é favorável: o recurso foi NÃO CONHECIDO por Súmula 7 e o resultado manteve a retomada do imóvel pela CEF (TRF5; caso de gaveteiros e DL 70/66, com edital das datas de leilão considerado suficiente). Serve só como limite e como confirmação da tese de que o edital pressupõe notificação pessoal frustrada. Aqui há duas entradas ADV na R39 (acima do teto de 1) porque o pedido incluía conferir os dois REsp.

ementa:
> RECURSO ESPECIAL. CIENTIFICAÇÃO PESSOAL DO DEVEDOR. FRUSTRAÇÃO. TENTATIVAS. INTIMAÇÃO POR EDITAL. REEXAME DE PROVAS. INVIABILIDADE. SÚMULA N. 7/STJ.
> 1. Segundo entendimento consolidado nesta Corte, "no regime de execução extrajudicial do Decreto-Lei nº 70/1966, somente é legítima a publicação de edital, inclusive da realização do leilão, quando frustrada a tentativa de notificação pessoal do devedor por meio do Cartório de Título e Documentos" (EDcl no AREsp 963.818/MG, Rel. Ministro RICARDO VILLAS BÔAS CUEVA, TERCEIRA TURMA, julgado em 17/11/2016, DJe 24/11/2016).
> 2. A revisão do entendimento adotado pelo Tribunal de origem, a fim de averiguar se as diligências para a notificação extrajudicial do devedor fiduciário teriam sido efetivamente esgotadas, implicaria reexame de matéria fática, o que é vedado em recurso especial, conforme a Súmula n. 7 do STJ.
> Recurso especial não conhecido.

### TRF4 · Apelação Cível 5007831-90.2023.4.04.7200
- regras: R39
- posicao: FAV
- tribunal: TRF4
- classe_numero: Apelação Cível 5007831-90.2023.4.04.7200
- orgao: Décima Primeira Turma
- relator: Des. Federal Eliana Paggiarin Marinho
- julgamento: 2025-06-26
- publicacao: 2025-06-26
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/trf-4/4132554502
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: A intimação por edital só vale depois de esgotadas as tentativas de intimação pessoal em todos os endereços conhecidos, inclusive o do imóvel; sem isso a consolidação da propriedade é nula.
- observacao: Publicação pela data do Jusbrasil (26/06/2025, data da sessão virtual de 18 a 26/06/2025 e do acórdão). Apelação da CEF desprovida por unanimidade; a sentença que anulou a consolidação foi mantida. Primeira escolha no TRF4: faltou julgado do TJPR com ementa utilizável (o fetch do TJPR omite a ementa).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. ALIENAÇÃO FIDUCIÁRIA DE BEM IMÓVEL. CONSOLIDAÇÃO DA PROPRIEDADE. AUSÊNCIA DE NOTIFICAÇÃO NO ENDEREÇO DO IMÓVEL. NULIDADE DO PROCEDIMENTO. SENTENÇA MANTIDA.
> I. CASO EM EXAME
> 1. Apelação interposta contra sentença que declarou a nulidade da consolidação da propriedade fiduciária do imóvel e determinou a suspensão dos atos expropriatórios.
> II. QUESTÃO EM DISCUSSÃO
> 2. Há duas questões em discussão: (i) verificar a regularidade da intimação do devedor fiduciante para fins de purgação da mora; (ii) definir se a ausência de tentativa de notificação em todos os endereços conhecidos invalida o procedimento de consolidação da propriedade.
> III. RAZÕES DE DECIDIR
> 3. A intimação do devedor para purgação da mora é requisito essencial à validade do procedimento de consolidação da propriedade fiduciária, conforme o art. 26 da Lei 9.514/1997.
> 4. A intimação por edital somente é válida quando esgotadas todas as tentativas de intimação pessoal nos endereços conhecidos do devedor, hipótese não verificada nos autos.
> 5. O oficial do cartório diligenciou apenas dois dos três endereços informados, deixando de realizar tentativa de notificação no próprio imóvel objeto da alienação fiduciária.
> 6. A jurisprudência do TRF4 corrobora que a intimação por edital exige prévia tentativa frustrada de intimação pessoal em todos os endereços disponíveis.
> IV. DISPOSITIVO
> 7. Recurso desprovido.

### TRF4 · Apelação Cível 5003660-80.2020.4.04.7108
- regras: R39
- posicao: FAV
- tribunal: TRF4
- classe_numero: Apelação Cível 5003660-80.2020.4.04.7108
- orgao: Terceira Turma
- relator: Des. Federal Cândido Alfredo Silva Leal Junior
- julgamento: 2023-12-12
- publicacao: 2023-12-13
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/trf-4/3809450451
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: O edital para purgar a mora exige o esgotamento das diligências de notificação pessoal; endereço diverso do contrato e devolução do requerimento de edital pelo registro de imóveis levaram à nulidade da consolidação.
- observacao: Sessão presencial de 12/12/2023; publicação pela data do Jusbrasil (13/12/2023, data da assinatura). Apelação da CEF desprovida por unanimidade. A grafia mista (maiúsculas e minúsculas) da ementa é a do texto do fetch.

ementa:
> ADMINISTRATIVO. APELAÇÃO. ALIENAÇÃO FIDUCIÁRIA. NULIDADE DA CONSOLIDAÇÃO DA PROPRIEDADE. PURGAÇÃO DA MORA. NOTIFICAÇÃO EDITALÍCIA. NECESSIDADE DO ESGOTAMENTO DAS DILIGÊNCIAS. ART. 26, § 4º, DA LEI 9.514/97.
> 1. A intimação do interessado para purgar a mora (art. 26, § 1º) é o único procedimento previsto pela Lei nº 9.514/97 que exige notificação pessoal do mutuário.
> 2. Portanto, imprescindível, o esgotamento de diligências que justificasse a subsidiária intimação editalícia.
> 3. Apelação desprovida.

## PJ-VULN — Vulnerabilidade da PJ: finalismo mitigado

Tese: A pessoa jurídica que toma crédito bancário (capital de giro, cédula de crédito bancário, cédulas comercial e industrial) pode ser equiparada a consumidora (CDC, arts. 2º, 4º, I, e 29) quando demonstrar vulnerabilidade técnica, jurídica, fática, econômica ou informacional perante a instituição financeira (teoria finalista mitigada ou aprofundada), e a ação revisional deve ser julgada sob o CDC.

### STJ · REsp 1.195.642/RJ
- regras: PJ-VULN
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.195.642/RJ
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2012-11-13
- publicacao: 2012-11-21
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/22829799
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Leading case do finalismo aprofundado: a PJ não destinatária final pode ser equiparada a consumidora (art. 29 CDC) se demonstrar vulnerabilidade técnica, jurídica, fática ou informacional, inclusive por dependência ou natureza adesiva do contrato; a vulnerabilidade jurídica não se presume para a PJ e cabe a ela demonstrá-la.
- observacao: A tese foi fixada em abstrato, mas no caso concreto o STJ afastou o CDC por ausência de vulnerabilidade (revendedora de veículos e serviço de telefonia que compõe a cadeia produtiva); o acórdão não é de contrato bancário. Citar para o critério e para o ônus da prova, nunca como precedente de resultado.

ementa:
> CONSUMIDOR. DEFINIÇÃO. ALCANCE. TEORIA FINALISTA. REGRA. MITIGAÇÃO. FINALISMO APROFUNDADO. CONSUMIDOR POR EQUIPARAÇÃO. VULNERABILIDADE.
> 1. A jurisprudência do STJ se encontra consolidada no sentido de que a determinação da qualidade de consumidor deve, em regra, ser feita mediante aplicação da teoria finalista, que, numa exegese restritiva do art. 2º do CDC, considera destinatário final tão somente o destinatário fático e econômico do bem ou serviço, seja ele pessoa física ou jurídica.
> 2. Pela teoria finalista, fica excluído da proteção do CDC o consumo intermediário, assim entendido como aquele cujo produto retorna para as cadeias de produção e distribuição, compondo o custo (e, portanto, o preço final) de um novo bem ou serviço. Vale dizer, só pode ser considerado consumidor, para fins de tutela pela Lei nº 8.078/90, aquele que exaure a função econômica do bem ou serviço, excluindo-o de forma definitiva do mercado de consumo.
> 3. A jurisprudência do STJ, tomando por base o conceito de consumidor por equiparação previsto no art. 29 do CDC, tem evoluído para uma aplicação temperada da teoria finalista frente às pessoas jurídicas, num processo que a doutrina vem denominando finalismo aprofundado, consistente em se admitir que, em determinadas hipóteses, a pessoa jurídica adquirente de um produto ou serviço pode ser equiparada à condição de consumidora, por apresentar frente ao fornecedor alguma vulnerabilidade, que constitui o princípio-motor da política nacional das relações de consumo, premissa expressamente fixada no art. 4º, I, do CDC, que legitima toda a proteção conferida ao consumidor.
> 4. A doutrina tradicionalmente aponta a existência de três modalidades de vulnerabilidade: técnica (ausência de conhecimento específico acerca do produto ou serviço objeto de consumo), jurídica (falta de conhecimento jurídico, contábil ou econômico e de seus reflexos na relação de consumo) e fática (situações em que a insuficiência econômica, física ou até mesmo psicológica do consumidor o coloca em pé de desigualdade frente ao fornecedor). Mais recentemente, tem se incluído também a vulnerabilidade informacional (dados insuficientes sobre o produto ou serviço capazes de influenciar no processo decisório de compra).
> 5. A despeito da identificação in abstracto dessas espécies de vulnerabilidade, a casuística poderá apresentar novas formas de vulnerabilidade aptas a atrair a incidência do CDC à relação de consumo. Numa relação interempresarial, para além das hipóteses de vulnerabilidade já consagradas pela doutrina e pela jurisprudência, a relação de dependência de uma das partes frente à outra pode, conforme o caso, caracterizar uma vulnerabilidade legitimadora da aplicação da Lei nº 8.078/90, mitigando os rigores da teoria finalista e autorizando a equiparação da pessoa jurídica compradora à condição de consumidora.
> 6. Hipótese em que revendedora de veículos reclama indenização por danos materiais derivados de defeito em suas linhas telefônicas, tornando inócuo o investimento em anúncios publicitários, dada a impossibilidade de atender ligações de potenciais clientes. A contratação do serviço de telefonia não caracteriza relação de consumo tutelável pelo CDC, pois o referido serviço compõe a cadeia produtiva da empresa, sendo essencial à consecução do seu negócio. Também não se verifica nenhuma vulnerabilidade apta a equipar a empresa à condição de consumidora frente à prestadora do serviço de telefonia. Ainda assim, mediante aplicação do direito à espécie, nos termos do art. 257 do RISTJ, fica mantida a condenação imposta a título de danos materiais, à luz dos arts. 186 e 927 do CC/02 e tendo em vista a conclusão das instâncias ordinárias quanto à existência de culpa da fornecedora pelo defeito apresentado nas linhas telefônicas e a relação direta deste defeito com os prejuízos suportados pela revendedora de veículos.
> 7. Recurso especial a que se nega provimento.

### STJ · AREsp 3.102.285/RS
- regras: PJ-VULN
- posicao: FAV
- tribunal: STJ
- classe_numero: AREsp 3.102.285/RS
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2026-05-04
- publicacao: 2026-05-08
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6796016353
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Acórdão recente e unânime da Terceira Turma que reafirma a regra e a exceção (CDC não se aplica à atividade econômica, salvo hipossuficiência técnica, jurídica ou econômica da PJ) e mantém o CDC reconhecido na origem a empresas de pequeno porte e microempresa contra banco de grande porte, por vulnerabilidade técnica e econômica.
- observacao: O mérito da vulnerabilidade não foi reexaminado (Súmulas 5 e 7/STJ); o acórdão preserva a conclusão da origem. O contrato era de antecipação de recebíveis de cartão de crédito, e não de capital de giro; a analogia com o capital de giro é do advogado. Publicação pelo DJEN/CNJ de 08/05/2026, conforme o texto.

ementa:
> AGRAVO EM RECURSO ESPECIAL. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO VERIFICADA. INCIDÊNCIA DO CDC. PESSOA JURÍDICA. TEORIA FINALISTA MITIGADA. VULNERABILIDADE. CONSTATADA. REVISÃO. IMPOSSIBILIDADE. SÚMULAS NºS 5 E 7/STJ.
> 1. Na espécie, não houve violação dos artigos 1.022 e 1025 do Código de Processo Civil, visto que agiu corretamente o tribunal de origem ao rejeitar os embargos de declaração por inexistir omissão, contradição, obscuridade ou erro material no acórdão atacado, ficando patente o intuito infringente da irresignação.
> 2. De acordo com a jurisprudência do Superior Tribunal de Justiça, em regra, não se aplica o Código de Defesa do Consumidor no caso em que o produto ou serviço seja contratado para implementação de atividade econômica, visto que não estaria configurado o destinatário final da relação de consumo e, em exceção a essa regra, admite-se a incidência das normas protetivas do consumidor quando ficar demonstrada a condição de hipossuficiência técnica, jurídica ou econômica da pessoa física/jurídica.
> 3. A modificação do acórdão recorrido para infirmar a conclusão do aresto atacado acerca da configuração da vulnerabilidade financeira e técnica da parte recorrida e a inversão do ônus da prova demandaria o reexame do conjunto fático-probatório e a interpretação de cláusula contratual, providências vedadas em recurso especial pelas Súmulas nºs 5 e 7/STJ.
> 4. Agravo conhecido para conhecer em parte do recurso especial e, nessa extensão, negar-lhe provimento.

### STJ · REsp 2.221.165/AL
- regras: PJ-VULN
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.221.165/AL
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2025-10-20
- publicacao: 2025-10-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6267278289
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Em contrato bancário firmado por empresa com finalidade empresarial, o STJ mantém a aplicação do CDC reconhecida na origem com base na teoria finalista mitigada e na vulnerabilidade da empresa frente à instituição financeira, e rejeita a tese de que o "mero capital de giro" bastaria para afastá-lo.
- observacao: Reexame da vulnerabilidade barrado pelas Súmulas 5 e 7/STJ. O voto define a vulnerabilidade como técnica, jurídica (expertise legal, contábil ou econômica) ou econômica (dependência ou assimetria de poder contratual) e lista os fatos a examinar: porte econômico, conhecimento técnico e jurídico, natureza de adesão e possibilidade real de negociar cláusulas. Sessão virtual de 14 a 20/10/2025; a data de 2025-10-20 vem do termo de julgamento; publicação pela data do Jusbrasil. A tomadora era sociedade anônima de grande porte, então a vulnerabilidade ali decorreu do contexto contratual e não do porte.

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. AÇÃO MONITÓRIA. CONTRATOS BANCÁRIOS. APLICAÇÃO DO CÓDIGO DE DEFESA DO CONSUMIDOR. EXIGIBILIDADE DE CONTRATO NÃO ASSINADO.
> I. CASO EM EXAME
> 1. Recurso especial interposto por instituição financeira contra acórdão do Tribunal de Justiça de Alagoas que, em ação monitória, reconheceu a aplicação do Código de Defesa do Consumidor à relação jurídica, declarou a inexigibilidade de contrato bancário desprovido de assinatura e manteve a multa moratória de 10% nos contratos pactuados antes da vigência da Lei nº 9.298/1996.
> 2. O acórdão recorrido rejeitou embargos de declaração sob o fundamento de ausência de omissão relevante.
> II. QUESTÃO EM DISCUSSÃO
> 3. Há três questões em discussão: (i) saber se houve violação do art. 1.022 do CPC, diante da alegada omissão do acórdão recorrido em se manifestar sobre pontos relevantes suscitados nos embargos de declaração; (ii) saber se o Código de Defesa do Consumidor é aplicável a contrato bancário firmado com pessoa jurídica com finalidade empresarial; e (iii) saber se contrato bancário desprovido de assinatura pode ser considerado válido no contexto de sucessivas operações formalizadas.
> III. RAZÕES DE DECIDIR
> 4. O Tribunal de origem entregou a prestação jurisdicional de forma completa e fundamentada, enfrentando as questões postas, não havendo omissão ou contradição. A discordância do recorrente com a tese jurídica adotada não caracteriza vício de fundamentação.
> 5. A aplicação do Código de Defesa do Consumidor foi fundamentada na teoria finalista mitigada, reconhecendo a vulnerabilidade da empresa recorrida frente à instituição financeira, conforme análise do contexto contratual e das partes envolvidas. A revisão dessa conclusão demandaria reexame de fatos e provas, vedado em recurso especial (Súmulas 5 e 7 do STJ).
> 6. A inexigibilidade do contrato bancário desprovido de assinatura foi fundamentada na ausência de requisito formal de validade e na insuficiência do documento como prova escrita da obrigação. A pretensão de validar o contrato com base no "contexto contratual" esbarra no óbice da Súmula 7 do STJ.
> IV. DISPOSITIVO
> Recurso especial conhecido em parte e improvido.

### STJ · REsp 2.001.086/MT
- regras: PJ-VULN
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.001.086/MT
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2022-09-27
- publicacao: 2022-09-30
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1660009012
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Limite da tese (ressalva obrigatória): o contrato de capital de giro para fomento da atividade empresarial não é relação de consumo; a teoria finalista mitigada exige vulnerabilidade comprovada, que não se presume.
- observacao: Unânime. O voto afirma que a mera identificação da tomadora como microempresa não serve, por si só, como fundamento idôneo para aplicar o CDC, e que a vulnerabilidade tem de ser demonstrada. A petição deve alegar e provar a vulnerabilidade concreta (porte, adesão, ausência de assessoria, dependência) e não só o enquadramento como ME ou EPP. Publicação pela data do Jusbrasil. O ônus da prova é da PJ.

ementa:
> RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. FINANCIAMENTO. PESSOA JURÍDICA. MÚTUO PARA FOMENTO DE ATIVIDADE EMPRESARIAL. CONTRATO DE CAPITAL DE GIRO. EMPRESA NÃO DESTINATÁRIA FINAL DO SERVIÇO. RELAÇÃO DE CONSUMO. INEXISTÊNCIA. CÓDIGO DE DEFESA DO CONSUMIDOR . INAPLICABILIDADE. TEORIA FINALISTA MITIGADA. VULNERABILIDADE NÃO PRESUMIDA. REVOLVIMENTO FÁTICO-PROBATÓRIO. IMPOSSIBILIDADE.
> 1. Ação revisional de contrato bancário ajuizada em 24/08/2021, da qual foi extraído o presente recurso especial interposto em 23/02/2022 e concluso ao gabinete em 01/06/2022.
> 2. O propósito recursal consiste em dizer se o Código de Defesa do Consumidor é aplicável à relação jurídica firmada entre as litigantes, oriunda de contratação de empréstimo para fomento de atividade empresarial.
> 3. Nos termos da jurisprudência do STJ, é inaplicável o diploma consumerista na contratação de negócios jurídicos e empréstimos para fomento da atividade empresarial, uma vez que a contratante não é considerada destinatária final do serviço. Precedentes. Não há que se falar, portanto, em aplicação do CDC ao contrato bancário celebrado por pessoa jurídica para fins de obtenção de capital de giro.
> 4. Dessa maneira, inexistindo relação de consumo entre as partes, mas sim, relação de insumo, afasta-se a aplicação do Código de Defesa do Consumidor e seus regramentos protetivos decorrentes, como a inversão do ônus da prova ope judicis (art. 6º, inc. VIII, do CDC).
> 5. A aplicação da Teoria Finalista Mitigada exige a comprovação de vulnerabilidade técnica, jurídica, fática e/ou informacional, a qual não pode ser meramente presumida. Nesta sede, porém, não se pode realizar referida análise, porquanto exigiria o revolvimento do conjunto fático-probatório dos autos (Súmula 7 /STJ).
> 6. Afasta-se a aplicação de multa, uma vez que não configura intuito protelatório ou litigância de má-fé a mera interposição de recurso legalmente previsto.
> 7. Recurso especial conhecido e provido.

### TJMG · Apelação Cível 5001492-96.2025.8.13.0625
- regras: PJ-VULN
- posicao: FAV
- tribunal: TJMG
- classe_numero: Apelação Cível 5001492-96.2025.8.13.0625
- orgao: 17ª Câmara Cível
- relator: Des. Amauri Pinto Ferreira
- julgamento: 2026-03-05
- publicacao: 2026-03-05
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mg/5956562612
- verificado_em: 2026-10-27
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito bancário de capital de giro (PRONAMPE) tomada por microempresa, o TJMG mantém a incidência do CDC sobre a instituição financeira com base na teoria finalista mitigada e na vulnerabilidade técnica e informacional da tomadora.
- observacao: Faltou TJPR: os acórdãos do TJPR identificados não entram porque o fetch devolve só o voto, sem a ementa (ver Relatório). Alinhamento parcial: no voto, o CDC já tinha sido aplicado na sentença e o TJ confirma que a sentença o aplicou, sem reanalisar a vulnerabilidade, e o pedido revisional foi desprovido no mérito. Datas de julgamento e publicação pela data do Jusbrasil (o texto não traz a data da sessão). Há divergência interna: outra apelação do TJMG, de 09/06/2026, também sobre cédula bancária de capital de giro (PRONAMPE), afirma na ementa que o CDC não se aplica a capital de giro para fomento empresarial (visto só no resumo da busca, não aberto).

ementa:
> APELAÇÃO CÍVEL - AÇÃO REVISIONAL DE CONTRATO - CONHECIMENTO PARCIAL DO RECURSO - PRELIMINAR - REJEITADA - CÉDULA DE CRÉDITO BANCÁRIO - CAPITAL DE GIRO - PRONAMPE - INSTITUIÇÃO FINANCEIRA - APLICAÇÃO DO CDC - TEORIA FINALISTA MITIGADA - JUROS REMUNERATÓRIOS - ABUSIVIDADE NÃO DEMONSTRADA - TAXA SELIC - INCIDÊNCIA AUTORIZADA POR LEGISLAÇÃO ESPECÍFICA - SISTEMA PRICE - LEGALIDADE - CAPITALIZAÇÃO EXPRESSAMENTE PACTUADA - PROVA PERICIAL - DESNECESSIDADE - CERCEAMENTO DE DEFESA NÃO CONFIGURADO - MORA CARACTERIZADA - SENTENÇA MANTIDA. É vedado à parte, em sede recursal, trazer à discussão questões que não foram apresentas ao Magistrado primevo, exceto aquelas que forem cognoscíveis de ofício, referirem-se a fatos supervenientes aos articulados ou não tiverem sido deduzidas anteriormente por força maior. Assim, não se enquadrando a matéria eriçada a tais exceções, não deve o recurso ser conhecido quanto à nova discussão. Inexiste cerceamento de defesa quando a prova pericial se mostra desnecessária ao deslinde da controvérsia, sobretudo quando as partes dispensam sua produção e a matéria é eminentemente de direito. É aplicável o Código de Defesa do Consumidor às instituições financeiras, inclusive às pessoas jurídicas, quando evidenciada a vulnerabilidade técnica ou informacional, nos termos da teoria finalista mitigada. A revisão dos juros remuneratórios somente é admitida em hipóteses excepcionais, quando comprovada abusividade manifesta capaz de colocar o consumidor em desvantagem exagerada, o que não se verifica pela simples comparação com a taxa média de mercado. Nos contratos firmados no âmbito do PRONAMPE, a incidência da Taxa Selic encontra respaldo expresso na Lei nº 13.999/2020, não configurando ilegalidade ou bis in idem. A utilização do Sistema Francês de Amortização (Tabela Price) não implica, por si só, capitalização ilícita de juros, sendo válida quando expressamente pactuada, nos termos da Medida Provisória nº 2.170-36/2001 e da jurisprudência do Superior Tribunal de Justiça.. Ausente abusividade nos encargos exigidos no período da normalidade contratual, mantém-se a caracterização da mora.
