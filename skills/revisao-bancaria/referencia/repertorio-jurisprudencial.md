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

1. **Fonte:** o conector Jusbrasil (busca e inteiro teor), a página do julgado no site do Jusbrasil
   lida em inteiro teor no navegador (mesmo acervo, sem cota; desde a onda 6) ou, para acórdão do TJPR, o portal de
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
- regras: R01, R02, R21, R22
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.058.114/RS
- orgao: Segunda Seção
- relator: Min. Nancy Andrighi (p/ acórdão Min. João Otávio de Noronha)
- julgamento: 2009-08-12
- publicacao: 2010-11-16
- precedente_qualificado: Tema 52/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106304712
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Acórdão de Turma (2023) que, enfrentando o mérito, reafirma que a comissão de permanência não pode ser cumulada com outros encargos, inclusive os moratórios, e que a repetição do indébito dispensa prova do erro (Súmula 322/STJ).
- observacao: Publicação pela data do Jusbrasil (o texto traz a sessão virtual de 12 a 18/09/2023 e a data de 19/09/2023, sem DJe). Ação civil pública de associação de consumidores (interesses individuais homogêneos); a conclusão sobre a efetiva cumulação no caso foi mantida por Súmulas 5 e 7/STJ, mas a tese (item 4 da ementa) é afirmada no voto contra o banco, que sustentava só ser vedada a cumulação com correção e juros remuneratórios.

ementa:
> AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. CIVIL, PROCESSO CIVIL E CONSUMIDOR. AÇÃO CIVIL PÚBLICA. INTERESSES INDIVIDUAIS HOMOGÊNEOS. 1. VIOLAÇÃO DOS ARTS. 489 E 1.022 DO CPC . OMISSÃO E NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO CONFIGURAÇÃO. 2. LEGITIMIDADE ATIVA DAS ASSOCIAÇÕES. RECONHECIMENTO. AUTORIZAÇÃO ASSEMBLEAR. DESNECESSIDADE. 3. INTERESSE PROCESSUAL. NECESSIDADE DE INTERPRETAÇÃO DE CLÁUSULAS CONTRATUAIS E DO REEXAME DE FATOS E PROVAS DOS AUTOS. INCIDÊNCIA DAS SÚMULAS NºS 5 E 7 DO STJ. 4. COMISSÃO DE PERMANÊNCIA. IMPOSSIBILIDADE DE CUMULAÇÃO COM OUTROS ENCARGOS, INCLUSIVE MORATÓRIOS. 5. VIOLAÇÃO AOS PRINCÍPIOS DA ISONOMIA E DA LIVRE CONCORRÊNCIA. ALEGAÇÃO GENÉRICA. INCIDÊNCIA DA SÚMULA Nº 284 DO STF. 6. REPETIÇÃO DE INDÉBITO . CABIMENTO. COMPROVAÇÃO DE ERRO NO PAGAMENTO. DISPENSABILIDADE. 7. PUBLICAÇÃO DA SENTENÇA EM JORNAIS DE GRANDE CIRCULAÇÃO. VIOLAÇÃO A DISPOSITIVOS CONSTITUCIONAIS. IMPOSSIBILIDADE DE ANÁLISE DA MATÉRIA, SOB PENA DE USURPAÇÃO DA COMPETÊNCIA DO STF. AGRAVO INTERNO NÃO PROVIDO.
> 1. Inexistem os vícios elencados nos arts. 489 e 1.022 do CPC, sendo forçoso reconhecer que a pretensão recursal ostenta caráter nitidamente infringente, visando rediscutir matéria que já foi analisada.
> 2. Para a defesa coletiva, são legitimadas concorrentes as associações legalmente constituídas há pelo menos um ano e que incluam entre seus fins institucionais a defesa dos interesses e direitos protegidos por este código, dispensada a autorização assemblear.
> 3. Rever as conclusões quanto à efetiva cumulação da comissão de permanência com outros encargos demandaria, necessariamente, reexame do conjunto fático-probatório dos autos e do contrato firmado entre as partes, o que é vedado em razão dos óbices das Súmulas nºs 5 e 7 do STJ.
> 4. A cobrança de comissão de permanência, cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato, exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual (Súmula nº 472/STJ).
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Acórdão recente de Turma que reafirma (item 2 da ementa) que a comissão de permanência só é admitida sem cumulação com correção monetária, juros remuneratórios, moratórios e multa, porque tem a mesma natureza desses encargos em conjunto (Súmulas 294 e 472), evitando dupla penalização; serve também a tomador pessoa jurídica (sem CDC).
- observacao: Resultado concreto desfavorável ao tomador (o TJPR reconheceu comissão pactuada e cobrada de forma isolada, e o STJ manteve por Súmulas 5 e 7); usar só pela tese do item 2. Tomador pessoa jurídica (crédito rotativo). DJe/STJ de 29/02/2024 conforme o texto.

ementa:
> AGRAVO INTERNO. EMBARGOS DE DECLARAÇÃO. RECURSO ESPECIAL. EMBARGOS À MONITÓRIA. CONTRATO DE ABERTURA DE CRÉDITO. REALIZAÇÃO DE PROVA PERICIAL. TAXA DE JUROS REMUNERATÓRIOS PRATICADAS PELO BANCO. AUSÊNCIA DE ABUSIVIDADE. CAPITALIZAÇÃO DOS JUROS. EXPRESSA PACTUAÇÃO. COMISSÃO DE PERMANÊNCIA. POSSIBILIDADE DE COBRANÇA. SÚMULA N. 472 DO STJ. ENCARGOS CONTRATUAIS PACTUADOS. REEXAME CONTRATUAL E FÁTICO DOS AUTOS. SÚMULAS N. 5 E 7 DO STJ.
> 1. Não cabe, em recurso especial, reexaminar matéria fático-probatória e interpretar cláusulas contratuais (Súmulas n. 5 e 7 /STJ).
> 2. A jurisprudência do STJ firmou o entendimento de que a comissão de permanência pode ser autorizada, de acordo com a Súmula n. 294 do STJ, desde que sem cumulação com correção monetária, com juros remuneratórios e moratórios e multa. Tal prática visa a evitar a ocorrência de dupla penalização, porque a comissão de permanência possui a mesma natureza desses encargos, conjuntamente, conforme estabelecido na Súmula n. 472 do STJ.
> 3. Agravo interno a que se nega provimento.

### TJPR · Apelação Cível 0023281-39.2015.8.16.0001
- regras: R01, R02
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0023281-39.2015.8.16.0001
- orgao: 15ª Câmara Cível
- relator: Des. Jucimar Novochadlo
- julgamento: 2025-11-29
- publicacao: 2025-11-30
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035529301/Ac%C3%B3rd%C3%A3o-0023281-39.2015.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em ação revisional de cédula e de limite de crédito de pessoa jurídica, o TJPR mantém o decote da comissão de permanência cumulada com os demais encargos moratórios: a comissão, cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios do contrato, exclui a exigibilidade de juros remuneratórios, juros de mora e multa (Súmula 472/STJ).
- observacao: Apelação do banco provida só quanto à sucumbência; o expurgo da cumulação foi mantido. Contratos anteriores a 01/09/2017 (ação ajuizada em 2015). Para a R02, o teto (soma dos encargos) é afirmado como premissa na ementa; o que se decidiu foi a exclusão da cumulação, não o decote de um excesso sobre o teto. A íntegra cita o próprio CNJ. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO. CONTRATOS DE ABERTURA DE CRÉDITO, BB GIRO EMPRESA FLEX E CÉDULA DE CRÉDITO BANCÁRIO. 1. COMISSÃO DE PERMANÊNCIA EM CUMULAÇÃO COM OUTROS ENCARGOS MORATÓRIOS. IMPOSSIBILIDADE. EXPURGO MANTIDO. 2. SUCUMBÊNCIA. REDISTRIBUIÇÃO DO ÔNUS. SENTENÇA PARCIALMENTE REFORMADA NESSA PARTE.1. A cobrança de comissão de permanência – cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato – exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual (Súmula nº 472 do STJ).2. O ônus de sucumbência deve ser distribuído considerando o aspecto quantitativo e jurídico em que cada parte decai de suas pretensões. No caso concreto, a parte autora restou vencida na maior parte da pretensão formulada na inicial, razão pela qual se faz necessária a redistribuição do ônus de sucumbência, nos termos do art. 86, parágrafo único, do CPC.Apelação Cível provida em parte.

### TJPR · Apelação Cível 0028004-92.2011.8.16.0017
- regras: R01, R02
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0028004-92.2011.8.16.0017
- orgao: 4ª Câmara Cível
- relator: Des.ª Astrid Maranhão de Carvalho Ruthes
- julgamento: 2025-06-30
- publicacao: 2025-06-30
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000032305051/Ac%C3%B3rd%C3%A3o-0028004-92.2011.8.16.0017
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em financiamento de 2010, o TJPR confirma a nulidade da cláusula que cumula comissão de permanência com juros moratórios e multa (Súmula 472/STJ) e reproduz o teto do REsp 1.058.114/RS: a comissão não pode ultrapassar a soma dos encargos remuneratórios e moratórios do contrato.
- observacao: Apelação do banco desprovida; sentença de nulidade da cumulação mantida. Contrato celebrado em 16/11/2010, anterior ao corte de 01/09/2017. O voto mantém só a comissão de permanência e exclui os juros remuneratórios excedentes à taxa de mercado; o teto da soma dos encargos entra como premissa (item 5 da ementa). O cabeçalho da íntegra aponta a 2ª Vara Cível de Paranaguá, enquanto o portal indica a comarca de Maringá; o CNJ, as partes e o conteúdo conferem com a ementa. Fonte: portal de jurisprudência do TJPR (comarca de Maringá). Ementa copiada do portal sem o rótulo inicial ("Ementa.").

ementa:
> direito civil. recurso de apelação. contrato de financiamento. possibilidade de revisão judicial. comissão de permanência. cobrança cumulada com juros moratórios e multa contratual. abusividade constatada. Recurso de apelação cível conhecido e não provido.I. Caso Em Exame 1. Recurso de apelação interposto contra sentença que reconheceu a nulidade de cláusulas contratuais em contrato de financiamento firmado entre as partes, notadamente aquelas que previam a cobrança cumulada de comissão de permanência com juros moratórios e multa contratual. O apelante sustenta a licitude do contrato, argumentando que as partes acordaram livremente com as cláusulas contratuais, afastando a possibilidade de nulidade. O juízo de origem entendeu pela nulidade das cláusulas contratuais que previam cobrança abusiva e cumulativa de encargos moratórios.
> II. Questões Em Discussão2. Existem duas questões em discussão: (i) averiguar caso a autonomia da vontade das partes impede a revisão judicial de cláusulas contratuais; e (ii) verificar a validade da cobrança cumulada de comissão de permanência com juros moratórios e multa contratual.
> III. Razões De Decidir3. A autonomia da vontade das partes não impede a revisão judicial de cláusulas contratuais quando constatados vícios que afetem a validade ou legalidade do contrato, em observância à função social dos contratos (art. 421 do Código Civil).4. Segundo a doutrina, "diante do princípio da conservação contratual, o juiz deve incentivar essa revisão, o que mantém relação direta com a função social dos contratos" (TARTUCE, Flávio. Direito Civil: teoria geral dos contratos e contratos em espécie. 19. ed. Rio de Janeiro: Forense, 2024, p. 189).5. Nos termos da jurisprudência do Superior Tribunal de Justiça, "a importância cobrada a título de comissão de permanência não poderá ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato" (STJ - REsp 1058114/RS, Rel. Min. Nancy Andrighi, DJe 16/11/2010).6. A previsão contratual de cobrança cumulativa de comissão de permanência com juros moratórios e multa contratual é considerada abusiva e afronta a Súmula 472 do STJ.7. O Tribunal de Justiça do Paraná firmou entendimento no sentido de que "a previsão contratual de cumulação da comissão de permanência com juros de mora e multa contratual é vedada, conforme orientação do STJ" (TJPR - 14ª Câmara Cível - Apelação Cível 0000565-57.2021.8.16.0017 - Rel. Des. Francisco Eduardo Gonzaga de Oliveira - J. 20/05/2024).8. Diante da manifesta abusividade das cláusulas contratuais, a sentença de origem deve ser mantida.
> IV. Dispositivo E Tese9. Recurso de apelação cível conhecido e negado provimento.Tese de julgamento: A revisão judicial das cláusulas contratuais é admissível quando constatada abusividade, em razão da função social do contrato. A cobrança cumulativa de comissão de permanência com juros moratórios e multa contratual é vedada, conforme entendimento consolidado do STJ._________________________________Dispositivos relevantes citados: Código Civil: art. 421; Código de Defesa do Consumidor: art. 52, § 1º.Jurisprudência relevante citada: STJ - REsp 1058114/RS, Rel. Min. Nancy Andrighi, DJe 16/11/2010. TJPR - 14ª Câmara Cível - Apelação Cível 0000565-57.2021.8.16.0017 - Rel. Des. Francisco Eduardo Gonzaga de Oliveira - J. 20/05/2024.

### TJPR · Apelação Cível 0016851-28.2012.8.16.0017
- regras: R01
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0016851-28.2012.8.16.0017
- orgao: 13ª Câmara Cível
- relator: Juiz Subst. 2º Grau Marcel Luis Hoffmann
- julgamento: 2025-11-05
- publicacao: 2025-11-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000034999761/Ac%C3%B3rd%C3%A3o-0016851-28.2012.8.16.0017
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: O TJPR mantém a sentença que expurgou a comissão de permanência cumulada com juros de mora e multa em contratos bancários de conta corrente e mútuo, deixando só a comissão, isolada (Súmula 472/STJ), com restituição simples do indébito.
- observacao: Apelação do banco conhecida em parte e desprovida. Ação de 2012, contratos anteriores a 01/09/2017. A íntegra do portal não cita o CNJ, mas descreve a mesma sentença da ementa (1ª Vara Cível de Maringá; expurgo da comissão cumulada, limitação à taxa média do BACEN, repetição simples, compensação), e foi tomada como do mesmo caso. A ementa traz as seções em linhas separadas, mantidas. Fonte: portal de jurisprudência do TJPR (comarca de Maringá). Ementa copiada do portal sem o rótulo inicial ("Ementa:").

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO C/C REPETIÇÃO DE INDÉBITO E PEDIDO DE TUTELA ANTECIPADA. LIMITAÇÃO DOS JUROS REMUNERATÓRIOS. IMPOSSIBILIDADE DE COBRANÇA CUMULADA DE COMISSÃO DE PERMANÊNCIA COM OUTROS ENCARGOS MORATÓRIOS.
> REPETIÇÃO DO INDÉBITO NA FORMA SIMPLES. RECURSO DESPROVIDO.I. CASO EM EXAME1.Apelação cível interposta por instituição financeira contra sentença que julgou parcialmente procedentes os pedidos formulados em ação revisional de contratos bancários, com repetição de indébito e pedido de tutela antecipada, para: (i) expurgar a cobrança cumulada de comissão de permanência com juros moratórios e multa; (ii) determinar a substituição das taxas de juros aplicadas por aquelas médias de mercado divulgadas pelo BACEN, quando favoráveis ao consumidor e de forma linear; (iii) deferir a repetição de indébito dos valores cobrados a maior; e (iv) reconhecer a compensação com débitos das autoras em ações conexas. A sentença também fixou a sucumbência recíproca, distribuindo os ônus de forma proporcional. O réu recorre alegando, entre outros pontos, a impossibilidade de revisão contratual, a legalidade da comissão de permanência e a indevida repetição de indébito.II. QUESTÃO EM DISCUSSÃO2. Há cinco questões em discussão:
> (i) verificar a possibilidade de revisão das cláusulas contratuais, com mitigação do princípio pacta sunt servanda;
> (ii) apurar a legalidade da limitação dos juros remuneratórios à taxa média de mercado do BACEN;
> (iii) examinar a validade da cobrança da comissão de permanência cumulada com outros encargos moratórios;
> (iv) estabelecer a possibilidade de repetição de indébito na forma simples;
> (v) definir a correta distribuição da sucumbência com base nos critérios legais.III. RAZÕES DE DECIDIR3. A preclusão impede o exame do pedido de revogação da tutela antecipada, por não ter sido impugnada no momento oportuno, nos termos do art. 507 do CPC.4. A revisão contratual é possível quando demonstrada onerosidade excessiva ou abusividade nas cláusulas, em consonância com a boa-fé objetiva e a função social do contrato, conforme entendimento do STJ.5. A relativização do princípio pacta sunt servanda é admitida especialmente em contratos de adesão firmados com instituições financeiras, não havendo ofensa à autonomia privada quando presentes indícios de abusividade.6. A estipulação de juros remuneratórios em patamar superior à taxa média de mercado, por si só, não caracteriza abusividade. No entanto, configura-se cobrança excessiva quando a taxa ultrapassa o dobro da média divulgada pelo BACEN, impondo-se sua limitação.7. Na ausência de juntada dos contratos de empréstimo, incide a presunção do art. 400 do CPC, permitindo a substituição das taxas por aquelas médias de mercado, nos termos da Súmula 530 do STJ.8. A cobrança cumulada de comissão de permanência com juros de mora e multa contratual é vedada, conforme Súmula 472/STJ, sendo legítima apenas a exigência da comissão de permanência isoladamente, se pactuada.9. A repetição do indébito deve ocorrer na forma simples, pois não demonstrada a má-fé da instituição financeira, conforme precedentes do STJ (AgRg no REsp 1.329.178/SC e AgRg no AREsp 573.065/RS).10. A distribuição dos ônus sucumbenciais segue o critério da sucumbência proporcional, nos termos do art. 85 do CPC, sendo descabida a aplicação do princípio da causalidade na hipótese dos autos.IV. DISPOSITIVO E TESE11. Recurso desprovido.________Teses de julgamento:
> 12. É admissível a revisão contratual quando verificada abusividade, com mitigação do princípio pacta sunt servanda, sobretudo em contratos bancários de adesão, sendo que a cobrança de juros remuneratórios superiores ao dobro da taxa média de mercado é considerada abusiva e deve ser limitada à taxa média do BACEN. É vedada a cumulação da comissão de permanência com outros encargos moratórios, como juros de mora e multa contratual, ao passo que a repetição de indébito deve ocorrer na forma simples quando ausente comprovação de má-fé do credor.
> ________Dispositivos relevantes citados:
> CF/1988, art. 5º, XXXII; CC, arts. 389, 422, 876 e 927; CDC, arts. 6º, V, e 51, IV e §1º; CPC, arts. 85, § 2º, 400 e 507.Jurisprudência relevante citada:
> STJ, AgInt no AREsp 1.506.600/RJ, Rel. Min. Marco Buzzi, j. 09.12.2019;
> STJ, REsp 1.061.530/RS, Rel. Min. Nancy Andrighi, j. 22.10.2008 (repetitivo);
> STJ, Súmulas 83, 472 e 530;
> TJPR, ApCiv 0001457-38.2022.8.16.0014, Rel. Juiz Marcos Vinícius Demchuk, j. 23.09.2022;
> TJPR, ApCiv 0028478-96.2020.8.16.0001, Rel. Desª Rosana Andrighetto de Carvalho, j. 21.10.2022.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Aplicação direta do Tema 52 em segundo juízo de retratação (após decisão do STJ): a comissão de permanência fica isolada, limitada à soma de juros remuneratórios (taxa média, sem passar a contratada), juros de mora de 1% ao mês e multa de 2%, com exclusão da cobrança separada de juros moratórios, multa e correção monetária e restituição simples do excesso.
- observacao: Complementa os acórdãos do TJPR desta tese. Cautela: a sentença havia excluído a comissão de permanência e mantido os encargos de mora; a retratação, por determinação do STJ (decisão monocrática, Súmulas 5 e 7), manteve a comissão isolada e dentro do teto, o que é menos favorável ao tomador que a sentença; citar apenas pela tese do teto e da vedação de cumulação. Contrato de 2012 (anterior a 01/09/2017). Ementa copiada sem o cabeçalho de identificação das partes que antecede o texto. Publicação pela data do Jusbrasil.

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

### TJPR · Apelação Cível 0031186-90.2018.8.16.0001
- regras: R02, R03
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0031186-90.2018.8.16.0001
- orgao: 13ª Câmara Cível
- relator: Des. Naor Ribeiro de Macedo Neto
- julgamento: 2023-02-03
- publicacao: 2023-02-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000022639311/Ac%C3%B3rd%C3%A3o-0031186-90.2018.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em cédula de capital de giro de 2017, o TJPR reconhece que os "juros remuneratórios para operação em atraso" são comissão de permanência encoberta, afasta os demais encargos moratórios e mantém a comissão limitada à soma dos encargos moratórios previstos no contrato (Súmula 472/STJ).
- observacao: Apelação da tomadora (pessoa jurídica) parcialmente provida. Cédula firmada em 28/06/2017, antes do corte de 01/09/2017. O limite à soma consta da ementa; o dispositivo do voto declara abusiva a cumulação dos juros remuneratórios do período de atraso com os demais encargos moratórios e afasta estes últimos, com restituição simples. Serve também à R03. A íntegra do portal não cita o CNJ, mas é do mesmo caso (ação revisional, cédula de capital de giro de 28/06/2017, sentença de improcedência, mesma ordem de temas e mesmo dispositivo). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CÉDULA DE CRÉDITO BANCÁRIO – CAPITAL DE GIRO. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA.1) CERCEAMENTO DE DEFESA. PROVA PERICIAL. FATOS DISCUTIDOS EM JUÍZO QUE PODEM SER SUFICIENTEMENTE ESCLARECIDOS POR MEIO DE MERA CONSULTA AO INSTRUMENTO DE CONTRATO. POSSIBILIDADE DE JULGAMENTO ANTECIPADO DO MÉRITO (ART. 355, I, CPC). PRELIMINAR REJEITADA.2) CAPITALIZAÇÃO DO JUROS MENSAL. EXPRESSA PREVISÃO. POSSIBILIDADE. 3) CAPITALIZAÇÃO DOS JUROS DE FORMA DIÁRIA. TAXA NÃO INFORMADA. VIOLAÇÃO AO DEVER DE INFORMAÇÃO. ABUSIVIDADE. DECRETADA.4) AMORTIZAÇÃO PELO SISTEMA PRICE. AUSÊNCIA DE ILEGALIDADE. SÚMULAS 539 E 541 DO STJ. CAPITALIZAÇÃO DOS JUROS QUE NÃO DECORRE DA SIMPLES APLICAÇÃO DA TABELA PRICE. CAPITALIZAÇÃO, ADEMAIS, EXPRESSAMENTE PREVISTA NO CONTRATO.5) JUROS REMUNERATÓRIOS ABUSIVOS. NÃO DEMONSTRAÇÃO EM RELAÇÃO À TAXA MÉDIA DE MERCADO. POSSIBILIDADE DE LIVRE PACTUAÇÃO. RESP 1.061.530-RS. COMPARATIVO COM AS TABELAS DO BACEN. JUROS APLICADOS NO CONTRATO QUE NÃO SE MOSTRARAM SUPERIORES AO DOBRO EM RELAÇÃO A MÉDIA DO MERCADO. 6) PRETENSÃO DE AFASTAMENTO DA COBRANÇA DE COMISSÃO DE PERMANÊNCIA CUMULADA COM DEMAIS ENCARGOS MORATÓRIOS. PREVISÃO CONTRATUAL DE JUROS REMUNERATÓRIOS PARA OPERAÇÃO EM ATRASO. COBRANÇA DE FORMA DISFARÇADA (CAMUFLADA). ABUSIVIDADE RECONHECIDA. SÚMULA 472 DO STJ. MANUTENÇÃO DA COMISSÃO DE PERMANÊNCIA LIMITADA À SOMA DOS DEMAIS ENCARGOS MORATÓRIOS PREVISTOS NO CONTRATO. REPETIÇÃO DE INDÉBITO DE FORMA SIMPLES.7) IMPOSTO SOBRE OPERAÇÕES FINANCEIRAS (IOF). MANUTENÇÃO. POSSIBILIDADE DE COBRANÇA DE FORMA DILUÍDA NO FINANCIAMENTO. ENTENDIMENTO FIRMADO PELO STJ EM SEDE DE RECURSO REPETITIVO (RESP Nº 1.251.331/RS E RESP Nº 1.255.2573 /RS).8) DESCARACTERIZAÇÃO DA MORA. ACOLHIMENTO. COBRANÇA DE VALORES INDEVIDOS DURANTE O PERÍODO DE NORMALIDADE CONTRATUAL. CONDENAÇÃO DO BANCO À RESTITUIÇÃO DESTES.9) REDISTRIBUIÇÃO DA VERBA SUCUMBENCIAL. HONORÁRIOS ADVOCATÍCIOS DE SUCUMBÊNCIA FIXADOS EM PERCENTUAL SOBRE O VALOR DA CAUSA. IMPOSSIBILIDADE DE SUA FIXAÇÃO MEDIANTE APRECIAÇÃO EQUITATIVA. VALOR DA CAUSA QUE NÃO SE MOSTRA IRRISÓRIO OU INESTIMÁVEL (ART. 85, §11, CPC) PRECEDENTES DO STJ.
> RECURSO PARCIALMENTE PROVIDO.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
> 5. A sentença de primeiro grau deve ser restabelecida, pois não houve violação ao disposto no art. 52, § 1º, do CDC.
> IV. DISPOSITIVO
> 6. Resultado do Julgamento: Recurso provido para restabelecer a sentença de primeiro grau.

### STJ · AREsp 2.671.164/GO
- regras: R03
- posicao: ADV
- tribunal: STJ
- classe_numero: AREsp 2.671.164/GO
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2025-10-20
- publicacao: 2025-10-29
- precedente_qualificado: não (delimita o alcance do Tema 52/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6267493482
- verificado_em: 2026-11-02
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: o STJ reformou acórdão do TJGO que tratara os juros remuneratórios do período de inadimplência como "comissão de permanência disfarçada" e os excluíra; nas cédulas de crédito rural (e, na fundamentação, industrial e comercial), a comissão de permanência é inexigível, mas o banco pode cobrar, após o vencimento, juros remuneratórios (até 12% ao ano) mais 1% ao ano de mora, multa e correção monetária (Decreto-Lei 167/1967, art. 5º, parágrafo único). A tese R03 não deve ser invocada para cédulas rurais, industriais ou comerciais; vale para os contratos bancários comuns regidos pelos repetitivos 1.058.114/RS e 1.063.343/RS.
- observacao: O fundamento do STJ é o escopo dos repetitivos (excluem cédulas de crédito rural, industrial e comercial, contratos de cooperativas de crédito, SFH e consignado, conforme trecho do voto da Min. Nancy Andrighi transcrito no acórdão), não uma rejeição da equiparação em si. O voto cita a premissa do TJGO ("comissão de permanência disfarçada") só para dizer que ela se apoiou em precedente inaplicável. A mesma exclusão pode ser invocada pela parte contrária em cooperativas e consignado; conferir a modalidade antes de citar R03. Publicação pela data do Jusbrasil (sessão virtual de 14 a 20/10/2025). Há acórdão no mesmo sentido, de 29/10/2026 (AgInt no REsp 2.255.341/MT, cédula rural), visto só no trecho de busca e não aberto.

ementa:
> DIREITO CIVIL. AGRAVO EM RECURSO ESPECIAL. REVISÃO DE CLÁUSULAS CONTRATUAIS. CÉDULA DE CRÉDITO RURAL. JUROS REMUNERATÓRIOS. COMISSÃO DE PERMANÊNCIA. RECURSO PARCIALMENTE PROVIDO.
> I. Caso em exame
> 1. Agravo contra decisão que inadmitiu recurso especial interposto por instituição financeira contra acórdão proferido em ação ordinária de revisão de cláusulas contratuais relativa à cédula rural pignoratícia e hipotecária.
> II. Questão em discussão
> 2. Há três questões em discussão: (i) saber se houve negativa de prestação jurisdicional e ausência de fundamentação no acórdão recorrido; (ii) saber se a petição inicial seria inepta por ausência de discriminação das cláusulas controvertidas e do valor incontroverso; e (iii) saber se o afastamento da comissão de permanência implica supressão dos juros remuneratórios no período de inadimplência.
> III. Razões de decidir
> 3. O acórdão recorrido não violou os arts. 489 e 1.022 do CPC, pois apresentou fundamentação suficiente para resolver a controvérsia, analisando os argumentos sobre a manutenção dos juros remuneratórios no período de inadimplência.
> 4. A ausência de depósito do valor incontroverso não torna inepta a petição inicial em ação revisional, sendo tal depósito exigido apenas para concessão de tutela antecipada, conforme entendimento consolidado no REsp 1.061.530/RS.
> 5. Nas cédulas de crédito rural, a comissão de permanência é inexigível, mas a instituição financeira está autorizada a cobrar juros remuneratórios limitados a 12% ao ano, acrescidos de juros de mora de 1% ao ano, multa de 10% e correção monetária, conforme o art. 5º, parágrafo único, do Decreto-Lei 167/1967 e jurisprudência do STJ.
> IV. Dispositivo e tese
> 6. Resultado do Julgamento: Recurso parcialmente provido para autorizar a incidência de juros remuneratórios no período de inadimplência, nos termos da jurisprudência do STJ.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Mantém sentença que reconheceu como comissão de permanência disfarçada a previsão de juros remuneratórios para o período de inadimplência cumulados com juros de mora e multa, por reunirem encargos remuneratórios e moratórios com o mesmo fato gerador (Súmula 472/STJ), e afastou a cumulação.
- observacao: Complementa os acórdãos do TJPR desta tese. O resultado prático é a exclusão da cumulação (a sentença afastou a incidência conjunta de juros remuneratórios, mora e multa na inadimplência). O voto transcreve a Súmula 472 de forma inexata; não citar o trecho do voto, só a ementa. A ementa confirma restituição em dobro, ponto não alinhado a esta tese e que não deve ser usado. Há acórdãos do próprio TJMT em sentido contrário. Publicação pela data do Jusbrasil.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Desprovê a apelação do banco e mantém a sentença que afastou os juros remuneratórios do período de inadimplência: ainda que a cláusula não mencione "comissão de permanência", a previsão de juros mensais, juros de mora e multa sobre o saldo devedor atualizado é a comissão de permanência sob outra roupagem, cuja cumulação é vedada.
- observacao: Complementa os acórdãos do TJPR desta tese. Aqui a consequência foi excluir os juros remuneratórios e manter mora e multa (diferente dos acórdãos do TJPR que li, que mantêm o encargo único isolado e afastam mora e multa); a petição deve pedir a consequência que mais convier ao contrato. Ementa com falhas de espaçamento do texto original, mantidas. O TJMT é dividido. Publicação pela data do Jusbrasil.

ementa:
> APELAÇÃO CÍVEL - AÇÃO DE BUSCA E APREENSÃO COMISSÃO DE PERMANÊNCIA DISFARÇADA - CUMULAÇÃO COM JUROS REMUNERATÓRIOS E OUTROS ENCARGOS - IMPOSSIBILIDADE - CUMULAÇÃO INDEVIDA - SENTENÇA MANTIDA - RECURSO DESPROVIDO. É possível a revisão de cláusulas pactuadas quando demonstrada a onerosidade excessiva ao consumidor, admitindo-se a relativização do princípio pacta sunt servanda a fim de estabelecer o equilíbrio contratual. A comissão de permanência constitui encargo incidente quando constituída a mora, apresentando o caráter múltiplo de atualizar e remunerar a moeda, não podendo haver a cumulação de multa com juros e comissão de permanência, o que não é permitido, por isso, merece ser mantida a sentença recorrida.

### TJPR · Apelação Cível 0003574-97.2023.8.16.0165
- regras: R03
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0003574-97.2023.8.16.0165
- orgao: 20ª Câmara Cível
- relator: Des. Antonio Franco Ferreira da Costa Neto
- julgamento: 2026-03-20
- publicacao: 2026-03-21
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000036798021/Ac%C3%B3rd%C3%A3o-0003574-97.2023.8.16.0165
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: "Juros remuneratórios para operações em atraso" têm a mesma natureza da comissão de permanência: o TJPR reforma a improcedência, reconhece a abusividade da cumulação com os demais encargos remuneratórios e moratórios (Súmulas 30 e 472/STJ) e manda restituir de forma simples.
- observacao: Apelação do autor provida. A íntegra cita o próprio CNJ. Cédula firmada em 30/08/2017, dois dias antes do corte de 01/09/2017; por isso o acórdão também serve às R01 e R02 (a ementa repete o teto da soma dos encargos). Repetição simples, sem pedido de dobro. Fonte: portal de jurisprudência do TJPR (comarca de Telêmaco Borba). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÃO CÍVEL – AÇÃO REVISIONAL – SENTENÇA DE IMPROCEDÊNCIA – INSURGÊNCIA DO AUTOR – JUROS remuneratórios para operações em atraso – MESMA NATUREZA DE COMISSÃO DE PERMANÊNCIA – IMPOSSIBILIDADE DE CUMULAÇÃO COM DEMAIS ENCARGOS REMUNERATÓRIOS E MORATÓRIOS – SÚMULAS Nº 30 E 472 DO STJ – ABUSIVIDADE VERIFICADA – RESTITUIÇÃO DEVIDA NA FORMA SIMPLES – RECURSO CONHECIDO E PROVIDO. 1. A previsão de “juros remuneratórios para período em atraso” revela caráter sancionatório decorrente da mora do mutuário, assumindo, em essência, a mesma finalidade econômica e jurídica da comissão de permanência.2. Nos termos da Súmula nº 472/STJ, a cobrança de comissão de permanência – cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato – exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual.

### TJPR · Apelação Cível 0000565-57.2021.8.16.0017
- regras: R03
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0000565-57.2021.8.16.0017
- orgao: 14ª Câmara Cível
- relator: Des. Francisco Eduardo Gonzaga de Oliveira
- julgamento: 2024-05-20
- publicacao: 2024-05-20
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000028299691/Ac%C3%B3rd%C3%A3o-0000565-57.2021.8.16.0017
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Cobrança "mascarada" de comissão de permanência sob a denominação "juros remuneratórios para operações em atraso", cumulada com juros de mora e multa: o TJPR reforma a improcedência, afasta os demais encargos moratórios (Súmula 472/STJ) e manda restituir de forma simples.
- observacao: Apelação do autor provida; inversão da sucumbência. A íntegra cita o próprio CNJ. É a decisão da 14ª Câmara que acórdãos posteriores de outras Câmaras (inclusive o da 4ª Câmara, de 2025, listado na R01) citam como precedente. A data do contrato não foi localizada; para a R03 não há corte temporal. Fonte: portal de jurisprudência do TJPR (comarca de Maringá). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL C/C TUTELA DE URGÊNCIA. SENTENÇA DE IMPROCEDÊNCIA. IRRESIGNAÇÃO DA PARTE AUTORA. COMISSÃO DE PERMANÊNCIA. COBRANÇA MASCARADA SOB A DENOMINAÇÃO DE “JUROS REMUNERATÓRIOS PARA OPERAÇÕES EM ATRASO”. PREVISÃO CONTRATUAL DE CUMULAÇÃO DO REFERIDO ENCARGO COM JUROS DE MORA E MULTA. IMPOSSIBILIDADE. INTELIGÊNCIA DA SÚMULA 472 DO STJ. AFASTAMENTO DOS DEMAIS ENCARGOS MORATÓRIOS. PRECEDENTES. REPETIÇÃO DO INDÉBITO DEVIDA, NA FORMA SIMPLES, SOB PENA DE ENRIQUECIMENTO ILÍCITO DA INSTITUIÇÃO FINANCEIRA. SENTENÇA REFORMADA, COM A INVERSÃO DO ÔNUS DE SUCUMBÊNCIA.RECURSO CONHECIDO E PROVIDO.

### TJPR · Apelação Cível 0002319-52.2019.8.16.0066
- regras: R03
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002319-52.2019.8.16.0066
- orgao: 1ª Câmara Cível
- relator: Juiz Subst. 2º Grau Everton Luiz Penter Correa
- julgamento: 2024-05-13
- publicacao: 2024-05-15
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000027280841/Ac%C3%B3rd%C3%A3o-0002319-52.2019.8.16.0066
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: "Encargos remuneratórios para operações em atraso" cumulados com juros de mora de 1% e multa de 2% são comissão de permanência camuflada; o TJPR a admite só isolada, exclui juros de mora e multa e manda restituir os valores cobrados (Tema 52/STJ).
- observacao: Apelação da autora parcialmente provida (sentença de improcedência reformada); sucumbência redistribuída em 70% e 30%. A íntegra cita o próprio CNJ. O voto mantém os 14,20% do encargo de atraso como comissão de permanência isolada. A data do contrato não foi localizada no voto; para a R03 não há corte temporal, mas o acórdão não deve ser citado para a R01/R02 sem conferir a data do contrato. Fonte: portal de jurisprudência do TJPR (comarca de Centenário do Sul). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. CÉDULA BANCÁRIA GARANTIDA POR ALIENAÇÃO FIDUCIÁRIA. SENTENÇA QUE JULGOU IMPROCEDENTES OS PEDIDOS. IRRESIGNAÇÃO DA PARTE AUTORA. ALEGAÇÃO DA CUMULAÇÃO DA COMISSÃO DE PERMANÊNCIA COM MULTA CONTRATUAL E JUROS DE MORA. ALEGAÇÃO DE ABUSIVIDADE NA COBRANÇA.
> COMISSÃO DE PERMANÊNCIA NOMINADA COMO “ENCARGOS REMUNERATÓRIOS PARA OPERAÇÕES EM ATRASO” CUMULADA COM JUROS DE MORA DE 1% E MULTA DE 2%. VEDAÇÃO. ENTENDIMENTO EXTERNADO PELO SUPERIOR TRIBUNAL DE JUSTIÇA EM SEDE DE INCIDENTE DE RECURSO REPETITIVO Nº 1.063.343/RS. CONSTATAÇÃO DA EXISTÊNCIA DE COMISSÃO DE PERMANÊNCIA CAMUFLADA. ADMISSIBILIDADE, NO ENTANTO, SE SUA INCIDÊNCIA, EXCLUINDO-SE, PORÉM, OS DEMAIS ENCARGOS CUMULATIVAMENTE COBRADOS. EXCLUSÃO DOS JUROS DE MORA E DA MULTA.
> RESTITUIÇÃO DOS VALORES INDEVIDAMENTE COBRADOS. REFORMA PARCIAL DA SENTENÇA. RECURSO PARCIALMENTE PROVIDO.

## R04 — TAC (tarifa de abertura de crédito) vedada em contratos posteriores a 30/04/2008

Tese: A tarifa de abertura de crédito (TAC), ou qualquer outra denominação para o mesmo fato gerador, não tem respaldo legal em contrato bancário de pessoa física celebrado a partir de 30/04/2008 (Res. CMN 3.518/2007 e Súmula 565/STJ), sendo indevida a cobrança e devida a restituição.

### STJ · REsp 1.251.331/RS
- regras: R04, R06, R08, CONTA-ENCARGOS
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.251.331/RS
- orgao: Segunda Seção
- relator: Min. Maria Isabel Gallotti
- julgamento: 2013-08-28
- publicacao: 2013-10-24
- precedente_qualificado: Temas 618 e 619/STJ (repetitivo); Súmula 565/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106302421
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Leading case: desde 30/04/2008 a TAC e a TEC não têm mais respaldo legal para pessoa física (2ª tese), de modo que a cobrança em contrato posterior é ilegal.
- observacao: Publicação pela data do Jusbrasil (confere com o DJe de 24/10/2013 citado em acórdão do TJPR). Numeração conferida no site do STJ em 28/10/2026: os dois REsps são paradigmas dos Temas 618 (validade até 30/04/2008), 619 (vedação de TAC e TEC desde 30/04/2008, o que a peça cita) e 620 (tarifa de cadastro). Limites que viram ressalva na peça: era válida a TAC/TEC em contratos até 30/04/2008 (ressalvado abuso em concreto); a Tarifa de Cadastro permanece válida no início do relacionamento (Súmula 566/STJ); a vedação é para pessoa física (TAC em contrato com pessoa jurídica é admitida, inclusive nos TJs).

ementa:
> CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. CONTRATO DE FINANCIAMENTO COM GARANTIA DE ALIENAÇÃO FIDUCIÁRIA.
> DIVERGÊNCIA. CAPITALIZAÇÃO DE JUROS. JUROS COMPOSTOS. MEDIDA PROVISÓRIA 2.170-36/2001. RECURSOS REPETITIVOS.
> CPC, ART. 543-C. TARIFAS ADMINISTRATIVAS PARA ABERTURA DE CRÉDITO (TAC), E EMISSÃO DE CARNÊ (TEC). EXPRESSA
> PREVISÃO CONTRATUAL. COBRANÇA. LEGITIMIDADE. PRECEDENTES. MÚTUO ACESSÓRIO PARA PAGAMENTO PARCELADO DO IMPOSTO
> SOBRE OPERAÇÕES FINANCEIRAS (IOF). POSSIBILIDADE. 1. "A capitalização dos juros em periodicidade inferior à
> anual deve vir pactuada de forma expressa e clara. A previsão no contrato bancário de taxa de juros anual
> superior ao duodécuplo da mensal é suficiente para permitir a cobrança da taxa efetiva anual contratada" (2ª
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
> 543-C do CPC: - 1ª Tese: Nos contratos bancários celebrados até 30.4.2008 (fim da vigência da Resolução CMN
> 2.303/96) era válida a pactuação das tarifas de abertura de crédito (TAC) e de emissão de carnê (TEC), ou
> outra denominação para o mesmo fato gerador, ressalvado o exame de abusividade em cada caso concreto. - 2ª
> Tese: Com a vigência da Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços bancários prioritários
> para pessoas físicas ficou limitada às hipóteses taxativamente previstas em norma padronizadora expedida pela
> autoridade monetária. Desde então, não mais tem respaldo legal a contratação da Tarifa de Emissão de Carnê
> (TEC) e da Tarifa de Abertura de Crédito (TAC), ou outra denominação para o mesmo fato gerador. Permanece
> válida a Tarifa de Cadastro expressamente tipificada em ato normativo padronizador da autoridade monetária, a
> qual somente pode ser cobrada no início do relacionamento entre o consumidor e a instituição financeira. - 3ª
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
- julgamento: 2024-04-08
- publicacao: 2024-04-09
- precedente_qualificado: Súmula 565/STJ
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000027588211/Ac%C3%B3rd%C3%A3o-0003835-59.2023.8.16.0069
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O TJPR declara inexigível e manda restituir a TAC cobrada em financiamento firmado após 30/04/2008, aplicando a Súmula 565/STJ.
- observacao: Turma Recursal (Juizado Especial), não Câmara Cível. A ementa mistura outros pontos (seguro e tarifa DOC/TED não contratados); o ponto da TAC é o descrito na ementa e no voto (contrato de 04/11/2020). Publicação pela data do Jusbrasil. Conferido no portal do TJPR em 29/10/2026: ementa e dados batem; ajustes: julgamento em 08/04/2024 (o Jusbrasil indicava 05/04/2024); link permanente do portal.

ementa:
> RECURSO INOMINADO. BANCÁRIO. DESCONTOS EM CONTA BANCÁRIA SOB A RUBRICA “BRADESCO VIDA E PREVIDÊNCIA” E
> “DOC/TED INTERNE”. AUSÊNCIA DE CONTRATAÇÃO. RESTITUIÇÃO DEVIDA. TARIFA DE ABERTURA DE CRÉDITO (TAC).
> INEXIGIBILIDADE DA COBRANÇA. CONTRATO FIRMADO APÓS 30.04.2008. INTELIGÊNCIA DA SÚMULA N. 565 DO SUPERIOR
> TRIBUNAL DE JUSTIÇA. INSURGÊNCIA ATINENTE AO DANO MORAL. MATÉRIA NÃO DISCUTIDA NO CASO CONCRETO, TAMPOUCO
> OBJETO DA SENTENÇA. NÃO CONHECIMENTO DO RECURSO NESSE PONTO. SENTENÇA MANTIDA. RECURSO CONHECIDO EM PARTE E,
> NA PARTE CONHECIDA, DESPROVIDO.

### TJPR · Apelação Cível 0018393-15.2024.8.16.0194
- regras: R04
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0018393-15.2024.8.16.0194
- orgao: 14ª Câmara Cível
- relator: Des. Fabio Luis Franco
- julgamento: 2026-08-17
- publicacao: 2026-08-19
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037665071/Ac%C3%B3rd%C3%A3o-0018393-15.2024.8.16.0194
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 14ª Câmara Cível mantém a ilegalidade da TAC cobrada em cédula posterior a 30/04/2008 e a restituição do valor, pela Súmula 565/STJ, mesmo quando o contratante é empresário individual com CNPJ.
- observacao: Embargos à execução de cédula de crédito bancário; apelo do banco provido em parte, mas desprovido quanto à TAC (0,5% do crédito, em operação posterior a 30/04/2008). O contratante é empresário individual, equiparado à pessoa física por não haver personalidade jurídica distinta. No mesmo acórdão o seguro prestamista foi tido por facultativo (instrumento apartado) e a cumulação de encargos moratórios foi admitida: não citar para R13. A ementa invoca o "Tema 619", que é de fato o da vedação de TAC e TEC desde 30/04/2008 (conferido no site do STJ). Correções na ementa: retirado o rótulo inicial "Ementa:"; inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). As 13ª a 16ª Câmaras declaram lícita a TAC em contrato de pessoa jurídica: a peça precisa provar que o contratante é pessoa física ou empresário individual.

ementa:
> DIREITO BANCÁRIO. APELAÇÃO CÍVEL. EMBARGOS À EXECUÇÃO. CÉDULA DE CRÉDITO BANCÁRIO. INSURGÊNCIA RECURSAL DA INSTITUIÇÃO FINANCEIRA PARA ALTERAR A SENTENÇA EM RELAÇÃO À COBRANÇA DO SEGURO PRESTAMISTA, DA TARIFA DE ABERTURA DE CRÉDITO (TAC) E DOS ENCARGOS MORATÓRIOS. SENTENÇA MANTIDA APENAS PARA MANTER A ILEGALIDADE DA COBRANÇA DA TARIFA DE ABERTURA DE CRÉDITO (TAC). RECURSO CONHECIDO E PROVIDO EM PARTE. I. CASO EM EXAME 1. Trata-se de Apelação Cível interposta pela instituição financeira exequente/embargada nos autos de Embargos à Execução, contra sentença que julgou parcialmente procedentes os pedidos iniciais do embargante/executado/apelado para: (i) reconhecer a prática de venda casada na contratação de seguro prestamista, com restituição em dobro dos valores; (ii) declarar abusiva a cobrança da Tarifa de Abertura de Crédito (TAC), com repetição do indébito; e (iii) afastar a cumulação de encargos no período de inadimplência, determinando o recálculo do débito. II. QUESTÃO EM DISCUSSÃO 2. Há três questões em discussão: (i) saber se a contratação do seguro prestamista configurou venda casada; (ii) saber se é lícita a cobrança da Tarifa de Abertura de Crédito (TAC) em operação celebrada por pessoa jurídica após 30/04/2008; e (iii) saber se é admissível a cumulação de juros remuneratórios, juros moratórios e multa no período de inadimplência, na ausência de comissão de permanência. III. RAZÕES DE DECIDIR 3. Não configurada venda casada do seguro prestamista, quando demonstrada a contratação facultativa, por meio de instrumento apartado, com ciência do consumidor, em consonância com a tese firmada no Tema 972 do Superior Tribunal de Justiça. 4. A Tarifa de Abertura de Crédito (TAC), por sua vez, não é válida em contratos celebrados com pessoa física após 30/04/2008, conforme entendimento consolidado do Superior Tribunal de Justiça (Tema 619 e Súmula 565). Ainda que o contratante possua inscrição no CNPJ, sendo empresário individual, não há personalidade jurídica distinta, equiparando-se à pessoa física, razão pela qual se mantém a ilegalidade da cobrança. 5. É lícita a cumulação de juros remuneratórios, juros de mora e multa contratual no período de inadimplência, quando inexistente comissão de permanência, por se tratarem de encargos de naturezas jurídicas distintas, conforme orientação pacífica do Superior Tribunal de Justiça. IV. DISPOSITIVO E TESE 6. Recurso conhecido e provido em parte. Tese de julgamento: “1. Não há venda casada na contratação de seguro prestamista quando a adesão é facultativa e formalizada em instrumento apartado.” “2. É indevida a cobrança de Tarifa de Abertura de Crédito (TAC) em contratos firmados com pessoa física após 30/04/2008, inclusive quando se tratar de empresário individual.” “3. É lícita a cumulação de juros remuneratórios, juros moratórios e multa no período de inadimplência, desde que inexistente comissão de permanência, por serem verbas de naturezas e com propósitos distintos.” Dispositivos relevantes citados: CPC, Arts. 1.009, 1.012, §1º, inc. III, 85, §§1º, 2º e 11; CDC, Art. 39, inc. I; CC, Arts. 389 e 406.Jurisprudência relevante citada: STJ – REsp 1.639.320/SP – Segunda Seção – Rel. Min. Paulo de Tarso Sanseverino – j. 12.12.2018; STJ – REsp 1.251.331/RS – Segunda Seção – Rel. Min. Maria Isabel Gallotti – j. 28.08.2013; STJ – REsp 2.200.904/SP – Quarta Turma – Rel. Min. Raul Araújo – j. 09.03.2026; STJ – REsp 2.104.438/SC – Terceira Turma – Rel. Min. Nancy Andrighi – j. em 24/9/2024; STJ – AgInt no AREsp 2.366.106/PB – Quarta Turma – Rel. Min. João Otávio de Noronha – j. 22/4/2024; STJ –AREsp n. 3.032.459/GO – Terceira Turma – Rel. Min Moura Ribeiro – j. 9/2/2026; TJPR – 16ª Câmara Cível – 0057094-96.2011.8.16.0001 – Rel.: Desembargador Marco Antonio Massaneiro – J. 25.05.2026; TJPR – 14ª Câmara Cível – 0005067-11.2022.8.16.0112 – Rel.: Desembargadora Josely Dittrich Ribas – J. 29.07.2024; TJPR – 14ª Câmara Cível – 0028248-88.2019.8.16.0001 – Rel.: Desembargador João Antônio De Marchi – J. 21.03.2022; TJPR – 16ª Câmara Cível – 0000508-47.2026.8.16.0087 – Rel.: Desembargador Luiz Henrique Miranda – J. 18.05.2026; TJPR – 14ª Câmara Cível – 0024317-92.2020.8.16.0017 Rel.: Desembargadora Josely Dittrich Ribas – J. 05.08.2025.

### TJPR · Apelação Cível 0003113-44.2016.8.16.0045
- regras: R04
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0003113-44.2016.8.16.0045
- orgao: 15ª Câmara Cível
- relator: Des.ª Denise Kruger Pereira
- julgamento: 2026-07-25
- publicacao: 2026-07-28
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038413341/Ac%C3%B3rd%C3%A3o-0003113-44.2016.8.16.0045
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 15ª Câmara Cível declara indevida a TAC cobrada de pessoa física em duas cédulas posteriores a 30/04/2008 (Súmula 565/STJ) e manda restituir, em dobro as parcelas pagas depois de 30/03/2021.
- observacao: Apelo do banco parcialmente provido (só no ponto dos juros remuneratórios, mantidos por não superarem o triplo da média); a TAC permaneceu ilegal. Restituição simples até 30/03/2021 e em dobro depois. A ementa registra "03.04.2008" na tese de julgamento, erro evidente de digitação (o corpo da ementa e o voto citam 30.04.2008); aqui, corrigido. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (mesmo objeto, mesmas duas cédulas e mesma comarca) e por embargos de declaração posteriores, rejeitados, que reafirmam a ilegalidade da TAC. Correções na ementa: retirado o rótulo inicial "EMENTA:"; juntadas 7 quebras de linha que o portal inseriu no meio de frases; inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Arapongas).

ementa:
> RECURSO DE APELAÇÃO. AÇÃO DE EXIBIÇÃO DE DOCUMENTOS CUMULADA COM PEDIDO DE TUTELA ANTECIPADA, REVISIONAL DE CLÁUSULAS, REPETIÇÃO DE INDÉBITO E INDENIZAÇÃO POR DANOS MORAIS DECORRENTE DE COBRANÇAS INDEVIDAS E ABUSIVAS. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSO DO BANCO REQUERIDO. PRELIMINARMENTE. INÉPCIA DA PETIÇÃO INICIAL. INOCORRÊNCIA. REQUISITOS DO ART. 330, § 2º, DO CPC PREENCHIDOS. MÉRITO. JUROS REMUNERATÓRIOS. ABUSIVIDADE AFASTADA. PERCENTUAL QUE NÃO ULTRAPASSA O TRIPLO DA MÉDIA DE MERCADO.
> TARIFA DE ABERTURA DE CRÉDITO – TAC. COBRANÇA INDEVIDA. CONTRATOS FIRMADOS APÓS 30.04.2008. REPETIÇÃO DE VALORES. CONSEQUÊNCIA LÓGICA. REPETIÇÃO EM DOBRO. OCORRÊNCIA PARA COBRANÇAS POSTERIORES A 30.03.2021. RECURSO PARCIALMENTE PROVIDO. I. CASO EM EXAME 1. Recurso de Apelação interposto contra sentença que julgou parcialmente procedentes os pedidos presentes na petição inicial, determinando a readequação da taxa de juros em dois contratos específicos. II. QUESTÃO EM DISCUSSÃO 2. A questão em discussão consiste em saber se é cabível a adequação da taxa de juros dos contratos. III. RAZÕES DE DECIDIR 3. Preliminarmente, não se configura a inépcia da petição inicial, já que preenchidos os requisitos do art. 330, § 2º, do CPC. 4. No mérito, não se constata a abusividade da taxa de juros que não excedam o triplo da média de mercado, já que essa margem respeita a liberalidade das instituições financeiras em atribuir o percentual que melhor se enquadra em sua atuação no ramo financeiro. 5. Quanto à Tarifa de Abertura de Crédito – TAC, sua cobrança se mostra indevida, já que os contratos foram firmados por pessoa física e após 30.04.2008, com fulcro na Súmula 565/STJ. 6. Em atenção ao entendimento vinculante do STJ, parte da restituição do indébito deve ser feita na forma simples, notadamente em relação aos descontos indevidos realizados até 30.03.2021, e, após essa data, em dobro. IV. DISPOSITIVO E TESE 7. Recurso parcialmente provido. Tese de julgamento: Não se mostra abusiva a taxa de juros que não ultrapassa o triplo da média de mercado. A cobrança de Tarifa de Abertura de Crédito – TAC se mostra indevida para contratos firmados com pessoa física após 30.04.2008._________ Dispositivos relevantes citados: CPC, art. 330, § 2º, 1.012; CDC, art. 14 e 42.Jurisprudência relevante citada: TJPR - 15ª Câmara Cível - 0021742-91.2022.8.16.0001 - Curitiba - Rel.: DESEMBARGADOR LUIZ CEZAR NICOLAU - J. 22.02.2025; STJ, REsp n. 1.061.530/RS, relatora Ministra Nancy Andrighi, Segunda Seção, julgado em 22/10/2008, DJe de 10/3/2009; TJPR - 15ª Câmara Cível - 0001461-57.2025.8.16.0083 - Francisco Beltrão - Rel.: SUBSTITUTO DAVI PINTO DE ALMEIDA - J. 13.06.2026; TJPR - 15ª Câmara Cível - 0001384-66.2026.8.16.0098 - Jacarezinho - Rel.: DESEMBARGADOR JUCIMAR NOVOCHADLO - J. 23.05.2026; TJPR - 15ª Câmara Cível - 0011789-14.2022.8.16.0160 - Sarandi - Rel.: SUBSTITUTO DAVI PINTO DE ALMEIDA - J. 23.05.2026; STJ, REsp n. 1.251.331/RS, relatora Ministra Maria Isabel Gallotti, Segunda Seção, julgado em 28/8/2013, DJe de 24/10/2013; TJPR - 15ª Câmara Cível - 0003843-93.2023.8.16.0050 - Bandeirantes - Rel.: DESEMBARGADOR JUCIMAR NOVOCHADLO - J. 31.05.2025; TJPR - 15ª Câmara Cível - 0004862-82.2021.8.16.0090 - Ibiporã - Rel.: DESEMBARGADOR LUIZ CARLOS GABARDO - J. 07.05.2025. Súmula 565/STJ.

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
- precedente_qualificado: Temas 618 e 619/STJ (repetitivo); Súmula 565/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106299943
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Repetitivo gêmeo do REsp 1.251.331/RS: a TEC e a TAC deixaram de ser pactuáveis em contratos posteriores a 30/04/2008, e a cobrança só é lícita nos contratos até essa data.
- observacao: Publicação pela data do Jusbrasil. Tema 619 conferido no site do STJ em 28/10/2026 (ver observação do REsp 1.251.331/RS). Mesmos limites: validade até 30/04/2008, Tarifa de Cadastro lícita (Súmula 566/STJ), vedação voltada à pessoa física. A ementa também trata de comissão de permanência e financiamento do IOF.

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
> efeitos do art. 543-C do CPC: - 1ª Tese: Nos contratos bancários celebrados até 30.4.2008 (fim da vigência da
> Resolução CMN 2.303/96) era válida a pactuação das tarifas de abertura de crédito (TAC) e de emissão de carnê
> (TEC), ou outra denominação para o mesmo fato gerador, ressalvado o exame de abusividade em cada caso
> concreto. - 2ª Tese: Com a vigência da Resolução CMN 3.518/2007, em 30.4.2008, a cobrança por serviços
> bancários prioritários para pessoas físicas ficou limitada às hipóteses taxativamente previstas em norma
> padronizadora expedida pela autoridade monetária. Desde então, não mais tem respaldo legal a contratação da
> Tarifa de Emissão de Carnê (TEC) e da Tarifa de Abertura de Crédito (TAC), ou outra denominação para o mesmo
> fato gerador. Permanece válida a Tarifa de Cadastro expressamente tipificada em ato normativo padronizador da
> autoridade monetária, a qual somente pode ser cobrada no início do relacionamento entre o consumidor e a
> instituição financeira. - 3ª Tese: Podem as partes convencionar o pagamento do Imposto sobre Operações
> Financeiras e de Crédito (IOF) por meio de financiamento acessório ao mútuo principal, sujeitando-o aos mesmos
> encargos contratuais. 11 . Recurso especial conhecido e parcialmente provido.

### TJPR · Apelação Cível 0006181-03.2011.8.16.0069
- regras: R06, R09, R13
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0006181-03.2011.8.16.0069
- orgao: 17ª Câmara Cível
- relator: Des.ª Dilmari Helena Kessler
- julgamento: 2023-12-04
- publicacao: 2023-12-18
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000025414751/Ac%C3%B3rd%C3%A3o-0006181-03.2011.8.16.0069
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 17ª Câmara Cível manda restituir a TEC de financiamento posterior a 30/04/2008 e, no mesmo acórdão, reconhece a venda casada do seguro prestamista (Tema 972/STJ) e a abusividade dos serviços de terceiros sem especificação.
- observacao: Revisional de financiamento de veículo. Apelo do banco desprovido na parte conhecida (TEC, tarifa de avaliação do bem e tarifa de aditamento de contrato, com restituição devida); apelo dos autores provido (seguro prestamista imposto, serviços de terceiros sem especificação e juros reflexos). A ementa grafa "Resolução CNM 518/2007" e "RESP 1.578.526/SP" (as referências corretas são Res. CMN 3.518/2007 e REsp 1.578.553/SP); mantido como no portal. Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Cianorte).

ementa:
> APELAÇÃO CÍVEL – AÇÃO DE REVISÃO DE CONTRATO DE FINANCIAMENTO DE VEÍCULO – SENTENÇA DE PARCIAL PROCEDÊNCIA. APELAÇÃO 1 (REQUERIDO): PARCIAL CONHECIMENTO – ALEGADA AUSÊNCIA DE ABUSIVIDADE NA COBRANÇA DA TAC E DA TARIFA DE CADASTRO - AUSÊNCIA DE CONDENAÇÃO – FALTA DE INTERESSE RECURSAL – RECURSO NÃO CONHECIDO NESTE PONTO – MÉRITO – ALEGADA VALIDADE DA COBRANÇA DE TARIFA DE EMISSÃO DE CARNÊ (TEC) – CONTRATO FIRMADO POSTERIORMENTE À RESOLUÇÃO CNM 518/2007 – ENTENDIMENTO EXARADO NO RESP Nº 1.255.573/RS – RESTITUIÇÃO DE VALORES DEVIDA – ALEGADA LEGALIDADE DA COBRANÇA DA TARIFA DE AVALIAÇÃO DO BEM – NÃO ACOLHIMENTO – AUSÊNCIA DE DEMONSTRAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO PELO APELANTE – TARIFA DE ADITAMENTO DE CONTRATO – ABUSIVIDADE – EQUIPARAÇÃO À COBRANÇA DA TARIFA DE CADASTRO, A QUAL É PERMITIDA UMA ÚNICA VEZ, NO INÍCIO DA RELAÇÃO CONTRATUAL – SÚMULA 566 DO STJ – COBRANÇA REALIZADA NO CONTRATO ORIGINAL – ABUSIVIDADE RECONHECIDA – DECISÃO MANTIDA. RECURSO PARCIALMENTE CONHECIDO E, NESTA EXTENSÃO, DESPROVIDO. APELAÇÃO 2 (AUTORES): ALEGADA ABUSIVIDADE NA COBRANÇA DE SEGURO PRESTAMISTA – ACOLHIMENTO – CONSUMIDOR, ORA APELANTE, QUE FOI COMPELIDO A CONTRATAR A SEGURADORA INDICADA PELA INSTITUIÇÃO FINANCEIRA – INTELIGÊNCIA DO TEMA Nº 972, DO STJ – AUSÊNCIA DE DEMONSTRAÇÃO DE QUE FORA POSSIBILITADA AO APELANTE A ESCOLHA DE OUTRA SEGURADORA – ÔNUS DA INSTITUIÇÃO BANCÁRIA – VENDA CASADA – COBRANÇA INDEVIDA – PRECEDENTES DESTE TRIBUNAL – NECESSIDADE DE DEVOLUÇÃO DOS VALORES E SEUS REFLEXOS – PEDIDO DE RECONHECIMENTO DE ABUSIVIDADE DOS SERVIÇOS DE TERCEIROS – INEXISTÊNCIA DE ESPECIFICAÇÃO QUANTO A QUEM SERÁ DESTINADO O REFERIDO VALOR, A UTILIDADE, NECESSIDADE, OU MOTIVO DE SUA COBRANÇA – ILEGALIDADE CONSTATADA – INTELIGÊNCIA DO ENTENDIMENTO DO RESP Nº 1.578.526/SP – PRECEDENTES DESTA CORTE – PLEITO DE RESTITUIÇÃO DOS JUROS REFLEXOS, INCIDENTES SOBRE OS VALORES INDEVIDAMENTE COBRADOS – ACOLHIMENTO – PEDIDO DE INVERSÃO DO ÔNUS SUCUMBENCIAL – PROVIMENTO – PARTE AUTORA QUE DECAIU MINIMAMENTE EM SEUS PEDIDOS – REDISTRIBUIÇÃO DA SUCUMBÊNCIA – DECISÃO REFORMADA. RECURSO CONHECIDO E PROVIDO.

### TJPR · Apelação Cível 0010629-97.2009.8.16.0001
- regras: R06, R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0010629-97.2009.8.16.0001
- orgao: 18ª Câmara Cível
- relator: Des. Vitor Roberto Silva
- julgamento: 2024-01-08
- publicacao: 2024-01-08
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000025022311/Ac%C3%B3rd%C3%A3o-0010629-97.2009.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 18ª Câmara Cível declara ilegal a TEC (lançada como "serviço de recebimento por parcela") em contrato posterior a 30/04/2008 e os serviços de terceiros sem especificação, com devolução dos valores e dos juros reflexos.
- observacao: Apelo da consumidora parcialmente provido: tarifa de cadastro e tarifa de registro de contrato foram mantidas como lícitas; TEC e serviços de terceiros, declarados ilegais. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (ementa e voto tratam das mesmas tarifas e do mesmo desfecho). Sem correções na ementa. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO. SENTENÇA DE PARCIAL PROCEDÊNCIA. APELO DA AUTORA. COBRANÇA DE RESSARCIMENTO DE SERVIÇOS DE TERCEIROS. AUSÊNCIA DE ESPECIFICAÇÃO DOS SERVIÇOS NO CONTRATO. ILEGALIDADE CONFIGURADA. TARIFA DE CADASTRO. POSSIBILIDADE DE COBRANÇA NO INÍCIO DO RELACIONAMENTO ENTRE O CONSUMIDOR E A INSTITUIÇÃO FINANCEIRA. VALOR NÃO ABUSIVO. ILEGALIDADE NÃO COMPROVADA. TARIFA DE REGISTRO DO CONTRATO. PACTUAÇÃO LÍCITA. EFETIVA PRESTAÇÃO DO SERVIÇO QUE SE OBSERVA NO DOCUMENTO DO VEÍCULO. ONEROSIDADE EXCESSIVA NÃO CONSTATADA NO CASO CONCRETO. TARIFA DE EMISSÃO DE CARNÊ (TEC). CONTRATO CELEBRADO APÓS 30.04.2008. ABUSIVIDADE CONSTATADA. RESOLUÇÃO 3.518/07 E CIRCULAR N° 3.371/07 - BACEN. JUROS REFLEXOS. PRETENSÃO QUE NÃO CARACTERIZA INOVAÇÃO RECURSAL. MERO DESDOBRAMENTO DO ACOLHIMENTO DO PEDIDO, AINDA QUE PARCIALMENTE. VALORES QUE, POR ESTAREM INSERIDOS NO FINANCIAMENTO, SÃO COBRADOS COM A INCIDÊNCIA DOS JUROS CONTRATADOS. DEVOLUÇÃO QUE DEVE ABRANGER TODO O VALOR PAGO INDEVIDAMENTE. HONORÁRIOS FIXADOS AO PATRONO DO APELADO. AUSÊNCIA DE EXCESSO. RECURSO CONHECIDO E PARCIALMENTE PROVIDO.

### TJPR · Apelação Cível 0001194-62.2010.8.16.0099
- regras: R06, R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001194-62.2010.8.16.0099
- orgao: 6ª Câmara Cível
- relator: Des.ª Lilian Romero
- julgamento: 2021-06-14
- publicacao: 2021-06-17
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000017169481/Ac%C3%B3rd%C3%A3o-0001194-62.2010.8.16.0099
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 6ª Câmara Cível aplica os Temas 618 e 619/STJ e mantém a restituição da TEC ("serviço de recebimento por parcela") de contrato firmado em 17/09/2008, além de afastar os serviços de terceiros não especificados.
- observacao: Julgado de 2021 (fora da preferência por 2023+), mas é a única Câmara adicional com TEC em contrato de 2008 e leitura direta dos repetitivos. Apelo do banco provido em parte, apenas para validar o IOF financiado; mantida a sentença quanto aos demais encargos, inclusive TEC. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (mesmo objeto e desfecho da ementa). Sem correções na ementa. Fonte: portal de jurisprudência do TJPR (comarca de Jaguapitã).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO, COM GARANTIA DE ALIENAÇÃO FIDUCIÁRIA. (I)
> COBRANÇA DE SERVIÇO DE TERCEIRO NÃO ESPECIFICADO. SERVIÇO NÃO COMPROVADO E NEM INFORMADO AO CONSUMIDOR. ABUSIVIDADE CONFIGURADA. AFASTAMENTO DA TAXA. RESP REPETITIVO Nº 1.578.553/SP (TEMA 958). (II) TEC (TARIFA DE EMISSÃO DE CARNÊ) DENOMINADA SERVIÇO DE RECEBIMENTO POR PARCELA. CONTRATAÇÃO POSTERIOR A 30.04.2008. ABUSIVIDADE DA COBRANÇA RECONHECIDA. RESP REPETITIVO 1.251.331/RS (TEMAS 618 E 619).
> (III) TRIBUTO SOBRE A OPERAÇÃO (IOF) FINANCIADO. PACTUAÇÃO EXPRESSA. ADMISSIBILIDADE. APLICAÇÃO DO ENTENDIMENTO FIRMADO NOS RECURSOS ESPECIAIS REPRESENTATIVOS DA CONTROVÉRSIA Nº 1.251.331/RS E Nº 1.255.573/RS (TEMA 621). SENTENÇA PONTUALMENTE REFORMADA. RECURSO PROVIDO EM PARTE.

## R08 — Tarifa de cadastro — duplicada ou em renovação

Tese: A tarifa de cadastro remunera a pesquisa cadastral do início do relacionamento e só pode ser cobrada uma vez, no início do relacionamento entre o consumidor e a instituição financeira (Súmula 566/STJ; Tema 620/STJ, 2ª tese do REsp 1.251.331/RS); cobrada de novo em contrato posterior, renovação ou refinanciamento com a mesma instituição, quando o relacionamento já existia, é indevida e deve ser restituída — e cabe à instituição, que guarda os próprios registros, provar que a cobrança se deu no início do relacionamento.

Nota: o leading case é o REsp 1.251.331/RS (Segunda Seção, Temas 618 a 620), cuja 2ª tese diz que a tarifa de cadastro "somente pode ser cobrada no início do relacionamento"; ele está listado sob a R04.

### STJ · AgInt no REsp 2.007.638/MS
- regras: R08
- posicao: ADV
- tribunal: STJ
- classe_numero: AgInt no REsp 2.007.638/MS
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2023-05-29
- publicacao: 2023-06-01
- precedente_qualificado: não (aplica o Tema 620/STJ e a Súmula 566/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1908224031
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva: a Quarta Turma reafirma que a tarifa de cadastro pactuada é válida e só pode ser cobrada no início do relacionamento (Tema 620), mas manteve a cobrança porque o tribunal de origem não viu elementos de relacionamento anterior, e só admite revisão do valor com demonstração cabal de abuso; a petição deve juntar a prova do vínculo anterior (contrato antigo, extrato, ficha de conta) ou pedir a exibição dos registros do banco, e não pode basear-se apenas na comparação com a tarifa média.
- observacao: Busca e apreensão com reconvenção revisional; agravo da consumidora desprovido (Súmula 83/STJ). O voto transcreve o TJMS: "não merece prosperar a assertiva de que a cobrança não teria ocorrido no início do relacionamento, pois, além de não haver elementos nesse sentido, referida taxa foi expressamente contratada". Sessão virtual de 23 a 29/05/2023. Publicação pela data do Jusbrasil (01/06/2023, data da lista de resultados; o inteiro teor não traz o DJe; o JSON-LD da página marca 24/07/2023, data de indexação). Ementa copiada da seção Ementa da página, igual à do inteiro teor salvo duas quebras de linha que o PDF inseriu no meio de frases.

ementa:
> AGRAVO INTERNO EM RECURSO ESPECIAL. AÇÃO DE BUSCA E APREENSÃO. RECONVENÇÃO. REVISÃO DO CONTRATO. JUROS REMUNERATÓRIOS. LIMITAÇÃO. ABUSIVIDADE DA TAXA CONTRATADA. DEMONSTRAÇÃO CABAL. NÃO OCORRÊNCIA. REVISÃO. IMPOSSIBILIDADE. SÚMULAS N. 5 E 7 DO STJ. TARIFA DE CADASTRO. SÚMULA N. 83 DO STJ. AGRAVO INTERNO DESPROVIDO.
> 1. Admite-se a revisão da taxa de juros remuneratórios excepcionalmente, quando ficar caracterizada a relação de consumo e a abusividade for devidamente demonstrada diante das peculiaridades do caso concreto.
> 2. O fato de a taxa contratada de juros remuneratórios estar acima da taxa média de mercado, por si só, não configura abusividade, devendo ser observados, para a limitação dos referidos juros, fatores como o custo de captação dos recursos, o spread da operação, a análise de risco de crédito do contratante, ponderando-se a caracterização da relação de consumo e eventual desvantagem exagerada do consumidor.
> 3. É inviável limitar a taxa de juros remuneratórios pactuada em contrato quando a corte de origem não tenha considerado cabalmente demonstrada sua abusividade com base nas peculiaridades do caso concreto. Incidência das Súmulas n. 5 e 7 do STJ.
> 4. A tarifa de cadastro pactuada é válida, podendo ser cobrada apenas no início do relacionamento contratual, conforme o Tema n. 620 do STJ.
> 5. Afasta-se eventual abuso na pactuação da tarifa de cadastro apenas na hipótese em que é cabalmente demonstrada abusividade no caso concreto, como ocorre na avaliação dos juros remuneratórios, isto é, mediante a análise das circunstâncias do caso, comparando-se os preços cobrados no mercado, o tipo de operação e o canal de contratação.
> 6. Para o reconhecimento da abusividade das tarifas administrativas, não se admitem a referência a conceitos jurídicos abstratos nem a convicção subjetiva do magistrado.
> 7. Agravo interno desprovido.

### TJPR · Apelação Cível 0010776-21.2022.8.16.0017
- regras: R08
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0010776-21.2022.8.16.0017
- orgao: 5ª Câmara Cível
- relator: Juiz Subst. 2º Grau Anderson Ricardo Fogaça
- julgamento: 2026-02-18
- publicacao: 2026-08-13
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000025593041/Ac%C3%B3rd%C3%A3o-0010776-21.2022.8.16.0017
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Caso-modelo da regra: dois financiamentos de veículo com a mesma instituição (2011 e 2019); a tarifa de cadastro do primeiro foi mantida e a do segundo declarada ilegal (Súmula 566 e Tema 620/STJ), com restituição; o banco admitira na contestação o relacionamento anterior.
- observacao: Recurso do consumidor parcialmente provido. O mesmo acórdão afasta a tarifa de avaliação (documento só com fotos externas e descrição genérica, e valor acima do praticado) — serve também à R11, mas não foi listado em `regras` para não passar de dois julgados locais por regra (a R11 tem dois acórdãos fundados só na falta de prova do serviço). Restituição simples porque a Câmara exigiu má-fé para o dobro — orientação superada pelo Tema 929/STJ; não citar este acórdão para a forma da restituição. A tarifa de registro foi mantida (serviço comprovado). Datas do portal: julgamento 18/02/2026 e publicação 13/08/2026. Correções na ementa: separados os títulos e itens que a extração emendou (ex.: "PROVIDOS.I. CASO EM EXAME1.1"), sem alterar o texto. Fonte: portal de jurisprudência do TJPR (comarca de Maringá).

ementa:
> DIREITO CIVIL. APELAÇÕES CÍVEIS. AÇÃO REVISIONAL CUMULADA COM REPETIÇÃO DE INDÉBITO. CONTRATOS DE FINANCIAMENTO DE VEÍCULO. COBRANÇA DE TARIFA DE CADASTRO EM CONTRATO POSTERIOR AO INÍCIO DO RELACIONAMENTO. ILEGALIDADE. TEMA 620/STJ E SÚMULA 566/STJ. TARIFA DE REGISTRO DE CONTRATO. LEGALIDADE. TEMA 958/STJ. TARIFA DE AVALIAÇÃO DO BEM. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO. ILEGALIDADE. SEGURO DE PROTEÇÃO FINANCEIRA. VENDA CASADA. TEMA 972/STJ. RESTITUIÇÃO SIMPLES A PARTIR DA CITAÇÃO. RECURSOS CONHECIDOS E PARCIALMENTE PROVIDOS.
> I. CASO EM EXAME
> 1.1 Ação revisional cumulada com repetição de indébito proposta por consumidor em face de instituição financeira, em razão de dois contratos de financiamento de veículo firmados em 2011 e 2019.
> 1.2 No primeiro contrato, cobrada tarifa de cadastro; no segundo, novas cobranças de tarifa de cadastro, tarifa de avaliação do bem, tarifa de registro do contrato e seguro de proteção financeira.
> 1.3 Sentença de parcial procedência para declarar a abusividade do seguro de proteção financeira e condenar à restituição simples do valor pago; improcedência dos demais pedidos.
> 1.4 Apelação do autor pleiteando a declaração de abusividade de todas as tarifas e devolução em dobro dos valores pagos; recurso da instituição financeira requerendo o afastamento da condenação relativa ao seguro de proteção financeira.
> II. QUESTÕES EM DISCUSSÃO
> 2.1 Há quatro questões em discussão: (i) se é válida a cobrança da tarifa de cadastro em contrato celebrado posteriormente ao início do relacionamento contratual; (ii) se é legítima a cobrança da tarifa de registro do contrato; (iii) se a tarifa de avaliação do bem, diante de laudo genérico, é devida; (iv) se a contratação do seguro de proteção financeira com seguradora indicada pelo banco configura venda casada.
> III. RAZÕES DE DECIDIR
> 3.1 A cobrança da tarifa de cadastro somente é válida no início do relacionamento entre consumidor e instituição financeira, nos termos da Súmula 566 e do Tema 620 do STJ, sendo ilegal sua repetição em contrato posterior, impondo-se a restituição simples do valor pago.
> 3.2 A tarifa de registro do contrato é considerada legítima quando prevista contratualmente, de valor razoável e efetivamente prestado o serviço, requisitos preenchidos no caso, nos termos do Tema 958/STJ.
> 3.3 A tarifa de avaliação do bem exige demonstração da efetiva prestação do serviço. Laudo genérico e superficial, sem descrição técnica do estado do veículo, configura cobrança indevida, devendo haver restituição simples do valor pago.
> 3.4 A contratação de seguro de proteção financeira com seguradora indicada pela instituição financeira, sem possibilidade de escolha pelo consumidor, caracteriza venda casada, prática vedada pelo art. 39, I, do CDC e pelo Tema 972 do STJ, impondo-se a restituição dos valores pagos a partir da citação.
> 3.5 A repetição do indébito em dobro exige demonstração de má-fé, o que não restou evidenciado, motivo pelo qual a devolução será simples.
> 3.6 Diante do provimento parcial dos recursos, impõe-se a redistribuição dos ônus sucumbenciais, observando-se os ganhos e perdas das partes.
> IV. DISPOSITIVO E TESE
> 4.1 Recurso do autor CONHECIDO E PARCIALMENTE PROVIDO para declarar a ilegalidade da cobrança da tarifa de cadastro no contrato de 2019 e da tarifa de avaliação do bem, com restituição simples dos valores pagos, corrigidos pelo IPCA-E desde a cobrança e acrescidos de juros de mora de 1% ao mês a partir da citação.
> 4.2 Recurso da instituição financeira CONHECIDO E PARCIALMENTE PROVIDO exclusivamente para limitar a restituição dos valores pagos a título de seguro de proteção financeira às parcelas quitadas a partir da citação, mantido o reconhecimento da abusividade da cobrança.
> 4.3 Tese de julgamento: “É indevida a cobrança da tarifa de cadastro em contrato bancário celebrado após o início do relacionamento entre as partes, conforme Tema 620 e Súmula 566 do STJ. É legítima a tarifa de registro de contrato quando prevista e efetivamente prestado o serviço (Tema 958/STJ). É abusiva a tarifa de avaliação do bem diante da ausência de demonstração da efetiva prestação do serviço ou da onerosidade excessiva. A imposição de seguro de proteção financeira com seguradora indicada pelo banco configura venda casada (Tema 972/STJ), sendo devida a restituição simples dos valores pagos a partir da citação, diante do princípio da boa-fé e da vedação ao enriquecimento ilícito.”
> Dispositivos relevantes citados: Constituição Federal: art. 5º, XXXII; Código de Defesa do Consumidor: art. 39, I; art. 42, parágrafo único; Código Civil: arts. 490 e 1.361; Código de Processo Civil: arts. 1.010, II e III; 85, §11; Resolução CMN nº 3.518/2007: art. 5º, V; Súmula 566/STJ; e Temas Repetitivos do STJ: 620, 958 e 972.
> Jurisprudência relevante citada: STJ, REsp 1.251.331/RS (Tema 620), Rel. Min. Maria Isabel Gallotti, DJe 24.10.2013; STJ, REsp 1.578.553/SP (Tema 958), Rel. Min. Paulo de Tarso Sanseverino, DJe 6.12.2018; STJ, REsp 1.639.320/SP e 1.639.259/SP (Tema 972), Rel. Min. Paulo de Tarso Sanseverino; STJ, AgInt no REsp 2.100.638/MS, Rel. Min. Ricardo Villas Bôas Cueva, DJe 26.6.2025.

### TJPR · Apelação Cível 0024266-66.2025.8.16.0030
- regras: R08, R11, R12
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0024266-66.2025.8.16.0030
- orgao: 6ª Câmara Cível
- relator: Des. Cláudio Smirne Diniz
- julgamento: 2026-10-26
- publicacao: 2026-10-26
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000039298171/Ac%C3%B3rd%C3%A3o-0024266-66.2025.8.16.0030
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Põe na instituição o ônus de provar que a tarifa de cadastro foi cobrada no início do relacionamento (o dado está nos registros do próprio banco; a mera previsão contratual não basta) e exige prova concreta da efetiva prestação dos serviços para as tarifas de avaliação do bem e de registro do contrato; mantém a restituição em dobro.
- observacao: Reconvenção revisional em busca e apreensão; apelo do banco desprovido. Na tarifa de cadastro não havia prova de contrato anterior: o ponto decidido é o ônus da prova do pressuposto (início do relacionamento), que fica com a instituição — útil quando o consumidor não tem a prova do vínculo anterior e em contraponto ao AgInt no REsp 2.007.638/MS. Na avaliação e no registro, o banco não indicou documento que provasse os serviços. A íntegra do portal não repete o CNJ no corpo, mas descreve o mesmo caso (mesmas questões e mesma distribuição de sucumbência). Correções na ementa: separados os títulos e itens que a extração emendou, sem alterar o texto. Fonte: portal de jurisprudência do TJPR (comarca de Foz do Iguaçu).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO DE BUSCA E APREENSÃO EM ALIENAÇÃO FIDUCIÁRIA. SENTENÇA DE PROCEDÊNCIA DA AÇÃO PRINCIPAL E PARCIAL PROCEDÊNCIA DA RECONVENÇÃO. TARIFA DE CADASTRO. AUSÊNCIA DE DEMONSTRAÇÃO DO INÍCIO DO RELACIONAMENTO. TARIFAS DE AVALIAÇÃO DO BEM E DE REGISTRO DO CONTRATO. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DOS SERVIÇOS. SEGURO DE PROTEÇÃO FINANCEIRA. AUSÊNCIA DE DEMONSTRAÇÃO DA LIBERDADE DE ESCOLHA DA SEGURADORA. REPETIÇÃO DO INDÉBITO EM DOBRO. INEXISTÊNCIA DE ENGANO JUSTIFICÁVEL DEMONSTRADO. SUCUMBÊNCIA RECÍPROCA MANTIDA. RECURSO CONHECIDO E NÃO PROVIDO.
> I. Caso em exame
> 1. Apelação cível interposta pela instituição financeira contra sentença que julgou procedente a ação de busca e apreensão e parcialmente procedente a reconvenção, para excluir cobranças relativas à tarifa de cadastro, avaliação de garantia, registro do contrato, seguro e outros serviços, declarar a nulidade das cláusulas correspondentes, determinar a restituição em dobro e autorizar a compensação com o saldo devedor recomposto.
> II. Questões em discussão
> 2. As questões em discussão consistem em saber: (i) se é válida a tarifa de cadastro; (ii) se houve comprovação da efetiva prestação dos serviços de avaliação do bem e registro do contrato; (iii) se a contratação do seguro de proteção financeira assegurou efetiva liberdade de escolha da seguradora; (iv) se deve ser mantida a declaração de nulidade das cláusulas correspondentes; (v) se a restituição dos valores deve ocorrer em dobro; e (vi) se a distribuição dos ônus sucumbenciais deve ser modificada.
> III. Razões de decidir
> 3. A tarifa de cadastro somente é admitida no início do relacionamento entre o consumidor e a instituição financeira. Impugnada a cobrança e não demonstrado, no caso, o pressuposto que autoriza sua incidência, mantém-se a exclusão do encargo.
> 4. A validade abstrata das tarifas de avaliação do bem e de registro do contrato não dispensa a comprovação da efetiva prestação dos serviços. Ausente indicação concreta de prova apta a infirmar a conclusão da sentença, preserva-se o reconhecimento da abusividade.
> 5. A contratação de seguro de proteção financeira não é, por si, vedada, mas o consumidor não pode ser compelido a contratar com a instituição financeira ou com seguradora por ela indicada. A mera previsão de facultatividade não substitui a demonstração da efetiva liberdade de escolha da seguradora.
> 6. A sentença promoveu revisão pontual dos encargos reputados abusivos, sem invalidar integralmente o negócio jurídico, mantendo, inclusive, a procedência da ação de busca e apreensão.
> 7. A repetição em dobro do indébito independe da demonstração de má-fé, salvo engano justificável. Não demonstrada circunstância concreta apta a justificar as cobranças indevidas, mantém-se a dobra.
> 8. O acolhimento de parcela relevante dos pedidos reconvencionais afasta a alegação de sucumbência mínima da instituição financeira. Mantém-se a distribuição fixada na origem.
> IV. Dispositivo e tese
> 9. Recurso conhecido e não provido.
> Tese de julgamento: “1. A tarifa de cadastro somente pode ser cobrada no início do relacionamento entre consumidor e instituição financeira. 2. A cobrança das tarifas de avaliação do bem e de registro do contrato exige prova da efetiva prestação dos serviços correspondentes. 3. A validade do seguro de proteção financeira pressupõe demonstração de que o consumidor teve efetiva liberdade de contratar e de escolher a seguradora. 4. A repetição em dobro prevista no art. 42, parágrafo único, do CDC é cabível quando a cobrança indevida não decorre de engano justificável.”

## R09 — Cláusula de ressarcimento de "serviços de terceiros" sem especificação do serviço

Tese: É abusiva a cláusula que transfere ao consumidor o ressarcimento de "serviços de terceiros" sem especificar o serviço efetivamente prestado, por violar o direito à informação adequada e impor desvantagem exagerada (CDC, arts. 6º, III, e 51, IV).

### STJ · REsp 1.578.553/SP
- regras: R09, R10, R29, R11, R12
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.578.553/SP
- orgao: Segunda Seção
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2018-11-28
- publicacao: 2018-12-06
- precedente_qualificado: Tema 958/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106314337
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- julgamento: 2025-10-13
- publicacao: 2025-10-14
- precedente_qualificado: Tema 958/STJ (aplicação)
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000033903631/Ac%C3%B3rd%C3%A3o-0021827-52.2024.8.16.0019
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O TJPR declara abusiva a tarifa de "despesas com terceiros" lançada de forma genérica no contrato de financiamento de veículo e determina a restituição simples.
- observacao: Turma Recursal (Juizado Especial). Julgado por maioria (um voto vencido); o voto vencido não consta na ementa, e o ponto da tarifa de terceiros foi decidido a favor do consumidor. A ementa também trata de prescrição (aplica o prazo decenal do art. 205 do CC). Publicação pela data do Jusbrasil. Há acórdãos de Câmara Cível do TJPR nesta tese. Conferido no portal do TJPR em 29/10/2026: ementa e dados batem; ajustes: julgamento em 13/10/2025 (o Jusbrasil indicava 10/10/2025); link permanente do portal.

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

### TJPR · Apelação Cível 0001334-38.2021.8.16.0026
- regras: R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001334-38.2021.8.16.0026
- orgao: 4ª Câmara Cível
- relator: Des. Abraham Lincoln Merheb Calixto
- julgamento: 2024-11-26
- publicacao: 2024-11-29
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000030858351/Ac%C3%B3rd%C3%A3o-0001334-38.2021.8.16.0026
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 4ª Câmara Cível reforma a sentença de improcedência: a cobrança de serviços de terceiros sem especificação no contrato viola o direito à informação (CDC, art. 6º, III) e deve ser restituída, com os juros reflexos.
- observacao: Apelo do consumidor provido. Restituição simples, por ser o contrato anterior a 30/03/2021 (modulação do EAREsp 600.663/RS, afastada depois pelo Tema 929/STJ, REsp 1.963.770/CE: não citar pela forma simples). A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (financiamento com alienação fiduciária, serviços de terceiros, restituição simples com reflexos). Sem correções na ementa. Fonte: portal de jurisprudência do TJPR (comarca de Campo Largo).

ementa:
> DIREITO CIVIL. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO GARANTIDO POR ALIENAÇÃO FIDUCIÁRIA. SERVIÇOS DE TERCEIROS. ABUSIVIDADE. ESPECIFICAÇÃO AUSENTE. RESTITUIÇÃO SIMPLES DOS VALORES COM OS REFLEXOS INCIDENTES.
> APELO PROVIDO.
> 1. CASO EM EXAME
> Ação Revisional de Contrato ajuizada para declaração da ilegalidade da cobrança de serviços de terceiros e respectiva restituição de valores, em que foi prolatada sentença de improcedência dos pleitos iniciais.
> 2. QUESTÕES EM DISCUSSÃO
> Se abusiva a exigência de serviços de terceiros quando não especificados no contrato, bem como se há direito à devolução dos valores cobrados indevidamente.
> 3. RAZÕES DE DECIDIR
> 3.1. O STJ, ao julgar o REsp 1.578.553/SP, estabeleceu que é abusiva a cláusula que prevê o ressarcimento de serviços prestados por terceiros sem a devida especificação, nos termos do Tema 958.
> 3.2. No caso em análise, a cobrança de serviços de terceiros não foi devidamente demonstrada nem especificada, violando o direito à informação previsto no art. 6º., III, do CDC. A mera previsão genérica contratual não é suficiente para justificar a cobrança.
> 3.3. Embora o STJ permita a devolução em dobro de valores cobrados indevidamente (AgInt no AREsp n.º 2.034.993/DF), a modulação dos efeitos desse entendimento restringe a devolução em dobro apenas aos pagamentos realizados após 30/03/2021. No presente caso, sendo o contrato anterior a essa data, aplica-se a restituição simples.
> 4. DISPOSITIVO E TESE
> Recurso provido.
> Tese de julgamento: É abusiva a cláusula que prevê a cobrança de serviços de terceiros sem especificação, sendo devida a devolução simples dos valores cobrados indevidamente.
> Dispositivos relevantes citados: Código de Defesa do Consumidor, art. 6º., III; Código Civil, art. 406; Código Tributário Nacional, art. 161, § 1º.
> Jurisprudência relevante citada STJ, REsp 1.578.553/SP; TJPR, Apelação Cível n.º 0003963-44.2017.8.16.0181; TJPR, Apelação Cível n.º 0003244-44.2023.8.16.0119.

### TJPR · Apelação Cível 0063099-03.2012.8.16.0001
- regras: R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0063099-03.2012.8.16.0001
- orgao: 16ª Câmara Cível
- relator: Des. Helio Henrique Lopes Fernandes Lima
- julgamento: 2025-08-04
- publicacao: 2025-08-04
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000016064121/Ac%C3%B3rd%C3%A3o-0063099-03.2012.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 16ª Câmara Cível nega provimento ao apelo do banco e mantém a restituição da tarifa de serviços de terceiros lançada sem especificação do serviço, em financiamento de veículo.
- observacao: Apelo do banco desprovido; restituição simples, majorados os honorários recursais. Ementa curta; o raciocínio está no voto, que cita o REsp 1.578.553/SP e precedentes do TJPR. Correção na ementa: inserido espaço em "FIXAÇÃO.RECURSO". Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> APELAÇÃO CÍVEL. REVISIONAL DE CONTRATO. CONTRATO DE FINANCIAMENTO PARA AQUISIÇÃO DE VEÍCULO. SERVIÇO DE TERCEIROS. COBRANÇA ABUSIVA. AUSÊNCIA DE ESPECIFICAÇÃO DOS SERVIÇOS PRESTADOS. REPETIÇÃO DE INDÉBITO. POSSIBILIDADE. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS. FIXAÇÃO. RECURSO DESPROVIDO. 1. Em ocasião recente, o Superior Tribunal de Justiça decidiu, em sede de recurso repetitivo, que é abusiva a cláusula que prevê a cobrança de ressarcimento de serviços prestados por terceiros, sem a especificação do serviço efetivamente prestado. 2. Possível, em demanda revisional, ver reconhecido o dever de restituição, sendo esta uma das causas de pedir, na hipótese. 3. Com o desprovimento do recurso de apelação do requerido, eleva-se o valor dos honorários advocatícios fixados em sentença, na esteira do § 11, do art.85, do CPC.

### TJPR · Apelação Cível 0031566-26.2012.8.16.0001
- regras: R09
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0031566-26.2012.8.16.0001
- orgao: 18ª Câmara Cível
- relator: Des. Alberto Junior Veloso
- julgamento: 2026-06-01
- publicacao: 2026-06-02
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037184811/Ac%C3%B3rd%C3%A3o-0031566-26.2012.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 18ª Câmara Cível confirma a abusividade do "ressarcimento de serviços de terceiros" lançado sem especificação em arrendamento mercantil e esclarece que a data de 25/02/2011 só vale para a comissão do correspondente bancário, não para esta tese.
- observacao: Apelo do banco, interposto contra a restituição simples de R$ 2.146,56, provido apenas em parte quanto à sucumbência (a autora passa a arcar com os ônus por ter decaído da quase totalidade dos pedidos); a abusividade foi mantida. A distinção entre as teses 2.1 e 2.2 do Tema 958/STJ é útil contra o argumento de que o marco de 25/02/2011 limitaria a tese de serviços de terceiros. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (mesmo valor e mesmo desfecho). Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E CONSUMIDOR. APELAÇÃO CÍVEL. ARRENDAMENTO MERCANTIL. REVISÃO CONTRATUAL. RESSARCIMENTO DE SERVIÇOS DE TERCEIROS. COBRANÇA GENÉRICA SEM ESPECIFICAÇÃO DO SERVIÇO PRESTADO. ABUSIVIDADE. TEMA 958/STJ. SUCUMBÊNCIA RECÍPROCA. SUCUMBÊNCIA MÍNIMA DO BANCO. PROVIMENTO PARCIAL. I. Caso em exame Apelação cível interposta por instituição financeira contra sentença que julgou parcialmente procedentes os pedidos em ação revisional de contrato de arrendamento mercantil, reconhecendo a abusividade da cobrança de R$ 2.146,56 a título de "Ressarcimento de Serviços de Terceiros", com restituição simples do valor, e fixando sucumbência recíproca na proporção de 80% para a autora e 20% para o banco. II. Questão em discussão Há duas questões em discussão: (i) saber se a cobrança de "Ressarcimento de Serviços de Terceiros" em contrato de arrendamento mercantil é abusiva quando ausente a especificação do serviço efetivamente prestado, à luz do Tema 958/STJ e (ii) saber se a distribuição dos ônus sucumbenciais na proporção de 80/20 deve ser substituída pela atribuição integral à autora, sob o argumento de sucumbência mínima do banco (art. 86, parágrafo único, do CPC). III. Razões de decidirA tese 2.1 do Tema 958/STJ estabelece a abusividade da cláusula que prevê a cobrança de ressarcimento de serviços prestados por terceiros sem a especificação do serviço a ser efetivamente prestado, independentemente da data de celebração do contrato. A mera indicação nominal de terceiro supostamente envolvido na operação não supre a exigência de especificação, que demanda discriminação clara e objetiva da natureza do serviço e de sua vinculação funcional à operação.O marco temporal de 25/02/2011 (Resolução CMN 3.954/2011), invocado pelo apelante, aplica-se exclusivamente à vedação da cobrança de comissão do correspondente bancário (tese 2.2 do Tema 958/STJ), não se confundindo com a hipótese de cobrança genérica e inespecífica de serviços de terceiros (tese 2.1).A autora decaiu da grande maioria dos pedidos formulados na inicial — extinção sem mérito do pedido de rescisão contratual, rejeição da revisão da tarifa de cadastro e do afastamento da comissão de permanência —, obtendo êxito apenas quanto ao ressarcimento de serviços de terceiros, o que configura sucumbência mínima do banco, atraindo a aplicação do art. 86, parágrafo único, do CPC. IV. Dispositivo Recurso conhecido e parcialmente provido, mantida a sentença quanto ao reconhecimento da abusividade da cobrança genérica de "Ressarcimento de Serviços de Terceiros" e reformada quanto à distribuição dos ônus sucumbenciais, atribuindo-se à autora a responsabilidade integral pelas custas processuais e honorários advocatícios, nos termos do art. 86, parágrafo único, do CPC.

## R10 — Comissão do correspondente bancário em contratos a partir de 25/02/2011

Tese: É abusiva a cláusula que transfere ao consumidor o ressarcimento da comissão do correspondente bancário em contratos celebrados a partir de 25/02/2011, data de vigência da Res. CMN 3.954/2011, devendo o valor ser restituído.

O REsp 1.578.553/SP (tese 2.2), listado sob R09 com `regras: R09, R10, R29`, também serve a esta tese.

### STJ · AgInt no REsp 2.179.148/SP
- regras: R10
- posicao: ADV
- tribunal: STJ
- classe_numero: AgInt no REsp 2.179.148/SP
- orgao: Terceira Turma
- relator: Min. Humberto Martins
- julgamento: 2026-10-27
- publicacao: 2026-10-29
- precedente_qualificado: aplica o Tema 958/STJ (tese 2.2)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7745058766
- verificado_em: 2026-11-02
- status: VERIFICADO
- uso_na_peca: Ressalva de peça: a Terceira Turma reafirma que a tese 2.2 do Tema 958 tem marco em 25/02/2011 (Res. CMN 3.954/2011) e que a cláusula de ressarcimento da comissão do correspondente é válida em contrato anterior, salvo onerosidade excessiva; a petição deve demonstrar a data do contrato e, havendo cobrança genérica de "serviços de terceiros", invocar também a tese 2.1.
- observacao: Arrendamento mercantil de veículo, contrato anterior à Res. CMN 3.954/2011, cláusula mantida como válida. Agravo improvido; o STJ distinguiu a cobrança genérica de serviços de terceiros (tese 2.1) da comissão do correspondente (tese 2.2, marco de 25/02/2011) e aplicou as Súmulas 5 e 7 ao ponto da especificação do serviço. Publicação pela data do Jusbrasil (o texto não traz a data do DJe).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. AGRAVO INTERNO EM RECURSO ESPECIAL. ARRENDAMENTO MERCANTIL FINANCEIRO. VRG. PRESCRIÇÃO E COMPENSAÇÃO. CORREÇÃO MONETÁRIA. SERVIÇOS DE TERCEIROS. IMPUGNAÇÃO ESPECÍFICA. ÓBICES SUMULARES.
> I. Caso em exame 1. Agravo interno interposto contra decisão monocrática que conheceu em parte de recurso especial e, nessa extensão, negou-lhe provimento, majorando honorários advocatícios, em ação de indenização relativa a arrendamento mercantil de veículo.
> 2. Pedidos e fundamentos. Pretensões de: (i) reconhecimento de prescrição das contraprestações vencidas e não pagas; (ii) alteração do termo inicial da correção monetária do Valor Residual Garantido (VRG) contratado; (iii) devolução de cobranças de serviços de terceiros; e (iv) reconhecimento de violação do art. 1.022 do CPC e afastamento dos óbices das Súmulas 5, 7 e 83/STJ.
> 3. As decisões anteriores. Acórdão do Tribunal de origem manteve a sentença, afastou a prescrição (prazo "sequer teve início"), reconheceu a compensação das parcelas inadimplidas com o produto da venda do bem, fixou a correção monetária a partir da alienação do bem e reputou legítima a cobrança de serviços de terceiros em contrato anterior à Resolução CMN nº 3.954/2011. Embargos de declaração rejeitados.
> II. Questão em discussão 4. A questão em discussão consiste em saber se houve negativa de prestação jurisdicional (art. 1.022 do CPC) diante de alegada omissão não enfrentada pelo Tribunal de origem, à luz do dever de impugnação específica (art. 1.021, § 1º, do CPC) e do art. 489, § 1º, IV, do CPC.
> 5. A questão em discussão consiste em definir os efeitos da prescrição quinquenal (art. 206, § 5º, I, do CC) sobre a compensação das parcelas inadimplidas com o VRG, notadamente o momento da coexistência e exigibilidade recíproca das dívidas no arrendamento mercantil e a possibilidade de reconhecimento da compensação legal após a rescisão e venda do bem.
> 6. A questão em discussão consiste em verificar o termo inicial da correção monetária do VRG para apuração do saldo no regime do Tema 500/STJ e se a insurgência recursal se dissocia do fundamento do acórdão recorrido.
> 7. Há duas questões em discussão: (i) saber se é abusiva a tarifa de serviços de terceiros à luz do Tema 958/STJ e da Resolução CMN nº 3.954/2011; e (ii) saber se a revisão pretendida demanda interpretação de cláusula contratual e reexame de prova (Súmulas 5 e 7/STJ).
> 8. A questão em discussão consiste em saber se há demonstração adequada de divergência jurisprudencial (alínea c do art. 105, III, da CF/1988), com cotejo analítico e identificação dos paradigmas (art. 1.029, § 1º, do CPC e art. 255, § 1º, do RISTJ), e se incide a Súmula 83/STJ.
> 9. A questão em discussão consiste em definir a incidência da multa do art. 1.021, § 4º, do CPC e a possibilidade de nova majoração de honorários (art. 85, § 11, do CPC).
> III. Razões de decidir 10. Não se verifica negativa de prestação jurisdicional. A parte não individualiza omissão relevante, não demonstra sua suscitação oportuna, tampouco sua aptidão para alterar o resultado, atraindo a aplicação do art. 489, § 1º, IV, do CPC e, por deficiência de fundamentação, da Súmula 284/STF.
> 11. O prazo prescricional para cobrança das parcelas inadimplidas é quinquenal (art. 206, § 5º, I, do CC), mas a controvérsia reside nos efeitos da prescrição sobre compensação já operada. A compensação legal (arts. 368 e 369 do CC) extingue obrigações até onde se compensarem, com efeitos que retroagem ao momento da coexistência de dívidas líquidas e exigíveis; a prescrição posterior não impede o reconhecimento desses efeitos (arts. 189 e 882 do CC). O art. 190 do CC não obsta a declaração de compensação já aperfeiçoada. Orientação alinhada ao Tema 500/STJ e ao REsp 1.983.238/SP.
> 12. No arrendamento mercantil, o momento de coexistência das dívidas ocorre na rescisão do contrato e na venda do bem, quando se apura o saldo e se consolida o direito ao VRG e à cobrança das parcelas inadimplidas. A tese recursal pressupõe premissas fáticas diversas das fixadas, demandando reexame de datas, valores, planilhas e critérios de cálculo, o que é vedado pela Súmula 7/STJ. Incide, ademais, a Súmula 83/STJ por conformidade do acórdão recorrido com a jurisprudência desta Corte.
> 13. Quanto ao termo inicial da correção monetária, o acórdão fixou a data da alienação do bem, em consonância com a finalidade de recomposição do valor da moeda e com o momento de apuração do saldo no Tema 500/STJ. A insurgência recursal dissocia-se do fundamento adotado, atraindo a Súmula 284/STF; eventual revisão exigiria análise de planilhas e cálculos, obstada pela Súmula 7/STJ.
> 14. A tarifa de serviços de terceiros é abusiva quando desprovida de especificação do serviço efetivamente prestado (Tema 958/STJ). Todavia, é válida a cláusula de ressarcimento da comissão de correspondente bancário em contratos anteriores à Resolução CMN nº 3.954/2011, ressalvada a onerosidade excessiva. O acórdão reconheceu a discriminação do serviço e sua legitimidade; a revisão demandaria interpretação de cláusula contratual e reexame de prova, atraindo as Súmulas 5 e 7/STJ.
> 15. A divergência jurisprudencial não foi demonstrada: faltam identificação do órgão prolator, natureza da decisão, data, repositório, cotejo analítico e similitude fática, em violação do art. 1.029, § 1º, do CPC e do art. 255, § 1º, do RISTJ. Quando o dissídio decorre de circunstâncias fáticas, não há divergência quanto à interpretação da lei federal.
> 16. A multa do art. 1.021, § 4º, do CPC não incide automaticamente, exigindo manifesta inadmissibilidade ou improcedência, circunstância não verificada. Incabível nova majoração de honorários, já promovida na decisão agravada (art. 85, § 11, do CPC).
> IV. Dispositivo Agravo interno improvido.

### TJPR · Apelação Cível 0031063-92.2024.8.16.0030
- regras: R10
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0031063-92.2024.8.16.0030
- orgao: 15ª Câmara Cível
- relator: Des. Luciano Campos de Albuquerque
- julgamento: 2026-03-07
- publicacao: 2026-03-07
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035925601/Ac%C3%B3rd%C3%A3o-0031063-92.2024.8.16.0030
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 15ª Câmara Cível declara abusiva a cláusula que repassa ao consumidor a comissão do correspondente bancário em empréstimo consignado posterior à Res. CMN 3.954/2011 e mantém a restituição dos valores.
- observacao: Revisional de empréstimo consignado; apelo do banco desprovido (prescrição decenal, abusividade mantida, honorários majorados). A premissa de contrato posterior à Res. CMN 3.954/2011 consta da ementa e do voto; a data exata do contrato não aparece na íntegra do portal. Mais recente dos acórdãos de Câmara Cível localizados que aplicam o corte de 25/02/2011 a favor do consumidor. A ementa do portal termina com um "Resumo em linguagem acessível", mantido por fazer parte do campo; não integra o voto. A íntegra não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (consignado, correspondente bancário, prescrição decenal, honorários). Correções na ementa: juntadas 26 quebras de linha que o portal inseriu no meio de frases. Fonte: portal de jurisprudência do TJPR (comarca de Foz do Iguaçu).

ementa:
> DIREITO CIVIL E DIREITO PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CONTRATO DE EMPRÉSTIMO CONSIGNADO. PRESCRIÇÃO DECENAL. COBRANÇA INDEVIDA DE COMISSÃO DE CORRESPONDENTE BANCÁRIO. RECURSO DESPROVIDO.
> I. CASO EM EXAME 1. Apelação cível interposta contra sentença que julgou procedente a ação revisional de contrato, declarando a abusividade da cláusula referente à cobrança de comissão de correspondente bancário e condenando o banco à restituição dos valores cobrados indevidamente, além de fixar honorários advocatícios. O banco alega a ocorrência de prescrição, a inexistência da cobrança contestada e requer a exclusão da condenação em honorários.
> II. QUESTÃO EM DISCUSSÃO 2. As questões em discussão consistem em verificar a ocorrência de prescrição e se é abusiva a cláusula que prevê a cobrança de comissão de correspondente bancário em contrato celebrado após a entrada em vigor da Resolução nº 3.954/2011 do CMN.
> III. RAZÕES DE DECIDIR 3. O prazo prescricional aplicável é o decenal, nos termos do artigo 205 do Código Civil.
> 4. “Nos termos da jurisprudência do STJ, deve-se considerar como termo inicial do prazo prescricional, nas ações de revisão de contrato bancário, a data da assinatura do contrato”. (AgInt no REsp n. 2.043.145/RS, relator Ministro Marco Buzzi, Quarta Turma, julgado em 8/5/2023, DJe de 11/5/2023.)
> 5. “De acordo com o entendimento firmado no REsp 1578.553/SP, é abusiva a cláusula que prevê a cobrança de valor relativo à comissão do correspondente bancário nos contratos firmados em momento posterior à entrada em vigor da Resolução nº 3954/2011, do CMN”. (TJPR - 15ª Câmara Cível - 0039915-66.2018.8.16.0014 - Londrina - Rel.: DESEMBARGADOR HAYTON LEE SWAIN FILHO - J. 19.06.2019)
> IV. DISPOSITIVO E TESE 6. Apelação cível conhecida e desprovida, mantendo a sentença que declarou a abusividade da cláusula referente à cobrança da comissão de correspondente bancário e condenou o réu à restituição dos valores indevidamente cobrados, com a majoração dos honorários advocatícios.
> Tese de julgamento:
> É abusiva a cláusula que prevê a cobrança de comissão de correspondente bancário em contratos celebrados após a entrada em vigor da Resolução nº 3.954/2011 do CMN, sendo ilegal a sua incidência em tais contratos.
> _________ Dispositivos relevantes citados:
> CC/2002, arts. 205 e 206, §3º, V; CPC/2015, art. 487, I; Resolução nº 3.954/2011, do CMN.
> Jurisprudência relevante citada:
> STJ, AgInt no REsp n. 2.043.145/RS, Rel. Min. Marco Buzzi, Quarta Turma, j. 08.05.2023; STJ, REsp n. 1.996.052/RS, Rel. Min. Nancy Andrighi, Terceira Turma, j. 17.05.2022; STJ, REsp 1.578.553/SP, Rel. Min. Luis Felipe Salomão, j. 19.06.2019; Súmula nº 211/STJ; Súmula nº 83/STJ.
> Resumo em linguagem acessível:
> O Tribunal decidiu que o Banco BS2 S/A não pode cobrar a comissão de correspondente bancário da cliente, pois essa cobrança é considerada abusiva, já que o contrato foi assinado após uma regra que proíbe essa prática. O banco tentou alegar que a ação estava fora do prazo, mas o Tribunal entendeu que o prazo para pedir a devolução dos valores é de dez anos, e não cinco, portanto, a ação estava certa. Assim, o pedido do banco foi negado, e ele terá que pagar os custos do processo e os honorários do advogado da cliente, que foram aumentados em 1% devido ao trabalho extra.

### TJPR · Apelação Cível 0039915-66.2018.8.16.0014
- regras: R10
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0039915-66.2018.8.16.0014
- orgao: 15ª Câmara Cível
- relator: Des. Hayton Lee Swain Filho
- julgamento: 2019-06-19
- publicacao: 2019-06-19
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000009514051/Ac%C3%B3rd%C3%A3o-0039915-66.2018.8.16.0014
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: A 15ª Câmara Cível declara abusiva a cobrança da comissão do correspondente bancário prevista em empréstimo consignado firmado depois da Res. CMN 3.954/2011 e mantém a restituição do valor.
- observacao: Revisional de empréstimo consignado; apelo do banco conhecido em parte e desprovido. Pela íntegra, o contrato é de junho de 2016 e traz a "Comissão" no campo "Correspondente"; o banco alegou que pagou a comissão com o lucro dos juros, e a Câmara entendeu que o custo foi repassado ao mutuário. A sentença mandou devolver de forma simples, e esse ponto não subiu. É o precedente que o acórdão de 2026 da mesma Câmara, já listado nesta tese, cita como fundamento. O título da ementa grafa "RESP. 1578.533/SP" e o corpo, "REsp 1578.553/SP" (o paradigma do Tema 958); mantido como no portal. Acórdão de 2019, anterior aos demais desta tese.

ementa:
> DIREITO CIVIL. REVISÃO CONTRATUAL. EMPRÉSTIMO CONSIGNADO. COBRANÇA DE COMISSÃO DE CORRESPONDENTE BANCÁRIO. IMPOSSIBILIDADE DE INCIDÊNCIA. CONTRATO FIRMADO APÓS A PUBLICAÇÃO DA RESOLUÇÃO 3954/2011, DO CMN. TESE FIXADA NO JULGAMENTO DO RESP. 1578.533/SP. SENTENÇA MANTIDA, MAS POR OUTRO FUNDAMENTO. De acordo com o entendimento firmado no REsp 1578.553/SP, é abusiva a cláusula que prevê a cobrança de valor relativo à comissão do correspondente bancário nos contratos firmados em momento posterior à entrada em vigor da Resolução nº 3954/2011, do CMN. APELAÇÃO CONHECIDA, EM PARTE, E NÃO PROVIDA.

### TJPR · Apelação Cível 0010469-76.2020.8.16.0069
- regras: R09, R10
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0010469-76.2020.8.16.0069
- orgao: 2ª Câmara Cível
- relator: Des. Rogério Luis Nielsen Kanayama
- julgamento: 2022-10-26
- publicacao: 2022-10-27
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000021331691/Ac%C3%B3rd%C3%A3o-0010469-76.2020.8.16.0069
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: A 2ª Câmara Cível afirma que, nos contratos celebrados após 25/02/2011, a comissão do correspondente bancário é indevida por vedação expressa e que a mera identificação do lojista intermediário não especifica os "serviços de terceiros", mantendo a restituição.
- observacao: Revisional de crédito direto ao consumidor com alienação fiduciária, com vários autores e contratos; apelo do banco parcialmente conhecido e parcialmente provido em outros pontos. Pela íntegra, o banco sustentou que os "serviços de terceiros" eram a comissão do correspondente; a Câmara rejeitou com dois fundamentos: falta de especificação (tese 2.1 do Tema 958) e, para um dos contratos, celebrado em 01/03/2011, a vedação da Res. CMN 3.954/2011 (tese 2.2). A restituição dos serviços de terceiros foi mantida. Na peça, apoiar o corte temporal no item "g" da ementa. Acórdão de 2022.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CRÉDITO DIRETO AO CONSUMIDOR COM ALIENAÇÃO FIDUCIÁRIA EM GARANTIA. VÁRIOS AUTORES. SENTENÇA DE PARCIAL PROCEDÊNCIA. APELAÇÃO DA INSTITUIÇÃO FINANCEIRA. NÃO CONHECIMENTO DA ALEGAÇÃO DE VALIDADE DA COMISSÃO DE PERMANÊNCIA DEVIDO AO PRINCÍPIO DA IRRETROATIVIDADE DAS NORMAS JURÍDICAS. INOVAÇÃO RECURSAL. DECLARAÇÃO, DE OFÍCIO, DE NULIDADE DA SENTENÇA QUANTO À ABUSIVIDADE DA COBRANÇA DE TARIFA DE REGISTRO. SENTENÇA EXTRA PETITA NO PONTO. AUSÊNCIA DE PEDIDO. VIOLAÇÃO À SÚMULA Nº 381 DO SUPERIOR TRIBUNAL DE JUSTIÇA. AINDA, RECONHECIMENTO, DE OFÍCIO, DE NULIDADE DA SENTENÇA A RESPEITO DA ABUSIVIDADE DA COBRANÇA DE TARIFA DE CADASTRO E COMISSÃO DE PERMANÊNCIA POR AUSÊNCIA DE FUNDAMENTAÇÃO. APLICAÇÃO DO ART. 1.013, § 3º, IV, DO CÓDIGO DE PROCESSO CIVIL. TARIFA DE CADASTRO. POSSIBILIDADE DE EXIGÊNCIA UMA ÚNICA VEZ. SÚMULA Nº 566 DO SUPERIOR TRIBUNAL DE JUSTIÇA. EXISTÊNCIA DE PROVA QUANTO AO RELACIONAMENTO ANTERIOR ENTRE CLIENTE E O BANCO. COMISSÃO DE PERMANÊNCIA. IMPOSSIBILIDADE DE CUMULAÇÃO COM JUROS MORATÓRIOS, REMUNERATÓRIOS E MULTA. SÚMULA Nº 472 DA CORTE SUPERIOR. SERVIÇOS DE TERCEIROS. TEMA Nº 958/STJ. NECESSIDADE DE ESPECIFICAÇÃO DO SERVIÇO. MERA IDENTIFICAÇÃO DO LOJISTA INTERMEDIÁRIO QUE NÃO É SUFICIENTE PARA ESSE FIM. COMISSÃO DO CORRESPONDENTE BANCÁRIO INDEVIDA A PARTIR DE 25.2.2011. TARIFA DE AVALIAÇÃO. TEMA Nº 958/STJ. VALIDADE EM RELAÇÃO AOS CONTRATOS EM QUE FICOU DEMONSTRADA A EFETIVA PRESTAÇÃO DO SERVIÇO. AFASTAMENTO QUANTO AOS DEMAIS. SEGURO PRESTAMISTA E TÍTULO DE CAPITALIZAÇÃO. TEMA Nº 972/STJ. PROIBIÇÃO DE CONTRATAÇÃO COMPULSÓRIA. REQUERENTES QUE OPTARAM LIVREMENTE PELA CONTRATAÇÃO DOS SEGUROS. INEXISTÊNCIA DE ARBITRARIEDADE OU ABUSIVIDADE NOS NEGÓCIOS FIRMADOS. RECURSO PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, PARCIALMENTE PROVIDO. a. Não se conhece de alegação não submetida ao Juízo de origem por caracterizar inovação recursal. b. A sentença é extra petita quando concede pedido não formulado pelas partes. Ainda, nos termos da Súmula nº 381 do Superior Tribunal de Justiça, “nos contratos bancários, é vedado ao julgador conhecer, de ofício, da abusividade das cláusulas”.c. É nula por falta de fundamentação a sentença que defere pedidos sem explicitar as razões para tanto. d. O art. 1.013, § 3º, IV, do Código de Processo Civil autoriza a análise do mérito pelo tribunal quando decretar a nulidade da sentença por falta de fundamentação. e. De acordo com a Súmula nº 566 do Superior Tribunal de Justiça, “nos contratos bancários posteriores ao início da vigência da Resolução-CMN n. 3.518/2007, em 30/4/2008, pode ser cobrada a tarifa de cadastro no início do relacionamento entre o consumidor e a instituição financeira”, de modo que, quando demonstrada a existência de relacionamento anterior entre cliente e banco, a cobrança da referida tarifa deve ser afastada.
> f. Conforme prevê a Súmula nº 472 do Superior Tribunal de Justiça, “a cobrança de comissão de permanência – cujo valor não pode ultrapassar a soma dos encargos remuneratórios e moratórios previstos no contrato – exclui a exigibilidade dos juros remuneratórios, moratórios e da multa contratual”. g. A mera identificação do lojista intermediário não é suficiente para afirmar que os “serviços de terceiros” estão especificados. Ademais, nos contratos celebrados após 25.2.2011, a comissão de correspondente bancário é indevida por expressa vedação legal. h. A cobrança de tarifa de avaliação é válida somente quando demonstrada a efetiva prestação do serviço. i. “Nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada” (STJ. REsp 1639259/SP, Rel. Ministro PAULO DE TARSO SANSEVERINO, SEGUNDA SEÇÃO, julgado em 12/12/2018, DJe 17/12/2018). No entanto, comprovado que os autores optaram livremente pela contratação do seguro e do título de capitalização, não há falar em abusividade ou arbitrariedade nos negócios firmados.

## R11 — Tarifa de avaliação — sem comprovação do serviço

Tese: A tarifa de avaliação do bem dado em garantia só é exigível se a instituição financeira comprovar que a avaliação foi efetivamente realizada (Tema 958/STJ, tese 2.3, ressalva 2.3.1); sem laudo, ou com documento unilateral e genérico que não demonstra avaliação técnica do bem, a cobrança é abusiva e o valor pago — com os juros que incidiram sobre ele — deve ser restituído.

Nota: o leading case é o REsp 1.578.553/SP (Segunda Seção, Tema 958), tese 2.3 com a ressalva 2.3.1 (cobrança por serviço não efetivamente prestado), listado sob a R09. Mais um favorável do TJPR (6ª Câmara Cível) está sob a R08.

### STJ · AREsp 3.162.498/RJ
- regras: R11, R12
- posicao: ADV
- tribunal: STJ
- classe_numero: AREsp 3.162.498/RJ
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2026-08-31
- publicacao: 2026-09-10
- precedente_qualificado: não (aplica o Tema 958/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7307680933
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva: a Terceira Turma reafirma que são válidas a tarifa de avaliação do bem e o ressarcimento do registro do contrato (Tema 958), ressalvados o controle de onerosidade e a vedação de cobrança por serviço não prestado, e deixa a verificação da prestação do serviço às instâncias ordinárias (Súmulas 5 e 7); a prova (ou a falta de prova pelo banco) tem de ser enfrentada no primeiro e no segundo grau, porque o STJ não a revê.
- observacao: Recurso do consumidor não conhecido; financiamento de veículo com tarifa de avaliação de R$ 550,00. O TJRJ manteve as tarifas "com base no contrato e em elementos fáticos". Sessão virtual de 25 a 31/08/2026. Publicação pela data do Jusbrasil (10/09/2026, data da lista de resultados; o inteiro teor não traz o DJEN). Ementa da seção Ementa da página, igual à do inteiro teor salvo uma quebra de linha do PDF no item 4 e o espaço em "7/ STJ".

ementa:
> PROCESSUAL CIVIL E DIREITO DO CONSUMIDOR. AGRAVO EM RECURSO ESPECIAL. AUSÊNCIA DE PREQUESTIONAMENTO QUANTO AOS ARTS. 371 E 479 DO CPC. SÚMULA 211/STJ. TARIFA DE AVALIAÇÃO DO BEM E DESPESA DE REGISTRO DO CONTRATO. TEMA 958/STJ. CONTROLE DE ABUSIVIDADE NO CASO CONCRETO. IMPOSSIBILIDADE DE REEXAME DE PROVAS E DE CLÁUSULAS CONTRATUAIS. SÚMULAS 5 E 7/STJ. AGRAVO CONHECIDO. RECURSO ESPECIAL NÃO CONHECIDO.
> 1. Agravo em recurso especial contra acórdão que manteve a validade da tarifa de avaliação do bem e da despesa de registro do contrato em financiamento de veículo, além da taxa de juros contratada.
> 2. A questão recursal consiste em examinar se (i) houve violação dos arts. 371 e 479 do CPC por ausência de apreciação da prova pericial; e (ii) houve abusividade na cobrança de tarifa de avaliação do bem e do registro do contrato, com repetição do indébito em dobro, à luz dos arts. 42, parágrafo único, e 51, IV e XII, do CDC.
> 3. A alegada violação dos arts. 371 e 479 do CPC não pode ser apreciada, por ausência de prequestionamento no acórdão do Tribunal estadual, aplicando-se a Súmula 211/STJ.
> 4. É válida a cobrança de tarifa de avaliação do bem dado em garantia e o ressarcimento de despesas com registro do contrato, conforme o Tema 958/STJ, ressalvados o controle de onerosidade e a vedação de cobrança por serviço não prestado. No caso, o acórdão afastou a abusividade com base no contrato e em elementos fáticos, sendo inviável, em recurso especial, o revolvimento de provas e a interpretação de cláusulas contratuais, nos termos das Súmulas 5 e 7/STJ.
> 5. Agravo conhecido. Recurso especial não conhecido.

### TJPR · Apelação Cível 0000286-02.2023.8.16.0082
- regras: R11, R12
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0000286-02.2023.8.16.0082
- orgao: 7ª Câmara Cível
- relator: Juiz Subst. 2º Grau Eduardo Lino Bueno Fagundes Junior
- julgamento: 2026-04-22
- publicacao: 2026-04-22
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000036043251/Ac%C3%B3rd%C3%A3o-0000286-02.2023.8.16.0082
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Declara abusivas, em financiamento de veículo, a tarifa de avaliação (só um "termo de avaliação" unilateral com conferência genérica, sem avaliação técnica do bem) e a tarifa de registro (nenhum documento do gravame nem do custo desembolsado), com restituição em dobro dos valores e dos juros remuneratórios que incidiram sobre essas tarifas.
- observacao: Recurso do consumidor provido nesses pontos. O voto registra que o termo de avaliação não verificou motor, câmbio e acessórios e que o banco não trouxe outro documento; no registro, que "a mera previsão em abstrato desse custo não significa dizer que o serviço foi, de fato, prestado". O acórdão também reconheceu onerosidade excessiva da tarifa de cadastro (valor muito acima da média), que não é a hipótese da R08. O seguro foi validado (instrumento apartado). Dobro fundado no EREsp 1.413.542/RS, sem exame da modulação (hoje afastada pelo Tema 929/STJ). Correções na ementa: separados os títulos e itens que a extração emendou e juntadas as quebras de linha do portal no bloco de dispositivos citados, sem alterar o texto. Fonte: portal de jurisprudência do TJPR (comarca de Formosa do Oeste).

ementa:
> APELAÇÕES CÍVEIS. DIREITO CIVIL E DO CONSUMIDOR. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO DE VEÍCULO COM ALIENAÇÃO FIDUCIÁRIA. CONTRATO DE ADESÃO. CONTROLE DE ABUSIVIDADE DE TARIFAS BANCÁRIAS. TARIFA DE AVALIAÇÃO DO BEM. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO. ILEGALIDADE. TARIFA DE REGISTRO DE CONTRATO. AUSÊNCIA DE PROVA DO REGISTRO E DOS CUSTOS DO SERVIÇO. COBRANÇA ABUSIVA. TARIFA DE CADASTRO. POSSIBILIDADE DE COBRANÇA APENAS NO INÍCIO DO RELACIONAMENTO. ONEROSIDADE EXCESSIVA DO VALOR COBRADO. RESTITUIÇÃO DO EXCEDENTE. SEGURO DE PROTEÇÃO FINANCEIRA. CONTRATAÇÃO EM DOCUMENTO APARTADO. AUSÊNCIA DE VENDA CASADA. VALIDADE. DEVOLUÇÃO DE ENCARGOS REFLEXOS. JUROS INCIDENTES SOBRE TARIFAS ILEGAIS. REPETIÇÃO DO INDÉBITO EM DOBRO. RECURSOS CONHECIDOS E PROVIDOS.
> I. CASO EM EXAME
> 1.1 Ação revisional de contrato de financiamento de veículo, ajuizada pelo consumidor em face de instituição financeira, com alegação de cobrança de tarifas e encargos abusivos inseridos no contrato.
> 1.2 Sentença proferida pelo Juízo da Vara Cível julgou parcialmente procedentes os pedidos para reconhecer a abusividade da cobrança de seguro prestamista por ausência de comprovação da contratação voluntária, determinando a restituição em dobro dos valores pagos, bem como dos juros incidentes, e rejeitando o pedido de indenização por danos morais.
> 1.3 A parte autora interpôs apelação, sustentando a abusividade das tarifas de registro do contrato, avaliação do bem e cadastro, com pedido de exclusão dos valores do montante financiado, recálculo das parcelas e restituição em dobro dos valores pagos indevidamente.
> 1.4 A instituição financeira também interpôs apelação, defendendo a validade da contratação do seguro prestamista mediante assinatura de proposta em documento apartado e requerendo, subsidiariamente, que eventual restituição ocorra de forma simples.
> II. QUESTÕES EM DISCUSSÃO
> 2.1 Há quatro questões em discussão: (i) analisar se é válida a cobrança da tarifa de avaliação do bem diante da ausência de prova da efetiva prestação do serviço; (ii) verificar se é legítima a cobrança da tarifa de registro do contrato sem comprovação do registro e dos custos correspondentes; (iii) analisar se a tarifa de cadastro cobrada no contrato apresenta onerosidade excessiva; e (iv) verificar se é válida a cobrança do seguro de proteção financeira diante da alegação de venda casada.
> III. RAZÕES DE DECIDIR
> 3.1 A revisão de cláusulas contratuais em contratos bancários submetidos ao Código de Defesa do Consumidor é admitida quando constatada abusividade ou violação aos princípios da boa-fé objetiva, função social dos contratos e equilíbrio contratual, mitigando-se o princípio do pacta sunt servanda.
> 3.2 A cobrança da tarifa de avaliação do bem somente é válida quando demonstrada a efetiva prestação do serviço, conforme tese fixada pelo Superior Tribunal de Justiça no Tema 958. Ausente prova de avaliação técnica pormenorizada do veículo, sendo apresentado apenas documento unilateral contendo conferência genérica de dados, caracteriza-se cobrança indevida.
> 3.3 A tarifa de registro do contrato pode ser repassada ao consumidor como ressarcimento de serviço prestado por terceiro, desde que comprovado o efetivo registro e o valor desembolsado pela instituição financeira. Inexistindo nos autos comprovação da realização do registro ou do custo correspondente, impõe-se o reconhecimento da abusividade da cobrança.
> 3.4 A tarifa de cadastro é admitida pela regulamentação do Conselho Monetário Nacional e pela jurisprudência do Superior Tribunal de Justiça, desde que cobrada uma única vez no início do relacionamento entre consumidor e instituição financeira. Todavia, quando o valor exigido supera de forma significativa a média de mercado, caracteriza-se vantagem manifestamente excessiva, ensejando a restituição do valor excedente.
> 3.5 O seguro de proteção financeira é válido quando contratado mediante manifestação livre e informada do consumidor, especialmente quando formalizado em documento apartado do contrato principal, circunstância que afasta a configuração de venda casada, nos termos da tese fixada pelo STJ no Tema 972.
> 3.6 Reconhecida a ilegalidade de determinadas tarifas contratuais, impõe-se também a restituição dos juros remuneratórios incidentes sobre tais encargos, por aplicação do princípio segundo o qual o acessório segue a sorte do principal, evitando enriquecimento sem causa da instituição financeira.
> 3.7 Nas relações de consumo, a repetição do indébito deve ocorrer em dobro quando inexistente engano justificável por parte do fornecedor, conforme entendimento firmado pelo STJ no julgamento dos Embargos de Divergência no REsp nº 1.413.542/RS.
> IV. DISPOSITIVO
> 4.1. Apelação do autor conhecida e provida para reconhecer a abusividade das tarifas de avaliação do bem e de registro do contrato, bem como a onerosidade excessiva da tarifa de cadastro, determinando a restituição dos valores indevidamente cobrados, com inclusão dos encargos reflexos.
> 4.2 Apelação da instituição financeira conhecida e provida para reconhecer a validade da contratação do seguro de proteção financeira, afastando a nulidade declarada na sentença.
> Dispositivos relevantes citados: CF, art. 5º, XXXII. CC, arts. 92, 427, 428, I, 884 e 1.361. CDC, arts. 6º, III; 30; 39, I e V; 42, parágrafo único; 47; 51, I e IV; 52, III; 54. CPC, arts. 373, II; 872. LINDB, art. 4º. CTN, art. 109. Resolução CMN nº 3.518/2007. Resolução CMN nº 3.919/2010. Resolução CONTRAN nº 320/2009.
> Jurisprudência relevante citada: STJ, AgInt no AREsp 1.638.853/RS. STJ, REsp 1.578.553/SP (Tema 958). STJ, REsp 1.578.526/SP. STJ, REsp 1.639.259/SP e REsp 1.639.320/SP (Tema 972). STJ, REsp 1.255.573/RS (Temas 618 a 621). STJ, EAREsp 1.413.542/RS. TJPR, Apelação Cível nº 0081859-72.2023.8.16.0014. TJPR, Apelação Cível nº 0015366-58.2023.8.16.0194. TJPR, Apelação Cível nº 0006095-17.2024.8.16.0056. TJPR, Apelação Cível nº 0015887-54.2020.8.16.0017. TJPR, Apelação Cível nº 0002007-50.2023.8.16.0094. TJPR, Apelação Cível nº 0067799-94.2023.8.16.0014. TJPR, Apelação Cível nº 0058218-21.2024.8.16.0014. TJPR, Mandado de Segurança nº 0045695-58.2020.8.16.0000. TJPR, Apelação Cível nº 0008984-86.2019.8.16.0130. TJPR, Agravo de Instrumento nº 0037481-15.2019.8.16.0000.

## R12 — Tarifa de registro — sem comprovação do registro

Tese: O ressarcimento da despesa de registro do contrato só é devido se a instituição financeira comprovar que o registro foi efetivamente feito (gravame no órgão de trânsito ou registro em cartório) e quanto desembolsou por ele (Tema 958/STJ, tese 2.3 e suas ressalvas); sem essa prova, a cobrança é abusiva e o valor pago, com os juros que incidiram sobre ele, deve ser restituído.

Nota: os julgados desta regra servem também à R08 ou à R11 e estão listados sob elas: dois favoráveis do TJPR (6ª e 7ª Câmaras Cíveis) e o adverso do STJ (AREsp 3.162.498/RJ). O leading case é o REsp 1.578.553/SP (Tema 958, tese 2.3 com a ressalva 2.3.1), listado sob a R09.

## R13 — Seguro prestamista — venda casada

Tese: A contratação de seguro prestamista (ou de proteção financeira) imposta pela instituição financeira, sem opção real de contratar ou de escolher outra seguradora, é venda casada (CDC, art. 39, I) e o valor cobrado deve ser restituído.

### STJ · REsp 1.639.259/SP
- regras: R13, CONTA-ENCARGOS
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.639.259/SP
- orgao: Segunda Seção
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2018-12-12
- publicacao: 2018-12-17
- precedente_qualificado: Tema 972/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106312540
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Limite da tese: a mera contratação do seguro prestamista não configura, automaticamente, venda casada; é preciso demonstrar que a adesão foi condicionante para a obtenção do financiamento (a inicial deve alegar e provar a compulsão).
- observacao: Recurso não conhecido (Súmulas 5 e 7) porque o tribunal de origem afirmou facultatividade, proposta em apartado e ausência de condicionamento. Linha reiterada em outros acórdãos de 2025-2026. O REsp 2.101.019/SP é decisão monocrática e não entrou.

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
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000034954581/Ac%C3%B3rd%C3%A3o-0002779-20.2025.8.16.0069
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Seguro prestamista pré-inserido no contrato de financiamento, sem comprovação documental de opção ou de liberdade de escolha da seguradora, é venda casada; a assinatura de documento apartado não prova a escolha quando o seguro já consta do instrumento principal.
- observacao: Julgado de Turma Recursal dos Juizados Especiais (não é Câmara Cível); o TJPR tem vários julgados favoráveis alinhados. A ementa traz o erro material "TEMA 972 STF" (o voto aplica o Tema 972/STJ); copiado como no original. Publicação pela data do Jusbrasil. Conferido no portal do TJPR em 29/10/2026: ementa e dados batem; ajustes: link permanente do portal.

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
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000037047501/Ac%C3%B3rd%C3%A3o-0000868-54.2025.8.16.0139
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Venda casada reconhecida mesmo com a opção "SIM" assinalada no contrato (seguro previamente indicado e incorporado ao valor financiado, seguradora do mesmo grupo, propostas firmadas no mesmo dia); restituição em dobro sem exigir má-fé (o acórdão limitou o dobro às cobranças posteriores a 30/03/2021, corte afastado depois pelo Tema 929/STJ: citar pela venda casada e pelo dobro, não pela data).
- observacao: Julgado de Turma Recursal dos Juizados Especiais. O marco de 30/03/2021 e a restituição em dobro estão no voto, não no texto da ementa. Publicação pela data do Jusbrasil. Conferido no portal do TJPR em 29/10/2026: ementa e dados batem; ajustes: link permanente do portal.

ementa:
> RECURSOS INOMINADOS. DIREITO BANCÁRIO E DO CONSUMIDOR. CONTRATO DE FINANCIAMENTO DE VEÍCULO. TARIFA DE AVALIAÇÃO DO BEM. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DO SERVIÇO. COBRANÇA INDEVIDA. TARIFA DE REGISTRO DE CONTRATO. SERVIÇO COMPROVADAMENTE PRESTADO. COBRANÇA LEGÍTIMA. SEGURO PRESTAMISTA E SEGURO DE ACIDENTES PESSOAIS. CONTRATAÇÃO SEM OPÇÃO REAL DO CONSUMIDOR. CONFIGURAÇÃO DE VENDA CASADA. RESTITUIÇÃO EM DOBRO DOS VALORES. JUROS MORATÓRIOS. LIMITAÇÃO A 1% AO MÊS. SÚMULA 379 DO STJ. SENTENÇA PARCIALMENTE REFORMADA. RECURSO DA AUTORA CONHECIDO E PARCIALMENTE PROVIDO. RECURSO DA RÉ CONHECIDO E DESPROVIDO.

### TJPR · Apelação Cível 0004837-86.2025.8.16.0136
- regras: R13
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0004837-86.2025.8.16.0136
- orgao: 20ª Câmara Cível
- relator: Des.ª Luciana Carneiro de Lara
- julgamento: 2026-08-28
- publicacao: 2026-08-28
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000039245881/Ac%C3%B3rd%C3%A3o-0004837-86.2025.8.16.0136
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 20ª Câmara Cível reconhece a venda casada do seguro prestamista em financiamento com alienação fiduciária, por falta de liberdade de escolha da seguradora, e manda restituir em dobro, sem exigir má-fé.
- observacao: Apelo do banco conhecido em parte e parcialmente provido: a venda casada foi mantida, mas a restituição ficou limitada às parcelas pagas após o ajuizamento da ação (em dobro). Atenção ao limite ao pedir o valor total. Correções na ementa: retirado o rótulo inicial "EMENTA:"; inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Pitanga).

ementa:
> DIREITO CIVIL E DIREITO DO CONSUMIDOR. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO. ALIENAÇÃO FIDUCIÁRIA. SEGURO PRESTAMISTA. VENDA CASADA. CONFIGURAÇÃO. AUSÊNCIA DE LIBERDADE NA ESCOLHA DA SEGURADORA. ABUSIVIDADE RECONHECIDA. RESTITUIÇÃO DOS VALORES. LIMITAÇÃO ÀS PARCELAS PAGAS APÓS O AJUIZAMENTO DA DEMANDA. REPETIÇÃO DO INDÉBITO EM DOBRO. CABIMENTO. DESNECESSIDADE DE COMPROVAÇÃO DE MÁ-FÉ. PEDIDO DE EFEITO SUSPENSIVO FORMULADO NO CORPO DA APELAÇÃO. NÃO CONHECIMENTO. PREQUESTIONAMENTO. DESNECESSIDADE DE MENÇÃO EXPRESSA A DISPOSITIVOS LEGAIS. MANUTENÇÃO DOS ÔNUS SUCUMBENCIAIS. RECURSO CONHECIDO EM PARTE E PARCIALMENTE PROVIDO. I. Caso em exame 1. Apelação cível interposta por BANCO PAN S.A. contra sentença que, na
> Ação Revisional de Contrato de financiamento garantido por alienação fiduciária, reconheceu a abusividade da cobrança de seguro prestamista, determinando a restituição em dobro dos valores pagos a esse título. A instituição financeira sustenta a regularidade da contratação do seguro, a inexistência de venda casada e a impossibilidade de repetição de indébito em dobro, requerendo a redistribuição dos ônus sucumbenciais. II. Questão em discussão 2. A questão em discussão consiste em saber se a contratação do seguro prestamista ocorreu de forma legal e facultativa, bem como se é cabível a restituição em dobro dos valores pagos a esse título. III. Razões de decidir 3. O pedido de concessão de efeito suspensivo ao recurso, formulado nas próprias razões recursais, não comporta conhecimento, uma vez que deve ser apresentado por requerimento apartado, nos termos do art. 1.012, §3º, do CPC. 4. Foi mantido o reconhecimento da abusividade da cobrança do seguro prestamista, em razão da venda casada, sendo devida a restituição dos valores pagos a esse título apenas em relação às parcelas vencidas e efetivamente adimplidas após o ajuizamento da demanda. 5. A restituição em dobro dos valores pagos indevidamente é cabível, conforme disposto no artigo 42, parágrafo único, do Código de Defesa do Consumidor. 6. O prequestionamento dispensa menção expressa aos dispositivos legais invocados, bastando que a matéria tenha sido efetivamente enfrentada no acórdão. 7. Em razão do parcial provimento da pretensão recursal, sem modificação substancial do êxito e sucumbência das partes na demanda, mantêm-se os ônus sucumbenciais fixados na origem, sendo incabível a majoração de honorários recursais. IV. Dispositivo e tese 8. Apelação cível conhecida em parte e parcialmente provida para limitar a restituição em dobro decorrente da venda casada do seguro prestamista aos valores efetivamente pagos a esse título após o ajuizamento da Ação, mantidos os demais termos da sentença. Tese de julgamento: Configura venda casada a imposição da contratação de seguro prestamista com seguradora vinculada à instituição financeira, sendo devida a restituição em dobro dos valores pagos após o ajuizamento da ação, no presente caso, ressalvando-se a proteção securitária até então disponível ao consumidor e autorizada eventual compensação de valores. _________ Dispositivos relevantes citados: CPC, art. 487, I, art. 1.012, § 3º, e art. 98, § 3º; CDC, arts. 6º, III, e 39; CC/2002, art. 406.Jurisprudência relevante citada: TJPR, Apelação Cível 0004560-90.2024.8.16.0173, Rel. Des. Antonio Franco Ferreira da Costa Neto, 20ª Câmara Cível, j. 21.03.2025; TJPR, Apelação Cível 0004037-58.2022.8.16.0170, Rel. Des. Rosaldo Elias Pacagnan, 20ª Câmara Cível, j. 11.03.2025; TJPR, Apelação Cível 0001430-26.2023.8.16.0174, Rel. Des. Fabio Marcondes Leite, 20ª Câmara Cível, j. 04.04.2024; TJPR, Apelação Cível 0002962-38.2021.8.16.0034, Rel. Des. Antonio Franco Ferreira da Costa Neto, 20ª Câmara Cível, j. 28.02.2025; TJPR, Apelação Cível 0007242-31.2023.8.16.0083, Rel. Des. Fabio Marcondes Leite, 20ª Câmara Cível, j. 29.11.2024; STJ, REsp 1.639.259/SP, Rel. Min. Paulo de Tarso Sanseverino, Segunda Seção, j. 12.12.2018; STJ, EAREsp 600.663/RS, Rel. Min. Maria Thereza de Assis Moura, Corte Especial, j. 21.10.2020; STJ, AgInt no AREsp 895.746/SP, Rel. Min. Mauro Campbell Marques, Segunda Turma, j. 09.08.2016; STJ, EREsp 1424404/SP, Rel. Min. Luis Felipe Salomão, Corte Especial, j. 20.10.2021; Súmula 7/STJ.Resumo em linguagem acessível: O Tribunal decidiu que o banco cobrou de forma abusiva o seguro prestamista, porque obrigou a cliente a contratar o seguro com uma empresa ligada ao próprio banco, sem deixar ela escolher outra seguradora. Por isso, essa cobrança configurou venda casada, o que não é permitido pela lei. O banco terá que devolver em dobro o valor que a cliente pagou pelo seguro depois que ela entrou com a ação na Justiça. A decisão manteve a divisão dos custos do processo, ficando a cliente responsável por 80% e o banco por 20%.RECURSO DE APELAÇÃO CÍVEL CONHECIDO EM PARTE E PARCIALMENTE PROVIDO NA PARTE CONHECIDA.

### TJPR · Apelação Cível 0003813-43.2025.8.16.0194
- regras: R13
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0003813-43.2025.8.16.0194
- orgao: 4ª Câmara Cível
- relator: Des. Abraham Lincoln Merheb Calixto
- julgamento: 2026-09-29
- publicacao: 2026-09-30
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037910331/Ac%C3%B3rd%C3%A3o-0003813-43.2025.8.16.0194
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 4ª Câmara Cível reforma a sentença para reconhecer a venda casada do seguro prestamista com seguradora pré-indicada (Tema 972/STJ) e determinar a restituição em dobro de todos os valores pagos.
- observacao: Apelo do consumidor parcialmente provido: tarifa de avaliação e juros remuneratórios foram mantidos, o dano moral foi afastado e a mora não foi descaracterizada. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (veículo antigo, tarifa de registro de R$ 350,00, seguro prestamista). Correção na ementa: inserido espaço em "REDISTRIBUÍDA.RECURSO". Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO DO CONSUMIDOR. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. FINANCIAMENTO GARANTIDO POR ALIENAÇÃO FIDUCIÁRIA. ÔNUS DA PROVA. DISTRIBUIÇÃO
> ESTÁTICA. JUROS REMUNERATÓRIOS. TAXA QUE NÃO SUPERA O DOBRO DA MÉDIA DE MERCADO. VEÍCULO ANTIGO. LICITUDE. TARIFA DE AVALIAÇÃO DO BEM. LEGALIDADE. SERVIÇO COMPROVADO. SEGURO PRESTAMISTA. VENDA CASADA CONFIGURADA. SEGURADORA PRÉ-INDICADA. RESTITUIÇÃO DO INDÉBITO EM DOBRO. DANOS MORAIS. NÃO CONFIGURAÇÃO. VIOLAÇÃO A DIREITOS DA PERSONALIDADE NÃO DEMONSTRADA. DESCARACTERIZAÇÃO DA MORA. NÃO OCORRÊNCIA. SUCUMBÊNCIA REDISTRIBUÍDA. RECURSO CONHECIDO E PARCIALMENTE PROVIDO.
> 1. CASO EM EXAME
> Trata-se de recurso de apelação cível interposto contra sentença que, em ação revisional de contrato, julgou parcialmente procedentes os pedidos, reconhecendo apenas a ilegalidade da tarifa de registro do contrato (R$ 350,00), com restituição simples, e mantendo hígidas as demais cobranças, além de revogar a tutela de urgência, com imposição de sucumbência majoritária à autora.
> 2. QUESTÕES EM DISCUSSÃO
> A controvérsia recursal consiste em: (i) verificar se o banco se desincumbiu do ônus probatório; (ii) aferir a abusividade dos juros remuneratórios; (iii) analisar a legalidade da tarifa de avaliação do bem (Tema 958/STJ); (iv) examinar a ocorrência de venda casada na contratação do seguro prestamista (Tema 972/STJ); (v) definir a forma de restituição; (vi) apreciar o pedido de danos morais; (vii) a descaracterização da mora
> 3. RAZÕES DE DECIDIR
> 3.1. O ônus da prova foi mantido nos moldes do artigo 373 do Código de Processo Civil, sem inversão. 3.2. Tratando-se de veículo antigo, com mais de 12 (doze) anos de fabricação, não se revestem de ilicitude os juros remuneratórios estabelecidos em patamar não supera o dobro da taxa média de mercado divulgada pelo BACEN. 3.3. A tarifa de avaliação do bem é válida (Tema 958/STJ), pois comprovada a efetiva prestação do serviço e ausente onerosidade excessiva. 3.4. O instrumento contratual indica seguradora previamente definida (TOO Seguros S.A., integrante do grupo econômico do banco), sem comprovação de que foi assegurada ao consumidor a liberdade de escolha, em violação ao Tema 972/STJ. 3.5. A restituição do indébito deve ocorrer em dobro, eis que o contrato foi assinado em data muito posterior ao julgamento dos EREsp 1.413.542/RS (30/03/2021) 3.6. Na espécie, a ilicitude da cobrança indevida não foi acompanhada de circunstâncias que ultrapassem os limites do mero aborrecimento, o que afasta a configuração de dano moral. 3.7. O provimento recursal não é suficiente para a descaracterização da mora, eis que não verificada a abusividade dos juros remuneratórios, ou qualquer irregularidade ou iliquidez na documentação apresentada pela financeira. 3.8. Diante do parcial provimento, redistribui-se a sucumbência, na forma da fundamentação.
> 4. DISPOSITIVO E TESES
> Recurso conhecido e parcialmente provido, para declarar a abusividade também da contratação do seguro prestamista, e ordenar a repetição de todo o indébito na forma dobrada.
> Teses de julgamento: 1. Tratando-se de veículo antigo, a taxa de juros remuneratórios que não excede o dobro da taxa média de mercado não é considerada abusiva; 2. É válida a cobrança da tarifa de avaliação do bem quando comprovada a efetiva prestação do serviço e a não onerosidade excessiva; 3. Configura venda casada a contratação de seguro prestamista com seguradora pré-indicada, sem comprovação da liberdade de escolha do consumidor; 4. A restituição em dobro independe da prova de má-fé, bastando a violação da boa-fé objetiva, observado o marco de 30/03/2021 na forma do decidido no EREsp 1.413.542/RS.
> Dispositivos relevantes citados: Código de Defesa do Consumidor, arts. 6º, III, 39, I, 42, parágrafo único, e 51, § 1º; Código de Processo Civil, arts. 85, § 2º, 86, 98, § 3º e 373.
> Jurisprudência relevante citada: STJ, REsp n.º 1.061.530/RS, 2ª Seção, Rel. Min. Nancy Andrighi, DJe 10/03/2009; STJ, AgInt no AREsp n.º 1.183.999/RS, 3ª Turma, Rel. Min. Ricardo Villas Bôas Cueva, DJe 29/06/2018; STJ, REsp n.º 1.578.553/SP (Tema 958), 2ª Seção, Rel. Min. Paulo de Tarso Sanseverino, DJe 28/11/2018; STJ, REsp n.º 1.639.259/SP (Tema 972), 2ª Seção, Rel. Min. Paulo de Tarso Sanseverino, DJe 17/12/2018; STJ, AgInt no AREsp n.º 2.034.993/DF, 3ª Turma, Rel. Min. Paulo de Tarso Sanseverino, DJe 27/06/2022; STJ, Súmula n.º 297; TJPR, AC n.º 0001100-73.2023.8.16.0127, 4ª Câmara Cível, Rel. Desembargadora Astrid Maranhão de Carvalho Ruthes, J. 14.10.2025; TJPR, AC n.º 0001215-93.2024.8.16.0116, 4ª Câmara Cível, Rel. Desembargador Luiz Taro Oyama, J. 09.09.2025; TJPR, AC n.º 0006702-17.2022.8.16.0083, 5ª Câmara Cível, Rel. Desembargadora Substituta Luciani de Lourdes Tesseroli Maronezi, J. 09.09.2025; TJPR, AC n.º 0016917-39.2025.8.16.0021, 16ª Câmara Cível, Rel. Desembargador Marco Antonio Massaneiro, J. 25.05.2026; TJPR, AC n.º 0000376-22.2022.8.16.0057, Campina da Lagoa, 4ª Câmara Cível, Rel. Desembargador Luiz Taro Oyama, J. 06.03.2025; TJPR, AC n.º 0004120-94.2025.8.16.0194, Curitiba, 4ª Câmara Cível, Rel. Desembargador Clayton de Albuquerque Maranhão, J. 04.08.2026; TJPR, AC n.º 0005419-14.2025.8.16.0160, Sarandi, 4ª Câmara Cível, Rel. Desembargador Abraham Lincoln Merheb Calixto, J. 24.06.2026; TJPR, AC n.º 0000786-57.2022.8.16.0194, Curitiba, 4ª Câmara Cível, Rel. Desembargador Abraham Lincoln Merheb Calixto, J. 01.04.2025.

### TJPR · Apelação Cível 0001660-47.2025.8.16.0126
- regras: R13
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001660-47.2025.8.16.0126
- orgao: 14ª Câmara Cível
- relator: Juiz Subst. 2º Grau Eduardo Novacki
- julgamento: 2026-09-28
- publicacao: 2026-09-29
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038530611/Ac%C3%B3rd%C3%A3o-0001660-47.2025.8.16.0126
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 14ª Câmara Cível reconhece a venda casada quando o banco usa a mesma assinatura eletrônica em vários instrumentos e não prova manifestação autônoma do consumidor para o seguro prestamista; restituição em dobro.
- observacao: Ação declaratória com repetição de indébito. Apelo do banco parcialmente provido apenas para afastar o dano moral (mero dissabor) e redistribuir a sucumbência; venda casada e dobro mantidos. Útil quando o seguro consta de termo "apartado" assinado por replicação eletrônica. A ementa traz ao final a lista de precedentes citados, com números de outros processos, mantida como no portal. Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Palotina).

ementa:
> DIREITO DO CONSUMIDOR. APELAÇÃO CÍVEL. AÇÃO DECLARATÓRIA DE INEXISTÊNCIA DE RELAÇÃO JURÍDICA CUMULADA COM REPETIÇÃO DE INDÉBITO E INDENIZAÇÃO POR DANOS MORAIS. SEGURO PRESTAMISTA. CONTRATAÇÃO VINCULADA À OPERAÇÃO DE CRÉDITO. ASSINATURA ELETRÔNICA REPLICADA EM MÚLTIPLOS INSTRUMENTOS CONTRATUAIS. AUSÊNCIA DE DEMONSTRAÇÃO DE MANIFESTAÇÃO AUTÔNOMA E ESPECÍFICA DE VONTADE. VENDA CASADA CONFIGURADA. TEMA 972 DO STJ. COBRANÇA INDEVIDA. REPETIÇÃO DO INDÉBITO EM DOBRO. ART. 42, PARÁGRAFO ÚNICO, DO CDC. DANO MORAL NÃO CONFIGURADO. AUSÊNCIA DE COMPROVAÇÃO DE LESÃO A DIREITO DA PERSONALIDADE. MERO DISSABOR CONTRATUAL. REDISTRIBUIÇÃO DA SUCUMBÊNCIA. RECURSO CONHECIDO E PARCIALMENTE PROVIDO. I. CASO EM EXAME: Recurso de apelação interposto contra sentença que julgou parcialmente procedentes os pedidos formulados em ação declaratória de inexistência de relação jurídica cumulada com repetição de indébito e indenização por danos morais. A parte apelante sustenta a regularidade da contratação eletrônica do seguro, afasta a ocorrência de venda casada, impugna a restituição em dobro e requer o afastamento ou a redução da indenização por danos morais. II. QUESTÕES EM DISCUSSÃO: Verificar se houve efetiva comprovação de contratação autônoma e válida do seguro prestamista. Definir se a situação caracteriza venda casada nos termos da orientação fixada pelo STJ no Tema 972. Verificar a possibilidade de repetição do indébito em dobro. Examinar a configuração do dano moral e a adequação do quantum indenizatório. III. RAZÕES DE DECIDIR: 1. A utilização da mesma assinatura eletrônica para diversos instrumentos contratuais, firmados por meio do mesmo link e em horários coincidentes, impede a conclusão segura de que houve manifestação autônoma de vontade quanto à contratação do seguro prestamista. 2. A contratação acessória vinculada à operação principal de crédito sem comprovação de liberdade efetiva de escolha configura venda casada, vedada pelo art. 39, I, do Código de Defesa do Consumidor e incompatível com a orientação firmada pelo STJ no Tema Repetitivo 972.3. A repetição em dobro é cabível quando a cobrança indevida revela conduta contrária à boa-fé objetiva, independentemente da demonstração de má-fé subjetiva, conforme entendimento consolidado pela Corte Especial do STJ. 4. A cobrança indevida de seguro prestamista, desacompanhada de prova concreta de ofensa à honra, imagem, dignidade ou outro direito da personalidade, não enseja indenização por danos morais, configurando mero dissabor decorrente da relação contratual. 5. Impõe-se a redistribuição dos ônus sucumbenciais em razão da parcial reforma da sentença. IV. DISPOSITIVO E TESE: Recurso conhecido e parcialmente provido. Tese de julgamento: É abusiva a cobrança de seguro prestamista quando a instituição financeira não demonstra a existência de manifestação autônoma e específica de vontade do consumidor para sua contratação. A cobrança indevida de seguro prestamista não gera, por si só, dano moral indenizável, exigindo-se comprovação concreta de violação a direito da personalidade. DISPOSITIVOS RELEVANTES: Constituição Federal, art. 5º, XXXII; Código Civil, arts. 398, 405 e 406; Código de Processo Civil; Código de Defesa do Consumidor, arts. 4º, III, 6º, III e VIII, 39, I, e 42, parágrafo único. JURISPRUDÊNCIA RELEVANTE: STJ, REsp 1.639.259/SP (Tema 972); STJ, EAREsp 600.663/RS; STJ. Corte Especial. EAREsp 676.608/RS, Rel. Min. Og Fernandes, julgado em 21/10/2020; TJPR - 14ª Câmara Cível - 0002584-26.2024.8.16.0148 - Rolândia - Rel.: DESEMBARGADOR SUBSTITUTO EDUARDO NOVACKI - J. 04.08.2026; TJPR - 14ª Câmara Cível - 0002341-48.2025.8.16.0148 - Rolândia - Rel.: DESEMBARGADOR FRANCISCO EDUARDO GONZAGA DE OLIVEIRA - J. 06.05.2026; TJPR - 14ª Câmara Cível - 0083856-56.2024.8.16.0014 - Londrina - Rel.: DESEMBARGADORA JOSELY DITTRICH RIBAS - J. 18.02.2026; TJPR - 14ª Câmara Cível - 0002406-74.2024.8.16.0149 - Salto do Lontra - Rel.: DESEMBARGADOR SUBSTITUTO EDUARDO NOVACKI - J. 09.02.2026.

## R15 — Juros remuneratórios abusivos — taxa muito acima da média de mercado do BACEN

Tese: Em contrato de consumo, os juros remuneratórios são abusivos (CDC, art. 51, § 1º) quando a taxa contratada supera expressivamente a taxa média de mercado do BACEN para a mesma espécie de operação e o banco não justifica a diferença com circunstâncias concretas; a taxa deve ser revista para a média.

### STJ · REsp 1.061.530/RS
- regras: R15, R21
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.061.530/RS
- orgao: Segunda Seção
- relator: Min. Nancy Andrighi
- julgamento: 2008-10-22
- publicacao: 2009-03-10
- precedente_qualificado: Temas 24, 25, 26, 27, 28 e 30/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106329912
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Prova que o STJ admite a revisão das taxas de juros remuneratórios em contrato de consumo quando a abusividade, capaz de colocar o consumidor em desvantagem exagerada (CDC, art. 51, § 1º), fica cabalmente demonstrada no caso concreto (Tema 27), e que a abusividade dos encargos da normalidade descaracteriza a mora (Tema 28).
- observacao: LIMITE, a constar como ressalva na peça: o mesmo repetitivo fixa que as instituições financeiras não se sujeitam à Lei de Usura (Súmula 596/STF; Tema 24) e que juros acima de 12% ao ano, por si só, não indicam abusividade (Tema 25; mesmo teor da Súmula 382/STJ). No caso concreto o STJ manteve a taxa contratada. A proposta da relatora de teto de 2x a taxa média ficou vencida: a média é referencial, não limite (ver a entrada ADV REsp 2.009.614/SC). Os textos das Súmulas 382/STJ e 596/STF foram conferidos nos votos abertos, não como documento autônomo. Tema 1378/STJ pendente (suspensos só REsp e AREsp). Publicação pela data do Jusbrasil.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Prova que o STJ chancela a limitação à taxa média quando a abusividade é fundamentada em circunstâncias concretas (taxa de 2 a 3 vezes a média em crédito de risco reduzido, banco que não comprova custo de captação, spread e risco de crédito), e não só na comparação aritmética com a média.
- observacao: O recurso do banco foi desprovido com apoio nas Súmulas 5, 7 e 83/STJ: o STJ não reexaminou os fatos, mas afirmou que a decisão de origem estava de acordo com sua jurisprudência por não se limitar ao cotejo com a média. A peça deve, por isso, narrar as peculiaridades concretas e imputar ao banco o ônus de justificar a taxa. Tema 1378/STJ pendente. Publicação pela data do Jusbrasil.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O TJPR limita à taxa média do BACEN os juros de empréstimo pessoal não consignado que superam em mais de duas vezes a média sem justificativa ligada ao perfil do consumidor, e manda devolver em dobro os pagamentos posteriores à modulação do EAREsp 676.608/RS.
- observacao: Apelação do banco desprovida. O critério do caso é o múltiplo da média (mais de duas vezes) somado à falta de justificativa concreta; a peça deve trazer a comparação com a série BACEN da mesma espécie e data. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O TJPR mantém a limitação dos juros de empréstimo pessoal à taxa média do BACEN diante de discrepância significativa para a mesma espécie e período, com restituição do pago a maior e afastamento da mora.
- observacao: A taxa média é tratada como vetor relevante, não critério absoluto: a peça precisa mostrar a discrepância concreta. Repetição conforme a modulação do EAREsp 676.608/RS. Fonte: portal de jurisprudência do TJPR (comarca de União da Vitória). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

ementa:
> DIREITO CIVIL E BANCÁRIO. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO DE EMPRÉSTIMO PESSOAL. JUROS REMUNERATÓRIOS. TAXA SUPERIOR À MÉDIA DE MERCADO. REPETIÇÃO DO INDÉBITO. RECURSO DESPROVIDO.I. CASO EM EXAME1. Apelação cível interposta contra sentença que julgou procedente ação revisional de contrato de empréstimo pessoal, reconhecendo a abusividade da taxa de juros remuneratórios pactuada, determinando sua limitação à taxa média de mercado divulgada pelo Banco Central do Brasil, bem como a restituição dos valores pagos a maior, afastando-se, ainda, os encargos moratórios.II. QUESTÃO EM DISCUSSÃO2. A questão em discussão consiste em: (i) saber se a simples estipulação de juros remuneratórios superiores à taxa média de mercado autoriza, no caso concreto, a revisão judicial das cláusulas contratuais; (ii) saber se é cabível a restituição dos valores pagos a maior, inclusive em dobro, diante do reconhecimento da abusividade; e (iii) saber se o reconhecimento da abusividade no período de normalidade contratual afasta a caracterização da mora do devedor.III. RAZÕES DE DECIDIR3. Embora as instituições financeiras não se submetam à limitação da Lei de Usura, admite-se a revisão dos juros remuneratórios em situações excepcionais, quando demonstrada abusividade capaz de colocar o consumidor em desvantagem exagerada, considerada a taxa média de mercado como relevante vetor de aferição, sem que se trate de critério absoluto.4. Constatada, no caso concreto, a discrepância significativa entre a taxa pactuada e a média de mercado para operações da mesma espécie e período, impõe-se a limitação dos juros remuneratórios aos parâmetros divulgados pelo Banco Central do Brasil.5. Reconhecida a abusividade no período de normalidade contratual, é devida a restituição dos valores pagos indevidamente, observada a modulação dos efeitos fixada pelo Superior Tribunal de Justiça quanto à aplicação da repetição em dobro, bem como o afastamento dos encargos moratórios.IV. DISPOSITIVO E TESE6. Recurso desprovido.Tese de julgamento:“1. A taxa média de mercado divulgada pelo Banco Central do Brasil constitui importante parâmetro para a aferição da abusividade dos juros remuneratórios, devendo ser analisadas as peculiaridades do caso concreto.”“2. Reconhecida a abusividade dos juros no período de normalidade contratual, é cabível a restituição dos valores pagos a maior, bem como o afastamento da mora do devedor.”Dispositivos relevantes citados:Código de Defesa do Consumidor, art. 42, parágrafo único.Código de Processo Civil, art. 487, I; art. 85, § 11.Jurisprudência relevante citada:STJ, Recurso Especial nº 1.061.530/RS, Rel. Ministra Nancy Andrighi, Segunda Seção, j. 22.10.2008.STJ, Agravo Interno no AREsp nº 2.150.980/RS, Rel. Ministra Nancy Andrighi, Terceira Turma, j. 09.11.2022.STJ, EAREsp nº 676.608/RS, Rel. Ministro Og Fernandes, Corte Especial, j. 21.10.2020.

## R16 — Juros remuneratórios — taxa não comprovada (Súmula 530/STJ)

Tese: Nos contratos bancários, inclusive cheque especial e conta garantida, quando a taxa de juros efetivamente contratada não pode ser comprovada — por ausência de pactuação ou porque o banco não juntou o instrumento —, os juros remuneratórios são limitados à taxa média de mercado divulgada pelo BACEN para a mesma modalidade, salvo se a taxa cobrada for mais vantajosa para o devedor (Súmula 530/STJ; Temas 233 e 234/STJ).

### STJ · REsp 1.112.879/PR
- regras: R16, R19, CONTA-CAPDIARIA
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.112.879/PR
- orgao: Segunda Seção
- relator: Min. Nancy Andrighi
- julgamento: 2010-05-12
- publicacao: 2010-05-19
- precedente_qualificado: Temas 233 e 234/STJ (repetitivo); Súmula 530/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106318712
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Leading case dos Temas 233 e 234, julgado em ação revisional de cheque especial cujo contrato não foi juntado: a Segunda Seção mandou aplicar a taxa média de mercado da espécie aos juros remuneratórios e afastou a capitalização por falta de prova da pactuação expressa.
- observacao: A tese 1 fala em 'mútuo em que a disponibilização do capital é imediata'. No caso concreto (cheque especial de pessoa jurídica, origem TJPR), o recurso era do banco: a origem, sem contrato nos autos, limitara os juros a 6% e depois 12% ao ano; a Seção trocou esse limite pela taxa média da espécie (tese 2) e manteve o afastamento da capitalização. É dessa redação que a Quarta Turma extrai a distinção do REsp 2.065.222/PR (ADV, abaixo); a Súmula 530/STJ (2015) generalizou a regra para os 'contratos bancários'. Unânime. Ementa do inteiro teor; correção: junção de linha partida na extração ('taxa de / juros').

ementa:
> BANCÁRIO. RECURSO ESPECIAL. AÇÃO REVISIONAL DE CLÁUSULAS DE CONTRATO BANCÁRIO. INCIDENTE DE PROCESSO REPETITIVO. JUROS REMUNERATÓRIOS. CONTRATO QUE NÃO PREVÊ O PERCENTUAL DE JUROS REMUNERATÓRIOS A SER OBSERVADO.
> I - JULGAMENTO DAS QUESTÕES IDÊNTICAS QUE CARACTERIZAM A MULTIPLICIDADE. ORIENTAÇÃO - JUROS REMUNERATÓRIOS
> 1 - Nos contratos de mútuo em que a disponibilização do capital é imediata, o montante dos juros remuneratórios praticados deve ser consignado no respectivo instrumento. Ausente a fixação da taxa no contrato, o juiz deve limitar os juros à média de mercado nas operações da espécie, divulgada pelo Bacen, salvo se a taxa cobrada for mais vantajosa para o cliente.
> 2 - Em qualquer hipótese, é possível a correção para a taxa média se for verificada abusividade nos juros remuneratórios praticados.
> II - JULGAMENTO DO RECURSO REPRESENTATIVO - Consignada, no acórdão recorrido, a abusividade na cobrança da taxa de juros, impõe-se a adoção da taxa média de mercado, nos termos do entendimento consolidado neste julgamento.
> - Nos contratos de mútuo bancário, celebrados após a edição da MP nº 1.963-17/00 (reeditada sob o nº 2.170-36/01), admite-se a capitalização mensal de juros, desde que expressamente pactuada.
> Recurso especial parcialmente conhecido e, nessa parte, provido. Ônus sucumbenciais redistribuídos.

### STJ · REsp 2.190.399/PR
- regras: R16
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.190.399/PR
- orgao: Terceira Turma
- relator: Min. Nancy Andrighi
- julgamento: 2025-05-26
- publicacao: 2025-05-29
- precedente_qualificado: não (aplica os Temas 233 e 234/STJ e a Súmula 530/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6302151863
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em revisão de conta corrente sem o contrato nos autos, a Terceira Turma reformou o TJPR, que só limitava os juros acima do dobro da média, e limitou os juros remuneratórios à taxa média de mercado 'independentemente da análise de sua abusividade' (Temas 233/234 e Súmula 530).
- observacao: Recurso do correntista (espólio) parcialmente conhecido e provido por unanimidade (sessão virtual de 20 a 26/05/2025); o ponto das tarifas não foi conhecido (Súmula 283/STF). Diverge da Quarta Turma no REsp 2.065.222/PR (ADV, abaixo). No mesmo sentido, na própria Quarta Turma: AgInt nos EDcl no REsp 2.048.901/PR (12/03/2024, em CONTA-ENCARGOS) e REsp 2.041.009/PR (30/03/2026, conta corrente com contrato de 1992 não juntado; lido no inteiro teor e não listado). O item 4 da ementa traz aspas de fechamento sem abertura, como no original.

ementa:
> DIREITO CIVIL, PROCESSUAL CIVIL E DO CONSUMIDOR. RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. VIOLAÇÃO DO ART. 489 DO CPC. INOCORRÊNCIA. FUNDAMENTO DO ACÓRDÃO NÃO IMPUGNADO. SÚMULA 283/STF. JUROS REMUNERATÓRIOS. AUSENTE A JUNTADA DO CONTRATO. MÉDIA DE MERCADO. TEMAS 233 E 234/STJ. REPETITIVOS.
> 1. Ação revisional de contrato bancário.
> 2. Devidamente analisadas e discutidas as questões de mérito, e fundamentado corretamente o acórdão recorrido, de modo a esgotar a prestação jurisdicional, não há que se falar em violação ao art. 489 do CPC.
> 3. A existência de fundamento do acórdão recorrido não impugnado - quando suficiente para a manutenção de suas conclusões - impede a apreciação do recurso especial.
> 4. Nos contratos de mútuo em que a disponibilização do capital é imediata, o montante dos juros remuneratórios praticados deve ser consignado no respectivo instrumento. Ausente a fixação da taxa no contrato o juiz deve limitar os juros à média de mercado nas operações da espécie, divulgada pelo Bacen, salvo se a taxa cobrada for mais vantajosa para o cliente." (REsp 1112879/PR, 2ª Seção, DJe 19/05/2010, Temas 233 e 234). Aplicação da Súmula 530/STJ.
> 5. Recurso especial parcialmente conhecido e, nesta extensão, parcialmente provido.

### STJ · REsp 2.065.222/PR
- regras: R16
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.065.222/PR
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2025-12-16
- publicacao: 2025-12-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6265811751
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: LIMITE a antecipar: para a Quarta Turma, no contrato de abertura de crédito em conta corrente (cheque especial), em que não há disponibilização imediata do crédito, a falta do instrumento não leva por si à taxa média; exige-se prova de discrepância significativa entre a taxa praticada e a média (no caso, o TJPR limitou só os meses acima do dobro da média, apurados em perícia).
- observacao: Recurso do correntista desprovido por unanimidade (sessão virtual de 09 a 16/12/2025); cita o AgInt no REsp 2.051.810/SC (Quarta Turma, 2023) e foi reafirmado no AgInt no REsp 2.015.710/PR (Quarta Turma, 18/05/2026). DIVERGÊNCIA: a Terceira Turma (REsp 2.190.399/PR) e a própria Quarta Turma em outros acórdãos (AgInt nos EDcl no REsp 2.048.901/PR, 2024; REsp 2.041.009/PR, março de 2026) aplicaram a Súmula 530 a conta corrente sem contrato. No TJPR, a 14ª Câmara Cível também afasta a Súmula 530 para os juros flutuantes da conta (distinguishing), e a 13ª e a 15ª aplicam. Na peça: pedir a taxa média pela Súmula 530 e, subsidiariamente, provar a discrepância pela perícia sobre os extratos (série BACEN da modalidade). O Tema 1378/STJ (critérios de abusividade dos juros; afetado e pendente) pode alterar a análise subsidiária.

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. REVISÃO DE CONTRATO BANCÁRIO. JUROS REMUNERATÓRIOS. ABUSIVIDADE. LIMITAÇÃO À MÉDIA DE MERCADO. RECURSO NÃO PROVIDO.
> 1. Nos contratos de abertura de crédito em conta corrente (cheque-especial), para os quais inexiste disponibilização imediata do crédito, a ausência do instrumento respectivo nos autos não enseja por si o reconhecimento da abusividade das taxas praticadas no período. Para tanto, deve ser comprovada a ocorrência de significativa discrepância entre a taxa média de mercado e aquela praticada pela instituição financeira.
> 2. Não foram opostos embargos de declaração para sanar a alegada omissão na apreciação da tese de se tratar de responsabilidade extracontratual a impor a incidência de juros de mora desde o evento danoso e também da tese de existência de lastro na prova pericial para fixação do valor do proveito econômico para o fim de arbitramento dos honorários advocatícios. Dessa forma, à falta do indispensável prequestionamento, incide, por analogia, o óbice das Súmulas 282 e 356 do STF.
> 3. Resultado do Julgamento: Recurso especial não provido.

### TJPR · Apelação Cível 0009951-67.2017.8.16.0174
- regras: R16, R19, CONTA-ENCARGOS, CONTA-EXIBICAO
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0009951-67.2017.8.16.0174
- orgao: 13ª Câmara Cível
- relator: Des. Fernando Ferreira de Moraes
- julgamento: 2026-09-04
- publicacao: 2026-09-04
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038829411/Ac%C3%B3rd%C3%A3o-0009951-67.2017.8.16.0174
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Conta corrente com cheque especial de pessoa jurídica, sem o contrato juntado pelo banco: juros limitados mês a mês à média da modalidade (série BACEN 20727, cheque especial PJ) pela Súmula 530, rejeitada a tese de 'uma vez e meia a média'; capitalização expurgada com recálculo em juros simples; 228 lançamentos de tarifas sem previsão restituídos; mora descaracterizada.
- observacao: Recurso do banco desprovido. Repetição simples (o correntista não recorreu). Fonte: portal de jurisprudência do TJPR (comarca de União da Vitória).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. CONTA CORRENTE COM UTILIZAÇÃO DE CHEQUE ESPECIAL — PESSOA JURÍDICA. PACTA SUNT SERVANDA. MITIGAÇÃO. POSSIBILIDADE DE REVISÃO DE CLÁUSULAS ABUSIVAS. JUROS REMUNERATÓRIOS. INSTRUMENTO CONTRATUAL. NÃO JUNTADO. ÔNUS PROBATÓRIO DO FORNECEDOR (ART. 373, INCISO II DO CPC E ART. 6º, INCISO VIII DO CDC). TAXA PACTUADA. NÃO VERIFICADA. LIMITAÇÃO À MÉDIA DE MERCADO. DEVIDA. SÚMULA 530 DO STJ. INCIDENTE. TESE ALTERNATIVA DE LIMITAÇÃO EM UMA VEZ E MEIA A MÉDIA. AFASTADA. CAPITALIZAÇÃO DE JUROS. PACTUAÇÃO EXPRESSA. AUSENTE. SÚMULA 539 DO STJ E RESP Nº 973.827/RS. RECÁLCULO EM JUROS SIMPLES. MANTIDO. CAPITALIZAÇÃO ANUAL (ART. 591 DO CC). INAPLICABILIDADE AOS CONTRATOS BANCÁRIOS. TARIFAS BANCÁRIAS. 228 LANÇAMENTOS SEM PREVISÃO CONTRATUAL OU AUTORIZAÇÃO ESPECÍFICA. RESTITUIÇÃO. DEVIDA. SÚMULA 44 DO TJPR. MORA. DESCARACTERIZADA. REPETIÇÃO SIMPLES. DEFINIDA. SÚMULA 322 DO STJ. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS ARBITRADOS. RECURSO NÃO PROVIDO.

### TJPR · Apelação Cível 0003555-14.2023.8.16.0126
- regras: R16, R19, CONTA-ENCARGOS
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0003555-14.2023.8.16.0126
- orgao: 15ª Câmara Cível
- relator: Des.ª Denise Kruger Pereira
- julgamento: 2026-10-24
- publicacao: 2026-10-26
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000039041001/Ac%C3%B3rd%C3%A3o-0003555-14.2023.8.16.0126
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Cheque especial em conta corrente sem o instrumento juntado pelo banco: aplica-se a taxa média de mercado (Súmula 530), afasta-se a capitalização por falta de pactuação expressa e são ilegais as tarifas sem prova de previsão contratual ou autorização (Súmula 44/TJPR).
- observacao: Apelação do banco desprovida e recurso adesivo do correntista provido. ATENÇÃO à repetição: o acórdão aplica a modulação do EAREsp 676.608/RS (simples até 29/03/2021, dobro depois); o Tema 929/STJ (REsp 1.963.770/CE, em R26) foi fixado sem modulação — não citar este julgado para o dobro. A íntegra do portal não repete o número do processo, mas descreve o mesmo caso (comarca, partes e dispositivo conferidos). Fonte: portal de jurisprudência do TJPR (comarca de Palotina). Correção: retirado o rótulo 'EMENTA:' que abre o texto do portal.

ementa:
> DIREITO CIVIL, DIREITO DO CONSUMIDOR E DIREITO BANCÁRIO. AÇÃO DE REVISÃO CONTRATUAL. CONTRATO DE CHEQUE ESPECIAL EM CONTA CORRENTE. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSO DE APELAÇÃO DA INSTITUIÇÃO FINANCEIRA. AUSÊNCIA DE JUNTADA DO INSTRUMENTO CONTRATUAL PELO BANCO. JUROS REMUNERATÓRIOS LIMITADOS À TAXA MÉDIA DE MERCADO. SÚMULA 530 DO STJ. CAPITALIZAÇÃO DE JUROS AFASTADA POR AUSÊNCIA DE PACTUAÇÃO EXPRESSA. REPETIÇÃO DO INDÉBITO. FORMA SIMPLES ATÉ 29.03.2021 E EM DOBRO A PARTIR DE 30.03.2021. MODULAÇÃO DO EAREsp 676.608/RS. IMPUGNAÇÃO AOS CÁLCULOS E AO LAUDO PERICIAL QUE NÃO ALTERA O DESFECHO. COMPENSAÇÃO DE VALORES COMO CONSECTÁRIO LEGAL. CORREÇÃO MONETÁRIA DESDE CADA DESEMBOLSO E JUROS DE MORA A PARTIR DA CITAÇÃO. RECURSO CONHECIDO E DESPROVIDO.RECURSO ADESIVO DO AUTOR. TARIFAS BANCÁRIAS. AUSÊNCIA DE COMPROVAÇÃO DE PREVISÃO CONTRATUAL OU AUTORIZAÇÃO. ILEGALIDADE. SÚMULA 44 DO TJPR. RESTITUIÇÃO NA FORMA SIMPLES ATÉ 29.03.2021 E EM DOBRO A PARTIR DE 30.03.2021. REDISTRIBUIÇÃO DOS ÔNUS SUCUMBENCIAIS EM DESFAVOR DA INSTITUIÇÃO FINANCEIRA. RECURSO CONHECIDO E PROVIDO.I. CASO EM EXAME1. Recursos de Apelação interpostos contra sentença que julgou parcialmente procedentes os pedidos formulados em Ação de Revisão Contratual referente a contrato de cheque especial, determinando a aplicação da taxa média de mercado divulgada pelo Banco Central aos juros remuneratórios e o afastamento da capitalização de juros, ambos por ausência de pactuação expressa, com repetição do indébito na forma simples até 29.03.2021 e em dobro a partir de 30.03.2021, mantida a legitimidade da cobrança das tarifas bancárias.II. QUESTÕES EM DISCUSSÃO2. As questões em discussão consistem em saber: (i) se, ausente a juntada do instrumento contratual, subsistem a limitação dos juros remuneratórios à taxa média de mercado e o afastamento da capitalização; (ii) se é devida a repetição do indébito em dobro sem demonstração de má-fé; (iii) se são legítimas as tarifas bancárias cobradas, ante a ausência de comprovação de previsão contratual ou autorização; (iv) se deve ser redistribuída a sucumbência.III. RAZÕES DE DECIDIR3. Não juntado o contrato pela instituição financeira, à qual incumbia o ônus, aplica-se a taxa média de mercado divulgada pelo Banco Central, nos termos da Súmula 530 do STJ.4. A capitalização de juros exige pactuação expressa, cuja demonstração não verificou ante a ausência do contrato, impondo-se o seu afastamento.5. As tarifas bancárias somente podem ser cobradas quando previstas no contrato ou expressa e previamente autorizadas pelo correntista, ainda que de forma genérica (Súmula 44 do TJPR); não comprovada a contratação, ante a não juntada do contrato, é ilegal a cobrança, impondo-se a restituição.6. A repetição do indébito, na esteira da modulação fixada no EAREsp 676.608/RS, opera-se de forma simples quanto às cobranças anteriores a 30.03.2021 e em dobro quanto às posteriores, independentemente de má-fé.7. Reconhecida a procedência integral dos pedidos, impõe-se a redistribuição dos ônus sucumbenciais em desfavor da instituição financeira.IV. DISPOSITIVO E TESE8. Apelação da instituição financeira conhecida e desprovida. Recurso adesivo do autor conhecido e provido.Teses de julgamento: “1. Ausente a juntada do instrumento contratual pela instituição financeira, aplica-se a taxa média de mercado aos juros remuneratórios (Súmula 530/STJ) e afasta-se a capitalização por falta de pactuação expressa. 2. A cobrança de tarifas bancárias sem comprovação de previsão contratual ou autorização é ilegal (Súmula 44/TJPR), impondo-se a restituição. 3. A repetição do indébito segue a modulação do EAREsp 676.608/RS: simples até 29.03.2021 e em dobro a partir de 30.03.2021.”___________Dispositivos relevantes citados: CC, art. 368; CPC, arts. 85, §§ 2º e 11, 86, 373, incisos I e II, e 997, § 2º.Jurisprudência relevante citada: STJ, REsp 1.061.530/RS, Rel. Min. Nancy Andrighi, Segunda Seção, j. 22.10.2008, DJe 10.03.2009; STJ, REsp 973.827/RS, Rel. p/ Acórdão Min. Maria Isabel Gallotti, Segunda Seção; STJ, EAREsp 676.608/RS, Rel. Min. Og Fernandes, Corte Especial; TJPR - 15ª Câmara Cível - 0022775-38.2026.8.16.0014 - Londrina - Rel.: DESEMBARGADORA DENISE KRUGER PEREIRA - J. 20.06.2026; TJPR - 15ª Câmara Cível - 0003155-19.2025.8.16.0194 - Curitiba - Rel.: DESEMBARGADOR JUCIMAR NOVOCHADLO - J. 22.08.2026; TJPR - 15ª Câmara Cível - 0000820-07.2025.8.16.0039 - Andirá - Rel.: DESEMBARGADORA LUCIANE BORTOLETO - J. 01.08.2026; Súmula 530/STJ; Súmula 297/STJ; Súmula 44/TJPR.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- julgamento: 2023-03-22
- publicacao: 2023-03-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-mg/1793581335
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Apelação da empresa tomadora de cédulas de crédito comercial provida em parte para limitar os juros remuneratórios a 12% a.a. (omissão do CMN), vedar a comissão de permanência e substituir o CDI pelo INPC.
- observacao: Complementa os acórdãos do TJPR desta tese. O voto mantém a capitalização, por ser pactuada (Súmula 93/STJ), ressalva que a petição deve prever. Data de julgamento conferida em 29/10/2026 na citação do acórdão feita por decisão da Vice-Presidência do TJMG ("julgamento em 22/03/2023, publicação da súmula em 23/03/2023"); publicação pela data do Jusbrasil. O número do processo foi montado a partir do título do Jusbrasil, no padrão CNJ.

ementa:
> APELAÇÃO CÍVEL - CÉDULA DE CRÉDITO COMERCIAL - JUROS REMUNERATÓRIOS - ABUSIVIDADE - FIXAÇÃO EM 12% AO ANO - CABIMENTO - COMISSÃO DE PERMANÊNCIA - INADMISSIBILIDADE - CDI (CERTIFICADO DE DEPÓSITO INTERBANCÁRIO) - ÍNDICE DE CORREÇÃO - AFASTAMENTO - SUBSTITUIÇÃO PELO INPC. - As cédulas de crédito rural, comercial e industrial acham-se submetidas a regramento próprio (Lei nº 6.840/80 e Decreto-Lei 413/69) que conferem ao Conselho Monetário Nacional o dever de fixar os juros a serem praticados. Diante da omissão desse órgão governamental, incide a limitação de 12% ao ano, prevista no Decreto n.º 22.626/33 (Lei da Usura) - Constatado que os juros remuneratórios foram estipulados em taxa superior ao limite legal de 12% ao ano, deve ser reconhecida sua abusividade. - Nas cédulas de crédito rural, comercial e industrial não se admite a cobrança de comissão de permanência. - Nos termos da súmula nº 176 do Superior Tribunal de Justiça, é nula a cláusula que prevê a aplicação do CDI (certificado de depósito interbancário), fornecido pela CETIP, como índice de correção monetária, devendo tal índice ser substituído pelo INPC.

### TJPR · Apelação Cível 0006472-61.2019.8.16.0153
- regras: R17
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0006472-61.2019.8.16.0153
- orgao: 14ª Câmara Cível
- relator: Des. Francisco Eduardo Gonzaga de Oliveira
- julgamento: 2023-03-06
- publicacao: 2023-03-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000022628601/Ac%C3%B3rd%C3%A3o-0006472-61.2019.8.16.0153
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito industrial (DL 413/1969), o TJPR acolhe a apelação da tomadora e limita os juros remuneratórios a 12% ao ano pela omissão do CMN, reformando a sentença que só os adequava à taxa média de mercado.
- observacao: Ação revisional da tomadora (pessoa jurídica); apelação da autora parcialmente provida (limitação a 12% a.a.) e apelação do banco conhecida em parte e desprovida. É cédula industrial, não CCB. A capitalização foi mantida por estar pactuada (Súmula 93/STJ; DL 413/1969, art. 14, VI), ressalva a prever na petição. A íntegra cita o próprio CNJ. Correções na ementa: "APELAÇAO" para "APELAÇÃO" e "CONTRATAÇAO" para "CONTRATAÇÃO" (til faltando). Fonte: portal de jurisprudência do TJPR (comarca de Santo Antônio da Platina). Ementa copiada do portal sem o rótulo inicial.

ementa:
> APELAÇÕES CÍVEIS. AÇÃO REVISIONAL. CÉDULA DE CRÉDITO INDUSTRIAL. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSO DE AMBAS AS PARTES LITIGANTES.
> APELAÇÃO CÍVEL (01). RECURSO DO BANCO RÉU. 1. INADMISSIBILIDADE PARCIAL DO APELO NO TOCANTE AOS JUROS REMUNERATÓRIOS E À MULTA CONTRATUAL. CONSTATAÇÃO DE AUSÊNCIA DE INTERESSE RECURSAL E DE VIOLAÇÃO AO PRINCÍPIO DA DIALETICIDADE, RESPECTIVAMENTE. 2. ALEGADA INÉPCIA DA INICIAL. NÃO ACOLHIMENTO. ENCARGOS CONSIDERADOS ABUSIVOS DEVIDAMENTE DELINEADOS, COM A INDICAÇÃO DO VALOR A SER RESTITUÍDO PELO BANCO. PRELIMINAR REJEITADA. 3. ALEGADA PRESCRIÇÃO.
> INOCORRÊNCIA. INTERRUPÇÃO DO PRAZO PRESCRICIONAL EM RAZÃO DE AÇÃO DE EXIBIÇÃO DE DOCUMENTOS ANTERIORMENTE AJUIZADA. PREJUDICIAL DE MÉRITO REJEITADA. 4. REVISÃO DAS CLÁUSULAS CONTRATADAS. POSSIBILIDADE. RELATIVIZAÇÃO DA FORÇA OBRIGATÓRIA DO CONTRATO (PRINCÍPIO DO PACTA SUNT SERVANDA). 5. restituição do indébito. desnecessidade de prova do erro. medida necessária para evitar o locupletamento indevido do banco. sentença mantida nesses pontos.RECURSO CONHECIDO EM PARTE E, PARTE CONHECIDA, NÃO PROVIDO.
> APELAÇÃO CÍVEL (02). RECURSO DA PARTE AUTORA. 1. JUROS REMUNERATÓRIOS. CÉDULA DE CRÉDITO INDUSTRIAL. MODALIDADE CONTRATUAL SUBMETIDA À REGRAMENTO PRÓPRIO. LIMITAÇÃO À 12% AO ANO DEVIDA. PRECEDENTES. SENTENÇA REFORMADA NO PONTO. 2. CAPITALIZAÇÃO DOS JUROS (ANATOCISMO). PRÁTICA AUTORIZADA PELA LEGISLAÇÃO DE REGÊNCIA E EXPRESSAMENTE PREVISTA EM CONTRATO. AUSÊNCIA DE ABUSIVIDADE. SÚMULA 93 DO SUPERIOR TRIBUNAL DE JUSTIÇA. 3. SEGURO. PROVA DOCUMENTAL INSUFICIENTE À COMPROVAÇÃO DA CONTRATAÇÃO DO SEGURO E DO VALOR REFERENTE AO PRÊMIO. ILEGALIDADE NA COBRANÇA RECONHECIDA. SENTENÇA REFORMADA NO PONTO. 4. SUCUMBÊNCIA MÍNIMA. NÃO ACOLHIMENTO, EM RAZÃO DA RELEVÂNCIA ECONÔMICA DO PEDIDO SUCUMBIDO. REDISTRIBUIÇÃO DA SUCUMBÊNCIA, POR OUTRO LADO, DEVIDA, EM RAZÃO DA REFORMA DA SENTENÇA EM GRAU RECURSAL. SENTENÇA PARCIALMENTE REFORMADA, COM NOVA FIXAÇÃO DE HONORÁRIOS ADVOCATÍCIOS. Recurso conhecido E PARCIALMENTE PROVIDO.

### TJPR · Apelação Cível 0002123-04.2023.8.16.0079
- regras: R17
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002123-04.2023.8.16.0079
- orgao: 16ª Câmara Cível
- relator: Juíza Subst. 2º Grau Cristiane Santos Leite
- julgamento: 2024-10-21
- publicacao: 2024-10-21
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000030358741/Ac%C3%B3rd%C3%A3o-0002123-04.2023.8.16.0079
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito rural, o TJPR dá provimento à apelação dos embargantes para limitar os juros a 12% ao ano (DL 167/1967 e Decreto 22.626/1933, na falta de deliberação do CMN) e descaracterizar a mora, com recálculo do débito.
- observacao: Embargos à execução; sentença de improcedência reformada. Cédula rural, não CCB; a ementa estende a regra às cédulas comercial e industrial. A íntegra cita o próprio CNJ. O voto ressalva entendimento pessoal só quanto aos honorários. Fonte: portal de jurisprudência do TJPR (comarca de Dois Vizinhos). Ementa copiada do portal sem o rótulo inicial.

ementa:
> DIREITO BANCÁRIO. APELAÇÃO CÍVEL.
> EMBARGOS À EXECUÇÃO. SENTENÇA DE IMPROCEDÊNCIA. CÉDULA DE CRÉDITO RURAL. LIMITAÇÃO DE JUROS. DECRETO-LEI Nº 167/67. TAXA DE JUROS CONSIDERADA ABUSIVA. DESCARACTERIZAÇÃO DA MORA. RECURSO PROVIDO. I. CASO EM EXAME 1.1. Recurso de Apelação Cível interposto em face da sentença que julgou improcedentes os Embargos à Execução e condenou os embargantes ao pagamento das custas, despesas processuais e honorários advocatícios.II. QUESTÕES EM DISCUSSÃO2.1. Limitação da taxa de juros a 12% ao ano, conforme Decreto-Lei nº 167/67. 2.2. Alegação de abusividade nas cobranças dos encargos moratórios e inadimplemento do contrato. 2.3. Descaracterização da mora devido à cobrança de encargos abusivos.III. RAZÕES DE DECIDIR3.1. Com base no entendimento do STJ e nos termos do Decreto-Lei nº 167/67, as cédulas de crédito rural, comercial e industrial têm seus juros regulados pela autoridade monetária, sendo limitada a taxa a 12% ao ano na ausência de autorização específica.3.2. Reconhecida a abusividade na cobrança de juros remuneratórios no período de normalidade contratual, o que implica na descaracterização da mora, conforme entendimento do STJ (REsp 1.061.530/RS). 3.3. A descaracterização da mora é consequência lógica do reconhecimento da cobrança abusiva, dispensando pedido expresso nos autos.IV. DISPOSITIVO E TESE 4.1. Recurso provido para limitar a taxa de juros a 12% ao ano e reconhecer a descaracterização da mora, determinando o recálculo do débito pelo juízo de origem. 4.2. Tese fixada: "A cobrança de juros acima de 12% ao ano contraria o disposto no Decreto-Lei n° 167/67 autorizando a limitação e a abusividade na cobrança de encargos no período de normalidade contratual implica na descaracterização da mora, com consequente recálculo do débito."

### TJPR · Apelação Cível 0001407-09.2024.8.16.0057
- regras: R17
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001407-09.2024.8.16.0057
- orgao: 13ª Câmara Cível
- relator: Juiz Subst. 2º Grau Marcel Luis Hoffmann
- julgamento: 2026-07-24
- publicacao: 2026-07-24
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037147961/Ac%C3%B3rd%C3%A3o-0001407-09.2024.8.16.0057
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito rural com juros de 16,15% a.a. sob a rubrica de "recursos livres", o TJPR mantém a limitação a 12% ao ano (legislação específica do crédito rural) e a descaracterização da mora decorrente da cobrança abusiva.
- observacao: Apelação da credora (cooperativa de crédito) desprovida. Cédula rural pignoratícia e hipotecária, não CCB. A ementa afasta o argumento de "recursos livres", que o banco costuma opor com base no MCR 6-3. A íntegra cita o próprio CNJ. Fonte: portal de jurisprudência do TJPR (comarca de Campina da Lagoa). Ementa copiada do portal sem o rótulo inicial ("Ementa:").

ementa:
> Direito civil e processual civil. Apelação cível. Embargos à execução. Cédula de crédito rural. Juros remuneratórios acima de 12% ao ano. Abusividade reconhecida em sentença. Descaracterização da mora mantida. Recurso desprovido.I. CASO EM EXAME1. Apelação interposta contra sentença que, em embargos à execução fundada em cédula de crédito rural, afastou a nulidade do título, reconheceu a abusividade de juros remuneratórios fixados acima de 12% ao ano e declarou a descaracterização da mora, com parcial extinção da execução.II. QUESTÃO EM DISCUSSÃO2. Há duas questões em discussão: (i) saber se embargos de declaração não conhecidos possuem efeito interruptivo do prazo recursal; (ii) saber se o reconhecimento da abusividade dos juros remuneratórios no período de normalidade contratual é suficiente para afastar a mora, independentemente do adimplemento parcial da obrigação.III. RAZÕES DE DECIDIR3. Os embargos de declaração, quando tempestivos e com indicação de vícios de omissão, contradição, obscuridade ou erro material interrompem o prazo recursal, salvo hipóteses de manifesta inadmissibilidade, conforme entendimento da Corte Especial do Superior Tribunal de Justiça.4. No caso, os embargos foram tempestivos e adequadamente fundamentados, devendo ser reconhecido o efeito interruptivo previsto no art. 1.026 do CPC.5. A limitação dos juros remuneratórios a 12% ao ano em cédula de crédito rural decorre da legislação específica e da jurisprudência consolidada, sendo abusiva a estipulação superior, ainda que sob a rubrica de “recursos livres”.6. O reconhecimento da abusividade dos encargos exigidos no período de normalidade contratual é suficiente para descaracterizar a mora, independentemente do percentual efetivamente pago pelo devedor, nos termos da orientação firmada em recurso repetitivo pelo Superior Tribunal de Justiça.7. A jurisprudência do Tribunal de Justiça do Estado do Paraná é pacífica no sentido de que, em contratos de crédito rural, a cobrança de juros abusivos enseja o afastamento da mora, em consonância com o entendimento do STJ.IV. DISPOSITIVO E TESE8. Recurso conhecido e desprovido.Tese de julgamento: “1. Embargos de declaração tempestivos, ainda que equivocadamente não conhecidos na origem, interrompem o prazo recursal quando presentes os requisitos de admissibilidade. 2. O reconhecimento da abusividade de encargos no período de normalidade contratual, como juros remuneratórios superiores a 12% ao ano em crédito rural, descaracteriza a mora, independentemente do adimplemento parcial da dívida.”Dispositivos relevantes citados: CPC/2015, arts. 1.009, 1.022, 1.026 e 1.010; Decreto-Lei 167/67, art. 5º, parágrafo único.Jurisprudência relevante citada: STJ, EAREsp 175.648/RS, Rel. Min. Og Fernandes, Corte Especial, j. 24.10.2016; STJ, REsp 1.061.530/RS (Tema repetitivo), Rel. Min. Nancy Andrighi, Segunda Seção, j. 22.10.2008; TJPR, AC nº 0001723-62.2025.8.16.0097, 13ª Câmara Cível, Rel. Des. Fabio Andre Santos Muniz, j. 20.03.2026; TJPR, AI nº 0064618-25.2026.8.16.0000, 13ª Câmara Cível, Rel. Des. Naor Ribeiro de Macedo Neto, j. 29.05.2026.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Prova que a capitalização em periodicidade inferior a um ano só é permitida se expressamente pactuada, e que a pactuação deve ser expressa e clara (primeira e segunda teses).
- observacao: LIMITE, a constar como ressalva na peça (Súmulas 539 e 541/STJ, que resumem este repetitivo): é lícita a capitalização mensal pactuada em contrato posterior a 31/03/2000 e a previsão de taxa anual superior ao duodécuplo da mensal basta como pactuação. O item 2 da ementa ainda afasta o argumento de que taxa efetiva e nominal, por si, caracterizam capitalização, de modo que a peça deve provar a capitalização concreta (juros incorporados ao saldo). Julgamento por maioria (vencidos o Min. Luis Felipe Salomão, relator originário, e os Mins. Paulo de Tarso Sanseverino e Nancy Andrighi). A proclamação da 2ª tese foi retificada no acórdão. Publicação pela data indicada em acórdãos posteriores (DJe 24/09/2012).

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Prova que, nos contratos bancários sujeitos ao CDC, a capitalização de juros não é automática: exige pactuação expressa e, se o contrato não foi juntado aos autos, é inviável presumir o ajuste do encargo.
- observacao: Julgado da Segunda Seção por maioria (vencidos os Mins. Maria Isabel Gallotti, Ricardo Villas Bôas Cueva, João Otávio de Noronha e Raul Araújo). A hipótese discutida é capitalização anual, em segunda fase de prestação de contas com pretensão revisional, e a ementa trata da capitalização em qualquer periodicidade como dependente de pactuação expressa. O acórdão foi republicado por incorreção na publicação do dia 14/04/2016 (data do texto do Jusbrasil).

ementa:
> AGRAVO REGIMENTAL NO AGRAVO (ART. 544 DO CPC)- AÇÃO DE PRESTAÇÃO DE CONTAS - SEGUNDA FASE - REVISIONAL DE CONTRATO BANCÁRIO NÃO EXIBIDO - TRIBUNAL A QUO QUE AFIRMA SER NECESSÁRIA A EXPRESSA PACTUAÇÃO PARA A COBRANÇA DO ENCARGO CAPITALIZAÇÃO DE JUROS - IRRESIGNAÇÃO DA CASA BANCÁRIA - DECISÃO MONOCRÁTICA QUE NEGOU PROVIMENTO AO RECLAMO - ÓRGÃO COLEGIADO DA QUARTA TURMA AFETANDO O JULGAMENTO DO RECURSO DE AGRAVO REGIMENTAL À SEGUNDA SEÇÃO. Hipótese: Possibilidade de cobrança de capitalização anual de juros independentemente de expressa pactuação entre as partes 1. A despeito de a demanda ter se iniciado como ação de prestação de contas, o feito já está em sua segunda fase procedimental, na qual prepondera verdadeira pretensão revisional do contrato. Não tendo qualquer das partes promovido irresignação sobre esse ponto, inviável é a extinção da demanda, sob pena de violação ao princípio da non reformatio in pejus . 2. A capitalização de juros consiste na incorporação dos juros ao capital ao final de cada período de contagem. 3. O retrospecto histórico do ordenamento jurídico pátrio acerca da regência legal da capitalização de juros denota que desde tempos remotos é proibido contar juros sobre juros, permitida a acumulação de juros vencidos aos saldos líquidos em conta corrente de ano a ano. 4. Com a evolução, passou-se a admitir a cobrança de juros sobre juros em contratos outros, desde que houvesse lei especial regulatória, bem ainda, prévio ajuste do encargo. 5. Tendo em vista que nos contratos bancários é aplicável o Código de Defesa do Consumidor (súmula 297/STJ), a incidência da capitalização anual de juros não é automática, devendo ser expressamente pactuada, visto que, ante o princípio da boa-fé contratual e a hipossuficiência do consumidor, esse não pode ser cobrado por encargo sequer previsto contratualmente. 6. A jurisprudência consolidada nesta Corte Superior é no sentido de que a cobrança de juros capitalizados em periodicidade anual nos contratos de mútuo firmado com instituições financeiras é permitida quando houver expressa pactuação. Precedentes. 7. Na hipótese, não colacionado aos autos o contrato firmado entre as partes, inviável presumir o ajuste do encargo. 8. Agravo regimental desprovido.

### STJ · REsp 2.256.586/RS
- regras: R19, CONTA-CAPDIARIA
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.256.586/RS
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2026-05-04
- publicacao: 2026-05-07
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6795866244
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Prova que o STJ (2026) afasta a capitalização diária que o contrato prevê sem indicar a taxa diária, não bastando a menção às taxas efetivas mensal e anual, e que, afastado o encargo da normalidade, fica descaracterizada a mora; o voto também reafirma que, sem o contrato nos autos, é inviável presumir o ajuste de capitalização.
- observacao: Mérito enfrentado e recurso do consumidor provido (revaloração jurídica, sem reexame de fatos). DIVERGÊNCIA NA PRÓPRIA QUARTA TURMA: oito dias depois, no REsp 2.227.062/RS (Min. Maria Isabel Gallotti, 12/05/2026, entrada ADV abaixo), a mesma Turma validou a capitalização diária sem taxa diária quando as taxas efetivas mensal e anual constam do contrato. O voto aplica o REsp 1.826.463/SC (Segunda Seção, 14/10/2020), citado no próprio acórdão. Sirva a peça para contratos com capitalização diária ou sem pactuação clara. Publicação pela data do Jusbrasil.

ementa:
> RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. RECURSO ESPECIAL PROVIDO. I. CASO EM EXAME 1. Recurso especial interposto contra acórdão proferido em apelação nos autos de ação revisional de contrato bancário. 2. A controvérsia decorre de ação revisional de contrato bancário em que foi reconhecida a validade da capitalização de juros. O Tribunal a quo concluiu que a indicação contratual das taxas mensal e anual, sendo a anual superior ao duodécuplo da mensal, é suficiente para admitir capitalização inferior à anual, inclusive diária, não havendo abusividade e permanecendo hígida a mora. No recurso especial, alegou-se que a capitalização diária exige previsão expressa da periodicidade e indicação da taxa diária, não bastando as taxas mensal e anual. II. QUESTÃO EM DISCUSSÃO 3. A questão em discussão consiste em definir sobre a validade da capitalização diária. III. RAZÕES DE DECIDIR 4. Conforme a orientação do STJ, para que seja admitida a cobrança da capitalização diária, é necessária a previsão expressa de sua periodicidade e da taxa diária, não sendo suficiente a menção às taxas efetivas anual e mensal no contrato. O acórdão recorrido contrariou esse entendimento ao admitir a capitalização diária sem previsão contratual expressa. 5. Evidenciada a abusividade das cláusulas contratuais do período da normalidade, resta descaracterizada a mora do devedor, o que impede a busca e apreensão. IV. DISPOSITIVO E TESE 6. Recurso especial conhecido e provido. Tese de julgamento: "1. A capitalização diária de juros exige previsão expressa da periodicidade e indicação da taxa diária. 2. A abusividade dos encargos no período da normalidade contratual descaracteriza a mora". Dispositivos relevantes citados: CDC, arts. 6º, 46, 52. Jurisprudência relevante citada: STJ, REsp n. 973.827/RS, Relatora para o Acórdão Ministra Maria Isabel Gallotti, Segunda Seção, julgado em 8/8/2012, DJe 24/9/2012; REsp n. 1.826.463/SC, relator Ministro Paulo de Tarso Sanseverino, Segunda Seção, julgado em 14/10/2020; STJ, AgRg no AREsp n. 429.029/PR, relator Ministro Marco Buzzi, Segunda Seção, julgado em 9/3/2016; STJ, REsp n. 1.061.530/RS, relatora Ministra Nancy Andrighi, Segunda Seção, julgado em 22/10/2008.

### STJ · REsp 2.227.062/RS
- regras: R19, CONTA-CAPDIARIA
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.227.062/RS
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2026-05-12
- publicacao: 2026-05-19
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6621879161
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Sem a juntada dos contratos pelo banco, apesar da ordem de exibição, o TJPR afasta a capitalização por falta de pactuação expressa, limita os juros à média de mercado (Súmula 530/STJ) e descaracteriza a mora.
- observacao: Autora pessoa jurídica. A sentença foi anulada em parte (citra petita) e o tribunal julgou o mérito (CPC, art. 1.013, § 3º, III). Repetição simples. Fonte: portal de jurisprudência do TJPR (comarca de Astorga). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CONTRATOS BANCÁRIOS. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA DA AUTORA. CONSTATADA NULIDADE PARCIAL. SENTENÇA CITRA PETITA. PLEITO DE EXIBIÇÃO DE CONTRATOS. PROVA PERICIAL QUE NÃO PODE SER REALIZADA PELA AUSÊNCIA DA JUNTADA DE VÁRIOS CONTRATOS INICIALMENTE REQUERIDOS. ALERTA EFETIVADO QUANTO À INCIDÊNCIA DO ARTIGO 400 DO CPC, NO CASO DE NÃO CUMPRIMENTO DA ORDEM PELO BANCO. MAGISTRADO, ENTRETANTO, QUE NÃO ADMITE COMO VERDADEIROS OS FATOS ALEGADOS, INOBSTANTE A INVERSÃO DO ÔNUS DA PROVA, E ANALISA, TÃO-SOMENTE, A AVENÇA COLACIONADA INICIALMENTE PELA DEMANDANTE. VÍCIO CONSTATADO. JUÍZO QUE VIOLOU OS PRINCÍPIOS DA CONGRUÊNCIA E DA INAFASTABILIDADE DA JURISDIÇÃO (CF, ART. 5º, INCISO XXXV). NULIDADE PARCIAL DA SENTENÇA RECONHECIDA. APLICABILIDADE DO ART. 1.013, §3º, III, DO CPC. EXAME DO MÉRITO DA AÇÃO: 1) JUROS REMUNERATÓRIOS. LIMITAÇÃO À MÉDIA DE MERCADO DIVULGADA PELO BACEN. CONTRATOS FIRMADOS ENTRE AS PARTES NÃO JUNTADOS AOS AUTOS. INCIDÊNCIA DA SÚMULA 530 DO SUPERIOR TRIBUNAL DE JUSTIÇA. 2) CAPITALIZAÇÃO DE JUROS. EXPRESSA PACTUAÇÃO NÃO DEMONSTRADA. ILEGALIDADE. 3) AFASTADAS AS TARIFAS COBRADAS DIANTE DA AUSÊNCIA PACTUAÇÃO EXPRESSA. 4) DESCARACTERIZAÇÃO DA MORA. NECESSIDADE. ABUSIVIDADE NOS ENCARGOS EXIGIDOS NO PERÍODO DA NORMALIDADE CONTRATUAL. 5) REPETIÇÃO DO INDÉBITO NA MODALIDADE SIMPLES, COM CORREÇÃO MONETÁRIA PELA MÉDIA DO INPC/IGP-DI DESDE CADA DESCONTO INDEVIDO ATÉ A CITAÇÃO, MOMENTO EM QUE A CORREÇÃO E OS JUROS DE MORA SERÃO ABARCADOS PELA TAXA SELIC. 6) DANOS MORAIS QUE NÃO SE APERFEIÇOAM NA FORMA IN RE IPSA. 7) PROCEDÊNCIA PARCIAL DOS PEDIDOS AUTORAIS. 8) REDISTRIBUIÇÃO DO ÔNUS DE SUCUMBÊNCIA.RECURSO PROVIDO, para decretar a nulidade parcial da sentença citra petita, e exame, desde logo, do mérito da ação.

### TJPR · Apelação Cível 0012097-79.2022.8.16.0021
- regras: R19, CONTA-CAPDIARIA
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0012097-79.2022.8.16.0021
- orgao: 13ª Câmara Cível
- relator: Des.ª Rosana Andriguetto de Carvalho
- julgamento: 2024-03-15
- publicacao: 2024-03-18
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000026680261/Ac%C3%B3rd%C3%A3o-0012097-79.2022.8.16.0021
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Em cheque especial sem pactuação expressa, o TJPR exclui a capitalização de juros e as tarifas sem previsão contratual.
- observacao: Correntista pessoa jurídica e credora cooperativa de crédito. A alegação do banco de que havia previsão expressa não foi conhecida (inovação recursal); o ponto decidido é a ausência de pactuação expressa. Fonte: portal de jurisprudência do TJPR (comarca de Cascavel). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. CONTRATO DE ABERTURA DE CONTA CORRENTE - CHEQUE ESPECIAL. SENTENÇA DE PROCEDÊNCIA.RECURSO DA INSTITUIÇÃO FINANCEIRA RÉ. ALEGADA PREVISÃO EXPRESSA DE CAPITALIZAÇÃO DE JUROS. NÃO CONHECIMENTO NESTE ASPECTO. INOVAÇÃO RECURSAL. RELATIVIZAÇÃO DO PRINCÍPIO DA PACTA SUNT SERVANDA EM RAZÃO DA FUNÇÃO SOCIAL DO CONTRATO DE ADESÃO E ONEROSIDADE EXCESSIVA. POSSIBILIDADE DE REVISÃO DO CONTRATO EM DISCUSSÃO. ALEGAÇÃO DE INOCORRÊNCIA DE CAPITALIZAÇÃO DE JUROS. NÃO VERIFICAÇÃO. AUSÊNCIA DE PACTUAÇÃO EXPRESSA. IMPOSSIBILIDADE DE COBRANÇA. ENTENDIMENTO CONSOLIDADO DO STJ. EXCLUSÃO DEVIDA. TARIFAS BANCÁRIAS. AUSÊNCIA DE PREVISÃO CONTRATUAL QUANTO À POSSIBILIDADE DE COBRANÇA, AINDA QUE GENÉRICA. CIRCUNSTÂNCIA QUE IMPEDE A COBRANÇA DE QUALQUER VALOR A ESTE TÍTULO, ANTE A AUSÊNCIA DE AUTORIZAÇÃO EXPRESSA DO CLIENTE. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS FIXADOS. RECURSO DA PARTE RÉ PARCIALMENTE CONHECIDO E, NA EXTENSÃO CONHECIDA, NÃO PROVIDO.

## R21 — Juros moratórios — acima de 1% a.m.

Tese: Nos contratos bancários não regidos por legislação específica que fixe outro teto para a mora — inclusive a cédula de crédito bancário, cuja Lei 10.931/2004 apenas autoriza pactuar encargos de mora, sem fixar percentual —, os juros moratórios não podem exceder 1% ao mês (Súmula 379/STJ; REsp 1.061.530/RS, Tema 30/STJ); a cláusula que os fixa acima desse limite é abusiva e deve ser reduzida a 1% ao mês, com restituição do que foi pago a mais.

Nota: os leading cases são o REsp 1.061.530/RS (Segunda Seção, Orientação 3 — juros moratórios até 1% ao mês, Tema 30/STJ), listado sob a R15, e o REsp 1.058.114/RS (Tema 52, item 3.b), listado sob a R01.

### STJ · AgInt no AREsp 2.483.893/PR
- regras: R21
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.483.893/PR
- orgao: Quarta Turma
- relator: Min. Antonio Carlos Ferreira
- julgamento: 2026-09-22
- publicacao: 2026-09-24
- precedente_qualificado: Súmula 379/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7643276456
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Acórdão recente (set/2026), vindo do TJPR, que mantém os juros moratórios limitados a 1% ao mês em cédula de crédito bancário: a Lei 10.931/2004 não é a "legislação específica" da Súmula 379, porque não fixa teto próprio para a mora (diferentemente dos DL 167/1967 e 413/1969), e afastar o limite exige autorização legislativa expressa.
- observacao: Agravo da cooperativa de crédito desprovido; tomadora pessoa jurídica — o limite da Súmula 379 não depende de relação de consumo. Sessão virtual de 15 a 22/09/2026. O fundamento do teto no item 2 (art. 406 do CC com o art. 161, § 1º, do CTN) é o da redação anterior à Lei 14.905/2024; o acórdão não trata da lei nova (ver o relatório). Publicação pela data do Jusbrasil (24/09/2026, data da lista de resultados; o inteiro teor não traz o DJEN; o JSON-LD da página marca 16/10/2026, data de indexação). Ementa com a divisão de linhas do inteiro teor (na página, "I. Razões de decidir" e "II. Dispositivo" vêm emendados aos itens).

ementa:
> DIREITO PROCESSUAL CIVIL. AGRAVO INTERNO NO AGRAVO EM RECURSO ESPECIAL. CONTRATOS BANCÁRIOS. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO OCORRÊNCIA. CÉDULA DE CRÉDITO BANCÁRIO. JUROS MORATÓRIOS. LEI N. 10.931/2004. SÚMULA N. 379/STJ. PRECEDENTES. DECISÃO MANTIDA.
> I. Razões de decidir
> 1. Inexiste afronta ao art. 1.022 do CPC quando o acórdão recorrido pronuncia-se, de forma clara e suficiente, acerca das questões suscitadas nos autos, manifestando-se sobre todos os argumentos que, em tese, poderiam infirmar a conclusão adotada pelo Juízo.
> 2. Na ausência de norma específica de mora na lei de regência contratual, aplica-se o limite legal de 1% ao mês, conforme a regra geral decorrente do art. 406 do CC combinado com o art. 161, § 1º, do CTN e a orientação da Súmula n. 379/STJ.
> 3. Não há violação do art. 927, IV, do CPC, pois o acórdão recorrido observou a ratio decidendi dos precedentes do STJ que exigem autorização legislativa expressa para afastar o limite de 1% ao mês em juros moratórios.
> II. Dispositivo
> 4. Agravo interno desprovido.

### STJ · REsp 2.224.194/BA
- regras: R21, R22
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.224.194/BA
- orgao: Terceira Turma
- relator: Min. Daniela Teixeira
- julgamento: 2026-03-09
- publicacao: 2026-03-12
- precedente_qualificado: Súmula 379/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6629966408
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Mantém, contra recurso do banco, a limitação dos juros de mora a 1% ao mês e da multa contratual a 2% em contrato bancário, "em consonância com o art. 52, § 1º, do CDC, o art. 406 do Código Civil e a Súmula 379 do STJ"; serve às duas regras.
- observacao: Recurso do banco provido só para admitir a capitalização mensal (taxa anual superior ao duodécuplo da mensal). O voto fala em "limitação da multa moratória a 2% em contratos de consumo". Sessão virtual de 03 a 09/03/2026. Publicação pela data do Jusbrasil (12/03/2026, data da lista de resultados; o inteiro teor não traz o DJEN; o JSON-LD marca 10/07/2026, data de indexação). Ementa do inteiro teor; juntada a palavra "encontra-se", que o PDF partiu entre linhas no item 3.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. JUROS REMUNERATÓRIOS. LIMITAÇÃO À TAXA MÉDIA DE MERCADO. SÚMULAS 5, 7 E 83 DO STJ. CAPITALIZAÇÃO MENSAL DE JUROS. POSSIBILIDADE. TAXA ANUAL SUPERIOR AO DUODÉCUPLO DA TAXA MENSAL. ENCARGOS MORATÓRIOS. LIMITAÇÃO A 1% AO MÊS E MULTA DE 2%. RECURSO ESPECIAL PARCIALMENTE CONHECIDO E, NESTA EXTENSÃO, PARCIALMENTE PROVIDO.
> I. Caso em exame
> 1. Recurso especial interposto, com fundamento no art. 105, inciso III, alíneas a e c, da Constituição Federal, contra acórdão que reconheceu a abusividade dos juros remuneratórios pactuados em contrato bancário, determinando sua limitação à taxa média de mercado divulgada pelo Banco Central, afastou a capitalização mensal de juros e limitou os encargos moratórios a juros de mora de 1% ao mês e multa contratual de 2%.
> II. Questão em discussão
> 2. Discute-se a possibilidade de revisão da taxa de juros remuneratórios acima da média de mercado, a validade da capitalização mensal de juros e a legalidade da limitação dos encargos moratórios.
> III. Razões de decidir
> 3. A conclusão do Tribunal de origem quanto à abusividade dos juros remuneratórios decorreu da análise fático-probatória do caso e da interpretação das cláusulas contratuais, sendo incabível sua revisão em recurso especial, nos termos das Súmulas 5 e 7 do STJ. O acórdão recorrido, ademais, encontra-se alinhado à jurisprudência consolidada desta Corte, incidindo a Súmula 83 do STJ.
> 4. No tocante à capitalização mensal, a taxa anual contratada (33,96%) supera o duodécuplo da taxa mensal (2,47%), circunstância que evidencia a pactuação expressa, de modo que se admite a cobrança em periodicidade inferior à anual, conforme entendimento consolidado nas Súmulas 539 e 541 do STJ.
> 5. Quanto aos encargos moratórios, correta a decisão do Tribunal de origem ao limitar os juros de mora a 1% ao mês e a multa contratual a 2%, em consonância com o art. 52, § 1º, do CDC, o art. 406 do Código Civil e a Súmula 379 do STJ.
> IV. Dispositivo
> 6. Recurso especial parcialmente conhecido e, nessa extensão, parcialmente provido, apenas para reconhecer a validade da capitalização mensal de juros.

### TJPR · Apelação Cível 0015525-89.2025.8.16.0045
- regras: R21
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0015525-89.2025.8.16.0045
- orgao: 4ª Câmara Cível
- relator: Des.ª Astrid Maranhão de Carvalho Ruthes
- julgamento: 2026-10-07
- publicacao: 2026-10-07
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000039200141/Ac%C3%B3rd%C3%A3o-0015525-89.2025.8.16.0045
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em financiamento de veículo por cédula de crédito bancário, declara abusivos juros moratórios de 6% ao mês e os limita a 1% ao mês (Súmula 379/STJ), porque a Lei 10.931/2004 não estabelece limite específico para a mora; mantida a restituição do excesso.
- observacao: Apelo do banco conhecido em parte e desprovido. O banco invocou também a Lei 14.905/2024 para defender a taxa convencionada; o acórdão manteve o limite sem examinar esse argumento (contrato de 27/03/2022, anterior à lei). Correções na ementa: retirado o rótulo inicial "Ementa:" e juntadas as quebras de linha que o portal inseriu no meio das frases, sem alterar o texto. Fonte: portal de jurisprudência do TJPR (comarca de Arapongas).

ementa:
> DIREITO CIVIL E DIREITO DO CONSUMIDOR. AÇÃO REVISIONAL CUMULADA COM REPETIÇÃO DE INDÉBITO. ABUSIVIDADE DE JUROS MORATÓRIOS. APLICAÇÃO DA SÚMULA 379 DO STJ. COMPENSAÇÃO DE VALORES E APLICAÇÃO DA TAXA SELIC. AUSÊNCIA DE INTERESSE RECURSAL. TÓPICOS JÁ CONSTAM NA SENTENÇA. RECURSO DE APELAÇÃO PARCIALMENTE CONHECIDO E, NA PARTE CONHECIDA, NÃO PROVIDO.
> I. Caso em exame
> 1. Apelação cível interposta por instituição financeira em face da sentença que julga parcialmente procedentes os pedidos em ação revisional cumulada com repetição de indébito, em que o consumidor questiona a abusividade da taxa de juros moratórios de 6% ao mês pactuada em contrato de financiamento de veículo, requerendo a limitação dos juros à taxa média de mercado, a restituição dos valores pagos a maior e a aplicação da justiça gratuita, além da condenação do banco nas verbas de sucumbência.
> II. Questão em discussão
> 2. As questões em discussão consistem na averiguação caso os juros moratórios pactuados em contrato de financiamento por meio de cédula de crédito bancário podem ser limitados a 1% ao mês, conforme a Súmula 379 do STJ, e se a instituição financeira deve restituir os valores pagos a maior decorrentes da abusividade da taxa de 6% ao mês.
> III. Razões de decidir
> 3. A Lei nº 10.931/2004 não estabelece limite específico para os juros moratórios nas cédulas de crédito bancário, mantendo-se aplicável a Súmula 379 do STJ, que limita tais juros a 1% ao mês.
> 4. A cláusula contratual que estipula juros moratórios de 6% ao mês é abusiva por exceder significativamente o limite de 1% ao mês previsto na jurisprudência consolidada.
> 5. A compensação de valores entre as partes já foi acolhida na sentença, não existindo interesse recursal sobre esse ponto.
> 6. A aplicação da Taxa Selic como índice único para atualização monetária e juros moratórios foi determinada na sentença, vedando-se a cumulação com outros índices, não existindo interesse recursal quanto a isso.
> IV. Dispositivo e tese
> 7. Recurso de apelação cível parcialmente conhecido e, na parte conhecida, negado provimento.
> Tese de julgamento: Nos contratos regidos por cédula de crédito bancário, os juros moratórios devem ser limitados a 1% ao mês conforme a Súmula 379 do STJ, sendo cabível a aplicação exclusiva da Taxa Selic para atualização monetária e juros moratórios, vedada a cumulação com outros índices, e a abusividade dos juros remuneratórios somente se reconhece quando ultrapassam substancialmente o dobro da taxa média de mercado para financiamentos de veículos antigos.
> Dispositivos relevantes citados: CPC, arts. 85, § 2º, 85, § 11º, e 86, parágrafo único; CC, art. 368; Lei nº 10.931/2004, art. 28, § 1º, incs. I e III; Lei nº 14.905/2024, art. 1º.

### TJPR · Apelação Cível 0001265-53.2022.8.16.0096
- regras: R21, R22, R31
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001265-53.2022.8.16.0096
- orgao: 16ª Câmara Cível
- relator: Juíza Subst. 2º Grau Vania Maria da Silva Kramer
- julgamento: 2025-09-22
- publicacao: 2025-09-26
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000033743411/Ac%C3%B3rd%C3%A3o-0001265-53.2022.8.16.0096
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Confirma, contra apelo da cooperativa de crédito, que a cédula de crédito bancário segue a Súmula 379/STJ (juros de mora até 1% ao mês, porque a Lei 10.931/2004 não tem regime próprio para a mora) e que a multa de 2% incide sobre o valor da prestação, não sobre o saldo devedor total (CDC, art. 52, § 1º).
- observacao: Ação monitória com embargos; a aplicação do CDC estava preclusa. A cooperativa obteve só a redistribuição da sucumbência. Nos juros, o cálculo da cooperativa já usava 1%, de modo que o acórdão afirmou o limite sem alterar a conta; na multa, a cláusula fazia os 2% incidirem sobre o débito total e o acórdão manteve a incidência sobre a prestação. Na multa, o voto reproduz precedente da 13ª Câmara Cível no mesmo sentido; a íntegra do portal cita o próprio CNJ. Correções na ementa: retirado o rótulo inicial "Ementa:" e separados os títulos e itens que a extração emendou, sem alterar o texto. Fonte: portal de jurisprudência do TJPR (comarca de Iretama).

ementa:
> Direito civil e processual civil. Apelações cíveis. Cédula de Crédito bancário. Limitação dos juros moratórios. Multa moratória sobre o valor da prestação. Cerceamento de defesa. Ônus de sucumbência. Recurso da Cooperativa parcialmente provido. Recurso da ré/Embargante desprovido.
> I. Caso em exame
> 1. Apelações interpostas por ambas as partes contra sentença que julgou parcialmente procedente o pedido inicial para constituir de pleno direito o crédito postulado pela instituição financeira, com limitação da multa moratória a 2% e dos juros moratórios a 1% ao mês, fixando a sucumbência recíproca em 70% para a parte ré (embargante) e 30% para a autora (instituição financeira). A instituição financeira recorreu defendendo a legalidade dos encargos moratórios aplicados e a redistribuição da sucumbência. A parte requerida, por sua vez, alegou cerceamento de defesa pela ausência de decisão de saneamento e indeferimento de perícia contábil, requerendo a nulidade da sentença.
> II. Questão em discussão
> 2. Há quatro questões em discussão: (i) determinar se houve cerceamento de defesa em virtude da não realização de prova pericial contábil; (ii) definir se a limitação dos juros moratórios a 1% ao mês é aplicável à cédula de crédito bancário; (iii) estabelecer a legalidade da cobrança da multa moratória sobre o valor total do débito; e (iv) decidir sobre a correta distribuição dos ônus de sucumbência.
> III. Razões de decidir
> 3. O indeferimento da prova pericial contábil não configura cerceamento de defesa, pois as questões controvertidas podiam ser resolvidas com base nos documentos apresentados pelas partes, sendo legítima a opção do julgador pelo julgamento antecipado da lide (CPC, art. 370 e art. 139, II).
> 4. A ausência de decisão de saneamento processual não enseja nulidade se não houver demonstração de prejuízo à parte, inexistente no caso concreto.
> 5. A cédula de crédito bancário é regida pela Lei nº 10.931/2004, que, entretanto, não prevê regime jurídico próprio para os juros moratórios. Assim, aplica-se a regra geral fixada na Súmula 379 do STJ, que limita os juros moratórios a 1% ao mês, não havendo ilegalidade na limitação imposta na sentença.
> 6. A cobrança de multa moratória de 2% sobre o valor total do saldo devedor não encontra respaldo; ela deve incidir sobre o valor da prestação, nos termos do art. 52, §1º, do CDC.
> 7. Verificada a sucumbência mínima da cooperativa, impõe-se a aplicação do art. 86, parágrafo único, do CPC, para que a parte adversa suporte integralmente as custas processuais e os honorários advocatícios. Em razão do desprovimento do recurso da parte embargante, procede-se à majoração dos honorários advocatícios em 2%, totalizando 12% sobre o valor atualizado da causa.
> IV. Dispositivo
> 8. Sentença reformada em parte. Recurso da Cooperativa parcialmente provido, para condenar a autora ao adimplemento da integralidade dos ônus sucumbenciais. Recurso da ré-embargante desprovido.
> _________
> Dispositivos relevantes citados: CPC, arts. 86, parágrafo único; 139, II; 370; CDC, art. 52, §1º.
> Jurisprudência relevante citada: STJ, Súmula 379.

## R22 — Multa contratual — acima de 2% em relação de consumo

Tese: Em contrato bancário de consumo, a multa de mora não pode exceder 2% do valor da prestação (CDC, art. 52, § 1º, na redação da Lei 9.298/1996; Súmula 285/STJ); a cláusula que prevê percentual maior, ou que faz a multa incidir sobre o saldo devedor total, deve ser reduzida a esse limite, com restituição do que foi pago a mais.

Nota: o leading case é o REsp 1.058.114/RS (Segunda Seção, Tema 52, item 3.c — "multa contratual limitada a 2% do valor da prestação, nos termos do art. 52, § 1º, do CDC"), listado sob a R01. Os favoráveis que servem também à R21 (REsp 2.224.194/BA e um acórdão da 16ª Câmara Cível do TJPR) estão sob a R21.

### STJ · REsp 1.497.574/SC
- regras: R22
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.497.574/SC
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2023-10-24
- publicacao: 2023-11-03
- precedente_qualificado: Súmula 285/STJ
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2108125058
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva com dois limites: a redução da multa para 2% só vale para contratos celebrados a partir da Lei 9.298/1996 (01/08/1996) — antes, o teto do CDC era 10% —, e a revisão pelo CDC alcança apenas a relação de consumo, não o empréstimo tomado por empresa para implementar ou incrementar a atividade (relação de insumo).
- observacao: Ação civil pública do MP/SC contra banco; recurso do banco parcialmente provido justamente para limitar a redução da multa aos contratos posteriores à Lei 9.298/1996 e a revisão aos contratos de consumo. Atenção: o item 3 da ementa põe entre aspas, como se fosse a Súmula 285/STJ, a frase do AgRg no AgRg no REsp 513.847/RS; o enunciado da Súmula 285, transcrito no voto, é "Nos contratos bancários posteriores ao Código de Defesa do Consumidor incide a multa moratória nele prevista" — citar a súmula pelo enunciado. O corte temporal da regra no motor ("contratos posteriores ao CDC, 11/03/1991") não coincide com o do STJ (Lei 9.298/1996). Publicação pela data do Jusbrasil (03/11/2023, data da lista de resultados; o JSON-LD marca 20/12/2023, data de indexação). Ementa copiada da seção Ementa da página, igual à do inteiro teor.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. RECURSO ESPECIAL. CONTRATOS BANCÁRIOS. CLÁUSULAS ABUSIVAS. AÇÃO CIVIL PÚBLICA. INCIDÊNCIA DO CDC. LIMITAÇÃO. RELAÇÃO DE CONSUMO. CAPITALIZAÇÃO MENSAL DE JUROS. PACTUAÇÃO EXPRESSA. REDUÇÃO DA MULTA MORATÓRIA. CONTRATOS CELEBRADOS A PARTIR DA LEI 9.298/96. TAXA SELIC. CUMULAÇÃO COM CORREÇÃO MONETÁRIA. IMPOSSIBILIDADE. MULTA DIÁRIA. INTIMAÇÃO PESSOAL. IMPRESCINDIBILIDADE. RECURSO ESPECIAL PARCIALMENTE PROVIDO.
> 1. Nos termos da jurisprudência do STJ, em regra, com base na Teoria Finalista, não se aplica o CDC aos contratos de empréstimo tomados por sociedade empresária para implementar ou incrementar suas atividades negociais, uma vez que a contratante não é considerada destinatária final do serviço e não pode ser considerada consumidora, limitando-se a revisão automática das cláusulas contratuais aos casos em que constatada a existência de relação de consumo, afastada a revisão em contratos relativos a relações de insumo.
> 2. "É permitida a capitalização de juros com periodicidade inferior à anual em contratos celebrados com instituições integrantes do Sistema Financeiro Nacional a partir de 31/3/2000 (MP 1.963-17/00, reeditada como MP 2.170-36/01), desde que expressamente pactuada".
> 3. Nos termos da Súmula 285/STJ, "A redução da multa para 2%, tal como definida na Lei nº 9.298, de 01.08.1996, somente é possível nos contratos celebrados após sua vigência".
> 4. Conforme entendimento pacificado no STJ, é vedada a incidência cumulativa da taxa SELIC com outro índice de atualização monetária, devendo ser afastada a correção monetária pelo índice do INPC no que tange aos valores a serem devolvidos pela instituição bancária.
> 5. "É necessária a prévia intimação pessoal do devedor para a cobrança de multa pelo descumprimento de obrigação de fazer ou não fazer antes e após a edição das Leis n. 11.232/2005 e 11.382/2006, nos termos da Súmula 410 do STJ, cujo teor permanece hígido também após a entrada em vigor do novo Código de Processo Civil" (EREsp 1.360.577/MG, Relator para o acórdão Ministro LUIS FELIPE SALOMÃO, CORTE ESPECIAL, julgado em 19/12/2018, DJe de 07/03/2019).
> 6. Recurso especial a que se dá parcial provimento.

## R23 — Rotativo e parcelamento da fatura — teto de 100% de juros e encargos (Lei 14.690/2023, art. 28; Res. CMN 5.112/2023)

Tese: Nas operações de crédito rotativo e de parcelamento de fatura de cartão de crédito realizadas a partir de 03/01/2024, o total cobrado a título de juros e encargos financeiros não pode exceder o valor original da dívida (excluído o IOF), devendo o saldo ser recalculado e o excesso restituído ou abatido.

### TJPR · Recurso Inominado Cível 0009187-95.2025.8.16.0014
- regras: R23
- posicao: FAV
- tribunal: TJPR
- classe_numero: Recurso Inominado Cível 0009187-95.2025.8.16.0014
- orgao: 5ª Turma Recursal dos Juizados Especiais
- relator: Juíza Fernanda de Quadros Jorgensen Geronasso
- julgamento: 2026-02-18
- publicacao: 2026-02-19
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000035954731/Ac%C3%B3rd%C3%A3o-0009187-95.2025.8.16.0014
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Turma Recursal do TJPR reconhece a regularidade do parcelamento automático, mas determina que os encargos sejam recalculados sobre o valor original da dívida, observado o limite do art. 28, § 1º, da Lei 14.690/2023, em vez de se limitar a taxa fixa.
- observacao: Julgado de Turma Recursal (Juizados), não de Câmara Cível. Dados conferidos no portal do TJPR em 29/10/2026: ementa idêntica, julgamento em 18/02/2026 (o Jusbrasil indicava 13/02) e publicação em 19/02/2026. ATENÇÃO: o voto e o dispositivo aplicam o limite de 100% do valor original (R$ 771,38), mas o item 14 da ementa ("tese de julgamento") escreve que o limite "restringe o total cobrado ao dobro do valor original da dívida"; citar na peça com base no art. 28, § 1º, e no voto, não nessa frase da tese. O mesmo julgado ressalva que o parcelamento automático (Res. BACEN 4.549/2017) é regular, o que o banco usará em contraponto. A ementa transcreve ementas de outros dois julgados (TJPR e TJMT), com números de processo.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Apelação provida em parte para declarar inexigíveis os encargos que excedam o art. 28, § 1º, da Lei 14.690/2023 e determinar o recálculo do débito (rotativo e parcelamento automático) de modo que juros e encargos não passem de 100% da dívida consolidada em 21/12/2023, com amparo na Res. CMN 5.112/2023.
- observacao: Complemento ao TJPR: lá, o favorável de Turma Recursal foi conferido no portal do TJPR em 29/10/2026, o de Câmara Cível é só uma tutela de urgência (15ª Câmara, 2026), e as Câmaras Cíveis consultadas em 28 e 29/10/2026 rejeitaram o teto nos casos concretos (operação anterior a 03/01/2024, teto apurado por operação, estouro não demonstrado). Publicação pela data do Jusbrasil. O acórdão preserva os encargos contratuais até 21/12/2023 e aplica o teto a partir daí (recálculo em cumprimento de sentença); mantém a regularidade do parcelamento automático, a negativação (mora confessada desde 07/2023) e afasta o dano moral, ressalvas a antecipar na peça. Ementa em texto corrido, sem divisão em itens, como no original.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Ressalva a antecipar: a Terceira Turma do STJ já registrou, em ementa, que a Lei 14.690/2023 não cria teto imediato e universal para o cartão e não alcança contratos anteriores à sua entrada em vigor; a peça deve invocar apenas operações posteriores a 03/01/2024 (Res. CMN 5.112, art. 2º-D).
- observacao: Posição ADV de alcance limitado: acórdão de agravo em REsp (ação monitória, contrato anterior à lei) que mantém a conclusão do TJMT; o voto reproduz o fundamento do tribunal de origem ("a norma não estabelece um teto generalizado... mecanismo de autorregulação") sem examinar a Res. CMN 5.112/2023, que o CMN editou em 21/12/2023, nem o seu art. 2º-D. Não é precedente qualificado. Publicação pela data do Jusbrasil. Não tratar como superação do teto; usar apenas como alerta do limite temporal e do ônus de demonstrar que a operação é posterior a 03/01/2024. Em 29/10/2026 o Jusbrasil lista, no mesmo número, decisão posterior em RE no AREsp (21/08/2026), cujo desfecho não foi conferido.

ementa:
> CIVIL. PROCESSUAL CIVIL. AGRAVO EM RECURSO ESPECIAL. AÇÃO MONITÓRIA. CONTRATOS BANCÁRIOS. CARTÃO DE CRÉDITO E CRÉDITO PESSOAL. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. NÃO OCORRÊNCIA. GRATUIDADE DA JUSTIÇA. AUSÊNCIA DE INTERESSE RECURSAL. VENCIMENTO ANTECIPADO DA DÍVIDA. PREVISÃO CONTRATUAL. REEXAME FÁTICO. SÚMULAS 5 E 7/STJ. JUROS REMUNERATÓRIOS. ABUSIVIDADE. ÔNUS DA PROVA. SÚMULA 596/STF. TEMA 27/STJ. LEI N. 14.690/2023. INAPLICABILIDADE AUTOMÁTICA. HONORÁRIOS RECURSAIS. MAJORAÇÃO. 1. Não configura negativa de prestação jurisdicional o acórdão que aprecia, de forma fundamentada, as questões controvertidas, ainda que de modo contrário aos interesses da parte recorrente. 2. Ausente o interesse recursal quando o benefício da gratuidade da justiça já foi concedido na instância de origem para fins de processamento do apelo. 3. Mantida a conclusão do Tribunal de origem sobre a validade do vencimento antecipado das parcelas vincendas diante do inadimplemento, por haver previsão contratual expressa e por demandar sua revisão o reexame de fatos e cláusulas contratuais - óbice das Súmulas n. 5 e 7/STJ. 4. As instituições financeiras não se sujeitam ao limite de juros da Lei de Usura, e a revisão das taxas remuneratórias exige demonstração cabal de abusividade em cotejo com a taxa média de mercado, nos termos da Súmula n. 596/STF e do Tema n. 27/STJ. 5. A Lei n. 14.690/2023 não institui teto imediato e universal de encargos para cartão de crédito, dependendo de implementação de mecanismos de autorregulação pelos emissores e de aprovação pelo Banco Central, sem aplicação retroativa sobre contratos anteriores já vigentes quando de sua entrada em vigor. 6. Agravo conhecido para negar provimento ao recurso especial.

### TJPR · Agravo de Instrumento 0114167-38.2025.8.16.0000
- regras: R23
- posicao: FAV
- tribunal: TJPR
- classe_numero: Agravo de Instrumento 0114167-38.2025.8.16.0000
- orgao: 15ª Câmara Cível
- relator: Juiz Subst. 2º Grau Davi Pinto de Almeida
- julgamento: 2026-03-14
- publicacao: 2026-03-16
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035384431/Ac%C3%B3rd%C3%A3o-0114167-38.2025.8.16.0000
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Em agravo de instrumento, a 15ª Câmara Cível suspende as cobranças de um aditamento para parcelamento da fatura de cartão firmado depois de 01/01/2024, porque o total exigido supera mais de três vezes o valor original da dívida, acima do limite do art. 28, § 1º, da Lei 14.690/2023 e da Res. CMN 5.112/2023.
- observacao: Decisão em tutela de urgência (cognição sumária), não julgamento de mérito; a própria Câmara ressalva que a liminar será revogada se a ação for julgada improcedente. Pela íntegra, o valor parcelado era de R$ 22.183,90, com total a pagar de R$ 70.489,44 em 48 parcelas; a Câmara reconheceu a probabilidade do direito porque a operação foi contratada após o início da vigência do limite, e o perigo da demora pelo peso das parcelas na renda do autor. Único favorável de Câmara Cível do TJPR localizado em 29/10/2026. Em sentido contrário, no mesmo tribunal: a 16ª Câmara apura o teto por operação, não sobre o saldo global; a 15ª e a 14ª afastam o limite para débito originado antes de 2024; e a 14ª Câmara, em embargos monitórios, exige que o devedor apresente o valor que entende devido e a memória de cálculo (CPC, art. 702, §§ 2º e 3º), sob pena de não conhecer o excesso. A íntegra não repete o número do agravo (cita o da ação de origem); o vínculo com o registro se confirma pelo conteúdo (aditamento para parcelamento de fatura, Lei 14.690/2023, tutela deferida). Correções na ementa: juntadas 3 quebras de linha que o portal inseriu no meio do texto.

ementa:
> AGRAVO DE INSTRUMENTO. AÇÃO REVISIONAL DE CONTRATO DE ADITAMENTO PARA PARCELAMENTO. ANTECIPAÇÃO DE TUTELA INDEFERIDA NA ORIGEM. INSURGÊNCIA DA PARTE AUTORA. PLEITO DE SUSPENSÃO DA COBRANÇA DAS PARCELAS DO MÚTUO CONTRATADO. POSSIBILIDADE. REQUISITOS LEGAIS PREVISTOS NO ART. 300 DO CPC PREENCHIDOS. JUROS E ENCARGOS FINANCEIROS COBRADOS EM PARCELAMENTO DE SALDO DEVEDOR DE FATURA DE CARTÃO DE CRÉDITO. LIMITAÇÃO ESTABELECIDA PELA LEI N° 14.690/2023 E REGULAMENTADA PELA RESOLUÇÃO CMN N° 5.112/2023. DECISÃO AGRAVADA REFORMADA. RECURSO CONHECIDO E PROVIDO.

## R24 — Cartão de crédito consignado com RMC/RCC em benefício previdenciário — nulidade/conversão em empréstimo consignado por falta de informação

Tese: A contratação de cartão de crédito consignado com reserva de margem consignável por consumidor que pretendia empréstimo consignado comum, sem informação clara sobre a natureza do produto e sobre a amortização, caracteriza falha no dever de informação e vício de consentimento, devendo o contrato ser anulado ou convertido em empréstimo consignado (juros pela taxa média do BACEN), com restituição do que foi pago a maior e indenização por danos morais.

### STJ · AREsp 3.118.740/MG
- regras: R24
- posicao: ADV
- tribunal: STJ
- classe_numero: AREsp 3.118.740/MG
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2026-09-29
- publicacao: 2026-10-02
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7547184856
- verificado_em: 2026-11-02
- status: VERIFICADO
- uso_na_peca: Ressalva de prazo: a Quarta Turma tem como orientação do STJ (Súmula 83) que a pretensão de anular o cartão consignado por vício de consentimento (erro) decai em 4 anos (CC, art. 178, II), contados da celebração do contrato, sem renovação a cada desconto; a peça deve ajuizar dentro do prazo ou estruturar o pedido para além da anulação (nulidade declaratória, abusividade, art. 51 do CDC, prescrição decenal).
- observacao: Candidato ADV, não FAV. Decide por Súmula 83 e Súmulas 5/7, mas a tese de julgamento (item 1) afirma a decadência quadrienal com termo na celebração do contrato. Cita no mesmo sentido AREsp 3.006.231/MG (3ª T., j. 01/12/2025) e AREsp 2.803.298/BA (3ª T., j. 20/10/2025). Contraponto na Terceira Turma: AREsp 3.104.258/MT. Publicação pela data do Jusbrasil. Na ementa, a lista de artigos do CDC do item 5 veio embaralhada no Jusbrasil e foi refeita pela lista de dispositivos citados no próprio acórdão (arts. 4º, I e III, 6º, III, 14, 39, IV, 46, 51, IV e 54, §§ 3º e 4º). Alerta: o Tema 1.414/STJ (Segunda Seção, afetado em 06/03/2026, com suspensão nacional) trata da validade do cartão consignado, da consequência da invalidação (conversão ou restituição) e do dano moral; sem tese fixada até onde se conferiu (último andamento visto: 03/07/2026), confirmar no ScON antes de usar a R24 em peça.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. AGRAVO EM RECURSO ESPECIAL. CONTRATO DE CARTÃO DE CRÉDITO CONSIGNADO. VÍCIO DE CONSENTIMENTO. DECADÊNCIA DO ART. 178, II, DO CC. TERMO INICIAL NA CELEBRAÇÃO DO CONTRATO. AGRAVO EM RECURSO ESPECIAL DESPROVIDO.
> I. CASO EM EXAME
> 1. Agravo em recurso especial interposto contra decisão de inadmissibilidade do recurso especial, por incidência da Súmula n. 7 do STJ, consonância do acórdão recorrido com a orientação do Superior Tribunal de Justiça (Súmula n. 83 do STJ) e prejudicialidade do dissídio pela alínea c , mantendo-se o não processamento do especial contra acórdão do Tribunal de Justiça de Minas Gerais.
> 2. A controvérsia envolve ação de obrigação de fazer c/c restituição em dobro c/c danos morais, com pedido de conversão de contrato de cartão de crédito consignado em empréstimo consignado, sob alegação de erro substancial.
> 3. O Juízo de primeiro grau reconheceu, de ofício, a decadência do art. 178, II, do Código Civil, extinguiu o mérito e fixou honorários com exigibilidade suspensa.
> 4. A Corte de origem manteve a improcedência, por consumação da decadência desde a celebração do contrato, convalidando a avença e julgando prejudicários os pedidos de conversão e indenizatórios.
> II. QUESTÃO EM DISCUSSÃO
> 5. Há seis questões em discussão: (i) saber se incide a decadência do art. 178, II, do Código Civil em pretensão fundada em vício de consentimento por erro substancial; (ii) saber se a natureza de trato sucessivo desloca o termo inicial para o último desconto, com aplicação dos arts. 26 e 27 do Código de Defesa do Consumidor; (iii) saber se a conversão do contrato prescinde de anulação prévia; (iv) saber se houve falha do dever de informação, prática abusiva e responsabilidade objetiva à luz dos arts. 4º, I e III, 6º, III, 14, 39, IV, 46, 51, IV e 54, §§ 3º e 4º, do Código de Defesa do Consumidor; (v) saber se há responsabilidade civil por danos materiais e morais (arts. 186 e 927 do Código Civil e art. 5º, V e X, da Constituição Federal); e (vi) saber se há divergência jurisprudencial pela alínea c do art. 105, III, da Constituição Federal.
> III. RAZÕES DE DECIDIR
> 6. Incide a Súmula n. 83 do STJ porque o acórdão recorrido está em conformidade com a jurisprudência desta Corte quanto à decadência quadrienal do art. 178, II, do Código Civil, com termo inicial na celebração do contrato, relativamente ao ponto jurídico do vício de consentimento por erro.
> 7. Incidem as Súmulas n. 5 e 7 do STJ porque a revisão da qualificação do vício, a interpretação de cláusulas e o revolvimento do conteúdo fático-probatório seriam necessários para afastar a conclusão de erro substancial e a convalidação do contrato, relativamente aos pedidos de conversão e indenização.
> 8. Do exame de suposta violação dos arts. 5º, V e X, da Constituição Federal não se pode conhecer, por incompetência desta Corte para análise de matéria constitucional.
> 9. Do dissídio jurisprudencial não se pode conhecer, por prejudicialidade decorrente do não processamento pela alínea a e da incidência da Súmula n. 83 do STJ sobre o tema da decadência.
> IV. DISPOSITIVO E TESE
> 10. Agravo em recurso especial desprovido. Tese de julgamento: "1. Incide a Súmula n. 83 do STJ quando o acórdão recorrido aplica o art. 178, II, do Código Civil para reconhecer a decadência quadrienal, com termo inicial na celebração do contrato, em pretensão de anulação por vício de consentimento.
> 2. Incidem as Súmulas n. 5 e 7 do STJ quando o acolhimento do recurso demandaria interpretação de cláusulas contratuais e reexame do acervo fático-probatório sobre a existência de erro substancial e seus efeitos. 3. Não se conhece de alegação fundada nos arts. 5º, V e X, da Constituição Federal em sede de recurso especial, por usurpação da competência do Supremo Tribunal Federal.
> 4. Do dissídio jurisprudencial não se pode conhecer quando a matéria está obstada pela solução pela alínea a e pela incidência da Súmula n. 83 do STJ.". Dispositivos relevantes citados: CC, arts. 178, II, 186 e 927; CDC, arts. 4º, I e III, 6º, III, 14, 26, 27, 39, IV, 46, 51, IV e 54, §§ 3º e 4º; CPC, art. 85, § 11; CF, arts. 5º, V e X, e 105, III, a e c. Jurisprudência relevante citada: STJ, Súmulas n. 5, 7 e 83; STJ, AgInt nos EDcl no AREsp n. 2.380.393/SP, relator Ministro Raul Araújo, Quarta Turma, julgados em 8/4/2024; STJ, AREsp n. 3.006.231/MG, relatora Ministra Daniela Teixeira, Terceira Turma, julgado em 1/12/2025; STJ, REsp n. 1.630.108/MG, relatora Ministra Nancy Andrighi, Terceira Turma, julgado em 27/2/2018; STJ, AREsp n. 2.803.298/BA, relatora Ministra Daniela Teixeira, Terceira Turma, julgado em 20/10/2025.

### TJRS · Apelação Cível 5004183-61.2022.8.21.0077
- regras: R24
- posicao: FAV
- tribunal: TJRS
- classe_numero: Apelação Cível 5004183-61.2022.8.21.0077
- orgao: 17ª Câmara Cível
- relator: Des. Vanise Röhrig Monte Aço
- julgamento: 2025-12-18
- publicacao: 2025-12-18
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-rs/5980568334
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Reconhece falha no dever de informação na contratação de cartão RMC por quem queria empréstimo consignado e determina a conversão em empréstimo pessoal consignado (valor sacado como capital, taxa média BACEN do consignado INSS na data da contratação, descontos imputados na amortização, restituição simples do excedente).
- observacao: Complementa os acórdãos do TJPR desta tese, que lá é majoritariamente contrária. Publicação pela data do Jusbrasil (sessão virtual de 17 a 18/12/2025). O acórdão NEGA dano moral e a repetição em dobro (restituição simples); o voto invoca, por precedente citado, o IRDR nº 28 do TJRS. Tema 1414/STJ (conversão como consequência da invalidação) segue pendente; a peça deve apresentar a conversão como pedido principal ou alternativo, ciente do risco de sobrestamento.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Reforma sentença de improcedência para declarar o vício de consentimento por falha no dever de informação (cartão não entregue, valor creditado por TED, contrato sem número de parcelas), converter o RMC em empréstimo consignado convencional pela taxa média BACEN da época e restituir de forma simples o pago a maior.
- observacao: Complementa os acórdãos do TJPR desta tese, que lá é majoritariamente contrária. Publicação pela data do Jusbrasil (julgamento em sessão de 19/11/2025). O texto do Jusbrasil junta palavras (ex.: "tratar-sede", "interessena"); aqui, separadas. O acórdão não trata de dano moral na tese (pedido não acolhido) e determina restituição simples, não em dobro. Mesma ressalva do Tema 1414/STJ.

ementa:
> EMENTA DIREITO DO CONSUMIDOR E BANCÁRIO. APELAÇÃO CÍVEL. CARTÃO DE CRÉDITO CONSIGNADO COM RESERVA DE MARGEM CONSIGNÁVEL (RMC). VÍCIO DE CONSENTIMENTO. FALHA NO DEVER DE INFORMAÇÃO. CONVERSÃO DO CONTRATO PARA EMPRÉSTIMO CONSIGNADO CONVENCIONAL. RESTITUIÇÃO SIMPLES DOS VALORES PAGOS A MAIOR. RECURSO PROVIDO. I. CASO EM EXAME 1. Recurso de apelação interposto contra sentença que julgou improcedentes os pedidos formulados na ação revisional de contrato cumulada com repetição do indébito e indenização por danos morais. A apelante sustenta ter sido induzida a erro ao celebrar contrato de cartão de crédito consignado com reserva de margem consignável (RMC), acreditando tratar-se de empréstimo consignado convencional, e pleiteia a revisão contratual, a restituição de valores pagos a maior e o reconhecimento do vício de consentimento. II. QUESTÃO EM DISCUSSÃO 1. Há duas questões centrais em discussão: (i) definir se houve vício de consentimento decorrente de falha no dever de informação na contratação do cartão de crédito consignado com RMC; (ii) determinar se é cabível a conversão da modalidade contratual para empréstimo consignado convencional, com restituição dos valores pagos indevidamente e limitação da taxa de juros à média de mercado. III. RAZÕES DE DECIDIR 1. O princípio da dialeticidade recursal não é violado quando as razões de apelação impugnam os fundamentos da sentença, ainda que repitam argumentos da inicial, desde que demonstrado o interesse na reforma do julgado (STJ, AgInt no AREsp 976.892/GO). 1. O cartão de crédito consignado com RMC constitui modalidade híbrida de crédito, cuja amortização ocorre por meio do desconto mínimo em folha, diferindo do empréstimo consignado tradicional, em que as parcelas amortizam integralmente o saldo devedor. 1. O dever de informação, previsto nos arts. 6º, III, e 46 do Código de Defesa do Consumidor, impõe ao fornecedor o ônus de prestar informações claras, precisas e ostensivas sobre o produto ou serviço oferecido, especialmente em operações financeiras complexas. 1. A ausência de entrega do cartão físico, a disponibilização do valor contratado por TED e a inexistência de informações claras no contrato quanto ao número de parcelas e encargos configuram falha no dever de informação, apta a caracterizar vício de consentimento. 1. A conversão do contrato de cartão de crédito consignado com RMC em empréstimo consignado convencional preserva o negócio jurídico e corrige o desvirtuamento da contratação, conforme o princípio da conservação dos contratos (CC, art. 170). 1. Os juros remuneratórios devem ser recalculados conforme a taxa média de mercado para empréstimos consignados, divulgada pelo Banco Central à época da contratação. 1. A restituição dos valores pagos a maior deve ocorrer de forma simples, pois não se comprovou má-fé da instituição financeira, conforme entendimento do STJ (AgInt no AREsp 1.110.103/DF). 1. A cumulação da Taxa Selic com o INPC é indevida, devendo incidir apenas a Taxa Selic para atualização dos valores a restituir. IV. DISPOSITIVO E TESE 1. Recurso provido. Tese de julgamento: 1. A contratação de cartão de crédito consignado, quando o consumidor acredita estar firmando empréstimo consignado tradicional, caracteriza vício de consentimento por falha no dever de informação. 1. A operação deve ser convertida em contrato de empréstimo consignado convencional, aplicando-se a taxa média de mercado para essa modalidade à época da contratação. 1. É devida a restituição simples dos valores pagos a maior, em razão da ausência de comprovação de má-fé da instituição financeira. 1. A atualização monetária deve observar exclusivamente a Taxa Selic, afastada a cumulação com o INPC. Dispositivos relevantes citados: CC, art. 170; CDC, arts. 6º, III, 39, III e V, 42, e 46. Jurisprudência relevante citada: STJ, AgInt no AREsp 976.892/GO, Rel. Min. Raul Araújo, Quarta Turma, DJe 29/08/2017; STJ, AgInt no REsp 1.823.145/SP, Rel. Min. Marco Buzzi, Quarta Turma, DJe 11/10/2019; STJ, AgInt no AREsp 1.110.103/DF, Rel. Min. Maria Isabel Gallotti, Quarta Turma, DJe 19/04/2018; TJMT, N.U 1025321-96.2021.8.11.0003, Rel. Des. Guiomar Teodoro Borges, j. 26/07/2023; TJMT, N.U 1031920-29.2024.8.11.0041, Rel. Des. Rubens de Oliveira Santos Filho, j. 30/04/2025.

### TJPR · Apelação Cível 0001158-73.2025.8.16.0170
- regras: R24
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001158-73.2025.8.16.0170
- orgao: 16ª Câmara Cível
- relator: Des. Luiz Henrique Miranda
- julgamento: 2026-02-09
- publicacao: 2026-02-09
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035094801/Ac%C3%B3rd%C3%A3o-0001158-73.2025.8.16.0170
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Cartão consignado (RMC) contratado por telefone, sem informação clara sobre encargos e forma de pagamento e sem contrato juntado: o TJPR reconhece erro substancial e vício de consentimento, converte o contrato em empréstimo consignado comum pela taxa média do BACEN da data da transferência e manda devolver em dobro a diferença entre o descontado e o valor creditado.
- observacao: Apelação da autora parcialmente provida (sentença de improcedência reformada). É o único acórdão de Câmara Cível do TJPR localizado que converte o RMC por falha de informação; a maioria das Câmaras reforma as conversões quando o contrato é claro. Antecipar: (i) a 13ª Câmara Cível mantém sobrestamento de ações de RMC pelo Tema 1.414/STJ (julgamento de 09/10/2026), de modo que o caso pode ficar suspenso; (ii) a ementa fixa dano moral em R$ 5.000,00, mas o voto e o dispositivo da íntegra arbitram R$ 7.000,00; citar o acórdão pela conversão e pela restituição, não pelo valor do dano moral. A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (3ª Vara Cível de Toledo, RMC contratado por telefone, banco réu, apelação da autora). Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Toledo).

ementa:
> APELAÇÃO CÍVEL. AÇÃO DECLARATÓRIA DE INEXIGIBILIDADE DE DÉBITO, COM PEDIDO CUMULADO DE INDENIZAÇÃO POR DANOS MATERIAIS E MORAIS. CARTÃO DE CRÉDITO COM RESERVA DE MARGEM CONSIGNÁVEL (RMC). SENTENÇA QUE JULGOU IMPROCEDENTES OS PEDIDOS INICIAIS. INSURGÊNCIA DA AUTORA. I. CASO EM EXAME Apelação cível visando a reforma de sentença que julgou improcedentes os pedidos de declaração de inexigibilidade de débito e de indenização por danos materiais e morais, em razão de contratação de cartão de crédito com reserva de margem consignável, alegadamente realizada sem a devida informação à autora sobre as condições do contrato.
> II. QUESTÃO EM DISCUSSÃO Saber se é válida a contratação de cartão de crédito com reserva de margem consignável realizada por telefone e se a autora tem direito à conversão do contrato em empréstimo consignado, bem como à restituição em dobro dos valores descontados e à indenização por danos morais. III. RAZÕES DE DECIDIR 1) Inexistência, à época da contratação, de vedação legal à oferta e celebração de contratos de empréstimo a aposentados e pensionistas por via telefônica.2) Vício de consentimento reconhecido. Em análise à gravação da conversa telefônica entre a correspondente bancária e a Autora, extrai-se que não foram fornecidas a esta informações claras e suficientes acerca das condições contratuais, em especial a forma de pagamento e os encargos aplicáveis ao saldo devedor. Ademais, o banco não apresentou instrumento contratual, tampouco as faturas do cartão de crédito.3) Considerando a vulnerabilidade técnica e financeira da Autora, que contava com mais de 47 anos à época da contratação e aufere pensão inferior a dois mil reais, é possível conjecturar que não tenha compreendido a natureza da operação de crédito e os encargos que seriam a ela imputados. 4) Reconhecida a anulabilidade do contrato por erro substancial, a relação contratual deve ser convertida em empréstimo consignado comum.5) A autora tem direito à devolução em dobro dos valores descontados indevidamente, além de indenização por danos morais no valor de R$ 5.000,00. VI. Dispositivo e tese APELAÇÃO CONHECIDA E PARCIALMENTE PROVIDA para converter o contrato de cartão de crédito em empréstimo consignado comum, condenando o réu ao pagamento em dobro da diferença entre os valores descontados do benefício previdenciário da autora e o montante a ela transferido, além de indenização por danos morais no valor de R$ 5.000,00.Tese de julgamento: É nula a contratação de cartão de crédito consignado realizada sem a devida informação clara sobre suas condições, especialmente em relação aos encargos e à natureza da operação, configurando vício de consentimento que permite a conversão do contrato em empréstimo consignado comum e a devolução em dobro dos valores pagos indevidamente.

### TJPR · Apelação Cível 0038387-97.2023.8.16.0021
- regras: R24
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0038387-97.2023.8.16.0021
- orgao: 14ª Câmara Cível
- relator: Des. João Antônio de Marchi
- julgamento: 2025-11-17
- publicacao: 2025-11-18
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000033095051/Ac%C3%B3rd%C3%A3o-0038387-97.2023.8.16.0021
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Quando o banco não exibe o contrato assinado, com especificação clara e adequada do produto, o TJPR confirma a nulidade do cartão consignado (RMC) e a conversão da modalidade em empréstimo consignado comum, com restituição simples do pago a maior.
- observacao: Apelação do banco parcialmente provida: mantidas a nulidade e a conversão; afastado o dano moral (proveito econômico do autor) e redistribuída a sucumbência (60% banco, 40% autor). O fundamento é a falta de prova do contrato com informação clara (ônus do banco, art. 373, II, do CPC), não a prova de erro do consumidor; serve como caminho probatório da R24 quando o instrumento não é juntado. A restituição é simples, como na sentença mantida. A íntegra cita o próprio CNJ. A ementa vem em texto corrido, como no original. Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Cascavel).

ementa:
> APELAÇÃO CÍVEL. “AÇÃO DE NULIDADE CONTRATUAL E DANOS MATERIAIS C/C DANOS MORAIS”. CARTÃO DE CRÉDITO CONSIGNADO (RMC). SENTENÇA. PROCEDÊNCIA. 1. INSURGÊNCIA DO BANCO RÉU: 1.1. CONTRATAÇÃO REGULAR. TESE NÃO ACOLHIDA. CARTÃO DE CRÉDITO CONSIGNADO COM RESERVA DE MARGEM CONSIGNÁVEL (RMC). CONTRATO NÃO JUNTADO PELO RÉU. AVENÇA NÃO COMPROVADA (CPC, ART. 373, II). NULIDADE DA CONTRATAÇÃO E CONVERSÃO DA MODALIDADE CONTRATUAL PARA EMPRÉSTIMO CONSIGNADO COMUM. PRECEDENTES. 1.2. EXCLUDENTE DE RESPONSABILIDADE, POR ATO DE TERCEIRO. NÃO ACOLHIMENTO. RELAÇÃO DE CONSUMO EVIDENCIADA (STJ, SÚMULA N.º 297). RESPONSABILIDADE OBJETIVA DO BANCO PELOS DANOS GERADOS POR FORTUITO INTERNO (STJ, SÚMULA N.º 479; CDC, ART. 14). PRECEDENTES. 1.3. DANO MORAL. AFASTAMENTO. TESE ACOLHIDA. AUTOR QUE OBTEVE PROVEITO ECONÔMICO COM O EMPRÉSTIMO. NÃO DEVOLUÇÃO ADMINISTRATIVA E NEM DEPÓSITO JUDICIAL DO VALOR CORRESPONDENTE AO CONTRATO. DESCONTOS INDEVIDOS EM BENEFÍCIO PREVIDENCIÁRIO QUE, NO CASO, NÃO ENSEJAM INDENIZAÇÃO POR DANO MORAL. MERO DISSABOR. PRECEDENTES. 1.4. DANOS MATERIAIS. JUROS MORATÓRIOS A PARTIR DA CITAÇÃO E/OU DA SENTENÇA E CORREÇÃO MONETÁRIA A PARTIR DA SENTENÇA. NÃO CABIMENTO. CORREÇÃO MONETÁRIA FIXADA CORRETAMENTE DESDE OS DESEMBOLSOS E JUROS MORATÓRIOS AQUI DEVIDOS DESDE O EVENTO DANOSO (CC, ART. 398; STJ, SÚMULA N.º 54), POR SE TRATAR DE RESPONSABILIDADE EXTRACONTRATUAL. PRECEDENTES. 1.5. PREQUESTIONAMENTO. AFASTADO. DESNECESSIDADE DE MENÇÃO EXPRESSA DOS DISPOSITIVOS DE LEI SUSCITADOS. INTELIGÊNCIA DO ART. 1.025 DO CPC. PRECEDENTES. 2. ÔNUS DE SUCUMBÊNCIA. SENTENÇA PARCIALMENTE REFORMADA. ALTERAÇÃO DO ESTADO DE DECAIMENTO DOS PEDIDOS DAS PARTES VERIFICADO NAQUELA OCASIÃO. REDISTRIBUIÇÃO DESSES ÔNUS ENTRE AS PARTES, COM NOVA FIXAÇÃO DE VERBA HONORÁRIA SUCUMBENCIAL, RESSALVADA A CONDIÇÃO SUSPENSIVA DE EXIGIBILIDADE (CPC, ART. 98, §3º) EM RELAÇÃO AO AUTOR. 3. HONORÁRIOS ADVOCATÍCIOS RECURSAIS. NÃO INCIDÊNCIA. INTELIGÊNCIA DO ART. 85, § 11, DO CPC. APELAÇÃO CONHECIDA E PARCIALMENTE PROVIDA.

## R26 — Repetição do indébito em dobro — boa-fé objetiva, sem exigir má-fé

Tese: A repetição em dobro (CDC, art. 42, parágrafo único) independe do elemento volitivo do fornecedor e cabe quando a cobrança indevida contraria a boa-fé objetiva, qualquer que seja a data do pagamento: o Tema 929/STJ (REsp 1.963.770/CE, Corte Especial, j. 15/09/2026) foi fixado sem modulação e afastou o corte de 30/03/2021 do EAREsp 676.608/RS. A omissão ou a recusa do banco diante de reclamação prévia do consumidor é indício suficiente do dobro (tese i.a), e cabe ao banco provar que não agiu de forma desleal ou descuidada (i.b). Limite (i.c): divergência jurisprudencial sobre o objeto da cobrança, ou cláusula depois declarada nula, é engano justificável e afasta o dobro; por isso a tese vale para a cobrança sem lastro contratual (gate da R26).

### STJ · REsp 1.963.770/CE
- regras: R26
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.963.770/CE
- orgao: Corte Especial
- relator: Min. Humberto Martins
- julgamento: 2026-09-15
- publicacao: 2026-11-03
- precedente_qualificado: Tema 929/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/7782005274
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Precedente obrigatório da repetição em dobro: independe do elemento volitivo e cabe na cobrança contrária à boa-fé objetiva, sem limite de data (tese fixada sem modulação, afastado o corte de 30/03/2021); a reclamação prévia ignorada ou recusada pelo banco é indício suficiente (i.a), e o ônus de provar a boa-fé é do banco (i.b). Sustenta o pedido de dobro sobre todo o período da cobrança sem lastro contratual.
- observacao: Tese fixada por maioria (vencidos parcialmente, só na redação, os Ministros João Otávio de Noronha, Raul Araújo e Maria Isabel Gallotti), em sessão virtual de 08 a 15/09/2026, "sem modulação de efeitos". Na retificação de voto, o relator adere ao voto do Ministro Luis Felipe Salomão: a modulação do EAREsp 676.608/RS e do EREsp 1.413.542/RS para contratos estritamente privados não atende ao art. 927, § 3º, do CPC e foi afastada. O mesmo acórdão traz o limite da tese (i.c), engano justificável, que vai em ressalvas quando a cobrança se funda em cláusula declarada nula ou em tema divergente. Caso concreto: financiamento com banco, restituição em dobro determinada. Publicação conferida na página do Tema 929 no STJ (03/11/2026); o Jusbrasil indexou em 06/11/2026. Correção de extração na ementa: "configurar-se- á" → "configurar-se-á".

ementa:
> CONSUMIDOR. RECURSO ESPECIAL REPETITIVO. TEMA 929/STJ. REPETIÇÃO EM DOBRO. ART. 42, PARÁGRAFO ÚNICO, DO CDC. COBRANÇA INDEVIDA AO CONSUMIDOR. MÁ-FÉ OBJETIVA. DESNECESSIDADE DE PROVA DO ELEMENTO VOLITIVO DO FORNECEDOR. DEMONSTRAÇÃO DA OMISSÃO OU RECUSA DO FORNECEDOR DIANTE DO PEDIDO PRÉVIO, E AINDA QUE INFORMAL, DO CONSUMIDOR APONTANDO A IRREGULARIDADE DA COBRANÇA. SUFICIÊNCIA PARA EMBASAR A PRETENSÃO DE RESTITUIÇÃO EM DOBRO. ÔNUS DO FORNECEDOR DE DEMONSTRAR ATUAÇÃO CONFORME À BOA-FÉ OBJETIVA. 1. Controvérsia: "Discussão quanto às hipóteses de aplicação da repetição em dobro prevista no art. 42, parágrafo único, do CDC." 2. Tese e subteses fixadas para o Tema 929/STJ (válidas tanto para contratos de direito privado quanto para contratos que envolvam prestação de serviço público): (i) A restituição em dobro do indébito (art. 42, parágrafo único, do CDC) independe da natureza do elemento volitivo do fornecedor que realizou a cobrança indevida, sendo cabível quando a referida cobrança consubstanciar conduta contrária à boa-fé objetiva. (i.a) A demonstração da omissão ou da recusa do fornecedor - como, por exemplo, em resposta a pedido informal e prévio do consumidor apontando a irregularidade da cobrança - será indício suficiente para embasar a pretensão de repetição em dobro. (i.b) Caberá ao fornecedor, na contestação ou na fase instrutória do processo, demonstrar que não atuou em contrariedade à boa-fé objetiva, isto é, que não agiu de forma desleal ou descuidada. (i.c) Se houver divergência jurisprudencial em relação ao objeto da cobrança indevida ou se a cláusula contratual em que se baseie for posteriormente declarada nula, configurar-se-á hipótese de engano justificável, excludente apta a afastar a incidência da sanção civil de repetição em dobro do indébito. Recurso especial julgado para firmar a tese e, no caso concreto, conhecido em parte e, nessa extensão, provido, a fim de determinar a restituição em dobro ao consumidor.

### STJ · EAREsp 676.608/RS
- regras: R26
- posicao: FAV
- tribunal: STJ
- classe_numero: EAREsp 676.608/RS
- orgao: Corte Especial
- relator: Min. Og Fernandes
- julgamento: 2020-10-21
- publicacao: 2021-03-30
- precedente_qualificado: não (embargos de divergência da Corte Especial; a tese foi reafirmada no Tema 929/STJ, REsp 1.963.770/CE, que afastou a modulação)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1205685304
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Origem da tese de que a restituição em dobro independe do elemento volitivo do fornecedor e cabe quando a cobrança indevida contraria a boa-fé objetiva. Citar depois do REsp 1.963.770/CE (Tema 929); a modulação de 30/03/2021 que este acórdão trazia foi afastada pelo repetitivo e não limita mais o pedido.
- observacao: Modulação confirmada no texto: aplica-se "apenas a partir da publicação do presente acórdão" às cobranças em contratos de consumo que não envolvam serviço público; a modulação vale só para a primeira tese. Mesma tese, mesma modulação e mesma data nos EREsp 1.413.542/RS, EAREsp 600.663/RS e outros (a redação da ementa difere: a do EAREsp 676.608/RS é a do voto do relator Og Fernandes; o STJ costuma citar Min. Herman Benjamin como relator para o acórdão da tese nesses embargos, o que a cópia aberta não registra). Os cabeçalhos de página "Superior Tribunal de Justiça" que o PDF inseriu no meio do texto foram retirados da ementa abaixo. Publicação conforme DJe indicado nos acórdãos posteriores. Em 16/11/2026: a modulação foi afastada no Tema 929/STJ (REsp 1.963.770/CE, sem modulação de efeitos).

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Acórdão recente da Terceira Turma, em contrato bancário (empréstimo consignado), mantendo a repetição em dobro sem exigir má-fé, porque a cobrança sem base contratual válida viola a boa-fé objetiva e não é engano justificável.
- observacao: Caso de consignado fraudulento (assinatura falsa) com idoso, não de tarifa ou seguro; o voto não examina a data dos descontos em relação ao marco de 30/03/2021 (reproduz a ementa do EAREsp 1.501.756/SC, que reafirma a modulação). Desde o Tema 929 (REsp 1.963.770/CE, sem modulação), a data dos descontos não limita mais o dobro. Publicação pela data do Jusbrasil.

ementa:
> PROCESSUAL CIVIL. CONSUMIDOR. AGRAVO EM RECURSO ESPECIAL. CONTRATO BANCÁRIO. EMPRÉSTIMO CONSIGNADO. FRAUDE. ASSINATURA FALSA. RESPONSABILIDADE OBJETIVA. REPETIÇÃO EM DOBRO. DANO MORAL. QUANTUM INDENIZATÓRIO. AGRAVOS CONHECIDOS PARA NEGAR PROVIMENTO AOS RECURSOS ESPECIAIS. RECURSO DE SABEMI SEGURADORA S.A. 1. Mantida a repetição em dobro dos valores indevidamente descontados, pois a cobrança indevida com violação da boa-fé objetiva dispensa a comprovação de má-fé do fornecedor, conforme orientação da Corte Especial firmada nos EREsp 1.413.542/RS. 2. Mantida a condenação por danos morais, cujo valor não se revela irrisório nem exorbitante diante da gravidade da fraude e da condição de idoso da vítima, afastando a intervenção excepcional desta Corte. 3. Agravo conhecido para negar provimento ao recurso especial. RECURSO DE BANCO PAN S.A. 1. Inexiste negativa de prestação jurisdicional quando o acórdão recorrido enfrenta os pontos necessários à resolução da lide e apresenta fundamentação suficiente para o desfecho da controvérsia, ainda que contrária aos interesses da parte. 2. Mantida a responsabilidade objetiva da instituição financeira pelos danos decorrentes de fraude contratual praticada por terceiro, diante do reconhecimento da falha na segurança do serviço. 3. Agravo conhecido para negar provimento ao recurso especial.

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
- url: https://portal.tjpr.jus.br/jurisprudencia/j/2100000036435831/Ac%C3%B3rd%C3%A3o-0009693-37.2024.8.16.0069
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Em financiamento de veículo, devolve em dobro, sem exigir má-fé, a tarifa de avaliação sem prova do serviço e o seguro com venda casada. O acórdão ainda aplicou a modulação de 30/03/2021, afastada depois pelo Tema 929 (REsp 1.963.770/CE): citar pelo dobro sem má-fé, não pelo corte.
- observacao: Julgado de Turma Recursal dos Juizados Especiais. O voto cita o marco como "[31/03/2021]" na transcrição da modulação, mas o DJe do EAREsp é 30/03/2021; usar 30/03/2021. Data de publicação igual à do julgamento (data do Jusbrasil). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem; ajustes: link permanente do portal.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Leading case do Tema 1061: impugnada a assinatura do contrato bancário, o ônus de provar a autenticidade é da instituição financeira.
- observacao: A ementa cita "arts. 6º, 368 e 429, II", mas a tese aprovada no acórdão, reproduzida pelo próprio STJ (página do Tema 1061, conferida em 28/10/2026) e pelos tribunais, é "arts. 6º, 369 e 429, II"; na peça, citar o art. 369. Oriundo de IRDR do TJMA sobre empréstimo consignado; a tese vale para "contrato bancário" em geral.

ementa:
> RECURSO ESPECIAL. PROCESSUAL CIVIL. ACÓRDÃO PROFERIDO EM IRDR. CONTRATOS BANCÁRIOS. EMPRÉSTIMO CONSIGNADO. DOCUMENTO PARTICULAR. IMPUGNAÇÃO DA AUTENTICIDADE DA ASSINATURA. ÔNUS DA PROVA. RECURSO ESPECIAL PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, DESPROVIDO. 1. Para os fins do art. 1.036 do CPC/2015, a tese firmada é a seguinte: "Na hipótese em que o consumidor/autor impugnar a autenticidade da assinatura constante em contrato bancário juntado ao processo pela instituição financeira, caberá a esta o ônus de provar a sua autenticidade (CPC, arts. 6º, 368 e 429, II)." 2. Julgamento do caso concreto. 2.1. A negativa de prestação jurisdicional não foi demonstrada, pois deficiente sua fundamentação, já que o recorrente não especificou como o acórdão de origem teria se negado a enfrentar questões aduzidas pelas partes, tampouco discorreu sobre as matérias que entendeu por omissas. Aplicação analógica da Súmula 284/STF. 2.2. O acórdão recorrido imputou o ônus probatório à instituição financeira, conforme a tese acima firmada, o que impõe o desprovimento do recurso especial. 3. Recurso especial parcialmente conhecido e, nessa extensão, desprovido.

### STJ · AgInt no AREsp 2.097.250/PR
- regras: R28
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no AREsp 2.097.250/PR
- orgao: Terceira Turma
- relator: Min. Paulo de Tarso Sanseverino (acórdão lavrado pelo Min. Ricardo Villas Bôas Cueva, art. 52, IV, b, do RISTJ)
- julgamento: 2023-04-03
- publicacao: 2023-04-27
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1922832316
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Reafirma o Tema 1061 em financiamento bancário (financeira que sustentava a dificuldade de provar a assinatura, inclusive no contrato eletrônico, perdeu): a impugnação do consumidor transfere à instituição financeira o ônus de provar a autenticidade.
- observacao: Decisão colegiada curta; o voto não esmiúça os fatos. A "data de julgamento" é a do encerramento da sessão virtual (28/03 a 03/04/2023). Publicação pela data do Jusbrasil. Conferido de novo em 16/11/2026: o `verificar_citacoes` do conector acusa relator divergente porque a base oficial do STJ registra quem lavrou o acórdão. O acórdão diz que o relator é o Min. Paulo de Tarso Sanseverino e que "Presidiu o julgamento o Sr. Ministro Ricardo Villas Bôas Cueva e lavrou este acórdão, nos termos do art. 52, IV, b, do RISTJ"; a citação traz os dois.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Impugnada a assinatura do empréstimo consignado, cabia ao banco provar a autenticidade (art. 429, II, CPC; Tema 1061); a perícia mostrou divergência das assinaturas, e o banco foi condenado (inexistência do contrato, restituição e dano moral).
- observacao: Complementa os acórdãos do TJPR desta tese. Data de publicação igual à do julgamento (data do Jusbrasil).

ementa:
> DIREITO DO CONSUMIDOR. APELAÇÃO CÍVEL. EMPRÉSTIMO CONSIGNADO. IMPUGNAÇÃO DE AUTENTICIDADE DA ASSINATURA. ÔNUS DA PROVA DA INSTITUIÇÃO FINANCEIRA. PERÍCIA GRAFOTÉCNICA. FRAUDE COMPROVADA. INEXISTÊNCIA DE RELAÇÃO JURÍDICA. DANOS MORAIS. RESPONSABILIDADE OBJETIVA DO BANCO. RECURSO DESPROVIDO. I. Caso em exame Apelação interposta contra sentença que declarou a inexistência do contrato de empréstimo consignado e condenou a instituição financeira à restituição dos valores descontados indevidamente do benefício previdenciário da autora, com correção monetária e juros, além do pagamento de indenização por danos morais no valor de R$ 8.000,00. A sentença ainda determinou o pagamento de custas, despesas processuais e honorários advocatícios pela parte ré. A instituição financeira sustenta a regularidade da contratação e requer a improcedência total da ação, alegando inexistência de dever de indenizar. II. Questão em discussão A questão em discussão consiste em verificar a validade da contratação do empréstimo consignado impugnado, bem como a responsabilidade da instituição financeira pelos descontos indevidos e a consequente obrigação de indenizar por danos morais. III. Razões de decidir A relação jurídica em questão envolve prestação de serviços bancários, aplicando-se o Código de Defesa do Consumidor (Súmula 297 /STJ). Nos termos do art. 429, II, do CPC, cabia à instituição financeira a prova da autenticidade da assinatura do contrato impugnado. A perícia grafotécnica constatou a divergência das assinaturas, evidenciando a falsidade documental e a inexistência de relação jurídica válida. O entendimento consolidado pelo Tema 1.061 /STJ atribui à instituição financeira o ônus da prova quanto à autenticidade do contrato bancário impugnado. A instituição financeira responde objetivamente pelos danos causados por falha na segurança de suas operações, nos termos do art. 14 do CDC e da Súmula 479 do STJ. O dano moral, em casos de descontos indevidos sobre benefício previdenciário, verba de caráter alimentar, é presumido (dano "in re ipsa"), não se exigindo comprovação do sofrimento pela parte prejudicada. O valor da indenização por danos morais fixado em R$ 8.000,00 mostra-se adequado, considerando a extensão do dano, a capacidade econômica das partes e o caráter pedagógico da condenação, ausente pedido de redução. Diante do improvimento do recurso, impõe-se a majoração dos honorários advocatícios recursais, nos termos do art. 85, § 11, do CPC . IV. Dispositivo e tese Recurso desprovido. Tese de julgamento: 1. A impugnação da autenticidade de assinatura contratual impõe à instituição financeira o ônus de comprovar sua validade, nos termos do art. 429, II, do CPC e do Tema 1.061 /STJ. 2. A falha na segurança dos serviços bancários configura responsabilidade objetiva da instituição financeira, nos termos do art. 14 do CDC . 3. O desconto indevido em benefício previdenciário caracteriza dano moral in re ipsa, sendo devida a reparação. Legislação relevante: CDC, art. 14; CPC, art. 429, II; CC, art. 406, § 1º e § 3º (redação dada pela Lei 14.905/2024). Jurisprudência relevante: STJ, Súmulas 297 e 479; STJ, Tema 1.061.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Impugnada a assinatura, cabe ao banco prová-la por prova técnica (Tema 1.061/STJ); sem ela, declara-se inexistente a relação jurídica e inexigível o débito. Assinatura eletrônica sem elementos mínimos de identificação e autenticação não valida o contrato.
- observacao: Embargos à execução de financiamento de veículo; o banco desistiu da perícia grafotécnica. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O TJPR mantém a nulidade de empréstimo consignado cuja assinatura foi impugnada e o banco não provou (CPC, art. 429, II; Tema 1.061/STJ), com dano moral e multa por litigância de má-fé imposta ao banco.
- observacao: O banco deixou precluir a perícia grafotécnica. Devolução conforme a modulação do EAREsp 676.608/RS. Fonte: portal de jurisprudência do TJPR (comarca de Guarapuava). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE INDENIZAÇÃO POR DANO MORAL E MATERIAL. CONTRATO DE EMPRÉSTIMO CONSIGNADO. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSO DO BANCO RÉU. PRETENSÃO DE RECONHECIMENTO DA REGULARIDADE DA CONTRATAÇÃO. NÃO OCORRÊNCIA. IMPUGNAÇÃO À AUTENTICIDADE DA ASSINATURA DO CONTRATO APRESENTADO. ÔNUS DO BANCO DE PROVAR A VERACIDADE. INTELIGÊNCIA DO ART. 429, II, DO CPC E DO TEMA 1.061 DO STJ. PRECLUSÃO QUANTO A SOLICITAÇÃO DE PERÍCIA GRAFOTÉCNICA. AUSÊNCIA DE PROVA HÁBIL QUANTO A AUTENTICIDADE DA ASSINATURA DA PARTE NO CONTRATO. NULIDADE DO CONTRATO MANTIDA. DEVOLUÇÃO DOS VALORES COBRADOS QUE DEVE SE DAR DE ACORDO COM A MODULAÇÃO DOS EFEITOS DO EARESP 676.608 DO STJ, SOB PENA DE REFORMATIO IN PEJUS. DANO MORAL CONFIGURADO. VALORES RECEBIDOS PELO AUTOR QUE FORAM DEPOSITADOS EM JUÍZO. IMPOSSIBILIDADE DE REDUÇÃO DO QUANTUM INDENIZATÓRIO. PRECEDENTES DESTA CORTE. TERMO INICIAL JUROS DE MORA. EVENTO DANOSO. SÚMULA Nº 54 DO STJ. FALHA NA PRESTAÇÃO DOS SERVIÇOS. PRETENSÃO DE AFASTAMENTO DA MULTA POR LITIGÂNCIA DE MÁ-FÉ. COMPORTAMENTO CONTRADITÓRIO DA INSTITUIÇÃO FINANCEIRA. MANUTENÇÃO DA CONDENAÇÃO EM MULTA POR LITIGÂNCIA DE MÁ-FÉ. ALTERAÇÃO DA VERDADE DOS FATOS E DEMANDA INFUNDADA. ARTIGO 80, INCISOS II E VI DO CPC. PREQUESTIONAMENTO DA MATÉRIA. EXPRESSA MENÇÃO DOS DISPOSITIVOS LEGAIS CONSIDERADOS VIOLADOS. DISPENSABILIDADE. PRECEDENTE DO STJ. SENTENÇA MANTIDA. HONORÁRIOS RECURSAIS FIXADOS. RECURSO DO BANCO RÉU CONHECIDO E NÃO PROVIDO.

## R29 — Comissão "flat" sem contraprestação de serviço autônomo

Tese: A comissão "flat" (percentual sobre o crédito a título de assessoria ou estruturação) é indevida quando não há contraprestação de serviço autônomo e efetivamente prestado, distinto da intermediação financeira já remunerada pelos juros, por abusividade (CDC, art. 51, IV) e ofensa à boa-fé e ao enriquecimento sem causa (CC, arts. 422 e 884).

Sem entrada verificada nesta onda. Base analógica: REsp 1.578.553/SP, tese 2.3.1, listado sob R09. Panorama e lacunas no Relatório.

### TJPR · Apelação Cível 0001221-92.2024.8.16.0151
- regras: R29
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001221-92.2024.8.16.0151
- orgao: 16ª Câmara Cível
- relator: Des. Luiz Henrique Miranda
- julgamento: 2026-08-31
- publicacao: 2026-08-31
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038383791/Ac%C3%B3rd%C3%A3o-0001221-92.2024.8.16.0151
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 16ª Câmara Cível mantém a abusividade da comissão flat, ainda que expressamente pactuada, por falta de prova da efetiva prestação do serviço de assessoria que seria a sua causa, e manda restituir.
- observacao: Embargos à execução de contrato de abertura de crédito empresarial; apelo do banco desprovido. Fundamento: boa-fé objetiva, vedação ao enriquecimento sem causa e aplicação analógica do Tema 958/STJ, com ônus da prova do serviço sobre o banco; o banco requereu julgamento antecipado e não produziu prova. A restituição alcança só o valor efetivamente desembolsado. A íntegra do portal não repete o CNJ no corpo do texto; o vínculo com o registro se confirma pelo conteúdo (comissão flat, assessoria na seleção da linha de crédito). Correções na ementa: inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Santa Izabel do Ivaí).

ementa:
> APELAÇÃO CÍVEL. EMBARGOS À EXECUÇÃO. CONTRATO DE ABERTURA DE CRÉDITO. COMISSÃO FLAT. REMUNERAÇÃO POR SUPOSTOS SERVIÇOS DE ASSESSORIA NA SELEÇÃO E ADEQUAÇÃO DA LINHA DE CRÉDITO. AUSÊNCIA DE COMPROVAÇÃO DA EFETIVA PRESTAÇÃO DOS SERVIÇOS. ABUSIVIDADE DA COBRANÇA. MANUTENÇÃO DA SENTENÇA. RECURSO DESPROVIDO. I. Caso em exame Trata-se de apelação cível interposta contra sentença que, em embargos à execução fundada em contrato de abertura de crédito empresarial, reconheceu a abusividade da cobrança da comissão flat e determinou a restituição dos valores correspondentes. A instituição financeira sustenta a licitude da cobrança, sob o argumento de que o encargo foi expressamente pactuado e constitui remuneração legítima pela assessoria prestada na seleção e adequação da linha de crédito. II. Questão em discussãoA questão em discussão consiste em saber se a cobrança da comissão flat, contratualmente prevista como remuneração por serviços de assessoria na seleção e adequação da linha de crédito, é válida independentemente da comprovação da efetiva prestação dos serviços que justificariam o encargo. III. Razões de decidir 1. A existência de cláusula contratual prevendo a cobrança da comissão flat não afasta, por si só, o controle jurisdicional de sua legalidade, sendo admissível o exame judicial da regularidade dos encargos pactuados à luz da boa-fé objetiva, da função social do contrato e da vedação ao enriquecimento sem causa. 2. A comissão flat não se confunde com tarifa bancária genérica ou remuneração por serviços colocados indistintamente à disposição do contratante. Trata-se de encargo destinado a remunerar atividade específica de assessoria na seleção e adequação da linha de crédito, aproximando-se da disciplina jurídica aplicável às cobranças por serviços prestados por terceiros. 3. Conforme orientação firmada pelo Superior Tribunal de Justiça no Tema Repetitivo n. 958, é abusiva a cobrança relacionada a serviços de terceiros quando inexistir adequada especificação do serviço ou demonstração de sua efetiva realização, entendimento que vem sendo aplicado por este Tribunal às hipóteses de cobrança de comissão flat. 4. No caso concreto, embora a cobrança encontre previsão contratual expressa, a instituição financeira não comprovou a efetiva prestação dos serviços de assessoria que justificariam a remuneração exigida. Ademais, requereu o julgamento antecipado da lide, sem produzir prova apta a demonstrar a realização das atividades alegadamente remuneradas pela comissão cobrada. 5. Ausente prova da efetiva contraprestação, revela-se abusiva a cobrança da comissão flat, impondo-se a manutenção da sentença que determinou a restituição dos valores correspondentes. IV. Dispositivo e tese Recurso de apelação conhecido e desprovido. Tese de julgamento: A cobrança da comissão flat em contrato bancário, ainda que expressamente prevista, exige a demonstração da efetiva prestação dos serviços de assessoria que constituem sua causa remuneratória, sendo abusiva a exigência do encargo quando ausente prova da correspondente contraprestação.

### TJPR · Apelação Cível 0007194-56.2024.8.16.0174
- regras: R29
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0007194-56.2024.8.16.0174
- orgao: 14ª Câmara Cível
- relator: Juiz Subst. 2º Grau Eduardo Novacki
- julgamento: 2026-06-15
- publicacao: 2026-06-16
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035162721/Ac%C3%B3rd%C3%A3o-0007194-56.2024.8.16.0174
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 14ª Câmara Cível declara nula a comissão flat (percentual fixo sobre o crédito sem contraprestação de serviço específico), tratada como tarifa disfarçada, com restituição simples.
- observacao: A autora é pessoa jurídica (CDC aplicado pela teoria finalista mitigada); apelo do banco desprovido e apelo da autora parcialmente provido, e a nulidade da flat foi declarada em julgamento imediato de omissão da sentença. O mesmo acórdão trata de venda casada, tarifas genéricas e juros do cheque especial, que não são o objeto desta linha. Correções na ementa: removido bloco de CSS que veio colado no início da ementa (defeito de extração); retirado o rótulo inicial "EMENTA:"; inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de União da Vitória).

ementa:
> DIREITO CIVIL, BANCÁRIO E DO CONSUMIDOR. APELAÇÕES CÍVEIS. AÇÃO REVISIONAL DE CONTRATOS BANCÁRIOS. SENTENÇA DE PARCIAL PROCEDÊNCIA. RECURSOS DE AMBAS AS PARTES.
> CHEQUE ESPECIAL. JUROS REMUNERATÓRIOS EXCESSIVOS. LIMITAÇÃO À TAXA MÉDIA DO BACEN. ABUSIVIDADE CONFIGURADA.
> SEGURO PRESTAMISTA. AUSÊNCIA DE INFORMAÇÃO E DE OPÇÃO DE ESCOLHA. VENDA CASADA. TEMA 972 DO STJ.
> TARIFAS BANCÁRIAS GENÉRICAS. AUSÊNCIA DE ESPECIFICAÇÃO DOS SERVIÇOS. NULIDADE.
> USO AUTOMÁTICO DO LIMITE DE CHEQUE ESPECIAL PARA PAGAMENTO DE DÉBITOS. CLÁUSULA ABUSIVA.
> CÉDULAS DE CRÉDITO BANCÁRIO (CCBs). JUROS REMUNERATÓRIOS DENTRO DA MÉDIA DE MERCADO. MANUTENÇÃO.
> OMISSÕES NA SENTENÇA. JUROS DA CONTA CORRENTE E COMISSÃO FLAT. JULGAMENTO IMEDIATO (ART. 1.013, §3º, III, CPC). JUROS DA CONTA CORRENTE SUPERIORES AO DOBRO DA TAXA MÉDIA DO BACEN. ABUSIVIDADE. LIMITAÇÃO PARCIAL.
> COMISSÃO FLAT. INEXISTÊNCIA DE CONTRAPRESTAÇÃO. TARIFA DISFARÇADA. NULIDADE.
> REPETIÇÃO DO INDÉBITO. AUSÊNCIA DE MÁ-FÉ. RESTITUIÇÃO SIMPLES.
> RECURSO DA INSTITUIÇÃO FINANCEIRA CONHECIDO E DESPROVIDO. RECURSO DA AUTORA CONHECIDO E PARCIALMENTE PROVIDO. I. CASO EM EXAME Apelações Cíveis interpostas contra sentença que julgou parcialmente procedentes os pedidos iniciais, limitando os juros do cheque especial à taxa média do BACEN, declarando a nulidade de tarifas e seguro (venda casada), além de afastar o desconto automático em conta sem saldo. A sentença manteve os juros das Cédulas de Crédito Bancário (CCBs) e a capitalização. A instituição financeira recorre defendendo a legalidade das cobranças. A empresa autora recorre buscando a limitação dos juros das CCBs, além de apontar omissão da sentença quanto aos juros da conta corrente e à comissão flat, pleiteando também a repetição em dobro. II. QUESTÃO EM DISCUSSÃOA questão em discussão consiste em verificar: a) a legalidade do seguro, das tarifas genéricas e da taxa de juros do cheque especial; b) a regularidade dos juros remuneratórios nas CCBs; c) a existência de omissão na sentença quanto aos juros da conta corrente e à comissão flat, e sua eventual abusividade; d) a possibilidade de repetição do indébito em dobro. III. RAZÕES DE DECIDIR 1. Incidência do Código de Defesa do Consumidor (Súmula 297 do STJ), aplicável à pessoa jurídica com base na teoria finalista mitigada, dada a vulnerabilidade frente à instituição financeira. 2. Recurso da instituição financeira: a cobrança de seguro sem a devida informação e opção clara de escolha configura venda casada (tema 972 do STJ). A cobrança de tarifas com referência genérica a tabelas, sem especificação dos serviços, é nula. A taxa de juros do cheque especial pactuada em 354,6% ao ano, quando a média do BACEN era de 34,4% ao ano, é flagrantemente abusiva, mantendo-se a limitação à média de mercado. É abusiva a cláusula que permite o uso automático do cheque especial para pagamento de dívidas, colocando a conta em descoberto sem autorização específica. 3. Recurso da empresa autora: constata-se a omissão da sentença quanto à comissão flat e aos juros da conta corrente, impondo-se o julgamento imediato (art. 1.013, parágrafo 3º, III, do CPC). 4. Juros das CCBs: as taxas cobradas (entre 1,07 e 1,39 vezes a média do BACEN) não caracterizam abusividade, conforme a súmula 382 do STJ, devendo ser mantidas. 5. Juros da conta corrente (omissão sanada): comprovada a cobrança de taxas que superam o dobro e até o triplo da média de mercado (ex: 42,23% cobrados versus 13,17% do BACEN). Abusividade configurada. Limitação à taxa média do BACEN devida apenas nos períodos em que a taxa cobrada superar o dobro da média divulgada. 6. Comissão flat (omissão sanada): a cobrança de percentual fixo sobre o crédito concedido, sem comprovação de qualquer contraprestação de serviço específico, configura tarifa disfarçada e onerosidade excessiva. Nulidade declarada. 7. Repetição do indébito: inexistindo comprovação de má-fé na época das cobranças, a restituição deve ocorrer de forma simples, conforme entendimento do STJ para encargos cobrados antes da modulação do EAResp 600.663/rs. IV. DISPOSITIVO E TESE Recurso da instituição financeira conhecido e desprovido. Recurso da empresa autora conhecido e parcialmente provido. Dispositivos relevantes citados: artigos 6º, inciso III e IV, 39, inciso I, e 51, inciso IV e parágrafo 1º, do CDC; artigos 421, 422 e 876 do CC/2002; artigo 1.013, parágrafo 3º, inciso III, do CPC/2015;Jurisprudência relevante citada: STJ, Tema 972 (RESP 1.639.320/SP); STJ, Temas 618 e 619; STJ, RESP 1.061.530/RS; Súmulas 297, 322, 382 E 539 do Superior Tribunal De Justiça.

### TJPR · Apelação Cível 0010275-45.2024.8.16.0131
- regras: R29
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0010275-45.2024.8.16.0131
- orgao: 16ª Câmara Cível
- relator: Des. Luiz Antonio Barry
- julgamento: 2025-12-15
- publicacao: 2025-12-16
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000034839491/Ac%C3%B3rd%C3%A3o-0010275-45.2024.8.16.0131
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: A 16ª Câmara Cível reconhece a abusividade da comissão flat quando o banco não demonstra a efetiva prestação dos serviços a ela vinculados, e declara o excesso da execução.
- observacao: Embargos à execução de cédula de crédito bancário; apelos parcialmente providos para julgar parcialmente procedentes os embargos apenas quanto à comissão flat e ao excesso de execução por juros em dias corridos (descaracterizada a mora); a multa moratória deixou de ser tida por abusiva. Correção na ementa: retirado o rótulo "Ementa:". Correções na ementa: retirado o rótulo inicial "Ementa:"; inseridos espaços onde a extração emendou palavras (títulos e numeração dos itens). Fonte: portal de jurisprudência do TJPR (comarca de Pato Branco).

ementa:
> Direito bancário e processual civil. Apelação cível. Abusividade de cláusulas contratuais em cédula de crédito bancário. Apelos parcialmente providos. I. Caso em exame 1. Apelação cível visando a reforma de sentença que julgou parcialmente procedentes embargos à execução, reconhecendo a abusividade da cobrança de multa moratória e comissão flat, bem como a existência de excesso na execução ante a cobrança de juros em dias corridos em desacordo com a expressa previsão contratual de cobrança em dias úteis dos encargos financeiros. II. Questão em discussão 2. A questão em discussão consiste em saber se é abusiva a cobrança da comissão flat, se existe abusividades nos encargos contratuais e moratórios e se há excesso na execução em razão da aplicação de encargos financeiros em dias corridos, além de discutir a descaracterização da mora. III. Razões de decidir 3. A sentença foi parcialmente procedente ao declarar a abusividade da cobrança da multa moratória e da comissão flat, além de reconhecer o excesso em execução. 4. A jurisprudência reconhece a abusividade da comissão flat quando não demonstrada a efetiva prestação dos serviços a ela vinculados. 5. O reconhecimento da abusividade nos encargos durante a normalidade do contrato descaracteriza a mora. 6. Os ônus sucumbenciais foram readequados, com a parte embargante arcando com 70% e a parte embargada com 30% das custas processuais. IV. Dispositivo e tese 7. Apelos providos para julgar parcialmente procedentes os embargos à execução, reconhecendo a abusividade da comissão flat e o excesso da execução, além de descaracterizar a mora. Tese de julgamento: É abusiva a cobrança de comissão flat em contratos bancários quando não demonstrada a efetiva prestação dos serviços a ela vinculados, configurando excesso na execução e descaracterização da mora em razão da abusividade dos encargos financeiros aplicados em desacordo com o contrato._________ Dispositivos relevantes citados:
> CPC/2015, art. 487, I; CC/2002, arts. 51, IV, e 39, V; Lei nº 10.931/2004, art. 28, § 2º, incisos I e II. Jurisprudência relevante citada:
> TJPR, AREsp 2.824.398/RS, Rel. Min. Ricardo Villas Bôas Cueva, Terceira Turma, j. 12.08.2025; TJPR, AgInt no AREsp 2.566.896/PR, Rel. Min. Raul Araújo, Quarta Turma, j. 19.08.2024; TJPR, AREsp 2.864.234/RS, Rel. Min. Moura Ribeiro, Terceira Turma, j. 28.04.2025; TJPR, REsp 1.578.553/SP, Rel. Min. Luis Felipe Salomão, Segunda Seção, j. 14.08.2013; TJPR, REsp 1.291.575/PR, Rel. Min. Luis Felipe Salomão, Segunda Seção, j. 14.08.2013; Súmula nº 539/STJ.

## R30 — Capitalização de juros moratórios

Tese: A cláusula que manda capitalizar os juros moratórios, expressamente ou por remissão à periodicidade dos remuneratórios, é abusiva: a capitalização em periodicidade inferior à anual (MP 2.170-36/2001, art. 5º; Súmulas 539 e 541/STJ) foi admitida só para os juros remuneratórios; os moratórios, de natureza sancionatória, limitam-se a 1% ao mês (Súmula 379/STJ) e incidem de forma simples (CC, art. 406), devendo ser recalculados e restituído o excesso efetivamente cobrado.

### STJ · AREsp 2.815.158/SP
- regras: R30
- posicao: FAV
- tribunal: STJ
- classe_numero: AREsp 2.815.158/SP
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2025-08-25
- publicacao: 2025-08-29
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6576118185
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: A Terceira Turma afirma que a capitalização em periodicidade inferior à anual das Súmulas 539 e 541 vale só para os juros remuneratórios e que é vedada a capitalização dos juros moratórios (Súmula 379/STJ): a cláusula que capitaliza a mora (no caso, diariamente) é abusiva, com limitação e restituição simples do excesso, sem descaracterizar a mora.
- observacao: Cartão de crédito. O agravante era o consumidor (pedia a limitação dos remuneratórios e a descaracterização da mora); a vedação da capitalização dos moratórios fora decidida pelo TJSP e o banco não recorreu. O STJ não só manteve o ponto como o endossou no voto ("com a devida precisão técnica, a Corte de origem diferenciou entre juros remuneratórios e juros moratórios, vedando a capitalização diária destes últimos, por ausência de previsão legal e por afronta à Súmula nº 379") e dele partiu para manter a mora; a tese é fundamento do acórdão, não objeto do recurso. Não há repetitivo nem acórdão de Seção sobre o tema; decisões monocráticas posteriores do STJ reproduzem esta ementa. Sessão virtual de 19 a 25/08/2025; DJEN de 29/08/2025, indicado no inteiro teor. Ementa sem correções.

ementa:
> AGRAVO EM RECURSO ESPECIAL. DIREITO CIVIL. REVISÃO DE CONTRATO. CARTÃO DE CRÉDITO. JUROS REMUNERATÓRIOS. CAPITALIZAÇÃO. JUROS MORATÓRIOS. MORA. ABUSIVIDADE PARCIAL. RESTITUIÇÃO SIMPLES. REEXAME DE PROVAS. SÚMULAS NºS 5 E 7 DO STJ.
> 1. A estipulação de juros remuneratórios em patamar inferior ou ligeiramente superior à taxa média de mercado divulgada pelo Bacen não configura, por si só, abusividade.
> 2. É válida a capitalização de juros remuneratórios em periodicidade inferior à anual, desde que pactuada, nos termos das Súmulas nºs 539 e 541 do STJ, sendo vedada a capitalização de juros moratórios, consoante a Súmula nº 379 do STJ.
> 3. Caracteriza-se abusiva a cláusula contratual que prevê a capitalização diária dos juros moratórios, impondo-se sua limitação e a restituição simples de eventuais valores pagos a maior.
> 4. O reconhecimento de abusividade restrita aos juros moratórios não descaracteriza a mora do devedor quanto aos encargos exigidos no período de normalidade contratual.
> 5. É inviável o recurso especial quando a pretensão de reforma do julgado pressupõe reexame do conjunto fático-probatório e interpretação de cláusulas contratuais, nos termos das Súmulas nºs 5 e 7/STJ.
> 6. Agravo em recurso especial conhecido para conhecer em parte do recurso especial e, nessa extensão, negar-lhe provimento.

### TJPR · Apelação Cível 0007057-09.2024.8.16.0131
- regras: R30
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0007057-09.2024.8.16.0131
- orgao: 13ª Câmara Cível
- relator: Des. Fernando Ferreira de Moraes
- julgamento: 2025-12-05
- publicacao: 2025-12-08
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035119391/Ac%C3%B3rd%C3%A3o-0007057-09.2024.8.16.0131
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em financiamento de veículo com alienação fiduciária (CCB), o TJPR mantém a capitalização mensal pactuada dos remuneratórios, mas afasta os "juros moratórios de 1% ao mês capitalizados": o encargo do período de inadimplência não admite capitalização sem previsão legal específica (a Lei 10.931/2004 não a traz), segue o art. 406 do CC e a Súmula 379/STJ, e passa a incidir a 1% ao mês, de forma simples.
- observacao: Revisional ajuizada pela consumidora; sentença de improcedência reformada em parte (também reconhecida a venda casada do seguro prestamista, com restituição simples). Mora mantida: a abusividade recaiu só sobre encargo da inadimplência e sobre encargo acessório. O voto cita, no mesmo sentido, a 13ª Câmara Cível (agravo de instrumento, j. 02/08/2024) e a 14ª Câmara Cível (apelação, j. 22/07/2025). A íntegra do portal cita o próprio CNJ. Ementa sem correções. Fonte: portal de jurisprudência do TJPR (comarca de Pato Branco).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL. ALIENAÇÃO FIDUCIÁRIA. CAPITALIZAÇÃO DIÁRIA. INOVAÇÃO RECURSAL. TEMA NÃO CONHECIDO. CERCEAMENTO DE DEFESA. NÃO OBSERVADO. PROVA PERICIAL. DESNECESSIDADE. CAPITALIZAÇÃO DE JUROS. EXPRESSA PACTUAÇÃO. VERIFICADA. JUROS MORATÓRIOS CAPITALIZADOS. ILEGALIDADE. AUSÊNCIA DE PREVISÃO NA LEI Nº 10.931/2004. SÚMULA 379 DO STJ. VERIFICADA. ABUSIVIDADE DOS JUROS REMUNERATÓRIOS. NÃO CONSTATADA. LIMITAÇÃO. INDEVIDA. SEGURO PRESTAMISTA. IRREGULARIDADE. VENDA CASADA. REPETIÇÃO DEVIDA, NA FORMA SIMPLES. MORA. NÃO DESCARACTERIZADA. SENTENÇA REFORMADA EM PARTE. ÔNUS SUCUMBENCIAL. REDEFINIDO. RECURSO CONHECIDO EM PARTE E, NA PARTE CONHECIDA, PARCIALMENTE PROVIDO.

### TJPR · Apelação Cível 0005062-02.2020.8.16.0001
- regras: R30
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0005062-02.2020.8.16.0001
- orgao: 14ª Câmara Cível
- relator: Des.ª Josely Dittrich Ribas
- julgamento: 2023-05-22
- publicacao: 2023-06-02
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000022968171/Ac%C3%B3rd%C3%A3o-0005062-02.2020.8.16.0001
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em embargos à execução de cédula de crédito bancário, o TJPR afasta a cláusula de juros de mora capitalizados diariamente: a Lei 10.931/2004 não disciplina os juros moratórios, aplica-se a Súmula 379/STJ (até 1% ao mês) e não há amparo legal para capitalizá-los; a capitalização ficou demonstrada no próprio cálculo do credor (taxa de mora efetiva de 12,68% ao ano em vez de 12%).
- observacao: Devedora pessoa jurídica. Recurso provido só para afastar os juros moratórios capitalizados, com recálculo da execução; a embargante ficou vencida quanto à comissão de permanência cumulada, ao CET e à estipulação prévia de honorários advocatícios (ponto relevante para a R32, em sentido contrário). Mostra o cuidado da R30: conferir se a memória do credor efetivamente capitalizou a mora. Julgado de 2023. A íntegra do portal cita o próprio CNJ. Correção na ementa: a quebra de linha do portal antes de "RECURSO CONHECIDO" foi trocada por espaço. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> APELAÇÃO CÍVEL. EMBARGOS À EXECUÇÃO. CÉDULA DE CRÉDITO BANCÁRIO (CONFISSÃO DE DÍVIDA). SENTENÇA DE IMPROCEDÊNCIA DOS PEDIDOS INICIAIS. PRELIMINAR DE VIOLAÇÃO DO PRINCÍPIO DA DIALETICIDADE SUSCITADA PELO BANCO RÉU NAS CONTRARRAZÕES. AFASTAMENTO. CERCEAMENTO DE DEFESA. INOCORRÊNCIA. QUESTÕES DE DIREITO QUE PODEM SER RESOLVIDAS MEDIANTE A ANÁLISE DOS DOCUMENTOS JUNTADOS AOS AUTOS. DESNECESSIDADE DE PRODUÇÃO DE PROVA PERICIAL NA ESPÉCIE. JUIZ, ADEMAIS, QUE É DESTINATÁRIO DAS PROVAS. JULGAMENTO ANTECIPADO DA LIDE QUE NÃO CONFIGURA CERCEAMENTO DE DEFESA, QUANDO O MAGISTRADO ENTENDE EXISTIREM PROVAS SUFICIENTES PARA O DESLINDE DA CONTROVÉRSIA. COBRANÇA DE JUROS DE MORA CAPITALIZADOS DIARIAMENTE. PREVISÃO CONTRATUAL. AFASTAMENTO. IMPOSSIBILIDADE DE COBRANÇA DE JUROS MORATÓRIOS NA FORMA CAPITALIZADA, POR AUSÊNCIA DE AMPARO LEGAL. APLICAÇÃO, NA HIPÓTESE, DO ENUNCIADO DA SÚMULA 379 DO STJ. PRECEDENTES DO STJ E DESTE TRIBUNAL. CASO EM QUE RESTOU DEMONSTRADA A COBRANÇA DOS JUROS DE MORA NA FORMA CAPITALIZADA. ILEGALIDADE RECONHECIDA. OMISSÃO, NO CONTRATO, DO CUSTO EFETIVO TOTAL (CET). INOCORRÊNCIA. INSTRUMENTO CONTRATUAL QUE, EMBORA NÃO TENHA INFORMADO A TAXA PERCENTUAL ANUAL, DISCRIMINA NO INSTRUMENTO, E EM TERMO SEPARADO, A TOTALIDADE DOS ENCARGOS COBRADOS. SENTENÇA PARCIALMENTE REFORMADA. RECURSO CONHECIDO E PARCIALMENTE PROVIDO.

## R31 — Multa moratória sobre base que inclui juros

Tese: A multa moratória incide sobre o valor da prestação vencida (CDC, art. 52, § 1º) ou sobre o principal da obrigação inadimplida, e não sobre o débito total apurado com os juros, em especial os moratórios, que já sancionam o mesmo atraso; a cláusula ou o cálculo que amplia a base da multa gera bis in idem, e o excesso deve ser decotado (CC, arts. 404 e 884).

### STJ · REsp 2.114.092/MG
- regras: R31
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.114.092/MG
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2026-03-09
- publicacao: 2026-03-16
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6613226320
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: o STJ admite a cumulação de multa moratória com juros de mora, por terem naturezas distintas, e fixa a multa em 2% "sobre o valor da prestação" (CDC, art. 52, § 1º). A R31 não deve atacar a cumulação, só a base ampliada; o parâmetro do próprio acórdão (valor da prestação) serve para recusar a multa calculada sobre o débito total acrescido de juros.
- observacao: Recurso do banco parcialmente provido: o TJMG havia excluído a multa por inviável a cumulação com juros de mora; o STJ restabeleceu a multa, reduzida de 10% para 2% do valor da prestação, e a capitalização pactuada. O acórdão não examinou se juros integram a base da multa. Crédito rotativo com pessoa jurídica. Sessão virtual de 03 a 09/03/2026. Publicação pela data do Jusbrasil (o inteiro teor não traz o DJEN). Ementa sem correções.

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. CAPITALIZAÇÃO MENSAL DE JUROS EM CONTRATOS BANCÁRIOS. CUMULAÇÃO DE MULTA MORATÓRIA COM JUROS DE MORA. RECURSO PARCIALMENTE PROVIDO.
> 1. A Medida Provisória nº 2.170-36/2001 permite a capitalização de juros com periodicidade inferior a um ano em contratos celebrados com instituições integrantes do Sistema Financeiro Nacional, desde que expressamente pactuada.
> 2. A jurisprudência do Superior Tribunal de Justiça, consolidada na Súmula 539, reconhece a legalidade da capitalização mensal de juros em contratos bancários celebrados após 31 de março de 2000, desde que expressamente pactuada. A previsão no contrato bancário de taxa de juros anual superior ao duodécuplo da mensal é suficiente para permitir a cobrança da taxa efetiva anual contratada, conforme entendimento da Súmula 541 do STJ.
> 3. A jurisprudência do STJ é firme no sentido de que é possível a cumulação de juros moratórios com multa moratória, pois possuem naturezas distintas: os juros remuneram o capital pelo atraso, enquanto a multa pune o inadimplemento.
> 4. A multa moratória deve ser limitada ao patamar de 2% sobre o valor da prestação, conforme disposto no artigo 52, § 1º, do Código de Defesa do Consumidor, aplicável às instituições financeiras.
> 5. Recurso especial parcialmente provido.

### TJPR · Apelação Cível 0002410-79.2024.8.16.0095
- regras: R31
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002410-79.2024.8.16.0095
- orgao: 14ª Câmara Cível
- relator: Des.ª Josely Dittrich Ribas
- julgamento: 2026-05-25
- publicacao: 2026-06-02
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035134121/Ac%C3%B3rd%C3%A3o-0002410-79.2024.8.16.0095
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: É a própria tese: a multa moratória incide exclusivamente sobre o valor da obrigação principal; aplicá-la sobre o débito total já acrescido de juros (no caso, principal corrigido + juros compensatórios + juros moratórios) amplia indevidamente a base e configura bis in idem. O TJPR restringe a multa de 2% ao principal e reconhece o excesso de execução.
- observacao: Embargos à execução de CCB do PRONAMPE (devedora micro ou pequena empresa); o recurso do embargante foi provido só neste ponto (o banco venceu quanto à SELIC do programa; mantidos juros, capitalização e mora). O "precedente do STJ" citado é o AgInt no REsp 1.891.797/RS (juros de mora não incidem sobre multa cominatória), aplicado por analogia: não há precedente do STJ específico sobre a base da multa contratual. A íntegra do portal cita o próprio CNJ. Correções na ementa: espaços inseridos onde o portal emendou título de seção ou ponto final ao texto seguinte (ex.: "EXAME1." → "EXAME 1."; "contratuais.II." → "contratuais. II."); nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Irati).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÕES CÍVEIS. EMBARGOS À EXECUÇÃO. CÉDULA DE CRÉDITO BANCÁRIO. PRONAMPE. INSURGÊNCIA DE AMBAS AS PARTES. APELO DA EMBARGADA CONHECIDO E PROVIDO. APELO DO EMBARGANTE PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, PARCIALMENTE PROVIDO. I. CASO EM EXAME 1. Apelações cíveis interpostas contra sentença que julgou parcialmente procedentes os embargos à execução, para o fim de declarar a ilegalidade da cumulação da SELIC com os encargos contratuais. II. QUESTÃO EM DISCUSSÃO 2. As questões em discussão consistem em verificar se: (i) o recurso do embargante comporta integral conhecimento; (ii) houve cerceamento de defesa; (iii) os juros remuneratórios são abusivos; (iv) é legal a capitalização de juros na espécie; (v) é possível a incidência de multa moratória sobre o valor total do débito; e (vi) deve ser descaracterizada a mora. III. RAZÕES DE DECIDIR 3.1. Apelação (02) não conhecida com relação à TAC, por ausência de interesse recursal, e à alegação de necessidade de observância do CET na análise da abusividade dos juros remuneratórios, por se tratar de inovação recursal. 3.2. Não há cerceamento de defesa, uma vez que a matéria é essencialmente de direito e os elementos constantes dos autos são suficientes para o deslinde da controvérsia, sendo desnecessária a produção de prova pericial. 3.3. Cédula de crédito bancário emitida no âmbito do Programa Nacional de Apoio às Microempresas e Empresas de Pequeno Porte – PRONAMPE, instituído pela Lei nº 13.999/2020. Previsão de incidência dos encargos básicos de acordo com a SELIC, somados aos encargos adicionais à taxa de 1,25% ao ano. Encargos que estão em consonância com o disposto no art. 3º, I, da Lei n° 13.999/2020, vigente à época da contratação. Inexistência de abusividade, por decorrer de expressa previsão legal. 3.4. Impossibilidade de limitação da taxa de juros à média de mercado, porquanto o percentual estabelecido no instrumento corresponde ao teto previsto na legislação específica aplicável na espécie. 3.5. Consoante os termos da súmula 539 do STJ, “é permitida a capitalização de juros com periodicidade inferior à anual em contratos celebrados com instituições integrantes do Sistema Financeiro Nacional a partir de 31/3/2000 (MP n. 1.963-17/2000, reeditada como MP n. 2.170-36/2001), desde que expressamente pactuada”. Ademais, a discrepância entre a taxa anual efetiva e o duodécuplo da taxa mensal prevista no contrato é suficiente para informar ao consumidor da existência da prática da capitalização de juros, conforme entendimento sedimentado pelo STJ (Súmula 541). No caso, além de o contrato prever expressamente a capitalização, a própria discrepância entre a taxa anual efetiva e o duodécuplo da taxa mensal prevista no contrato é suficiente para informar ao consumidor da existência da prática da capitalização de juros. Abusividade e onerosidade excessiva da cobrança não demonstrada. 3.6. Multa moratória que deve incidir exclusivamente sobre o valor da obrigação principal. Aplicação da multa moratória sobre o valor total do débito apurado, já acrescido de juros moratórios, implica indevida ampliação da base de cálculo e conduz a resultado incompatível com a sistemática das obrigações civis, pois configura bis in idem, ao penalizar duplamente o devedor. Precedente do STJ. 3.7. Não havendo abusividade nos encargos cobrados durante o período de normalidade contratual, não há que se falar em descaracterização da mora. IV. DISPOSITIVO 4.1. Recurso da embargada conhecido e provido. 4.2. Recurso do embargante parcialmente conhecido e, nessa extensão, parcialmente provido.______Dispositivos relevantes citados: CPC, arts. 141, 370 e 492; CC, art. 394; e Lei nº 13.999/2020, art. 3º. Jurisprudência relevante citada: STJ, AREsp n. 2.961.237/MS, relator Ministro Raul Araújo, Quarta Turma, julgado em 20/10/2025; STJ, AREsp n. 2.591.400/PR, relator Ministro Ricardo Villas Bôas Cueva, Terceira Turma, julgado em 18/8/2025; STJ, AgInt no REsp n. 1.891.797/RS, relatora Ministra Maria Isabel Gallotti, Quarta Turma, julgado em 23/5/2022; TJPR - 14ª Câmara Cível - 0006618-09.2025.8.16.0019 - Rel.: DES. FRANCISCO EDUARDO GONZAGA DE OLIVEIRA - J. 06.05.2026.

## R32 — Honorários advocatícios extrajudiciais cumulados com judiciais

Tese: Na cobrança judicial do contrato bancário, os honorários do advogado do credor são os de sucumbência, arbitrados pelo juízo (CPC, art. 85); a cláusula que soma honorários "extrajudiciais" a honorários "judiciais", ambos em percentual sobre o total da dívida, prefixa verba que só o juiz fixa e cobra duas vezes pela mesma cobrança, de modo que a rubrica extrajudicial lançada na execução sem prova de cobrança extrajudicial efetivamente feita por advogado deve ser decotada (CC, art. 884).

### STJ · REsp 2.166.423/DF
- regras: R32
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.166.423/DF
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2025-12-09
- publicacao: 2025-12-12
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6266031655
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: O STJ mantém o afastamento da cumulação de honorários contratuais "vinculados à cobrança em juízo" com os honorários sucumbenciais do CPC, por duplicidade sobre a mesma base da execução; no voto, registra que a prefixação só se admite para a cobrança extrajudicial e que, na via judicial, rege a verba sucumbencial do CPC, sem ofensa aos arts. 389, 395 e 404 do CC.
- observacao: Não é contrato bancário: execução promovida por sociedade de advogados contra cliente, com cláusula de 20% de honorários "em caso de execução judicial da dívida". O STJ aplicou a Súmula 5 à releitura das cláusulas, mas afirmou, no mérito, que não há violação dos arts. 389, 395 e 404 do CC quando se afasta a sobreposição na via judicial. Sessão virtual de 03 a 09/12/2025. Publicação pela data do Jusbrasil (o inteiro teor não traz o DJEN). Ementa sem correções.

ementa:
> CIVIL. PROCESSUAL CIVIL. RECURSO ESPECIAL. EMBARGOS À EXECUÇÃO. HONORÁRIOS CONTRATUAIS E HONORÁRIOS SUCUMBENCIAIS. NEGATIVA DE PRESTAÇÃO JURISDICIONAL. INOCORRÊNCIA. BIS IN IDEM NA VIA JUDICIAL. CLÁUSULAS CONTRATUAIS. SÚMULA 5/STJ. RECONHECIMENTO. RECURSO NÃO PROVIDO.
> 1. Não há negativa de prestação jurisdicional quando o acórdão recorrido aprecia os pontos essenciais, corrige contradição na distribuição dos honorários e enfrenta o pedido subsidiário com fundamentação suficiente.
> 2. Afastada a cumulação de honorários contratuais - vinculados à cobrança em juízo - com honorários sucumbenciais previstos no CPC, considerando a duplicidade sobre a mesma base fática da execução, reinterpretar as cláusulas contratuais invocadas encontra óbice na Súmula 5 do STJ.
> 3. Inviável o afastamento/compartilhamento de honorários sucumbenciais entre embargos distintos, por se tratarem de processos autônomos com partes e despesas próprias, sendo devida a verba em cada demanda conforme o trabalho realizado.
> 4. Recurso desprovido.

### STJ · REsp 2.157.400/RS
- regras: R32
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.157.400/RS
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2026-04-22
- publicacao: 2026-04-27
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6794461806
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: é válida a cláusula que, na mora, impõe ao devedor as despesas da cobrança extrajudicial, inclusive honorários de advogado (CC, arts. 389, 395 e 404), e esses honorários "não se confundem" com os de sucumbência. A R32 só se sustenta contra a rubrica que remunera a própria cobrança judicial ou contra a extrajudicial lançada sem prova de cobrança extrajudicial efetiva.
- observacao: Consórcio; o STJ reformou o TJRS, que reputara a cláusula abusiva pelo art. 51, XII, do CDC. O voto reafirma o REsp 1.002.445/DF (Quarta Turma, 2015), o AgInt no REsp 1.730.248/PE (Terceira Turma, 2022) e o REsp 1.971.958/DF (Terceira Turma, 2025): a reciprocidade do art. 51, XII, é assegurada ao consumidor pela própria lei, e a falta dela no contrato não torna a cláusula abusiva. Sessão virtual de 14 a 22/04/2026. Publicação pela data do Jusbrasil. Ementa copiada do inteiro teor, sem correções.

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. AÇÃO DE COBRANÇA EM CONSÓRCIO. VALIDADE DE CLÁUSULA DE RESSARCIMENTO DE DESPESAS DE COBRANÇA EXTRAJUDICIAL, INCLUSIVE HONORÁRIOS ADVOCATÍCIOS. RECURSO ESPECIAL CONHECIDO E PROVIDO.
> I. CASO EM EXAME
> 1. Recurso especial interposto contra acórdão estadual que negou provimento ao apelo da autora e deu parcial provimento ao apelo dos réus, com reconhecimento de ilegitimidade passiva de dois corréus e redistribuição dos ônus sucumbenciais.
> 2. A controvérsia envolve ação de cobrança de saldo remanescente de cotas de consórcio após alienação extrajudicial, com incidência de encargos de inadimplência previstos em cláusula contratual e sem ressarcimento de despesas de cobrança extrajudicial.
> 3. Na sentença, o Juízo de primeiro grau julgou parcialmente procedentes os pedidos para condenar solidariamente os réus ao pagamento do saldo remanescente, com encargos de inadimplência, vedando o ressarcimento das despesas de cobrança extrajudicial; fixou custas e honorários em 10% sobre o valor da condenação.
> 4. A Corte de origem negou provimento ao apelo da autora e deu parcial provimento ao apelo dos réus para reconhecer a ilegitimidade passiva de dois corréus e repartir os ônus sucumbenciais entre a administradora e os demais corréus.
> II. QUESTÃO EM DISCUSSÃO
> 5. A questão em exame consiste em saber se é válida a cláusula contratual que prevê o ressarcimento, pelo devedor inadimplente, das despesas de cobrança extrajudicial, inclusive honorários advocatícios, tendo em vista as disposições constantes dos arts. 389, 395 e 404 do CC e 51, XII, do CDC.
> III. RAZÕES DE DECIDIR
> 6. À luz da orientação consolidada do STJ, é válida a cláusula contratual que, em caso de mora, impõe ao devedor inadimplente o pagamento das despesas decorrentes de cobrança extrajudicial, inclusive honorários advocatícios, prerrogativa igualmente assegurada ao consumidor, independentemente de previsão contratual, nos termos do art. 51, XII, do CDC.
> IV. DISPOSITIVO E TESE
> 7. Recurso especial conhecido e provido.
> Tese de julgamento: "1. É válida a cláusula que, na mora, obriga o devedor ao pagamento das despesas de cobrança extrajudicial, inclusive honorários advocatícios".
> Dispositivos relevantes citados: CC, arts. 389, 395 e 404; CDC, art. 51, XII.
> Jurisprudência relevante citada: STJ, AgInt no REsp n. 1.730.248/PE, relator Ministro Paulo de Tarso Sanseverino, Terceira Turma, julgado em 16/5/2022.

### TJPR · Apelação Cível 0002573-05.2021.8.16.0050
- regras: R32
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002573-05.2021.8.16.0050
- orgao: 19ª Câmara Cível
- relator: Des. Domingos José Perfetto
- julgamento: 2023-07-24
- publicacao: 2023-07-24
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000024942471/Ac%C3%B3rd%C3%A3o-0002573-05.2021.8.16.0050
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em revisional de financiamento com alienação fiduciária, o TJPR mantém o afastamento da cláusula que previa honorários de até 10% do saldo devedor na cobrança extrajudicial e de 20% do valor da causa na judicial: além da falta de reciprocidade (CDC, art. 51, XII), a cláusula prefixa honorários de sucumbência, cuja fixação é atribuição exclusiva do juiz (CPC, art. 85).
- observacao: O fundamento da reciprocidade (art. 51, XII) contraria a orientação do STJ (REsp 1.002.445/DF; REsp 2.157.400/RS); na peça, usar o segundo fundamento (prefixação da sucumbência, que só o juiz fixa). A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (revisional contra financeira, comissão de permanência cumulada e honorários extrajudiciais); o parágrafo final do voto traz erro material ("desprovimento do recurso interposto pelo autor, a fim de manter a improcedência"), em desacordo com a fundamentação, a ementa e a sentença de parcial procedência que foi mantida. Publicação igual à data do julgamento, conforme o portal. Correções na ementa: as quebras de linha do portal foram unidas e inserido um espaço em "CONTRATO–"; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Bandeirantes).

ementa:
> APELAÇÃO CÍVEL – AÇÃO REVISIONAL DE CONTRATO – COMISSÃO DE PERMANÊNCIA AFASTADA EM SENTENÇA POR ABUSIVIDADE – MANUTENÇÃO – IMPOSSIBILIDADE DE CUMULAÇÃO COM DEMAIS ENCARGOS REMUNERATÓRIOS OU MORATÓRIOS, SOB PENA DE BIS IN IDEM - CLÁUSULA QUE POSSIBILITA A COBRANÇA DE HONORÁRIOS EXTRAJUDICIAIS – ABUSIVIDADE – AUSÊNCIA DE RECIPROCIDADE EM FAVOR DO CONSUMIDOR – ARTIGO 51, XII DO CDC – VERBA DE NATUREZA SUCUMBENCIAL - REDAÇÃO INEQUÍVOCA DA RESPECTIVA CLÁUSULA – PRERROGATIVA EXCLUSIVA DO PODER JUDICIÁRIO - MANUTENÇÃO DO AFASTAMENTO - RECURSO CONHECIDO E DESPROVIDO.

## R33 — Encargo com base de cálculo indeterminável pelo devedor

Tese: É inexigível o encargo cujo valor ou base de cálculo não pode ser apurado pelo devedor a partir do próprio instrumento — como a comissão ou encargo de concessão de garantia (CCG do FGO, ECG do FGI-PEAC) ou a tarifa remetidos a fator ou tabela externa, sem valor na cédula e fora do CET declarado —, por violar o dever de informação (CDC, arts. 6º, III, e 52; Lei 10.931/2004, art. 28, § 2º, I) e a determinabilidade do objeto (CC, art. 104, II; Tema 958/STJ, tese 2.1, por analogia); cabe à instituição exibir a memória de apuração e, não o fazendo, restituir o valor cobrado.

Regra sem precedente consolidado: um acórdão de Câmara do TJPR decide exatamente a hipótese; no STJ só há o limite (o repasse da comissão é lícito se expressamente pactuado). Ver o relatório.

### STJ · REsp 1.848.714/PR
- regras: R33
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.848.714/PR
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2022-11-29
- publicacao: 2022-12-09
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/1730644817
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva: o repasse ao tomador da comissão de concessão de garantia (CCG) do FGO é lícito "desde que expressamente pactuado" (Lei 12.087/2009, art. 9º, § 3º); a petição não deve atacar a existência do encargo, mas a falta de valor ou de critério apurável no próprio instrumento — ponto que o STJ não examinou.
- observacao: Recurso da CEF provido para reformar acórdão do TRF4 que declarava nula, em si, a cláusula de CCG. O voto transcreve o § 3º do art. 9º da Lei 12.087/2009 na redação da Lei 14.042/2020 ("seu custo poderá ser repassado ao tomador do crédito, nos termos dos regulamentos de operações dos fundos"). Reafirmado pela Quarta Turma no AREsp 2.830.378/PR (j. 09/02/2026, origem TJPR, Súmulas 5 e 7). DJe de 9/12/2022, conforme a citação deste acórdão no AREsp 2.830.378/PR e a data da lista de resultados do Jusbrasil. Ementa copiada da seção Ementa da página, igual à do inteiro teor.

ementa:
> RECURSO ESPECIAL. DIREITO BANCÁRIO. EMBARGOS À EXECUÇÃO. CONTRATO DE FINANCIAMENTO. FUNDO DE GARANTIA DE OPERAÇÕES (FGO). COMISSÃO DE CONCESSÃO DE GARANTIA (CCG). TOMADOR. REPASSE. POSSIBILIDADE. LEI Nº 12.087/2009. PREVISÃO LEGAL EXPRESSA.
> 1. Recurso especial interposto contra acórdão publicado na vigência do Código de Processo Civil de 2015 (Enunciados Administrativos nºs 2 e 3/STJ).
> 2. Nos contratos de financiamento em que a garantia é complementada pelo Fundo de Garantia de Operações (FGO), a Comissão de Concessão de Garantia (CCG) pode ser repassada ao tomador do empréstimo, desde que expressamente pactuada.
> 3. Recurso especial provido.

### TJPR · Apelação Cível 0002802-54.2017.8.16.0001
- regras: R33
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002802-54.2017.8.16.0001
- orgao: 14ª Câmara Cível
- relator: Des.ª Josely Dittrich Ribas
- julgamento: 2026-10-05
- publicacao: 2026-10-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037784491/Ac%C3%B3rd%C3%A3o-0002802-54.2017.8.16.0001
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Caso-modelo da regra: a cédula previa a CCG do FGO só por remissão a um "fator K" de tabela divulgada no site do banco, sem o valor no quadro da operação; a Câmara declarou o encargo inexigível e manteve a restituição, porque a falta de informação do valor e do critério de apuração viola os arts. 6º, III, e 52 do CDC e o art. 28 da Lei 10.931/2004, e a memória de cálculo unilateral da execução não supre a omissão.
- observacao: Embargos à execução de cédula de crédito bancário de 2015; apelo do banco desprovido (corrigido só erro material na sucumbência). O voto reconhece que a CCG é válida em abstrato (Lei 12.087/2009) e que a própria Câmara já a admitiu quando expressamente pactuada (0034401-45.2016 e 0026391-07.2019, citados na ementa, ambos contrários ao tomador); o que a afastou foi a indeterminação do valor no título: "a remissão à obtenção de informações externas à cédula de crédito [...] reforça a deficiência informacional, especialmente porque o contrato não indicou o valor da comissão, tampouco forneceu elementos suficientes para sua imediata apuração". É CCG do FGO, não ECG do FGI-PEAC: usar por analogia no PEAC. O fundamento principal é o CDC; em tomador pessoa jurídica sem relação de consumo, apoiar-se também no art. 28, § 2º, I, da Lei 10.931/2004, citado no voto. Correções na ementa: nenhuma no texto (só a divisão das linhas). Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E DIREITO DO CONSUMIDOR. EMBARGOS À EXECUÇÃO. COBRANÇA ABUSIVA DE COMISSÃO DE CONCESSÃO DE GARANTIA (CCG) E DIREITO À INFORMAÇÃO DO CONSUMIDOR. RECURSO DE APELAÇÃO DESPROVIDO.
> I. CASO EM EXAME
> 1. Apelação cível interposta pelo embargado contra sentença que julgou parcialmente procedentes os pedidos iniciais, reconhecendo a abusividade da cobrança da Comissão de Concessão de Garantia (CCG) na cédula de crédito bancário em execução, determinando a restituição dos valores pagos, acrescidos de juros e correção monetária, e estabelecendo a distribuição proporcional das custas e honorários entre as partes.
> II. QUESTÃO EM DISCUSSÃO
> 2. A questão em discussão consiste em verificar se: (i) a cobrança da Comissão de Concessão de Garantia (CCG) prevista na cédula de crédito bancário é abusiva, diante da ausência de informações claras a respeito da origem, valor e finalidade do encargo; e (ii) é caso de redistribuição do ônus sucumbencial entre as partes, com aplicação do princípio da causalidade.
> III. RAZÕES DE DECIDIR
> 3.1. A cobrança da Comissão de Concessão de Garantia (CCG), embora admitida pelo ordenamento jurídico, pressupõe informação clara e adequada acerca do valor do encargo e dos critérios empregados em sua apuração.
> 3.2. O título de crédito não atendeu aos requisitos legais de clareza e transparência exigidos pelo art. 52 do CDC e pela Lei nº 10.931/2004, especialmente quanto à demonstração clara da finalidade do encargo e forma de apuração do valor correspondente.
> 3.3. A memória de cálculo que instruiu a execução, embora discrimine o montante cobrado, não demonstra os elementos considerados nem a operação realizada para sua obtenção.
> 3.4. A deficiência informacional viola os arts. 6º, III, e 52 do Código de Defesa do Consumidor e impede a exigência do encargo no caso concreto.
> 3.5. A obtenção de êxito relevante quanto a um dos pedidos formulados nos embargos caracteriza sucumbência recíproca e afasta a aplicação exclusiva do princípio da causalidade.
> IV. DISPOSITIVO
> 4. Apelação cível conhecida e desprovida.
> _________
> Dispositivos relevantes citados: CDC, art. 6º, III; Lei nº 10.931/2004, arts. 26, 28, §§ 1º e 2º; Lei nº 12.087/2009; CPC, arts. 85, §§ 2º e 11.
> Jurisprudência relevante citada: TJPR, Apelação Cível 0034401-45.2016.8.16.0001, Rel. Des. Francisco Eduardo Gonzaga de Oliveira, 14ª Câmara Cível, j. 24.03.2026; TJPR, Apelação Cível 0026391-07.2019.8.16.0001, Rel. Des. Hamilton Rafael Marins Schwartz, 14ª Câmara Cível, j. 14.04.2025.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Ressalva da peça, com saída processual: a Tabela Price não gera juros sobre juros por si só, mas a existência de anatocismo é questão de fato e exige perícia contábil; indeferi-la é cerceamento de defesa.
- observacao: Dados antes [CONFERIR] agora conferidos: relatora Min. Maria Isabel Gallotti, Quarta Turma, sessão virtual de 07/04/2026 a 13/04/2026 (julgamento em 13/04/2026), unânime; votaram Antonio Carlos Ferreira, Luís Carlos Gambogi (Des. convocado TJMG), Noronha e Raul Araújo. Publicação pela data do Jusbrasil (16/04/2026). Recurso da construtora desprovido: o STJ manteve a anulação da sentença de improcedência liminar e o retorno para perícia. A ementa fala do SFH, mas o contrato do caso é de compra e venda com alienação fiduciária feita com construtora fora do SFN/SFH/SFI; no voto, a relatora cita o Tema 572/STJ e reafirma, com AgInt nos EDcl no REsp 2.060.160/RN, AgInt no REsp 1.905.596/PR e AgInt no AREsp 2.519.062/DF, que construtora fora do SFI não pode cobrar juros capitalizados (aproveitável na R35, mas esse ponto não está na ementa). Aqui há duas entradas ADV na R34 (acima do teto de 1 da regra de seleção) porque o pedido incluía conferir os dois REsp.

ementa:
> RECURSO ESPECIAL. TABELA PRICE. ANATOCISMO. PERÍCIA CONTÁBIL NECESSÁRIA. ANULAÇÃO DA SENTENÇA PARA REALIZAÇÃO DE PERÍCIA MANTIDA.
> 1. A utilização do Sistema Francês de Amortização, Tabela Price, para o cálculo das prestações não é ilegal e não enseja, por si só, a incidência de juros sobre juros.
> 2. Esta Corte, no julgamento de recurso submetido ao regime do art. 543-C do CPC/1973, assentou a impossibilidade de o STJ analisar a existência de capitalização de juros com a utilização da Tabela Price, em razão da incidência das Súmulas n. 5 e 7 do STJ (REsp n. 1.070.297/PR, Relator Ministro LUIS FELIPE SALOMÃO, SEGUNDA SEÇÃO, julgado em 9/9/2009, DJe 18/9/2009).
> 3. Em se verificando que matérias de fato ou eminentemente técnicas foram tratadas como exclusivamente de direito, reconhece- se o cerceamento, para que seja realizada a prova pericial. Decisão do Tribunal de origem em consonância com o entendimento do STJ.
> 4. Recurso especial conhecido e não provido.

### TJPR · Apelação Cível 0009938-53.2025.8.16.0056
- regras: R34
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0009938-53.2025.8.16.0056
- orgao: 13ª Câmara Cível
- relator: Des. José Camacho Santos
- julgamento: 2026-02-27
- publicacao: 2026-03-02
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035696271/Ac%C3%B3rd%C3%A3o-0009938-53.2025.8.16.0056
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em financiamento do SFH de 31/08/1995 com instituição financeira, o TJPR mantém o expurgo da capitalização de juros apurada por perícia (incorporação de juros ao saldo devedor na Tabela Price), por ser vedada em qualquer periodicidade antes da Lei 11.977/2009 (REsp 1.070.297/PR e REsp 1.124.552/RS).
- observacao: Apelação da instituição financeira parcialmente conhecida e, quanto à capitalização, desprovida; de ofício, anulada parcialmente a sentença (ultra petita, quanto à TR) e alterados os consectários legais (IPCA e Selic). A Tabela Price não prova capitalização por si; o acórdão depende do laudo, que constatou incorporação de juros ao saldo devedor. A íntegra do portal não cita o CNJ da apelação (cita o da ação de origem), mas o relatório e o voto descrevem o mesmo caso da ementa (apelação do banco contra sentença de procedência em revisional de SFH, contrato de 31/08/1995, sentença com TR e capitalização). Ementa sem correções. Fonte: portal de jurisprudência do TJPR (comarca de Cambé).

ementa:
> DIREITO CIVIL E DIREITO PROCESSUAL CIVIL. APELO. REVISÃO DE CONTRATO BANCÁRIO DO SFH. SENTENÇA ULTRA PETITA, RECONHECIMENTO DA PARCIAL NULIDADE DA SENTENÇA, EX OFFICIO. RECURSO PARCIALMENTE CONHECIDO E, NESSA EXTENSÃO, NÃO PROVIDO.
> I. CASO EM EXAME:I.1. Sentença na qual se julgara procedente a Revisional aforada pela parte ativa, reconhecendo a abusividade da capitalização dos juros e da incidência da TR. Parte apelante que, inconformada, interpusera apelação, arguindo nulidade da sentença por dita falta de fundamentação e ante alegado cerceamento processual, além de alegar a legalidade da tabela Price e a validade dos encargos contratuais.
> II. QUESTÃO EM DISCUSSÃO:II.1. Consiste em saber se houvera, ou não, abusividade dos encargos contratuais aplicadas pela Instituição financeira, e se na sentença (em que se ocorrera isto ou aquilo) padeceria, ou não, de nulidade.
> III. RAZÕES DE DECIDIR:III.1. Sentença ultra petita. Declaração de parcial nulidade da sentença, porque a parte autora não pedira, na inicial, nulidade da TR, como índice de correção monetária.
> III.2. Constatação da ausência de interesse recursal quanto às teses relativas aos juros remuneratórios e à repetição de indébito.
> III.3. Ausência de nulidade da sentença por falta de fundamentação ou cerceamento. Técnica da fundamentação por referência (= per relationem), permitida, desde que o Juiz, ao reproduzir trechos de documento e/ou parecer como razões de decidir, enfrente, e ainda que de forma sucinta, as novas questões relevantes ao julgamento do processo, dispensada análise pormenorizada de cada qual das alegações e/ou provas.
> III.4. No CDC, norma de ordem pública e interesse social, autoriza-se mitigação da força obrigatória dos contratos sempre que necessário a assegurar-se a proteção do Consumidor. Portanto, mesmo contratos celebrados sob a égide do PCR, podem ser objeto de revisão judicial, caso haja afronta aos princípios da boa-fé, transparência e equilíbrio contratual.
> III.5. Capitalização abusiva dos juros. Nos contratos abrangidos pelo SFH, em especial, nos celebrados anteriormente ao advento da Lei n. 11.977/09 (na qual fora inserido o art. 15-A, à Lei n. 380/64), como neste caso, em que o contrato fora subscrito aos 31.8.95, o entendimento adotado no STJ, por ocasião dos julgamentos dos RESP’S repetitivos ns. 1070297 / PR e 1124552 / RS, o fora pela impossibilidade de capitalização dos juros e, ainda, pela necessidade de produção de prova técnica a aferir-se a existência, ou não, de capitalização dos juros.
> III.6. Modificação, de ofício, da sentença, para que os índices de correção monetária e dos juros da mora se deem segundo o contido na redação da Lei n. 14.905/94, dada aos arts. 389 e 406, do CC.
> III.7. Ônus sucumbencial à razão de 50% (cinquenta por cento) a cargo de cada parte, e arbitrados os honorários advocatícios em 10% (dez por cento) do valor da condenação atualizado.
> III.8. Honorários advocatícios recursais arbitrados em 02% (dois por cento), de modo a majorar-se a verba advocatícia sucumbencial para 12% (doze por cento) do valor da responsabilização devida ao Patrona da parte ativa.
> IV. DISPOSITIVO E TESE:IV.1. Apelação parcialmente conhecida, mas não provida.
> Tese de julgamento: a capitalização de juros nos contratos celebrados no âmbito do SFH não era admitida até a edição da Lei n. 11.977/09, na qual se incluíra o art. 15-A, à Lei 4.380/64, porém, a partir daí, passara a admitir a sua pactuação em periodicidade mensal. Destarte, antes dessa norma legal, era vedada a capitalização dos juros em qualquer periodicidade nos contratos de financiamento celebrados no âmbito do SFH, como ocorrera no caso._________Dispositivos relevantes citados: art. 93, inc. IX, da CF, 389 e 406, do CC, 141 e 492, do CPC.
> Jurisprudência relevante citada: STJ, RESP n. 2.150.218 / MA, Rel. Min. LUIS FELIPE SALOMÃO, Corte Especial, julgado em 20.8.25, RESP n. 1114049 / PE, Rel. Min. LUIS FELIPE SALOMÃO, 4ª T., julgado em 7.4.11, publicado no DJE de 29.4.1, REsp 1070297 / PR, Rel. Min. LUIS FELIPE SALOMÃO, 2ª Seção, julgado em 9.9.09, REsp 1124552 / RS, Rel. Min. LUIS FELIPE SALOMÃO, Corte Especial, julgado em 3.12.14, STJ, 4ª T., AGRG no RESP n. 1242968 / PB, Rel. Min. MARCO BUZZI, julgado em 3.9.15, TJPR, 15ª CC, 0030068-64.2023.8.16.0014, Londrina, Rel. Des. JUCIMAR NOVOCHADLO, julgado de 21.9.24, TJPR, 15ª CC, 0005226-45.2022.8.16.0017, Maringá, Relª. Desª. LUCIANE BORTOLETO, julgado de 14.9.24, TJPR, 13ª CC, n. 0041109-23.2017.8.16.0019, AC, Rel. hoje Des. Substituto, RODRIGO FERNANDES LIMA DALLEDONE, julgado de 14.10.19.
> Resumo em linguagem acessível: nesta Corte, decidira-se que a apelação não poderia ser integralmente conhecida, já que a parte recorrente impugnara temas dos quais não lhe foram prejudiciais. Ainda, se reconhecera, ex officio, que a sentença teria ocorrido em parcial nulidade, pois julgara tema não invocado pela parte autora (em relação à análise da Taxa Referencial). No mais, o Tribunal mantivera a sentença quanto ao reconhecimento de abusividade na cobrança da capitalização dos juros.

### TJPR · Apelação Cível 0030759-35.2014.8.16.0001
- regras: R34
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0030759-35.2014.8.16.0001
- orgao: 18ª Câmara Cível
- relator: Des. Luiz Henrique Miranda
- julgamento: 2021-07-21
- publicacao: 2021-07-21
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000017849421/Ac%C3%B3rd%C3%A3o-0030759-35.2014.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Mútuo habitacional do SFH firmado em 05/06/2008, antes da Lei 11.977/2009: a capitalização de juros é vedada e o TJPR mantém o expurgo, apurado por perícia (juros computados sobre a parcela de juros das prestações não pagas incorporadas ao saldo devedor).
- observacao: Apelações da instituição financeira e da autora não providas: mantida a sentença que afastou a capitalização e determinou a restituição simples, com sucumbência recíproca e honorários majorados a 13%. A ementa ressalva que a Tabela Price, por si só, não gera capitalização; o anatocismo veio da incorporação de prestações vencidas ao saldo devedor, como apurou o laudo. Julgado de 2021, fora da faixa preferida (2023 em diante). A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (revisão de mútuo habitacional com alienação fiduciária, 18ª Vara Cível de Curitiba, recursos de ambas as partes). A ementa traz uma frase final solta, fora da numeração, como no original. A ementa vem em texto corrido, como no original. Ementa sem correções. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE MÚTUO HABITACIONAL GARANTIDO POR ALIENAÇÃO FIDUCIÁRIA. CONTRATO VINCULADO AO SISTEMA FINANCEIRO HABITACIONAL – SFH. PRETENSÃO PARCIALMENTE ACOLHIDA EM 1º GRAU, PARA O FIM DE PROIBIR A CAPITALIZAÇÃO DOS JUROS REMUNERATÓRIOS. SENTENÇA CORRETA, NO PONTO, UMA VEZ QUE O CONTRATO FOI FIRMADO ANTES DA LEI Nº 11.977/2009. ENTENDIMENTO DO STJ. NECESSIDADE DE ESCLARECER, CONTUDO, QUE A PRÁTICA REPROVÁVEL NÃO DECORREU, NO CASO CONCRETO, DA UTILIZAÇÃO DO SISTEMA FRANCÊS DE AMORTIZAÇÃO (TABELA PRICE) PARA A DEFINIÇÃO DO VALOR DAS PRESTAÇÕES, E SIM, CONFORME FICOU ESCLARECIDO NO LAUDO PERICIAL, DA INCORPORAÇÃO DE ALGUMAS PRESTAÇÕES NÃO PAGAS NO VENCIMENTO AO SALDO DEVEDOR, FAZENDO COM QUE SOBRE A PARCELA DOS JUROS NELAS INCORPORADAS FOSSEM COMPUTADOS JUROS ADICIONAIS.
> ÔNUS SUCUMBENCIAIS ADEQUADAMENTE DISTRIBUÍDOS ENTRE OS LITIGANTES. AUTORA QUE SAGROU-SE VITORIOSA NA QUESTÃO DA CAPITALIZAÇÃO, SUCUMBINDO, PORÉM, NA PRETENSÃO DE OBTER A NÃO APLICAÇÃO DA TABELA PRICE E, POR VIAS TRANSVERSAS, A REDUÇÃO DA TAXA DOS JUROS. RECURSOS CONHECIDOS E NÃO PROVIDOS.O uso do sistema francês de amortização (SFA), também conhecido como Tabela Price, não acarreta, de per si, a capitalização de juros que é reprovada pelo artigo 4º do Decreto 22.626/1933, já que se trata de técnica de composição de juros vencíveis que não provoca a incidência de novos juros sobre juros vencidos.

### TJPR · Apelação Cível 0006880-67.2026.8.16.0004
- regras: R34
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0006880-67.2026.8.16.0004
- orgao: 19ª Câmara Cível
- relator: Andrei de Oliveira Rech
- julgamento: 2026-10-26
- publicacao: 2026-10-26
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000039981321/Ac%C3%B3rd%C3%A3o-0006880-67.2026.8.16.0004
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Contrato do SFH anterior à Lei 11.977/2009, amortizado pela Tabela Price: a perícia constatou capitalização mensal e o TJPR mantém o seu expurgo (Temas 48 e 572/STJ), com a ressalva de que a Price, por si só, não implica anatocismo.
- observacao: Apelação da companhia de habitação mutuante parcialmente provida apenas para redistribuir a sucumbência (70% autores, 30% ré); o afastamento da capitalização foi mantido. ATENÇÃO: a ré é companhia de habitação popular (agente do SFH), não banco; conferir se serve ao caso antes de citar. O portal não informa o cargo do relator. Após o expurgo, o laudo apurou a quitação na parcela 160 de 240. A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (apelação da companhia de habitação contra sentença que afastou a Tabela Price, comarca de Curitiba). A ementa vem em texto corrido, como no original. Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> Direito civil e processual civil. Apelação cível. Ação revisional de contrato vinculado ao Sistema Financeiro da Habitação. Tabela Price. Capitalização mensal de juros constatada por prova pericial. Contrato anterior à Lei nº 11.977/2009. Redistribuição proporcional dos ônus sucumbenciais. Recurso conhecido e parcialmente provido. I. CASO EM EXAME Apelação cível interposta pela COHAB-CT contra sentença que julgou parcialmente procedente ação revisional de contrato declarar a ilegalidade da cláusula que prevê a amortização pela Tabela Price e, consequentemente, afastar a capitalização de juros. A apelante sustenta a ausência dos pressupostos da revisão por onerosidade excessiva, a inexistência de capitalização ilegal e, subsidiariamente, sua sucumbência mínima. Em contrarrazões, os autores suscitam preclusão pela ausência de impugnação oportuna ao laudo pericial. II. QUESTÕES EM DISCUSSÃO As questões em discussão são 4 (quatro), a saber: (i) definir se a ausência de impugnação oportuna ao laudo pericial impede o exame das teses jurídicas deduzidas no recurso; (ii) verificar se a revisão do contrato depende da demonstração dos pressupostos da onerosidade excessiva previstos nos arts. 478 a 480 do Código Civil; (iii) examinar se deve ser mantido o afastamento da capitalização de juros no contrato vinculado ao Sistema Financeiro da Habitação; e (iv) determinar se a distribuição dos ônus sucumbenciais deve ser modificada. III. RAZÕES DE DECIDIR III.i. Rejeita-se a preliminar de preclusão, pois a ausência de impugnação oportuna ao laudo impede a posterior formulação de objeções de natureza técnica quanto aos critérios, à metodologia e aos cálculos periciais, mas não obsta o exame das teses jurídicas decorrentes da prova produzida.III.ii. A sentença realizou controle de legalidade de encargo contratual à luz do Código de Defesa do Consumidor, e não revisão fundada na teoria da imprevisão. A declaração de abusividade prescinde, portanto, da demonstração dos pressupostos dos arts. 478 a 480 do Código Civil, observado o disposto nos arts. 6º, V, e 51, IV e § 1º, do CDC. III.iii. A Tabela Price não implica, por si só, anatocismo, mas a perícia constatou, no caso concreto, capitalização mensal de juros e apurou que, após seu expurgo, o saldo devedor se extinguiria na parcela 160, antes do prazo contratual de 240 meses. Não infirmada a conclusão técnica, mantém-se o afastamento da capitalização no contrato firmado antes da Lei nº 11.977/2009, conforme os Temas 48 e 572 do STJ. III.iv. O acolhimento do pedido de afastamento da capitalização de juros exclui a hipótese de sucumbência mínima da ré, mas os autores decaíram dos demais pedidos formulados na inicial, impondo-se a redistribuição proporcional dos ônus sucumbenciais, nos termos do art. 86, caput, do CPC, na proporção de 70% para os autores e 30% para a ré. Mantidos os honorários em 10% sobre o proveito econômico e a suspensão da exigibilidade em razão da gratuidade da justiça. III.v. Incabível majoração dos honorários em grau recursal diante do parcial provimento do recurso. IV. DISPOSITIVO E TESE Recurso de apelação conhecido e parcialmente provido, apenas para redistribuir os ônus sucumbenciais, atribuindo aos autores 70% e à ré 30% das custas, despesas processuais e honorários advocatícios fixados na sentença, mantida a decisão recorrida nos demais termos e suspensa a exigibilidade na forma do art. 98, § 3º, do CPC. Tese de julgamento: “1. A ausência de impugnação oportuna ao laudo pericial não impede o exame, em grau recursal, das consequências jurídicas decorrentes da prova produzida. 2. O controle de legalidade de cláusula contratual abusiva não se confunde com a revisão fundada na teoria da imprevisão, sendo inaplicáveis, para esse fim, os pressupostos dos arts. 478 a 480 do Código Civil. 3. A utilização da Tabela Price não implica, por si só, capitalização de juros, mas esta deve ser afastada em contrato do Sistema Financeiro da Habitação anterior à Lei nº 11.977/2009 quando constatada concretamente por prova pericial. 4. O acolhimento de pedido com relevante repercussão econômica afasta a sucumbência mínima da parte ré, sem impedir a distribuição proporcional dos ônus sucumbenciais diante da rejeição dos demais pedidos.”Dispositivos relevantes citados: CC, arts. 478 a 480; CDC, arts. 6º, V, e 51, IV e § 1º; CPC, arts. 85, §§ 2º e 11, 86, caput e parágrafo único, e 98, § 3º; Lei nº 4.380/1964, art. 15-A.Jurisprudência relevante citada: STJ, Tema Repetitivo nº 48 (REsp nº 1.070.297/PR), Rel. Min. Luis Felipe Salomão, Segunda Seção, j. 09.09.2009; STJ, Tema Repetitivo nº 572 (REsp nº 1.124.552/RS), Rel. Min. Luis Felipe Salomão, Corte Especial; STJ, Terceira Turma, AgInt no AREsp nº 1.349.182/RJ, Rel. Min. Moura Ribeiro, j. 10.06.2019, DJe 12.06.2019; STJ, Segunda Turma, REsp nº 1.804.904/SP, Rel. Min. Herman Benjamin, j. 16.05.2019, DJe 30.05.2019; TJPR, 19ª Câmara Cível, Apelação Cível nº 0050174-47.2023.8.16.0014, Rel. Rotoli de Macedo, j. 18.09.2023.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Contrato de compra e venda de imóvel com instituição fora do SFI não admite juros capitalizados em periodicidade inferior à anual.
- observacao: Dados antes [CONFERIR] agora conferidos: relator Min. Raul Araújo, Quarta Turma, sessão virtual de 22/04/2025 a 28/04/2025 (julgamento em 28/04/2025), unânime; votaram Noronha, Gallotti, Antonio Carlos Ferreira e Buzzi. Publicação pela data do Jusbrasil. O relator reconsiderou decisão monocrática anterior que dera provimento ao recurso da incorporadora e negou provimento ao recurso especial dela, aplicando a Súmula 83/STJ; o acórdão de origem (TJMG, IRDR Tema 56) admitia só a capitalização anual. O voto transcreve a ementa do REsp 2.086.650/MG (Nancy Andrighi, 3ª Turma), que é o leading case da 3ª Turma, mas este não entra como entrada própria.

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
- verificado_em: 2026-10-29
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
- relator: Des. Carlos Roberto da Silva (conferido em 29/10/2026 no rodapé do acórdão exibido pelo Jusbrasil; o texto do fetch omite o relator)
- julgamento: 2025-05-29
- publicacao: 2025-05-29
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/tj-sc/3944222624
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Incorporadora fora do SFI não pode cobrar juros capitalizados; a Tabela Price que capitaliza, constatada por perícia contábil, é nula e as parcelas são recalculadas na liquidação.
- observacao: Complementa os três acórdãos do TJPR desta tese: aqui a perícia constatou a capitalização e a sentença mandou recalcular as parcelas. Publicação pela data do Jusbrasil (29/05/2025). O texto do fetch também traz a ata da sessão virtual de 29/05/2025 (7ª Câmara de Direito Civil, unânime). Contrato de promessa de compra e venda de apartamento em construção com incorporadora (SPE), não com banco.

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE REVISÃO DE CONTRATO. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA DO AUTOR. PROMESSA DE COMPRA E VENDA DE APARTAMENTO EM CONSTRUÇÃO. TESE EXORDIAL DE CAPITALIZAÇÃO DE JUROS. DEFENDIDA A COBRANÇA ABUSIVA DE ENCARGOS FINANCEIROS. ACOLHIMENTO. RÉ NÃO INTEGRANTE DO SISTEMA FINANCEIRO IMOBILIÁRIO (SFI). IMPOSSIBILIDADE DE UTILIZAÇÃO DAS PRERROGATIVAS PREVISTAS NA LEI N. 9.514/1997. CAPITALIZAÇÃO DE JUROS CONSTATADA POR PERÍCIA CONTÁBIL. PRÁTICA ABUSIVA EVIDENCIADA. APURAÇÃO DO VALOR DE CADA PARCELA A SER FEITA EM FASE DE LIQUIDAÇÃO DE SENTENÇA. INVERSÃO DOS ÔNUS SUCUMBENCIAIS. "'[...] em se tratando de contratos de compra e venda de imóvel, somente é permitida a capitalização dos juros quando o financiamento for pactuado com entidade bancária que respeite as normas do Sistema Financeiro Imobiliário, não se enquadrando nessas hipóteses as construtoras de imóveis, as quais devem aplicar os juros na forma simples' (Apelação Cível n. 2014.065045-1, da Capital, rel. Des. Saul Steil, j. 16-12-2014)" (TJSC, Apelação n. 5004719-75.2020.8.24.0007, rel. Des. José Agenor de Aragão, Quarta Câmara de Direito Civil, j. 3-4-2025). RECURSO CONHECIDO E PROVIDO.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: A loteadora não se equipara a instituição financeira e não pode capitalizar juros em periodicidade inferior à anual (MP 2.170-36/2001, art. 5º) no financiamento direto de imóvel; a perícia constatou a capitalização pela Tabela Price.
- observacao: Ação de resolução contratual por culpa da vendedora; o ponto da capitalização é o item 1 da ementa. Fonte: portal de jurisprudência do TJPR (comarca de Maringá). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Em promessa de compra e venda de lote com financiamento da vendedora, o TJPR afirma a impossibilidade da capitalização mensal e reconhece, pela perícia, juros capitalizados sem previsão contratual.
- observacao: Favorável só na tese: o comprador estava em mora e havia saldo devedor, por isso não houve repetição nem descaracterização da mora, e a multa compensatória foi reduzida a 10%. Fonte: portal de jurisprudência do TJPR (comarca de Cascavel). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Empresa que não integra o Sistema Financeiro Imobiliário não pode capitalizar juros; havendo indício de Tabela Price, a perícia contábil é indispensável e o julgamento sem ela é cerceamento de defesa (Tema 572/STJ).
- observacao: Sentença cassada para a perícia; o mérito não foi julgado. Serve à vedação e ao pedido de perícia em "Das provas". Fonte: portal de jurisprudência do TJPR (comarca de Curitiba). Conferido no portal do TJPR em 29/10/2026: ementa e dados batem.

ementa:
> APELAÇÃO CÍVEL. AÇÃO DE REVISÃO CONTRATUAL C/C REPETIÇÃO DE INDÉBITO. NEGÓCIO PARTICULAR DE COMPRA E VENDA DE IMÓVEL URBANO. SENTENÇA DE IMPROCEDÊNCIA. INSURGÊNCIA RECURSAL DOS AUTORES (PROMISSÁRIOS COMPRADORES). PRELIMINAR DE CERCEAMENTO DE DEFESA PELO JULGAMENTO ANTECIPADO DA LIDE SEM A PRODUÇÃO DE PROVA TÉCNICA. Acolhimento. Matéria de fato relevante acerca da cobrança de juros remuneratórios e sua capitalização. Autores que assinaram apenas proposta de compra em que não eram previstos juros. Instrumentos contratuais outros, elaborados pela empresa ré, que não foram assinados. Relação típica de consumo. Documentos emitidos pela promitente vendedora sobre os pagamentos feitos que sinalizam para aplicação da Tabela Price como método de amortização da dívida e eventual capitalização. Prova pericial contábil que foi especificamente requerida por ambas as partes. Empresa ré que não integra o Sistema Financeiro Imobiliário. Capitalização de juros vedada na espécie, o que justifica a realização de perícia para sua confirmação e/ou afastamento. Tema Repetitivo nº 572 do Superior Tribunal de Justiça. Cassação da sentença e retorno dos autos à origem para regular instrução probatória, com a realização da perícia e a prévia definição quanto a extensão da inversão do ônus da prova incidentemente decretada. Demais questões prejudicadas. RECURSO CONHECIDO E PROVIDO.

## R36 — SFH: amortização negativa — juros impagos incorporados ao saldo

Tese: Nos contratos do SFH anteriores à Lei 11.977/2009, quando a prestação não cobre sequer os juros do mês (amortização negativa), os juros não pagos não podem ser incorporados ao saldo devedor para render novos juros: devem ser lançados em conta separada, sujeita apenas à correção monetária, e o anatocismo apurado deve ser expurgado do saldo e restituído.

### STJ · REsp 1.095.852/PR
- regras: R36
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.095.852/PR
- orgao: Segunda Seção
- relator: Min. Maria Isabel Gallotti
- julgamento: 2012-03-14
- publicacao: 2012-03-19
- precedente_qualificado: não (Segunda Seção; interpreta o repetitivo REsp 1.070.297/PR)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/21428658
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Leading case da Segunda Seção: no SFH, se a prestação não cobre sequer os juros, os juros vencidos e não pagos vão para conta separada, sujeita apenas à correção monetária, para evitar o anatocismo; o voto determina a criação dessa conta para preservar a vedação do Decreto 22.626/1933.
- observacao: LIMITE no mesmo acórdão: o recurso da instituição financeira foi provido para (i) imputar os pagamentos primeiro aos juros (CC, art. 354; REsp 1.194.402/RS, repetitivo) e (ii) permitir a capitalização ANUAL dos juros vencidos e não pagos, independentemente de pactuação, em contrato anterior à Lei 11.977/2009; o TRF4 havia mandado desconsiderar os juros impagos, solução afastada. Há tensão posterior: o REsp 2.186.454/SP (Quarta Turma, 2026) fala em conta separada "com atualização apenas monetária, vedada a cobrança de novos juros", e o TRF4 (AC 5048665-28.2015.4.04.7100) recusou a capitalização anual pedida pelo agente financeiro. Unânime. DJe de 19/03/2012, indicado no inteiro teor. Correção na ementa: til restaurado em "HABITAÇÃO", "CAPITALIZAÇÃO" e "IMPUTAÇÃO" (o inteiro teor grafa "HABITAÇAO" etc.); nenhuma palavra alterada.

ementa:
> RECURSO ESPECIAL. SISTEMA FINANCEIRO DA HABITAÇÃO. SFH. CAPITALIZAÇÃO ANUAL DE JUROS. POSSIBILIDADE. ENCARGOS MENSAIS. IMPUTAÇÃO DO PAGAMENTO. ART. 354 CC 2002. ART. 993 CC 1916.
> 1. Interpretação do decidido pela 2ª Seção, no Recurso Especial Repetitivo 1.070.297, a propósito de capitalização de juros, no Sistema Financeiro da Habitação.
> 2. Segundo o acórdão no Recurso Repetitivo 1.070.297, para os contratos celebrados no âmbito do Sistema Financeiro da Habitação até a entrada em vigor da Lei 11.977/2009 não havia regra especial a propósito da capitalização de juros, de modo que incidia a restrição da Lei de Usura (Decreto 22.626/33, art. 4º). Assim, para tais contratos, não é válida a capitalização de juros vencidos e não pagos em intervalo inferior a um ano, permitida a capitalização anual, regra geral que independe de pactuação expressa. Ressalva do ponto de vista da Relatora, no sentido da aplicabilidade, no SFH, do art. 5º da MP 2.170-36, permissivo da capitalização mensal, desde que expressamente pactuada.
> 3. No Sistema Financeiro da Habitação, os pagamentos mensais devem ser imputados primeiramente aos juros e depois ao principal, nos termos do disposto no art. 354 Código Civil em vigor (art. 993 Código de 1916). Entendimento consagrado no julgamento, pela Corte Especial, do Recurso Especial nº 1.194.402-RS (Relator Min. Teori Albino Zavascki), submetido ao rito do art. 543-C.
> 4. Se o pagamento mensal não for suficiente para a quitação sequer dos juros, a determinação de lançamento dos juros vencidos e não pagos em conta separada, sujeita apenas à correção monetária, com o fim exclusivo de evitar a prática de anatocismo, encontra apoio na jurisprudência atual do STJ. Precedentes.
> 5. Recurso especial provido.

### STJ · REsp 2.186.454/SP
- regras: R36, R38
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.186.454/SP
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2026-03-02
- publicacao: 2026-03-11
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6806310814
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Acórdão recente que decide as duas teses: (R36) nos períodos de amortização negativa, os juros não pagos vão para planilha separada, com atualização apenas monetária, vedada a cobrança de novos juros; (R38) o CES só pode ser cobrado com expressa previsão contratual, não podendo ser imposto com base em circulares administrativas ou resoluções do extinto BNH.
- observacao: Recurso do mutuante do SFH (entidade pública estadual) provido só para afastar o CDC (contrato de 1988, anterior ao Código); mantidos a exclusão do CES (contrato sem cláusula) e o afastamento da capitalização apurada em perícia. O voto afirma a vedação da capitalização "em qualquer periodicidade" (Súmula 121/STF), em tensão com o REsp 1.095.852/PR (capitalização anual permitida). Sessão virtual de 24/02 a 02/03/2026. Publicação pela data do Jusbrasil (o inteiro teor não traz o DJEN). Ementa sem correções (o item "2 A cobrança", sem ponto, está assim no original).

ementa:
> DIREITO CIVIL. RECURSO ESPECIAL. AÇÃO REVISIONAL DE CONTRATO DE FINANCIAMENTO IMOBILIÁRIO. COEFICIENTE DE EQUIPARAÇÃO SALARIAL (CES). CÓDIGO DE DEFESA DO CONSUMIDOR. CAPITALIZAÇÃO DE JUROS. RECURSO PARCIALMENTE PROVIDO.
> 1. O acórdão recorrido examinou de forma suficiente todas as matérias controvertidas, emitindo pronunciamento fundamentado sobre os pontos essenciais ao deslinde da causa, não havendo omissão ou negativa de prestação jurisdicional.
> 2 A cobrança do Coeficiente de Equiparação Salarial (CES) é admissível na hipótese de expressa previsão contratual, não podendo ser imposta unilateralmente com base em circulares administrativas ou resoluções do extinto BNH.
> 3. O Código de Defesa do Consumidor não se aplica aos contratos regidos pelo Sistema Financeiro da Habitação celebrados antes de sua vigência, em razão do princípio da irretroatividade das leis e da proteção ao ato jurídico perfeito.
> 4. É vedada a capitalização de juros nos contratos regidos pelo Sistema Financeiro da Habitação, ainda que haja previsão contratual expressa, conforme o enunciado da Súmula 121 do Supremo Tribunal Federal.
> 5. Nos períodos de amortização negativa, o valor dos juros não pagos deve ser lançado em planilha separada, com atualização apenas monetária, vedada a cobrança de novos juros sobre o montante, a fim de evitar anatocismo.
> 6. Recurso parcialmente provido, para afastar a aplicação do Código de Defesa do Consumidor ao contrato em questão.

### STJ · REsp 1.476.395/RS
- regras: R36
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.476.395/RS
- orgao: Terceira Turma
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2018-08-14
- publicacao: 2018-10-11
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/3445134702
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: o reconhecimento da amortização negativa não descaracteriza a mora do mutuário, porque a disfunção decorre do próprio sistema da Lei 4.380/1964 (prestação pelo PES e saldo por índice diverso), não de ato abusivo do agente financeiro; não pedir o afastamento da mora só com base na R36.
- observacao: O mesmo acórdão ajuda no mérito: o voto qualifica a reincorporação dos juros não pagos ao saldo como "vedado anatocismo" e, por maioria (vencidos os Ministros Villas Bôas Cueva e Bellizze), nega o recurso da instituição financeira e mantém o recálculo do TRF4 que garante a amortização em cada prestação (item 2.4 da ementa); o recurso dos mutuários foi desprovido por unanimidade. Julgamento concluído em 14/08/2018, após voto-vista; DJe de 11/10/2018, indicado no inteiro teor. Divergência: o TRF4 (AC 5048665-28.2015.4.04.7100, 2023) afastou a mora em caso análogo. Correções na ementa: espaços inseridos em "IMPOSSIBILIDADE.1.1." e "CONSUMIDOR.2.1." e em "NESSAPARTE"; grafias do original mantidas ("inexitindo", "muito vezes", "decádas").

ementa:
> RECURSOS ESPECIAIS DAS DUAS PARTES. CIVIL E PROCESSUAL CIVIL. SISTEMA FINANCEIRO HABITACIONAL.
> I - RECURSO ESPECIAL DOS MUTUÁRIOS. CONTRATO DE FINANCIAMENTO. AMORTIZAÇÃO NEGATIVA. DESCARACTERIZAÇÃO DA MORA. IMPOSSIBILIDADE. 1.1. O reconhecimento, na origem, da amortização negativa não se mostra suficiente para o afastamento da mora do mutuário. A disfunção gerada pelo sistema de amortização decorre da Lei 4.380/64 a estabelecer métodos de correção diversos em relação às prestações e ao saldo devedor, inexitindo, no que respeita, agir abusivo por parte da instituição mutuante a justificar o afastamento da mora dos mutuários.
> 1.2. Demais questões impugnadas no apelo excepcional dos autores obstaculizadas pelos enunciados 282/STF e 7/STJ.
> 1.3. RECURSO ESPECIAL DOS MUTUÁRIOS EM PARTE CONHECIDO E, NESSA PARTE, DESPROVIDO. II - RECURSO ESPECIAL. SISTEMA DE AMORTIZAÇÃO DO SALDO DEVEDOR. INTERPRETAÇÃO CONTIDA NO ACÓRDÃO RECORRIDO QUE SE AMOLDA AO SISTEMA DE FINANCIAMENTO DA HABITAÇÃO, À FUNÇÃO SOCIAL DO CONTRATO E À PROTEÇÃO DO CONSUMIDOR. 2.1. Densidade social do Sistema Financeiro Habitacional presente em vários dos dispositivos da Lei 4.380/64, priorizando a construção de conjuntos habitacionais destinados à população de baixa renda, buscando a eliminação de favelas, mocambos e outras aglomerações em condições sub-humanas de habitação, bem como projetos municipais ou estaduais com oferta de terrenos já urbanizados que permitam o início imediato da construção; projetos de cooperativas e outras formas associativas de construção de casa própria, além daqueles da iniciativa privada voltados à solução de problemas habitacionais e a construção de moradia à população rural.
> 2.2. Fixação, porém, de um sistema de amortização do saldo devedor deficiente, pois, mediante o plano de equivalência salarial, as parcelas do financiamento tinham atualização vinculada aos reajustes dos salários (ou do salário mínimo), sucessivamente congelados ou subdimensionados, submetidos a mal sucedidos planos econômicos, e o saldo devedor era atualizado mediante índices de remuneração da poupança.
> 2.3. Como resultado desse sistema, ao término de longos prazos de amortização (15 a 30 anos), em face da deficiente amortização do saldo devedor, passaram a remanescer insolúveis saldos devedores, muito vezes superiores ao montante dos financiamentos originalmente contratados e do próprio valor dos imóveis adquiridos, exigindo, após o prazo previsto no contrato, o recálculo de prestações, alcançando-se valores incompatíveis com a capacidade financeira dos adquirentes, e a prorrogação do contrato por decádas outras a fio.
> 2.4. A solução ao grave problema criado, adotada pelo acórdão recorrido, no sentido de determinar que sejam os pagamentos recalculados durante todo o contrato e que se garanta a amortização e o pagamento dos juros, amolda-se à função social dos contratos celebrados no âmbito do Sistema Financeiro Habitacional; preserva o mínimo existencial dos mutuários, projetado no direito à habitação, e resguarda o consumidor, garantindo-lhe uma interpretação mais favorável das cláusulas contratuais.
> 2.5. RECURSO ESPECIAL DA CEF DESPROVIDO. 3. RECURSO ESPECIAL DOS MUTUÁRIOS PARCIALMENTE CONHECIDO E, NESSA PARTE, DESPROVIDO E RECURSO ESPECIAL DA CEF DESPROVIDO.

### TRF4 · Apelação Cível 5048665-28.2015.4.04.7100/RS
- regras: R36
- posicao: FAV
- tribunal: TRF4
- classe_numero: Apelação Cível 5048665-28.2015.4.04.7100/RS
- orgao: 4ª Turma
- relator: Juíza Federal Vera Lúcia Feil (convocada)
- julgamento: 2023-08-16
- publicacao: 2023-08-18
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/trf-4/3077696683
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Com amortização negativa incontroversa num contrato do SFH, o TRF4 mantém a sentença que destacou do saldo devedor os juros não pagos: a parcela de juros impaga vai para conta apartada, com correção monetária pelos índices contratuais e sem novos juros; rejeita a tese do agente financeiro de que esses juros devem voltar ao saldo a cada ano.
- observacao: Recurso do agente financeiro desprovido e o dos mutuários provido (inversão da sucumbência). O TRF4 também afastou os encargos moratórios por entender descaracterizada a mora, ponto em que diverge do STJ (REsp 1.476.395/RS): não usar este acórdão para a mora. Contrato com PES/CP. Julgamento em 16/08/2023 (voto assinado em 17/08/2023); publicação pela data do Jusbrasil. Ementa sem correções; grafias do original mantidas ("CAPITLIZAÇÃO", "para ao cálculo").

ementa:
> SFH. REVISIONAL. TABELA PRICE. CAPITLIZAÇÃO DE JUROS. AMORTIZAÇÃO NEGATIVA. AFASTAMENTO. CÁLCULO EM CONTA APARTADA. ENCARGOS DE MORA. HONORÁRIOS ADVOCATÍCIOS. SUCUMBÊNCIA RECÍPROCA.
> 1. A utilização da Tabela Price como técnica de amortização não implica obrigatoriamente em capitalização de juros, eis que não há previsão para a incidência de juros sobre juros. Tal prática somente ocorre quando verificada a ocorrência de "amortização negativa", que ocorre quando a prestação mensal não quita sequer a parcela referente aos juros.
> 2. Todavia, verificada a amortização negativa e não havendo previsão contratual para ao cálculo de juros capitalizado mensalmente, impõe-se que a parcela dos juros não-paga seja acumulada em conta apartada, sujeita à correção monetária pelos índices contratuais, sem a incidência de novos juros. Precedentes.
> 3. A ré sucumbiu em parcela significativamente maior, devendo arcar com o maior percentual de honorários, enquanto a parte autora sucumbiu em parte menor, sendo justa a condenação em percentual menor de honorários. Merece reforma, portanto, a sentença, para determinação de inversão dos percentuais de honorários sucumbenciais devidos na origem.
> 4. Negado provimento à apelação da Caixa Econômica Federal, provida a apelação dos autores.

### TRF4 · Apelação Cível 5009409-21.2014.4.04.7001/PR
- regras: R36, R38
- posicao: FAV
- tribunal: TRF4
- classe_numero: Apelação Cível 5009409-21.2014.4.04.7001/PR
- orgao: 3ª Turma
- relator: Des.ª Federal Vânia Hack de Almeida
- julgamento: 2018-08-21
- publicacao: 2018-08-23
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/trf-4/3762835434
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em contrato do SFH de 1988 sem cláusula de CES, o TRF4 mantém a exclusão do coeficiente das prestações (R38: antes da lei que introduziu o CES, só com cláusula contratual expressa) e a revisão do saldo para que os juros não amortizados formem conta separada, sujeita só à correção monetária (R36).
- observacao: Apelações do agente financeiro e dos mutuários desprovidas; repetição simples (art. 23 da Lei 8.004/1990), sem dobro por falta de má-fé. O laudo confirmou amortizações negativas em cerca de um terço dos encargos. A ementa grafa "L 8.962/1993"; a lei que introduziu o CES é a Lei 8.692/1993, de 28/07/1993 (data citada no voto): mantida a grafia do acórdão, corrigir na peça. Ementa do campo "Ementa" do Jusbrasil (o inteiro teor traz o cabeçalho em versalete); grafia do original mantida ("Não à que se falar"). Julgado de 2018, fora da faixa preferida: não se achou acórdão do TRF4 de 2023–2026 sobre o CES. Publicação pela data do Jusbrasil (voto assinado em 23/08/2018).

ementa:
> ADMINISTRATIVO E CIVIL. SISTEMA FINANCEIRO DA HABITAÇÃO. CDC. CES. CAPITALIZAÇÃO DE JUROS. REPETIÇÃO EM DOBRO. COMPENSAÇÃO.
> 1. A aplicação do Código de Defesa do consumidor nas relações de financiamento habitacional não é regra de aplicação automática, porquanto o legislador tratou de maneira diferenciada as relações de financiamento para a aquisição da casa própria. Não tendo o mutuário comprovado o atendimento dos pressupostos aludidos no inc. VIII do art. 6º da Lei nº 8.078/90, não lhe assiste o direito à inversão do ônus da prova.
> 2. A cobrança do CES foi introduzida na legislação do SFH com a edição da L 8.962/1993, que prevê, no art. 8º, a incidência do coeficiente nos contratos regidos com cláusula PES. No caso de contratos celebrados em período anterior ao da vigência desse diploma legal, é imprescindível a existência de cláusula contratual que justifique a cobrança.
> 3. A aplicação do Sistema Francês de amortização aos contratos vinculados ao Sistema Financeiro da Habitação (SFH) é admitida por este Tribunal Regional da Quarta Região. Todavia, se o pagamento mensal não for suficiente para a quitação sequer dos juros, a determinação de lançamento dos juros vencidos e não pagos em conta separada, sujeita apenas à correção monetária, com o fim exclusivo de evitar a prática de anatocismo, encontra apoio na jurisprudência atual do STJ.
> 4. Conforme orientação do STJ, a repetição em dobro prevista no artigo 42, parágrafo único, do CDC, somente se aplica nas hipóteses em que há prova de que o credor agiu com má-fé, nos contratos firmados no âmbito do SFH.
> 5. Não à que se falar em compensação de valores quando não subsiste dívida do mutuário frente ao agente financeiro.

## R38 — SFH: CES sem cláusula expressa; PES/CP e TR

Tese: O Coeficiente de Equiparação Salarial só pode ser cobrado nos contratos do SFH com cláusula contratual expressa: resolução do extinto BNH ou circular do Banco Central não supre a falta de pactuação, e o pagamento da primeira prestação com o acréscimo não convalida a cobrança; ausente a cláusula, o CES deve ser excluído das prestações e restituído o que foi pago a maior.

### STJ · REsp 2.166.103/SP
- regras: R38
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 2.166.103/SP
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2025-12-09
- publicacao: 2025-12-12
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6266006669
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: O STJ mantém a exclusão do CES da primeira prestação: a cobrança depende de expressa pactuação contratual, não bastando referência a resoluções do BNH ou circulares do Banco Central (normas infralegais não criam obrigação sem pactuação), e o pagamento da primeira prestação com o acréscimo não convalida cláusula inexistente em contrato de adesão.
- observacao: Recurso do banco desprovido; julgado na mesma sessão e pelo mesmo relator do REsp 2.166.177/SP, em que o CES foi mantido porque o contrato o previa (ver a entrada ADV). No mesmo caso foram mantidos o PES/CP nas prestações, a TR como indexador pactuado e a repetição simples. Sessão virtual de 03 a 09/12/2025; DJEN de 12/12/2025, conforme citação em decisão posterior do STJ e a data do Jusbrasil. Correção na ementa: "PES /CP" → "PES/CP" (espaço de extração); grafia "INFRAALEGAIS" mantida.

ementa:
> PROCESSUAL CIVIL E DIREITO BANCÁRIO. RECURSO ESPECIAL. AÇÃO REVISIONAL DE MÚTUO HABITACIONAL NO SFH. PES/CP NAS PRESTAÇÕES. TR COMO INDEXADOR PACTUADO. ATUALIZAÇÃO DO SALDO DEVEDOR ANTES DA AMORTIZAÇÃO. JUROS REMUNERATÓRIOS SEM LIMITAÇÃO LEGAL EM 10% AO ANO. CES NA PRIMEIRA PARCELA. AUSÊNCIA DE PREVISÃO CONTRATUAL E DE BASE LEGAL À ÉPOCA. NORMAS INFRAALEGAIS DO BNH E BACEN INSUFICIENTES. PREQUESTIONAMENTO DEFICIENTE DOS DISPOSITIVOS FEDERAIS. RECURSO ESPECIAL NÃO PROVIDO.
> 1. Trata-se de recurso especial, fundado na alínea a do inciso III do art. 105 da Constituição Federal, interposto contra acórdão que, em ação revisional de mútuo habitacional, determinou a observância ao Plano de Equivalência Salarial por Categoria Profissional nas prestações, admitiu a TR como indexador pactuado, reconheceu a legitimidade da atualização e incidência de juros antes do abatimento da prestação, afastou a limitação dos juros a 10% ao ano, excluiu o Coeficiente de Equiparação Salarial na primeira parcela por ausência de previsão contratual e legal, assegurou a liberdade de escolha da seguradora e fixou a repetição simples.
> 2. O objetivo recursal é decidir se (i) houve violação dos arts. 82, 145, III, 148 e 151 do Código Civil de 1916 ao excluir o CES sem considerar a alegada ratificação e execução voluntária pelos mutuários; (ii) a aplicação do CES na primeira parcela encontra respaldo nas normas do extinto BNH e do Banco Central do Brasil, prescindindo de cláusula contratual expressa; (iii) a exclusão do CES implicou indevida alteração do equilíbrio contratual e do regime jurídico do SFH; (iv) houve prequestionamento suficiente dos dispositivos federais indicados.
> 3. A cobrança do Coeficiente de Equiparação Salarial depende de expressa pactuação contratual, não bastando a mera referência a resoluções ou circulares administrativas, e a alegada ratificação pelo pagamento isolado da primeira prestação não convalida cláusula inexistente em contrato de adesão.
> 4. A conclusão decorre de que a validade de encargos acessórios em financiamentos do SFH exige consentimento claro e inequívoco das partes; normas infralegais não criam obrigações sem pactuação; a discussão sobre eventual benefício econômico do CES é irrelevante diante da ausência de cláusula; e não houve enfrentamento específico, no acórdão recorrido, dos arts. 145, III, 148 e 150 do Código Civil de 1916, nem dos atos regulamentares invocados, evidenciando prequestionamento insuficiente.
> 5. Recurso especial não provido.

### STJ · REsp 2.166.177/SP
- regras: R38
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 2.166.177/SP
- orgao: Terceira Turma
- relator: Min. Moura Ribeiro
- julgamento: 2025-12-09
- publicacao: 2025-12-12
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6266010904
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Ressalva da peça: havendo previsão expressa do CES no contrato (no caso, coeficiente de 1,15), o STJ o valida mesmo em contrato anterior à Lei 8.692/1993. A ementa apoia a validade no "regime normativo" do SFH (Res. BNH 36/69, Circular Bacen 1.278/1988), argumento que o banco usará para defender CES sem cláusula: distinguir, porque no caso havia previsão explícita do coeficiente, e no REsp 2.166.103/SP, da mesma sessão, a falta de cláusula levou à exclusão.
- observacao: Recurso do mutuário desprovido; contrato de 07/03/1989 com banco estadual; também mantidos Tabela Price, correção do saldo antes da amortização e TR como componente da remuneração da poupança, e negada a repetição em dobro (sem relação de consumo apta). O voto registra que "consta, de forma explícita", o CES de 1,15 (item "z", conforme a sentença transcrita). Sessão virtual de 03 a 09/12/2025. Publicação pela data do Jusbrasil. Correções na ementa: espaços inseridos em "dobro.5." e "contratação;a"; a numeração do original salta do item 3 para o 5 e volta ao 4.

ementa:
> PROCESSUAL CIVIL E DIREITO BANCÁRIO. RECURSO ESPECIAL. AÇÃO REVISIONAL DE MÚTUO HABITACIONAL (SFH). COEFICIENTE DE EQUIPARAÇÃO SALARIAL. CONTRATO ANTERIOR À LEI 8.692/1993. REGIME NORMATIVO PRÉVIO (DECRETO-LEI 2.291/1986, RESOLUÇÃO CMN 1.446/1988, CIRCULAR BACEN 1.278/1988). VALIDADE. TABELA PRICE. AUSÊNCIA DE ANATOCISMO. ATUALIZAÇÃO DO SALDO DEVEDOR ANTES DA AMORTIZAÇÃO. VINCULAÇÃO À REMUNERAÇÃO DA CADERNETA DE POUPANÇA. UTILIZAÇÃO DA TR. CÓDIGO DE DEFESA DO CONSUMIDOR. INAPLICABILIDADE DA REPETIÇÃO EM DOBRO SEM DEMONSTRAÇÃO DE CLÁUSULA SURPRESA OU FALHA INFORMACIONAL. RECURSO ESPECIAL NÃO PROVIDO.
> 1. Trata-se de recurso especial interposto em ação revisional de contrato de mútuo habitacional, visando afastar a incidência do Coeficiente de Equiparação Salarial, substituir a Taxa Referencial pelo Índice Nacional de Preços ao Consumidor e aplicar o Código de Defesa do Consumidor para repetição de indébito em dobro.
> 2. O objetivo recursal é decidir se (i) o Coeficiente de Equiparação Salarial incide em contratos anteriores à Lei 8.692/1993; (ii) a Taxa Referencial pode ser utilizada como parâmetro de atualização do saldo devedor em contratos vinculados à remuneração da caderneta de poupança firmados antes da Lei 8.177/1991; (iii) incide o Código de Defesa do Consumidor para autorizar interpretação contratual favorável ao mutuário e repetição de indébito em dobro.
> 3. O Coeficiente de Equiparação Salarial integra o regime jurídico do SFH antes da Lei 8.692/1993 e é disciplinado por atos normativos válidos, com previsão expressa no regramento técnico aplicável; a atualização do saldo devedor pela variação dos índices da caderneta de poupança autoriza a utilização da Taxa Referencial como componente da remuneração dessa aplicação, não configurando substituição indevida de índice contratual; a natureza adesiva e o dirigismo contratual do SFH, por si sós, não tornam abusivas cláusulas sem prova de surpresa ou deficiência informacional, não se aplicando a repetição em dobro. 5. A conclusão decorre dos seguintes fundamentos: a validade do CES se apoia no regime normativo do SFH vigente à época da contratação; a Tabela Price e o critério de correção do saldo antes da amortização não implicam anatocismo; a vinculação contratual à remuneração da poupança permite a utilização da TR como componente dessa remuneração; a ausência de relação de consumo apta a atrair a repetição em dobro afasta a aplicação pretendida do art. 42, parágrafo único, do CDC; não há demonstração de cláusula surpresa ou falha informacional a justificar o afastamento de cláusulas com base nos arts. 46 e 47 do CDC.
> 4. Recurso especial não provido.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: A intimação por edital só vale depois de esgotadas as tentativas de intimação pessoal em todos os endereços conhecidos, inclusive o do imóvel; sem isso a consolidação da propriedade é nula.
- observacao: Publicação pela data do Jusbrasil (26/06/2025, data da sessão virtual de 18 a 26/06/2025 e do acórdão). Apelação da CEF desprovida por unanimidade; a sentença que anulou a consolidação foi mantida. Complementa os acórdãos do TJPR desta tese.

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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: O edital para purgar a mora exige o esgotamento das diligências de notificação pessoal; endereço diverso do contrato e devolução do requerimento de edital pelo registro de imóveis levaram à nulidade da consolidação.
- observacao: Sessão presencial de 12/12/2023; publicação pela data do Jusbrasil (13/12/2023, data da assinatura). Apelação da CEF desprovida por unanimidade. A grafia mista (maiúsculas e minúsculas) da ementa é a do texto do fetch.

ementa:
> ADMINISTRATIVO. APELAÇÃO. ALIENAÇÃO FIDUCIÁRIA. NULIDADE DA CONSOLIDAÇÃO DA PROPRIEDADE. PURGAÇÃO DA MORA. NOTIFICAÇÃO EDITALÍCIA. NECESSIDADE DO ESGOTAMENTO DAS DILIGÊNCIAS. ART. 26, § 4º, DA LEI 9.514/97.
> 1. A intimação do interessado para purgar a mora (art. 26, § 1º) é o único procedimento previsto pela Lei nº 9.514/97 que exige notificação pessoal do mutuário.
> 2. Portanto, imprescindível, o esgotamento de diligências que justificasse a subsidiária intimação editalícia.
> 3. Apelação desprovida.

### TJPR · Apelação Cível 0001410-56.2025.8.16.0112
- regras: R39
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001410-56.2025.8.16.0112
- orgao: 6ª Câmara Cível
- relator: Des. Fernando Paulino da Silva Wolff Filho
- julgamento: 2026-09-03
- publicacao: 2026-09-03
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037829661/Ac%C3%B3rd%C3%A3o-0001410-56.2025.8.16.0112
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Financiamento imobiliário com alienação fiduciária: sem diligências nos dois endereços do devedor, inclusive o do imóvel, a intimação por edital para purgar a mora é nula e a consolidação da propriedade também (Lei 9.514, art. 26, §§ 3º, 4º e 4º-B; STJ, AgInt no AREsp 2.925.916/MG).
- observacao: Apelação do mutuário provida: sentença de improcedência reformada, pedido inicial julgado procedente e sucumbência invertida. Acórdão mais recente do conjunto e já alinhado ao precedente do STJ do repertório. A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (ação declaratória de nulidade da consolidação, financiamento habitacional com alienação fiduciária, apelação do autor contra improcedência, comarca de Marechal Cândido Rondon). Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Marechal Cândido Rondon).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. ALIENAÇÃO FIDUCIÁRIA DE IMÓVEL. AÇÃO DECLARATÓRIA DE NULIDADE DE CONSOLIDAÇÃO DA PROPRIEDADE. INTIMAÇÃO PARA PURGAÇÃO DA MORA POR EDITAL. ESGOTAMENTO DAS TENTATIVAS DE INTIMAÇÃO PESSOAL NÃO CARACTERIZADO. INTIMAÇÃO NO ENDEREÇO DO IMÓVEL ALIENADO NÃO REALIZADA. VIOLAÇÃO DO DISPOSTO NO ART. 26, § 4º -B, DA LEI Nº 9.514/97. INTIMAÇÃO POR EDITAL NULA. CONSOLIDAÇÃO DA PROPRIEDADE IGUALMENTE NULA. PRECEDENTES DO STJ. SENTENÇA ALTERADA. SUCUMBÊNCIA REDISTRIBUÍDA. RECURSO PROVIDO. I. CASO EM EXAME 1. Por meio do presente recurso, o autor busca a reforma da sentença que julgou improcedente a ação declaratória de nulidade da consolidação da propriedade, na medida em que considerou válida a notificação para purgação da mora por edital. II. QUESTÕES EM DISCUSSÃO 2. A questão em discussão diz respeito à validade da notificação para purgar a mora por edital – se a instituição financeira ré esgotou todas as possibilidades de intimação pessoal antes da intimação por edital -.III. RAZÕES DE DECIDIR 3.1. A Lei nº 9.514/97 admite a intimação por edital quando frustradas as tentativas de localização do devedor, desde que certificadas pelo oficial competente Art. 26, §§ 3º, 4º e 4 -B). A propósito, sobre o tema o STJ pacificou o entendimento, no sentido de que “a intimação por edital, para fins de purgação da mora em contrato de alienação fiduciária de bem imóvel regido pela Lei 9.514/1997, pressupõe o esgotamento de todas as possibilidades de intimação pessoal do devedor” (AgInt no AREsp n. 2.925.916/MG, relator Ministro Raul Araújo, Quarta Turma, julgado em 30/3/2026, DJEN de 8/4/2026. 3.2. No caso dos autos, a intimação para purgação da mora por edital, como afirmado pelo autor, ora apelante, é nula, eis que não foram promovidas diligências nos dois endereços/contatos atribuídos ao devedor, em especial no endereço do imóvel alienado, o equivale dizer que não foram esgotados todos os meios de localização pessoal do devedor, o que era de rigor.3.3. Passando-se as coisas dessa forma, a sentença deve ser alterada e o pedido inicial julgado procedente. IV. DISPOSITIVO 4. Apelação provida. Dispositivos relevantes citados:
> Lei nº 9.514/97, art. 26, §§ 1º, 3º, 4 e 4-Bº.Jurisprudência relevante citada: STJ - AgInt no AREsp n. 2.925.916/MG, relator Ministro Raul Araújo, Quarta Turma, julgado em 30/3/2026, DJEN de 8/4/2026.STJ - REsp n. 1.906.475/AM, relatora Ministra Nancy Andrighi, Terceira Turma, julgado em 18/5/2021, DJe de 20/5/2021.

### TJPR · Apelação Cível 0028751-07.2022.8.16.0001
- regras: R39
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0028751-07.2022.8.16.0001
- orgao: 5ª Câmara Cível
- relator: Des. Rogério Etzel
- julgamento: 2025-08-11
- publicacao: 2025-08-15
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000033823841/Ac%C3%B3rd%C3%A3o-0028751-07.2022.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Tese expressa: a intimação por edital na alienação fiduciária de imóvel só é válida depois de esgotados todos os meios de localização pessoal do devedor (STJ, REsp 1.906.475/AM); o TJPR mantém a nulidade da consolidação.
- observacao: Apelação do credor desprovida; sentença que declarou a nulidade do procedimento de consolidação mantida e honorários majorados. Ementa curta, em texto corrido. A íntegra cita o próprio CNJ. A ementa vem em texto corrido, como no original. Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO ANULATÓRIA DE CONSOLIDAÇÃO DE PROPRIEDADE. ALIENAÇÃO FIDUCIÁRIA DE BEM IMÓVEL. INTIMAÇÃO POR EDITAL. AUSÊNCIA DE ESGOTAMENTO DOS MEIOS DE LOCALIZAÇÃO DO DEVEDOR. NULIDADE. SENTENÇA MANTIDA. RECURSO CONHECIDO E DESPROVIDO. I. Caso em exame 1. Apelação cível interposta contra sentença que julgou procedentes os pedidos formulados na ação anulatória de consolidação de propriedade. II. Questão em discussão 2. A questão em discussão consiste em saber se a intimação por edital do devedor para purgar a mora foi válida no caso. III. Razões de decidir 3. A intimação por edital com fins de purgação da mora é autorizada no art. 26, § 4º da Lei nº 9.514/97.4. Segundo o Superior Tribunal de Justiça, a intimação por edital é válida somente após o esgotamento de todos os meios de localização do devedor, o que não ocorreu no presente caso. IV. Dispositivo e tese 5. Apelação cível conhecida e não provida. Tese de julgamento: “A intimação por edital no procedimento de alienação fiduciária de bem imóvel é válida somente após o esgotamento de todas as tentativas de localização do devedor por meios pessoais, conforme entendimento do STJ.”Dispositivos relevantes citados: Lei nº 9.514/97, art. 26, § 4º.Jurisprudência relevante citada: STJ, REsp 1.906.475/AM, Rel. Min. Nancy Andrighi, Terceira Turma, j. 18.05.2021; TJPR, 20ª Câmara Cível, Apelação Cível 0003025-55.2024.8.16.0035, Rel. Des. Luciana Carneiro de Lara, j. 16.05.2025.

### TJPR · Apelação Cível 0005665-08.2002.8.16.0001
- regras: R39
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0005665-08.2002.8.16.0001
- orgao: 19ª Câmara Cível
- relator: Juíza Subst. 2º Grau Renata Estorilho Baganha
- julgamento: 2026-08-03
- publicacao: 2026-08-03
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000034918251/Ac%C3%B3rd%C3%A3o-0005665-08.2002.8.16.0001
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Vertente do DL 70/66 (SFH, garantia hipotecária): o banco não comprovou as comunicações exigidas (Súmula 199/STJ) nem o esgotamento das diligências antes do edital (art. 31, § 2º), e o TJPR mantém a nulidade do leilão extrajudicial.
- observacao: Apelação do banco desprovida; mantidos a nulidade do leilão extrajudicial e o expurgo da cumulação de encargos moratórios, com honorários majorados. Distinção: financiamento à produção (construção de empreendimento imobiliário) com garantia hipotecária, mutuários a construtora em falência e coautores pessoas físicas, não crédito ao adquirente final; a nulidade assenta na falta de prova das comunicações e do esgotamento das diligências, e o acórdão afasta os precedentes da Lei 9.514 para esse regime. A íntegra do portal não cita o CNJ, mas descreve o mesmo caso da ementa (apelação do banco, 1ª Vara Cível do Foro Central de Curitiba, leilão extrajudicial nulo, expurgo de comissão de permanência cumulada). Correções na ementa: só espaços inseridos onde o portal emendou título de seção ou ponto final à palavra seguinte; nenhuma palavra alterada. Fonte: portal de jurisprudência do TJPR (comarca de Curitiba).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. FINANCIAMENTO IMOBILIÁRIO COM GARANTIA HIPOTECÁRIA. SISTEMA FINANCEIRO DA HABITAÇÃO. LEILÃO EXTRAJUDICIAL. DECRETO-LEI Nº 70/66. 01) NULIDADE DO PROCEDIMENTO EXECUTIVO. AUSÊNCIA DE COMPROVAÇÃO DAS NOTIFICAÇÕES PARA PURGAÇÃO DA MORA. INOBSERVÂNCIA DO PROCEDIMENTO. NÃO DEMONSTRAÇÃO DO ESGOTAMENTO DAS DILIGÊNCIAS PRÉVIAS À NOTIFICAÇÃO POR EDITAL. MANUTENÇÃO DA SENTENÇA. 02) ALEGAÇÃO DE JULGAMENTO “EXTRA PETITA”. INOCORRÊNCIA. SENTENÇA QUE, NOS LIMITES DA CAUSA DE PEDIR, AFASTOU A CUMULAÇÃO INDEVIDA DE ENCARGOS MORATÓRIOS, SEM EXTRAPOLAR OS PEDIDOS DA INICIAL. MERO ACOLHIMENTO PARCIAL DA PRETENSÃO REVISIONAL. CONFORMIDADE COM OS ARTS. 141 E 492 DO CPC. 03) HONORÁRIOS ADVOCATÍCIOS. ARBITRAMENTO POR EQUIDADE. IMPOSSIBILIDADE. VALOR DA CAUSA ELEVADO. APLICAÇÃO DO ART. 85, § 2º, DO CPC, EM CONSONÂNCIA COM O TEMA 1.076 DO STJ. MANUTENÇÃO DO PERCENTUAL FIXADO NA SENTENÇA. 04) RECURSO NÃO PROVIDO. I. Caso em exame 1. Apelação interposta por instituição financeira contra sentença que declarou nulo o procedimento de leilão extrajudicial e determinou a revisão contratual de financiamento habitacional com garantia hipotecária. A controvérsia envolve a validade das notificações para purgação da mora, a forma de cobrança da comissão de permanência cumulada com juros e correção monetária, e a fixação dos honorários advocatícios na ação cautelar. II. Questão em discussão 2. A questão em discussão consiste em saber se o procedimento de leilão extrajudicial realizado pelo banco foi válido, considerando a alegação de regularidade das notificações para purgação da mora, a existência de julgamento “extra petita” quanto à comissão de permanência e a adequação da fixação dos honorários advocatícios na ação cautelar. III. Razões de decidir 3. A nulidade do procedimento executivo extrajudicial decorreu da ausência de comprovação pelo banco do envio das comunicações indispensáveis e do esgotamento das diligências antes da notificação por edital, conforme exigido pelo Decreto-Lei nº 70/66 e pela Lei nº 5.741/71.4. Não houve julgamento “extra petita” quanto à comissão de permanência, pois a sentença acolheu parcialmente o pedido revisional para afastar a cumulação abusiva de encargos moratórios, dentro do objeto e da causa de pedir deduzidos na inicial.5. A fixação dos honorários advocatícios em 10% sobre o valor atualizado da causa na ação cautelar está correta, pois o valor da causa é elevado, não sendo cabível o arbitramento por equidade nos termos do Tema 1076 do STJ. IV. Dispositivo e tese 6. Apelação conhecida e desprovida. Tese de julgamento: Na execução hipotecária de crédito vinculado ao Sistema Financeiro da Habitação, a nulidade do procedimento executivo extrajudicial decorre da ausência de comprovação pelo credor do envio das comunicações indispensáveis e do esgotamento das diligências para localização do devedor antes da notificação por edital, sendo imprescindível o respeito às formalidades previstas no Decreto-Lei nº 70/66 e na Lei nº 5.741/71 para a constituição válida da mora e regularidade do ato expropriatório._________Dispositivos relevantes citados:
> Decreto-Lei nº 70/1966, arts. 30, § 2º, e 31, § 2º; Lei nº 5.741/1971; Código de Processo Civil, arts. 2º, 85, § 2º, § 8º, e 141, 492.Jurisprudência relevante citada:
> TJPR, Ap. Cível 0024433-78.2022.8.16.0001, Rel. Domingos José Perfetto, 19ª Câmara Cível, j. 28.08.2023; Súmula 199/STJ.

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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
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
- verificado_em: 2026-10-29
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito bancário de capital de giro (PRONAMPE) tomada por microempresa, o TJMG mantém a incidência do CDC sobre a instituição financeira com base na teoria finalista mitigada e na vulnerabilidade técnica e informacional da tomadora.
- observacao: Complementa os acórdãos do TJPR desta tese. Alinhamento parcial: no voto, o CDC já tinha sido aplicado na sentença e o TJ confirma que a sentença o aplicou, sem reanalisar a vulnerabilidade, e o pedido revisional foi desprovido no mérito. Datas de julgamento e publicação pela data do Jusbrasil (o texto não traz a data da sessão). Há divergência interna: outra apelação do TJMG, de 09/06/2026, também sobre cédula bancária de capital de giro (PRONAMPE), afirma na ementa que o CDC não se aplica a capital de giro para fomento empresarial (visto só no resumo da busca, não aberto).

ementa:
> APELAÇÃO CÍVEL - AÇÃO REVISIONAL DE CONTRATO - CONHECIMENTO PARCIAL DO RECURSO - PRELIMINAR - REJEITADA - CÉDULA DE CRÉDITO BANCÁRIO - CAPITAL DE GIRO - PRONAMPE - INSTITUIÇÃO FINANCEIRA - APLICAÇÃO DO CDC - TEORIA FINALISTA MITIGADA - JUROS REMUNERATÓRIOS - ABUSIVIDADE NÃO DEMONSTRADA - TAXA SELIC - INCIDÊNCIA AUTORIZADA POR LEGISLAÇÃO ESPECÍFICA - SISTEMA PRICE - LEGALIDADE - CAPITALIZAÇÃO EXPRESSAMENTE PACTUADA - PROVA PERICIAL - DESNECESSIDADE - CERCEAMENTO DE DEFESA NÃO CONFIGURADO - MORA CARACTERIZADA - SENTENÇA MANTIDA. É vedado à parte, em sede recursal, trazer à discussão questões que não foram apresentas ao Magistrado primevo, exceto aquelas que forem cognoscíveis de ofício, referirem-se a fatos supervenientes aos articulados ou não tiverem sido deduzidas anteriormente por força maior. Assim, não se enquadrando a matéria eriçada a tais exceções, não deve o recurso ser conhecido quanto à nova discussão. Inexiste cerceamento de defesa quando a prova pericial se mostra desnecessária ao deslinde da controvérsia, sobretudo quando as partes dispensam sua produção e a matéria é eminentemente de direito. É aplicável o Código de Defesa do Consumidor às instituições financeiras, inclusive às pessoas jurídicas, quando evidenciada a vulnerabilidade técnica ou informacional, nos termos da teoria finalista mitigada. A revisão dos juros remuneratórios somente é admitida em hipóteses excepcionais, quando comprovada abusividade manifesta capaz de colocar o consumidor em desvantagem exagerada, o que não se verifica pela simples comparação com a taxa média de mercado. Nos contratos firmados no âmbito do PRONAMPE, a incidência da Taxa Selic encontra respaldo expresso na Lei nº 13.999/2020, não configurando ilegalidade ou bis in idem. A utilização do Sistema Francês de Amortização (Tabela Price) não implica, por si só, capitalização ilícita de juros, sendo válida quando expressamente pactuada, nos termos da Medida Provisória nº 2.170-36/2001 e da jurisprudência do Superior Tribunal de Justiça.. Ausente abusividade nos encargos exigidos no período da normalidade contratual, mantém-se a caracterização da mora.
### TJPR · Apelação Cível 0003516-02.2025.8.16.0173
- regras: PJ-VULN
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0003516-02.2025.8.16.0173
- orgao: 14ª Câmara Cível
- relator: Des. Iraja Pigatto Ribeiro
- julgamento: 2026-05-08
- publicacao: 2026-05-09
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035419191/Ac%C3%B3rd%C3%A3o-0003516-02.2025.8.16.0173
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: Em cédula de crédito para capital de giro, o TJPR reforma a sentença e reconhece a incidência do CDC a favor de pessoa jurídica de pequeno porte (consumidora por equiparação, art. 29), por vulnerabilidade fática e técnica frente ao banco, na teoria finalista mitigada.
- observacao: Apelação da autora parcialmente provida apenas para reconhecer a relação de consumo; a inversão do ônus da prova foi negada, o seguro prestamista e as tarifas foram mantidos e a improcedência dos demais pedidos subsistiu. Vulnerabilidade reconhecida em concreto (porte e ausência de paridade na contratação). A íntegra cita o próprio CNJ. Fonte: portal de jurisprudência do TJPR. Ementa copiada do portal sem o rótulo inicial ("Ementa:"). Na amostra de 2025-2026, a maioria das Câmaras do TJPR afasta o CDC em capital de giro: usar só com prova concreta da vulnerabilidade.

ementa:
> Direito civil e do consumidor. Apelação cível. Ação revisional de cédula de crédito bancário. Capital de giro. Relação de consumo. Teoria finalista mitigada. Seguro prestamista. Venda casada não configurada. Tarifas bancárias. Previsão contratual. Recurso parcialmente provido.I. Caso em exame1. Apelação cível interposta contra sentença que julgou improcedentes os pedidos formulados em ação revisional de Cédula de Crédito Bancário - Empréstimo Capital de Giro, dentre eles o reconhecimento de relação de consumo entre as partes, a declaração de nulidade do seguro prestamista por venda casada e a restituição em dobro dos valores cobrados indevidamente, com o consequente recálculo do saldo devedor e a reparação por danos morais.II. Questões em Discussão2. Há quatro questões em discussão: (i) definir se incide o Código de Defesa do Consumidor na relação entre pessoa jurídica de pequeno porte e instituição financeira em contrato de crédito para capital de giro, à luz da teoria finalista mitigada; (ii) definir se cabe inversão do ônus da prova em favor da autora; (iii) determinar se a contratação de seguro prestamista configura venda casada vedada; e (iv) estabelecer se a cobrança da tarifa bancária prevista no contrato é válida.III. Razões de decidir3. A relação entre as partes é de natureza bancária, sujeitando-se às normas de proteção do CDC. Pessoa jurídica de pequeno porte. Vulnerabilidade fática e técnica frente à instituição financeira. Ausência de paridade e simetria no estágio da contratação. Incidência das normas de proteção da Lei n. 8.078/1990. Possibilidade, em caráter extraordinário. Aplicação da teoria finalista mitigada. Consumidora por equiparação. CDC, art. 29. Sentença reformada no ponto.4. Inversão do ônus da prova. Medida que não decorre automática e necessariamente da incidência das regras do CDC e que não está justificada no caso em concreto, ou decorre meramente do vislumbre da hipossuficiência do consumidor. Elementos nos autos que, de princípio, não apontam impossível ou de sobrelevada dificuldade à autora a comprovação do que alegou.5. Seguro prestamista. Alegação de venda casada. Contratação clara e validamente ajustada. Vinculação da seguradora ao grupo econômico da instituição financiadora que não configura, por si só, venda casada, sobretudo quando há previsão contratual de cancelamento a qualquer tempo, direito não exercido pela autora. Validade da cobrança.6. Tarifas bancárias. Súmula TJPR n. 44. Cobrança admitida ante a existência de previsão contratual, ainda que genérica. Quebra do dever de informação (CDC, art. 6º, III) não observada. Ausência, portanto, de abusividade e valor a ser restituído.IV. Dispositivo7. Apelação interposta pela autora conhecida e parcialmente provida, apenas para reconhecer a existência de relação de consumo entre as partes.________________Teses de julgamento: “1. A pessoa jurídica de pequeno porte que contrata crédito bancário para capital de giro pode ser equiparada ao consumidor, nos termos da teoria finalista mitigada, quando demonstrada vulnerabilidade no estágio da contratação. 2. O reconhecimento da relação de consumo não implica automática e necessária revisão contratual nem inversão do ônus da prova, exigindo-se a demonstração concreta de abusividade ou desproporcionalidade nas cláusulas ajustadas e hipossuficiência que ponha em risco o direito à prova do alegado. 3. A contratação de seguro prestamista não configura venda casada quando o contrato prevê expressamente a faculdade de adesão e a possibilidade de cancelamento a qualquer tempo, sem a demonstração do condicionamento do crédito à contratação do seguro.”__________Dispositivos relevantes citados: CDC, arts. 2º, 4º, I, 6º, III e VIII, 29, 39, I, e 46; CC, art. 422; CPC/2015, arts. 85, § 11, 86, 98, § 3º, 373, I, 396, 408 e 927, III; Resolução CMN n. 3.919/2010, art. 5º, II; Resolução CMN n. 5.050/2022.Jurisprudência relevante citada: STJ, REsp n. 1.826.463/SC, Rel. Ministro PAULO DE TARSO SANSEVERINO, Segunda Seção, julgado em 14/10/2020; STJ, REsp n. 1.195.642/RJ, Rel. Ministra NANCY ANDRIGHI, Terceira Turma, julgado em 13/11/2012; STJ, REsp n. 2.020.811/SP, Rel. Ministra NANCY ANDRIGHI, Terceira Turma, julgado em 29/11/2022; STJ, Temas 972 e 1.059; STJ, Súmulas 297 e 473; e TJPR, Súmula 44.

### TJPR · Apelação Cível 0008931-06.2022.8.16.0129
- regras: PJ-VULN
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0008931-06.2022.8.16.0129
- orgao: 13ª Câmara Cível
- relator: Juiz Subst. 2º Grau Marcel Luis Hoffmann
- julgamento: 2026-08-31
- publicacao: 2026-08-31
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000036033971/Ac%C3%B3rd%C3%A3o-0008931-06.2022.8.16.0129
- verificado_em: 2026-10-28
- status: VERIFICADO
- uso_na_peca: O TJPR aplica o CDC a pessoa jurídica devedora de financiamento bancário (FOPAG COVID-19) por vulnerabilidade técnica, informacional e probatória, inverte o ônus da prova e cassa a sentença de cobrança para reabrir a instrução.
- observacao: Ação de cobrança do banco; apelação da empresa devedora parcialmente provida (relação de consumo reconhecida, ônus invertido, sentença cassada de ofício). Vulnerabilidade reconhecida em concreto: os dados sobre o valor efetivamente creditado nas contas dos empregados estavam na esfera exclusiva do banco. Não decide a revisão dos encargos. A íntegra do portal não cita o CNJ, mas é do mesmo caso (ação de cobrança do banco contra a empresa, FOPAG, 1ª Vara Cível de Paranaguá, mesmo dispositivo). Fonte: portal de jurisprudência do TJPR (comarca de Paranaguá). Ementa copiada do portal sem o rótulo inicial ("Ementa:").

ementa:
> Direito civil, processual civil e do consumidor. Apelação cível em ação de cobrança. FOPAG COVID-19. Aplicação do CDC à pessoa jurídica por vulnerabilidade técnica e informacional. Inversão do ônus da prova. Insuficiência de instrução probatória e divergência quanto ao valor mutuado. Cassação de ofício da sentença e retorno dos autos à origem. Recurso parcialmente provido.I. CASO EM EXAME1. Recurso de apelação interposto contra sentença que julgou procedente ação de cobrança fundada em contrato de financiamento vinculado ao programa FOPAG COVID-19, condenando a parte ré ao pagamento de saldo devedor. A recorrente sustenta a aplicação do Código de Defesa do Consumidor, a nulidade da cobrança por ausência de demonstrativo idôneo do débito, a existência de excesso de cobrança e a inadequação dos encargos. Requer, ainda, a remessa ao CEJUSC em segundo grau e a reforma da sentença para improcedência dos pedidos. II. QUESTÃO EM DISCUSSÃO2. Há três questões em discussão: (i) saber se incide o Código de Defesa do Consumidor na relação contratual firmada entre instituição financeira e pessoa jurídica, diante de eventual vulnerabilidade; (ii) saber se é cabível a inversão do ônus da prova em razão da impossibilidade de produção probatória pela devedora; (iii) saber se a sentença pode subsistir diante da divergência entre os documentos apresentados e da ausência de comprovação do valor efetivamente mutuado, exigindo maior dilação probatória.III. RAZÕES DE DECIDIR3. Aplica-se o Código de Defesa do Consumidor ao caso, em razão da vulnerabilidade técnica, informacional e probatória da pessoa jurídica frente à instituição financeira, nos termos da teoria finalista mitigada adotada pelo Superior Tribunal de Justiça.4. A inversão do ônus da prova é medida adequada, pois os elementos necessários à comprovação do valor efetivamente disponibilizado encontram-se na esfera exclusiva da instituição financeira, sendo inviável à parte devedora demonstrar fato negativo ou acessar registros internos do credor.5. Verifica-se divergência substancial entre os documentos que instruem a inicial quanto ao valor mutuado e à forma de liberação dos recursos, bem como ausência de comprovação dos créditos realizados, o que compromete a liquidez e a certeza do débito.6. A insuficiência da instrução probatória inviabiliza o exercício do contraditório e da ampla defesa, tornando imprescindível a reabertura da fase instrutória para apuração do montante efetivamente liberado, das parcelas adimplidas, da correta evolução da dívida e da correção dos encargos.7. Diante da deficiência da prova e da ausência de elementos mínimos para julgamento, impõe-se a cassação de ofício da sentença, com retorno dos autos à origem para regular instrução.8. Inviável a remessa ao CEJUSC de segundo grau na ausência de manifestação bilateral de interesse na autocomposição.IV. DISPOSITIVO E TESE9. Recurso parcialmente provido, com cassação de ofício da sentença e retorno dos autos à origem para reabertura da instrução probatória, reconhecida a incidência do Código de Defesa do Consumidor e determinada a inversão do ônus da prova.Tese de julgamento: “1. Aplica-se o Código de Defesa do Consumidor às relações contratuais entre instituição financeira e pessoa jurídica quando demonstrada vulnerabilidade técnica, informacional ou probatória. 2. É cabível a inversão do ônus da prova quando os elementos necessários à comprovação do débito estão na posse exclusiva do fornecedor. 3. A divergência entre os documentos apresentados e a ausência de comprovação do valor efetivamente mutuado comprometem a certeza e a liquidez da obrigação, o que impõem a cassação da sentença para reabertura da instrução probatória.”Dispositivos relevantes citados: CPC, arts. 373, II, e 487, I; CDC, art. 6º, VIII; CC, art. 405.Jurisprudência relevante citada: STJ, Recurso Especial nº 2.020.811/SP, Rel. Ministra Nancy Andrighi, Terceira Turma, julgado em 29.11.2022; TJPR, Agravo de Instrumento nº 0033126-15.2026.8.16.0000, Rel. Des. Fernando Ferreira de Moraes, julgado em 26.06.2026; TJPR, Apelação Cível nº 0033974-04.2023.8.16.0001, Rel. Des. Fabio André Santos Muniz, julgado em 27.06.2025.

## CONTA-CAPDIARIA — Capitalização diária de juros em conta corrente sem pactuação expressa

Tese: Em conta corrente, cheque especial e conta garantida, a capitalização de juros em periodicidade inferior à anual — inclusive a diária — só é exigível se expressamente pactuada no instrumento exibido pelo banco, com informação clara da periodicidade e da taxa diária; sem o instrumento, ou diante de cláusula genérica de capitalização diária sem a taxa diária, afasta-se a capitalização diária na recomposição do saldo, substituída pela mensal quando pactuadas as taxas mensal e anual (Súmula 541/STJ) ou por juros simples quando nada estiver pactuado.

### STJ · REsp 1.826.463/SC
- regras: CONTA-CAPDIARIA, R19
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.826.463/SC
- orgao: Segunda Seção
- relator: Min. Paulo de Tarso Sanseverino
- julgamento: 2020-10-14
- publicacao: 2020-10-29
- precedente_qualificado: não (Segunda Seção, sem rito repetitivo; a questão está afetada no Tema 1474/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2678916690
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Leading case da Segunda Seção: cláusula de capitalização diária que não informa a taxa diária viola o dever de informação (CDC, arts. 6º, III, 46 e 52) e é abusiva na parte em que omite essa taxa, mantidas as taxas efetivas mensal e anual pactuadas; é a base do cenário de recomposição com capitalização mensal.
- observacao: Cédula de crédito bancário, não conta corrente; o voto reproduz, do REsp 1.568.290/RS, simulação feita com dívida de cheque especial. Unânime. ALERTA: a questão foi afetada ao rito dos repetitivos no Tema 1474/STJ (ProAfR no REsp 2.252.171/RS, Segunda Seção, 01/09/2026: basta a previsão da periodicidade diária ou é indispensável a taxa diária?), pendente de julgamento e com suspensão dos REsps e AREsps sobre a matéria; conferir o resultado antes de citar. No cheque especial com juros flutuantes, ver a distinção do EDcl no REsp 2.162.177/PR (ADV, abaixo).

ementa:
> RECURSO ESPECIAL. DIREITO CIVIL, PROCESSUAL CIVIL E DO CONSUMIDOR. (EN. 3/STJ). CÉDULA DE CRÉDITO BANCÁRIO. CAPITALIZAÇÃO DIÁRIA DE JUROS REMUNERATÓRIOS. TAXA DIÁRIA NÃO INFORMADA. VIOLAÇÃO AO DEVER DE INFORMAÇÃO. ABUSIVIDADE.
> 1. Controvérsia acerca do cumprimento de dever de informação na hipótese em que pactuada capitalização diária de juros em contrato bancário.
> 2. Necessidade de fornecimento, pela instituição financeira, de informações claras ao consumidor acerca da periodicidade da capitalização dos juros adotada no contrato, e das respectivas taxas.
> 3. Insuficiência da informação acerca das taxas efetivas mensal e anual, na hipótese em que pactuada capitalização diária, sendo imprescindível, também, informação acerca da taxa diária de juros, a fim de se garantir ao consumidor a possibilidade de controle 'a priori' do alcance dos encargos do contrato. Julgado específico da Terceira Turma.
> 4. Na espécie, abusividade parcial da cláusula contratual na parte em que, apesar de pactuar as taxas efetivas anual e mensal, que ficam mantidas, conforme decidido pelo acórdão recorrido, não dispôs acerca da taxa diária.
> 5. RECURSO ESPECIAL DESPROVIDO, COM MAJORAÇÃO DE HONORÁRIOS.

### STJ · AgInt no REsp 1.414.764/PR
- regras: CONTA-CAPDIARIA, R19, CONTA-ENCARGOS, CONTA-EXIBICAO, CONTA-HAMBURGUES
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no REsp 1.414.764/PR
- orgao: Quarta Turma
- relator: Min. Raul Araújo
- julgamento: 2017-02-21
- publicacao: 2017-03-13
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/443358095
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em contrato de abertura de crédito em conta corrente, a capitalização em qualquer periodicidade (mensal ou anual) só é exigível com pactuação expressa e, sem o contrato nos autos, não se presume o ajuste; tarifas e demais encargos também dependem de previsão contratual, com o ônus da prova do banco.
- observacao: Ação de prestação de contas (segunda fase) de conta corrente de pessoa jurídica; agravo interno do banco desprovido por unanimidade. O item 1 não conheceu da tese de capitalização anual por inovação recursal, mas os itens 2 e 3 afirmam a regra e o item 4 mantém sentença que acolheu o laudo pericial com saldo credor para a correntista.

ementa:
> AGRAVO INTERNO NO RECURSO ESPECIAL. AÇÃO DE PRESTAÇÃO DE CONTAS. CONTRATO DE ABERTURA DE CRÉDITO EM CONTA-CORRENTE. CAPITALIZAÇÃO ANUAL DE JUROS. INOVAÇÃO RECURSAL. NECESSIDADE DE PACTUAÇÃO EXPRESSA DA CAPITALIZAÇÃO, SEJA MENSAL OU ANUAL. AUSÊNCIA DOS CONTRATOS. ÔNUS DA INSTITUIÇÃO FINANCEIRA. TAXAS, TARIFAS E DEMAIS ENCARGOS. EXCLUSÃO ANTE A AUSÊNCIA DE PROVA DE CONTRATAÇÃO. DECISÃO MANTIDA. RECURSO DESPROVIDO.
> 1. A legitimidade da cobrança da capitalização anual deixou de ser suscitada perante o primeiro grau, sendo vedado ao Tribunal de origem apreciar o tema no julgamento da apelação, sob pena de supressão de instância e inobservância do princípio do duplo grau de jurisdição.
> 2. A Segunda Seção do Superior Tribunal de Justiça, no julgamento do AgRg no AREsp 429.029/PR, Rel. Ministro MARCO BUZZI, DJe de 14/04/2016, consolidou o entendimento de que a cobrança de juros capitalizados - inclusive na periodicidade anual - só é permitida quando houver expressa pactuação. Nas hipóteses em que o contrato não é juntado, é inviável presumir o ajuste do encargo, mesmo sob a periodicidade anual.
> 3. É necessária a expressa previsão contratual das tarifas e demais encargos bancários para que possam ser cobrados pela instituição financeira. Não juntados aos autos os contratos, deve a instituição financeira suportar o ônus da prova, afastando-se as respectivas cobranças.
> 4. A sentença suficientemente fundamentada que acata laudo pericial apontando saldo credor em favor da autora, com a ressalva de que a parte ré não se desincumbiu do ônus da prova, abstendo-se de apresentar os contratos e as autorizações para débito em conta-corrente, imprescindíveis à apuração das contas, não ofende os arts. 131 e 436 do CPC/73. 5. Agravo interno não provido.

### STJ · EDcl no REsp 2.162.177/PR
- regras: CONTA-CAPDIARIA
- posicao: ADV
- tribunal: STJ
- classe_numero: EDcl no REsp 2.162.177/PR
- orgao: Quarta Turma
- relator: Min. Maria Isabel Gallotti
- julgamento: 2026-04-13
- publicacao: 2026-04-22
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/6621158222
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: LIMITE a antecipar: no cheque especial com juros flutuantes e apuração diária sobre saldo variável, a Quarta Turma reputou suficiente a cláusula expressa de capitalização diária acompanhada da metodologia de cálculo (saldo devedor de cada dia multiplicado pela taxa e dividido por 30) e das taxas mensal e anual, distinguindo o REsp 1.826.463/SC; a peça deve mostrar que o instrumento exibido não traz cláusula expressa nem metodologia, ou que a taxa era prefixada e informável.
- observacao: Embargos de declaração rejeitados por unanimidade (sessão virtual de 07 a 13/04/2026); o acórdão embargado (REsp 2.162.177/PR, que negou provimento ao recurso do correntista e manteve a capitalização diária em ação de cobrança de cooperativa de crédito, origem TJPR) não foi localizado no Jusbrasil, e a ementa dos embargos resume a distinção. Decisões monocráticas de 2026 repetem-na (REsp 2.259.943, 2.260.172, 2.263.229, 2.265.273 e 2.278.340). Publicação pelo DJEN indicado nos dados do Jusbrasil. A questão está no Tema 1474/STJ (afetado em 01/09/2026, pendente). Em sentido contrário, o TJPR (14ª Câmara Cível) afastou a capitalização diária sem taxa diária em cheque especial (apelação listada abaixo).

ementa:
> PROCESSUAL CIVIL. EMBARGOS DE DECLARAÇÃO NO RECURSO ESPECIAL. ART. 1.022 DO CPC. CABIMENTO RESTRITO. INEXISTÊNCIA DE OMISSÃO, OBSCURIDADE, CONTRADIÇÃO OU ERRO MATERIAL. AÇÃO DE COBRANÇA. CONTRATO DE ABERTURA DE CRÉDITO EM CONTA CORRENTE (CHEQUE ESPECIAL). CAPITALIZAÇÃO DIÁRIA DE JUROS REMUNERATÓRIOS. CLÁUSULA EXPRESSA. JUROS FLUTUANTES. METODOLOGIA DE CÁLCULO DIÁRIO PREVISTA NO CONTRATO. DEVER DE INFORMAÇÃO. ANÁLISE À LUZ DAS PARTICULARIDADES DA CONTRATAÇÃO. REsp 1.826.463/SC. DISTINÇÃO FUNDAMENTADA NO ACÓRDÃO EMBARGADO. AUSÊNCIA DE DECISÃO SURPRESA. ARTS. 9º E 10 DO CPC. INAPLICABILIDADE. PRETENSÃO DE REDISCUSSÃO DO MÉRITO. EMBARGOS REJEITADOS.
> 1. Os embargos de declaração possuem cabimento restrito às hipóteses previstas no art. 1.022 do CPC, não se prestando à rediscussão do mérito nem à reapreciação do entendimento adotado no julgamento do recurso especial.
> 2. Não se caracteriza obscuridade quanto ao dever de informação na capitalização diária de juros quando o acórdão embargado, considerando a natureza do cheque especial, reconhece a inviabilidade de fixação prévia de taxa diária única e reputa suficiente, para fins de transparência, a previsão expressa da capitalização diária aliada à explicitação da metodologia de cálculo e aos demais elementos informativos constantes do contrato.
> 3. O precedente da Segunda Seção no REsp 1.826.463/SC foi devidamente enfrentado, tendo o acórdão embargado explicitado distinção fundada nas particularidades do contrato rotativo, com juros flutuantes e apuração diária sobre saldo variável, afastando a alegação de aplicação automática da tese firmada naquele julgamento.
> 4. Inexiste omissão ou nulidade por violação aos arts. 9º e 10 do CPC, uma vez que o julgado não se apoiou em fatos novos, mas realizou qualificação jurídica a partir de premissas constantes do próprio objeto litigioso.
> 5. Embargos de declaração rejeitados.

### TJPR · Apelação Cível 0015851-98.2023.8.16.0019
- regras: CONTA-CAPDIARIA, R19
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0015851-98.2023.8.16.0019
- orgao: 14ª Câmara Cível
- relator: Des.ª Josely Dittrich Ribas
- julgamento: 2026-02-03
- publicacao: 2026-02-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000033880771/Ac%C3%B3rd%C3%A3o-0015851-98.2023.8.16.0019
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: No cheque especial (adiantamento a depositante com encargos 'aplicados sobre o saldo devedor diário'), a previsão genérica de capitalização diária sem a taxa diária não vale: o TJPR afastou a capitalização, mandou calcular os encargos de forma simples e descaracterizou a mora.
- observacao: Ação de cobrança de cooperativa de crédito; recurso do correntista provido. Aplica o REsp 1.826.463/SC e é anterior ao EDcl no REsp 2.162.177/PR (Quarta Turma, abril de 2026), que validou cláusula semelhante de cooperativa com metodologia descrita; conferir o instrumento antes de citar. Consequência fixada: encargos calculados de forma simples, e não a capitalização mensal. Fonte: portal de jurisprudência do TJPR (comarca de Ponta Grossa).

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO DE COBRANÇA. CHEQUE ESPECIAL. SENTENÇA DE PROCEDÊNCIA. ILEGALIDADE DA CAPITALIZAÇÃO DE JUROS. DESCARACTERIZAÇÃO DA MORA. RECURSO CONHECIDO E PROVIDO.I. CASO EM EXAME1. Apelação cível interposta contra sentença que julgou procedente a pretensão deduzida na ação de cobrança, condenando o réu ao pagamento dos valores devidos em razão do inadimplemento do contrato de cheque especial. Inconformismo da parte ré. II. QUESTÕES EM DISCUSSÃO2. A questão em discussão consiste em verificar se: (i) há cobrança indevida da capitalização de juros; e (ii) deve ser descaracterizada a mora. III. RAZÕES DE DECIDIR3.1. A capitalização de juros exige expressa pactuação, conforme Súmula 539 do STJ. Pactuação da cobrança de juros capitalizados diariamente não demonstrada. A ausência de indicação clara e expressa quanto à taxa diária de juros inviabiliza a cobrança de capitalização diária, mesmo havendo previsão contratual genérica nesse sentido.3.2. Conforme o entendimento firmado pelo STJ no REsp nº 1.061.530/RS, a cobrança de encargos abusivos no período de normalidade contratual descaracteriza a mora. Hipótese aplicável ao caso concreto, diante da ausência de pactuação válida da capitalização de juros. Sentença reformada nesse ponto, com a redistribuição da sucumbência. IV. DISPOSITIVO 4. Recurso conhecido e provido. ____________________________________________________Dispositivos relevantes citados: CPC/2015, art. 85, §11; Súmulas nº 539 e 541 do STJ.Jurisprudência relevante citada: STJ, REsp nº 1.061.530/RS, rel. Min. Nancy Andrighi, Segunda Seção, j. 22.10.2008, DJe 10.03.2009.

### TJPR · Apelação Cível 0001945-76.2016.8.16.0119
- regras: CONTA-CAPDIARIA, R19, CONTA-ENCARGOS, CONTA-EXIBICAO
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001945-76.2016.8.16.0119
- orgao: 14ª Câmara Cível
- relator: Des. Francisco Eduardo Gonzaga de Oliveira
- julgamento: 2024-07-29
- publicacao: 2024-07-29
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000027371621/Ac%C3%B3rd%C3%A3o-0001945-76.2016.8.16.0119
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Na conta garantida (cédula de crédito bancário), a capitalização diária pactuada só com as taxas mensal e anual, sem a taxa diária, é ilegal e deve ser expurgada; as tarifas da conta corrente vinculada caem porque o banco, intimado, não apresentou o contrato; mora descaracterizada.
- observacao: Ação monitória do banco contra empresa correntista; apelação do banco desprovida, com nulidade parcial de ofício da sentença na parte em que revisou contratos de capital de giro não impugnados (ultra petita). Aplica o REsp 1.826.463/SC. Fonte: portal de jurisprudência do TJPR (comarca de Nova Esperança).

ementa:
> APELAÇÃO CÍVEL. AÇÃO MONITÓRIA. CÉDULA DE CRÉDITO BANCÁRIO – CONTA GARANTIDA. EMBARGOS À MONITÓRIA PARCIALMENTE ACOLHIDOS. IRRESIGNAÇÃO DA PARTE AUTORA. 1. REVISÃO DOS CONTRATOS ANTERIORES (STJ, SÚMULA 286). POSSIBILIDADE, DESDE QUE ESPECIFICADOS OS ENCARGOS SUPOSTAMENTE ABUSIVOS NOS CONTRATOS ORIGINÁRIOS. CASO CONCRETO: ARGUIÇÃO DE ABUSIVIDADES SOMENTE EM RELAÇÃO AO TÍTULO OBJETO DE COBRANÇA E À CONTA CORRENTE VINCULADA. PLEITO REVISIONAL QUE DEVE SE LIMITAR A TAIS OPERAÇÕES. SENTENÇA QUE ANALISOU A LEGALIDADE DOS ENCARGOS INCIDENTES EM DOIS CONTRATOS DE EMPRÉSTIMO – CAPITAL DE GIRO. JULGAMENTO ULTRA PETITA CARACTERIZADO. VIOLAÇÃO AOS ARTIGO 141 E 492 DO CÓDIGO DE PROCESSO CIVIL. NULIDADE PARCIAL RECONHECIDA DE OFÍCIO. DECOTE DA PARTE EXCEDENTE. 2. CAPITALIZAÇÃO DIÁRIA DE JUROS. POSSIBILIDADE, DESDE QUE HAJA EXPRESSA INFORMAÇÃO AO CONSUMIDOR DA TAXA DIÁRIA. PACTUAÇÃO CONTRATUAL APENAS DAS TAXAS MENSAL E ANUAL DE JUROS. ILEGALIDADE DA COBRANÇA. EXPURGO DEVIDO. 3. TARIFAS BANCÁRIAS. COBRANÇA CONDICIONADA À PREVISÃO CONTRATUAL, AINDA QUE GENÉRICA. SÚMULA 44 DO TJPR. INSTITUIÇÃO FINANCEIRA QUE, EMBORA INTIMADA A APRESENTAR O CONTRATO DE CONTA CORRENTE, PERMANECEU INERTE. EXPURGO DEVIDO. 4. DESCARACTERIZAÇÃO DA MORA. MANUTENÇÃO. ABUSIVIDADE DOS ENCARGOS DE NORMALIDADE RECONHECIDA. SENTENÇA MANTIDA, COM A FIXAÇÃO DE HONORÁRIOS RECURSAIS (CPC, ART. 85, §11). DECRETAÇÃO, DE OFÍCIO, DA NULIDADE PARCIAL DA SENTENÇA. RECURSO CONHECIDO E NÃO PROVIDO.

## CONTA-HAMBURGUES — Saldo devedor diário (método hamburguês) como metodologia pericial

Tese: Na revisão de conta corrente, cheque especial e conta garantida, a perícia que reconstitui o saldo dia a dia a partir dos extratos e apura os encargos sobre o saldo devedor diário (método hamburguês) é metodologia idônea para a recomposição, e os extratos e planilhas do próprio banco, impugnados com prova, não demonstram por si a regularidade do débito: sem contrato que preveja outra metodologia, prevalece o laudo e cabe ao banco provar o crédito.

### STJ · REsp 1.783.253/SP
- regras: CONTA-HAMBURGUES
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.783.253/SP
- orgao: Terceira Turma
- relator: Min. Ricardo Villas Bôas Cueva
- julgamento: 2019-08-06
- publicacao: 2019-08-13
- precedente_qualificado: não
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2679605128
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em monitória de contratos de conta garantida, o contrato com os extratos basta para iniciar a cobrança (Súmula 247), mas é presunção que cede à prova contrária: infirmada a idoneidade dos documentos do banco (perícia, escrituração frágil), passa a ele o ônus de provar o crédito.
- observacao: Recurso especial da massa falida do banco desprovido por unanimidade; fatos peculiares (notas promissórias devolvidas como liquidadas, reciprocidade entre as partes). Não trata do método hamburguês: serve à segunda parte da tese (extrato e planilha do banco, impugnados com prova, não demonstram por si o débito). O STJ não tem acórdão de mérito sobre o método (questão de prova, Súmula 7); só decisões monocráticas o mencionam.

ementa:
> RECURSO ESPECIAL. PROCESSUAL CIVIL. AÇÃO MONITÓRIA. EMBARGOS. CONTRATO DE LIMITE DE CRÉDITO. IDONEIDADE INFIRMADA PELO EMBARGANTE. EXISTÊNCIA DO CRÉDITO. PROVA. ÔNUS DO AUTOR/EMBARGADO.
> 1. Recurso especial interposto contra acórdão publicado na vigência do Código de Processo Civil de 1973 (Enunciados Administrativos nºs 2 e 3/STJ).
> 2. Para dar início ao processo monitório, o autor deve exibir prova escrita capaz de comprovar os fatos constitutivos do direito alegado, não havendo dúvida de que os contratos de limite de crédito, acompanhados dos respectivos extratos, constituem documentos idôneos para a propositura da demanda, a teor do disposto na Súmula nº 247/STJ.
> 3. A decisão que considera idôneo o documento apresentado pelo autor da ação monitória e determina a expedição do correspondente mandado de pagamento é proferida em juízo de cognição sumária.
> 4. Na ação monitória, o contraditório é exercitado de modo diferido, por meio do oferecimento de embargos, momento em que o magistrado passa a exercer cognição plena e exauriente acerca da presença ou não dos pressupostos necessários à concessão de eficácia executiva ao mandado expedido initio litis.
> 5. Hipótese em que as instâncias ordinárias, com base na prova pericial produzida, na fragilidade da escrituração contábil de ambas as partes, na relação de reciprocidade havida entre autor e réu e na existência de peculiaridades que sempre permearam os negócios realizados pelo Banco Santos S.A., concluíram que os documentos apresentados pela parte autora, conquanto suficientes para dar início ao procedimento monitório, não conferiam credibilidade à dívida cobrada a ponto de se atribuir eficácia executiva ao mandado monitório.
> 6. Nos embargos monitórios, cabe ao réu/embargante desconstituir a presunção inicial que milita em favor do autor/embargado, utilizando-se dos meios de prova disponíveis em direito.
> 7. Se o réu/embargante apresenta prova hábil para infirmar a idoneidade do documento escrito no qual se funda a ação monitória, passa a ser do autor/embargado a incumbência de provar a presença dos requisitos necessários para a atribuição de força executiva ao mandado monitório.
> 8. A presunção que se estabelece em favor do autor da ação monitória no momento em que se expede o mandado para pagamento cede diante da produção de prova capaz de ilidir a existência do crédito.
> 9. Recurso especial não provido.

### TJPR · Agravo de Instrumento 0006305-13.2022.8.16.0000
- regras: CONTA-HAMBURGUES
- posicao: FAV
- tribunal: TJPR
- classe_numero: Agravo de Instrumento 0006305-13.2022.8.16.0000
- orgao: 14ª Câmara Cível
- relator: Juíza Subst. 2º Grau Cristiane Santos Leite
- julgamento: 2022-09-19
- publicacao: 2022-09-19
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000020183921/Ac%C3%B3rd%C3%A3o-0006305-13.2022.8.16.0000
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: No cumprimento de sentença de revisional de conta corrente (cheque especial), o TJPR manteve a perícia que apurou os juros pelo método hamburguês, sobre os dias em que o saldo esteve negativo, como 'método predominantemente aceito' (CPC, art. 473, III), rejeitando a base de dias úteis do banco, que não exibiu contrato com metodologia diversa.
- observacao: Agravo do banco parcialmente provido só quanto às tarifas (limites da coisa julgada); no ponto da metodologia, favorável ao correntista. ATENÇÃO: o próprio voto cita precedentes que exigem a base de dias úteis quando prevista no contrato ou quando o título não a altera (acórdãos da 14ª e da 15ª Câmaras Cíveis citados no voto) — a perícia deve declarar a base de dias e justificá-la pela falta de cláusula. Fonte: portal de jurisprudência do TJPR (comarca de Faxinal). Correção: 'INSURGêNCIA' por 'INSURGÊNCIA' (defeito de extração).

ementa:
> AGRAVO DE INSTRUMENTO. CUMPRIMENTO DE SENTENÇA. DECISÃO HOMOLOGATÓRIA DOS CÁLCULOS PERICIAIS. INSURGÊNCIA DA INSTITUIÇÃO FINANCEIRA EXECUTADA.1. PERIODICIDADE DA TAXA DE JUROS REMUNERATÓRIOS. PERÍCIA APURA DIAS QUE A CONTA PERMANECEU NEGATIVA. ALEGAÇÃO QUE O CORRETO SERIA DIAS ÚTEIS. SEM RAZÃO. ART. 473, INCISO III, DO CÓDIGO DE PROCESSO CIVIL, IMPÕE QUE O CÁLCULO DEVE LEVAR EM CONTA O MÉTODO PREDOMINANTEMENTE ACEITO PELOS ESPECIALISTAS DA ÁREA DO CONHECIMENTO. NESTE ASPECTO, NÃO HÁ DÚVIDAS QUANTO A HIGIDEZ DOS CÁLCULOS DO PERITO JUDICIAL, POIS LEVOU EM CONTA O MÉTODO PREDOMINANTEMENTE ACEITO, O MÉTODO HAMBURGUÊS, QUE LEVA EM CONTA O TOTAL DE DIAS EM QUE O SALDO ESTAVA NEGATIVO. OMISSO O TÍTULO JUDICIAL EXEQUENDO QUANTO À METODOLÓGICA APLICADA, A DISCUSSÃO SOMENTE TERIA RELEVÂNCIA ACASO EXPRESSAMENTE PACTUADO ALGUM MÉTODO ESPECIFICO ENTRE AS PARTES. CONTUDO, A INSTITUIÇÃO FINANCEIRA AGRAVANTE NÃO APRESENTOU CONTRATOS OU TERMOS ADITIVOS DA CONTA CORRENTE REVISADA, CONTENDO CONDIÇÕES ESPECÍFICAS QUANTO À METODOLOGIA DO CÁLCULO PARA EXCLUSÃO DA CAPITALIZAÇÃO MENSAL DE JUROS DOS SALDOS DEVEDORES. PRECEDENTES DESTA CÂMARA CÍVEL. DECISÃO MANTIDA.2. DEVOLUÇÃO TARIFAS BANCÁRIAS. ALEGAÇÃO DE OFENSA À COISA JULGADA. COM RAZÃO. O PLEITO INICIAL, BEM COMO O TÍTULO EXECUTIVO, DELIMITARAM OS VALORES INDEVIDOS A SEREM RESTITUÍDOS, ENCARGOS SOB DENOMINAÇÃO “NHOC”(CÓDIGO 62) E SEUS REFLEXOS, NÃO ABRANGENDO DEMAIS ENCARGOS QUE NÃO SEJAM ESTES. VEDADO AO JULGADOR CONHECER, DE OFÍCIO, DA ABUSIVIDADE DAS CLÁUSULAS. SÚMULA 381 DO SUPERIOR TRIBUNAL DE JUSTIÇA. DECISÃO REFORMADA.RECURSO CONHECIDO E PARCIALMENTE PROVIDO.

### TJPR · Apelação Cível 0006221-09.2021.8.16.0077
- regras: CONTA-HAMBURGUES, R16, R19, CONTA-ENCARGOS, CONTA-EXIBICAO
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0006221-09.2021.8.16.0077
- orgao: 16ª Câmara Cível
- relator: Juíza Subst. 2º Grau Vania Maria da Silva Kramer
- julgamento: 2026-07-06
- publicacao: 2026-07-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000037589291/Ac%C3%B3rd%C3%A3o-0006221-09.2021.8.16.0077
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Na revisional de conta corrente, prevaleceu o laudo que, pelo método hamburguês e pela dinâmica dos lançamentos dos extratos, demonstrou capitalização composta sem pactuação; o banco, intimado, não exibiu o contrato nem os instrumentos dos encargos, o que atraiu a presunção de veracidade (art. 400 do CPC) e levou ao expurgo da capitalização, à taxa média e à restituição das tarifas sem contratação.
- observacao: Recurso do banco parcialmente provido só para afastar o dobro (cobranças anteriores a 30/03/2021, pela modulação do EAREsp 676.608/RS; o Tema 929/STJ foi fixado sem modulação — ver R26). A ação anterior de exigir contas interrompeu a prescrição. O rol de dispositivos da ementa menciona o art. 192, § 3º, da CF só porque o banco o invocou; não é fundamento. Serve também a CONTA-EXIBICAO e CONTA-ENCARGOS. Fonte: portal de jurisprudência do TJPR (comarca de Cruzeiro do Oeste). Correção: retirado o rótulo 'Ementa:' que abre o texto do portal.

ementa:
> DIREITO CIVIL E PROCESSUAL CIVIL. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTA CORRENTE CUMULADA COM REPETIÇÃO DE INDÉBITO. CONTRATO BANCÁRIO. RELAÇÃO DE CONSUMO. INVERSÃO DO ÔNUS DA PROVA. AUSÊNCIA DE APRESENTAÇÃO DO CONTRATO PELA INSTITUIÇÃO FINANCEIRA. CAPITALIZAÇÃO DE JUROS NÃO PACTUADA. JUROS REMUNERATÓRIOS ACIMA DA TAXA MÉDIA DE MERCADO. COBRANÇA DE TARIFAS BANCÁRIAS SEM COMPROVAÇÃO DE CONTRATAÇÃO. INTERRUPÇÃO DA PRESCRIÇÃO POR AÇÃO ANTERIOR DE EXIGIR CONTAS. RESTITUIÇÃO SIMPLES DO INDÉBITO. PARCIAL PROVIMENTO DO RECURSO.I. Caso em exame1. Apelação cível interposta contra sentença que julgou procedentes os pedidos para declarar a ilegalidade da capitalização de juros, das tarifas bancárias e da cobrança de juros remuneratórios acima da taxa média de mercado, condenando o banco à restituição dos valores cobrados indevidamente. II. Questão em discussão2. Há quatro questões em discussão: (i) definir se a ação anterior de exigir contas interrompeu o prazo prescricional da posterior ação revisional; (ii) estabelecer se a ausência de apresentação do contrato bancário autoriza o reconhecimento da ilegalidade da capitalização de juros, das tarifas bancárias e da cobrança de juros remuneratórios acima da média de mercado; (iii) determinar se a petição inicial é inepta pela ausência de consignação do valor incontroverso e de especificação suficiente das cláusulas impugnadas; e (iv) verificar se é cabível a restituição em dobro dos valores cobrados indevidamente.III. Razões de decidir3. A relação jurídica entre as partes possui natureza consumerista, o que autoriza a inversão do ônus da prova em favor do correntista, diante de sua hipossuficiência técnica e documental perante a instituição financeira.4. A instituição financeira, embora intimada, não apresentou o contrato de abertura de conta corrente nem os instrumentos de pactuação dos encargos cobrados, circunstância que atrai a presunção de veracidade das alegações autorais e impede a comprovação da regularidade das cobranças.5. A pretensão revisional de contrato bancário submete-se ao prazo prescricional decenal do art. 205 do Código Civil, observada a regra de transição do art. 2.028 do mesmo diploma, sendo interrompida pela citação válida em ação anterior de exigir contas referente ao mesmo contrato, ainda que extinta sem resolução do mérito.6. A petição inicial não é inepta quando descreve adequadamente a relação jurídica, delimita o período controvertido, identifica as rubricas impugnadas e formula pedidos certos e determinados, sendo inaplicável ao caso a exigência de consignação do valor incontroverso prevista no art. 330, § 2º, do CPC.7. A primeira perícia judicial demonstrou, mediante método hamburguês e análise da dinâmica dos lançamentos bancários, a ocorrência de capitalização composta de juros sem pactuação expressa, sendo legítima a prevalência desse laudo diante de sua maior coerência técnica e aderência aos elementos dos autos.8. A ausência de contrato inviabiliza a comprovação da pactuação válida da capitalização mensal de juros, impondo o afastamento e a restituição dos valores cobrados indevidamente.9. A cobrança de juros remuneratórios acima da taxa média de mercado restou comprovada por perícia judicial, sendo adequada a utilização das taxas médias divulgadas pelo Banco Central como parâmetro de aferição da abusividade, diante da ausência de comprovação da taxa contratada.10. A cobrança de tarifas bancárias exige previsão contratual expressa, autorização do correntista e comprovação da efetiva prestação do serviço correspondente, requisitos não demonstrados pela instituição financeira nos autos.11. A repetição em dobro do indébito não é cabível em relação a cobranças realizadas antes de 30/03/2021 sem demonstração de má-fé da instituição financeira, devendo a restituição ocorrer de forma simples.IV. Dispositivo e tese12. Recurso parcialmente provido.____________Dispositivos relevantes citados: CDC, arts. 6º, VIII, e 42, parágrafo único; CPC/2015, arts. 330, §§ 2º e 3º, 371, 373, § 1º, 400, 479 e 85, § 2º e § 11; CC/2002, arts. 202, I, 205, 354 e 2.028; CC/1916, art. 177; CF/1988, art. 192, § 3º; MP nº 2.170-36/2001.Jurisprudência relevante citada: STJ, AgInt no AREsp nº 2.978.345/PR, Rel. Min. Humberto Martins, 3ª Turma, j. 23.03.2026; STJ, AgInt no REsp nº 2.124.259/SP, Rel. Min. Raul Araújo, 4ª Turma, j. 22.09.2025; STJ, AgInt no REsp nº 1.934.949/PR, Rel. Min. Maria Isabel Gallotti, 4ª Turma, j. 29.11.2021; STJ, AgInt no AREsp nº 1.948.228/PR, Rel. Min. Marco Aurélio Bellizze, 3ª Turma, j. 14.03.2022; STJ, REsp nº 1.497.831/PR, Rel. Min. Maria Isabel Gallotti, 2ª Seção, j. 14.09.2016; STJ, EAREsp nº 676.608/RS; Súmulas nº 530 e 539/STJ.

## CONTA-ENCARGOS — Débitos em conta sem lastro contratual (tarifas, seguros e títulos de capitalização)

Tese: Tarifas, seguros, títulos de capitalização e pacotes de serviços debitados na conta corrente sem previsão contratual expressa ou autorização do correntista são indevidos e devem ser restituídos e expurgados do saldo recomposto: não juntado o contrato, o ônus da prova é do banco (telas sistêmicas unilaterais não bastam), a exigência de pactuação alcança também tarifas anteriores a 30/04/2008 e o seguro imposto com a abertura da conta ou do limite é venda casada (CDC, art. 39, I; Tema 972/STJ).

### STJ · AgInt no REsp 2.017.968/PR
- regras: CONTA-ENCARGOS
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt no REsp 2.017.968/PR
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2024-07-01
- publicacao: 2024-07-08
- precedente_qualificado: não (aplica os Temas 618/619 e 972/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2939392900
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em revisão de conta corrente com contrato não exibido, a Quarta Turma afastou as tarifas sem previsão contratual — inclusive as anteriores a 30/04/2008, porque esse marco só diz respeito à TAC e à TEC — e declarou ilegal o seguro de vida debitado na conta sem livre contratação (Tema 972).
- observacao: Agravo interno do banco desprovido por unanimidade (sessão virtual de 25/06 a 01/07/2024), mantida a decisão que deu provimento ao recurso especial dos correntistas. O TJPR havia mantido as tarifas debitadas desde 1998 pela Res. CMN 2.303/1996 e o seguro 'por ser em favor dos correntistas'; o STJ tratou como revaloração jurídica (sem Súmula 7).

ementa:
> AGRAVO INTERNO NO RECURSO ESPECIAL. AÇÃO REVISIONAL. CONTRATO BANCÁRIO. TAXAS E TARIFAS. SERVIÇOS BANCÁRIOS. SEGURO. COBRANÇA. NECESSIDADE DE PACTUAÇÃO. DECISÃO MANTIDA. AGRAVO INTERNO DESPROVIDO.
> 1. As normas regulamentadoras editadas pela autoridade monetária permitem que as instituições financeiras efetuem cobranças administrativas de taxas e tarifas pela prestação de serviços bancários não isentos, desde que expressamente previstas no contrato.
> 2. Nos contratos bancários em geral, o consumidor não pode ser compelido a contratar seguro com a instituição financeira ou com seguradora por ela indicada.
> 3. Agravo interno desprovido.

### STJ · AgInt nos EDcl no REsp 2.048.901/PR
- regras: CONTA-ENCARGOS, R16, CONTA-EXIBICAO
- posicao: FAV
- tribunal: STJ
- classe_numero: AgInt nos EDcl no REsp 2.048.901/PR
- orgao: Quarta Turma
- relator: Min. João Otávio de Noronha
- julgamento: 2024-03-12
- publicacao: 2024-03-14
- precedente_qualificado: não (aplica a Súmula 530/STJ)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2939390777
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em revisão de conta corrente (abertura de limite de crédito), a Quarta Turma afastou as tarifas debitadas sem cláusula contratual expressa, inclusive as de 2001 a 2005 que o TJPR mantinha pela Res. CMN 2.303/1996, e limitou os juros à taxa média (Súmula 530) mesmo tendo a perícia apurado as taxas pelos extratos, porque o contrato não previa as taxas e o banco não apresentou outro instrumento.
- observacao: Agravo interno do banco desprovido por unanimidade (sessão virtual de 05 a 12/03/2024). Quanto aos juros do cheque especial, diverge do REsp 2.065.222/PR (mesma Turma, dez/2025; ver R16).

ementa:
> AGRAVO INTERNO NOS EMBARGOS DE DECLARAÇÃO EM RECURSO ESPECIAL. AÇÃO REVISIONAL. CONTRATO BANCÁRIO. JUROS REMUNERATÓRIOS. TAXA CONTRATADA. NECESSIDADE DE COMPROVAÇÃO. TAXAS E TARIFAS BANCÁRIAS. COBRANÇA. NECESSIDADE DE EXPRESSA PREVISÃO CONTRATUAL.
> 1. Nos contratos bancários, na impossibilidade de comprovar a taxa de juros efetivamente contratada - por ausência de pactuação ou pela falta de juntada do instrumento aos autos -, aplica-se a taxa média de mercado, divulgada pelo Bacen, praticada nas operações da mesma espécie, salvo se a taxa cobrada for mais vantajosa para o devedor.
> 2. As normas regulamentares editadas pela autoridade monetária facultam às instituições financeiras a cobrança administrativa de taxas e tarifas para a prestação de serviços bancários não isentos, desde que comprovadamente pactuadas mediante cláusula contratual expressa.
> 3. Agravo interno não provido.

### TJPR · Apelação Cível 0001681-42.2025.8.16.0055
- regras: CONTA-ENCARGOS
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0001681-42.2025.8.16.0055
- orgao: 15ª Câmara Cível
- relator: Des. Luiz Cezar Nicolau
- julgamento: 2026-08-29
- publicacao: 2026-08-31
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000038747221/Ac%C3%B3rd%C3%A3o-0001681-42.2025.8.16.0055
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Em conta corrente: o seguro do limite (LIS) contratado no próprio instrumento de abertura, sem apólice nem escolha de seguradora, é venda casada (CDC, art. 39, I; Tema 972); títulos de capitalização, seguros e pacotes de serviços sem prova inequívoca de contratação — telas sistêmicas não bastam — são cobrança indevida, com restituição e dano moral (conta de benefício previdenciário).
- observacao: Recurso da correntista parcialmente provido; mantida só a tarifa de extrato excedente, prevista no contrato e na Res. CMN 3.919/2010. ATENÇÃO à repetição: o acórdão aplica a modulação do EAREsp 676.608/RS (dobro só a partir de 31/03/2021) — o Tema 929/STJ (REsp 1.963.770/CE, em R26) foi fixado sem modulação; não citar este julgado para o dobro. A íntegra do portal não repete o número do processo, mas descreve o mesmo caso. Fonte: portal de jurisprudência do TJPR (comarca de Cambará).

ementa:
> AÇÃO DECLARATÓRIA DE INEXISTÊNCIA DE DÉBITO CUMULADA COM REPETIÇÃO DE INDÉBITO E INDENIZAÇÃO POR DANO MORAL POR COBRANÇA INDEVIDA DE TAXAS E TARIFAS BANCÁRIAS NÃO CONTRATADAS. SEGURO LIS, SEGURO DE VIDA, SEGURO RESIDENCIAL, SEGURO CARTÃO PROTEGIDO, PIC (TÍTULO DE CAPITALIZAÇÃO), COMBINAQUI, PACOTE DE SERVIÇOS DE CONTA CORRENTE E TARIFA DE MOVIMENTAÇÃO DE EXTRATO. IMPROCEDÊNCIA DOS PEDIDOS. INSURGÊNCIA DA AUTORA.(A) SEGURO LIS. CONTRATAÇÃO DO SEGURO NO MESMO INSTRUMENTO DE ABERTURA DA CONTA, SEM APÓLICE OU DEMONSTRAÇÃO DA POSSIBILIDADE DE ESCOLHA DE OUTRA SEGURADORA. VENDA CASADA. PRÁTICA ABUSIVA (CDC, ART. 39, INCISO I). NULIDADE DO CONTRATO DE SEGURO. ORIENTAÇÃO DO SUPERIOR TRIBUNAL DE JUSTIÇA NO RECURSO ESPECIAL REPETITIVO 1.639.320/SP (TEMA 972).(B) TÍTULOS DE CAPITALIZAÇÃO (PIC), SEGURO DE VIDA, SEGURO CARTÃO PROTEGIDO, SEGURO RESIDENCIAL, PACOTES DE SERVIÇO DE CONTA CORRENTE E SERVIÇO COMBINAQUI. AUSÊNCIA DE PROVA INEQUÍVOCA DA CONTRATAÇÃO DOS SERVIÇOS. TELAS SISTÊMICAS SEM INDICAÇÃO DE FORMA E LOCAL OU DISPOSITIVO DE CONTRATAÇÃO. COBRANÇA INDEVIDA.(C) TARIFA DE MOVIMENTAÇÃO DE EXTRATO. SERVIÇO EXCEDENTE PREVISTO NO CONTRATO DE ABERTURA DE CONTA E NAS CONDIÇÕES GERAIS. PREVISÃO NA RESOLUÇÃO 3919/2010 DO BACEN. AUTORA QUE NÃO CONTROVERTEU O FORNECIMENTO DO EXTRATO, APENAS A COBRANÇA DA TARIFA. COBRANÇA REGULAR.(D) APLICAÇÃO DO INSTITUTO DA SUPRESSIO. IMPOSSIBILIDADE. INEXISTÊNCIA DE RELAÇÃO CONTRATUAL ENTRE AS PARTES. NÃO CARACTERIZAÇÃO DE LEGÍTIMA EXPECTATIVA DE UMA DAS PARTES EM VER MANTIDA UMA OBRIGAÇÃO QUE JAMAIS FOI FIRMADA. APLICAÇÃO DO INSTITUTO QUE SERIA CONTRÁRIA A BOA-FÉ OBJETIVA.(E) REPETIÇÃO DO INDÉBITO. CONSEQUÊNCIA DO RECONHECIMENTO DA COBRANÇA ILEGAL. VEDAÇÃO AO ENRIQUECIMENTO ILÍCITO. REPETIÇÃO EM DOBRO (CDC, ART. 42, PARÁGRAFO ÚNICO). APLICABILIDADE PARCIAL DA TESE FIRMADA NO ERESP 1.413.542/RS, ANTE A MODULAÇÃO DE EFEITOS. ENTENDIMENTO JURISPRUDENCIAL ANTERIOR ACERCA DA NECESSIDADE DE COMPROVAÇÃO DA MÁ-FÉ DO FORNECEDOR. PARTE AUTORA QUE NÃO SE DESINCUMBIU DESTE ÔNUS. CABIMENTO DA RESTITUIÇÃO EM DOBRO APENAS DOS VALORES COBRADOS POSTERIORMENTE À PUBLICAÇÃO DO ACÓRDÃO PELA CORTE SUPERIOR.(F) DANO MORAL. CARACTERIZAÇÃO. BANCO QUE RESPONDE OBJETIVAMENTE POR FORTUITO INTERNO. DANO EVIDENCIADO. DESCONTOS INDEVIDOS EM CONTA CORRENTE NA QUAL A AUTORA RECEBE BENEFÍCIO PREVIDENCIÁRIO. VERBA DE NATUREZA ALIMENTAR ESSENCIAL AO SEU SUSTENTO.(G) VALOR DA INDENIZAÇÃO. UTILIZAÇÃO DO MÉTODO BIFÁSICO ORIENTADO PELO SUPERIOR TRIBUNAL DE JUSTIÇA. TÉCNICA DO GRUPO DE CASOS ATRELADA À ANÁLISE DAS CIRCUNSTÂNCIAS DO CASO CONCRETO. COMPENSAÇÃO ARBITRADA EM OITO MIL REAIS.(H) ÔNUS DA SUCUMBÊNCIA. DECAIMENTO MÍNIMO DA AUTORA. RESPONSABILIZAÇÃO INTEGRAL DO RÉU PELO RECOLHIMENTO DAS CUSTAS PROCESSUAIS E PELO PAGAMENTO DOS HONORÁRIOS ADVOCATÍCIOS. ART. 86, PARÁGRAFO ÚNICO, DO CPC.RECURSO PARCIALMENTE PROVIDO.

## CONTA-EXIBICAO — Exibição do contrato e dos extratos pela instituição financeira

Tese: Na revisão de conta corrente, cheque especial ou conta garantida, a instituição financeira deve exibir o instrumento de abertura da conta e do limite, os aditivos e os extratos do período (arts. 396 a 404 do CPC), obrigação legal que, pedida dentro da ação, não depende de prévio requerimento administrativo nem de pagamento de custo; a recusa ou a omissão injustificada faz presumir verdadeiros os fatos que o correntista pretendia provar (art. 400 do CPC) — em especial a falta de pactuação da taxa, da capitalização e das tarifas — e admite multa coercitiva nos termos do Tema 1000/STJ.

### STJ · REsp 1.388.972/SC
- regras: CONTA-EXIBICAO, R19, CONTA-CAPDIARIA
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.388.972/SC
- orgao: Segunda Seção
- relator: Min. Marco Buzzi
- julgamento: 2017-02-08
- publicacao: 2017-03-13
- precedente_qualificado: Tema 953/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106307171
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Repetitivo julgado em revisional de contratos de conta corrente, limite de crédito e capital de giro: não exibidos os contratos apesar da ordem judicial, aplica-se ao banco a pena do art. 359 do CPC/73 (art. 400 do CPC/2015), tendo-se por verdadeira a não pactuação dos encargos, e a capitalização em qualquer periodicidade só é cobrada com pactuação expressa (Tema 953).
- observacao: A tese repetitiva é a do item 1.1 (capitalização); a aplicação do art. 359/400 está no caso concreto (item 2.2) e no voto, que a estende à 'não pactuação ou abusividade dos encargos cobrados'. Autora microempresa, com o CDC aplicado; unânime no resultado (vencidos quatro ministros só quanto à redação da tese). Correção: 'ara' por 'para' no item 2.5 (erro de digitação).

ementa:
> RECURSO ESPECIAL REPRESENTATIVO DE CONTROVÉRSIA - ARTIGO 1036 E SEGUINTES DO CPC/2015 - AÇÃO REVISIONAL DE CONTRATOS BANCÁRIOS - PROCEDÊNCIA DA DEMANDA ANTE A ABUSIVIDADE DE COBRANÇA DE ENCARGOS - INSURGÊNCIA DA CASA BANCÁRIA VOLTADA À PRETENSÃO DE COBRANÇA DA CAPITALIZAÇÃO DE JUROS
> 1. Para fins dos arts. 1036 e seguintes do CPC/2015.
> 1.1 A cobrança de juros capitalizados nos contratos de mútuo é permitida quando houver expressa pactuação.
> 2. Caso concreto:
> 2.1 Quanto aos contratos exibidos, a inversão da premissa firmada no acórdão atacado acerca da ausência de pactuação do encargo capitalização de juros em qualquer periodicidade demandaria a reanálise de matéria fática e dos termos dos contratos, providências vedadas nesta esfera recursal extraordinária, em virtude dos óbices contidos nos Enunciados 5 e 7 da Súmula do Superior Tribunal de Justiça.
> 2.2 Relativamente aos pactos não exibidos, verifica-se ter o Tribunal a quo determinado a sua apresentação, tendo o banco-réu, ora insurgente, deixado de colacionar aos autos os contratos, motivo pelo qual lhe foi aplicada a penalidade constante do artigo 359 do CPC/73 (atual 400 do NCPC), sendo tido como verdadeiros os fatos que a autora pretendia provar com a referida documentação, qual seja, não pactuação dos encargos cobrados.
> 2.3 Segundo a jurisprudência do Superior Tribunal de Justiça, é possível tanto a compensação de créditos quanto a devolução da quantia paga indevidamente, independentemente de comprovação de erro no pagamento, em obediência ao princípio que veda o enriquecimento ilícito. Inteligência da Súmula 322/STJ.
> 2.4 Embargos de declaração manifestados com notório propósito de prequestionamento não tem caráter protelatório. Inteligência da súmula 98/STJ.
> 2.5 Recurso especial parcialmente provido apenas para afastar a multa imposta pelo Tribunal a quo.

### STJ · REsp 1.133.872/PB
- regras: CONTA-EXIBICAO
- posicao: FAV
- tribunal: STJ
- classe_numero: REsp 1.133.872/PB
- orgao: Segunda Seção
- relator: Min. Massami Uyeda
- julgamento: 2011-12-14
- publicacao: 2012-03-28
- precedente_qualificado: Tema 411/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106305749
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Repetitivo: na ação em que o correntista discute a conta, cabe inverter o ônus para que o banco exiba os extratos, obrigação legal e de integração contratual compulsória que não se sujeita a recusa nem a condicionantes (adiantamento de custos ou prévia recusa administrativa); ao correntista cabe indicar a relação e os períodos.
- observacao: Caso de expurgos de poupança, com a exibição dos extratos determinada dentro da própria ação de cobrança. É o contraponto do Tema 648 (ADV, abaixo): prévio pedido e pagamento do custo são requisitos da ação cautelar autônoma, não da exibição pedida dentro da revisional. A peça deve especificar contas e períodos. Unânime. Correção: 'incindindo' por 'incidindo' no item III (erro de digitação).

ementa:
> RECURSO ESPECIAL REPETITIVO (ART. 543-C DO CPC)- AÇÃO DE COBRANÇA - EXPURGOS INFLACIONÁRIOS EM CADERNETA DE POUPANÇA - PLANOS BRESSER E VERÃO - PRELIMINAR - PRESCRIÇÃO VINTENÁRIA - NÃO-OCORRÊNCIA - EXIBIÇÃO DOS EXTRATOS BANCÁRIOS - INVERSÃO DO ÔNUS DA PROVA EM FAVOR DA CORRENTISTA - POSSIBILIDADE - OBRIGAÇÃO DECORRENTE DE LEI - CONDICIONAMENTO OU RECUSA - INADMISSIBILIDADE - RESSALVA - DEMONSTRAÇÃO DE INDÍCIOS MÍNIMOS DA EXISTÊNCIA DA CONTRATAÇÃO - INCUMBÊNCIA DO AUTOR (ART. 333, I, DO CPC)- ART. 6º DA LEI DE INTRODUÇÃO AO CÓDIGO CIVIL - AUSÊNCIA DE PREQUESTIONAMENTO - INCIDÊNCIA DO ENUNCIADO N. 211/STJ - NO CASO CONCRETO, RECURSO ESPECIAL IMPROVIDO.
> I - Preliminar: nas ações em que se discutem os critérios de remuneração de caderneta de poupança e são postuladas as respectivas diferenças de correção monetária e dos juros remuneratórios, o prazo prescricional é de vinte anos, não transcorrido, na espécie;
> II - A obrigação da instituição financeira de exibir os extratos bancários necessários à comprovação das alegações do correntista decorre de lei, já que se trata de relação jurídica tutelada pelas normas do Código do Consumidor, de integração contratual compulsória, não podendo ser objeto de recusa nem de condicionantes, em face do princípio da boa-fé objetiva;
> III - A questão relativa ao art. 6º da LICC não foi objeto de debate no v. acórdão recorrido, ressentindo-se o especial, portanto, do indispensável prequestionamento, incidindo, na espécie, o Enunciado n. 211/STJ;
> IV - Para fins do disposto no art. 543-C, do Código de Processo Civil, é cabível a inversão do ônus da prova em favor do consumidor para o fim de determinar às instituições financeiras a exibição de extratos bancários, enquanto não estiver prescrita a eventual ação sobre eles, tratando-se de obrigação decorrente de lei e de integração contratual compulsória, não sujeita à recusa ou condicionantes, tais como o adiantamento dos custos da operação pelo correntista e a prévia recusa administrativa da instituição financeira em exibir os documentos, com a ressalva de que ao correntista, autor da ação, incumbe a demonstração da plausibilidade da relação jurídica alegada, com indícios mínimos capazes de comprovar a existência da contratação, devendo, ainda, especificar, de modo preciso, os períodos em que pretenda ver exibidos os extratos;
> V - Recurso especial improvido, no caso concreto.

### STJ · REsp 1.349.453/MS
- regras: CONTA-EXIBICAO
- posicao: ADV
- tribunal: STJ
- classe_numero: REsp 1.349.453/MS
- orgao: Segunda Seção
- relator: Min. Luis Felipe Salomão
- julgamento: 2014-12-10
- publicacao: 2015-02-02
- precedente_qualificado: Tema 648/STJ (repetitivo)
- url: https://www.jusbrasil.com.br/jurisprudencia/stj/2106314257
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: LIMITE a antecipar: a ação cautelar autônoma de exibição de documentos bancários exige relação jurídica, prévio pedido à instituição não atendido em prazo razoável e pagamento do custo do serviço; para evitar a extinção, pedir a exibição dentro da revisional (Tema 411) ou instruir a cautelar com o protocolo do pedido administrativo e o comprovante da tarifa.
- observacao: Caso de expurgos de poupança: o recurso da poupadora foi provido para restabelecer a sentença que acolhera a cautelar contra o banco; a tese repetitiva é que fixa os requisitos da cautelar autônoma. O voto lembra que a exibição pedida na ação principal já é regida pelo Tema 411 (REsp 1.133.872/PB, acima). Sobre multa: a Súmula 372/STJ ('na ação de exibição de documentos, não cabe a aplicação de multa cominatória') consta vigente no catálogo do BNP, mas o Tema 1000/STJ (REsp 1.763.462/MG, Segunda Seção, 09/06/2021, transitado) admite multa no CPC/2015, incidental ou autônoma, após contraditório e tentativa de busca e apreensão ou outra medida — o Tema 1000 não foi aberto nesta pesquisa (texto conferido no Radar).

ementa:
> PROCESSO CIVIL. RECURSO ESPECIAL REPRESENTATIVO DE CONTROVÉRSIA. ART. 543-C DO CPC. EXPURGOS INFLACIONÁRIOS EM CADERNETA DE POUPANÇA. EXIBIÇÃO DE EXTRATOS BANCÁRIOS. AÇÃO CAUTELAR DE EXIBIÇÃO DE DOCUMENTOS. INTERESSE DE AGIR. PEDIDO PRÉVIO À INSTITUIÇÃO FINANCEIRA E PAGAMENTO DO CUSTO DO SERVIÇO. NECESSIDADE.
> 1. Para efeitos do art. 543-C do CPC, firma-se a seguinte tese: A propositura de ação cautelar de exibição de documentos bancários (cópias e segunda via de documentos) é cabível como medida preparatória a fim de instruir a ação principal, bastando a demonstração da existência de relação jurídica entre as partes, a comprovação de prévio pedido à instituição financeira não atendido em prazo razoável, e o pagamento do custo do serviço conforme previsão contratual e normatização da autoridade monetária.
> 2. No caso concreto, recurso especial provido.

### TJPR · Apelação Cível 0002541-25.2018.8.16.0108
- regras: CONTA-EXIBICAO, R16, R19, CONTA-ENCARGOS
- posicao: FAV
- tribunal: TJPR
- classe_numero: Apelação Cível 0002541-25.2018.8.16.0108
- orgao: 14ª Câmara Cível
- relator: Juiz Subst. 2º Grau Eduardo Novacki
- julgamento: 2026-03-30
- publicacao: 2026-04-06
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035460091/Ac%C3%B3rd%C3%A3o-0002541-25.2018.8.16.0108
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Revisão de abertura de crédito em conta corrente: a não exibição dos contratos, apesar de reiteradas ordens judiciais, faz presumir verdadeiros os fatos que o correntista pretendia provar (art. 400 do CPC), com taxa média de mercado (Súmula 530), expurgo da capitalização não pactuada e restituição do seguro e do consórcio debitados sem contratação válida (venda casada).
- observacao: Correntista pessoa jurídica; apelação do banco desprovida; repetição simples mantida. A íntegra do portal não repete o número do processo, mas descreve o mesmo caso (comarca, partes e pedidos conferidos). Fonte: portal de jurisprudência do TJPR (comarca de Mandaguaçu).

ementa:
> DIREITO BANCÁRIO. APELAÇÃO CÍVEL. AÇÃO REVISIONAL DE CONTRATO BANCÁRIO. SENTENÇA DE PARCIAL PROCEDÊNCIA. CONTRATO DE ABERTURA DE CRÉDITO EM CONTA CORRENTE. NÃO EXIBIÇÃO DOS CONTRATOS. APLICAÇÃO DO ART. 400 DO CPC. PRESUNÇÃO DE VERACIDADE DAS ALEGAÇÕES AUTORAIS. LIMITAÇÃO DOS JUROS REMUNERATÓRIOS À TAXA MÉDIA DE MERCADO. CAPITALIZAÇÃO DE JUROS. NECESSIDADE DE PACTUAÇÃO EXPRESSA. COBRANÇA DE SEGURO E CONSÓRCIO SEM COMPROVAÇÃO DE CONTRATAÇÃO VÁLIDA. VENDA CASADA. CONFIGURAÇÃO. REPETIÇÃO SIMPLES DO INDÉBITO. HONORÁRIOS RECURSAIS. RECURSO DE APELAÇÃO CONHECIDO E DESPROVIDO.I. CASO EM EXAMEAção revisional de contrato bancário julgada parcialmente procedente para reconhecer a ilegalidade da capitalização de juros, da cobrança de juros superiores à taxa média de mercado e da cobrança de valores referentes a seguro e consórcio, com condenação à restituição simples do indébito. Sustenta a instituiçãofinanceira em suas razões recursais, a regularidade da taxa de juros flutuante, a inexistência de capitalização de juros, a legalidade das cobranças de seguro e consórcio e a inaplicabilidade do art. 400 do CPCII. QUESTÕES EM DISCUSSÃODiscute-se: (a) a aplicação do art. 400 do CPC em razão da não exibição dos contratos bancários; (b) a legalidade da capitalização de juros sem pactuação expressa; (c) a abusividade dos juros remuneratórios e a possibilidade de limitação à taxa média de mercado; (d) a regularidade da cobrança de seguro e consórcio sem comprovação de contratação válida ou autorização expressa; e (e) o cabimento da majoração dos honorários advocatícios em grau recursal, nos termos do art. 85, § 11, do CPC.III. RAZÕES DE DECIDIR1. A não exibição dos contratos bancários, apesar de reiteradas determinações judiciais, autoriza a aplicação das penalidades previstas no art. 400 do CPC, presumindo-se verdadeiros os fatos que a parte autora pretendia demonstrar por meio da prova documental.2. A capitalização de juros em periodicidade inferior à anual é admitida apenas quando expressamente pactuada em contratos firmados após a vigência da Medida Provisória nº 2.170-36/2001, o que não restou comprovado nos autos.3. Na ausência de comprovação da taxa de juros efetivamente contratada, impõe-se a aplicação da taxa média de mercado divulgada pelo Banco Central do Brasil, nos termos da Súmula 530 do Superior Tribunal de Justiça.4. A cobrança de seguro e de consórcio sem prova de contratação válida ou de autorização expressa configura prática abusiva, vedada pelo art. 39, inc. I, do CDC, caracterizando venda casada.5. Mantida a condenação à restituição simples dos valores cobrados indevidamente.6. Com o desprovimento do recurso, é devida a majoração dos honorários advocatícios, nos termos do art. 85, §11, do CPC.7. Jurisprudência relevante do Superior Tribunal de Justiça e deste Tribunal de Justiça do Paraná aplicada ao caso concreto.IV. DISPOSITIVO E TESERecurso de apelação conhecido e desprovido.Teses de julgamento: a) A não exibição de contratos bancários autoriza a aplicação do art. 400 do CPC, com presunção de veracidade das alegações do consumidor; b) A capitalização de juros exige pactuação expressa, sendo indevida na ausência de comprovação contratual; c) Na impossibilidade de comprovação da taxa de juros contratada, aplica-se a taxa média de mercado; d) É abusiva a cobrança de seguro e consórcio sem contratação válida ou autorização expressa; e) Mantida a restituição simples do indébito e majorados os honorários recursais.DISPOSITIVOS RELEVANTES:CPC/2015, arts. 85, §11; 373, II; 400; 1.009.CDC, arts. 6º, VIII; 39, I; 42.MEDIDA PROVISÓRIA Nº 2.170-36/2001, art. 5º.SÚMULAS DO STJ: 530, 539.JURISPRUDÊNCIA:STJ, REsp 1.061.530/RS.STJ, REsp 1.388.972/SC.TJPR, 14ª Câmara Cível, Apelação Cível 0011720-86.2023.8.16.0017.TJPR, 14ª Câmara Cível, Apelação Cível 0004927-34.2023.8.16.0017.

### TJPR · Agravo de Instrumento 0078285-15.2025.8.16.0000
- regras: CONTA-EXIBICAO
- posicao: FAV
- tribunal: TJPR
- classe_numero: Agravo de Instrumento 0078285-15.2025.8.16.0000
- orgao: 14ª Câmara Cível
- relator: Des. Iraja Pigatto Ribeiro
- julgamento: 2026-03-16
- publicacao: 2026-03-19
- precedente_qualificado: não
- url: https://portal.tjpr.jus.br/jurisprudencia/j/4100000034278511/Ac%C3%B3rd%C3%A3o-0078285-15.2025.8.16.0000
- verificado_em: 2026-11-16
- status: VERIFICADO
- uso_na_peca: Na revisional de conta corrente, mantida a ordem de exibição do contrato de abertura, dos aditivos e dos extratos sob multa diária limitada (Tema 1000/STJ, após contraditório e busca e apreensão frustrada), com a advertência da presunção do art. 400 do CPC, que decorre do próprio art. 400 e independe da vulnerabilidade do correntista.
- observacao: Agravo do banco conhecido em parte e desprovido; correntista pessoa jurídica, com documentos pedidos havia cerca de 16 anos em ação anterior. Fonte: portal de jurisprudência do TJPR (comarca de Cidade Gaúcha). Correção: retirado o rótulo 'Ementa:' que abre o texto do portal.

ementa:
> Direito processual civil. Agravo de instrumento. Ação revisional de conta corrente. Exibição de documentos bancários. Imposição de astreintes. Art. 400 do CPC. Tema 1.000 do STJ. Multa mantida. Recurso conhecido em parte e não provido.I. Caso em exame1. Agravo de instrumento interposto contra a decisão proferida em ação revisional de conta corrente com pedido de repetição do indébito, que determinou ao recorrente a exibição do contrato de abertura de conta bancária, eventuais aditamentos, extratos e demais documentos vinculados, no prazo de 30 dias, sob pena de multa diária limitada, bem como advertiu acerca da presunção de veracidade em caso de recusa injustificada.II. Questão em discussão2. Há duas questões em discussão: (i) definir a possibilidade de imposição de multa diária para compelir a instituição financeira à exibição de documentos bancários, à luz do art. 400 do CPC e do Tema 1.000 do STJ; e (ii) estabelecer se o valor da multa fixada é excessivo ou desproporcional, a justificar sua redução ou afastamento.III. Razões de decidir3. Não há interesse recursal quanto à discussão sobre a inaplicabilidade do Código de Defesa do Consumidor e da inversão do ônus da prova, objeto de decisão anterior transitada em julgado.4. Exibição de documentos, sob pena de multa. Requisitos fixados pelo STJ no Tema Repetitivo n. 1.000 suficientemente demonstrados. Prova da relação jurídica entre as partes e probabilidade da existência dos documentos pretendidos. Ocorrência de contraditório prévio e de tentativa infrutífera de busca e apreensão.5. Multa diária fixada em valor moderado e limitada a montante máximo adequados e proporcionais ao longo lapso temporal de inadimplemento da obrigação de exibição e à expressiva capacidade econômica da instituição financeira, cumprindo, dentro de parâmetros de razoabilidade, o efeito coercitivo que lhe é próprio.IV. Dispositivo e teses6. Recurso conhecido em parte e não provido._______________Teses de julgamento: “1. É cabível a imposição de multa diária para compelir a parte à exibição de documentos, uma vez observados os requisitos do art. 400 do CPC e fixados pelo STJ no Tema Repetitivo n.1.000. 2. A multa cominatória fixada em valor razoável e proporcional, diante da capacidade econômica do obrigado e da renitência histórica da parte em cumprir a obrigação processual, não comporta redução.Dispositivos relevantes citados: CPC, arts 400, caput e parágrafo único, e 1.040.Jurisprudência relevante citada: STJ, REsp n. 1.763.462/MG, Rel. Min. PAULO DE TARSO SANSEVERINO, Segunda Seção, j. 09/6/2021.
