# -*- coding: utf-8 -*-

"""
Insere o conteudo de todos os arquivos spec.md encontrados em WORK_DIR\\specs
dentro do elemento <div id="Especificacao"></div> do arquivo WORK_DIR\\html\\Analise.html.

Cada spec.md recebe um <h3> com o nome da pasta pai como titulo.
Os specs sao inseridos em ordem alfabetica pelo nome da pasta.

Uso:
    python "<SKILL_DIR>\\scripts\\inserir-especificacao.py" "<WORK_DIR>"
"""

import os
import re
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ID_ALVO        = "Especificação"
ENCODINGS      = ("utf-8-sig", "utf-8", "cp1252", "latin-1")


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


def montar_bloco_html(titulo, conteudo_md):
    conteudo_escapado = escapar_html(conteudo_md.strip())
    return (
        f'<h3 style="margin-top:32px;margin-bottom:8px;">{escapar_html(titulo)}</h3>\n'
        f'<pre style="white-space:pre-wrap;word-break:break-word;">'
        f'{conteudo_escapado}'
        f'</pre>'
    )


def main():
    work_dir   = resolver_work_dir()
    specs_dir  = work_dir / "specs"
    html_file  = work_dir / "html" / "Analise.html"

    if not specs_dir.exists():
        raise FileNotFoundError(f"Pasta specs nao encontrada: {specs_dir}")

    if not html_file.exists():
        raise FileNotFoundError(f"Analise.html nao encontrado: {html_file}")

    # Coleta todos os spec.md ordenados pelo nome da pasta pai
    specs = sorted(
        specs_dir.rglob("spec.md"),
        key=lambda p: p.parent.name.lower()
    )

    if not specs:
        raise FileNotFoundError(f"Nenhum arquivo spec.md encontrado em: {specs_dir}")

    print(f"Specs encontrados: {len(specs)}")

    blocos = []
    for spec in specs:
        titulo  = spec.parent.name
        conteudo = ler_texto(spec)
        blocos.append(montar_bloco_html(titulo, conteudo))
        print(f"  + {titulo}")

    html_conteudo = "\n\n".join(blocos)

    html = ler_texto(html_file)

    padrao = re.compile(
        r'(<div\s[^>]*id=["\']Especifica[çc][aã]o["\'][^>]*>)(.*?)(</div>)',
        re.DOTALL | re.IGNORECASE,
    )

    if not padrao.search(html):
        raise ValueError(
            f'Elemento <div id="{ID_ALVO}"> nao encontrado em: {html_file}\n'
            'Verifique se o id esta escrito exatamente como "Especificação" ou "Especificacao".'
        )

    novo_html = padrao.sub(
        lambda m: m.group(1) + "\n" + html_conteudo + "\n" + m.group(3),
        html,
        count=1,
    )

    html_file.write_bytes(novo_html.encode("utf-8"))

    print(f"\nEspecificacao inserida em: {html_file}")


if __name__ == "__main__":
    main()
