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


def main():
    pasta_atual = resolver_work_dir()

    pasta_saida = pasta_atual / PASTA_SAIDA
    pasta_saida.mkdir(exist_ok=True)

    pasta_artefatos = pasta_atual / PASTA_ARTEFATOS
    pasta_artefatos.mkdir(exist_ok=True)

    arquivo_saida = pasta_saida / ARQUIVO_SAIDA

    conteudo_final = []

    for caminho in pasta_atual.rglob("*"):
        if not caminho.is_file():
            continue

        if caminho.suffix.lower() not in ARQUIVOS_SUPORTADOS:
            continue

        # Ignora pastas geradas pelo próprio fluxo
        if PASTA_SAIDA in caminho.parts or PASTA_ARTEFATOS in caminho.parts:
            continue

        # Ignora próprio arquivo de saída
        if caminho.name == ARQUIVO_SAIDA:
            continue

        print(f"LENDO: {caminho}")

        try:
            texto = extrair_texto(caminho)

            if not texto.strip():
                texto = "[ARQUIVO SEM TEXTO EXTRAÍDO]"

        except Exception as e:
            texto = f"[ERRO AO PROCESSAR ARQUIVO: {e}]"

        bloco = f"""
# {caminho.name}

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