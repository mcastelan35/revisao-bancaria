# Consulta BACEN pelo conector — protocolo

Referência do plugin `revisao-bancaria` para obter taxas de mercado e séries de
indexador. **Ler antes da primeira consulta de taxa.**

## Premissa

O conector **Radar Apogeu** está na sessão, ativo e validado. A skill é distribuída junto com
ele e a mesma assinatura dá acesso aos dois — o aluno tem chave própria. Não existe passo de
detecção, teste de disponibilidade nem caminho paralelo. Use o conector como quem usa uma
biblioteca instalada.

Isso não é conveniência: o conector é a **fonte declarada** das taxas, e é o que torna a
apuração reproduzível por terceiro. Trocar a fonte sem declarar quebra a reprodutibilidade do
laudo em contraditório.

## O que o cache garante

O conector materializa as séries do SGS no próprio banco, competência a competência.

- **Competência coberta responde do banco**, em milissegundos, com o valor oficial congelado e
  datado. Dez anos de IPCA custam o mesmo que um mês.
- **O que falta cai no SGS ao vivo**, com resultado idêntico — os pontos são sempre recortados à
  janela pedida, então cache e ao vivo não divergem.
- **O mês corrente é sempre ao vivo.** Só competência encerrada é congelada.
- **BACEN fora do ar não interrompe a análise** no que já está coberto.
- Toda resposta declara `procedencia: { cache, ao_vivo, banco_indisponivel }` — registre isso na
  metodologia do entregável.

`listar_series_bacen` traz o alcance do cache de cada série em `cache: { competencias, primeira,
ultima }`. Não é preciso adivinhar nem sondar.

## As quatro chamadas

### 1. `listar_series_bacen({ filtro, segmento? })`

Resolve três coisas de uma vez: **qual código** usar para a modalidade, a **identidade
autoritativa** da série (nome, unidade, periodicidade, segmento) e o **alcance do cache**. Não
bate em API externa.

O catálogo do conector é autoritativo. Não confirme identidade por segunda ferramenta, não
infira unidade pela magnitude do valor, não mantenha catálogo paralelo nesta skill.

**No plugin, ela raramente é necessária.** O código da modalidade sai de `<rb> serie` (o
mapeamento `series_bacen_por_modalidade` usa os mesmos códigos do catálogo do conector, sem
gastar quota) e a identidade da série — nome, unidade, periodicidade, segmento — volta na
própria resposta de `consultar_taxa_bacen`. Chame `listar_series_bacen` só quando a modalidade
não estiver no mapeamento, quando o usuário perguntar o alcance do cache ou para o alarme de
drift (`referencia/teste-contrato-bacen.md`).

### 2. `consultar_taxa_bacen({ codigo, data_inicial, data_final, pontos? })`

Série + estatísticas prontas (mín, máx, média, mediana, contagem) + `fator_acumulado` +
`variacao_acumulada_pct` + `procedencia` + `ponta`.

- **Taxa média de mercado** (séries mensais 254xx): use o modo padrão. As estatísticas já vêm
  calculadas — não recalcule à mão.
- **Série diária de indexador** (CDI 12, Selic 11, TR 226): use **`pontos: "completos"`**. Sem
  isso o texto lista 60 pontos de N e o produtório sai errado.
- **Várias séries na mesma janela**: passe `codigos: [...]` (até 6) em vez de `codigo` — uma
  chamada devolve todas, cada uma com seus pontos, estatísticas, `fator_acumulado`, `procedencia`
  e `ponta`. É o jeito de pegar a série da modalidade e o indexador de uma vez. Uma série que
  falhe na fonte vira `erro` no lote sem derrubar as outras. **`pontos: "completos"` é recusado
  com `codigos`** — a série diária inteira de várias estouraria a resposta; para ela, uma chamada
  com `codigo` sozinho.
- Datas em `yyyy-MM-dd`. Em série **mensal**, `data_inicial` no **dia 1º** da competência: o
  ponto do mês é datado no primeiro dia e uma data posterior o deixa de fora da janela.
- A `procedencia` distingue `sem_dado` (mês sem publicação) de `fonte_indisponivel` (o SGS
  falhou) e traz `capturado_em_min` (a captura mais antiga do cache na janela). Timeout do SGS
  **não** é ausência de índice — não declare lacuna por causa dele; reconsulte.

