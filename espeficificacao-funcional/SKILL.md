---
name: especificacao-funcional
description: roteiro completo para criar o entendimento de um problema e quebra em uma especificação
disable-model-invocation: true

## Ambiente Python

- Windows, Python via `python` (não `python3`)
- NÃO usar `.venv`, `virtualenv`, `conda` ou ambientes temporários
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
- Se faltar biblioteca: pip install python-docx PyPDF2 textract


---

# Skill: Unificar Arquivos

## Script

```text
scripts/unificar-arquivos.py
```

## Execução
O script pertence à pasta da skill, NÃO ao projeto atual.
Antes de executar:
1. localizar a pasta da skill
2. executar o script a partir dela
```bash
PYTHONUTF8=1 python scripts/unificar-arquivos.py
```

## Observação

Toda a lógica de leitura, consolidação e geração do arquivo final já está implementada no script.
