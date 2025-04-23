from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import os
import gdown

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta local del modelo y enlace de Google Drive
MODEL_PATH = "modelos/best.pt"
DRIVE_ID = "TU_ID_DE_GOOGLE_DRIVE"  # 👈 Reemplaza esto con tu ID real

# Descargar modelo desde Google Drive si no existe
os.makedirs("modelos", exist_ok=True)
if not os.path.exists(MODEL_PATH):
    url = f"https://drive.google.com/uc?id={DRIVE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

# Cargar modelo
modelo = YOLO(MODEL_PATH)

@app.get("/")
def read_root():
    return {"mensaje": "API del medidor de pie activo."}

@app.post("/api/detectar_billete")
async def detectar_billete(file: UploadFile = File(...)):
    contents = await file.read()
    path = f"static/{file.filename}"
    os.makedirs("static", exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)

    # Predicción
    resultados = modelo(path)[0]
    clases = resultados.names
    cajas = resultados.boxes

    return {
        "clases": [clases[int(c.item())] for c in cajas.cls],
        "confianzas": [float(c.item()) for c in cajas.conf]
    }
