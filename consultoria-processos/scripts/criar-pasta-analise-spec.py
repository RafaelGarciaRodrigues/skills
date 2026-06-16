# -*- coding: utf-8 -*-

"""
Cria a pasta "analise spec" dentro do WORK_DIR.

Uso:
    python "<SKILL_DIR>\\scripts\\criar-pasta-analise-spec.py" "<WORK_DIR>"
"""

import os
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"


def resolver_work_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return Path.cwd().resolve()


def main():
    work_dir  = resolver_work_dir()
    pasta     = work_dir / "analise-spec"
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"Pasta criada em: {pasta}")


if __name__ == "__main__":
    main()
