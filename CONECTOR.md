# Instruções do conector — Revisão bancária (versão curta)

> Cole isto nas **instruções do Projeto no claude.ai** (ou do conector) quando a
> análise revisional usar a chave do Radar Apogeu **sem o plugin** `revisao-bancaria`.
> É a versão condensada do protocolo `skills/revisao-bancaria/referencia/bacen-consulta.md`;
> com o plugin instalado, a skill já carrega o protocolo completo.

O conector é a **fonte única** das taxas e índices do BACEN nesta análise, e está
sempre ativo. Regras:

1. **Não sonde, use.** Nada de "testar se o conector está disponível". Ele é
   pré-requisito, não acelerador opcional. Chamada de ferramenta consome a quota
   do plano — sondagem, reconfirmação de identidade e reconsulta da mesma série
   gastam quota sem produzir informação.

2. **Código da série: mapeamento ou `listar_series_bacen`.** Com o plugin, o
   código por modalidade sai do mapeamento local (`revisao.py serie`), sem quota,
   e a identidade da série volta na própria resposta de `consultar_taxa_bacen`.
   Sem o plugin, uma `listar_series_bacen` dá o código certo, a **identidade
   autoritativa** (nome, unidade, periodicidade, segmento) e o alcance do **cache
   persistente**. Não confirme identidade por segunda tool nem infira unidade pela
   magnitude do valor.

3. **O cache é o caminho normal.** Competência já materializada responde do
   banco em milissegundos, com valor oficial congelado e datado — é o que torna
   o laudo reproduzível por terceiro. O que falta, e sempre o mês corrente, cai
   no SGS ao vivo. Registre `procedencia` na metodologia do entregável.

4. **Série diária de indexador → `pontos: "completos"`.** No modo padrão o texto
   lista 60 pontos de N e declara a omissão. Se aparecer `OMITIDOS DESTE TEXTO`,
   a série está pela metade e **nenhum produtório sobre ela vale**. Precisa de
   várias séries na mesma janela (modalidade + indexador)? `codigos: [...]` numa
   chamada só — mas `pontos: "completos"` não vale com `codigos`.

5. **Série mensal → `data_inicial` no dia 1º.** O ponto da competência é datado
   no primeiro dia do mês; data posterior o deixa fora da janela.

6. **Confira o fator antes de assinar.** `consultar_taxa_bacen` e
   `consultar_indice` devolvem `fator_acumulado` — cruze com o produtório local
   sobre a **mesma janela fechada**. É o que pega série truncada e calendário
   divergente. Cobertura e ponta de série *não* pegam recorte.

7. **Ponta insuficiente é lacuna bloqueante.** O motor precisa da série até o
   último dia útil ANTES da data-base (o `alcanca_data_final` do conector mede
   contra a data final inclusive — `false` por um dia de publicação D+1 é
   normal). Faltando mais que isso, recue a data-base para o último ponto
   efetivo e declare — nunca repita o último fator nem interpole.

8. **"Nenhum dado encontrado" ≠ falha.** É ausência de publicação na janela. Só
   resposta com erro significa fonte indisponível; aí, uma nova tentativa e,
   persistindo, `web_fetch` como contingência **declarada**.

9. **`bash`/`curl` na `api.bcb.gov.br` é defeito**, em qualquer cenário: ignora o
   cache, dispensa a conferência de fator e produz número não reproduzível.

10. **Correção do indébito → `atualizar_debito`**, que devolve memória linha a
    linha e hash de auditoria. Restituição parcela a parcela: `valores: [{ valor,
    data_inicial, rotulo }]` corrige as N parcelas numa chamada, cada uma da sua
    data-base. O regime é escolha do operador, declarada na metodologia:
    `segmentos` (índice e juros trecho a trecho) ou a regra pronta
    `regra: { tipo: "civil_lei_14905", juros_desde }`. Confira
    `calculo_interrompido` (por valor e no `resumo_geral`): se faltou índice em
    alguma competência, o total não cobre o período pedido.
