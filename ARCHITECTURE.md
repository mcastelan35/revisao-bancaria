# Arquitetura do plugin `revisao-bancaria`

> Versão do pacote: **v6.0.0** (26/10/2026). Este arquivo é o mapa; o comportamento normativo
> está na `SKILL.md` do orquestrador e nas camadas. Em divergência, a camada prevalece no seu
> escopo — e a divergência é bug: `python ferramentas/verificar_consistencia.py` e a suíte de
> testes falham quando versão, contagens, tiers, cores do schema, numeração das regras de
> conduta, arquivos citados ou identidade pré-preenchida divergem entre os arquivos.

## Visão geral

Plugin de análise revisional bancária em **duas rotas** (mais os ramos cartão e SFH/SFI),
definidas pelo gate R0 na primeira interação, com gates de aprovação obrigatórios em cada
camada. O conector MCP **Radar Apogeu** (BACEN/SGS, cache persistente) é pré-requisito e fonte
única de taxas e índices: a skill raciocina e calcula, o conector entrega a série oficial
datada, e os dois juntos tornam o laudo reproduzível por terceiro.

| Rota | Objeto | Camadas | Motor |
|---|---|---|---|
| INSTRUMENTO | O contrato e suas cláusulas | L-1 → L0 → L4 | `motores/calculo.py` (Price/SAC) + `motores/cet.py` (pós-fixadas/CET) |
| INSTRUMENTO · SFH/SFI | Mútuo habitacional com saldo indexado | L-1 → L0 → L1 → L2 + L2b → L3 → L4 | `motores/calculo.py` (`tabela_sfh`, `comparar_sfh`) |
| INSTRUMENTO · cartão | Faturas | L-1 → L0 → `camadas/analise-faturas-cartao.md` (substitui L1–L3) → L4 | `motores/cartao.py` |
| CONTA | O extrato e a evolução do saldo | L-1 → C0 → C6 | `motores/conta_corrente.py` (saldo diário, SMD, art. 354) — **beta** enquanto o repertório estiver em ESQUELETO |

As rotas compartilham conector, cascata de taxa, gate de qualificação do regime, encargos sem
lastro, exibição de documentos e encontro de contas. **Não compartilham motor nem regra de
capitalização.**

## Estrutura de arquivos

