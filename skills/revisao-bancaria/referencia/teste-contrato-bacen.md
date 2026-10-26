# Teste de contrato — catálogo BACEN do conector

Regressão que alarma quando a identidade de uma série muda no conector. **Não roda em toda
análise.** Rode quando o conector for atualizado, quando uma série mapeada não responder, ou
periodicamente — nunca como pré-requisito de um laudo.

## Por que deixou de ser rotina (v4.4)

A versão anterior mandava rodar a bateria "antes de confiar em qualquer série numa análise".
Custava **sete chamadas** por caso, todas de verificação e nenhuma de dado, e duas delas — as
probes de identidade e o teste de não-aliasing 11×12 — disparavam alarme falso garantido contra o
conector atual. Chamada de ferramenta é a unidade de quota do aluno.

O que mudou no conector e tornou a bateria dispensável no caminho normal:

- `listar_series_bacen` publica a **identidade autoritativa** (nome, unidade, periodicidade,
  segmento) e a cobertura do cache, numa chamada, sem tocar API externa. É a mesma identidade que
  `consultar_taxa_bacen`, `consultar_indice` e `atualizar_debito` usam — travada por teste no
  próprio conector.
- O catálogo foi reconstruído contra o Portal de Dados Abertos do BCB: **226 é TR**, 12 é CDI, 11
  é Selic fator diário, e as 254xx são as mensais corretas por modalidade.
- `consultar_taxa_bacen` devolve nome, unidade, periodicidade e segmento preenchidos. Não há mais
  o que "confirmar por segunda tool".

**Não existe aliasing 11≡12 no conector.** Selic e CDI publicam fator diário muito próximo — isso
é o mercado, e a chave de cache inclui o código da série. Testar "bytes diferentes" entre as duas
produz alarme sobre um não-defeito.

## Snapshot de referência (verificado ago/2026; catálogo reconferido em 26/10/2026)

Fonte de verdade: Portal de Dados Abertos do BCB / SGS. Na reconferência de 26/10/2026,
`listar_series_bacen({})` devolveu um catálogo de 48 códigos; os 24 do mapeamento `series_bacen_por_modalidade`
estavam todos presentes, com o mesmo nome e unidade `% a.m.`. Cache: modalidades até a
competência 2026-08, índices até 2026-09; a 29543 (taxa legal) sem competência materializada.

| Código | Identidade oficial | Unidade | Papel |
|---|---|---|---|
| 12 | CDI — diário | % a.d. | indexador pós-fixado |
| 11 | Selic — fator diário | % a.d. | indexador pós-fixado |
| 226 | TR — diária | % a.d. | indexador; **não é CDI** |
| 433 | IPCA — variação mensal | % a.m. | correção monetária |
| 188 | INPC — variação mensal | % a.m. | correção monetária |
| 4390 | Selic acumulada no mês | % a.m. | juros do motor de débitos |
| 4189 | Selic acumulada no mês anualizada (base 252) | % a.a. | referência |
| 432 | Selic meta (COPOM) | % a.a. | referência |
| 7811 | TR — mensal | % a.m. | índice do saldo (SFH/SFI) |
| 196 | Poupança — mensal | % a.m. | índice do saldo (SFH/SFI) |
| 195 / 25 | Poupança — diária (regra nova / antiga) | % a.d. | índice do saldo (SFH/SFI) |
| 7478 | IPCA-15 (base do IPCA-E) | % a.m. | correção monetária |
| 29543 | Taxa legal (art. 406 do CC) | % a.m. | juros da regra `civil_lei_14905` |
| 207xx | taxas médias consolidadas e desconto de cheques | % a.a. | **não** servem à razão por modalidade |
| 254xx | taxa média por modalidade | % a.m. | eixo contratada × média |

## Como rodar (uma chamada)

```
listar_series_bacen({})        # catálogo inteiro, com identidade e cobertura de cache
```

Conferir contra a tabela acima e contra `series_bacen_por_modalidade` em
`regras-bancarias.json`:

1. **Existência.** Todo código mapeado aparece na resposta? Ausência = drift → procurar o
   equivalente por modalidade na resposta viva, não abortar.
2. **Identidade.** Nome e unidade batem? Divergência de nome numa série de referência (ex.: 226
   voltando como CDI) é **falha** — parar e reportar ao time do conector.
3. **Unidade.** Toda série de modalidade em `% a.m.`? Uma `% a.a.` na faixa 254xx é **falha**: a
   razão contratada/média sairia em bases diferentes.
4. **Cobertura.** `cache.ultima` muito atrás do mês anterior sugere rotina mensal de
   materialização parada — reportar, mas não bloqueia: a consulta cai ao vivo.

Backstop de sanidade, e só quando algo já parecer errado: uma série de modalidade devolvendo
**> 25% a.m.** cheira a código anual. Não use magnitude como teste de rotina — cartão rotativo
(~15% a.m.) e cheque especial PJ (~13,5% a.m.) passam de 10, e imobiliário anual (~12% a.a.) fica
abaixo.

## Conferência que vale por análise

Uma só, e não custa chamada extra, porque o fator vem na mesma resposta da série:

```python
conferir_fator(serie, resposta["fator_acumulado"])
```

Ela pega os dois modos de falha silenciosa — série carregada pela metade (texto recortado em 60
pontos) e calendário divergente. `cobertura()` e `verificar_ponta_da_serie()` não pegam nenhum dos
dois, porque o recorte preserva justamente as duas pontas.

A janela é **fechada** nos dois extremos, igual à do conector. Não confundir com `dias_uteis()`,
que é semiaberto `[inicio, fim)` — essa é a convenção do CDI para a reconstrução financeira, e
comparar uma contra a outra acusa divergência de um dia em todo contrato cuja data-base caia em
dia útil publicado.

## Reportar drift ao conector

Falha nos itens 2 ou 3 vira report ao time do conector, com código, identidade esperada,
identidade recebida e a fonte oficial consultada. O conector versiona o catálogo e trava por
teste a coerência entre as visões — um report com esses dados vira correção de catálogo e teste
de regressão.
