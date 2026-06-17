import re
from pathlib import Path

html = Path(r'c:\Users\cs385499\.claude\skills\consultoria-processos\html\relatorio-modelo.html').read_text(encoding='utf-8', errors='replace')

ids = re.findall(r'id="([^"]+)"', html)
secoes = [i for i in ids if any(c.isdigit() for c in i) or i in [
    'Especificacao','Analise-Especificacao','plano-especificacao',
    'dimensionamento-especificacao','convergencia-especificacao','maturidade-especificacao'
]]
print('Tamanho HTML:', len(html))
print('Secoes encontradas:')
for s in secoes[:40]:
    print(' ', s)

# Checar secoes esperadas
esperadas = [
    '1.resumo-conversa','2.problema-central','3.titulo','4.necessidades',
    '5.requisitos','6.mapa-mental','7.numeros','8.temas-abertos',
    '9.contradicoes','10.maturidade','11.maturidade-qualitativa','12.participantes',
    'plano-especificacao','dimensionamento-especificacao','convergencia-especificacao'
]
print('\nVerificacao:')
for e in esperadas:
    print(' ', e, '->', 'OK' if e in html else 'FALTANDO')
