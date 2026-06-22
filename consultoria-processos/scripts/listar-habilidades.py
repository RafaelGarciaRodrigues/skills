# -*- coding: utf-8 -*-

"""
Lista as habilidades da skill em ordem alfabetica e prepara uma fila para o agente.

Uso:
    python "<SKILL_DIR>\\scripts\\listar-habilidades.py" "<WORK_DIR>"

Saida:
    - Cria/atualiza "<WORK_DIR>\\artefatos\\_fila_habilidades.json"
    - Imprime no terminal os comandos de cada habilidade em ordem alfabetica
"""

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"


def resolver_skill_dir():
    return Path(__file__).resolve().parents[1]


def resolver_work_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    return Path.cwd().resolve()


def ler_texto(caminho):
    return caminho.read_text(encoding="utf-8", errors="ignore")


def main():
    skill_dir = resolver_skill_dir()
    work_dir = resolver_work_dir()
    habilidades_dir = skill_dir / "habilidades"
    artefatos_dir = work_dir / "artefatos"

    if not habilidades_dir.exists():
        raise FileNotFoundError(f"Pasta de habilidades nao encontrada: {habilidades_dir}")

    artefatos_dir.mkdir(parents=True, exist_ok=True)

    habilidades = []

    for caminho in sorted(habilidades_dir.iterdir(), key=lambda item: item.name.lower()):
        if not caminho.is_file():
            continue

        # Arquivos prefixados com "00." são prompts de workflow (ex: 00.estado-atual.md),
        # não habilidades geradoras de artefato — ignorar nesta fila.
        if caminho.name.startswith("00."):
            continue

        conteudo = ler_texto(caminho)
        habilidades.append(
            {
                "nome": caminho.name,
                "origem": str(caminho),
                "destino": str(artefatos_dir / caminho.name),
                "comandos": conteudo,
            }
        )

    fila_saida = artefatos_dir / "_fila_habilidades.json"
    fila_saida.write_text(
        json.dumps(habilidades, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Fila de habilidades salva em: {fila_saida}")
    print(f"Total de habilidades: {len(habilidades)}")

    for indice, habilidade in enumerate(habilidades, start=1):
        print("\n" + "=" * 80)
        print(f"HABILIDADE {indice}: {habilidade['nome']}")
        print(f"ORIGEM: {habilidade['origem']}")
        print(f"DESTINO ESPERADO: {habilidade['destino']}")
        print("-" * 80)
        print(habilidade["comandos"])


if __name__ == "__main__":
    main()
