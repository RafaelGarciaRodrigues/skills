# -*- coding: utf-8 -*-

"""
Monta o relatorio analitico em WORK_DIR\\html\\Analise.html.

Uso:
    python "<SKILL_DIR>\\scripts\\montar-relatorio-analitico.py" "<WORK_DIR>"

Regra interna:
    O JSON inserido no HTML deve ficar em uma unica linha fisica.
"""

import os
import json
import re
import shutil
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

MARCADOR_ARTEFATOS = "##INSIRA_CONTEUDO_artefatos.json##"
ENCODINGS_SUPORTADOS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def resolver_skill_dir():
    return Path(__file__).resolve().parents[1]


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


def ler_texto(caminho):
    return decodificar_texto(caminho.read_bytes())


def compactar_json(conteudo_json):
    dados = json.loads(conteudo_json)
    json_linha_unica = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))

    if "\r" in json_linha_unica or "\n" in json_linha_unica:
        raise ValueError("O JSON compactado ainda contem quebras de linha reais.")

    return json_linha_unica


def resolver_json_artefatos(work_dir):
    caminhos_possiveis = [
        work_dir / "json" / "artefatos.json",
        work_dir / "artefatos" / "artefatos.json",
    ]

    for caminho in caminhos_possiveis:
        if caminho.exists():
            return caminho

    raise FileNotFoundError(
        "Arquivo artefatos.json nao encontrado. Caminhos verificados:\n"
        + "\n".join(str(caminho) for caminho in caminhos_possiveis)
    )


def inserir_json_no_template(template, conteudo_json):
    if MARCADOR_ARTEFATOS not in template:
        raise ValueError(f"Marcador nao encontrado no template: {MARCADOR_ARTEFATOS}")

    padrao_objeto_com_marcador = re.compile(
        r"\{\s*" + re.escape(MARCADOR_ARTEFATOS) + r"\s*\}",
        re.MULTILINE,
    )

    if padrao_objeto_com_marcador.search(template):
        return padrao_objeto_com_marcador.sub(lambda _: conteudo_json.strip(), template, count=1)

    return template.replace(MARCADOR_ARTEFATOS, conteudo_json.strip(), 1)


def main():
    skill_dir = resolver_skill_dir()
    work_dir = resolver_work_dir()

    template_origem = skill_dir / "html" / "relatorio-modelo.html"
    json_artefatos = resolver_json_artefatos(work_dir)
    html_dir = work_dir / "html"
    relatorio_saida = html_dir / "Analise.html"

    if not template_origem.exists():
        raise FileNotFoundError(f"Template nao encontrado: {template_origem}")

    html_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template_origem, relatorio_saida)

    template = ler_texto(relatorio_saida)
    conteudo_json = compactar_json(ler_texto(json_artefatos))
    relatorio = inserir_json_no_template(template, conteudo_json)

    relatorio_saida.write_bytes(relatorio.encode("utf-8"))

    print(f"Relatorio analitico salvo em: {relatorio_saida}")
    print(f"JSON inserido a partir de: {json_artefatos}")


if __name__ == "__main__":
    main()
