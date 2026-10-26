# L2b — Procedimento expropriatório (SFH/SFI)

Camada do plugin `revisao-bancaria`. Entra na L2 do ramo SFH/SFI sempre que os
autos contiverem consolidação da propriedade, leilão, execução extrajudicial ou intimação
(R39 e R40). Não calcula nada: é checklist documental com semáforo. É a frente mais forte do
ramo porque não depende de conta gráfica nem de perícia — depende de certidão.

## Por que existe

Em SFH/SFI as teses de encargo (juros, Price, TR, taxa de administração, seguro) estão
esgotadas em STJ e TRF4. O que ainda anula o procedimento é falha de notificação: edital
publicado sem esgotar a localização pessoal do devedor, e ciência dos leilões tratada como se
suprisse a intimação para purgar (REsp 2.107.242/ES, 17/08/2026; REsp 2.218.731/PE,
23/10/2025). O contrário também é firme e precisa estar no laudo: edital é válido se a
notificação pessoal foi frustrada (REsp 1.698.322/RJ) ou recusada (TRF4 AC 5008761-44, só
trecho); no DL 70/66 a nulidade exige prejuízo concreto (REsp 1.977.553/SP); e a comunicação
dos leilões se faz por correspondência aos endereços do contrato, não por intimação pessoal
(TRF4 AC 5000201-87.2022.4.04.7209; art. 27, §2º-A). Laudo que omite o lado contrário é peça
de parte — regra de conduta 8.

## Entrada

Da L0: `data_contrato`, `data_consolidacao`, `enderecos_contrato` (inclusive e-mail),
matrícula atualizada, certidões do cartório de títulos e documentos, edital, comunicações
dos leilões, autos de leilão/arrematação. Documento ausente é pedido ao usuário e, se
inexistente nos autos, vira requerimento de exibição no briefing — nunca presunção.

## Checklist (um semáforo por item)

| # | Item | Fonte | Verde | Vermelho (achado) | Amarelo |
|---|---|---|---|---|---|
| 1 | Diligências pessoais antes do edital | Certidão do RTD: número, datas, endereços tentados, resultado | Diligências em todos os endereços do contrato, certificadas, antes do edital | Edital sem certidão de diligência, ou diligência em endereço diverso do contratual (R39) | Certidão genérica ("não localizado") sem datas ou endereços |
| 2 | Prazo de purga | Intimação (art. 26, §1º) | 15 dias contados da intimação válida | Consolidação averbada antes do 15º dia | Contagem ambígua (recebimento × publicação) |
| 3 | Recusa × frustração | Certidão | Recusa expressa e certificada (edital válido) | — | Frustração por ausência sem nova tentativa |
| 4 | Averbação da consolidação | Matrícula | Averbada após o prazo, com os requisitos do art. 26, §7º | Averbação sem prova do ITBI ou sem a intimação válida | Data da averbação não localizada |
| 5 | Comunicação dos leilões | Correspondência aos endereços do contrato (art. 27, §2º-A) | Enviada aos endereços e e-mail contratuais | Nenhuma comunicação | Enviada a endereço diverso sem atualização cadastral pelo devedor |
| 6 | Prazo dos leilões (30 dias) | Matrícula × edital | Dentro do prazo | — | Fora do prazo: mera irregularidade, não anula (TRF4 AC 5000201-87) — vai em ressalvas |
| 7 | Preço no 2º leilão | Edital, auto | Maior lance ≥ dívida + encargos (art. 27, §2º) | Lance abaixo do piso legal | Preço vil alegado contra avaliação: tese fraca (>50% da avaliação não é vil — TRF4 AG 5024900-07) |
| 8 | Purga tardia (R40) | Datas do contrato e da consolidação × 11/07/2017 | Ambas anteriores: tese forte | Ambas posteriores: não há tese | Só o contrato anterior: divergência STJ (REsp 2.187.505 × 2.005.064) — decisão do advogado |
| 9 | Prejuízo concreto (DL 70/66) | Proposta de purga, depósito, tentativa de renegociação | Prova nos autos | — | Sem prova: a nulidade formal não basta (REsp 1.977.553) — juntar antes de ajuizar |

## Saída (volta à L2)

Lista de achados R39/R40 com tier, documentos faltantes para exibição, e o bloco contrário
já redigido para `ressalvas`. No briefing da L4: requerer exibição das certidões do RTD e do
auto de leilão quando ausentes; em DL 70/66, instruir a prova do prejuízo. Precedentes entram
no laudo só com identificação completa (regra de conduta 3): os do JSON estão `[CONFERIR]`
quanto a relator, órgão e data de julgamento até que o operador complete no portal.