### 3. `consultar_indice({ codigo, data_inicial, data_final })`

Mesmo cache, todos os pontos, `fator_acumulado` e `variacao_acumulada_pct`.

**A resposta inteira vem como JSON no TEXTO.** As duas tools do motor
(`consultar_indice` e `atualizar_debito`) não emitem `structuredContent` — o texto já é a
serialização completa, e duplicá-la transmitiria a série em dobro. Não procure campo em payload
estruturado nestas duas; parseie o texto (`carregar_de_consultar_indice` aceita `dict` ou `str`).

Para série diária grande, `consultar_taxa_bacen` com `pontos: "completos"` é mais enxuto e traz o
fator do mesmo jeito.

Identidade da série em `cabecalho.serie.nome` — **não** `serie.nome`.

> **Limitação conhecida — TR e poupança.** Essas séries publicam um período de referência
> (`dataFim`): a data do ponto é o início da vigência, não o dia em que o índice se aplica. O
> conector preserva esse campo, mas os adaptadores do `motores/cet.py` carregam só `data`/`valor`.
> Em reconstrução indexada a TR ou poupança, declare a convenção de ancoragem na metodologia do
> entregável em vez de assumir que a data do ponto é a data de incidência.

### 4. `atualizar_debito({ valor_original | valores, segmentos | regra, … })`

Correção monetária e juros do *quantum* a restituir, com memória linha a linha e hash de
auditoria para o demonstrativo pericial. O motor não decide regime jurídico — e a skill também
não: o regime é escolhido pelo operador no gate da L3/C6 e declarado na metodologia. O conector
aceita duas formas, mutuamente exclusivas:

- **`segmentos`** — trechos em ordem cronológica, cada um com `data_inicial`, `indice_codigo`
  (ex.: 433 IPCA, 188 INPC, 7478 IPCA-15/IPCA-E; omitido = sem correção no trecho) e `juros`
  (`tipo`: `selic` | `percentual_mensal` | `nenhum`; `capitalizacao`: `simples` (padrão) |
  `composta`). É a forma para o regime que o operador indicar, trecho a trecho.
- **`regra: { tipo: "civil_lei_14905", juros_desde?, indice_correcao_anterior? }`** — regra
  pronta do conector para dívida civil sem índice nem taxa no contrato ou no título: até
  29/08/2024, Selic única; a partir de 30/08/2024, IPCA + taxa legal (série 29543), com pro rata
  nos meses parciais. `juros_desde` fixa o termo inicial dos juros quando ele não é a data-base
  de cada valor (ex.: citação); `indice_correcao_anterior` é o índice do título para o período
  sem juros anterior a 30/08/2024. Usar só se o operador adotar esse regime para o indébito.

Também existem `pro_rata_die` (padrão `false`: índice integral do mês), `multa_percentual`,
`honorarios_percentual` e `art_523` (multa e honorários do cumprimento de sentença). São da fase
de cumprimento, não do laudo revisional — só com pedido expresso do operador. Fazenda Pública
não tem regra pronta no conector.

- `data_inicial` de cada segmento no **dia 1º** da competência. O conector alarga a janela de
  busca até a borda da competência, mas o dia 1º mantém a memória de cálculo legível.
- **Restituição parcela a parcela**: passe `valores: [{ valor, data_inicial, rotulo }]` no lugar
  de `valor_original` (`rotulo` livre, como "parcela 07/48" — nunca nome, CPF ou número de
  contrato do cliente). Cada parcela é corrigida da sua própria data-base, sob o mesmo regime de
  `segmentos`, e a série é buscada **uma vez só** — 48 parcelas custam uma chamada, não 48. A
  resposta traz `resumo_geral` (somatórios) e a memória de cada valor. É o caminho certo para o
  Tema 929: cada pagamento indevido entra no timeline na data em que foi pago.
- Confira **`calculo_interrompido`** (em cada valor e no `resumo_geral`). Quando falta índice
  publicado em alguma competência o cálculo para ali e `ultima_competencia_calculada` diz onde —
  o total não cobre o período pedido.

## Orçamento de chamadas