```
revisao-bancaria/                         ← raiz do repositório = plugin = marketplace
├── .claude-plugin/
│   ├── plugin.json                       ← manifesto do plugin (versão única)
│   └── marketplace.json                  ← marketplace de um plugin só (source "./")
├── skills/
│   ├── revisao-bancaria/                 ← skill principal (autocontida)
│   │   ├── SKILL.md                      ← orquestrador: ordem, comando base, mapa, L-1, regra crítica, conector, 29 regras de conduta (0–28)
│   │   ├── revisao.py                    ← linha de comando única (JSON na saída)
│   │   ├── camadas/
│   │   │   ├── R0-gate-roteamento.md     ← gate inicial + R0-b (um laudo por instrumento)
│   │   │   ├── L0-intake-contrato.md     ← INSTRUMENTO: recepção, classificação, datação, comparação BACEN imediata
│   │   │   ├── L1-mapeamento-clausulas.md
│   │   │   ├── L2-motor-conformidade.md  ← motor de regras + semáforo + tier
│   │   │   ├── L2b-procedimento-expropriatorio.md ← SFH/SFI: checklist da consolidação/execução (R39/R40)
│   │   │   ├── L3-analise-quantitativa.md← memória do credor, motores, simulação, indébito
│   │   │   ├── L4-geracao-demonstrativos.md ← payload → PREMIUM/PANORAMA/planilha
│   │   │   ├── C0-C6-rota-conta.md       ← CONTA: intake→inventário→SMD→conformidade→trinca→nexo/exibição→encontro
│   │   │   └── analise-faturas-cartao.md ← ramo cartão
│   │   ├── referencia/
│   │   │   ├── bacen-consulta.md         ← protocolo do conector (ler antes da 1ª consulta)
│   │   │   ├── payload-schema.md         ← contrato de dados L3 → saída
│   │   │   ├── pesquisa-base.md          ← pesquisa consolidada (INSTRUMENTO)
│   │   │   ├── repertorio-jurisprudencial-contas.md ← ESQUELETO — [PENDENTE], preencher via JusIA
│   │   │   └── teste-contrato-bacen.md   ← alarme de drift do catálogo do conector
│   │   ├── dados/
│   │   │   └── regras-bancarias.json     ← base do motor de regras (versão = a do pacote)
│   │   └── motores/                      ← pacote Python, só biblioteca padrão (+ openpyxl na planilha)
│   │       ├── __init__.py               ← VERSAO
│   │       ├── comum.py                  ← brl/pct/pt, parse pt-BR estrito, competências, guarda de escala
│   │       ├── calculo.py                ← Price/SAC/tabelado, decote, tabela_sfh/comparar_sfh
│   │       ├── cet.py                    ← custo efetivo real / pós-fixadas, adaptadores do conector, conferir_fator
│   │       ├── cartao.py                 ← faturas, teto da Lei 14.690, bola de neve
│   │       ├── conta_corrente.py         ← rota CONTA
│   │       ├── regras.py                 ← motor de regras determinístico
│   │       ├── operador.py               ← identidade de quem assina (fora do pacote, na pasta de dados)
│   │       └── relatorios.py             ← renderizador único (PREMIUM, PANORAMA, planilha)
│   ├── triagem/SKILL.md                  ← taxa × média BACEN sem documento (uma chamada)
│   └── configurar/SKILL.md               ← operador, ambiente e conector
├── ferramentas/
│   ├── verificar_consistencia.py         ← docs ↔ JSON ↔ renderizador ↔ manifestos (exit 1 = divergência)
│   └── empacotar_plugin.py               ← gera dist/revisao-bancaria-<versão>.plugin para o claude.ai
├── tests/                                ← pytest: motores, motor de regras, operador, CLI, plugin
├── .github/workflows/testes.yml          ← suíte em Windows e Linux a cada envio
├── CONECTOR.md                           ← instruções curtas para Projetos do claude.ai sem o plugin
├── ARCHITECTURE.md · CHANGELOG.md · README.md
```

A skill principal é autocontida: tudo o que ela lê ou executa está na própria pasta, com
caminhos relativos a ela. `configurar` e `triagem` usam a linha de comando da principal por
`${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py`.

## Pipeline

```
USUÁRIO ─▶ R0 (gate de roteamento) ─▶ R0-b (nº de instrumentos) ─▶ L-1 (operador)
             │
   ┌─────────┴──────────────┐
   ▼ INSTRUMENTO            ▼ CONTA
 L0 intake+datação+BACEN  C0 intake + saldo inicial datado + qualificação do regime
   ▼ gate                   ▼ gate
 L1 mapa de cláusulas     C1 inventário CSV canônico (pt-BR estrito) + RECONCILIAÇÃO
   ▼ gate                   ▼ gate
 L2 motor de regras +     C2 saldo diário, SMD, perfil, razão (reaproveita BACEN)
    semáforo                ▼ gate
   ▼ gate (teses)         C3 conformidade da conta (motor de regras)
 L3 memória do credor →     ▼ gate
    motores + simulação   C4 trinca de cenários (faixa, não ponto)
   ▼ gate (números)         ▼ gate (cenário-líder)
 L4 payload → entrega     C5 nexo cruzado + exibição
                            ▼ gate
                          C6 encontro de contas + entrega (fallback HTML declarado)
```

Rota AMBAS: CONTA primeiro — o saldo recomposto e o `nexo_cruzado` alimentam o encontro de
contas dos contratos. Ramo cartão: L0 (intake) → `analise-faturas-cartao.md` → L4. A `triagem`
fica fora do pipeline: responde sem documento e devolve para o R0 quando há tese.

