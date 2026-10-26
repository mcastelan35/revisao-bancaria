# L3 — Análise quantitativa e simulação de cenários

Camada do plugin `revisao-bancaria`. Calcula o impacto financeiro da revisão, consulta a série completa de taxas no BACEN, e gera a simulação contratado vs. correto com projeção de restituição.

## Entrada

Recebe as teses aprovadas pelo usuário na L2, a ficha de intake da L0 e o mapa de cláusulas da L1.

## Consulta BACEN — taxa média da espécie

**O conector está na sessão, ativo e validado — é premissa, não hipótese a testar.** Não gastar chamada com sondagem de disponibilidade. Ver `referencia/bacen-consulta.md` para o protocolo. **Nunca `bash`/`curl` na `api.bcb.gov.br`**: ignora o cache persistente e dispensa a conferência de fator. `web_fetch` só se o conector devolver erro de fonte, e declarado na metodologia.

1. Identificar a modalidade de crédito do contrato e localizar a série com `<rb> serie` (mapeamento `series_bacen_por_modalidade`, sem quota). A identidade da série (nome, unidade, periodicidade, segmento) volta na própria resposta de `consultar_taxa_bacen`; `listar_series_bacen` só entra se a modalidade não estiver no mapeamento ou se houver suspeita de drift do catálogo.

2. **Reaproveitar a consulta da L0** (regra de conduta 2): a série da modalidade já foi trazida na janela inteira do contrato. Só chamar `consultar_taxa_bacen({ codigo, data_inicial, data_final })` se a L0 não a tiver; datas em `yyyy-MM-dd`, `data_inicial` no **dia 1º** em série mensal. As estatísticas (mín, máx, média, mediana) vêm prontas — **não recalcular**.

3. Registrar a **fonte** e a **procedência** (`procedencia.cache` / `procedencia.ao_vivo`) — as duas constam na metodologia do demonstrativo e do payload. É o que permite a um terceiro refazer a apuração.

### Operação pós-fixada — série diária do indexador

Contrato indexado a CDI, Selic, TR ou IPCA **não** se resolve pela taxa média da modalidade: exige reconstrução dia útil a dia útil com `motores/cet.py`.

1. Obter a série diária numa chamada: `consultar_taxa_bacen({ codigo, data_inicial, data_final, pontos: "completos" })`. O `pontos: "completos"` é **obrigatório** aqui — no modo padrão o texto lista 60 pontos de N. Carregar com `carregar_de_consultar_taxa_bacen(resposta)`; o adaptador recusa resposta recortada em vez de aceitá-la pela metade. A mesma resposta já traz o `fator_acumulado`. (`consultar_indice` faz o mesmo, com payload maior — use se preferir JSON estrito.)
2. `conferir_fator(serie, resposta["fator_acumulado"])` **antes** de qualquer conclusão. É a guarda que pega série carregada pela metade e calendário divergente, e divergência **invalida a reconstrução**. Não custa chamada: o fator veio junto.
3. `cobertura(serie, liberacao, data_base, pontos_esperados=resposta["pontos_total"])` e `verificar_ponta_da_serie(max(serie), data_base)`. A reconstrução usa os dias úteis **anteriores** à data-base (convenção semiaberta), então a série precisa alcançar o **último dia útil antes da data-base** — não a data-base em si. O `ponta.alcanca_data_final` do conector mede contra a data final inclusive: `false` com a série chegando ao dia útil anterior é normal (o SGS publica em D+1) e o motor aceita; `false` com buraco antes disso é **lacuna bloqueante**: recuar a data-base e declarar na metodologia. Jamais interpolar nem repetir o último fator. Estas duas guardas **não** detectam recorte — quem detecta é o `conferir_fator`.
4. Rodar `ReconstrucaoPosFixada` e passar `custo_efetivo_aa` e o resultado de `conferir_saldo()` ao payload da L4. Pagamentos: informar todos, inclusive o da data-base (abatido no fim, sem encargo do dia); vários no mesmo dia são somados; pagamento em dia não útil é deslocado ao próximo dia útil da série e listado em `pagamentos_deslocados` — declarar na metodologia. Pagamento fora do período ou maior que o saldo é erro, não ajuste silencioso.
   Auditoria do CET declarado (`auditar_cet`): o CET do demonstrativo é **ex-ante** (Res. CMN 4.881/2020 — indexador vigente na contratação). Informar `indexador_aa_na_contratacao` e `spread_aa` para que o motor compare o declarado com o CET esperado ex-ante; sem esses dados o CET-01 sai `A verificar`, nunca `Ilícito` — custo ex-post maior que CET ex-ante é o efeito do indexador, não vício do demonstrativo.
