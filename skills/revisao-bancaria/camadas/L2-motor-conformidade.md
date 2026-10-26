# L2 — Motor de conformidade

Camada do plugin `revisao-bancaria`. Aplica as 40 regras do `dados/regras-bancarias.json` às
cláusulas mapeadas na L1, gerando o semáforo de legalidade e a classificação por tier de
ataque. A aplicabilidade (tipo, regime, marcos, regras desligadas, status e validade das
pendências) é resolvida pelo motor determinístico — o agente não lê o JSON inteiro nem refaz
esse filtro à mão (regra de conduta 28).

## Entrada

Recebe o mapa de cláusulas aprovado na L1 e a ficha de intake da L0 (tipo de contrato, regime
qualificado, datas e dados-chave).

## Passo 1 — Regras aplicáveis ao caso (uma chamada)

```bash
<rb> regras --tipo <tipo> --regime <consumerista|civil_empresarial> --data-contrato <AAAA-MM-DD> \
    [--data-consolidacao <AAAA-MM-DD>] --categorias <categorias do mapa da L1>,repeticao_indebito,procedimentais
```

A saída traz `aplicaveis` (com `tier` e `consequencia` já ajustados pelo regime e, na R03,
pela leitura do marco MT04), `confirmar` (aplicável, mas falta dado ou decisão — sempre com
`motivo`) e `nao_aplicaveis` (com `motivo`). Em cada item: `teste` (lógica e campos
necessários), `corte` (marco que reparte a apuração por pagamento ou por operação em vez de
excluir a regra), `conclusiva`, `alerta`, `pendencias` e `alertas_vencidos`. Para o painel,
`--formato resumo`; para redigir a fundamentação, `<rb> regra R..` traz o texto integral.

O que o motor já fez e não se refaz:

- **Tipos habitacionais** (`sfh`, `sfi`, `imobiliario_fora_sfi`): as regras de
  `regras_desligadas` (R15, R18 e, conforme o tipo, R19) saem em `nao_aplicaveis` — não é
  "aplicar e marcar lícita", é não aplicar: o laudo não pode conter badge de razão BACEN nem
  conclusão de "capitalização pactuada válida" nesses contratos.
- **Corte temporal** com a base certa: data do contrato; cada pagamento no MT05 (dobro × simples);
  a operação de rotativo no MT06; contrato e consolidação no MT10.
- **Regime**: consequência e tier da R15 pelo bloco `regime`; regra consumerista fora do regime
  consumerista; no `empresarial_pj` civil-empresarial, regra fora de `regras_sem_cdc` vai para
  `confirmar`.

Itens em `confirmar` vão ao gate como perguntas, uma de cada vez. Resposta do operador que muda
a aplicação é registrada em `premissas`.

## Passo 2 — Para cada regra aplicável × cláusula do mapa

1. **Ramo SFH/SFI.** Carregar `camadas/L2b-procedimento-expropriatorio.md` sempre que houver
   consolidação, leilão, execução extrajudicial ou intimação nos autos (R39/R40 — o item traz
   `requer_sub_skill`). R34 e R36 só concluem `ilicita` com `comparar_sfh`/`tabela_sfh` rodados
   sobre a conta gráfica integral; sem ela, o resultado é `a_verificar`
   (`resultado_se_sem_conta_grafica`) e o gate diz que a tese depende de perícia.

2. **Verificar campos necessários**: `teste.campos_necessarios` lista os dados que o teste
   exige. Se faltarem dados que NÃO foram extraídos na L0/L1, **perguntar ao usuário** (gate
   interno). Nunca presumir o valor de um campo faltante.

3. **Executar o teste lógico**: avaliar a condição de `teste.logica`. O teste é descritivo (não
   é código executável) — o agente o interpreta com os dados da cláusula.

4. **Taxa média BACEN — reaproveitar a L0.** Regras com `teste.requer_consulta_bacen: true`
   (R02, R15, R16) usam a série que a L0 já consultou na janela inteira do contrato (regra de
   conduta 2). Só consultar aqui se a L0 não conseguiu (taxa obtida tardiamente):
   `consultar_taxa_bacen` com o código de `<rb> serie`, `data_inicial` no **dia 1º** em série
   mensal, uma chamada. Nunca `bash`/`curl`. Ver `referencia/bacen-consulta.md`.

5. **Razão de abusividade (R15)**: a de `<rb> razao`, já calculada na L0, classifica:
   - < 1,5x → `licita` (badge verde: "dentro da faixa de mercado")
   - >= 1,5x e < 2,0x → `zona_cinzenta` (badge amarelo: "zona de abusividade — X,XXx a média")
   - >= 2,0x → `ilicita` (badge vermelho: "fortemente abusivo — X,XXx a média")
   - Sempre exibir a razão exata como badge na linha dos juros

