"""Corrige os títulos (title, og:title, twitter:title): o WordPress exporta "Página - " (sem nome do site).
Resultado: "Página | FTS Brasil". A home vira "FTS Brasil | Distribuidora de Produtos para o Mercado de Combustíveis".
Idempotente. Uso: python scripts/ajustar_titulos.py"""
import re
from pathlib import Path
MARCA = 'FTS Brasil'
HOME = MARCA + ' | Distribuidora de Produtos para o Mercado de Combustíveis'
n = 0
for p in Path('site').rglob('index.html'):
    if p.parts[1] in ('wp-content', 'wp-includes'): continue
    t = old = p.read_text(encoding='utf-8')
    def fix(m):
        titulo = m.group(2).strip()
        if titulo in ('Home', 'Início'): novo = HOME
        elif titulo == 'Redirecting...': return m.group(0)
        else: novo = f'{titulo} | {MARCA}'
        return m.group(1) + novo + m.group(3)
    t = re.sub(r'(<title>)(.*?) - (</title>)', fix, t)
    t = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")(.*?) - (")', fix, t)
    if t != old: p.write_text(t, encoding='utf-8'); n += 1
print('páginas ajustadas:', n)