Chamada de ferramenta é a **unidade de quota** do plano do aluno. O código da série sai de
`<rb> serie`, sem chamada. Um contrato pós-fixado típico resolve-se em **uma** chamada de dado:

1. `consultar_taxa_bacen({ codigos: [série da modalidade, indexador diário], … })` — as duas
   séries numa chamada, cada uma com identidade, estatísticas, `fator_acumulado`,
   `procedencia` e `ponta`.

Se a reconstrução pós-fixada precisar da série diária **inteira** (produtório dia a dia), aí é
uma chamada dedicada `consultar_taxa_bacen({ codigo: 12, pontos: "completos" })` — o lote recusa
`completos`. Mais `atualizar_debito` quando houver indébito a corrigir, e com `valores` ele
cobre a restituição parcela a parcela **numa só chamada**. **Um laudo completo cabe em duas a
três chamadas.**

Não gaste quota com: sondagem de disponibilidade, reconfirmação de identidade de série, teste de
não-aliasing entre séries, repetição de consulta que já está no contexto, ou recálculo de
estatística que a resposta já trouxe.

## Verificações obrigatórias antes de assinar

Todas usam dado que a resposta já traz — nenhuma custa chamada extra.

```python
# 1. A série carregada é a série que o conector serviu?
conferir_fator(serie, resposta["fator_acumulado"])   # divergência invalida a reconstrução

# 2. A ponta alcança o último dia útil ANTES da data-base?
verificar_ponta_da_serie(max(serie), data_base)      # devolve ponta_necessaria e alcanca_data_base

# 3. A série cobre o período da apuração?
cobertura(serie, liberacao, data_base, pontos_esperados=resposta["pontos_total"])
```

**`conferir_fator` é a guarda central.** Ela cruza o produtório local contra o fator do conector
sobre a mesma janela e é o que pega os dois modos de falha silenciosa: série carregada pela
metade (texto recortado) e calendário divergente (feriado, chunking, intervalo aberto contra
fechado). `cobertura()` e `verificar_ponta_da_serie()` **não** pegam truncamento nem buraco no miolo — as
duas olham só as pontas, e o recorte preserva justamente as pontas. Passar `pontos_esperados` à
`cobertura()` fecha essa brecha; sem ele, quem detecta é o `conferir_fator`.

**Ponta insuficiente é lacuna bloqueante — e "suficiente" tem régua definida.** A reconstrução
usa os dias úteis anteriores à data-base (convenção semiaberta), então o motor precisa da série
até o **último dia útil antes da data-base**, não até a data-base. O `ponta.alcanca_data_final`
do conector mede contra a data final inclusive: `false` com a série chegando ao dia útil
anterior é normal (o SGS publica em D+1) e o motor aceita; `false` com buraco antes disso é
lacuna. Nesse caso recue a data-base para o último ponto efetivo e declare na metodologia. Jamais
repita o último fator para os dias faltantes nem interpole.

## Sinais de erro do conector

| Sinal | Significado | O que fazer |
|---|---|---|
| `OMITIDOS DESTE TEXTO` no texto | série recortada em 60 pontos | rechamar com `pontos: "completos"`. Nenhum produtório sobre o texto recortado vale |
| `Nenhum dado encontrado para o período` | não há ponto publicado ali — resposta normal, não erro | conferir código e janela; em série mensal, `data_inicial` no dia 1º |
| resposta com erro (`isError`) | a **fonte** falhou: timeout, recusa, parâmetro inválido | 1 nova tentativa; persistindo, `web_fetch` como contingência **declarada** |
| `procedencia.banco_indisponivel: true` | cache fora, tudo veio ao vivo | resultado válido; registrar na metodologia |
| `resumo.calculo_interrompido: true` | faltou índice numa competência | o total não cobre o período; ver `ultima_competencia_calculada` |

**`bash`/`curl` na `api.bcb.gov.br` não é caminho em nenhum cenário.** Ignora o cache, dispensa a
conferência de fator e produz número não reproduzível. Já ocorreu em produção: a reconstrução
saiu certa por sorte, sem cruzamento com fonte independente.

**`web_fetch` no SGS é contingência declarada**, admissível só quando o conector responde erro de
fonte, sempre registrada na metodologia do entregável, e refeita pelo conector quando ele voltar.

