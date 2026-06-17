# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente em WORK_DIR\\analise-spec\\analise-spec.json.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-analise-spec.py" "<WORK_DIR>" "<arquivo-com-saida-utf8>"
"""

import json
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
    work_dir = resolver_work_dir()
    conteudo = ler_conteudo().strip()

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as e:
        raise ValueError(f"Saida nao e JSON valido: {e}")

    if not isinstance(dados, dict):
        raise ValueError("JSON deve ser um objeto (dict) na raiz.")

    if "analise-spec" not in dados:
        raise ValueError("JSON deve conter a chave 'analise-spec'.")

    if not isinstance(dados["analise-spec"], list):
        raise ValueError("'analise-spec' deve ser uma lista de categorias.")

    pasta_saida = work_dir / "analise-spec"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivo_saida = pasta_saida / "analise-spec.json"
    arquivo_saida.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Remove arquivo .md legado se existir
    md_legado = pasta_saida / "analise-spec.md"
    if md_legado.exists():
        md_legado.unlink()

    # Remove arquivo temporario de input
    tmp = Path(sys.argv[2]).expanduser().resolve()
    if tmp.exists():
        tmp.unlink()

    categorias = len(dados["analise-spec"])
    itens = sum(len(c.get("itens", [])) for c in dados["analise-spec"])
    print(f"Analise salva em: {arquivo_saida}")
    print(f"  {categorias} categorias, {itens} itens no total")


if __name__ == "__main__":
    main()