6. **Classificar resultado**: `ilicita`, `ilicita_parcial`, `licita`, `zona_cinzenta`,
   `inversao_onus`, `dobro`, `simples`.

7. **Atribuir semáforo visual**:
   - Vermelho (com ícone de alerta): `ilicita`, `ilicita_parcial`
   - Amarelo (com ícone de atenção): `zona_cinzenta`
   - Verde (com check): `licita`

8. **Registrar tier** — o da saída do motor, já ajustado pelo regime: T1 (ataque prioritário —
   alta taxa de êxito, tese objetiva), T2 (ataque secundário — depende de prova ou tem
   incerteza), ou sem tier (lícita).

9. **Regra não conclusiva** (`conclusiva: false` — status `suspensa` ou
   `sem_precedente_consolidado`): NÃO emitir conclusão definitiva. Exibir o `alerta` ao lado
   do resultado. Sinalizar como "tese pendente de julgamento — decisão do advogado" ou "tese
   sem repetitivo — pesquisa obrigatória antes da peça".

10. **Pendência vencida** (`alertas_vencidos` não vazio): emitir o alerta junto ao da regra. O
    motor não sabe o resultado de um julgamento que ninguém conferiu — validar via
    `pesquisa-jurisprudencial-jusia`; a atualização do `verificado_em` no JSON sai numa nova
    versão do plugin.

## Regras que exigem interação extra

| Regra | Dado faltante frequente | Pergunta ao usuário |
|---|---|---|
| R07/R08 | Se é primeiro contrato | "É o primeiro contrato do cliente com esta instituição?" |
| R11 | Laudo de avaliação | "Há laudo de avaliação do bem nos autos?" |
| R12 | Comprovante de registro | "O registro do contrato (Detran/cartório) foi efetivamente realizado?" |
| R13 | Livre escolha da seguradora | "O cliente teve opção de escolher outra seguradora?" |
| R14 | Proposta apartada | "O seguro foi contratado por proposta apartada e separada?" |
| R28 | Assinatura impugnada | "O cliente reconhece a assinatura no contrato?" |
| R34/R36 | Conta gráfica integral | "Há a conta gráfica/evolução do saldo desde a primeira prestação? Sem ela a amortização negativa fica a verificar." |
| R35 | Periodicidade da capitalização | "A cláusula diz capitalização mensal, anual ou é silente? Qual a taxa anual e a mensal?" |
| R38 | Cláusula de CES | "O contrato tem cláusula expressa de CES? Ele foi cobrado na primeira prestação?" |
| R39 | Certidões de notificação | "Estão nos autos as certidões do cartório com as diligências pessoais antes do edital?" |
| R40 | Datas | "Data de assinatura do contrato e data da averbação da consolidação?" |

Essas perguntas são gates internos — fazer UMA de cada vez, conforme a cláusula for analisada.

## Saída (gate para L3)

### Passo 1 — Painel visual INLINE no chat (obrigatório)

ANTES de gerar qualquer arquivo, apresentar o resultado da L2 no chat. Se a sessão tiver ferramenta de widget visual (ex.: `show_widget`), usá-la; se não tiver, apresentar as mesmas seções em tabela markdown com o semáforo em texto (🔴/🟡/🟢) e os botões como lista de opções numeradas — nunca travar nem pular o gate por falta da ferramenta. O painel deve conter:

**Seção 1 — KPIs de parcela** (3 cards no topo):
- Parcela contratada / Parcela correta / Economia por parcela
- Se a taxa não for conhecida (Proposta ausente), mostrar "Pendente" nos KPIs de parcela e destacar os encargos já calculáveis

**Seção 2 — Mapa de cláusulas com semáforo** (tabela interativa):
- Colunas: Cláusula | Conteúdo | Potencial ilegalidade | Valor | Tier
- Badges de cor: vermelho (ilícita), amarelo (zona cinzenta), verde (lícita), cinza (pendente)
- Badge de razão contratada/média na linha dos juros
- Flag "[TEMA PENDENTE]" quando regra suspensa

**Seção 3 — Gráfico de evolução acumulada** (Chart.js / SVG):
- Linhas contratado vs. correto com área de economia
- Se não houver dados para gráfico (Proposta ausente), omitir esta seção

**Seção 4 — Nota de rodapé:**
- Alerta do Tema 1378 + regra de repetição em dobro (Tema 929) + disclaimer

**Seção 5 — Botões de ação (ou opções numeradas, no fallback):**
- "Prosseguir com todas as teses T1"
- "Selecionar teses manualmente"
- "Parar aqui com este relatório"
- "Analisar outro contrato"

Aguardar escolha do usuário antes de prosseguir para L3.
