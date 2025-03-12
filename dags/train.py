import joblib
import numpy as np
import pandas as pd
from airflow import DAG
from sklearn.svm import SVC
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split
from airflow.operators.python_operator import PythonOperator
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sqlalchemy import create_engine
import json

# Configuración de parámetros por defecto del DAG de Airflow
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 10),
}

# Función para entrenar el modelo SVM
def train_model():
    # Conexión a la base de datos MySQL
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Consulta para cargar los datos desde la tabla en la base de datos
    query = "SELECT * FROM penguins"
    
    # Leer los datos desde MySQL
    penguins = pd.read_sql(query, con=engine)

    # Eliminar columnas irrelevantes o no necesarias
    penguins.drop(['studyName','Sample Number','Region','Island','Stage','Individual ID','Clutch Completion',
                   'Date Egg', 'Comments'], axis=1, inplace=True)

    # Reemplazar valores '.' por NaN para manejo de datos faltantes
    penguins.replace(".", np.nan, inplace=True)

    # Convertir columnas categóricas a tipo "category"
    penguins[['Sex', 'Species']] = penguins[['Sex', 'Species']].astype('category')

    # Dividir los datos en características (X) y variable objetivo (y)
    X = penguins.drop(columns='Species')
    y = penguins['Species']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=54)

    # Definir transformaciones para columnas numéricas
    numeric_transformer = Pipeline(steps=[
        ("imputer", KNNImputer(n_neighbors=15)), 
        ("scaler", StandardScaler())
    ])

    # Definir transformaciones para columnas categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent', missing_values=np.nan)),
        ('onehot', OneHotEncoder(drop='first'))
    ])

    # Combinación de transformadores en un preprocesador
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, X.select_dtypes(exclude="category").columns),
        ("cat", categorical_transformer, X.select_dtypes(include="category").columns)
    ])

    # Definir el modelo SVM dentro de un pipeline
    clf = Pipeline(steps=[
        ("preprocessor", preprocessor), 
        ("SVM", SVC())
    ])

    # Separación de columnas numéricas/categóricas
    numeric_cols = X.select_dtypes(exclude="category").columns
    cat_cols = X.select_dtypes(include="category").columns


    # Entrenar el modelo SVM
    clf.fit(X_train, y_train)

    # Guardar el modelo entrenado en un archivo .joblib
    joblib.dump(clf, '/opt/airflow/datos/SVM_model.pkl')
    
    schema_info = {
        "numeric_features": list(numeric_cols),
        "categorical_features": list(cat_cols)
    }

    # Guardar el esquema como JSON
    with open('/opt/airflow/datos/SVM_model_schema.json', 'w') as f:
        json.dump(schema_info, f)
        

# Crear el DAG para el entrenamiento del modelo SVM
dag = DAG('training', default_args=default_args, schedule_interval=None)

# Tarea para entrenar el modelo SVM
train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)
