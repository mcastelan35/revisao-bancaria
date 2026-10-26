# Análise de faturas de cartão de crédito

Referência de negócio para a camada L1 quando o objeto for cartão de crédito.
Motor correspondente: `motores/cartao.py`. Regra do teto: R23. Marco: MT06.

---

## Por que cartão é um regime à parte

Cartão de crédito quase nunca tem instrumento contratual disponível. O que o
cliente tem são as **faturas**. Elas deixam de ser documento acessório e passam
a ser a fonte probatória principal — e a única fonte da taxa, que a fatura é
obrigada a informar.

Consequências operacionais:

1. Não existe "contrato para ler". A L1 lê fatura, não cláusula.
2. Não se usa Price nem SAC. A dívida não é série de prestações: é saldo que
   rola de competência em competência com encargos variáveis.
3. A taxa vem impressa na fatura. Se estiver ilegível ou ausente naquela
   competência, isso é **lacuna documental**, não hipótese para estimativa pela
   média BACEN. Registrar em `competencias_sem_taxa` e pedir a fatura legível.

---

## Regra inegociável — proibição de presunção

**Vale para cartão e para financiamento, sem exceção.**

Só há duas origens admissíveis de dado:

| Origem | Aceita? |
|---|---|
| Extraído do documento enviado | Sim — registrar a página ou o campo |
| Informado expressamente pelo usuário | Sim — registrar como declaração |
| Inferido, estimado, arbitrado ou "adotado como praxe" pelo analista | **Não** |

Não há terceira categoria. Dado ausente vira **lacuna bloqueante**, com pedido
específico do documento ou da informação, nunca premissa de trabalho. O
`motores/cartao.py` implementa isso em código: campo `None` levanta `DadoAusente`
com o nome do campo e a competência, e nenhuma função tem valor padrão.

O relatório reflete a mesma separação. A seção de premissas tem duas listas —
"informado pelo usuário" e "extraído do documento", cada linha com a origem — e
uma terceira lista de "lacunas pendentes". Premissa do analista não existe.

---

## Sequência de trabalho

### 1. Gate de abertura (obrigatório, logo após o envio das faturas)

Perguntar ao usuário, antes de qualquer cálculo:

- Qual saldo deve ser considerado **valor original da dívida** para o teto da
  Lei 14.690? Em regra é o saldo da primeira fatura que entrou no rotativo, mas
  a identificação depende de confirmação — o motor não infere.
- Houve **parcelamento de fatura, renegociação ou portabilidade** no período? Se
  sim, em quais competências?
- A discussão é de **teto legal** (R23), de **taxa** (comparação com média
  BACEN) ou de ambos?
- O período está completo ou faltam faturas?

### 2. Extração por competência

Para cada fatura, extrair: competência, saldo anterior, compras do período,
pagamento efetuado, encargos financeiros, IOF, total da fatura e taxa informada.

**IOF fica sempre apartado dos encargos.** A Resolução CMN 5.112/2023 exclui o
IOF do cômputo do teto. Somar IOF aos encargos infla o excesso e derruba o laudo.

### 3. Segmentação da série

`segmentar_serie()` divide em trechos contínuos e lista as competências
faltantes. Buraco na série **não interrompe** o trabalho e **não é
interpolado**: analisam-se os trechos contínuos, marca-se o corte no relatório e
emite-se pedido nominal das faturas faltantes.

### 4. Candidatos a evento

`detectar_candidatos()` sinaliza competências em que o saldo anterior declarado
diverge do saldo aritmeticamente esperado. A saída é **candidato**, com
hipóteses possíveis — parcelamento, renegociação, portabilidade, estorno — e
nunca classificação. Levar cada candidato ao usuário e só então rotular.

### 5. Evolução da dívida — a bola de neve

`evolucao_divida()` reconstrói a formação do débito: competência de origem do
rotativo, encargos acumulados, participação dos encargos no saldo e
multiplicador do saldo inicial ao final.

Esta é a peça de maior valor comunicativo. O cliente não entende percentual ao
mês; entende que uma dívida de determinado valor virou o dobro em seis
competências, e entende ver quanto do saldo atual é principal e quanto é
encargo.

### 6. Quantificação

Dois caminhos, que podem coexistir:

- **Teto legal** — `teto_lei_14690(valor_original, faturas, novas_dividas=None)`.
  Parâmetro objetivo, não depende de comparação com média de mercado. Só as
  competências a partir de 03/01/2024 entram no cômputo: as anteriores saem
  listadas em `competencias_excluidas_pre_marco` e ficam fora do somatório (o
  teto não retroage); série inteiramente anterior ao marco devolve
  `aplicavel: False`. Compras novas que rolaram para o rotativo constituem dívida
  própria com teto próprio (Res. CMN 5.112/2023, art. 2º, §1º): informar em
  `novas_dividas=[("2024-03", 500.0), …]` — sem isso o motor apura sobre o valor
  original único e devolve `ressalva` obrigatória para o laudo. O motor recusa
  competência duplicada e fatura cujo total não fecha com saldo anterior +
  compras + encargos + IOF (tolerância R$ 0,05) — extração inconsistente é
  lacuna, não arredondamento.
- **Taxa** — `excesso_por_taxa()`. Compara os encargos cobrados com os
  admissíveis a uma taxa de referência sobre o saldo anterior de cada
  competência, **nominal por competência e sem efeito composto** (critério de
  menor excesso; o campo `metodo` da saída declara isso e o laudo transcreve).

---

## O que o relatório de cartão precisa mostrar

Ordem de valor decrescente para o usuário final:

1. **Excesso de encargos por competência e acumulado.** É o produto principal.
   Gráfico de barras para o excesso do mês e linha para o acumulado —
   `svg_excesso()` já emite no padrão do chassi canônico.
2. **Linha do tempo da bola de neve.** Competência de origem, saldo naquele
   momento, saldo atual, multiplicador e quanto do saldo atual é encargo.
3. **Régua do teto.** Valor original, teto de 100%, quanto já foi cobrado, a
   competência de estouro e a margem restante.
4. **Tabela de competências** com saldo anterior, compras, pagamento, encargos,
   IOF, total e taxa informada — com as competências faltantes visíveis como
   corte, não como omissão silenciosa.
5. **Candidatos a evento** confirmados pelo usuário, com o que cada um alterou.

Gráfico sem número ao lado é decoração. Toda série plotada tem tabela
correspondente, e toda tabela declara a origem do dado.

---

## Erros que invalidam o trabalho

Somar IOF aos encargos no cômputo do teto. Estimar taxa não impressa pela média
de mercado. Interpolar competência faltante. Classificar parcelamento sem
confirmação. Aplicar o teto de 100% a operação anterior a 03/01/2024. Usar
Price ou SAC para projetar rotativo. Tratar a data de assinatura do contrato de
cartão como marco — o marco é a data da operação de rotativo ou parcelamento.
