# -*- coding: utf-8 -*-

"""
===========================================================
UNIFICADOR DE ARQUIVOS -> UNIFICADO/UNIFICADO.md
===========================================================

REGRAS DE EXECUÇÃO
------------------

- Windows: usar `python` (NUNCA `python3`)
- NÃO usar `.venv`, `virtualenv`, `conda` ou ambientes temporários
- Usar sempre o Python global da máquina
- Se faltar biblioteca:
    pip install python-docx PyPDF2 textract

- Sempre executar com UTF-8:
    PYTHONUTF8=1 python unificar-arquivos.py

OU deixar o próprio script forçar:
    os.environ["PYTHONUTF8"] = "1"

BIBLIOTECAS USADAS
------------------

DOCX:
    python-docx

PDF:
    PyPDF2

DOC:
    textract
    (no Windows pode exigir Word instalado)

TXT / MD:
    biblioteca padrão

COMPORTAMENTO
--------------

- Varre a pasta atual recursivamente
  ou a pasta informada no primeiro argumento
- Lê:
    .doc
    .docx
    .pdf
    .txt
    .md

- Ignora:
    pasta UNIFICADO
    pasta artefatos
    próprio arquivo UNIFICADO.md

- Cria:
    ./UNIFICADO/
    ./artefatos/

- Salva:
    ./UNIFICADO/UNIFICADO.md

FORMATO FINAL
--------------

# nome_arquivo.ext

conteúdo...

===========================================================
"""

import os
import sys
import datetime

os.environ["PYTHONUTF8"] = "1"

from pathlib import Path

ARQUIVOS_SUPORTADOS = {".doc", ".docx", ".pdf", ".txt", ".md"}

PASTA_SAIDA = "UNIFICADO"
PASTA_ARTEFATOS = "artefatos"
ARQUIVO_SAIDA = "UNIFICADO.md"


def resolver_work_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    return Path.cwd().resolve()


def ler_txt_md(caminho):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def ler_docx(caminho):
    try:
        from docx import Document
    except ImportError:
        raise ImportError(
            "Biblioteca ausente: python-docx\n"
            "Instale com:\n"
            "pip install python-docx"
        )

    doc = Document(caminho)

    linhas = []

    for p in doc.paragraphs:
        texto = p.text.strip()

        if texto:
            linhas.append(texto)

    return "\n".join(linhas)


def ler_pdf(caminho):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError(
            "Biblioteca ausente: PyPDF2\n"
            "Instale com:\n"
            "pip install PyPDF2"
        )

    texto_final = []

    reader = PdfReader(caminho)

    for pagina in reader.pages:
        try:
            texto = pagina.extract_text()

            if texto:
                texto_final.append(texto)

        except Exception as e:
            texto_final.append(f"[ERRO AO LER PÁGINA PDF: {e}]")

    return "\n".join(texto_final)


def ler_doc(caminho):
    try:
        import textract
    except ImportError:
        raise ImportError(
            "Biblioteca ausente: textract\n"
            "Instale com:\n"
            "pip install textract"
        )

    try:
        texto = textract.process(str(caminho))
        return texto.decode("utf-8", errors="ignore")

    except Exception as e:
        return f"[ERRO AO LER DOC: {e}]"


def extrair_texto(caminho):
    ext = caminho.suffix.lower()

    if ext in [".txt", ".md"]:
        return ler_txt_md(caminho)

    elif ext == ".docx":
        return ler_docx(caminho)

    elif ext == ".pdf":
        return ler_pdf(caminho)

    elif ext == ".doc":
        return ler_doc(caminho)

    return ""


PROMPT_INSTRUCIONAL = """\
> [!INSTRUÇÃO PARA O AGENTE]
>
> Os trechos abaixo são transcrições de conversas que ocorreram **separadamente e em momentos
> cronológicos distintos**. Elas fazem parte de um mesmo processo de levantamento que começa
> amplo e superficial e, ao longo das sessões, vai aprofundando e convergindo os temas —
> tornando o entendimento progressivamente mais claro e preciso.
>
> Por isso:
>
> - Um assunto que aparece **indefinido ou incoerente em um trecho** pode ter sua definição
>   mais clara em uma sessão posterior. **Não considere trechos isolados** como verdade
>   absoluta; leia o conjunto.
> - Ao fazer **resumos ou análises aprofundadas**, leve em conta a evolução cronológica do
>   entendimento: o que foi dito mais tarde tende a ser mais preciso do que o que foi dito
>   antes.
> - Contradições aparentes entre trechos geralmente indicam **refinamento de entendimento**,
>   não erro — dê preferência à versão mais recente ou mais detalhada.
> - O processo começa com uma **conversa exploratória e ampla** (descuberta de problemas,
>   necessidades e contexto) e evolui para sessões de **aprofundamento e especificação**
>   (definição de requisitos, decisões e restrições). Considere essa lógica ao interpretar
>   o grau de certeza de cada informação.

---

"""


def data_criacao(caminho: Path) -> str:
    """
    Retorna a data de criação do arquivo no formato dd/mm/aaaa HH:MM.
    No Windows, os.path.getctime() retorna o tempo real de criação.
    Em outros SOs usa o menor entre ctime e mtime como aproximação.
    """
    try:
        ctime = os.path.getctime(caminho)
        mtime = os.path.getmtime(caminho)
        ts = min(ctime, mtime)           # garante que nunca ultrapassa mtime
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return "data desconhecida"


def main():
    pasta_atual = resolver_work_dir()

    pasta_saida = pasta_atual / PASTA_SAIDA
    pasta_saida.mkdir(exist_ok=True)

    pasta_artefatos = pasta_atual / PASTA_ARTEFATOS
    pasta_artefatos.mkdir(exist_ok=True)

    arquivo_saida = pasta_saida / ARQUIVO_SAIDA

    # Coleta apenas arquivos diretamente em WORK_DIR (sem subpastas)
    arquivos = []
    for caminho in pasta_atual.iterdir():
        if not caminho.is_file():
            continue
        if caminho.suffix.lower() not in ARQUIVOS_SUPORTADOS:
            continue
        if caminho.name == ARQUIVO_SAIDA:
            continue
        arquivos.append(caminho)

    # Ordena cronologicamente pela data de criação (mais antigo primeiro)
    arquivos.sort(key=lambda p: os.path.getctime(p))

    conteudo_final = [PROMPT_INSTRUCIONAL]

    for caminho in arquivos:
        print(f"LENDO: {caminho}")

        try:
            texto = extrair_texto(caminho)
            if not texto.strip():
                texto = "[ARQUIVO SEM TEXTO EXTRAÍDO]"
        except Exception as e:
            texto = f"[ERRO AO PROCESSAR ARQUIVO: {e}]"

        dt = data_criacao(caminho)

        bloco = f"""# {caminho.name}

**Data de criação:** {dt}
Origem: {caminho}

{texto}


"""

        conteudo_final.append(bloco)

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(conteudo_final))

    print("\n===================================")
    print("FINALIZADO")
    print(f"Arquivo salvo em:\n{arquivo_saida}")
    print(f"Pasta de artefatos criada em:\n{pasta_artefatos}")
    print("===================================\n")


if __name__ == "__main__":
    main()