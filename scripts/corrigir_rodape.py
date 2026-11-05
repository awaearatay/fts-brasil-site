from pathlib import Path
import os,re
root=Path("site")
icons={"facebook":"<rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#1877f2\"/><path fill=\"#fff\" d=\"M28 44V27h6l1-7h-7v-4c0-2 1-3 3-3h4V7h-6c-6 0-10 4-10 10v3h-5v7h5v17z\"/>","instagram":"<rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#c13584\"/><rect x=\"10\" y=\"10\" width=\"28\" height=\"28\" rx=\"8\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\"/><circle cx=\"24\" cy=\"24\" r=\"7\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\"/><circle cx=\"33\" cy=\"15\" r=\"2\" fill=\"#fff\"/>","linkedin":"<rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#0a66c2\"/><circle cx=\"13\" cy=\"14\" r=\"3\" fill=\"#fff\"/><path fill=\"#fff\" d=\"M10 20h6v18h-6zm10 0h6v2c2-3 5-3 7-2 4 1 5 4 5 8v10h-6V28c0-3-1-4-3-4s-3 2-3 4v10h-6z\"/>","whatsapp":"<rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#128c4a\"/><path d=\"M12 36l2-7a14 14 0 1 1 6 7z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2.5\" stroke-linejoin=\"round\"/><path d=\"M19 16c-2 0-3 2-2 5 2 6 6 10 12 12 3 1 5-1 5-3l-5-3-2 2c-3-1-6-4-7-7l2-2z\" fill=\"#fff\" transform=\"translate(-1 -2)\"/>","youtube":"<rect width=\"48\" height=\"48\" rx=\"12\" fill=\"#e62117\"/><rect x=\"7\" y=\"13\" width=\"34\" height=\"23\" rx=\"7\" fill=\"#fff\"/><path d=\"M21 19l11 6-11 6z\" fill=\"#e62117\"/>"}
directory=root/"img/site/home"
directory.mkdir(parents=True,exist_ok=True)
for name,shapes in icons.items():
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">'+shapes+'</svg>\n'
    (directory/(name+".svg")).write_text(svg,encoding="utf-8")
changed=0
for p in root.rglob("*.html"):
    old=p.read_text(encoding="utf-8")
    text=old
    for name in icons:
        text=text.replace("img/site/home/"+name+".png","img/site/home/"+name+".svg")
    home=os.path.relpath(root/"index.html",p.parent).replace(os.sep,"/")
    def logo(match):
        tag=match.group(0)
        if re.search(r'aria-label=["\']FTS Brasil["\']',tag,re.I):
            return re.sub(r'href=(["\']).*?\1','href="'+home+'"',tag,count=1,flags=re.I)
        if re.search(r'aria-label=["\']Facebook FTS Brasil["\']',tag,re.I):
            tag=re.sub(r'\s+(?:target|rel|referrerpolicy)=(["\']).*?\1',"",tag,flags=re.I)
            return tag[:-1]+' target="_self" rel="noreferrer" referrerpolicy="no-referrer">'
        return tag
    text=re.sub(r'<a\b[^>]*>',logo,text,flags=re.I)
    if text!=old:
        p.write_text(text,encoding="utf-8");changed+=1
print("Páginas corrigidas:",changed)
