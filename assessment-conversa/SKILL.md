---
name: assessment-conversa
description: cria json de transcrição e monta html via base.html
disable-model-invocation: true
---

## 1. GERAR resumo.json

Leia todos os arquivos da pasta que iniciem com `TRANSC` e gere `resumo.json` com a estrutura abaixo.

**Regras gerais:**
- Traduza tudo para português se a transcrição estiver em inglês
- Gere o JSON completo, sem interrupções
- Preencha todos os campos conforme as instruções
```json
{
  "titulo": "Frase curta que resume o contexto da conversa",
  "quando": "Data/hora criação — fuso America/Sao_Paulo",
  "problema_central": "Uma frase descrevendo o problema central",
  "resumo": "350 palavras. Impessoal, como narrativa. Parágrafos separados com <p> por assunto. Sem repetição no final. Trata todos os temas com riqueza de detalhes.",
  "necessidades": [
    {
      "necessidade": "Frase curta — mín. 7 itens. Só causas raízes de problemas reais. Não começa com verbo de ação. Não inclui requisitos/pedidos.",
      "desc_necessidade": "Explicação detalhada, com citações se necessário."
    }
  ],
  "requisitos_tecnicos": [
    {
      "requisito": "Frase curta — mín. 7 itens. Apenas pedidos, requisitos, ações ou soluções solicitadas. Não inclui problemas ou dificuldades.",
      "desc_requisito": "Explicação detalhada do requisito."
    }
  ],
  "insights": [
    "Ideias acionáveis não discutidas na conversa. Analista de estratégia: direto, sem elogio, sem coaching. Curtas, com porquê mínimo. Aponte riscos se houver. Nada genérico sem um 'como'."
  ],
  "sentimentos": {
    "confiança": 0,
    "entusiasmo": 0,
    "colaboração": 0,
    "satisfação": 0
  },
  "bibliografia": ["Livro/artigo/autor relevante ao tema — sem resumos longos"],
  "markdown": "Mapa mental em Markdown. Inicia com macro tema > problemas > causas raiz / soluções (responsável + data se houver) / insights / números. Hierárquico, máximo detalhe, sem resumir, sem inventar, sem introdução/conclusão. Sem ``` no início/fim.",
  "timeline": {
    "parte1": "Tema principal do 1º quinto da conversa",
    "parte2": "Tema principal do 2º quinto",
    "parte3": "Tema principal do 3º quinto",
    "parte4": "Tema principal do 4º quinto",
    "parte5": "Tema principal do 5º quinto"
  },
  "reuniao_em_numeros": ["Valor numérico + frase explicativa — liste todos os números da transcrição"],
  "perguntas_sem_respostas": ["Questões levantadas sem definição clara — pode ser pequeno texto contextualizando"],
  "contradicoes": [
    {
      "trechos": ["trecho A", "trecho B"],
      "explicacao": "Explicação da contradição"
    }
  ],
  "fluxo-processo": "Pseudocódigo code2flow: texto; → nó | if(cond?){} → decisão | else{} → alternativo | while(cond?){} → loop | // → comentário",
  "nomeParticipantes": [
    {
      "participante": "Nome ou identificação",
      "responsabilidade": "Função/responsabilidade identificada na transcrição"
    }
  ]
}
```

---

## 2. GERAR Assessment.html

1. Leia `base.html` e salve cópia como `Assessment.html` na mesma pasta
2. Substitua `##INSIRA_CONTEUDO_JSON##` pelo conteúdo textual de `resumo.json`
3. Substitua `###PSEUDOCODIGO_FLUXO_PROCESSO###` pelo campo `fluxo-processo` do JSON
   - Quebre linhas reais no arquivo (sem `\n` literal)
4. Salve `Assessment.html`

**Gerar apenas:** `resumo.json` e `Assessment.html` — nenhum outro arquivo.