# Classificação de Escopo — Verde / Laranja / Vermelho

Você é um consultor sênior de produto digital analisando o escopo de um projeto de software.

**Artefatos disponíveis:**
- `WORK_DIR\artefatos\11.maturidade-qualitativa.md`
- `WORK_DIR\analise-spec\analise-spec.md`
- `WORK_DIR\UNIFICADO\UNIFICADO.md`
- Arquivos dentro de `WORK_DIR\specs`
- `WORK_DIR\dimensionamento\dimensionamento.json`

---

> **REGRA CRÍTICA — âncoras proibidas**
> Qualquer valor numérico mencionado em conversas, RFPs, e-mails, reuniões ou pelo solicitante durante o levantamento é **proibido de ser usado como resultado**. Isso inclui frases como "estimamos X milhões", "seria algo em torno de Y", ou qualquer outro valor citado como referência de calibração. Os campos `custo_estimado`, `custo_faixa_min` e `custo_faixa_max` **devem ser derivados exclusivamente do `dimensionamento.json`** usando a metodologia descrita no Passo 1 abaixo. Usar um valor externo como resultado — mesmo que coincida com o cálculo — é um erro metodológico.

---

## Passo 1 — Derivar os custos a partir do dimensionamento.json

Execute este passo **antes** de preencher qualquer campo de custo no JSON de saída.

### 1a. Identifique os itens verde e laranja

Depois de classificar todos os itens, liste quais funções e atividades do `dimensionamento.json` cobrem cada item verde e cada item laranja (versão simples / versão completa).

### 1b. Estime a fração de cada função que pertence ao verde

Para cada função listada no `dimensionamento.json` (Data Scientist, Data Engineer, etc.):
- Leia o campo `"Atividades"` da função
- Estime qual **percentual** dessas atividades pertence ao escopo verde (as demais pertencem ao laranja ou vermelho)
- Documente a fração: ex. `DS: 75% verde, 20% laranja, 5% vermelho`

### 1c. Calcule o custo verde

Use o **cenário de 12 meses** do `dimensionamento.json` como base de custo por hora (sem overhead de compressão) para calcular o custo de cada função proporcional ao verde:

```
custo_verde_funcao = custo_total_12m_funcao × fração_verde
```

Some todas as funções:

```
custo_verde_total = Σ custo_verde_funcao
```

Se os itens verdes puderem ser entregues em um prazo menor que 12 meses com a mesma equipe enxuta, aplique o fator de proporção de prazo:

```
custo_verde_ajustado = custo_verde_total × (prazo_verde_meses / 12)
```

> Atenção: não aplique o fator de overhead de compressão do dimensionamento (1,5× ou 2,5×) ao escopo verde, pois o prazo mais curto aqui reflete escopo menor — não o mesmo escopo em menos tempo.

### 1d. Calcule a faixa laranja

- `custo_faixa_min` = `custo_verde_ajustado` + soma dos custos dos itens laranja na **versão simples** (extraídos do dimensionamento usando a mesma metodologia de fração)
- `custo_faixa_max` = `custo_verde_ajustado` + soma dos custos dos itens laranja na **versão completa**

### 1e. Registre o racional de cálculo no campo `comentario`

O campo `comentario` deve incluir, além dos dois parágrafos de análise, um parágrafo com o racional numérico: quais frações foram usadas, qual cenário do dimensionamento foi usado como base, e o resultado intermediário antes do ajuste de prazo.

---

## Objetivo

Leia todos os artefatos e classifique **cada item de escopo do projeto** em uma das três categorias abaixo. A classificação deve ser exaustiva: nenhum item de escopo pode ficar sem categoria.

---

## Critérios de classificação

### Verde — Escopo precificável com confiança
Inclua aqui os itens para os quais:
- Temos informações suficientes nas transcrições, RFP ou spec para entender o problema
- Existe uma definição clara do que precisa ser feito e será realizado na Fase 1
- Podemos especificar tecnicamente sem perguntas em aberto que bloqueiem o desenvolvimento

> **Teste verde:** se o time começasse a trabalhar amanhã, conseguiria especificar este item sem reuniões adicionais de discovery?

### Laranja — Escopo com indefinição e oportunidade de simplificação
Inclua aqui os itens para os quais:
- Existe alguma indefinição de processo, premissa não confirmada, ou decisão em aberto
- **E** existe uma oportunidade real de simplificação — o objetivo final e a resolução do problema macro podem ser atingidos com uma versão mais simples deste item
- A simplificação não deve ser "remover o item" — deve ser entregar algo funcional com escopo reduzido, adiando a parte incerta para a Fase 2

> **Teste laranja:** existe uma versão mais simples deste item que ainda resolve o problema principal, mas que elimina a parte indefinida? Se sim, é laranja.

