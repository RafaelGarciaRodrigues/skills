---
name: consultoria-processos
description: Roteiro completo para criar o entendimento de um problema e quebrá-lo em uma especificação. Use quando houver transcrições, documentos de processo, assessments, consolidação de arquivos ou geração de resumo/especificação.
disable-model-invocation: true
---

# Consultoria de Processos

## Quando Usar

Use esta skill para conduzir análise de processos a partir de arquivos do usuário, consolidar insumos e gerar artefatos como `resumo.json` e `Assessment.html`.

## Ambiente Python

- Windows, Python via `python` (não `python3`)
- NÃO usar `.venv`, `virtualenv`, `conda` ou ambientes temporários
- NUNCA crie virtualenvs ou ambientes temporários; use sempre o Python do sistema
- Se uma biblioteca não estiver instalada, instale com `pip install <lib>` globalmente no sistema
- Sempre usar `encoding="utf-8"` ao abrir/escrever arquivos
- Sempre incluir `PYTHONUTF8=1` ao rodar scripts Python via bash:
  `PYTHONUTF8=1 python script.py`
- Ou definir no próprio script:
  `import os; os.environ["PYTHONUTF8"] = "1"`
- Preferir escrever scripts em arquivo `.py` temporário em vez de heredoc inline

## Preferências Gerais

- Economize tokens: sem verbose desnecessário
- Manipulação de arquivos `.docx`, `.xlsx`, `.pdf`: use as libs já instaladas no sistema
- Se faltar biblioteca: `pip install python-docx PyPDF2 textract`

## Arquitetura de Diretórios

Esta skill opera com DOIS diretórios distintos. Não confunda:

### `SKILL_DIR`

Pasta onde este `SKILL.md` reside. Contém os artefatos da skill, que não devem ser modificados nem copiados:

- `SKILL.md`
- `base.html` (template HTML)
- `scripts/extract_docx.py`
- `scripts/unificar-arquivos.py`
- `scripts/listar-habilidades.py`
- `scripts/salvar-artefato.py`
- `scripts/criar-pasta-json.py`
- `scripts/consolidar-artefatos-json.py`
- `scripts/montar-relatorio-analitico.py`
- `html/relatorio-modelo.html`
- `habilidades/`

### `WORK_DIR`

Pasta de trabalho do usuário, ou seja, o cwd atual ou a pasta indicada explicitamente pelo usuário.

Contém:

- INPUTS: arquivos de transcrição (`.txt`, `.docx`, `.pdf`, `.md`, `.json`, `.html`, `.xlsx`, `.pptx`, `.doc`, `.ppt`, `.xls`)
- OUTPUTS gerados: `resumo.json`, `Assessment.html`, `json\artefatos.json` e `html\Analise.html`

## Regras Invariantes

1. NUNCA leia inputs de `SKILL_DIR`. Inputs vêm de `WORK_DIR`.
2. NUNCA grave outputs em `SKILL_DIR`. Outputs vão para `WORK_DIR`.
3. NUNCA copie scripts ou `base.html` para `WORK_DIR`. Eles ficam em `SKILL_DIR`.
4. Sempre invoque os scripts passando caminhos ABSOLUTOS, prefixando:
   - scripts: `<SKILL_DIR>\scripts\<script>.py`
   - template: `<SKILL_DIR>\base.html`
   - inputs/outputs: `<WORK_DIR>\<arquivo>`
5. `SKILL_DIR` é o caminho absoluto da pasta onde você (IA) leu este `SKILL.md`. Resolva-o no momento da execução; não hardcode.
6. `WORK_DIR` é o cwd do shell atual ou a pasta passada pelo usuário. Em PowerShell: `$PWD.Path`. Não assuma um caminho fixo.
7. Sempre envolva os caminhos em aspas duplas, pois há computadores com espaços e acentos no caminho do usuário, ex.: `OneDrive - Empresa`.
8. **NUNCA use `Get-ChildItem` para listar ou verificar arquivos em `WORK_DIR`.** Em Windows, `Get-ChildItem` retorna vazio silenciosamente quando o caminho contém caracteres acentuados (ex.: `í`, `ã`, `ç`). Use sempre `cmd /c dir /b "<WORK_DIR>"` para listar arquivos, ou confie diretamente nos scripts Python da skill.

## Exemplos de Invocação Correta

### Extrair DOCX

PowerShell, Windows:

```powershell
python "<SKILL_DIR>\scripts\extract_docx.py" "<WORK_DIR>\entrada.docx" "<WORK_DIR>\entrada.txt"
```

## Workflows

### 1. Unificar Arquivos

Script:

```text
scripts/unificar-arquivos.py
```

O script pertence à pasta da skill, NÃO ao projeto atual.

Antes de executar:

1. Localizar a pasta da skill
2. Resolver o `WORK_DIR` como o cwd atual ou a pasta indicada pelo usuário
3. Executar o script da skill passando o `WORK_DIR` como argumento

Execução:

```powershell
python "<SKILL_DIR>\scripts\unificar-arquivos.py" "<WORK_DIR>"
```

Observação:

Toda a lógica de leitura, consolidação e geração do arquivo final já está implementada no script. Ele gera `UNIFICADO\UNIFICADO.md` e cria a pasta `artefatos` dentro do `WORK_DIR`.

### 2. Gerar Artefatos

Use os scripts abaixo para reduzir leitura manual e consumo de tokens:

```text
scripts/listar-habilidades.py
scripts/salvar-artefato.py
```

Preparar a fila de habilidades:

```powershell
python "<SKILL_DIR>\scripts\listar-habilidades.py" "<WORK_DIR>"
```

Para cada item da fila, o agente deve executar os comandos da habilidade e salvar a saída diretamente em `WORK_DIR\artefatos`, usando o mesmo nome do arquivo de origem.

- Não salve artefatos em `SKILL_DIR` e não altere os arquivos originais em `SKILL_DIR\habilidades`.
- Não crie arquivos temporários em `SKILL_DIR` e nem `WORK_DIR`.
- Não use terminal para gravar texto gerado pelo agente: não use pipe, stdin, `echo`, `type`, redirecionamento `>`, `Out-File` ou `Set-Content`.
- Grave os artefatos diretamente com ferramenta de escrita/edição de arquivo do agente, em UTF-8.
- Se qualquer artefato aparecer com padrões como `reuni?o`, `Aus?ncia` ou `gest??o`, descarte e regenere esse artefato a partir do Passo 2. Não tente corrigir por encoding, pois o caractere original já foi perdido.

### 3. Consolidar em um único .json

Use os scripts abaixo:

```text
scripts/criar-pasta-json.py
scripts/consolidar-artefatos-json.py
```

Criar a pasta `json`:

```powershell
python "<SKILL_DIR>\scripts\criar-pasta-json.py" "<WORK_DIR>"
```

Gerar `json\artefatos.json` a partir dos arquivos `.md` em `WORK_DIR\artefatos`:

```powershell
python "<SKILL_DIR>\scripts\consolidar-artefatos-json.py" "<WORK_DIR>"
```

Se o script bloquear por perda de acentuação, não investigue os scripts e não avance para o Passo 4. Volte ao Passo 2 e regenere os `.md` indicados em UTF-8.

### 4. Monta Relatório Analítico

Use o script abaixo:

```text
scripts/montar-relatorio-analitico.py
```

Gerar `html\Analise.html`:

```powershell
python "<SKILL_DIR>\scripts\montar-relatorio-analitico.py" "<WORK_DIR>"
```