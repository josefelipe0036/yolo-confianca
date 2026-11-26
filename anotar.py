# Desenha as caixas (conf >= 0.25) no estilo da identidade DADO CRU
import json
from PIL import Image, ImageDraw, ImageFont
det = json.load(open("deteccoes.json"))["fotos/eixao.jpg"]
img = Image.open("fotos/eixao.jpg").convert("RGB")
d = ImageDraw.Draw(img)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 22)
except OSError: f = ImageFont.load_default()
top = max(det, key=lambda x: x["conf"])
for x in sorted([x for x in det if x["conf"] >= 0.25], key=lambda x: x["conf"]):
    cor = (255, 74, 28) if x is top else (11, 11, 11)
    x1, y1, x2, y2 = x["caixa"]
    d.rectangle([x1, y1, x2, y2], outline=cor, width=5 if x is top else 3)
    txt = f"{x['classe']} {x['conf']:.2f}"
    w = d.textlength(txt, font=f)
    d.rectangle([x1, y1 - 28, x1 + w + 10, y1], fill=cor)
    d.text((x1 + 5, y1 - 27), txt, fill=(255, 255, 255) if x is not top else (11, 11, 11), font=f)
img.save("eixao_anotada.jpg", quality=92)
print("ok", top)
