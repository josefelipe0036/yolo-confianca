# Roda o YOLO numa foto e lista cada detecção com seu score de confiança
import sys, json
from ultralytics import YOLO

modelo = YOLO(sys.argv[1])
saida = {}
for foto in sys.argv[2:]:
    r = modelo.predict(foto, conf=0.05, verbose=False)[0]
    dets = [{"classe": r.names[int(c)], "conf": round(float(p), 3), "caixa": [round(float(v)) for v in b]}
            for b, p, c in zip(r.boxes.xyxy, r.boxes.conf, r.boxes.cls)]
    saida[foto] = dets
    acima = [d for d in dets if d["conf"] >= 0.25]
    print(f"{foto}: {len(acima)} detecções com conf >= 0.25, {len(dets)} com conf >= 0.05")
    for d in sorted(acima, key=lambda d: -d["conf"]):
        print(f"   {d['classe']:<14} {d['conf']:.3f}")
json.dump(saida, open("deteccoes.json", "w"), indent=1)
