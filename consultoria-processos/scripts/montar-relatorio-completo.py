# -*- coding: utf-8 -*-

"""
Monta o relatorio analitico completo em WORK_DIR\\html\\Analise.html,
inserindo todos os artefatos opcionais que existirem.

Uso:
    python "<SKILL_DIR>\\scripts\\montar-relatorio-completo.py" "<WORK_DIR>"

Ordem de execucao:
    1. montar-relatorio-analitico.py  (base obrigatoria com artefatos.json)
    2. inserir-especificacao.py       (se specs/ existir)
    3. inserir-analise-spec.py        (se analise-spec/analise-spec.md existir)
    4. inserir-dimensionamento.py     (se dimensionamento/dimensionamento.json existir)
    5. inserir-convergencia.py        (se convergir/convergir.json existir)
    6. inserir-plano.py               (se plano/plano.json existir)
"""

import os
import subprocess
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

SCRIPTS = [
    ("montar-relatorio-analitico.py",  None,                                    True),
    ("inserir-especificacao.py",        "specs",                                 False),
    ("inserir-analise-spec.py",         "analise-spec/analise-spec.md",          False),
    ("inserir-dimensionamento.py",      "dimensionamento/dimensionamento.json",   False),
    ("inserir-convergencia.py",         "convergir/convergir.json",              False),
    ("inserir-plano.py",                "plano/plano.json",                      False),
]


def main():
    skill_dir = Path(__file__).resolve().parents[1]

    if len(sys.argv) > 1:
        work_dir = Path(sys.argv[1]).expanduser().resolve()
    else:
        work_dir = Path.cwd().resolve()

    print(f"WORK_DIR: {work_dir}")
    print()

    for script, condicao, obrigatorio in SCRIPTS:
        script_path = skill_dir / "scripts" / script

        if condicao:
            alvo = work_dir / condicao
            if not alvo.exists():
                print(f"[SKIP] {script}  ({condicao} nao encontrado)")
                continue

        print(f"[RUN]  {script}")
        result = subprocess.run(
            [sys.executable, str(script_path), str(work_dir)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.stdout.strip():
            for linha in result.stdout.strip().splitlines():
                print(f"       {linha}")

        if result.returncode != 0:
            msg = result.stderr.strip() or "(sem mensagem de erro)"
            if obrigatorio:
                print(f"[ERRO] {script} falhou:\n{msg}")
                sys.exit(1)
            else:
                print(f"[AVISO] {script} retornou erro (nao critico):\n{msg}")
        print()

    print("Relatorio completo montado com sucesso.")


if __name__ == "__main__":
    main()
