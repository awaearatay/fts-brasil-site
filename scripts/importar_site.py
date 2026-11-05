from pathlib import Path
from PIL import Image
import re, base64, io, hashlib, zipfile, urllib.request
root=Path('site'); root.mkdir(exist_ok=True)
archive=Path('/tmp/fts-original.zip')
urllib.request.urlretrieve('https://gray-hamster-154972.hostingersite.com/wp-content/uploads/simply-static/temp-files/simply-static-1-1793835252.zip',archive)
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='d6c3e3e077e1a549bbe1193b3f7a3d5fa6c96f5963ed89a46d8bb81ab76337b2', 'A exportação original mudou'
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():
        dest=(root/info.filename).resolve()
        assert dest.is_relative_to(root.resolve()), 'Caminho inválido'
    z.extractall(root)
cache={}
pat=re.compile(rb'data:image/(?:png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=\r\n]+)',re.I)
def replace(m):
    data=base64.b64decode(m.group(1)); key=hashlib.sha256(data).digest()
    if key not in cache:
        im=Image.open(io.BytesIO(data)); im.load(); replacement=None
        if not getattr(im,'is_animated',False):
            out=io.BytesIO(); im.save(out,format='WEBP',quality=84,method=5)
            result=b'data:image/webp;base64,'+base64.b64encode(out.getvalue())
            if len(result)<len(m.group(0))*0.95: replacement=result
        cache[key]=replacement
    return cache[key] or m.group(0)
for p in root.rglob('*.html'):
    raw=p.read_bytes(); new=pat.sub(replace,raw)
    if new!=raw:p.write_bytes(new)
for p in root.rglob('*.png'):
    if p.stat().st_size<100000:continue
    im=Image.open(p); im.load()
    if getattr(im,'is_animated',False):continue
    out=io.BytesIO()
    if im.mode in ('RGBA','LA') or 'transparency' in im.info:
        converted=im.convert('RGBA').quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
    else:
        converted=im.convert('RGB').quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    converted.save(out,format='PNG',optimize=True); data=out.getvalue()
    if len(data)<p.stat().st_size*0.9:p.write_bytes(data)
(root/'.nojekyll').touch()
assert (root/'index.html').is_file()
print('Cópia otimizada:',len(list(root.rglob('*'))),'entradas')
