# payload-schema.md — contrato de dados entre L3 e L4

A partir da v4 o relatório **não calcula nada**. A camada L3 monta um objeto JSON — o
*payload* — e `<rb> gerar` (renderizador `motores/relatorios.py`) produz os três entregáveis a partir dele.

Isso existe por um motivo concreto: enquanto o template calculava, o entregável ficava
amarrado a Price/SAC e à premissa de que havia excesso a decotar. Com o payload, qualquer
sistema de amortização e qualquer veredito cabem no mesmo chassi.

## Regra de ouro

**Todo número do payload sai dos motores (`motores/calculo.py`, `motores/cet.py`, `motores/cartao.py`, `motores/conta_corrente.py`).** Nenhum valor é
digitado à mão no JSON, nenhum é arredondado "para ficar bonito", nenhum é estimado. Se um
campo não tem origem documental ou de série oficial, ele não entra no payload — entra em
`lacunas`. Isso é a regra 0 aplicada à camada de saída.

## Estrutura

```jsonc
{
  "ramo":      "instrumento",                        // opcional: "instrumento" (padrão) | "conta" — ver "Ramo CONTA"
  "marca":     { "nome": "Escritório Exemplo" },   // cabeçalho — vem do gate L-1, nunca de exemplo
  "tipo_doc":  "Laudo pericial contábil",
  "titulo":    "…",
  "subtitulo": "…",                                 // 1 a 3 linhas, justificado
  "emissao":   "17 de agosto de 2026",

  "identificacao": {
    "referencia": "REF-2026-0001",
    "slug":       "ccb-000000",                  // entra no nome do arquivo
    "campos": [                                     // [rótulo, valor, ORIGEM DO DADO]
      ["Emitente", "…", "instrumento"],
      ["Encargos", "CDI + 3,00% a.a.", "instrumento"]
    ]
  },

  "kpis": [                                         // exatamente 4 no dashboard da planilha
    { "lab": "Custo efetivo real", "val": "18,3737%", "cor": "red", "sub": "ao ano" }
  ],                                                // cor: "red" | "grn" | "amb" | ausente

  "objeto":      ["parágrafo", "…"],
  "documentos":  [["Cédula …", "17/07/2025", "credor"]],
  "metodologia": ["parágrafo", "…"],

  "conferencia": {                                  // ramo instrumento; no ramo conta é o bloco `conta`
    "veredito":        "CONFORME",                  // ou "DIVERGENTE" — vem de conferir_saldo()
    "data_base":       "10/04/2026",
    "diferenca":       2357.74,                     // apurado pela credora − recalculado; OBRIGATÓRIO se DIVERGENTE
    "diferenca_pct":   0.15,
    "limiar_conforme": 10000,
    "natureza_cenarios": "conferencia",             // opcional: "conferencia" (default) | "recomposicao"
    "cenarios": [                                   // vem de tabela_contrafactual()
      { "premissa": "Apurado pela credora", "taxa_aa": null, "saldo": 1547563.74, "diferenca": null }
    ]                                               // taxa_aa em PONTOS PERCENTUAIS (18.3737, não 0.183737)
  },

  "achados": [                                      // motor de regras + auditar_cet()
    { "id": "A1", "tier": "T1", "resultado": "Ilícito",
      "titulo": "…", "detalhe": "…", "fundamento": "…",
      "regras": ["R04"] }                           // opcional: ids do motor; o `espelho` puxa os julgados por eles
  ],
  "valor_causa": "…",                               // opcional: só o `espelho` usa; ausente, sai [A DEFINIR]

  "ressalvas":    ["…"],                            // OBRIGATÓRIO quando houver achado pró-banco
  "lacunas":      ["…"],
  "premissas":    ["…"],                            // afirmado pelo operador e não comprovado — RENDERIZADO
  "agenda_jusia": ["prompt calibrado", "…"],        // SAI EM ARQUIVO APARTADO — não vai ao laudo

  "memoria": { "titulo": "…", "nota": "…", "colunas": [], "linhas": [[]] },   // inteiro = contagem (1, 2…), sem casas; decimal = valor (1000.0 → 1.000,00)
  "abas":    [ { "nome": "Apuração diária", "titulo": "…", "nota": "…",
                 "colunas": [], "larguras": [], "linhas": [[]], "totais": [] } ],

  "conclusao": ["…"],

  "assinatura": {                                   // gate da L-1 decide o tipo; as 4 chaves existem sempre
    "nome": "…", "registro": "OAB/UF 00.000", "entidade": "…", "cidade": "Cidade-UF"
  },

  "panorama": {
    "titulo": "…", "subtitulo": "…", "selo": "…",
    "verificado":   ["…"],
    "barras":       [ { "rotulo": "Cobrado", "valor": 1547563.74, "cor": "#A62B2B" } ],
    "secoes":       [ { "titulo": "…", "paragrafos": ["…"] } ],
    "recomendacao": ["…"]
  }
}
```