### URL do fallback, se for o caso

```
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{CODIGO}/dados?formato=json&dataInicial={DD/MM/AAAA}&dataFinal={DD/MM/AAAA}
```

Datas em `DD/MM/AAAA` — o conector usa `yyyy-MM-dd`. Resposta: `[{ "data": "01/03/2023", "valor":
"2.01" }]`, valores como string com ponto decimal. Estatísticas e fator ficam por sua conta, e o
cruzamento de fator deixa de existir — mais uma razão para ser contingência, não caminho.

## Séries por modalidade

O objeto `series_bacen_por_modalidade` em `regras-bancarias.json` (consultado por `<rb> serie`)
mapeia modalidade de contrato → código SGS. Ele existe para você **não escolher série por
intuição**; a identidade final, porém, é a que o conector devolve — no cabeçalho da própria
consulta ou em `listar_series_bacen`. Todas as séries de modalidade são **mensais (% a.m.)** da
faixa 254xx: a razão contratado/média sai na mesma base, sem conversão.

Backstop frouxo: série de modalidade devolvendo **> 25% a.m.** cheira a código errado — pare e
reconfira em `listar_series_bacen`. Não use magnitude para inferir unidade: cartão rotativo
(~15% a.m.) e cheque especial PJ (~13,5% a.m.) passam de 10, e imobiliário anual (~12% a.a.) fica
abaixo.

Índices de referência de uso frequente: **11** Selic fator diário, **12** CDI diário, **226** TR
diária (**não** é CDI), **433** IPCA mensal, **188** INPC mensal, **189** IGP-M mensal, **4390**
Selic acumulada no mês (% a.m.), **4189** Selic acumulada no mês anualizada base 252 (% a.a.),
**432** meta Selic do COPOM.

Selic (11) e CDI (12) publicam fator diário muito próximo — isso é o mercado, não defeito do
conector. São séries distintas na fonte; use a que o contrato indexa.

Demais séries do catálogo do conector (48 no total em 26/10/2026), por papel:

- **Índice do saldo no SFH/SFI**: **7811** TR mensal, **196** poupança mensal, **195** poupança
  diária (regra da Lei 12.703/2012), **25** poupança diária (regra antiga), além de 226 e 433.
  TR e poupança têm período de referência (ver a limitação em `consultar_indice`): declarar a
  convenção de ancoragem à data de aniversário do contrato.
- **Correção monetária**: **7478** IPCA-15 (base do IPCA-E), **7447** IGP-DI, **190** IGP-OG,
  **13522** IPCA acumulado em 12 meses (% a.a. — não é índice mensal), **1178** Selic anualizada
  base 252 (diária, % a.a.), **29543** taxa legal do art. 406 do CC (sem competência no cache
  em 26/10/2026: vem ao vivo — registrar a `procedencia`).
- **Taxas médias anuais e agregadas — não servem à razão por modalidade**: **20714** crédito
  total, **20715** PJ total, **20716** PF total, **20717** recursos livres e **20720** desconto de
  cheques PJ, todas em % a.a. O eixo da razão é a série mensal 254xx da espécie. Desconto de
  cheques não está no mapeamento: se for a espécie do caso, a conversão anual → mensal e a sua
  convenção são decisão declarada na metodologia, nunca inferência.

## Formato do registro na análise

Independentemente do caminho, registrar:

```json
{
  "serie": 25471,
  "nome": "Aquisição de veículos — PF",
  "unidade": "% a.m.",
  "fonte": "consultar_taxa_bacen",
  "procedencia": { "cache": ["2023-03", "…"], "ao_vivo": [] },
  "periodo": { "inicio": "2023-03-01", "fim": "2024-03-01" },
  "estatisticas": { "min": 0, "max": 0, "media": 0, "mediana": 0 },
  "fator_acumulado": "1.00000000",
  "ponta": { "ultimo_ponto": "01/03/2024", "alcanca_data_final": true },
  "taxa_referencia": 0,
  "data_referencia": "mês do contrato"
}
```

`fonte` e `procedencia` vão para a metodologia do demonstrativo — é o que permite a um terceiro
refazer a apuração e chegar ao mesmo número.
