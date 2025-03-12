from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine, inspect

# Configuración de argumentos por defecto para el DAG
default_args = {
    'owner': 'airflow',  # Propietario del DAG
    'depends_on_past': False,  # Indica que las tareas no dependen de ejecuciones pasadas
    'start_date': datetime(2025, 3, 10)  # Fecha de inicio fija
}

def delete_data():
    """
    Función para eliminar los datos de la tabla 'penguins' en la base de datos MySQL.
    Verifica si la tabla existe antes de intentar eliminar su contenido.
    """
    # Crear la conexión a la base de datos MySQL usando SQLAlchemy
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Crear un inspector para verificar la existencia de la tabla
    inspector = inspect(engine)

    # Verificar si la tabla 'penguins' existe en la base de datos
    if 'penguins' in inspector.get_table_names():
        # Eliminar todos los registros de la tabla 'penguins'
        engine.execute("DELETE FROM penguins")
        print("Contenido de la tabla 'penguins' eliminado exitosamente.")
    else:
        print("La tabla 'penguins' no existe en la base de datos.")

# Definición del DAG para la eliminación de datos
with DAG(
    dag_id='delete_data',  # Identificador único del DAG
    default_args=default_args,  # Argumentos por defecto definidos anteriormente
    description='DAG para borrar contenido de la base de datos',
    schedule_interval=None,  # Ejecución manual del DAG
) as dag:

    # Definición de la tarea para ejecutar la función delete_data
    delete_task = PythonOperator(
        task_id='delete_data_task',  # Identificador único de la tarea
        python_callable=delete_data,  # Función Python a ejecutar
    )
