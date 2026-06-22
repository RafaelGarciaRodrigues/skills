# -*- coding: utf-8 -*-

"""
Salva a saída da IA do estado-atual em WORK_DIR/estado-atual/.

Espera que o arquivo de saída da IA contenha dois blocos
separados pela linha exata: ---DUVIDAS---

Bloco 1 → estado-atual.md
Bloco 2 → lista-duvidas.md

Também atualiza WORK_DIR/estado-atual/arquivos-processados.json
com os arquivos listados em WORK_DIR/_tmp/arquivos-novos.json.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-estado.py" "<WORK_DIR>" "<arquivo-com-saida>"
"""

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

DELIMITADOR = "---DUVIDAS---"


def main():
    if len(sys.argv) < 3:
        print("Uso: python salvar-estado.py <WORK_DIR> <arquivo-com-saida>")
        sys.exit(1)

    work_dir    = Path(sys.argv[1]).expanduser().resolve()
    arquivo_ia  = Path(sys.argv[2]).expanduser().resolve()

    pasta_estado  = work_dir / "estado-atual"
    pasta_tmp     = work_dir / "_tmp"
    estado_md     = pasta_estado / "estado-atual.md"
    duvidas_md    = pasta_estado / "lista-duvidas.md"
    rastreio_json = pasta_estado / "arquivos-processados.json"
    novos_json    = pasta_tmp    / "arquivos-novos.json"
    input_md      = pasta_tmp    / "estado-input.md"

    if not arquivo_ia.exists():
        print(f"[ERRO] Arquivo não encontrado: {arquivo_ia}")
        sys.exit(1)

    conteudo = arquivo_ia.read_text(encoding="utf-8")

    # ── Divide nos dois blocos ─────────────────────────────────────────────
    if DELIMITADOR not in conteudo:
        print(f"[ERRO] O arquivo não contém o delimitador '{DELIMITADOR}'.")
        print("       Verifique se a IA seguiu o formato especificado em 00.estado-atual.md.")
        sys.exit(1)

    idx = conteudo.index(DELIMITADOR)
    bloco_estado  = conteudo[:idx].strip()
    bloco_duvidas = conteudo[idx + len(DELIMITADOR):].strip()

    if not bloco_estado:
        print("[ERRO] Bloco do estado-atual está vazio.")
        sys.exit(1)

    pasta_estado.mkdir(exist_ok=True)

    # ── Salva arquivos ─────────────────────────────────────────────────────
    estado_md.write_text(bloco_estado, encoding="utf-8")
    print(f"[OK] estado-atual.md salvo em: {estado_md}")

    if bloco_duvidas:
        duvidas_md.write_text(bloco_duvidas, encoding="utf-8")
        print(f"[OK] lista-duvidas.md salvo em: {duvidas_md}")
    else:
        print("[AVISO] Bloco de dúvidas vazio — lista-duvidas.md não foi criado.")

    # ── Atualiza rastreio de arquivos processados ──────────────────────────
    if novos_json.exists():
        try:
            novos = json.loads(novos_json.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[AVISO] Falha ao ler arquivos-novos.json: {e}")
            novos = []

        if rastreio_json.exists():
            try:
                processados = json.loads(rastreio_json.read_text(encoding="utf-8"))
                if not isinstance(processados, list):
                    processados = []
            except Exception:
                processados = []
        else:
            processados = []

        # Adiciona novos sem duplicar
        for nome in novos:
            if nome not in processados:
                processados.append(nome)

        rastreio_json.write_text(
            json.dumps(processados, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] arquivos-processados.json atualizado ({len(processados)} arquivos no total)")
    else:
        print("[AVISO] arquivos-novos.json não encontrado em _tmp — rastreio não atualizado.")

    # ── Limpa temporários ──────────────────────────────────────────────────
    for tmp in [arquivo_ia, novos_json, input_md]:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass

    print("\n[CONCLUÍDO] Estado-atual atualizado com sucesso.")
    print("            Os modelos analíticos (ex: 10.maturidade) lerão estado-atual.md.")


if __name__ == "__main__":
    main()
