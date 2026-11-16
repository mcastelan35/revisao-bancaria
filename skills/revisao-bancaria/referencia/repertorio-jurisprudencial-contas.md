# Repertório jurisprudencial — rota CONTA

Status: **validado** (onda 6, 16/11/2026). As teses da rota CONTA (conta corrente, cheque especial
e conta garantida) estão no repertório principal, `referencia/repertorio-jurisprudencial.md`, com a
mesma regra de entrada das demais: ementa integral lida no inteiro teor (Jusbrasil ou portal do
TJPR), identificação completa e link. Este arquivo é o mapa; os julgados saem só pelo motor:

```
<rb> jurisprudencia consultar --regras CONTA-CAPDIARIA,CONTA-HAMBURGUES,CONTA-ENCARGOS,CONTA-EXIBICAO,R16,R26
```

Nada se cita de memória nem fora do que a consulta devolve (regra de conduta 3). Os laudos de
terceiros usados como corpus de referência invocavam fundamentos revogados — art. 192, §3º, da CF,
teto de 12% a.a., Lei de Usura como vedação absoluta —, banidos pela regra de conduta 19.

## Mapa das teses

| Tese da rota | Onde está no repertório | Julgados (STJ FAV / STJ ADV / local FAV) | Observação |
|---|---|---|---|
| 1. Capitalização diária sem pactuação expressa | `CONTA-CAPDIARIA` (e entradas da R19 ligadas a ela) | 2 / 1 / 2, mais os da R19 | **Tema 1474/STJ afetado**: se a capitalização diária exige a taxa diária expressa (pendência das R18 e R19). Sem contrato nos autos, a pactuação não se presume; com taxas mensal e anual, cai a diária e fica a mensal; sem nada pactuado, juros simples |
| 2. Taxa não comprovada em cheque especial e conta garantida (Súmula 530) | `R16` | 2 / 1 / 2 | Quarta Turma dividida no cheque especial; no TJPR, a 14ª Câmara Cível afasta e a 13ª, a 15ª e a 16ª aplicam (alerta da R16) |
| 3. Saldo devedor diário (método hamburguês) na perícia | `CONTA-HAMBURGUES` | 1 / 0 / 2 | O STJ não julga a metodologia (Súmula 7); o FAV sustenta só que o demonstrativo unilateral do banco, impugnado, não prova o débito. O laudo declara a base de dias adotada (o TJPR diverge) |
| 4. Débitos em conta sem lastro contratual | `CONTA-ENCARGOS` | 2 / 0 / 1, mais os ligados | Tarifa só com cláusula expressa, inclusive antes de 30/04/2008; seguro pelo Tema 972 |
| 5. Comissão de permanência disfarçada em encargos de conta | `R03` | os da R03 | Mesma tese da rota de contratos, pela função do encargo |
| 6. Exibição do contrato e dos extratos | `CONTA-EXIBICAO` | 2 / 1 / 2 | Pedida dentro da revisional, sem pedido administrativo nem custo (Tema 411); o Tema 648 (ADV) vale para a cautelar autônoma; multa do Tema 1000 depois de frustrada a busca e apreensão |
| 7. Repetição em dobro de encargos de conta | `R26` | os da R26 | Tema 929 sem modulação: dobro para a cobrança sem lastro contratual, em qualquer data; engano justificável (i.c) vai à base simples |

## Como entra no laudo e na petição

- A C6 fundamenta com a consulta acima e o espelho da petição sai pelo `<rb> espelho`, com os
  achados do payload apontando em `regras` para os ids da tabela (`["CONTA-CAPDIARIA", "R19"]`).
- Vários acórdãos do TJPR desta rota ainda aplicaram a modulação antiga do EAREsp 676.608: para a
  forma da devolução, vale a R26 (Tema 929), não o que eles decidiram sobre a data.
- Revalidar cada entrada um ano depois do `verificado_em`; pesquisa nova pelo mesmo procedimento
  (`pesquisa-jurisprudencial-jusia`, inteiro teor lido, ementa integral).