**`marca.nome` e `assinatura` vêm do operador gravado na L-1, nunca de exemplo.** Ausentes do
payload, `<rb> gerar` as preenche a partir do operador (`<rb> operador mostrar`); presentes,
prevalecem. Os valores acima são placeholders; qualquer nome, OAB, CRC ou cidade pré-preenchido
em arquivo do plugin é defeito (SKILL.md, L-1 e regra de conduta 26). O autoteste do
renderizador falha se o módulo contiver dado real de operador.

## Valores admitidos em `resultado`

`Conforme`, `Lícito` e `Revisão inviável` renderizam em verde. `Ilícito`, `Ilícito parcial`, `Divergência`,
`Contradição`, `Excesso`, `Prejudicial`, `Não discriminado` e `Base de cálculo` renderizam
em vermelho. `Lacuna`, `A demonstrar`, `A verificar`, `Excessivo` e `Inconsistência`
renderizam em âmbar. Valor fora dessa lista renderiza sem cor — sinal de que a L2
classificou errado — e `validar_detalhado()` devolve um aviso (não recusa).

A lista é espelhada em `CORES` / `RESULTADOS_ADMITIDOS` de `motores/relatorios.py` e vale para os
três entregáveis: a planilha usa a mesma classificação (âmbar é âmbar, não vermelho). Alterar
aqui sem alterar lá quebra o autoteste.

## `premissas` — renderizado

Lista de afirmações do operador sem comprovação documental (ex.: data de liberação informada
pelo cliente). Quando presente e não vazia, o PREMIUM ganha a seção "Premissas declaradas" em
caixa neutra, logo antes de "Lacunas documentais declaradas", com o texto fixo *"Afirmadas pelo
operador e não comprovadas documentalmente — os achados que delas dependem estão classificados
como A verificar"*, e a aba "Metodologia e fontes" da planilha ganha o bloco PREMISSAS
DECLARADAS. Ausente ou vazia, nada é renderizado. O PANORAMA não a imprime. A consequência é
de classificação: achado que depende de premissa é `A verificar`, nunca `Ilícito`.

## `conferencia.natureza_cenarios` — o que os cenários significam

Opcional. Dois valores:

- **`"conferencia"`** (default, texto atual) — rota pós-fixada/CET. A caixa de conclusão fala
  em "aferido pela metodologia efetivamente pactuada" e a nota sob a tabela diz que os cenários
  *não constituem proposta de recomposição do saldo*: medem o diferencial entre custo informado
  e custo praticado, para dimensionamento.
- **`"recomposicao"`** — rota Price/SAC (`motores/calculo.py`), em que os cenários SÃO a
  recomposição. A conclusão fala em "aferido pelos parâmetros contratados" e a nota diz que
  *os cenários recompõem o saldo sob a taxa revisada e constituem a base da repetição*.

Valor fora desses dois é erro de validação. Laudo Price/SAC com o texto default afirma por
escrito que a própria recomposição não é recomposição — por isso o campo existe.

## `conferencia.cenarios[*].taxa_aa` — escala

Pontos percentuais (`18.3737` renderiza `18,3737%`). O `motores/cet.py` devolve fração
(`0.183737`); se chegar assim, o renderizador trata `0 < taxa_aa < 1` como fração, multiplica
por 100 e `validar_detalhado()` avisa ("parece fração; convertida para %"). É guarda de
escala, não licença: converter na L3 continua sendo o certo.

## Três campos que a v3 não tinha e que agora são obrigatórios na prática

