# -*- coding: utf-8 -*-

"""
Insere o conteudo de analise-spec.json no placeholder
##INSIRA_CONTEUDO_analise-spec.json## em WORK_DIR\\html\\Analise.html.

Aceita tambem o formato legado analise-spec.md (inserido como pre).

Uso:
    python "<SKILL_DIR>\\scripts\\inserir-analise-spec.py" "<WORK_DIR>"
"""

import json
import os
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

MARCADOR   = "##INSIRA_CONTEUDO_analise-spec.json##"
ENCODINGS  = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


def resolver_work_dir():
    if len(sys.argv) < 2:
        raise ValueError("Uso: python inserir-analise-spec.py <WORK_DIR>")
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


def escapar_html(texto):
    return (
        texto
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    work_dir  = resolver_work_dir()
    pasta     = work_dir / "analise-spec"
    html_path = work_dir / "html" / "Analise.html"

    if not html_path.exists():
        raise FileNotFoundError(f"Analise.html nao encontrado: {html_path}")

    html = ler_texto(html_path)

    # ── Prioridade 1: JSON ────────────────────────────────────────────────────
    json_path = pasta / "analise-spec.json"
    if json_path.exists():
        if MARCADOR not in html:
            raise ValueError(f"Marcador nao encontrado em Analise.html: {MARCADOR}")

        conteudo_json = compactar_json(ler_texto(json_path))

        padrao = re.compile(r"\{\s*" + re.escape(MARCADOR) + r"\s*\}", re.MULTILINE)
        if padrao.search(html):
            html = padrao.sub(lambda _: conteudo_json.strip(), html, count=1)
        else:
            html = html.replace(MARCADOR, conteudo_json.strip(), 1)

        html_path.write_bytes(html.encode("utf-8"))
        print(f"Analise inserida em: {html_path}")
        return

    # ── Fallback: MD legado ───────────────────────────────────────────────────
    md_path = pasta / "analise-spec.md"
    if md_path.exists():
        conteudo_md = ler_texto(md_path)
        conteudo_html = (
            f'<pre style="white-space:pre-wrap;word-break:break-word;">'
            f'{escapar_html(conteudo_md.strip())}'
            f'</pre>'
        )
        padrao_div = re.compile(
            r'(<div\s[^>]*id=["\']Analise-Especifica[çc][aã]o["\'][^>]*>)(.*?)(</div>)',
            re.DOTALL | re.IGNORECASE,
        )
        if not padrao_div.search(html):
            raise ValueError('Elemento <div id="Analise-Especificação"> nao encontrado.')

        novo_html = padrao_div.sub(
            lambda m: m.group(1) + "\n" + conteudo_html + "\n" + m.group(3),
            html,
            count=1,
        )
        html_path.write_bytes(novo_html.encode("utf-8"))
        print(f"Analise (MD legado) inserida em: {html_path}")
        return

    raise FileNotFoundError(
        f"Nenhum arquivo analise-spec.json ou analise-spec.md encontrado em: {pasta}"
    )


if __name__ == "__main__":
    main()
