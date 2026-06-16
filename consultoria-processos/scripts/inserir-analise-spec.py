# -*- coding: utf-8 -*-

"""
Insere o conteudo de WORK_DIR\\analise-spec\\analise-spec.md
dentro de <div id="Analise-Especificação"></div> no WORK_DIR\\html\\Analise.html.

Uso:
    python "<SKILL_DIR>\\scripts\\inserir-analise-spec.py" "<WORK_DIR>"
"""

import os
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


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


def escapar_html(texto):
    return (
        texto
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    work_dir      = resolver_work_dir()
    md_origem     = work_dir / "analise-spec" / "analise-spec.md"
    html_file     = work_dir / "html" / "Analise.html"

    if not md_origem.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {md_origem}")

    if not html_file.exists():
        raise FileNotFoundError(f"Analise.html nao encontrado: {html_file}")

    conteudo_md  = ler_texto(md_origem)
    html         = ler_texto(html_file)

    conteudo_html = (
        f'<pre style="white-space:pre-wrap;word-break:break-word;">'
        f'{escapar_html(conteudo_md.strip())}'
        f'</pre>'
    )

    padrao = re.compile(
        r'(<div\s[^>]*id=["\']Analise-Especifica[çc][aã]o["\'][^>]*>)(.*?)(</div>)',
        re.DOTALL | re.IGNORECASE,
    )

    if not padrao.search(html):
        raise ValueError(
            'Elemento <div id="Analise-Especificação"> nao encontrado em: '
            f'{html_file}'
        )

    novo_html = padrao.sub(
        lambda m: m.group(1) + "\n" + conteudo_html + "\n" + m.group(3),
        html,
        count=1,
    )

    html_file.write_bytes(novo_html.encode("utf-8"))

    print(f"Analise inserida em: {html_file}")


if __name__ == "__main__":
    main()