## Motor de regras determinístico (`motores/regras.py`)

Entrada: tipo, regime (`consumerista` | `civil_empresarial`), data do contrato, data da
consolidação, categorias da L1 e a data da análise. Para cada regra, o primeiro passo que
exclui decide o destino:

1. `superada` → não aplicável.
2. Regra em `regras_desligadas` do tipo → não aplicável (ramo SFH/SFI).
3. Tipo: as tags de `tipo_contrato` são expandidas pelos `grupos` (`todos`, `todos_sfn`,
   `todos_sem_lei_especifica`); `empresarial_pj` em regime consumerista (CDC mitigado) também
   casa as regras `consumo_pf`. Sem casamento, a repetição de indébito em regime consumerista
   de outro tipo vai para `confirmar` (regra de conduta 9); o resto, não aplicável.
4. Regime: bloco `regime` com `aplica: false` → não aplicável; regra só `consumo_pf` em regime
   civil-empresarial → não aplicável; `empresarial_pj` civil-empresarial com regra fora de
   `regras_sem_cdc` e sem bloco `regime` → `confirmar`.
5. Corte temporal pela `base` do marco: `contrato` (exclui ou, sem data, `confirmar`);
   `pagamento` e `operacao` (não excluem: o corte reparte a apuração, registrado em `corte`);
   `contrato_ou_consolidacao` (MT10: datar os dois; só um anterior → aplicável com a leitura
   divergente registrada).

Saída: `aplicaveis` (tier e consequência resolvidos por regime e, na R03, por marco),
`confirmar` (com motivo) e `nao_aplicaveis` (com motivo), mais `conclusiva`, `pendencias` e
`alertas_vencidos` calculados na data. `validar_dados()` trava a integridade do JSON (grupos
derivados, marcos e regras citados existentes, `regras_afetadas` derivado do corte).

## Linha de comando (`skills/revisao-bancaria/revisao.py`)

| Subcomando | Para quê |
|---|---|
| `autoteste` | autoteste de todos os motores, resumo de uma linha por módulo |
| `regras` | regras aplicáveis ao caso (L2, C3, triagem) |
| `regra`, `sumula` | texto integral para fundamentar |
| `marcos` | posição do contrato em MT01–MT10 (L0) |
| `serie` | série BACEN da modalidade, sem gastar quota do conector |
| `razao` | razão contratada/média, limiares 1,5x/2,0x (Decimal) |
| `comparar` | Price/SAC contratado × revisado |
| `gerar` | entregáveis a partir do payload, com marca e assinatura do operador |
| `operador` | mostrar e salvar a identidade de quem assina |

Códigos de saída: 0 ok · 1 autoteste com falha · 2 erro de entrada · 3 operador não configurado.

## Dependências externas

| Componente | Tipo | Obrigatória? | Função |
|---|---|---|---|
| Conector Radar Apogeu | Servidor MCP | **Pré-requisito** | `consultar_taxa_bacen` (lote/`pontos:"completos"`), `consultar_indice`, `atualizar_debito` (`valores[]`, `segmentos` ou `regra`), `listar_series_bacen` (só fora do mapeamento ou drift), `status_conta` (na `configurar`) |
| API SGS/BACEN | API pública | Contingência declarada (`falha_fonte`) | Fonte primária, atrás do cache |
| Python ≥ 3.10 | Interpretador | Sim | Motores e linha de comando, só biblioteca padrão |
| `openpyxl` | Pacote Python | Só para a planilha | O renderizador confere antes de escrever; o autoteste pula a planilha sem ele |
| Skill de peticionamento do operador | Skill | Opcional (gravada na L-1) | Petição pós-L4/C6 |
| `pesquisa-jurisprudencial-jusia` | Skill | Opcional (obrigatória p/ preencher o repertório CONTA e p/ pendências vencidas) | Validação de precedentes |
| `briefing-estrategico` / `proposta-comercial` | Skill | Opcional | Risco para o cliente / prospecção |
| `liquidacao-correcao-debitos` | Skill | Opcional | Regimes de correção fora do `atualizar_debito` |
| `html-pdf-impressao-segura` | Skill | Opcional (fallback do entregável CONTA) | CSS anti-quebra |
| `design-quality-guard` | Skill | Opcional | Checklist visual |

