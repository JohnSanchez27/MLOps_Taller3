import os
import joblib
import json

def cargar_modelos():
    print("Ingresando a la carga de modelos...")
    modelos = {}
    try:
        models_dir = os.path.dirname(os.path.abspath(__file__))
        print("Directorio del script:", models_dir)
        
        modelo_path = os.path.join(models_dir, "datos", "SVM_model.pkl")
        print("Intentando cargar el modelo desde:", modelo_path)

        if not os.path.exists(modelo_path):
            print(f"⚠️ ERROR: El archivo {modelo_path} NO EXISTE.")
            return None  # Retorna None si el archivo no existe
        
        # Intentar cargar el modelo
        modelos["modelo1"] = joblib.load(modelo_path)
        
        print("✅ Modelo cargado exitosamente.")
        return modelos

    except FileNotFoundError as e:
        print(f"🚨 Error: No se encontró el archivo {modelo_path}. Detalles: {e}")
        return None
    except Exception as e:
        print(f"🚨 Error al cargar los modelos: {e}")
        return None
