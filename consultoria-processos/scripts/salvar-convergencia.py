# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente em WORK_DIR\\convergir\\convergir.json.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-convergencia.py" "<WORK_DIR>" "<arquivo-com-saida-utf8>"
"""

import os
import json
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")


def resolver_work_dir():
    if len(sys.argv) < 3:
        raise ValueError(
            "Uso: python salvar-convergencia.py <WORK_DIR> <arquivo-com-saida>"
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


def validar_e_corrigir(conteudo):
    """
    Valida e corrige os campos calculáveis do JSON de convergência:
      - reducao_total      = custo_baseline - custo_simplificado
      - percentual_reducao = round(reducao_total / custo_baseline * 100)

    Retorna o JSON já corrigido como string.
    """
    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as e:
        raise ValueError(f"Conteúdo não é um JSON válido: {e}")

    baseline      = int(dados.get("custo_baseline", 0) or 0)
    simplificado  = int(dados.get("custo_simplificado", 0) or 0)
    reducao_orig  = int(dados.get("reducao_total", 0) or 0)
    pct_orig      = int(dados.get("percentual_reducao", 0) or 0)

    reducao_correto = baseline - simplificado
    pct_correto     = round(reducao_correto / baseline * 100) if baseline else 0

    avisos = []

    if reducao_orig != reducao_correto:
        avisos.append(
            f"  reducao_total: agente informou {reducao_orig:,} → corrigido para {reducao_correto:,}"
        )
        dados["reducao_total"] = reducao_correto

    if pct_orig != pct_correto:
        avisos.append(
            f"  percentual_reducao: agente informou {pct_orig}% → corrigido para {pct_correto}%"
        )
        dados["percentual_reducao"] = pct_correto

    # Soma das reduções individuais vs reducao_total — apenas aviso informativo
    soma_itens = sum(int(s.get("custo_reducao", 0) or 0) for s in dados.get("simplificacoes", []))
    if soma_itens != reducao_correto:
        avisos.append(
            f"  ATENÇÃO: soma de custo_reducao das simplificações ({soma_itens:,}) "
            f"≠ reducao_total ({reducao_correto:,}). "
            f"Isso pode indicar efeito composição ou erro do agente — verifique o campo 'comentario'."
        )

    if avisos:
        print("Correções aplicadas no JSON:")
        for a in avisos:
            print(a)
    else:
        print("Valores calculados consistentes. Nenhuma correção necessária.")

    return json.dumps(dados, ensure_ascii=False, indent=2)


def main():
    work_dir = resolver_work_dir()
    arquivo_temp = Path(sys.argv[2]).expanduser().resolve()
    conteudo = ler_conteudo()

    conteudo_corrigido = validar_e_corrigir(conteudo)

    pasta_saida = work_dir / "convergir"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivo_saida = pasta_saida / "convergir.json"
    arquivo_saida.write_text(conteudo_corrigido, encoding="utf-8")

    print(f"Convergência salva em: {arquivo_saida}")

    try:
        arquivo_temp.unlink()
        print(f"Arquivo temporário removido: {arquivo_temp}")
    except Exception as e:
        print(f"Aviso: não foi possível remover o arquivo temporário: {e}")


if __name__ == "__main__":
    main()
