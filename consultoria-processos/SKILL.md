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
- `scripts/iniciar-speckit.bat`
- `scripts/inserir-especificacao.py`
- `scripts/criar-pasta-analise-spec.py`
- `scripts/listar-analise-spec.py`
- `scripts/salvar-analise-spec.py`
- `scripts/inserir-analise-spec.py`
- `scripts/salvar-plano.py`
- `scripts/inserir-plano.py`
- `analise-spec/`
- `plano/plano.md`
- `html/relatorio-modelo.html`
- `habilidades/`

### `WORK_DIR`

Pasta de trabalho do usuário, ou seja, o cwd atual ou a pasta indicada explicitamente pelo usuário.

Contém:

- INPUTS: arquivos de transcrição (`.txt`, `.docx`, `.pdf`, `.md`, `.csv`, `.json`, `.html`, `.xlsx`, `.pptx`, `.doc`, `.ppt`, `.xls`)
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

Para cada item da fila, o agente deve executar os comandos da habilidade e salvar a saída em `WORK_DIR\artefatos`, usando **extensão `.json`** (ex.: `4.necessidades.json`).

**Formato de saída obrigatório:** cada habilidade pede que a IA responda com um JSON puro — sem blocos de código markdown, sem texto explicativo antes ou depois. O agente deve gravar exatamente o que a IA produziu em um arquivo temporário e então invocar o script:

```powershell
python "<SKILL_DIR>\scripts\salvar-artefato.py" "<WORK_DIR>" "4.necessidades.json" "<arquivo-com-saida>"
```

O script valida o JSON e salva em `WORK_DIR\artefatos\4.necessidades.json`.

Regras:
- Não salve artefatos em `SKILL_DIR` e não altere os arquivos originais em `SKILL_DIR\habilidades`.
- Não crie arquivos temporários em `SKILL_DIR` e nem `WORK_DIR` além do necessário para o script.
- Não use terminal para gravar texto gerado pelo agente: não use pipe, stdin, `echo`, `type`, redirecionamento `>`, `Out-File` ou `Set-Content`.
- Grave os artefatos diretamente com ferramenta de escrita/edição de arquivo do agente, em UTF-8.
- Se qualquer artefato apresentar padrões como `reuni?o`, `Aus?ncia` ou `gest??o`, descarte e regenere a partir do Passo 2. Não tente corrigir por encoding.
- Se o script retornar erro de JSON inválido, peça à IA para regenerar a saída em formato JSON puro e tente novamente.

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

Use o script unificado abaixo. Ele executa em sequência todos os inserts disponíveis (especificação, análise, dimensionamento, convergência, plano), pulando automaticamente os que ainda não existirem:

```text
scripts/montar-relatorio-completo.py
```

```powershell
python "<SKILL_DIR>\scripts\montar-relatorio-completo.py" "<WORK_DIR>"
```

> **Regra:** sempre use `montar-relatorio-completo.py` em vez de `montar-relatorio-analitico.py` para evitar perder conteúdos já inseridos nas execuções anteriores.

### 5. Iniciar Spec Kit

Script:

```text
scripts/iniciar-speckit.bat
```

Pré-requisito: `specify-cli` instalado via `uv`. Instale uma vez:

```powershell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

Execução:

```powershell
"<SKILL_DIR>\scripts\iniciar-speckit.bat" "<WORK_DIR>"
```

O script inicializa o Spec Kit na pasta `WORK_DIR` com integração para o Cursor. Após rodar, os comandos `/speckit.*` ficam disponíveis no chat para conduzir o desenvolvimento a partir da especificação gerada nos passos anteriores.

### 6. Especificar com Spec Kit

O agente executa este passo diretamente, sem interação do usuário.

1. Localizar o arquivo de comando do Spec Kit dentro de `WORK_DIR`:
   - `.claude\commands\specify.md` (integração Cursor/Claude)
   - ou `.cursor\rules\specify.md`
2. Ler o arquivo encontrado para entender o formato exigido pelo `/speckit.specify`
3. Ler `WORK_DIR\json\artefatos.json`
4. Extrair os campos `problema-central`, `necessidades` e `requisitos`
5. Seguir as instruções do arquivo de comando e gerar `specs\001-[titulo]\spec.md` dentro do `WORK_DIR`

Regras:
- Use o conteúdo real dos campos, sem truncar.
- Não inclua campos de análise interna como `maturidade`, `contradicoes` ou `mapa-mental`.
- Se `necessidades` ou `requisitos` estiverem em Markdown com `#` e `-`, mantenha a formatação.
- Se o arquivo de comando não for encontrado, o Passo 5 (`iniciar-speckit.bat`) ainda não foi executado. Execute-o antes de continuar.

