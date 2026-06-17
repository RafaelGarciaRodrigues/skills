# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente em WORK_DIR\\convergir\\convergir.json.

Novo formato: JSON com três seções (verde, laranja, vermelho), cada uma
contendo uma lista de itens de escopo classificados por nível de confiança.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-convergencia.py" "<WORK_DIR>" "<arquivo-com-saida-utf8>"
"""

import os
import json
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")

CHAVES_OBRIGATORIAS = {"verde", "laranja", "vermelho", "comentario"}
CHAVES_ITEM_VERDE   = {"id", "titulo", "categoria", "contexto", "motivo_classificacao", "premissa_operacional", "fonte"}
CHAVES_ITEM_LARANJA = {"id", "titulo", "categoria", "contexto", "motivo_classificacao", "versao_simples", "versao_completa", "pergunta_ao_negocio", "fonte"}
CHAVES_ITEM_VERMELHO = {"id", "titulo", "categoria", "contexto", "motivo_classificacao", "acao_recomendada", "fonte"}


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


def validar_estrutura(dados):
    """
    Valida a estrutura do JSON de convergência no novo formato (verde/laranja/vermelho).
    Retorna lista de avisos (não críticos) e lança ValueError para erros críticos.
    """
    avisos = []

    # Chaves de topo
    faltando = CHAVES_OBRIGATORIAS - set(dados.keys())
    if faltando:
        raise ValueError(f"Chaves obrigatórias ausentes no JSON: {faltando}")

    # Verde
    verde = dados.get("verde", {})
    if not isinstance(verde.get("itens"), list) or len(verde["itens"]) == 0:
        avisos.append("  AVISO: verde.itens está vazio ou ausente.")
    else:
        for i, item in enumerate(verde["itens"]):
            falt = CHAVES_ITEM_VERDE - set(item.keys())
            if falt:
                avisos.append(f"  AVISO: item verde[{i}] faltando campos: {falt}")

    if not verde.get("custo_estimado"):
        avisos.append("  AVISO: verde.custo_estimado não informado.")

    # Laranja
    laranja = dados.get("laranja", {})
    if not isinstance(laranja.get("itens"), list) or len(laranja["itens"]) == 0:
        avisos.append("  AVISO: laranja.itens está vazio ou ausente.")
    else:
        for i, item in enumerate(laranja["itens"]):
            falt = CHAVES_ITEM_LARANJA - set(item.keys())
            if falt:
                avisos.append(f"  AVISO: item laranja[{i}] faltando campos: {falt}")

    if not laranja.get("custo_faixa_min") or not laranja.get("custo_faixa_max"):
        avisos.append("  AVISO: laranja.custo_faixa_min ou custo_faixa_max não informados.")
    elif laranja.get("custo_faixa_min", 0) > laranja.get("custo_faixa_max", 0):
        avisos.append("  AVISO: laranja.custo_faixa_min > custo_faixa_max — verifique os valores.")

    # Vermelho
    vermelho = dados.get("vermelho", {})
    if not isinstance(vermelho.get("itens"), list) or len(vermelho["itens"]) == 0:
        avisos.append("  AVISO: vermelho.itens está vazio ou ausente.")
    else:
        for i, item in enumerate(vermelho["itens"]):
            falt = CHAVES_ITEM_VERMELHO - set(item.keys())
            if falt:
                avisos.append(f"  AVISO: item vermelho[{i}] faltando campos: {falt}")

    # IDs únicos entre todas as categorias
    todos_ids = (
        [i.get("id") for i in verde.get("itens", [])] +
        [i.get("id") for i in laranja.get("itens", [])] +
        [i.get("id") for i in vermelho.get("itens", [])]
    )
    ids_duplicados = {x for x in todos_ids if todos_ids.count(x) > 1}
    if ids_duplicados:
        avisos.append(f"  AVISO: IDs duplicados entre categorias: {ids_duplicados}")

    # Resumo de contagem
    n_verde   = len(verde.get("itens", []))
    n_laranja = len(laranja.get("itens", []))
    n_vermelho = len(vermelho.get("itens", []))
    print(f"Itens classificados: {n_verde} verde | {n_laranja} laranja | {n_vermelho} vermelho")

    return avisos


def main():
    work_dir = resolver_work_dir()
    arquivo_temp = Path(sys.argv[2]).expanduser().resolve()
    conteudo = ler_conteudo()

    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as e:
        raise ValueError(f"Conteúdo não é um JSON válido: {e}")

    avisos = validar_estrutura(dados)

    if avisos:
        print("Avisos encontrados:")
        for a in avisos:
            print(a)
    else:
        print("Estrutura validada. Nenhum aviso.")

    pasta_saida = work_dir / "convergir"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivo_saida = pasta_saida / "convergir.json"
    arquivo_saida.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Convergência salva em: {arquivo_saida}")

    try:
        arquivo_temp.unlink()
        print(f"Arquivo temporário removido: {arquivo_temp}")
    except Exception as e:
        print(f"Aviso: não foi possível remover o arquivo temporário: {e}")


if __name__ == "__main__":
    main()
