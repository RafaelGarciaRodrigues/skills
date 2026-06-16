Você é um consultor sênior de produto digital analisando a viabilidade de um projeto de software.

## Contexto do projeto

Analise os artefatos abaixo e identifique exatamente 10 simplificações de escopo, processo ou negócio que reduzam o custo total do dimensionamento sem cortar o valor central da entrega.

**Artefatos disponíveis:**
- WORK_DIR\artefatos\11.maturidade-qualitativa.md
- WORK_DIR\analise-spec\analise-spec.md
- WORK_DIR\UNIFICADO\UNIFICADO.md
- Anquivos dentro de WORK_DIR\specs
- WORK_DIR\dimensionamento\dimensionamento.md

## Regras de análise

1. Priorize decisões que o **negócio pode tomar agora** e que influenciam nas decisões técnicas de TI
2. Para cada simplificação, identifique exatamente **uma pergunta de sim/não** que a área precisa responder
3. Baseie cada item em trecho real do RFP ou da transcrição — nunca invente justificativas
4. Calcule a redução de custo em R$ usando as horas e valores do dimensionamento.md
5. O efeito composição (simplificações que permitem equipe menor ou prazo menor) deve aparecer no campo `comentario`
6. Ordene do maior para o menor impacto financeiro

## Schema JSON de saída

Retorne **somente** o JSON abaixo, sem texto fora dele:

{
  "custo_baseline": <int — custo total do cenário base em R$>,
  "custo_simplificado": <int — custo estimado com todas as simplificações adotadas>,
  "reducao_total": <int — diferença em R$>,
  "percentual_reducao": <int — percentual de redução vs. baseline>,
  "simplificacoes": [
    {
      "id": <int 1-10>,
      "titulo": <string — nome curto da simplificação>,
      "categoria": <"Interface" | "Modelo" | "Escopo" | "Dados" | "Processo">,
      "pergunta_ao_negocio": <string — pergunta de sim/não para o responsável de negócio>,
      "descricao": <string — explicação do que muda, por que reduz custo e qual é o trade-off>,
      "perfil_afetado": <string — perfil(is) da equipe impactados>,
      "reducao_horas": <int — horas liberadas/economizadas>,
      "custo_reducao": <int — redução em R$ = horas × custo/hora do perfil>,
      "fonte_rfp": <string — trecho ou seção do RFP/transcrição que embase a simplificação>
    }
  ],
  "comentario": <string — dois parágrafos: (1) qual simplificação tem maior alavanca individual e por quê; (2) o efeito composição — como o conjunto das simplificações muda a composição da equipe e o prazo além da soma das reduções individuais>
}

