# A mesma foto, pequenas alterações: a "confiança" do YOLO muda?
import json
from PIL import Image, ImageEnhance, ImageOps
from ultralytics import YOLO

modelo = YOLO("yolo26n.pt")
orig = Image.open("fotos/eixao.jpg").convert("RGB")

def variantes():
    yield "original", orig, 640
    yield "resolução maior (1280)", orig, 1280
    yield "10% mais claro", ImageEnhance.Brightness(orig).enhance(1.10), 640
    yield "espelhada", ImageOps.mirror(orig), 640
    orig.save("/tmp/q30.jpg", quality=30); yield "JPEG comprimido", Image.open("/tmp/q30.jpg").convert("RGB"), 640

def iou(a, b):
    x1, y1, x2, y2 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    i = max(0, x2 - x1) * max(0, y2 - y1)
    return i / ((a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - i)

W = orig.width
ref = None
res = []
for nome, img, tam in variantes():
    r = modelo.predict(img, conf=0.05, imgsz=tam, verbose=False)[0]
    dets = [(r.names[int(c)], float(p), [float(v) for v in b]) for b, p, c in zip(r.boxes.xyxy, r.boxes.conf, r.boxes.cls)]
    if nome == "espelhada":   # desespelha as caixas para comparar
        dets = [(c, p, [W - b[2], b[1], W - b[0], b[3]]) for c, p, b in dets]
    if ref is None:
        ref = sorted([d for d in dets if d[0] == "bus"], key=lambda d: -d[1])[0]   # o ônibus mais confiante
    match = max([d for d in dets if d[0] == "bus"], key=lambda d: iou(d[2], ref[2]), default=None)
    conf_bus = match[1] if match and iou(match[2], ref[2]) > 0.5 else None
    n = {t: sum(p >= t for _, p, _ in dets) for t in (0.25, 0.5)}
    res.append({"variante": nome, "conf_onibus": conf_bus, "n_025": n[0.25], "n_050": n[0.5]})
    print(f"{nome:<24} ônibus: {conf_bus if conf_bus is None else round(conf_bus,3)}   objetos conf>=0.25: {n[0.25]:2d}   conf>=0.5: {n[0.5]:2d}")
json.dump({"onibus_ref_caixa": ref[2], "variantes": res}, open("estabilidade.json", "w"), indent=1)
