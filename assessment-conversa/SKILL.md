---
name: assessment-conversa
description: cria json de transcrição e monta html via base.html
disable-model-invocation: true


## Ambiente Python

- Windows: usar `python` (nunca `python3`)
- Nunca criar virtualenv, venv, conda env ou ambientes temporários
- Sempre usar o Python global do sistema
- Bibliotecas ausentes:
  `pip install <lib>`
- Sempre usar UTF-8:
  - `encoding="utf-8"`
  - `PYTHONUTF8=1`
- Preferir scripts `.py` reutilizáveis
- Evitar `python -c` multiline
- Evitar heredoc inline
- Não embutir lógica Python no shell

## Shell / PowerShell

- Sempre usar PowerShell no Windows
- Nunca executar comandos PowerShell dentro do Bash
- Evitar:
  - `bash -lc`
  - pipelines complexos
  - subexpressions `$(...)`
  - `foreach` inline
  - comandos multiline longos
  - comandos acima de ~800 caracteres
- Preferir:
  - scripts `.py`
  - scripts `.ps1`
  - variáveis explícitas
  - comandos curtos
  - lógica fora do shell

## Automação

- Preferir Python para automações
- Não reimplementar lógica inline no terminal
- Reutilizar scripts existentes sempre que possível
- Qualquer lógica complexa deve ir para arquivo reutilizável

## Arquivos Office

- Nunca usar:
  - python -c multiline
  - COM objects
  - `Word.Application`
  - automação Office via PowerShell
- Para `.docx`, `.xlsx`, `.pdf`:
  - usar bibliotecas Python instaladas no sistema
  - Não usar Python inline para manipulação de filesystem.

- Sempre criar:
  - script reutilizável em scripts/

## Extração DOCX

Usar sempre:

`python scripts/extract_docx.py [arquivo.docx] [saida.txt]`


Nunca implementar extração DOCX inline.




## Arquitetura de Diretórios (LEIA PRIMEIRO)

Esta skill opera com DOIS diretórios distintos. Não confunda:

- `SKILL_DIR` = pasta onde este `SKILL.md` reside.
  Contém os artefatos da skill (não modificar, não copiar):
  - `SKILL.md`
  - `base.html`           (template HTML)
  - `scripts/extract_docx.py`
  - `scripts/gerar_assessment.py`

- `WORK_DIR` = pasta de trabalho do usuário (cwd atual, ou a pasta que
  o usuário indicar explicitamente). Contém:
  - INPUTS: arquivos de transcrição (.txt, .docx, .pdf, .md, .json, .html, .xlsx, .pptx, .doc, .ppt, .xls)
  - OUTPUTS gerados: `resumo.json` e `Assessment.html`

### Regras invariantes

1. NUNCA leia inputs de `SKILL_DIR`. Inputs vêm de `WORK_DIR`.
2. NUNCA grave outputs em `SKILL_DIR`. Outputs vão para `WORK_DIR`.
3. NUNCA copie scripts ou `base.html` para `WORK_DIR`. Eles ficam em `SKILL_DIR`.
4. Sempre invoque os scripts passando caminhos ABSOLUTOS, prefixando:
   - scripts: `<SKILL_DIR>\scripts\<script>.py`
   - template: `<SKILL_DIR>\base.html`
   - inputs/outputs: `<WORK_DIR>\<arquivo>`
5. `SKILL_DIR` é o caminho absoluto da pasta onde você (IA) leu este
   `SKILL.md`. Resolva-o no momento da execução; não hardcode.
6. `WORK_DIR` é o cwd do shell atual (ou a pasta passada pelo usuário).
   Em PowerShell: `$PWD.Path`. Não assuma um caminho fixo.

### Exemplos de invocação correta (PowerShell, Windows)

Extrair DOCX:
    python "<SKILL_DIR>\scripts\extract_docx.py" "<WORK_DIR>\entrada.docx" "<WORK_DIR>\entrada.txt"


Sempre envolva os caminhos em aspas duplas (há computadores com espaços
e acentos no caminho do usuário, ex.: `OneDrive - Empresa`).



## Execução de Scripts

- Antes de criar lógica nova, procurar scripts existentes na pasta `scripts\`
- Se existir script compatível, reutilizar o script existente
- Não reimplementar lógica inline no shell
- Não usar `python -c` para lógica já existente em script

## Caminhos e Referências

- Scripts devem usar caminhos locais e relativos
- Nunca usar caminhos absolutos hardcoded
- Sempre resolver caminhos relativos ao:
  - diretório atual
  - ou ao próprio script (`__file__`)

Preferir:

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

---






## 1. GERAR resumo.json

- Leia todos os arquivos da pasta com as extensões: "*.txt", "*.doc", "*.docx", "*.xls", "*.xlsx", "*.pdf", "*.ppt", "*.pptx", "*.md", "*.json", "*.html",   
- crie um arqivo chamado `resumo.json` baseado nos arquivos lidos na pasta com a estrutura descrita abaixo.


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

Use o script:

scripts/gerar_assessment.py

Responsabilidades:
- Ler base.html
- Ler resumo.json
- Inserir JSON no placeholder:
  {##INSIRA_CONTEUDO_JSON##}
- Inserir fluxo-processo no placeholder:
  ###PSEUDOCODIGO_FLUXO_PROCESSO###
- Gerar Assessment.html

Execução:

python scripts/gerar_assessment.py

## Restrições

Nunca usar:
- Word.Application
- COM Objects
- PowerShell gigante inline
- Replace complexo em linha
- JSON multilinha embutido em comando

## Preferências

Preferir:
- Scripts Python
- pathlib
- json.loads
- arquivos temporários
- comandos curtos


**Gerar apenas:** `resumo.json` e `Assessment.html` — nenhum outro arquivo.