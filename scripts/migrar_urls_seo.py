"""Migra os endereços do site para o padrão SEO com o domínio definitivo.
- renomeia pastas (produtos-para-aviacao -> catalogo-pecas-aviacao etc.)
- atualiza links internos, canonical, og:url, dados estruturados (JSON-LD) e mensagens do Joinchat
- atualiza os sitemaps antigos
Pode rodar mais de uma vez: só age sobre os nomes antigos."""
import re, subprocess, urllib.parse
from pathlib import Path
BASE = 'https://www.ftsbrasil.com.br'
root = Path('site')
RENAMES = {  # pasta antiga -> pasta nova (relativas a site/)
    'produtos-para-aviacao': 'catalogo-pecas-aviacao',
    'valvulas': 'catalogo-valvulas',
    'sensores': 'catalogo-sensores',
    '1175-2': 'meio-ambiente',
}
for old, new in RENAMES.items():
    if (root / old).is_dir() and not (root / new).exists():
        subprocess.run(['git', 'mv', str(root / old), str(root / new)], check=True)
OLD = '|'.join(map(re.escape, RENAMES))
def slugs(t):
    t = t.replace('produtos-para-aviacao', RENAMES['produtos-para-aviacao'])
    sub = lambda m: m.group(1) + RENAMES[m.group(2)] + m.group(3)
    # href relativo, URL absoluta e formas do Joinchat (.// e %2F)
    t = re.sub(r'((?:\./|\.\./)+)(valvulas|sensores|1175-2)(/index\.html)', sub, t)
    t = re.sub(r'(\.//|' + re.escape(BASE) + r'/)(valvulas|sensores|1175-2)(/)', sub, t)
    t = re.sub(r'(%2F%2F|%2F)(valvulas|sensores|1175-2)(%2F)', sub, t)
    return t
BASE_ENC = urllib.parse.quote(BASE + '/', safe='')
def pagina(path):
    rel = path.parent.relative_to(root).as_posix()
    return BASE + '/' + ('' if rel == '.' else rel + '/')
def ld(m):  # JSON-LD: "//x" (exportação quebrada) -> URL absoluta
    j = re.sub(r'"//( ?)', '"' + BASE + '/', m.group(2))
    j = j.replace('https://gray-hamster-154972.hostingersite.com', BASE)
    return m.group(1) + j + m.group(3)
n = 0
for p in list(root.rglob('index.html')) + list(root.glob('*sitemap*.xml')):
    if p.parts[1] in ('wp-content', 'wp-includes'): continue
    old = p.read_text(encoding='utf-8')
    t = slugs(old)
    if p.suffix == '.html':
        t = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', ld, t, flags=re.S)
        t = re.sub(r'(?<![\w/.])\.//(?=[\w"\'<\s])', BASE + '/', t)
        t = t.replace('.%2F%2F', BASE_ENC).replace('https%3A%2F%2Fgray-hamster-154972.hostingersite.com', BASE_ENC.rstrip('%2F'))
        url = pagina(p)
        t = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), t)
        t = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), t)
    if t != old:
        p.write_text(t, encoding='utf-8'); n += 1
print('arquivos atualizados:', n)
