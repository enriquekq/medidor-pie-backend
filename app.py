from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI()

# Permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Servidor funcionando"}

@app.post("/api/detectar_billete")
async def detectar_billete(file: UploadFile = File(...)):
    try:
        save_path = f"static/{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resultado = {
            "estatus": "éxito",
            "billete": "100 pesos",
            "tamaño": "134 mm x 66 mm",
            "archivo": file.filename,
        }
        return JSONResponse(content=resultado)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
