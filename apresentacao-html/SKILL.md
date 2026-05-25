---
name: apresentacao-html
description: monta uma apresentação em html com base em textos na mesma pasta
disable-model-invocation: true

## Ambiente Python

- Windows, Python via `python` (não `python3`)
- NUNCA crie virtualenvs ou ambientes temporários — use sempre o Python do sistema
- Se uma biblioteca não estiver instalada, instale com `pip install <lib>` globalmente no sistema
- Sempre usar `encoding="utf-8"` ao abrir/escrever arquivos
- Sempre incluir `PYTHONUTF8=1` ao rodar scripts Python via bash:
  `PYTHONUTF8=1 python script.py`
  ou definir no próprio script: `import os; os.environ["PYTHONUTF8"] = "1"`
- Preferir escrever scripts em arquivo `.py` temporário em vez de heredoc inline

## Preferências gerais

- Economize tokens: sem verbose desnecessário
- Manipulação de arquivos .docx, .xlsx, .pdf: use as libs já instaladas no sistema


---

## 1. ANALISAR

Leia todos os arquivos da pasta que ".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".html", ".md"

Você é um especialista em storytelling, design de apresentações e desenvolvimento front-end.
Quero que você analise todo o conteúdo e transforme em uma apresentação em HTML + CSS + JavaScript completa, com uma única página (arquivo Apresentacao.html).


**Regras gerais:**
- Traduza tudo para português se a transcrição estiver em inglês
- entenda o problema central e busque mais bibliografia



## Estrutura da apresentação:
- Slide 1 (Capa/Título)
-- Título principal: uma frase impactante que representa o problema central.
-- Subtítulo: explicação curta e clara.
-- Pequeno texto de contexto.

- Slide 2 (Sumário)
-- Liste os capítulos/principais seções que serão abordados, com links clicáveis que levem diretamente para o slide correspondente.

- Slides seguintes (slides de conteúdo)
-- Divida o conteúdo dos textos em slides lógicos, seguindo uma narrativa de storytelling fluida e envolvente (defina a melhor abordagem de storytelling para este tema e justifique brevemente).



## Estilo visual e UX dos slides de conteúdo:
- Design clean, profissional e moderno.
- Agrupe slides de um mesmo assunto em sequencia, somente o primeiro slide do assunto aparece no sumário
- Títulos grandes e impactantes.
- Textos curtos e bem hierarquizados.
- Mantenha o código limpo, bem comentado e fácil de editar.
- insira comentários no HTML para fácil edição
- Boas práticas de UX: hierarquia clara de tipografia, tamanhos de título e texto confortáveis para leitura em tela cheia, bom espaçamento, responsividade básica.


## Entrega:
- leia na mesma pasta do arquivo SKILL.md o arquivo chamado `Base_Apresentacao.html`
-- o arquivo `Base_Apresentacao.html` contem a estrutura da apresentação que deverá sem montada
-- observe os comentários que iniciam com `<!--COMANDO:` eles contém o que deve ser alterado 
- Salve `Apresentacao.html` na pasta que contem os textos que alimentaram o conteúdo

Analise primeiro o conteúdo dos arquivos da pasta e depois gere a apresentação seguindo todos esses critérios.

- gere um arquivo texto (postagem.txt) na mesma pasta onde irá salvar o `Apresetacao.html` com:
-- texto de até 500 caracteres para uma postagem no linkedin
-- mostre dados concretos, busque referências e destacando essas referências
-- não insira links externos
-- Texto dissertativo-argumentativo sutil
-- Linguagem: humanizada, informal, simples e conversada.
-- Separe os parágrafos com duplo espaço.
-- Insira exatamente uma vez "..." para dar sensação de continuidade natural.
-- Inclua 2 a 4 pequenos erros de grafia ou pontuação para soar humano (ex: faltar acento, vírgula errada, “realmente” sem acento, “gostariamos”, etc.).
-- Nunca use: listas, travessão (—), dois pontos (:) explicativos, “eu acho”, “na minha opinião”, "pessoal", "amigos", "gente", etc.
-- Escreva de forma direta, limpa e natural, como se fosse um texto humano fluido. Evite construções passivas formais como 'Identifica-se que', 'Percebe-se que', 'Observa-se que', 'Nota-se que'. Comece as frases direto no assunto, use menos verbos introdutórios e torne o texto mais conciso e conversacional, sem perder o tom profissional.





**Gerar apenas:** `Apresetacao.html` e `postagem.txt` — nenhum outro arquivo.