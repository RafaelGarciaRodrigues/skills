# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente na pasta artefatos do WORK_DIR.

Uso com arquivo de entrada:
    python "<SKILL_DIR>\\scripts\\salvar-artefato.py" "<WORK_DIR>" "nome-habilidade.md" "<arquivo-com-saida-utf8>"

Saida:
    - Cria/atualiza "<WORK_DIR>\\artefatos\\nome-habilidade.md"
"""

import os
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS_SUPORTADOS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")
PADRAO_PERDA_ACENTO = re.compile(r"[A-Za-zÀ-ÿ]\?[A-Za-zÀ-ÿ]|\?\?")


def resolver_work_dir():
    if len(sys.argv) < 3:
        raise ValueError(
            "Uso: python salvar-artefato.py <WORK_DIR> <nome_habilidade> [arquivo_conteudo]"
        )

    return Path(sys.argv[1]).expanduser().resolve()


def resolver_nome_habilidade():
    nome = Path(sys.argv[2]).name

    if not nome:
        raise ValueError("Nome da habilidade nao informado.")

    return nome


def decodificar_texto(dados):
    for encoding in ENCODINGS_SUPORTADOS:
        try:
            return dados.decode(encoding)
        except UnicodeDecodeError:
            continue

    return dados.decode("utf-8", errors="replace")


def ler_conteudo():
    if len(sys.argv) > 3:
        caminho_conteudo = Path(sys.argv[3]).expanduser().resolve()
        return decodificar_texto(caminho_conteudo.read_bytes())

    raise ValueError(
        "Informe um arquivo de conteudo UTF-8. Entrada via stdin foi removida "
        "porque pode corromper acentos no Windows."
    )


def validar_conteudo(conteudo):
    if PADRAO_PERDA_ACENTO.search(conteudo):
        raise ValueError(
            "Possivel perda de acentuacao detectada no conteudo. "
            "Exemplo comum: 'reuni?o' em vez de 'reunião'. "
            "Regere a saida em UTF-8 antes de salvar o artefato."
        )


def main():
    work_dir = resolver_work_dir()
    nome_habilidade = resolver_nome_habilidade()
    conteudo = ler_conteudo()
    validar_conteudo(conteudo)

    artefatos_dir = work_dir / "artefatos"
    artefatos_dir.mkdir(parents=True, exist_ok=True)

    arquivo_saida = artefatos_dir / nome_habilidade
    arquivo_saida.write_text(conteudo, encoding="utf-8")

    print(f"Artefato salvo em: {arquivo_saida}")


if __name__ == "__main__":
    main()
