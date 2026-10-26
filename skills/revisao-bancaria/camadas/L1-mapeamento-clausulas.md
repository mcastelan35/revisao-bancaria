# L1 — Mapeamento e classificação de cláusulas

Camada do plugin `revisao-bancaria`. Percorre o contrato cláusula a cláusula, classifica cada uma nas categorias do motor de regras e detecta comissão de permanência disfarçada.

## Entrada

Recebe a ficha de intake aprovada na L0 com: tipo de contrato, dados-chave, marcos temporais resolvidos e lista de encargos identificados.

## Categorias de classificação

Cada cláusula é mapeada para uma (e apenas uma) das 14 categorias do `dados/regras-bancarias.json`:

| Categoria | O que procurar no contrato |
|---|---|
| `comissao_de_permanencia` | Cláusula de inadimplência com percentual próprio (inclusive disfarçada) |
| `tarifas` | TAC, TEC, tarifa de cadastro, tarifa de contratação, tarifa de formalização |
| `servicos_terceiros` | Avaliação do bem, registro, correspondente bancário, "serviços de terceiros" genérico |
| `seguro_prestamista` | Seguro de proteção financeira, seguro prestamista, seguro de vida vinculado |
| `juros_remuneratorios` | Taxa de juros do contrato (mensal e anual) |
| `capitalizacao` | Relação entre taxa mensal e anual (Súmula 541: anual > 12x mensal) |
| `juros_moratorios` | Percentual de juros de mora estipulado |
| `multa_contratual` | Percentual de multa por atraso |
| `iof` | IOF financiado (embutido nas parcelas) |
| `cartao_credito` | Anuidade, rotativo, parcelamento de fatura, encargos do cartão |
| `repeticao_indebito` | Não é cláusula — é consequência calculada nas camadas L2/L3 |
| `procedimentais` | Cláusulas de foro, arbitragem, assinatura (relevantes para R28) |

## Detecção de comissão de permanência disfarçada

Esta é a operação mais crítica da L1. Usar a regra R03 do motor de regras.

**Passo 1 — Match de termos:** comparar a nomenclatura de cada cláusula de inadimplência contra os 12 termos suspeitos:

- taxa de permanência
- taxa de remuneração para operações em atraso
- taxa de remuneração de operações vencidas
- encargo por atraso
- remuneração de operações vencidas
- spread de inadimplência
- taxa de rentabilidade em atraso
- encargo de inadimplência
- taxa de administração de atraso
- custo de carregamento de inadimplência
- taxa de manutenção de débito em atraso
- taxa operacional de inadimplência

**Passo 2 — Heurística econômica:** mesmo sem match textual, classificar como CP disfarçada qualquer percentual ou taxa que:
- Incida APENAS no período de inadimplência (não na vigência normal)
- Seja cobrado ALÉM dos juros moratórios e/ou multa
- Reconstitua, na prática, a tríade juros remuneratórios + juros moratórios + multa sob uma única nomenclatura

**Passo 3 — Classificação:** se identificada CP disfarçada, classificar a cláusula como `comissao_de_permanencia` (não como `juros_moratorios` ou `multa_contratual`), registrando o nome original usado no contrato.

## Extração de valores

Para cada cláusula classificada, extrair:
- Nomenclatura exata usada no contrato (para citação em peça)
- Valor numérico (R$ fixo ou percentual)
- Base de incidência (sobre o saldo devedor, sobre a parcela, sobre o valor financiado)
- Frequência (única, mensal, anual)

## Cláusulas atípicas

Cláusulas que não se enquadram em nenhuma categoria conhecida devem ser registradas como "cláusula atípica" com o texto integral, para revisão manual pelo advogado. Não descartar — podem ser relevantes.

## Saída (gate para L2)

Apresentar o mapa de cláusulas ao usuário usando o formato visual aprovado (tabela com 4 colunas):

| Cláusula | Conteúdo extraído | Categoria | Valor |

Incluir flag "[CP DISFARÇADA]" quando aplicável.

Perguntar: "Alguma cláusula foi mal classificada? Faltou alguma?"

Só prosseguir para L2 após aprovação explícita. Se o usuário corrigir uma classificação, ajustar e reapresentar.
