# -*- coding: utf-8 -*-

"""
Salva a saída produzida pelo agente em WORK_DIR\\plano\\plano.json.
Valida o JSON e remove o arquivo temporário após salvar.

Uso:
    python "<SKILL_DIR>\\scripts\\salvar-plano.py" "<WORK_DIR>" "<arquivo-com-saida-utf8>"
"""

import os
import json
import sys
from pathlib import Path

os.environ["PYTHONUTF8"] = "1"

ENCODINGS = ("utf-8-sig", "utf-8", "cp850", "cp437", "cp1252", "latin-1")


def resolver_args():
    if len(sys.argv) < 3:
        raise ValueError(
            "Uso: python salvar-plano.py <WORK_DIR> <arquivo-com-saida>"
        )
    return (
        Path(sys.argv[1]).expanduser().resolve(),
        Path(sys.argv[2]).expanduser().resolve(),
    )


def ler_conteudo(caminho):
    for enc in ENCODINGS:
        try:
            return caminho.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return caminho.read_text(encoding="utf-8", errors="replace")


MACRO_ETAPAS_OBRIGATORIAS = [
    "ENTENDER",
    "DIAGNOSTICAR",
    "SIMPLIFICAR",
    "ESTRUTURAR",
    "AUTOMATIZAR",
    "INTERFACE",
    "DOCUMENTAR",
]


def validar_json(conteudo):
    try:
        dados = json.loads(conteudo)
    except json.JSONDecodeError as e:
        raise ValueError(f"Conteúdo não é um JSON válido: {e}")

    if "plano" not in dados or not isinstance(dados["plano"], list):
        raise ValueError("JSON inválido: campo 'plano' ausente ou não é uma lista.")

    macros_recebidas = [m.get("macro_etapa", "") for m in dados["plano"]]

    if macros_recebidas != MACRO_ETAPAS_OBRIGATORIAS:
        raise ValueError(
            f"O plano deve conter exatamente as 7 macro-etapas na ordem correta.\n"
            f"Esperado: {MACRO_ETAPAS_OBRIGATORIAS}\n"
            f"Recebido: {macros_recebidas}"
        )

    for i, macro in enumerate(dados["plano"]):
        for campo in ("macro_etapa", "objetivo", "etapas"):
            if campo not in macro:
                raise ValueError(
                    f"macro_etapa[{i}] sem campo obrigatório '{campo}'."
                )
        for j, etapa in enumerate(macro.get("etapas", [])):
            for campo in ("atividade", "concluido", "responsavel", "prioridade", "inicio", "fim"):
                if campo not in etapa:
                    raise ValueError(
                        f"macro_etapa[{i}].etapas[{j}] sem campo '{campo}'."
                    )
            inicio = etapa.get("inicio")
            fim    = etapa.get("fim")
            if not isinstance(inicio, int) or not isinstance(fim, int):
                raise ValueError(
                    f"macro_etapa[{i}].etapas[{j}]: 'inicio' e 'fim' devem ser inteiros."
                )
            if fim < inicio:
                raise ValueError(
                    f"macro_etapa[{i}].etapas[{j}]: 'fim' ({fim}) < 'inicio' ({inicio})."
                )

    return json.dumps(dados, ensure_ascii=False, indent=2)


def main():
    work_dir, arquivo_temp = resolver_args()
    conteudo = ler_conteudo(arquivo_temp)
    conteudo_validado = validar_json(conteudo)

    pasta_saida = work_dir / "plano"
    pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivo_saida = pasta_saida / "plano.json"
    arquivo_saida.write_text(conteudo_validado, encoding="utf-8")
    print(f"Plano salvo em: {arquivo_saida}")

    try:
        arquivo_temp.unlink()
        print(f"Arquivo temporário removido: {arquivo_temp}")
    except Exception as e:
        print(f"Aviso: não foi possível remover o arquivo temporário: {e}")


if __name__ == "__main__":
    main()