Orçamento de chamadas do caso típico: **uma** de dado (`consultar_taxa_bacen`, em lote quando
duas séries) + `atualizar_debito` quando houver indébito; a série diária inteira de um
indexador custa uma chamada dedicada. Chamada é a unidade de quota do aluno.

## Decisões de projeto

- **Operador fora do pacote.** `operador.json` fica em `${CLAUDE_PLUGIN_DATA}` (ou na pasta de
  configuração do usuário fora do Claude Code): sobrevive a atualizações e nunca entra no
  repositório. O `gerar` o aplica ao payload quando faltam `marca`/`assinatura`.
- **Identidade da série pela própria consulta.** O mapeamento modalidade → código usa os mesmos
  códigos do catálogo do conector; a identidade volta na resposta de `consultar_taxa_bacen`.
  `listar_series_bacen` virou exceção, não rotina.
- **Ambiguidade vira pergunta.** Onde o JSON e a prosa divergiam (regras `todos` fora de
  `regras_sem_cdc`; repetição de indébito em tipo consumerista que não é `consumo_pf`), o motor
  devolve `confirmar` com o motivo — não aplica nem descarta em silêncio.
- **Relatório = payload renderizado** (regra 14), **um laudo por instrumento** (regra 25) e
  **menor excesso** (regra 23) seguem como na v5.

## Motor de regras — estatísticas (v6.0.0)

40 regras em 14 categorias (19 T1, 13 T2, 8 sem tier); 33 vigentes, 2 suspensas (R15 — Tema
1378; R24 — Temas 1328/1414), 5 sem precedente consolidado (R30–R33, R40); 10 marcos temporais
com `base` declarada (`regras_afetadas` derivado do `corte_temporal` de cada regra); 23 súmulas
com texto integral; 24 modalidades mapeadas para séries BACEN mensais (faixa 254xx); 12 termos
de CP disfarçada (dentro da R03); 10 tipos de contrato (três habitacionais: `sfh`, `sfi`,
`imobiliario_fora_sfi`, com `regras_desligadas`) e 3 grupos derivados; bloco
`pendencias_jurisprudenciais` com `verificado_em` e `validade_dias`.

## Regra crítica: abusividade de juros (1,5x / 2,0x)

Razão contratada/média BACEN: < 1,5x lícita; 1,5x-2,0x zona de abusividade; ≥ 2,0x
fortemente abusiva. Sempre exibida; consequência por regime. Alerta permanente do Tema
1378/STJ e alerta vencido quando a pendência passar da validade.

## Rota CONTA — decisões de projeto

Motor **puro**: não parseia PDF nem chama conector — a C1 extrai para o CSV canônico (pt-BR
estrito) com gate de aprovação, e a **reconciliação contra o saldo impresso** valida a extração
(fechamento por dia; divergência ou competência faltante = lacuna bloqueante). Janela começa na
`data_inicial` do saldo informado. Trinca padrão: C1_TAXA_MEDIA (S. 530/abusividade) ·
C2_CAP_MENSAL (expurgo da capitalização diária) · C3_TAXA_LIMPA (só encargos sem lastro).
Convenções declaradas: hamburguês (dias_corridos | dias_devedores), taxa-dia (linear_mes
padrão | linear_30 | exponencial_30), capitalização (mensal | nenhuma, com imputação do art.
354). ESTORNO de juros simétrico ao ENCARGO. Corte do Tema 929 por competência inteira na
base simples (menor excesso).

## Pendências abertas

