# L4 — Entregáveis e saída

Camada do plugin `revisao-bancaria`. Produz os entregáveis da análise e
orquestra o fluxo pós-entrega.

## O que mudou na v4 (08/2026)

Eram seis formatos, três HTML e três XLSX, cada um com a lógica de cálculo embutida em
`<script>` e gerado por edição manual das constantes `P`, `rC`, `rR` e `n`.

Passaram a ser **dois entregáveis mais uma planilha**, renderizados por
`motores/relatorios.py` a partir de um payload:

| Entregável | O que é | Para quem |
|---|---|---|
| **PREMIUM** | Laudo pericial completo, A4 retrato, com memória de apuração, quadro de achados com fundamento e tier, ressalvas de imparcialidade, lacunas declaradas e agenda de validação jurisprudencial | Instrução processual, assistente técnico, contraditório |
| **PANORAMA** | Panorâmica estratégica de duas a três páginas, com selo de veredito, KPIs, barras comparativas, semáforo resumido e recomendação | Reunião com o cliente, decisão de ajuizar |
| **PLANILHA** | XLSX único, dashboard na primeira aba, abas de memória, aba de metodologia e lacunas, A4 retrato ajustado à largura | Conferência independente, anexo processual |

**O template não calcula mais nada.** Todo número vem do payload, produzido pelas camadas
L0-L3 com `motores/calculo.py` e `motores/cet.py`. Ver `referencia/payload-schema.md`.

## Entrada

Recebe da L3: reconstrução do saldo, veredito de conferência, cenários contrafactuais,
achados classificados do motor de regras e da auditoria de CET, ressalvas, lacunas
declaradas e a ficha de intake da L0 com a origem de cada dado.

## Um laudo por instrumento

Antes do gate, conferir o resultado do R0-b. **N instrumentos, N payloads, N laudos.** O chassi
é mono-instrumento: `conferencia` tem um veredito só. Duas cédulas num payload fazem o veredito
de uma valer como aval às duas — erro material, não de diagramação. Cada laudo leva bloco de
advertência de conexão em `objeto` e `conclusao`, e `slug` prefixado por `opN-`.

## Gate de entrega (obrigatório — pergunta com botões)

| Opção | Gera | `--formatos` |
|---|---|---|
| Premium (laudo pericial) | HTML premium + planilha | `premium,planilha` |
| Panorâmica (executivo) | HTML panorama + planilha | `panorama,planilha` |
| Os dois | premium + panorama + planilha | omitir |
| Só a planilha | XLSX | `planilha` |

A validação respeita o gate: `panorama` só é campo obrigatório quando o panorama foi pedido.

Não oferecer mais os rótulos "Clássico", "Executivo" e "Pericial" — foram aposentados.

## Geração — processo obrigatório (5 passos)

**Passo 1 — Autoteste.** Se ainda não rodou nesta sessão:

```bash
<rb> autoteste      # todos os motores, inclusive o renderizador e o motor de regras
```

Qualquer falha interrompe a L4. Não gerar entregável com motor quebrado. `relatorios` PULADO
por falta de `openpyxl` significa que a planilha não sai: instalar (skill `configurar`) ou
gerar sem `planilha` em `--formatos`, dizendo isso ao usuário.

**Passo 2 — Montar o payload.** Seguir `referencia/payload-schema.md`. Todo número sai do
motor. Nenhum valor é digitado à mão no JSON. Campo sem origem documental vira `lacunas`.

**Passo 3 — Preencher os três campos que a v3 não tinha.**

`conferencia.veredito` sai de `conferir_saldo()`. Se o saldo confere, o laudo diz isso em
destaque — é o que sustenta a credibilidade do resto.

`ressalvas` recebe **todo achado que favorece o banco**. Isso não é opcional: laudo que só
acusa é peça de parte, e o assistente técnico do outro lado encontra o ponto sozinho.

`lacunas` recebe cada documento ausente que impediria conclusão definitiva. Os achados que
dependem dele são classificados `A verificar`, jamais `Ilícito`.

