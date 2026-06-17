
Analise criticamente a specification (spec.md) e os artefatos.
Atue como arquiteto cético, mas não descreva algo como: "Essa análise foi feita como um arquiteto cético olhando para a especificação".
Tente quebrar a specification, sem citar que está tentando fazer isso.

Faça perguntas objetivas para convergir a arquitetura.

- Linguagem: humanizada, informal, simples e conversada.

---

# Formato de saída

Responda APENAS com o JSON abaixo, sem texto antes ou depois,
sem blocos de código markdown:

{
  "analise-spec": [
    {
      "categoria": "Ambiguidades",
      "itens": [
        {
          "titulo": "frase curta identificando a ambiguidade",
          "descricao": "explicação detalhada + pergunta objetiva de convergência"
        }
      ]
    },
    {
      "categoria": "Inconsistências",
      "itens": [...]
    },
    {
      "categoria": "Requisitos Conflitantes",
      "itens": [...]
    },
    {
      "categoria": "Edge Cases",
      "itens": [...]
    },
    {
      "categoria": "Riscos Técnicos",
      "itens": [...]
    },
    {
      "categoria": "Gargalos",
      "itens": [...]
    },
    {
      "categoria": "Decisões Faltantes",
      "itens": [...]
    },
    {
      "categoria": "Necessidade de Esclarecimentos",
      "itens": [...]
    },
    {
      "categoria": "Questionamento de Premissas Implícitas",
      "itens": [...]
    },
    {
      "categoria": "Decisões Irreversíveis de Arquitetura",
      "itens": [...]
    },
    {
      "categoria": "Riscos de Cybersegurança",
      "itens": [...]
    }
  ]
}

Regras do JSON:
- Aspas internas escapadas com \"
- Sem quebras de linha dentro de strings
- Inclua apenas categorias que tiverem ao menos 1 item
- Mínimo de 2 itens por categoria incluída
- "titulo" deve ser uma frase curta (máximo 10 palavras)
- "descricao" deve conter a explicação + ao menos uma pergunta objetiva

Não implemente ainda.
