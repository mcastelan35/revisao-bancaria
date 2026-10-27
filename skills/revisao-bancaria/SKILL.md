---
name: revisao-bancaria
description: "Revisao bancaria por rotas. INSTRUMENTO: contratos (financiamento, consignado, capital de giro, cedulas, leasing) com 40 regras, Price/SAC, pos-fixados e CET; ramo cartao (teto Lei 14.690); ramo SFH/SFI (Lei 4.380, Lei 9.514, alienacao fiduciaria): saldo indexado, amortizacao negativa, capitalizacao vedada, checklist de consolidacao e leilao. CONTA: extratos de conta corrente, garantida e cheque especial (saldo diario, art. 354 CC, tres cenarios, encontro de contas). Taxas BACEN via Radar Apogeu, gates, laudo PREMIUM/PANORAMA e planilha. Use SEMPRE que o usuario enviar contrato bancario, extrato, fatura de cartao ou financiamento habitacional/imobiliario, pedir revisional, laudo, impugnacao a laudo do credor, ou mencionar juros abusivos, SFH, SFI, CEF, TR, PES, CES, FCVS, consolidacao da propriedade, leilao extrajudicial, purga da mora, DL 70/66, sumulas 382, 450, 530, 539, 541, temas 972 e 1378, TAC, TEC, comissao de permanencia, seguro prestamista, venda casada, anatocismo."
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - Bash(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - PowerShell(python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - Bash(uv run --no-project --python 3.12 --with openpyxl python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
  - PowerShell(uv run --no-project --python 3.12 --with openpyxl python "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py" *)
metadata:
  version: "6.0.0"
  connector: "Radar Apogeu (BACEN/SGS, via MCP) — pré-requisito ATIVO"
---

# Revisão bancária — orquestrador

Análise revisional bancária em **duas rotas** (INSTRUMENTO e CONTA, mais os ramos cartão e
SFH/SFI dentro da primeira), escolhidas pelo gate R0, com gates de aprovação obrigatórios em
cada camada. Este arquivo é o **orquestrador**: diz a ordem, o que carregar e as regras de
conduta. O comportamento de cada camada está em `camadas/` — fonte normativa que este arquivo
não repete. Em divergência entre este arquivo e uma camada, a camada prevalece no seu escopo e
a divergência é bug a corrigir.

| Rota | Objeto | Camadas | Motor | Arquivo |
|---|---|---|---|---|
| **INSTRUMENTO** | contrato e cláusulas | L-1 → L0 → L4 | `motores/calculo.py` (Price/SAC) · `motores/cet.py` (pós-fixado/CET) | `camadas/L0…L4-*.md` |
| **INSTRUMENTO · SFH/SFI** | mútuo habitacional/imobiliário com saldo indexado | L-1 → L0 → L1 → L2 + L2b → L3 → L4 | `motores/calculo.py` (`tabela_sfh`, `comparar_sfh`) | `camadas/L0…L4-*.md` + `camadas/L2b-procedimento-expropriatorio.md` |
| **INSTRUMENTO · cartão** | faturas | L-1 → L0 → `camadas/analise-faturas-cartao.md` (substitui L1–L3) → L4 | `motores/cartao.py` | `camadas/analise-faturas-cartao.md` |
| **CONTA** | extrato e evolução do saldo | L-1 → C0 → C6 | `motores/conta_corrente.py` | `camadas/C0-C6-rota-conta.md` |

As rotas compartilham conector BACEN, cascata de taxa, qualificação do regime, encargos sem
lastro, exibição de documentos e encontro de contas. **Não compartilham motor nem regra de
capitalização**: em mútuo com prestação fixa, duodécuplo e prestação constante afastam
anatocismo; em rotativo, a discussão é periodicidade e metodologia; em SFH/SFI a lógica é
invertida — a capitalização inferior à anual é vedada mesmo pactuada e o anatocismo real é a
incorporação de juros impagos ao saldo indexado (amortização negativa). Aplicar a leitura de
uma rota ou ramo na outra é defeito grave.

Pergunta pontual sem documento ("essa taxa é abusiva?", "qual a média do BACEN para tal
modalidade?") é da skill `triagem`, que responde com uma consulta ao conector. Identificação do
operador e diagnóstico do ambiente fora de uma análise: skill `configurar`.

## Ambiente — comando base

Caminhos deste arquivo são relativos à pasta da skill
(`${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria`; fora do Claude Code, a pasta onde está esta
SKILL.md).

**Comando base** (`<rb>` neste texto): `python3 "${CLAUDE_PLUGIN_ROOT}/skills/revisao-bancaria/revisao.py"`
— no Windows, `python` no lugar de `python3`. A planilha exige `openpyxl`; sem ele, prefixe com
`uv run --no-project --python 3.12 --with openpyxl` (e use `python`) ou rode a skill
`configurar`. Saída em JSON (salvo `autoteste`). Códigos: 0 ok · 1 autoteste com falha ·
2 erro de entrada · 3 operador não configurado.

| Necessidade | Comando |
|---|---|
| Autoteste dos motores — antes da 1ª apuração da sessão | `<rb> autoteste` |
| Regras aplicáveis ao caso (L2, C3) | `<rb> regras --tipo T --regime consumerista\|civil_empresarial --data-contrato AAAA-MM-DD [--data-consolidacao AAAA-MM-DD] [--categorias a,b] [--formato resumo\|padrao\|completo]` |
| Texto integral de regra ou súmula, para fundamentar | `<rb> regra R15 R16` · `<rb> sumula 530 541` |
| Julgados validados das regras do caso (estratégia, petição) | `<rb> jurisprudencia consultar --regras R04,R13` · `<rb> jurisprudencia cobertura` |
| Espelho da petição inicial (gate pós-entrega da L4) | `<rb> espelho payload.json --saida <pasta de saída> --config-dir "${CLAUDE_PLUGIN_DATA}"` |
| Posição do contrato nos marcos MT01–MT10 (L0) | `<rb> marcos --data-contrato AAAA-MM-DD [--data-consolidacao AAAA-MM-DD]` |
| Série BACEN da modalidade | `<rb> serie --buscar "cheque especial"` · `<rb> serie --modalidade aquisicao_veiculo_pf` |
| Razão contratada/média e limiares 1,5x / 2,0x | `<rb> razao --contratada-pct 2.99 --unidade-contratada am_efetiva --media-pct 1.85 --tipo T` |
| Simulação Price/SAC contratado × revisado | `<rb> comparar --sistema price --pv 50000 --n 48 --taxa-contratada-pct 2.99 --taxa-revisada-pct 1.85` |
| Entregáveis (L4, C6) | `<rb> gerar payload.json --saida <pasta de saída> --formatos premium,planilha --config-dir "${CLAUDE_PLUGIN_DATA}"` — PDF por padrão (`--pdf auto`; `sim` exige, `nao` desliga) e tema do escritório lido da pasta de configuração (`--sem-tema` força o padrão) |
| Operador (L-1) | `<rb> operador mostrar --config-dir "${CLAUDE_PLUGIN_DATA}"` · `<rb> operador salvar --tipo advogado\|contador --nome … --registro … --entidade … --cidade … --skill-peticao … --skill-layout … --config-dir "${CLAUDE_PLUGIN_DATA}"` |
| Identidade visual (opcional, `configurar`) | `<rb> tema mostrar --config-dir "${CLAUDE_PLUGIN_DATA}"` · `<rb> tema salvar --arquivo tema.json --config-dir "${CLAUDE_PLUGIN_DATA}"` · `<rb> tema remover --config-dir "${CLAUDE_PLUGIN_DATA}"` |

Cálculo que a CLI não cobre (reconstrução pós-fixada, SFH, conta, cartão, decote, auditoria da
memória do credor): numa sessão Python, `sys.path.insert(0, "<pasta da skill>")` e
`from motores import calculo, cet, cartao, conta_corrente`, com as funções citadas nas camadas.

## Ordem de execução

1. **R0 — gate de roteamento** (`camadas/R0-gate-roteamento.md`): antes de abrir qualquer
   documento, uma pergunta sobre o que o usuário espera; documento anexado permite inferir e
   confirmar em uma linha, nunca dispensa a confirmação. Inclui o **R0-b**: contar os
   instrumentos — um laudo por instrumento, sem exceção.
2. **L-1 — identificação do operador** (abaixo).
3. **Modos** (só INSTRUMENTO): *auditoria rápida* (L0+L1+L2, semáforo em um turno) ou
   *revisão completa* (L0–L4 com gates). A rota CONTA tem gates próprios.
4. A rota escolhida, camada a camada, com gate ao fim de cada uma. Rota AMBAS executa CONTA
   primeiro (o saldo recomposto alimenta o encontro de contas).

## Mapa de arquivos e o que carregar

| Quando | Carregar |
|---|---|
| Sempre, antes da 1ª consulta de taxa | `referencia/bacen-consulta.md` (protocolo do conector) |
| L1, L2 e C3 | `<rb> regras …` — motor determinístico sobre `dados/regras-bancarias.json` (40 regras, 10 marcos, 14 categorias, 23 súmulas, 24 séries, 10 tipos, 12 termos de CP disfarçada, `pendencias_jurisprudenciais`). O JSON inteiro só se lê para manter o próprio motor |
| Antes do 1º cálculo da sessão | `<rb> autoteste` |
| Contrato indexado ou com CET | `motores/cet.py` |
| Ramo SFH/SFI com consolidação, leilão ou execução extrajudicial | `camadas/L2b-procedimento-expropriatorio.md` (checklist documental R39/R40) |
| Cartão | `camadas/analise-faturas-cartao.md` + `motores/cartao.py` |
| Rota CONTA, antes de fundamentar | `referencia/repertorio-jurisprudencial-contas.md` — **ESQUELETO**: entrada `[PENDENTE]`/`[CONFERIR]` não se cita |
| L4 / C6 | `referencia/payload-schema.md` → `<rb> gerar` |
| Estratégia e petição (INSTRUMENTO) | `referencia/repertorio-jurisprudencial.md` — pelo `<rb> jurisprudencia consultar`, nunca lido inteiro |
| Pesquisa consolidada (INSTRUMENTO) | `referencia/pesquisa-base.md` |
| Atualização do conector ou série que não responde | `referencia/teste-contrato-bacen.md` |

Utilitários compartilhados (formatação pt-BR, parse numérico estrito, competências, guarda de
escala de taxa) estão em `motores/comum.py` — nenhum motor formata ou arredonda por conta.

## L-1 — Identificação do operador

Rodar `<rb> operador mostrar --config-dir "${CLAUDE_PLUGIN_DATA}"`. Configurado: confirmar em
uma linha ("Relatórios sairão em nome de {nome} — {registro}. Trocar?"). Código 3: perguntar,
por opção ou texto, **tipo** (`advogado` | `contador`), **nome**, **registro** (OAB/UF 00.000
ou CRC/UF 000000/O), **entidade** (sociedade ou escritório, se houver), **cidade** (praça da
assinatura, ex.: Cidade-UF) e **skill de peticionamento** que receberá o briefing da L4/C6 (se
o operador tiver uma), e gravar com `<rb> operador salvar …`. A pasta de dados do plugin
sobrevive a atualizações; fora do Claude Code vale a pasta de configuração do usuário. Sem
como gravar (ambiente efêmero): memória do usuário; senão, repetir a pergunta a cada sessão.

O tipo muda o entregável, não só a assinatura: laudo pericial para contraditório em juízo é
assinado por contador com CRC e sai no cabeçalho do escritório contábil; parecer técnico que
instrui peça é assinado por advogado com OAB. O `gerar` preenche `marca` e `assinatura` a
partir do operador gravado quando o payload não as traz — não copiar identidade à mão. Sem
dados, a assinatura sai em branco com a pendência no rodapé. **Nunca** substituir por nome de
terceiro; nome, OAB ou marca pré-preenchidos em arquivo do plugin são defeito — a suíte de
testes falha se encontrar.

## Regra crítica: abusividade de juros

A taxa contratada só é abusiva quando supera **1,5x a taxa média BACEN** da mesma espécie
(exceção: tipos `sfh`, `sfi` e `imobiliario_fora_sfi`, onde a R15 está desligada — regra 27).
Abaixo de 1,5x: "dentro da faixa de mercado". Entre 1,5x e 2,0x: "zona de abusividade"
(contestável). Acima de 2,0x: "fortemente abusiva". A razão e os limiares saem de
`<rb> razao` (aritmética decimal, limiares lidos da R15) e são exibidos em **toda** análise de
juros remuneratórios, em qualquer rota e qualquer tipo de contrato; o que muda com o regime
(consumerista / civil-empresarial) é a consequência e o tier — bloco `regime` da R15, já
resolvido por `<rb> regras`. Alerta permanente do **Tema 1378/STJ** em toda análise; se a
pendência estiver vencida (`alertas_vencidos` na saída de `<rb> regras`), emitir também o
alerta vencido e não concluir sem validar via `pesquisa-jurisprudencial-jusia`.

## Conector BACEN — fonte única, cache primeiro

O conector Radar Apogeu está na sessão, ativo e validado — premissa, não hipótese. Sem
sondagem, sem teste de disponibilidade, sem caminho paralelo. Protocolo completo em
`referencia/bacen-consulta.md`; o essencial:

| Necessidade | Chamada |
|---|---|
| Código por modalidade, identidade autoritativa, alcance do cache | `<rb> serie` resolve a modalidade sem quota; `listar_series_bacen({ filtro })` só se o mapeamento não cobrir o caso — uma vez por sessão |
| Taxa média da modalidade (séries mensais 254xx, `data_inicial` no dia 1º) | `consultar_taxa_bacen({ codigo \| codigos[≤6], data_inicial, data_final })` — estatísticas prontas |
| Série diária inteira do indexador (CDI 12, Selic 11, TR 226) | `consultar_taxa_bacen({ codigo, …, pontos: "completos" })` → `cet.carregar_de_consultar_taxa_bacen` |
| Índice do saldo no SFH/SFI (TR, poupança, IPCA) | `consultar_indice({ codigo, data_inicial, data_final })` |
| Correção do indébito parcela a parcela | `atualizar_debito({ valores: [...], segmentos \| regra, data_final })` — uma chamada; o regime (segmentos montados ou a regra pronta `civil_lei_14905`) é escolha do operador no gate, declarada na metodologia |

Orçamento do caso típico: **uma** `consultar_taxa_bacen` (em lote quando duas séries) +
`atualizar_debito` se houver indébito. Chamada é a unidade de quota do aluno. Antes de
assinar: `conferir_fator()` contra o `fator_acumulado` da resposta (pega série recortada e
calendário divergente — divergência invalida a reconstrução); `ponta` — o motor precisa da
série até o **dia útil anterior** à data-base (o conector reporta a ponta contra a data final
inclusive; ponta insuficiente é lacuna bloqueante: recuar a data-base e declarar);
`procedencia` registrada na metodologia. `bash`/`curl` na API do BACEN é defeito em qualquer
cenário; `web_fetch` só como contingência declarada após `falha_fonte`. Período vazio não é
falha de fonte.

## Regras de conduta

0. **Proibição de presunção — prevalece sobre todas.** Só há duas origens de dado: extraído do
   documento enviado ou informado expressamente pelo usuário. Dado ausente é lacuna bloqueante:
   pedir e parar. Jamais valor "de praxe", jamais estimar taxa que deveria constar do documento,
   jamais interpolar competência, jamais arbitrar sistema de amortização, jamais adivinhar
   escala de taxa (o motor recusa `7,9` onde espera `0,079`) ou número ambíguo (`1.500`). Toda
   linha do relatório declara a origem do dado.
1. **Taxa de juros é bloqueante.** Não prossegue sem a taxa (contrato, proposta, planilha CET,
   extrato, app do banco). Só quando o usuário confirmar que não há como obtê-la: R16
   (Súmula 530 — média BACEN substitutiva). Nunca "taxa pendente" em relatório.
2. **Comparação BACEN na L0, uma consulta só.** Assim que a taxa for obtida, consultar a série
   na janela inteira do contrato e calcular a razão antes do gate de intake; L2, L3 e C2
   reaproveitam esse resultado — não reconsultar. Razão abaixo de 1,5x se diz no próprio gate.
3. **Jurisprudência só do acervo.** Súmulas, temas e precedentes do `regras-bancarias.json`
   (lidos por `<rb> regra` e `<rb> sumula`), do repertório validado (`<rb> jurisprudencia
   consultar`, que só devolve entrada conferida no Jusbrasil ou no portal do TJPR e dentro da validade) e do
   repertório da rota CONTA, nada além. Toda
   ementa citada vai **na íntegra**, padrão sanduíche (tese → ementa integral → identificação
   completa: tribunal, número, relator, órgão, datas → aplicação). Entrada `[PENDENTE]`/
   `[CONFERIR]` não se cita; completar identificação por memória é falta absoluta. Fora do
   acervo: dizer que não está coberto e remeter a `pesquisa-jurisprudencial-jusia`.
4. **Regra suspensa ou sem precedente consolidado não conclui.** `status: suspensa` ou
   `sem_precedente_consolidado` (`conclusiva: false` na saída do motor) → só o `alerta`,
   decisão do advogado. Pendência vencida → alerta vencido obrigatório.
5. **Sempre mostrar a razão contratada/média** e o limiar aplicado (regra crítica).
6. **Gates são obrigatórios.** O usuário controla o fluxo; nenhuma camada avança sem aprovação.
7. **Classificar pela natureza, não pelo nome.** Comissão de permanência disfarçada se detecta
   pela função econômica (12 termos da R03 + heurística), não pela nomenclatura.
8. **Encargos lícitos existem e vão em ressalvas.** O que não é atacável (tarifa de cadastro
   inicial, IOF pactuado, seguro voluntário) e todo achado que favorece o banco entram em
   `ressalvas`. Laudo que só acusa é peça de parte.
9. **Repetição em dobro tem corte e regime.** Dobro só para pagamentos posteriores a
   30/03/2021 (Tema 929) e só em regime consumerista; a competência que contém o corte vai
   inteira na base simples (menor excesso).
10. **Painel inline antes de arquivo.** Na L2/C2/C4 o resultado é apresentado no chat antes de
    qualquer arquivo — como widget visual quando a sessão tiver ferramenta para isso; senão,
    tabela com semáforo em texto. O HTML/XLSX só sai na L4/C6 após aprovação.
11. **Conector é a fonte única das taxas.** Cache primeiro; `pontos: "completos"` para série
    diária; `conferir_fator`, `ponta` e `procedencia` antes de assinar (seção acima).
12. **Cálculo só pelos motores da rota.** Nenhuma prestação, saldo, decote, SMD ou excesso nasce
    fora de `motores/` (`calculo`, `cet`, `cartao`, `conta_corrente`). `<rb> autoteste` antes da
    primeira apuração da sessão; falha interrompe. Em SAC o saldo é idêntico nos dois cenários
    — plotar a prestação (`plotar` vem resolvido). Cenário revisado mais caro que o contratado
    sai com `favoravel: false` e vai em ressalvas.
13. **Decote de encargo financiado tem dois números.** `decotar_encargo_financiado()` devolve
    `valor_presente` (= o encargo) e `impacto_nominal` (soma das diferenças de parcela, que já
    contém os juros sobre o encargo). Nunca corrigir monetariamente o `impacto_nominal` como se
    fosse valor presente; para `atualizar_debito` usar as diferenças parcela a parcela.
14. **Relatório = payload renderizado.** Dois entregáveis (PREMIUM e PANORAMA) mais a
    PLANILHA, por `<rb> gerar` a partir do payload do `referencia/payload-schema.md` — nas duas
    rotas: a CONTA usa `ramo: "conta"` com o bloco montado por `conta_corrente.bloco_payload`.
    Não editar CSS, não escrever HTML novo, não digitar número que não saiu do motor. Sem
    exceção de rota. O PDF de cada HTML sai do próprio `gerar` quando houver navegador
    Chromium (Chrome, Edge, Chromium ou Brave) e a identidade visual do escritório, quando
    configurada (`tema.json`), é aplicada por ele; sem navegador, o HTML segue e o JSON do
    `gerar` diz como fechar o PDF à mão.
15. **Cartão é ramo próprio.** Sem Price nem SAC; a fatura é a fonte da taxa (ausente = lacuna,
    não média BACEN); IOF apartado do teto (Res. CMN 5.112/2023); competências anteriores a
    03/01/2024 ficam fora do teto; compras novas roladas constituem dívida própria
    (`novas_dividas`); gate obrigatório de valor original, eventos e completude.
16. **Texto justificado** em todo parágrafo corrido dos entregáveis HTML.
17. **Rota travada no R0 e não se mistura.** Motor da rota é o único motor. AMBAS = CONTA
    primeiro.
18. **Qualificação do regime é prejudicial.** `regime = consumerista | civil-empresarial`
    antes de calcular ou fundamentar — é parâmetro obrigatório de `<rb> regras`. PJ com capital
    de giro ou conta garantida é relação de insumo por regra; vulnerabilidade não se presume —
    exige elementos concretos gravados em `premissas`; sem eles, achados dependentes do CDC
    ficam `A verificar`.
19. **Fundamentos revogados estão banidos.** Nunca art. 192, §3º, CF (EC 40/2003), teto de 12%
    a.a. a instituição financeira, Lei de Usura como vedação absoluta (Súmulas 596/STF e
    382/STJ) ou anatocismo proibido per se. Em laudo de terceiro, apontar o vício ao impugnar.
20. **A rota CONTA entrega faixa, não ponto, e instrui perícia.** Sempre três cenários com
    condição de aplicabilidade; metodologia auditável; advertência de que os valores dependem
    de confirmação pericial; briefing com requerimento de prova pericial contábil.
21. **Prompt de pesquisa nunca vai ao laudo.** `agenda_jusia` sai em
    `INTERNO-agenda-pesquisa-<slug>.md`, apartado e com aviso de não juntar aos autos.
22. **Audite a memória do credor antes de recalcular o contrato.** Em execução ajuizada o
    resultado útil costuma estar na planilha: as seis conferências da L3 vêm primeiro.
23. **Critério de menor excesso.** Duas leituras defensáveis → apurar nas duas, adotar a menor,
    declarar a descartada na metodologia.
24. **"Não há excesso" é resultado.** Razão abaixo de 1,5x, capitalização pactuada e prestação
    que reproduz a taxa → veredito `revisão contratual inviável — atacar a composição do
    débito`, dito no gate da L0.
25. **Um laudo por instrumento.** N instrumentos → N payloads e N laudos (R0-b), cada um com
    veredito próprio, achados renumerados, `slug` `opN-` e advertência de conexão. Consolidar
    é erro material, não de diagramação.
26. **Identidade do operador nunca é pré-preenchida** (L-1).
27. **SFH/SFI invertem a leitura do SFN.** Nos tipos `sfh`, `sfi` e `imobiliario_fora_sfi`
    as regras em `regras_desligadas` (R15; R18/R19) não se aplicam — nem como lícitas: sem
    badge de razão BACEN, sem "capitalização pactuada válida". No SFI a taxa anual acima do
    duodécuplo prova a capitalização vedada (R35, REsp 2.086.650/MG); no SFH a vedação é em
    qualquer periodicidade, mas a Price por si não prova anatocismo (R34) — a prova é a conta
    gráfica integral rodada em `comparar_sfh` (juros impagos incorporados × conta apartada,
    R36). Saldo corrige antes de amortizar (Súmula 450, R37) e a amortização negativa não afasta
    a mora (REsp 1.476.395/RS): o laudo não pede descaracterização da mora por esse fundamento.
    Consolidação, leilão ou execução extrajudicial nos autos → `L2b` obrigatória (R39/R40), com
    o bloco contrário em `ressalvas`. O conector entra por `consultar_indice` (série do índice
    do saldo), não pela série de modalidade. Precedentes do ramo estão `[CONFERIR]` quanto a
    relator, órgão e data de julgamento — a regra 3 impede citá-los em peça antes de completar.
28. **Aplicabilidade sai do motor de regras.** Tipo, regime, marcos temporais, regras
    desligadas, status e validade das pendências são resolvidos por `<rb> regras` — não
    reinterpretar o JSON à mão. Item em `confirmar` é pergunta ao operador no gate (dado
    ausente ou decisão de regime), nunca aplicação silenciosa; item em `nao_aplicaveis` traz o
    motivo e só volta por decisão expressa do operador, registrada em `premissas`.

## Interação com outras skills

`triagem` (pergunta pontual de taxa, sem documento) e `configurar` (operador e ambiente), do
próprio plugin. `pesquisa-jurisprudencial-jusia` (validar precedentes e preencher o repertório
CONTA — a única via para tirar uma entrada de `[PENDENTE]`); skill de peticionamento gravada
na L-1 (`skill_peticao`, a skill canônica do escritório: recebe o espelho da inicial da L4 e o
briefing da C6; sem ela, o espelho sai em formato neutro); `briefing-estrategico` (risco para o
cliente antes de ajuizar); `proposta-comercial` (prospecção); `liquidacao-correcao-debitos`
(quando a correção do indébito exigir regime que o `atualizar_debito` não parametriza);
`design-quality-guard` (checklist visual); a skill de layout do escritório (`skill_layout` do
operador, de onde a `configurar` importou o `tema.json`; o `gerar` nunca a chama). As skills
externas são opcionais: ausentes, entregar o briefing em markdown. Conector
**Radar Apogeu**: `listar_series_bacen`, `consultar_taxa_bacen`, `consultar_indice`,
`atualizar_debito`.

## Versionamento

Uma versão só, a do plugin: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`,
`metadata.version` aqui, `versao` do JSON, `VERSAO` de `motores/__init__.py`, `CHANGELOG.md` e
`ARCHITECTURE.md` — `ferramentas/verificar_consistencia.py` e a suíte de testes falham se
divergirem. Ao mudar o JSON: julgamento de tema → `status` e `consequencia` da regra,
`verificado_em` da pendência; nova súmula → `sumulas_consolidadas` + regra; nova resolução CMN
→ `marcos_temporais` com a `base` do corte (`regras_afetadas` é derivado do `corte_temporal`
das regras, não se edita à mão); cancelamento → `status: superada`, nunca deletar. Registrar
em `notas_de_versao` e no CHANGELOG.