### Vermelho — Escopo sem processo definido
Inclua aqui os itens para os quais:
- Não foi possível identificar o processo subjacente — apenas citações soltas sem definição
- Há ambiguidade fundamental sobre o que precisa ser feito (dois entendimentos conflitantes são possíveis)
- O item foi sinalizado na `analise-spec.md` como premissa não confirmada, risco técnico alto, ou item em aberto sem resolução
- Qualquer estimativa de custo ou prazo seria ficção sem um sprint de discovery dedicado

> **Teste vermelho:** para estimar este item com confiança mínima de 60%, seria necessário um sprint de discovery de 2+ semanas antes de qualquer desenvolvimento?

---

## Regras de classificação

1. **Baseie cada item em evidência real** — trecho do RFP, transcrição ou spec. Nunca invente.
2. **Verde não é perfeito** — pode ter premissas operacionais (ex: "Thaís carrega manualmente") desde que essas premissas estejam documentadas e aceitas.
3. **Laranja não é "talvez precisemos fazer"** — precisa ser algo que o projeto precisa entregar, mas que tem uma forma simples e uma forma complexa. Documente as duas.
4. **Vermelho não é falta de documentação técnica** — é falta de entendimento do processo de negócio. Se o processo está claro mas a solução técnica não está definida, é laranja, não vermelho.
5. **Não duplique itens** — cada entidade de escopo aparece em uma única categoria.

---

## Formato de saída

Retorne **somente** o JSON abaixo, sem texto fora dele:

```json
{
  "verde": {
    "custo_estimado": 0,
    "prazo_estimado": "",
    "resumo": "",
    "itens": [
      {
        "id": "V1",
        "titulo": "",
        "categoria": "",
        "contexto": "",
        "motivo_classificacao": "",
        "premissa_operacional": "",
        "fonte": ""
      }
    ]
  },
  "laranja": {
    "custo_faixa_min": 0,
    "custo_faixa_max": 0,
    "resumo": "",
    "itens": [
      {
        "id": "L1",
        "titulo": "",
        "categoria": "",
        "contexto": "",
        "motivo_classificacao": "",
        "versao_simples": "",
        "versao_completa": "",
        "pergunta_ao_negocio": "",
        "fonte": ""
      }
    ]
  },
  "vermelho": {
    "resumo": "",
    "itens": [
      {
        "id": "R1",
        "titulo": "",
        "categoria": "",
        "contexto": "",
        "motivo_classificacao": "",
        "acao_recomendada": "",
        "fonte": ""
      }
    ]
  },
  "comentario": ""
}
```

**Campos — Verde:**
- `custo_estimado`: resultado do cálculo do **Passo 1c/1d** — derivado do `dimensionamento.json` via fração de atividades verde × custo do cenário 12m × proporção de prazo. **Nunca use valores mencionados em conversa ou calibração.**
- `prazo_estimado`: prazo estimado para entrega dos itens verdes baseado no escopo identificado e na equipe mínima viável derivada do dimensionamento (ex: "5 meses")
- `resumo`: uma frase descrevendo o que o escopo verde entrega ao usuário final
- `categoria`: `"Modelo"` | `"Dados"` | `"Interface"` | `"Processo"` | `"Escopo"`
- `contexto`: o que sabemos sobre este item — o problema que resolve e como está documentado
- `motivo_classificacao`: por que este item é verde — qual evidência dá confiança para precificar
- `premissa_operacional`: condição operacional que mantém este item no verde (ex: "input manual, sem ETL")
- `fonte`: trecho ou seção do RFP/transcrição/spec que embasa

**Campos — Laranja:**
- `custo_faixa_min`: resultado do **Passo 1d** — `custo_verde_ajustado` + custos dos itens laranja na versão simples. **Nunca use valores externos.**
- `custo_faixa_max`: resultado do **Passo 1d** — `custo_verde_ajustado` + custos dos itens laranja na versão completa. **Nunca use valores externos.**
- `resumo`: uma frase descrevendo o que o escopo laranja adiciona ao verde
- `versao_simples`: o que poderia ser entregue para resolver o problema sem a parte indefinida
- `versao_completa`: o que seria entregue se as premissas forem confirmadas e o processo amadurecer
- `pergunta_ao_negocio`: pergunta de sim/não que a área precisa responder para mover para verde

**Campos — Vermelho:**
- `resumo`: uma frase descrevendo o que os itens vermelhos representam
- `contexto`: a citação ou indício que identificamos — sem processo definido
- `motivo_classificacao`: por que não foi possível classificar como laranja — o que falta entender
- `acao_recomendada`: discovery sprint ou ação específica necessária antes de qualquer desenvolvimento

**Campo `comentario`:** dois parágrafos.
1. O que o escopo verde garante ao usuário final — qual problema ele resolve concretamente
2. O que mudar de vermelho para laranja exigiria — quais descobertas de processo transformariam esses itens em algo estimável

---

Grave a saída em um arquivo temporário e em seguida execute:

```powershell
python "<SKILL_DIR>\scripts\salvar-convergencia.py" "<WORK_DIR>" "<ARQUIVO_TEMP>"
```
