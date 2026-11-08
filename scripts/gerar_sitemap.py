"""Gera site/sitemap.xml e site/robots.txt com URLs absolutas.
Uso: python scripts/gerar_sitemap.py [URL_BASE]
Para outro domínio: python scripts/gerar_sitemap.py https://outrodominio.com.br"""
import re, sys
from datetime import date
from pathlib import Path
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'https://www.ftsbrasil.com.br').rstrip('/')
root = Path('site')
EXTRA = {'catalogo-pecas-aviacao/sistema-deadman': date.today().isoformat()}  # páginas alteradas depois da exportação
urls = {}
for f in ('post-type-page-sitemap-1.xml', 'post-type-post-sitemap-1.xml'):
    xml = (root / f).read_text(encoding='utf-8')
    for loc, lm in re.findall(r'<loc>\./([^<]*)</loc>\s*<lastmod>([^<]*)', xml):
        slug = loc.removesuffix('index.html').strip('/')
        if (root / slug / 'index.html').is_file() or (slug == '' and (root / 'index.html').is_file()):
            urls[slug] = lm[:10]
# páginas novas (fora da lista antiga do WordPress): entram automaticamente, com a data de hoje
SKIP = ('wp-content', 'wp-includes', 'form', 'author', 'category', 'img', 'feed', 'comments')
for p in root.rglob('index.html'):
    slug = p.parent.relative_to(root).as_posix()
    slug = '' if slug == '.' else slug
    if slug.split('/')[0] in SKIP or slug in urls: continue
    urls[slug] = date.today().isoformat()
urls.update({k: v for k, v in EXTRA.items() if k in urls})
def prio(slug):
    if slug == '': return '1.0'
    if slug == 'catalogo-pecas-aviacao': return '0.9'
    if slug.startswith('catalogo-pecas-aviacao/'): return '0.8'
    return '0.6'
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for slug in sorted(urls, key=lambda s: (s != '', s)):
    loc = BASE + '/' + (slug + '/' if slug else '')
    out.append(f'  <url><loc>{loc}</loc><lastmod>{urls[slug]}</lastmod><priority>{prio(slug)}</priority></url>')
out.append('</urlset>')
(root / 'sitemap.xml').write_text('\n'.join(out) + '\n', encoding='utf-8')
(root / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n', encoding='utf-8')
print(len(urls), 'URLs em', BASE)