### 7. Inserir Especificação no Relatório

```powershell
python "<SKILL_DIR>\scripts\inserir-especificacao.py" "<WORK_DIR>"
```

O script encontra todos os `spec.md` dentro de `WORK_DIR\specs`, ordena pelo nome da pasta e insere o conteúdo em `<div id="Especificação"></div>` no `Analise.html`. Cada spec recebe um `<h3>` com o nome da pasta como título.

### 8. Analisar a Especificação

Criar a pasta `analise-spec` em `WORK_DIR`:

```powershell
python "<SKILL_DIR>\scripts\criar-pasta-analise-spec.py" "<WORK_DIR>"
```

Ler e imprimir os comandos de análise:

```powershell
python "<SKILL_DIR>\scripts\listar-analise-spec.py" "<WORK_DIR>"
```

O script lê o arquivo em `SKILL_DIR\analise-spec` e imprime os comandos para o agente executar.

O agente executa os comandos e salva a saída em `WORK_DIR\analise-spec\analise-spec.md`:

```powershell
python "<SKILL_DIR>\scripts\salvar-analise-spec.py" "<WORK_DIR>" "<arquivo-com-saida>"
```

- Toda a gravação é feita pelo script Python, sem intervenção do agente.

### 9. Inserir Análise no Relatório

```powershell
python "<SKILL_DIR>\scripts\inserir-analise-spec.py" "<WORK_DIR>"
```

### 10. Dimensionamento

Ler o arquivo de comando:

```text
<SKILL_DIR>\dimensionamento\dimensionamento.md
```

```powershell
python "<SKILL_DIR>\scripts\salvar-dimensionamento.py" "<WORK_DIR>" "<arquivo-com-saida>"
```

O resultado é salvo em `WORK_DIR\dimensionamento\dimensionamento.json`.

### 11. Inserir Dimensionamento no Relatório

```powershell
python "<SKILL_DIR>\scripts\inserir-dimensionamento.py" "<WORK_DIR>"
```

O script lê `WORK_DIR\dimensionamento\dimensionamento.json`, insere o conteúdo no placeholder `##INSIRA_CONTEUDO_dimensionamento.json##` dentro de `Analise.html` e salva o arquivo. O JavaScript do relatório consome esse JSON e renderiza automaticamente as 3 tabelas de cenário, a seção de atividades por função e a análise.

### 12. Convergência de Escopo

Ler o arquivo de comando:

```text
<SKILL_DIR>\convergencia\convergecia.md
```

O agente lê todos os artefatos referenciados no arquivo, executa a análise e grava a saída em um arquivo temporário. Em seguida executa:

```powershell
python "<SKILL_DIR>\scripts\salvar-convergencia.py" "<WORK_DIR>" "<arquivo-com-saida>"
```

O resultado é salvo em `WORK_DIR\convergir\convergir.json`. Para inserir no relatório:

```powershell
python "<SKILL_DIR>\scripts\inserir-convergencia.py" "<WORK_DIR>"
```


### 13. Plano de Execução

Ler o arquivo de comando:

```text
<SKILL_DIR>\plano\plano.md
```

O agente lê todos os artefatos referenciados no arquivo, executa a análise e grava a saída JSON em um arquivo temporário. Em seguida executa:

```powershell
python "<SKILL_DIR>\scripts\salvar-plano.py" "<WORK_DIR>" "<arquivo-com-saida>"
```

O resultado é salvo em `WORK_DIR\plano\plano.json` (a pasta é criada automaticamente). O script valida o JSON contra o schema esperado e remove o arquivo temporário ao final.

Para inserir no relatório:

```powershell
python "<SKILL_DIR>\scripts\inserir-plano.py" "<WORK_DIR>"
```

O script insere o conteúdo de `plano.json` no placeholder `##INSIRA_CONTEUDO_plano.json##` dentro de `Analise.html`. O JavaScript do relatório renderiza automaticamente as 5 macro-etapas (ENTENDER → DIAGNOSTICAR → SIMPLIFICAR → ESTRUTURAR → AUTOMATIZAR) com tabela de atividades, indicadores de conclusão, responsáveis e badges de prioridade.








