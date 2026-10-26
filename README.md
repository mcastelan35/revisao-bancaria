# Revisão bancária — Claude para Advogados

Plugin desenvolvido por **Marcos Vilas Boas** — [fale comigo](https://www.instagram.com/advvilasboas/) (Instagram @advvilasboas).

Análise revisional de contratos bancários no Claude, para advogados e contadores, em dupla com o
conector **Radar Apogeu**, que entrega as taxas e os índices oficiais do BACEN:

- **Contratos** — financiamento, consignado, capital de giro, cédulas e leasing: 40 regras
  jurídicas aplicadas por motor determinístico, Price/SAC, pós-fixados (CDI, Selic, TR, IPCA) com
  reconstrução dia útil a dia útil e auditoria do CET, auditoria da memória de cálculo do credor.
- **Cartão de crédito** — faturas, teto de 100% da Lei 14.690/2023, bola de neve da dívida.
- **Financiamento habitacional e imobiliário (SFH/SFI)** — saldo indexado, amortização negativa,
  capitalização vedada e checklist da consolidação da propriedade e dos leilões.
- **Conta corrente, cheque especial e conta garantida** — saldo diário, método hamburguês,
  imputação do art. 354 do CC, três cenários de recomposição e encontro de contas.

Cada camada termina num **gate**: nada avança sem a sua aprovação. A taxa contratada é sempre
comparada com a **média BACEN** da mesma espécie (limiares de 1,5x e 2,0x, com o alerta do Tema
1378/STJ), nenhum número nasce fora dos motores de cálculo e nenhum dado é presumido — o que falta
vira lacuna declarada. A entrega é um **laudo PREMIUM** (pericial, A4), uma **panorâmica** de duas
a três páginas para o cliente e uma **planilha** com toda a memória de cálculo.

## Instalação

No Claude Code (aba **Code** do app Claude, terminal ou IDE):

```
/plugin marketplace add mcastelan35/revisao-bancaria
/plugin install revisao-bancaria@revisao-bancaria
```

No claude.ai, envie o arquivo `revisao-bancaria-<versão>.plugin` (seção **Releases** do GitHub, ou
gerado com `python ferramentas/empacotar_plugin.py`) em **Personalizar › Plugins**.

### Pré-requisito: o conector Radar Apogeu

O plugin trabalha **sempre** com o conector: ele é a fonte única das taxas médias por modalidade,
das séries de indexador e da correção do indébito, servidas de um cache persistente que torna o
laudo reproduzível por terceiro. Sem ele, a revisão não roda.

1. Adicione o conector **Radar Apogeu** em **Configurações › Conectores**.
2. Configure a chave de acesso **no próprio conector** — nunca cole a chave no chat. A chave é
   pessoal e acompanha a assinatura.
3. Abra uma conversa nova.

### Primeiro uso

Diga **"configura a revisão bancária"** (ou rode `/revisao-bancaria:configurar`). O Claude confere
o Python, roda o autoteste dos motores, pergunta quem assina os laudos — advogado com OAB ou
contador com CRC — e confirma o conector com uma chamada.

## Uso

| Você diz ou envia | O que acontece |
|---|---|
| "a taxa de 3,2% ao mês do consignado INSS de março de 2023 é abusiva?" | **triagem**: uma consulta ao conector, razão contra a média, limiares e próximo passo |
| contrato, CCB, cédula ou proposta | revisão do **instrumento** (L0 a L4) |
| extratos de conta corrente | revisão da **conta** (C0 a C6) |
| faturas do cartão | ramo **cartão** |
| contrato habitacional, consolidação ou leilão | ramo **SFH/SFI** |
| memória de cálculo de uma execução | auditoria da **memória do credor** antes de recalcular |
| "gera o laudo" ao fim da análise | PREMIUM, PANORAMA e planilha, em nome do operador configurado |

As três skills do plugin: `revisao-bancaria` (a análise completa), `triagem` (pergunta pontual de
taxa, sem documento) e `configurar` (operador, ambiente e conector).

## Linha de comando

Os motores ficam em `skills/revisao-bancaria/motores/` (Python 3.10+, só biblioteca padrão; a
planilha usa `openpyxl`). O Claude os chama pela linha de comando, que também serve para conferir
à mão:

```bash
python skills/revisao-bancaria/revisao.py autoteste
python skills/revisao-bancaria/revisao.py regras --tipo consumo_pf --regime consumerista --data-contrato 2022-05-10 --formato resumo
python skills/revisao-bancaria/revisao.py razao --contratada-pct 3.2 --media-pct 1.75
python skills/revisao-bancaria/revisao.py serie --buscar "cheque especial"
```

Subcomandos: `autoteste`, `regras`, `regra`, `sumula`, `marcos`, `serie`, `razao`, `comparar`,
`gerar` e `operador` — detalhes em [ARCHITECTURE.md](ARCHITECTURE.md).

## Testes e manutenção

```bash
uv run --no-project --python 3.12 --with pytest --with openpyxl pytest   # suíte completa
python ferramentas/verificar_consistencia.py                             # documentos × JSON × motores × manifestos
python ferramentas/empacotar_plugin.py                                   # dist/revisao-bancaria-<versão>.plugin
```

O GitHub Actions roda a suíte a cada envio, no Windows e no Linux. A versão é uma só — manifestos,
`SKILL.md`, `regras-bancarias.json`, `motores/__init__.py`, CHANGELOG e ARCHITECTURE — e a
consistência falha se divergirem. Quem já instalou só recebe código novo quando a versão sobe.

## Privacidade e limites

- Contratos, extratos e faturas são lidos na sua sessão do Claude e não entram neste repositório
  (o `.gitignore` bloqueia PDFs, planilhas, HTML e payloads). Ao conector vão apenas códigos de
  série, datas e, na correção do indébito, valores e datas de pagamento — nunca nome, CPF ou o
  documento.
- A identidade de quem assina fica na pasta de dados do plugin, fora do código, e nunca vem
  pré-preenchida.
- A razão contratada/média é aritmética; a tese de juros abusivos depende do Tema 1378/STJ,
  pendente. Regras suspensas ou sem precedente consolidado não concluem: a decisão é do advogado.
- Jurisprudência só do acervo do plugin, com ementa integral; o que não estiver lá vai para
  pesquisa (JusIA). A rota CONTA é **beta** enquanto o repertório jurisprudencial dela estiver em
  esqueleto.
- Os valores da rota CONTA são faixa, não ponto, e instruem a perícia contábil.
- Todo entregável é sujeito a revisão por advogado(a) ou contador(a) responsável.

---

Desenvolvido por **Marcos Vilas Boas** — Claude para Advogados. Dúvidas, sugestões e contato:
[instagram.com/advvilasboas](https://www.instagram.com/advvilasboas/).
