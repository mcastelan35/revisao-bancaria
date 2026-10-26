---
name: triagem
description: "Triagem rapida de viabilidade de revisional bancaria, sem documento: compara a taxa contratada com a taxa media BACEN da modalidade no mes do contrato (uma consulta ao conector Radar Apogeu) e diz se fica dentro da faixa de mercado, na zona de abusividade (1,5x) ou fortemente abusiva (2x), com limiares, consequencia por regime, alerta do Tema 1378/STJ e, se houver valor e prazo, a economia nominal estimada. Use quando o usuario perguntar 'essa taxa e abusiva?', 'qual a taxa media do BACEN para consignado, veiculo, cheque especial ou capital de giro em tal mes', 'vale a pena entrar com revisional?', ou trouxer so a taxa, a modalidade e a data. Com contrato, extrato ou fatura em maos, use a skill revisao-bancaria."
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - Bash(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - PowerShell(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
---

# Triagem de taxa — revisão bancária

Objetivo: num turno e com **uma** chamada ao conector, dizer onde a taxa de um contrato fica em
relação à média BACEN da mesma espécie. É triagem, não laudo: não gera arquivo, não usa a
identidade do operador e não substitui a revisão com o instrumento (skill `revisao-bancaria`).

**Comando base** (`<rb>`): `python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"`
— no Windows, `python` no lugar de `python3`. Saída em JSON.

## 1. Dados — perguntar só o que faltar

Com botões quando a sessão tiver (`AskUserQuestion`), uma pergunta por vez:

- **Modalidade e segmento** (PF ou PJ). Consignado: INSS, setor público ou setor privado.
- **Data da contratação** — dia, mês e ano; a média usada é a do mês do contrato.
- **Taxa contratada e unidade**: ao mês ou ao ano; se ao ano, efetiva ou nominal. Número sem
  unidade ("2,5%") nunca se completa por palpite — pergunta-se. Se o usuário não souber se a
  anual é efetiva ou nominal, calcule as duas leituras, adote a de **menor** razão e declare a
  descartada (critério de menor excesso).
- **Quem contratou**: pessoa física consumidora → regime `consumerista`; empresa → regime
  `civil_empresarial` (vulnerabilidade de PJ não se presume).
- Opcional, para estimar economia: valor financiado, número de parcelas e sistema (Price ou SAC).

**Financiamento habitacional ou imobiliário (SFH, SFI, alienação fiduciária de imóvel,
construtora):** parar aqui. A razão contratada/média BACEN não é tese nesses contratos (R15
desligada — regra de conduta 27 da skill `revisao-bancaria`); o que decide esses casos é a conta
gráfica e o procedimento de consolidação. Encaminhe para a revisão completa.

## 2. Série da modalidade — sem quota

`<rb> serie --buscar "<termo>"` (ex.: "veiculos", "consignado", "cheque especial", "capital de
giro"). Mais de um candidato (PF × PJ, prazo do capital de giro, rotativo × parcelado) →
perguntar. Nenhum → uma `listar_series_bacen({ filtro })`.

## 3. Uma consulta ao conector

`consultar_taxa_bacen({ codigo, data_inicial: "AAAA-MM-01", data_final: "<último dia do mês>" })`
no mês do contrato. O ponto do mês é a taxa média em % a.m.; anote a `procedencia`.
"Nenhum dado encontrado" não é falha: o mês ainda não foi publicado (o BACEN publica com
defasagem). Diga qual é o último mês disponível e pergunte se a triagem pode usá-lo, declarando
a troca — nunca interpolar. Resposta com erro de fonte: uma nova tentativa; persistindo, dizer
que o conector está indisponível. Nunca `curl` na API do BACEN.

## 4. Razão e regras de juros

```bash
<rb> razao --contratada-pct <taxa> --unidade-contratada am_efetiva|aa_efetiva|aa_nominal --media-pct <média do mês>
<rb> regras --tipo <tipo> --regime consumerista|civil_empresarial --data-contrato AAAA-MM-DD \
    --categorias juros_remuneratorios,capitalizacao --formato padrao
```

`<tipo>`: `consumo_pf` (crédito pessoal, consignado, veículo PF), `empresarial_pj` (capital de
giro, veículo PJ, desconto), `cartao_credito`, `cartao_consignado` ou `cedula_rural` /
`cedula_comercial` / `cedula_industrial`. Nas cédulas a saída traz também a R17 (teto legal de
12% a.a., que independe da média) — mostrar as duas comparações. Sem o dia do contrato, omita
`--data-contrato`: as regras com corte pela data voltam em `confirmar`. Da saída de `regras`
saem a consequência e o tier da R15 conforme o regime, o `alerta` do Tema 1378 e os
`alertas_vencidos`.

## 5. Economia estimada — só se a razão for ≥ 1,5x e houver valor, prazo e sistema

`<rb> comparar --sistema price|sac --pv <valor> --n <parcelas> --taxa-contratada-pct <taxa> --taxa-revisada-pct <média> [--unidade …]`

Apresente `excesso_total` como **estimativa nominal**, sem correção monetária, sem encargos e
sem repetição em dobro — não é valor a restituir. Abaixo de 1,5x não há economia a mostrar.

## 6. Resposta

Curta, nesta ordem:

```
Triagem — <modalidade> — contrato de <mês/ano>
Taxa contratada: X% a.m. (informada: <valor e unidade como o usuário disse>)
Média BACEN <código — nome> em <mês/ano>: Y% a.m. (<cache | ao vivo>)
Razão: N,NNx → <dentro da faixa de mercado | zona de abusividade | fortemente abusiva>
Limiares: 1,5x = A% a.m. · 2,0x = B% a.m.
Regime: <consumerista | civil-empresarial> → <consequência da R15 nesse regime>
Tema 1378/STJ: <alerta da R15> [+ alerta vencido, se houver]
[Economia nominal estimada: R$ … — estimativa, não é valor a restituir]
Próximo passo: …
```

- A R15 está **suspensa** pelo Tema 1378: a razão é aritmética e a conclusão é do advogado —
  dizer isso, não "é abusiva".
- Razão ≥ 1,5x: há tese de juros a examinar. Para laudo, revisão completa (skill
  `revisao-bancaria`) com o contrato ou CCB, a proposta ou planilha do CET e o extrato da
  operação ou os boletos.
- Razão < 1,5x: a tese de juros abusivos não se sustenta neste contrato. Se houver interesse, a
  revisão completa ainda pode atacar encargos (tarifas, seguro, comissão de permanência) e a
  composição do débito.

Orçamento: uma chamada ao conector (`consultar_taxa_bacen`); `listar_series_bacen` só se o
mapeamento não tiver a modalidade.
