# -*- coding: utf-8 -*-

"""
Prepara o contexto para atualização do estado-atual.

- Identifica arquivos novos em WORK_DIR (não ainda processados)
- Monta WORK_DIR\_tmp\estado-input.md com:
    Seção 1: conteúdo do estado-atual.md existente (ou marcação PRIMEIRA RODADA)
    Seção 2: conteúdo dos arquivos novos, ordenados cronologicamente
- Salva WORK_DIR\_tmp\arquivos-novos.json com a lista de arquivos novos
  (para salvar-estado.py referenciar ao atualizar o rastreio)

Uso:
    python "<SKILL_DIR>\\scripts\\preparar-estado.py" "<WORK_DIR>"
"""

import json
import os
import sys
import datetime
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ARQUIVOS_SUPORTADOS = {".doc", ".docx", ".pdf", ".txt", ".md", ".csv"}

# Pastas internas da skill que nunca devem ser lidas como input
PASTAS_IGNORADAS = {
    "unificado", "artefatos", "_tmp", "estado-atual",
    "html", "json", "specs", "analise-spec",
    "dimensionamento", "convergir", "plano",
    ".git", ".cursor", ".claude",
}


def resolver_work_dir():
    if len(sys.argv) < 2:
        raise ValueError("Uso: python preparar-estado.py <WORK_DIR>")
    return Path(sys.argv[1]).expanduser().resolve()


def data_criacao(caminho: Path) -> str:
    try:
        ctime = os.path.getctime(caminho)
        mtime = os.path.getmtime(caminho)
        ts = min(ctime, mtime)
        dt = datetime.datetime.fromtimestamp(ts)
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return "data desconhecida"


def extrair_texto(caminho: Path) -> str:
    ext = caminho.suffix.lower()
    if ext in {".txt", ".md", ".csv"}:
        try:
            return caminho.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return f"[ERRO AO LER: {e}]"
    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(caminho)
            return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            return f"[ERRO DOCX: {e}]"
    if ext == ".pdf":
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(caminho)
            partes = []
            for pg in reader.pages:
                t = pg.extract_text()
                if t:
                    partes.append(t)
            return "\n".join(partes)
        except Exception as e:
            return f"[ERRO PDF: {e}]"
    if ext == ".doc":
        try:
            import textract
            return textract.process(str(caminho)).decode("utf-8", errors="ignore")
        except Exception as e:
            return f"[ERRO DOC: {e}]"
    return ""


def coletar_arquivos_work_dir(work_dir: Path) -> list[Path]:
    """Retorna arquivos suportados diretamente em WORK_DIR, ordenados por data de criação."""
    arquivos = []
    for caminho in work_dir.iterdir():
        if not caminho.is_file():
            continue
        if caminho.suffix.lower() not in ARQUIVOS_SUPORTADOS:
            continue
        if caminho.parent.name.lower() in PASTAS_IGNORADAS:
            continue
        arquivos.append(caminho)
    arquivos.sort(key=lambda p: os.path.getctime(p))
    return arquivos


def main():
    work_dir = resolver_work_dir()

    pasta_estado  = work_dir / "estado-atual"
    pasta_tmp     = work_dir / "_tmp"
    pasta_tmp.mkdir(exist_ok=True)
    pasta_estado.mkdir(exist_ok=True)

    estado_md     = pasta_estado / "estado-atual.md"
    rastreio_json = pasta_estado / "arquivos-processados.json"
    input_md      = pasta_tmp / "estado-input.md"
    novos_json    = pasta_tmp / "arquivos-novos.json"

    # Carrega lista de arquivos já processados
    if rastreio_json.exists():
        try:
            processados = set(json.loads(rastreio_json.read_text(encoding="utf-8")))
        except Exception:
            processados = set()
    else:
        processados = set()

    # Identifica arquivos novos
    todos = coletar_arquivos_work_dir(work_dir)
    novos = [p for p in todos if p.name not in processados]

    if not novos:
        print("\n[INFO] Nenhum arquivo novo encontrado em WORK_DIR.")
        print("       O estado-atual já está atualizado com todos os arquivos existentes.")
        print("       Para forçar uma re-síntese, apague o estado-atual/arquivos-processados.json.\n")
        sys.exit(0)

    print(f"\n[ESTADO ATUAL] Arquivos já processados: {len(processados)}")
    print(f"[NOVOS]        Arquivos a incorporar:    {len(novos)}")
    for p in novos:
        print(f"  + {p.name}  ({data_criacao(p)})")

    # ── Monta o documento de entrada para a IA ─────────────────────────────
    partes = []

    # Seção 1: estado existente ou marcação de primeira rodada
    if estado_md.exists():
        estado_conteudo = estado_md.read_text(encoding="utf-8").strip()
        partes.append("## ESTADO ATUAL\n\n" + estado_conteudo)
    else:
        partes.append("## ESTADO ATUAL\n\n[PRIMEIRA RODADA — nenhum estado anterior existe]")

    # Seção 2: arquivos novos
    blocos_novos = []
    for caminho in novos:
        texto = extrair_texto(caminho)
        if not texto.strip():
            texto = "[ARQUIVO SEM TEXTO EXTRAÍDO]"
        blocos_novos.append(
            f"### {caminho.name}\n"
            f"**Data:** {data_criacao(caminho)}\n\n"
            f"{texto}"
        )

    partes.append("## ARQUIVOS NOVOS\n\n" + "\n\n---\n\n".join(blocos_novos))

    input_md.write_text("\n\n---\n\n".join(partes), encoding="utf-8")

    # Salva lista de arquivos novos para salvar-estado.py referenciar
    novos_json.write_text(
        json.dumps([p.name for p in novos], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n[OK] Contexto salvo em: {input_md}")
    print(f"[OK] Lista de novos:    {novos_json}")
    print("\n── Próximo passo ────────────────────────────────────────────────────")
    print("1. Leia o prompt em:  habilidades/00.estado-atual.md")
    print(f"2. Use como contexto: {input_md}")
    print("3. Salve a saída da IA em um arquivo temporário")
    print("4. Execute:")
    print(f'   python "<SKILL_DIR>\\scripts\\salvar-estado.py" "{work_dir}" "<arquivo-com-saida>"')
    print("─────────────────────────────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
