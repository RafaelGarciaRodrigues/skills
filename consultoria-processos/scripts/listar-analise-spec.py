# -*- coding: utf-8 -*-

"""
Le o arquivo de analise em SKILL_DIR\\analise-spec e imprime
os comandos para o agente executar.

Uso:
    python "<SKILL_DIR>\\scripts\\listar-analise-spec.py" "<WORK_DIR>"
"""

import os
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def resolver_skill_dir():
    return Path(__file__).resolve().parents[1]


def resolver_work_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return Path.cwd().resolve()


def ler_texto(caminho):
    for enc in ENCODINGS:
        try:
            return caminho.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return caminho.read_text(encoding="utf-8", errors="replace")


def main():
    skill_dir    = resolver_skill_dir()
    analises_dir = skill_dir / "analise-spec"

    if not analises_dir.exists():
        raise FileNotFoundError(f"Pasta analise-spec nao encontrada: {analises_dir}")

    arquivos = sorted(
        (p for p in analises_dir.iterdir() if p.is_file()),
        key=lambda p: p.name.lower(),
    )

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em: {analises_dir}")

    for arquivo in arquivos:
        conteudo = ler_texto(arquivo)
        print("=" * 80)
        print(f"ARQUIVO: {arquivo.name}")
        print("-" * 80)
        print(conteudo)
        print("=" * 80)


if __name__ == "__main__":
    main()
