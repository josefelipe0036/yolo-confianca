# A "confiança" do YOLO é uma probabilidade?

Rodei o YOLO26n (Ultralytics 8.4, CPU) numa foto da Rodoviária do Plano Piloto, em Brasília, e testei como o score de confiança reage a pequenas mudanças na mesma imagem.

| Versão | Conf. do ônibus | Objetos ≥ 0,25 | Objetos ≥ 0,5 |
|---|---|---|---|
| Original | 0,862 | 20 | 14 |
| Resolução 1280 | 0,925 | 45 | 28 |
| 10% mais clara | 0,859 | 20 | 14 |
| Espelhada | 0,836 | 22 | 15 |
| JPEG comprimido | 0,858 | 20 | 13 |

Uma foto só não mede calibração. Para isso é preciso uma curva de confiabilidade feita com milhares de imagens rotuladas.

## Como rodar
```bash
pip install ultralytics
python detectar.py yolo26n.pt fotos/eixao.jpg
python estabilidade.py
python anotar.py
```

Foto: "Rodoviária do Plano Piloto e o Eixão", de victoria.camara / Portal da Copa 2014, CC BY 3.0, via Wikimedia Commons. A imagem anotada (`eixao_anotada.jpg`) é uma obra derivada sob a mesma licença.
