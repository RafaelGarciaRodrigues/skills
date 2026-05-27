import json
import sys
from pathlib import Path

if len(sys.argv) < 4:
    print(
        "Uso: python gerar_assessment.py <base.html> <resumo.json> <Assessment.html>"
    )
    sys.exit(1)

base_path = Path(sys.argv[1]).resolve()
json_path = Path(sys.argv[2]).resolve()
output_path = Path(sys.argv[3]).resolve()

base_content = base_path.read_text(encoding="utf-8")
json_content = json_path.read_text(encoding="utf-8")

json_obj = json.loads(json_content)

fluxo_processo = json_obj.get("fluxo-processo", "")

html_content = (
    base_content
    .replace("{##INSIRA_CONTEUDO_JSON##}", json_content)
    .replace("###PSEUDOCODIGO_FLUXO_PROCESSO###", fluxo_processo)
)

output_path.write_text(html_content, encoding="utf-8")

print(f"Assessment.html criado: {output_path}")
print(f"Tamanho: {output_path.stat().st_size} bytes")