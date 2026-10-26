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

  "conferencia": {
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
      "titulo": "…", "detalhe": "…", "fundamento": "…" }
  ],

  "ressalvas":    ["…"],                            // OBRIGATÓRIO quando houver achado pró-banco
  "lacunas":      ["…"],
  "premissas":    ["…"],                            // afirmado pelo operador e não comprovado — RENDERIZADO
  "agenda_jusia": ["prompt calibrado", "…"],        // SAI EM ARQUIVO APARTADO — não vai ao laudo

  "memoria": { "titulo": "…", "nota": "…", "colunas": [], "linhas": [[]] },
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

## Ramo CONTA — pendente

O payload ainda não tem os campos da rota CONTA (`motores/conta_corrente.py`): veredito da
reconciliação com pontos conferidos, trinca de cenários com condições e série de indébito por
competência. `conferencia`/`cenarios` deste schema modelam saldo de instrumento, não evolução
de conta. Até o ramo existir, a C6 segue o fallback descrito em
`camadas/C0-C6-rota-conta.md` (item 3 da C6): entregável HTML no padrão visual financeiro com o
CSS canônico de `html-pdf-impressao-segura`, com metodologia, veredito da reconciliação,
procedência das séries, trinca, ressalvas, lacunas e a advertência da regra de conduta 20.
Pendência declarada no CHANGELOG e em ARCHITECTURE.md.

## Quando não há excesso

`resultado: "Revisão inviável"` e KPIs de parcela zerados são saída legítima. Laudo que só sabe
acusar excesso perde a causa em que o excesso não existe — e a declaração de conformidade é o que
dá credibilidade à impugnação seletiva que vier depois.