**`conferencia.veredito`.** Quando a reconstrução confirma o saldo do credor, dizer isso em
destaque é o que dá credibilidade ao resto do laudo. Relatório que só sabe acusar excesso
perde a causa em que o excesso não existe.

**`ressalvas`.** Todo achado que favorece o banco entra aqui, em caixa verde. É o que separa
laudo pericial de peça de parte — e é o que impede o assistente técnico do outro lado de
descobrir sozinho.

**`lacunas`.** Nenhuma conclusão pode extrapolar o acervo examinado. Cada documento ausente
que impediria conclusão definitiva vira uma linha aqui, e os achados dependentes dele são
classificados como `A verificar`, nunca como `Ilícito`.

## Validação — estrutural

O renderizador valida o payload antes de renderizar. Desde a v4.1 a validação é
**estrutural**: tudo o que o render lê com `[...]` é exigido, de modo que payload aprovado nunca
dá `KeyError` no meio da geração. Duas funções:

- `validar(payload, formatos) -> list[str]` — contrato antigo, mantido: lista de erros, vazia
  quando válido.
- `validar_detalhado(payload, formatos) -> {"erros": [...], "avisos": [...]}` — o que `gerar()`
  usa. `erros` recusa a geração (`ValueError`); `avisos` vão ao stderr e não recusam.

**Erros** (recusam): `marca.nome`; `identificacao.slug` e `identificacao.campos` (lista de
listas de 3); `conferencia.veredito` ∈ {CONFORME, DIVERGENTE}, `conferencia.data_base`,
`conferencia.diferenca_pct`, `conferencia.cenarios` (lista com `premissa`/`saldo`);
`conferencia.diferenca` quando DIVERGENTE; `conferencia.natureza_cenarios` fora dos dois
valores; `achados[*]` com `id`/`tier`/`resultado`/`titulo`/`detalhe`/`fundamento`;
`assinatura` com `nome`/`registro`/`entidade`/`cidade` (podem ser vazios, as chaves existem);
`memoria` e `abas[*]` com as chaves que o render lê; `panorama.titulo/subtitulo/selo/verificado/
barras/secoes/recomendacao` só quando o panorama foi pedido em `formatos`.

