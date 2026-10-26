# R0 — Gate de roteamento

Camada do plugin `revisao-bancaria`. Primeira coisa a executar, sempre —
antes da L-1, antes de abrir qualquer documento. Define a rota e trava motor e regras.

## A pergunta (tap obrigatório)

> "O que você espera desta análise?"

Use a ferramenta de perguntas com botões da sessão quando houver (`AskUserQuestion` no Claude
Code; tap no claude.ai); senão, opções numeradas.

| Opção | Rota | Motor travado | Camadas |
|---|---|---|---|
| Revisar um contrato (financiamento, consignado, capital de giro, cédula, leasing) | **INSTRUMENTO** | `motores/calculo.py` | L-1 → L0 → L4 |
| Revisar financiamento habitacional ou imobiliário (SFH, SFI, alienação fiduciária, consolidação, leilão) | **INSTRUMENTO (ramo SFH/SFI)** | `motores/calculo.py` (`tabela_sfh` / `comparar_sfh`) | L-1 → L0 → L1 → L2 (+ `L2b-procedimento-expropriatorio.md`) → L3 → L4 |
| Revisar a movimentação de uma conta (cheque especial, limite, conta garantida) | **CONTA** — *beta enquanto o repertório jurisprudencial estiver em ESQUELETO; avisar ao confirmar a rota* | `motores/conta_corrente.py` | L-1 → C0 → C6 |
| Analisar faturas de cartão de crédito | **INSTRUMENTO (ramo cartão)** | `motores/cartao.py` | L-1 → L0 (intake) → `camadas/analise-faturas-cartao.md` (**substitui L1–L3**: gate de valor original, extração por competência, teto e excesso) → L4 |
| Contrato E conta (encontro de contas) | **AMBAS** | os dois | CONTA primeiro, depois INSTRUMENTO |
| Só saber se a taxa está acima da média de mercado, sem documento | — (não é rota) | nenhum | skill `triagem`: uma consulta ao conector, razão e limiares; se houver tese, volta para cá com os documentos |

## Regras

1. **Documento já enviado permite inferir, nunca dispensa a confirmação.** Extrato anexado
   → propor CONTA e confirmar em uma linha ("Recebi extratos — a análise é da movimentação
   da conta, correto?"). CCB anexada → propor INSTRUMENTO. A confirmação é obrigatória
   porque o mesmo PDF pode servir às duas rotas (extrato que instrui revisão de contrato).

1-b. **Ramo SFH/SFI tem lógica invertida em relação ao SFN — por isso é opção própria.**
   Contrato com Lei 4.380/64, FGTS, apólice SH/SFH, CEF/EMGEA, FCVS, PES/CP, CES → `sfh`;
   com Lei 9.514/97, alienação fiduciária, consolidação da propriedade, leilão → `sfi`;
   construtora ou loteadora vendendo a prazo → `imobiliario_fora_sfi`. Nesses três tipos a
   Súmula 539 e o duodécuplo NÃO validam capitalização (no SFI a taxa anual acima do
   duodécuplo PROVA a capitalização vedada — R35), e a razão contratada/média BACEN (R15)
   não é tese (STJ e TRF4 rejeitam limitar juros no SFH). Rodar a leitura do SFN nesses
   contratos produz laudo contra o cliente. O que decide esses casos é documento: conta
   gráfica desde a primeira prestação (R34/R36) e certidões do procedimento de consolidação
   (R39/R40, camada `L2b`).

2. **Definida a rota, ela não se mistura.** Regra de conduta 17 (rota travada) da SKILL.md: cada rota tem
   motor, regras de capitalização e repertório próprios. Aplicar a leitura de uma na outra
   é defeito grave — em mútuo com prestação fixa, duodécuplo e prestação constante afastam
   anatocismo; em rotativo, a discussão é periodicidade e metodologia.

3. **Rota AMBAS executa CONTA primeiro**: o saldo recomposto da conta alimenta o encontro
   de contas dos contratos (parcelas debitadas em conta entram pelo `nexo_cruzado`).

4. Depois do R0, seguir para a L-1 (identificação do operador) e então para a primeira
   camada da rota escolhida. Os "modos de operação" (auditoria rápida / revisão completa)
   valem só para a rota INSTRUMENTO; a rota CONTA tem gates próprios (C0-C6).

---

## Gate R0-b — quantos instrumentos? (obrigatório na rota INSTRUMENTO)

Contar os instrumentos **antes** da L0. Execução bancária com mais de uma operação é o
padrão em cooperativa de crédito, não exceção: vencimento antecipado cruzado costuma
disparar todas as cédulas do associado no mesmo intervalo de dias.

**Um instrumento por laudo. Sem exceção.** O chassi do renderizador (`motores/relatorios.py`) é
mono-instrumento por construção: `conferencia` tem UM veredito, UMA data-base e UM conjunto
de cenários; `memoria` é singular; a tabela de identificação é uma só. Empurrar duas cédulas
nesse molde não produz documento confuso — produz **erro material**, porque o veredito de
conferência de uma operação passa a ler-se como aval às duas.

| Instrumentos | Procedimento |
|---|---|
| 1 | Fluxo normal L0 → L4 |
| 2 ou mais | L0 e L1 podem correr em paralelo para comparação; **L4 gera N payloads e N laudos**, cada um autossuficiente |

Em N instrumentos, cada payload recebe obrigatoriamente:

- Identificação própria, com o número da cédula na primeira linha da tabela e no título
- Veredito de conferência próprio — eles **não se comunicam**
- Achados renumerados a partir de A1 dentro do laudo
- Ressalvas e lacunas específicas daquele instrumento
- Memória de apuração correspondente àquela metodologia
- Bloco de advertência de conexão em `objeto` e em `conclusao`, na forma: *"Este laudo examina
  exclusivamente o instrumento identificado no quadro acima; a operação [nº] é objeto de laudo
  apartado, e nenhuma conclusão aqui firmada — inclusive o veredito de conferência — se estende a ela."*
- `slug` prefixado por `opN-`, para que os arquivos não se sobreponham

Achados que se repetem entre instrumentos (cláusulas de formulário) entram nos dois laudos,
com os números daquela operação. Não remeter de um laudo para o outro.

**Alerta ao peticionar.** Se os embargos forem únicos para as execuções reunidas, a petição
precisa tratar as operações em tópicos distintos: as teses raramente são simétricas — uma pode
ter erro de método e a outra erro de índice com saldo correto. Confundi-las na peça reproduz
o defeito que a segmentação do laudo existe para evitar.
