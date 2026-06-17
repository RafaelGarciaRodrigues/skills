from pathlib import Path

p = list(Path(r'C:\Users\cs385499\OneDrive - MinhaTI\Documentos').rglob('Analise.html'))[2].parent.parent
print('WORK_DIR:', p)

checks = {
    'dimensionamento/dimensionamento.json': None,
    'convergir/convergir.json': None,
    'plano/plano.json': None,
}
for rel, _ in checks.items():
    f = p / rel
    checks[rel] = f.exists()
    print(f'  {rel}: {"EXISTE" if f.exists() else "nao existe"}')
