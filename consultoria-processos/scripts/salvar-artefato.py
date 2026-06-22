# -*- coding: utf-8 -*-

"""
Salva a saida produzida pelo agente na pasta artefatos do WORK_DIR.

Uso com arquivo de entrada:
    python "<SKILL_DIR>\\scripts\\salvar-artefato.py" "<WORK_DIR>" "nome-habilidade.json" "<arquivo-com-saida-utf8>"

Saida:
    - Cria/atualiza "<WORK_DIR>\\artefatos\\nome-habilidade.json"
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
    if len(sys.argv) < 3:
        raise ValueError(
            "Uso: python salvar-artefato.py <WORK_DIR> <nome_habilidade> [arquivo_conteudo]"
        )

    return Path(sys.argv[1]).expanduser().resolve()


def resolver_nome_habilidade():
    nome = Path(sys.argv[2]).name

    if not nome:
        raise ValueError("Nome da habilidade nao informado.")

    return nome


def decodificar_texto(dados):
    for encoding in ENCODINGS_SUPORTADOS:
        try:
            return dados.decode(encoding)
        except UnicodeDecodeError:
            continue

    return dados.decode("utf-8", errors="replace")


def ler_conteudo():
    if len(sys.argv) > 3:
        caminho_conteudo = Path(sys.argv[3]).expanduser().resolve()
        return decodificar_texto(caminho_conteudo.read_bytes())

    raise ValueError(
        "Informe um arquivo de conteudo UTF-8. Entrada via stdin foi removida "
        "porque pode corromper acentos no Windows."
    )


def validar_conteudo(conteudo, eh_json):
    if PADRAO_PERDA_ACENTO.search(conteudo):
        raise ValueError(
            "Possivel perda de acentuacao detectada no conteudo. "
            "Exemplo comum: 'reuni?o' em vez de 'reunião'. "
            "Regere a saida em UTF-8 antes de salvar o artefato."
        )

    if eh_json:
        try:
            dados = json.loads(conteudo)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Conteudo nao e um JSON valido: {e}\n"
                "Verifique se o agente gerou JSON puro, sem blocos de codigo markdown."
            )

        if not isinstance(dados, dict):
            raise ValueError(
                "O JSON deve ser um objeto (dict) com a chave da habilidade. "
                f"Recebido: {type(dados).__name__}"
            )

        return dados

    return conteudo


def envolver_se_necessario(dados: dict, nome_arquivo: str) -> dict:
    """
    Se o JSON não tiver a chave esperada (stem do arquivo) como única chave raiz,
    envolve automaticamente sob essa chave.

    Exemplo: salvar-artefato.py recebe '14.mapa-processo.json' com conteúdo
    {"processo": [...], "entrega": {...}}. A chave esperada é "14.mapa-processo".
    Como ela não existe no JSON, o conteúdo é envolvido:
    {"14.mapa-processo": {"processo": [...], "entrega": {...}}}

    Não envolve se a chave esperada já for a única chave raiz (comportamento padrão
    das outras habilidades que já envolvem corretamente).
    """
    chave_esperada = Path(nome_arquivo).stem  # "14.mapa-processo" a partir de "14.mapa-processo.json"

    if chave_esperada in dados:
        return dados  # já está no formato correto

    # A IA gerou o conteúdo sem o wrapper — envolve automaticamente
    print(f"[INFO] Chave '{chave_esperada}' ausente no JSON raiz. Envolvendo automaticamente.")
    return {chave_esperada: dados}


def main():
    work_dir = resolver_work_dir()
    nome_habilidade = resolver_nome_habilidade()
    conteudo_raw = ler_conteudo()

    eh_json = nome_habilidade.lower().endswith(".json")
    dados = validar_conteudo(conteudo_raw, eh_json)

    artefatos_dir = work_dir / "artefatos"
    artefatos_dir.mkdir(parents=True, exist_ok=True)

    arquivo_saida = artefatos_dir / nome_habilidade

    if eh_json:
        dados = envolver_se_necessario(dados, nome_habilidade)
        arquivo_saida.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    else:
        arquivo_saida.write_text(conteudo_raw, encoding="utf-8")

    print(f"Artefato salvo em: {arquivo_saida}")


if __name__ == "__main__":
    main()