**Passo 3-b — A agenda de pesquisa NÃO entra no laudo.**

`agenda_jusia` continua no payload, mas sai em arquivo apartado — `INTERNO-agenda-pesquisa-*.md`
— com aviso de não juntar aos autos. Laudo pericial destina-se ao processo: expor nele o roteiro
de pesquisa entrega a estratégia à parte contrária e, pior, admite por escrito que as teses estão
sem lastro. O laudo apenas sinaliza quais achados ficaram pendentes de verificação, sem dizer o
que será pesquisado a respeito deles. Ao entregar, **nunca** apresentar o arquivo da agenda junto
com o laudo sem alertar que ele é interno.

**Passo 3-c — Formatação numérica.**

Percentuais e fatores em padrão brasileiro: vírgula decimal, ponto de milhar. F-string com
`:.2f` produz ponto e vaza para o PDF. Usar o helper `pt()` ao montar o payload e conferir com
`grep -E '[0-9]\.[0-9]'` no JSON antes de renderizar — separador de milhar é ponto e não deve
ser confundido com decimal.

**Passo 4 — Renderizar.**

```bash
<rb> gerar payload.json --saida <diretório de saída da sessão> \
    --formatos premium,planilha --config-dir "${CLAUDE_PLUGIN_DATA}"
```

O diretório de saída é o que a sessão usa para entregar arquivos ao usuário (varia por
ambiente: pasta do caso no Claude Code, pasta de saída no Cowork/claude.ai); o payload fica
fora do repositório do plugin. `marca` e `assinatura` ausentes do payload são preenchidas a
partir do operador gravado na L-1. `validar_detalhado()` roda antes de qualquer escrita — erro
interrompe, aviso vai ao stderr e deve ser lido.

**Passo 5 — Validar a paginação antes de entregar.** Renderizar em PDF e conferir que
nenhuma página transborda e que não há folha meio vazia por bloco indivisível que não coube.
Sobra de setenta a cem pixels ao pé da folha é a margem normal; acima de cento e trinta
indica bloco que não coube e migrou inteiro. Só então entregar os arquivos ao usuário.

## Gate pós-entrega

- "Encerrar a análise"
- "Analisar outro contrato"
- "Montar o roteiro estratégico de ajuizamento" → estrutura os tópicos da fundamentação a
  partir dos achados, gradua as teses por tier e entrega os prompts calibrados de pesquisa
  para a skill `pesquisa-jurisprudencial-jusia` antes da redação
- "Gerar a petição com base nesta análise" → briefing estruturado para a skill de
  peticionamento gravada na L-1 (`skill_peticao` do operador). Sem skill configurada, entregar
  o briefing em markdown

## Erros que esta camada existe para não repetir

**Dois números para a mesma grandeza.** Fixar a convenção de contagem ANTES do primeiro
cálculo e registrá-la em `metodologia`. Apurar duas vezes com convenções diferentes produz
divergência de dezenas de reais e entrega munição ao contraditório. Em série diária, a
armadilha específica é `dias_uteis()` (semiaberta) versus `dias_uteis_fechado()`: use
`auditar_fator_declarado()`, que resolve as duas e declara qual adotou.

**Empurrar N instrumentos num payload.** Ver o topo desta camada. É o erro mais caro que esta
skill já cometeu, porque o documento sai plausível e o defeito só aparece na leitura atenta.

**Prompt de pesquisa dentro do laudo.** Ver o passo 3-b.

**Critério que maximiza o excesso.** Havendo duas leituras defensáveis, adotar a de menor
excesso e declarar a descartada na metodologia. Impugnação que escolhe sistematicamente a
leitura mais favorável ao credor e ainda assim encontra erro é muito mais difícil de rebater
do que a que infla números.

**Narrar escrita que não aconteceu.** Conferir o resultado de cada gravação antes de afirmar
que o arquivo foi gerado ou atualizado.

**Forçar o caso no molde do template.** Se o payload não descreve o caso, o problema é o
payload ou o schema — nunca inventar seção fora do chassi nem reescrever o CSS.
