# -*- coding: utf-8 -*-

"""
Consolida arquivos .json (e .md legados) de WORK_DIR\\artefatos em WORK_DIR\\json\\artefatos.json.

Regras:
- Arquivos .json: parseados e mesclados diretamente no objeto final
- Arquivos .md (legado): armazenados como string (chave = stem do arquivo)
- Se existirem .json e .md com mesmo stem, o .json tem precedência

Uso:
    python "<SKILL_DIR>\\scripts\\consolidar-artefatos-json.py" "<WORK_DIR>"
"""

import json
import os
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS_SUPORTADOS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")
PADRAO_PERDA_ACENTO = re.compile(r"[A-Za-zÀ-ÿ]\?[A-Za-zÀ-ÿ]|\?\?")


def resolver_work_dir():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    return Path.cwd().resolve()


def decodificar_texto(dados):
    for encoding in ENCODINGS_SUPORTADOS:
        try:
            return dados.decode(encoding)
        except UnicodeDecodeError:
            continue

    return dados.decode("utf-8", errors="replace")


def main():
    work_dir = resolver_work_dir()
    artefatos_dir = work_dir / "artefatos"
    json_dir = work_dir / "json"
    arquivo_saida = json_dir / "artefatos.json"

    if not artefatos_dir.exists():
        raise FileNotFoundError(f"Pasta de artefatos nao encontrada: {artefatos_dir}")

    json_dir.mkdir(parents=True, exist_ok=True)

    artefatos = {}
    arquivos_com_possivel_perda = []

    # Coleta stems já processados para prioridade .json > .md
    stems_processados = set()

    # Primeira passagem: arquivos .json (ignora arquivos que começam com _)
    for caminho in sorted(artefatos_dir.glob("*.json"), key=lambda p: p.name.lower()):
        if caminho.name.startswith("_"):
            continue
        conteudo = decodificar_texto(caminho.read_bytes())

        if PADRAO_PERDA_ACENTO.search(conteudo):
            arquivos_com_possivel_perda.append(caminho.name)
            continue

        try:
            dados = json.loads(conteudo)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Arquivo {caminho.name} nao e um JSON valido: {e}"
            )

        if not isinstance(dados, dict):
            raise ValueError(
                f"Arquivo {caminho.name}: o JSON deve ser um objeto (dict). "
                f"Recebido: {type(dados).__name__}"
            )

        artefatos.update(dados)
        stems_processados.add(caminho.stem)

    # Segunda passagem: arquivos .md legados (ignorados se já existe .json com mesmo stem)
    for caminho in sorted(artefatos_dir.glob("*.md"), key=lambda p: p.name.lower()):
        if caminho.stem in stems_processados:
            continue

        conteudo = decodificar_texto(caminho.read_bytes())
        artefatos[caminho.stem] = conteudo

        if PADRAO_PERDA_ACENTO.search(conteudo):
            arquivos_com_possivel_perda.append(caminho.name)

    if arquivos_com_possivel_perda:
        mensagem = [
            "Possivel perda de acentuacao detectada. O JSON nao foi gerado.",
            "Arquivos com problema:",
        ]
        mensagem.extend(f"- {nome}" for nome in arquivos_com_possivel_perda)
        mensagem.append(
            "Acao obrigatoria: volte ao Passo 2 e regenere esses artefatos "
            "diretamente em UTF-8. Nao investigue este script e nao avance para o Passo 4."
        )
        raise ValueError("\n".join(mensagem))

    arquivo_saida.write_text(
        json.dumps(artefatos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    total_json = len([k for k in artefatos if True])
    print(f"JSON consolidado salvo em: {arquivo_saida}")
    print(f"Total de artefatos consolidados: {len(artefatos)}")


if __name__ == "__main__":
    main()
