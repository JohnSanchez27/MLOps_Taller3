from typing import Union
import joblib
from fastapi import FastAPI
from cargar_modelos import cargar_modelos
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()
modelos= cargar_modelos()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes, restringe en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

class Pinguino(BaseModel):
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    delta_15_n: float
    delta_13_c: float
    sex: str

@app.post("/pinguino")
def postPinguino(pinguino: Pinguino):
    print("//"*32)
    print("modelo1 ",modelos['modelo1'])
    print(pinguino)
    print("//"*32)
    # Crear DataFrame con la fila de datos a predecir
    X_new = pd.DataFrame([{
        "Culmen Length (mm)":pinguino.culmen_length_mm,
        "Culmen Depth (mm)": pinguino.culmen_depth_mm,
        "Flipper Length (mm)": pinguino.flipper_length_mm,
        "Body Mass (g)":pinguino.body_mass_g,
        "Delta 15 N (o/oo)":pinguino.delta_15_n,
        "Delta 13 C (o/oo)":pinguino.delta_13_c,
        "Sex": pinguino.sex
    }])

    # Realizar la predicción
    prediccion = modelos["modelo1"].predict(X_new)

    # Convertir la predicción en un formato JSON serializable
    return {"message": "Predicción realizada", "prediccion": prediccion.tolist()}

    




