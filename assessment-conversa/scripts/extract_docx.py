from docx import Document
import sys

if len(sys.argv) < 3:
    print("Uso: python extract_docx.py entrada.docx saida.txt")
    sys.exit(1)

entrada = sys.argv[1]
saida = sys.argv[2]

doc = Document(entrada)

texto = "\n".join(p.text for p in doc.paragraphs)

with open(saida, "w", encoding="utf-8") as f:
    f.write(texto)

print(f"OK: {len(texto)} caracteres")