**Avisos** (não recusam): `kpis` com número diferente de 4 (o dashboard da planilha usa 4);
achado pró-banco (`Conforme`, `Lícito`, `Revisão inviável`) sem `ressalvas` ("há achado
pró-banco sem ressalva"); `resultado` fora da lista admitida; `taxa_aa` que parece fração.

`gerar()` confere ainda, antes de escrever qualquer arquivo, se `openpyxl` está instalado quando
a planilha foi pedida — sem ele, `ImportError` e nenhum HTML pela metade.

`<rb> autoteste` (que inclui o renderizador) roda antes da primeira geração de cada sessão.


## `agenda_jusia` não entra no laudo

O campo permanece no payload, mas `render_premium` não o imprime. Ele sai em
`INTERNO-agenda-pesquisa-<slug>.md`, com aviso de não juntar aos autos. Laudo pericial destina-se
ao processo: roteiro de pesquisa ainda não executada entrega a estratégia à parte contrária e
admite por escrito que as teses estão sem lastro. O laudo apenas sinaliza quais achados ficaram
pendentes de verificação — sem dizer o que será pesquisado sobre eles.

Ao apresentar os arquivos, o da agenda vai separado e sempre com a advertência de uso interno.

## Um payload por instrumento

`conferencia` tem um veredito, `memoria` é singular, a identificação é uma só. Duas cédulas num
payload fazem o veredito de uma valer como aval às duas. Em execução com N operações: N payloads,
`slug` prefixado por `opN-`, achados renumerados a partir de A1 em cada um, e bloco de advertência
de conexão em `objeto` e `conclusao`.

## Formatação numérica

Todo número que chega ao PDF passa por formatação pt-BR, e a fonte é uma só: `motores/comum.py`.
`comum.brl(v)` → `1.234,57` (Decimal, ROUND_HALF_UP); `comum.brl_rs(v)` → `R$ 1.234,57`;
`comum.pct(v)` → `12,35%` com `v` já em pontos percentuais; `comum.pt(f"{x:.4f}")` → `0,8500`
para fatores sem separador de milhar. O renderizador delega a elas (os `brl`/`pct` locais
só acrescentam `None -> "—"` e o default de 4 casas em `pct`, para taxa a.a.). F-string com
`:.2f` crua produz `0.85%` no laudo; `brl()` de outro motor com arredondamento próprio diverge
no centavo — e centavo divergente em perícia é munição para a parte contrária.

## Ramo CONTA

`ramo` é opcional: `"instrumento"` (padrão, tudo o que está acima) ou `"conta"`, a rota de conta
corrente, cheque especial e conta garantida (`motores/conta_corrente.py`). No ramo `conta` o bloco
`conferencia` não é exigido (se vier, é ignorado, com aviso) e passa a ser exigido o bloco `conta`.
O resto do payload — `marca`, `identificacao`, `kpis`, `objeto`, `documentos`, `metodologia`,
`achados`, `ressalvas`, `lacunas`, `premissas`, `memoria`, `abas`, `conclusao`, `assinatura` —
vale como no ramo instrumento. O `panorama` dispensa `selo` e `barras`: saem de `conta`.

O bloco **não se digita**: `conta_corrente.bloco_payload(reconciliacao, trinca, cenario_lider,
encontro, series, correcao=None)` o monta das saídas de `reconciliar`, `rodar_trinca` e
`encontro_de_contas`, copiando só os campos abaixo. Só `series` (da consulta ao conector) e
`correcao` (do `atualizar_debito`) vêm de fora do motor.

```jsonc
"ramo": "conta",
"conta": {
  "reconciliacao": { "veredito": "CONFORME", "pontos_conferidos": 212, "divergencias": [],
                     "competencias_sem_lancamento": [],
                     "janela": { "data_inicial": "2019-01-02", "data_final": "2024-06-28" } },
  "cenarios": [                                     // a trinca, na ordem do motor
    { "cenario": "C1_TAXA_MEDIA", "condicao": "…", "excesso_final": 48213.55, "favoravel": true },
    { "cenario": "C2_CAP_MENSAL", "omitido": true, "motivo": "…" } ],
  "cenario_lider": "C1_TAXA_MEDIA",                 // o escolhido no gate da C4; tem de ter rodado
  "encontro": { "cenario": "C1_TAXA_MEDIA", "excesso_final": 48213.55,
                "base_repeticao_simples": 31870.10, "base_repeticao_dobro": 16343.45,
                "competencia_corte": "2021-03", "nota": "…" },
  "series": [ { "serie": "Taxa média — cheque especial PF", "codigo": "…", "procedencia": "…",
                "periodo": "…" } ],
  "correcao": { "valor_corrigido": 61478.22, "data_final": "2024-06-28", "indice": "…", "hash": "…" }
}                                                   // `correcao` é opcional: o resumo do atualizar_debito
```

**Como sai.** Rótulos amigáveis da trinca (`ROTULOS_CENARIOS`, usados também na planilha):
`C1_TAXA_MEDIA` → "C1 — Taxa média BACEN", `C2_CAP_MENSAL` → "C2 — Capitalização mensal",
`C3_TAXA_LIMPA` → "C3 — Só encargos sem lastro".

- **PREMIUM** — as mesmas seções e a mesma ordem; a seção 3 vira "3 — Reconciliação do extrato e
  recomposição da conta": caixa do veredito da reconciliação (pontos conferidos e janela), tabela
  da trinca (condição de aplicabilidade e excesso final; omitido com o motivo; o líder marcado),
  quadro do encontro de contas (bases simples e dobro, competência de corte e nota), procedência
  das séries e a correção do conector, quando há. Logo depois, em caixa neutra, a advertência
  fixa: *"Os valores apurados na conta corrente formam uma faixa entre cenários de recomposição
  e não um valor fechado. Eles instruem o pedido de prova pericial contábil e dependem de
  confirmação pericial."*
- **PANORAMA** — KPIs do payload; o selo diz se há excesso **no cenário líder** (o CONFORME do
  extrato prova a extração, não a ausência de excesso, e vai à parte, em "O que foi verificado");
  barras dos cenários não omitidos; as mesmas seções de texto; a mesma advertência.
- **PLANILHA** — Dashboard com reconciliação, trinca e encontro; abas de memória como hoje
  (`abas`); "Metodologia e fontes" com as séries, a correção e a advertência.

**Erros** (recusam, além das chaves ausentes de cada bloco):

- `reconciliacao.veredito` fora de CONFORME/DIVERGENTE; **DIVERGENTE**, `divergencias` ou
  `competencias_sem_lancamento` não vazios. É a lacuna bloqueante da C1: laudo de conta não se
  gera com extração não reconciliada.
- `cenario_lider` que não consta de `cenarios` ou que foi omitido; `encontro.cenario`, se
  presente, diferente do líder.
- `base_repeticao_simples + base_repeticao_dobro` diferente de `excesso_final` por mais de 0,01.
- Cenário com `favoravel: false` e `ressalvas` vazio: cenário desfavorável é reportado, não
  escondido (`camadas/C0-C6-rota-conta.md`, C4, item 2).
- Valor monetário que não é número (texto, booleano, NaN); `ramo` fora de instrumento/conta.

**Avisos:** `pontos_conferidos` igual a zero (a extração não foi conferida contra saldo
impresso), `series` vazia, `encontro.excesso_final` diferente do excesso do líder, `conferencia`
sobrando no ramo conta e bloco `conta` sobrando no ramo instrumento.

## Tema visual

A identidade visual do escritório (cores, fontes, logo, linha de cabeçalho e rodapé) fica em
`tema.json`, na **mesma pasta** do `operador.json` (`${CLAUDE_PLUGIN_DATA}` no Claude Code), fora
do pacote e do repositório. O `<rb> gerar` o lê sozinho; `--sem-tema` força o visual padrão e o
JSON de saída traz `"tema": "<nome>"` ou `"padrao"`. Sem `tema.json`, o HTML é o do plugin, byte
a byte. Gravar, ver e apagar: `<rb> tema salvar --arquivo tema.json`, `tema mostrar`, `tema remover`
(todos com `--config-dir`). O esquema é fechado — chave desconhecida é erro — e o código está em
`motores/tema.py`:

| Campo | O que é |
|---|---|
| `nome` | Rótulo do tema (ex.: "Identidade do escritório") |
| `skill_origem` | Opcional. Skill de layout de onde o tema foi importado; só registro |
| `cores` | `tinta`, `destaque`, `destaque_claro`, `fundo_destaque` — só `#RRGGBB`. Viram `--ink`, `--gold`, `--glt` e `--gpale` do CSS e as cores equivalentes da planilha |
| `fontes` | `titulo`, `texto`, `mono` — nome de família (letras, números, espaço e hífen); o fallback do CSS fica |
| `fontes_url` | Opcional. Só `https://fonts.googleapis.com/css2?...`. Sem ela, o link do Google cobre apenas as famílias padrão que o tema ainda usa; fonte do tema sem link depende de estar instalada |
| `logo` | PNG, JPG ou SVG de até 300 KB, embutido como data URI no cabeçalho, à esquerda da marca (altura de até 14 mm). SVG com `<script` ou atributo de evento é recusado. Na gravação, o arquivo é copiado para a pasta de configuração |
| `cabecalho_linha` | Opcional. Texto curto sob a marca (endereço ou registro da sociedade) |
| `rodape` | Opcional. Substitui "Documento confidencial" no rodapé |

**O que não muda com o tema:** as cores do semáforo (vermelho, verde e âmbar, com seus fundos) —
o significado jurídico não muda com a marca —, a estrutura do laudo, o texto das seções e as
fontes de reserva. Todo texto do tema passa por `esc()` e nada dele entra cru no CSS fora das
variáveis validadas. A planilha usa as cores de destaque e tinta nas faixas e cabeçalhos; o logo
não vai a ela. A validação do tema avisa (não recusa) fonte própria sem `fontes_url` e tinta que
contrasta pouco com o papel ou com o fundo de destaque.

## Quando não há excesso

`resultado: "Revisão inviável"` e KPIs de parcela zerados são saída legítima. Laudo que só sabe
acusar excesso perde a causa em que o excesso não existe — e a declaração de conformidade é o que
dá credibilidade à impugnação seletiva que vier depois.