5. Para auditar o fator que o CREDOR aplicou, usar `auditar_fator_declarado()` — nunca
   `fator_indexador(serie, dias_uteis(...))` direto. `dias_uteis()` é semiaberta à direita, convenção
   de reconstrução de saldo; o fator declarado pelo credor refere-se a intervalo fechado. Misturar as
   duas produz dois números para a mesma grandeza, que é o erro que a L4 existe para não repetir.

4. Usar a taxa média na data do contrato como parâmetro revisional. Se não houver dado exato para o mês, usar o ponto mais próximo.

5. Se o conector devolver **erro de fonte** (timeout/recusa do SGS): tentar 1 vez mais; persistindo, `web_fetch` como contingência declarada, ou perguntar ao usuário se fornece a taxa (https://www.bcb.gov.br/estatisticas/txjuros) — nunca inventar. **"Nenhum dado encontrado" não é erro de fonte**: é ausência de publicação naquela janela. Conferir o código e, em série mensal, se `data_inicial` está no dia 1º.


## Auditoria da memória do credor — executar ANTES dos cenários contrafactuais

A L3 nasceu para recalcular o contrato. Mas em execução já ajuizada o resultado útil quase
sempre está na **planilha do credor**, não na revisão da taxa: o instrumento costuma estar
dentro da média de mercado e com capitalização pactuada, enquanto a memória, montada por
sistema, erra em pontos verificáveis. Rodar esta seção primeiro; ela é barata e frequentemente
decide onde vale gastar o resto do esforço.

Seis conferências, todas contra o que a própria memória declara:

**1. Percentuais uniformes entre parcelas vencidas e vincendas.** Extrair, de cada linha, o
quociente entre cada rubrica de encargo e o principal daquela linha. Percentual idêntico em
todas as parcelas — inclusive nas de vencimento futuro — significa que o credor aplicou o mesmo
período de mora a obrigações que ainda não venceram. Pode ser legítimo sob vencimento
antecipado, mas só se o desconto a valor presente (item 3) estiver correto.

**2. Base de incidência da multa.** Dividir a multa lançada pelo principal, depois pelo
principal somado aos juros. O divisor que devolve exatamente o percentual contratual revela a
base efetivamente usada. Base ampliada → R31.

**3. Desconto a valor presente das parcelas vincendas.** Sob vencimento antecipado, o credor
deve trazer as vincendas a valor presente pela taxa contratual. Conferir a razão entre parcelas
consecutivas: ela deve ser constante e igual a `1/(1+i)`. Razão menor que essa indica desconto
insuficiente. Apurar nas duas convenções (`meses_civis` e `dias_corridos/30`) e adotar a de
menor excesso, declarando ambas na metodologia.

**4. Fator do indexador contra a série oficial.** Em operação pós-fixada, confrontar o fator
declarado com o produtório da série no intervalo que o próprio credor anunciou, por
`auditar_fator_declarado()` do `motores/cet.py`. A função apura nas duas convenções de janela e
adota a de menor excesso. Divergência acima de um pregão de índice não é arredondamento.

**5. Coerência entre saldo declarado e amortizações informadas.** Memória que informa
"amortizações: R$ 0,00" e ao mesmo tempo abre a cobrança na parcela nº N está declarando que as
N−1 anteriores foram pagas sem registrar o abatimento. Reconstruir o saldo e conferir por
`conferir_saldo()`.

**6. Metodologia declarada versus praticada.** Comparar o que o cabeçalho da memória anuncia
(sistema de amortização, índices, datas de vencimento antecipado) com o que as linhas fazem.
Divergência entre o anunciado e o praticado é o achado mais forte que existe, porque dispensa
controvérsia jurídica: basta confrontar o documento consigo mesmo.

Achado desta seção é sempre `Excesso`, `Divergência` ou `Base de cálculo` — nunca `Ilícito`,
porque não se trata de vício de cláusula, e sim de desconformidade entre a cláusula e a conta.

## Quando a revisão contratual não tem o que decotar

Se a razão contra a média BACEN ficar abaixo de 1,5x, a capitalização estiver pactuada e a
prestação reproduzir a taxa do instrumento, **dizer isso primeiro e sem rodeio**, antes de
qualquer outro resultado. O veredito de saída é `revisão contratual inviável — atacar a
composição do débito`, e os KPIs de parcela vão a zero de economia em vez de exibir número
inflado por tese que não se sustenta.

Isso não é derrota da análise: é o resultado que impede o cliente de ajuizar revisional
perdida e que dá credibilidade à impugnação seletiva da memória. Laudo que só sabe acusar
excesso perde a causa em que o excesso não existe.

## Cálculos por cláusula

Para cada tese aprovada pelo usuário:

### Juros remuneratórios (R15)
- Recalcular parcelas usando o mesmo sistema de amortização (Price/SAC) com a taxa média BACEN
- **Não calcular à mão.** Para o resumo dos dois cenários, `<rb> comparar --sistema price|sac --pv … --n … --taxa-contratada-pct … --taxa-revisada-pct … [--unidade …] [--tabela]`; para trabalhar parcela a parcela, `from motores import calculo` e `calculo.Cenario(sistema, pv, r, n)` + `calculo.comparar(contratado, revisado)`. `favoravel: false` no resultado significa que o cenário revisado é mais caro — vai em ressalvas, não some
- Normalizar a taxa antes: `normalizar_taxa(valor, unidade)` com unidade `am_efetiva` | `aa_efetiva` | `aa_nominal` — a unidade é lida da cláusula, nunca inferida
- Price: `PMT = PV × r / (1 - (1+r)^-n)`, com guarda para `r = 0` (→ `PV/n`) e parcela de ajuste na última competência
- SAC: amortização constante `A = PV/n`, `J_k = SD_{k-1} × r`, `P_k = A + J_k`. Como `A` independe da taxa, o **saldo devedor coincide nos dois cenários** — o que diverge é a prestação
- Prazo: declarar a convenção (`meses_civis` | `dias_30_360` | `dias_corridos`) na seção de premissas do relatório
- Carência e parcela antecipada: `aplicar_carencia()` e `antecipado=True`
- Diferença mensal: `parcela_contratada - parcela_revisada`
- Diferença acumulada: soma das diferenças mensais
- Decomposição por parcela: juros, amortização e saldo devedor em ambos os cenários

### Juros em cédula rural/comercial/industrial (R17)
- Mesmo cálculo, mas com taxa fixa de 12% a.a. (1% a.m.) como revisada
- Não depende de consulta BACEN — o teto é legal, não de mercado

### Encargos acessórios (R04, R06, R09, R10, R11, R12, R13)
- Se o encargo foi pago à vista e não integrou o principal: repetição do valor nominal corrigido
- Se o encargo foi financiado ou debitado na liberação: `decotar_encargo_financiado(pv, r, n, encargo)` devolve dois números que não se confundem: `valor_presente` (= o encargo, por construção) e `impacto_nominal` (soma das diferenças de parcela ao longo do prazo, que já embute os juros sobre o encargo). O laudo reporta os dois com rótulo; a correção monetária vai sobre as diferenças parcela a parcela em suas datas (`diferencas_parcela` → `atualizar_debito`), nunca sobre o `impacto_nominal` como se fosse valor presente

### Multa e juros moratórios excessivos (R21, R22)
- Diferença = excedente acima do teto (1% a.m. para mora, 2% para multa)

### Comissão de permanência cumulada/disfarçada (R01, R02, R03)
- Decotar encargos cumulados, mantendo apenas a CP limitada ao teto

## Cálculo de repetição de indébito

Para CADA valor indevido, aplicar a modulação temporal do Tema 929:

1. Determinar as datas de cada pagamento indevido (parcelas mensais a partir da primeira)
2. Pagamentos com data <= 30/03/2021 → repetição simples (1x)
3. Pagamentos com data > 30/03/2021 → repetição em dobro (2x)
4. Encargos únicos (TAC, seguro, avaliação): usar a data do pagamento (geralmente embutido na primeira parcela ou financiado)

A atualização monetária de cada pagamento indevido, da sua data-base até a data do cálculo, vai
ao conector numa chamada só: `atualizar_debito({ valores: [{ valor, data_inicial, rotulo }],
segmentos, data_final })`. Cada parcela entra no timeline de correção na sua própria data; a
resposta traz `resumo_geral` e a memória de cada valor, com hash de auditoria. Não fazer uma
chamada por parcela — são N vezes a quota do aluno pelo mesmo resultado. A modulação do dobro
(abaixo) é aplicada sobre os valores já corrigidos.

**O regime de correção e juros do indébito é escolha jurídica do operador, feita no gate desta
camada antes da chamada** — o conector não decide regime. Duas formas, ambas descritas em
`referencia/bacen-consulta.md` §4: `segmentos` montados com o índice e os juros que o operador
indicar (trecho a trecho), ou a regra pronta `regra: { tipo: "civil_lei_14905", juros_desde }`
quando o operador a adotar. A escolha, com o fundamento que o operador der, vai à metodologia;
regime que o conector não parametriza vai para `liquidacao-correcao-debitos`.

Resultado:
- Subtotal simples (pagamentos pré-30/03/2021)
- Subtotal dobro (pagamentos pós-30/03/2021)
- Total de restituição = simples + dobro

## Simulação de cenários

Gerar dois cenários completos parcela a parcela:

**Cenário contratado:**
- Parcela fixa (Price) ou decrescente (SAC) com taxa contratada
- Para cada mês: parcela, juros, amortização, saldo devedor
- Total de juros pagos, total pago

**Cenário revisado:**
- Mesma estrutura com taxa média BACEN (ou 12% a.a. para cédulas)
- Para cada mês: parcela, juros, amortização, saldo devedor
- Total de juros pagos, total pago

**Diferenças:**
- Excesso por mês (constante no Price; decrescente no SAC, segundo `SD × (r_contratado − r_revisado)`)
- Excesso acumulado
- Economia percentual sobre o CET

## Saída (gate para L4)

Apresentar os números ao usuário no formato visual híbrido:

**KPIs:**
- Parcela contratada / Parcela revisada / Economia mensal
- Total contratado / Total revisado / Economia total
- Restituição (simples + dobro)

**Tabela de cláusulas com valores calculados:**

| Cláusula | Valor contratado | Valor devido | Excesso | Repetição (simples/dobro) | Total a restituir |

**Gráfico de evolução acumulada:**
Linhas de contratado vs. correto com área de economia.

Perguntar: "Os cálculos estão corretos? Quer ajustar algum parâmetro?"

Botões de ação:
- "Gerar relatório / demonstrativo" → L4
- "Analisar outro contrato" → volta para L0
- "Ajustar parâmetros e recalcular" → refazer L3 com novos inputs
