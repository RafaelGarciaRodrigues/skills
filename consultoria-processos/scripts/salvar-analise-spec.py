# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente em WORK_DIR\\analise-spec\\analise-spec.md.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-analise-spec.py" "<WORK_DIR>" "<arquivo-com-saida-utf8>"
"""

import os
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")


def resolver_work_dir():
    if len(sys.argv) < 3:
        raise ValueError(
            "Uso: python salvar-analise-spec.py <WORK_DIR> <arquivo-com-saida>"
        )
    return Path(sys.argv[1]).expanduser().resolve()


def ler_conteudo():
    caminho = Path(sys.argv[2]).expanduser().resolve()
    for enc in ENCODINGS:
        try:
            return caminho.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return caminho.read_text(encoding="utf-8", errors="replace")


def main():
    work_dir  = resolver_work_dir()
    conteudo  = ler_conteudo()

    pasta_saida  = work_dir / "analise-spec"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivo_saida = pasta_saida / "analise-spec.md"
    arquivo_saida.write_text(conteudo, encoding="utf-8")

    print(f"Analise salva em: {arquivo_saida}")


if __name__ == "__main__":
    main()
