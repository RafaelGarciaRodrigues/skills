# -*- coding: utf-8 -*-

"""
Insere o conteúdo de plano.json no placeholder
##INSIRA_CONTEUDO_plano.json## em WORK_DIR\\html\\Analise.html.

Uso:
    python "<SKILL_DIR>\\scripts\\inserir-plano.py" "<WORK_DIR>"
"""

import os
import json
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

MARCADOR  = "##INSIRA_CONTEUDO_plano.json##"
ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def resolver_work_dir():
    if len(sys.argv) < 2:
        raise ValueError("Uso: python inserir-plano.py <WORK_DIR>")
    return Path(sys.argv[1]).expanduser().resolve()


def ler_texto(caminho):
    dados = caminho.read_bytes()
    for enc in ENCODINGS:
        try:
            return dados.decode(enc)
        except UnicodeDecodeError:
            continue
    return dados.decode("utf-8", errors="replace")


def compactar_json(texto):
    dados = json.loads(texto)
    linha = json.dumps(dados, ensure_ascii=False, separators=(",", ":"))
    if "\r" in linha or "\n" in linha:
        raise ValueError("JSON compactado ainda contém quebras de linha.")
    return linha


def main():
    work_dir  = resolver_work_dir()
    json_path = work_dir / "plano" / "plano.json"
    html_path = work_dir / "html" / "Analise.html"

    if not json_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {json_path}")
    if not html_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {html_path}")

    conteudo_json = compactar_json(ler_texto(json_path))
    html = ler_texto(html_path)

    if MARCADOR not in html:
        raise ValueError(f"Marcador não encontrado em Analise.html: {MARCADOR}")

    padrao = re.compile(r"\{\s*" + re.escape(MARCADOR) + r"\s*\}", re.MULTILINE)
    if padrao.search(html):
        html = padrao.sub(lambda _: conteudo_json.strip(), html, count=1)
    else:
        html = html.replace(MARCADOR, conteudo_json.strip(), 1)

    html_path.write_bytes(html.encode("utf-8"))
    print(f"plano.json inserido em: {html_path}")


if __name__ == "__main__":
    main()