1. Repertório jurisprudencial da rota CONTA: preencher as 7 teses via JusIA (inteiro teor
   conferido) — até lá a rota é **beta** e a C6 fundamenta só no `regras-bancarias.json`.
2. Renderizador: ramo `conta` no payload-schema (reconciliação, trinca, série por competência)
   para PREMIUM/PANORAMA saírem do renderizador único.
3. **Decisão jurídica do autor — regras para PJ sem CDC.** `empresarial_pj.regras_sem_cdc`
   lista R01, R02, R03, R17–R21 e R25, mas a L2 da v5 só excluía as regras exclusivas de
   `consumo_pf`. Regras `todos` fora da lista (R11, R12, R14, R16, R28–R33) hoje saem em
   `confirmar`. Definir regra a regra se dependem do CDC e atualizar a lista ou marcar
   `depende_cdc` no JSON.
4. **Decisão jurídica do autor — consumidor fora de `consumo_pf`.** R26/R27 (dobro/simples) são
   marcadas só para `consumo_pf`, mas a regra de conduta 9 as liga ao regime consumerista. Em
   cartão PF, cartão consignado e SFI consumerista elas saem em `confirmar`. Definir se as tags
   devem incluir esses tipos.
5. Cartão como terceira rota explícita (F0–F3) em vez de ramo que atravessa L1–L3.
6. Regressão com caso real anonimizado: rodar um extrato verdadeiro ponta a ponta e congelar
   como fixture, no molde do `teste-contrato-bacen.md`.
7. Conferir o status dos temas em `pendencias_jurisprudenciais`: os conferidos em 26/08/2026
   valem até 24/11/2026 e os de 09/10/2026 até 07/01/2027 (validade de 90 dias); depois disso
   o motor passa a emitir o alerta vencido em toda análise que os invoque.
8. Ramo SFH/SFI: completar relator, órgão e data de julgamento dos 15 precedentes `[CONFERIR]`
   no JSON; validar no TRF4 a recepção do REsp 2.086.650/MG (R35); congelar uma conta gráfica
   real da CEF como fixture de `tabela_sfh` (o autoteste usa fixture calculada à mão).
9. Renderizador: ramo `sfh` no payload (credor × revisado de `comparar_sfh`, conta apartada e
   checklist L2b) — até lá o laudo SFH/SFI usa a natureza `recomposicao` com a conta apartada
   declarada em texto.
10. Séries longas passam pelo contexto do modelo (a resposta do conector precisa ser
    transcrita para o motor). Um modo do conector que entregue a série como arquivo, ou um
    recurso MCP, cortaria esse custo nas reconstruções pós-fixadas de vários anos.
11. Agente de extração para extratos e faturas longos (C1 e cartão), para manter o contexto
    principal enxuto em casos de centenas de páginas.

## Benchmarks que mudam o plugin

| Evento | Impacto | Ação |
|---|---|---|
| Julgamento Tema 1378 | Critério de juros abusivos (as duas rotas) | Atualizar R15 e limiares; `verificado_em` |
| Conclusão Tema 929 | Modulação do dobro | Atualizar R26/R27 e corte MT05 |
| Julgamento Temas 1328/1414 | RMC | Atualizar R24 |
| Nova resolução CMN (cartão) | Teto de 100% | Atualizar R23 e MT06 |
| Repertório CONTA validado | Habilita fundamentação plena da C6 | Retirar status ESQUELETO/beta |
| STJ unifica o critério temporal da purga (Lei 13.465) | R40 | Mudar `status` para vigente e fixar o critério |
| TRF4 aplica (ou rejeita) o REsp 2.086.650/MG | R35 | Atualizar `alerta` e pendência; se rejeitar, rebaixar a T2 |
| Conector muda o contrato de uma tool | Protocolo | Atualizar `referencia/bacen-consulta.md`, `CONECTOR.md` e rodar `referencia/teste-contrato-bacen.md` |
