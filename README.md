# Taller: Uso practico de Airflow

## 📌 Descripción

**Este repositorio contiene un entorno para el procesamiento de datos y entrenamiento de modelos basado en `Apache Airflow`, `Docker` y `Python`. Su diseño modular permite la automatización de flujos de trabajo con soporte para `PostgreSQL`, `MySQL` y `Redis`, mejorando la gestión y orquestación de tareas en entornos distribuidos.

## 📂 Estructura del Proyecto

La estructura del proyecto está organizada para garantizar una correcta separación de responsabilidades y modularidad. Los flujos de trabajo se encuentran en la carpeta dags/, donde cada script maneja tareas específicas como la carga, eliminación y entrenamiento de datos. La carpeta app/ contiene los scripts principales de la aplicación, incluyendo el manejo de modelos y dependencias. La carpeta datos/ contiene los archivos de entrada requeridos para el procesamiento, mientras que logs/ almacena los registros de ejecución para facilitar el monitoreo. Los archivos de configuración, como docker-compose.yml y Dockerfile, permiten la implementación del entorno en contenedores, asegurando escalabilidad y reproducibilidad.

```
TALLER_3/
│── app/                      # Código de la aplicación principal
│   ├── cargar_modelos.py     # Script para carga de modelos
│   ├── Dockerfile.app        # Dockerfile específico para la app
│   ├── main.py               # Script principal
│   ├── requirements.txt      # Dependencias específicas de la app
│── dags/                      # Definición de flujos de trabajo
│   ├── carga_datos.py         # Carga de datos
│   ├── elimina_datos.py       # Eliminación de datos
│   ├── train.py               # Entrenamiento del modelo
│── datos/                     # Almacenamiento de datos
│   ├── penguins_lter.csv      # Conjunto de datos en formato CSV
│── logs/                      # Registro de ejecución
│── plugins/                   # Extensiones para Airflow
│── docker-compose.yml         # Orquestación de servicios
│── Dockerfile                 # Construcción de la imagen Docker
│── README.md                  # Documentación del proyecto
│── requirements.txt           # Dependencias generales del proyecto
```

## 🛠 Instancia MySQL
Para crear la instancia de la base de datos mysql, fue necesario incluir el servicio mysql dentro del docker-compose y el volume mysql_data como se encuentra a continuación:

```
mysql:
    # Nombre del servicio
    image: mysql:latest  # Imagen Docker para el contenedor MySQL
    ports:
      - "3306:3306"  # Mapeo de puertos del contenedor al host
    environment:
      MYSQL_ROOT_PASSWORD: airflow  # Contraseña de root para MySQL
      MYSQL_DATABASE: penguin_data  # Nombre de la base de datos MySQL
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]  # Comando de verificación de salud
      interval: 10s  # Frecuencia de la verificación de salud
      timeout: 5s  # Tiempo máximo de espera para la verificación de salud
      retries: 3  # Número de intentos de verificación de salud
      start_period: 10s  # Tiempo antes de iniciar las verificaciones de salud
    restart: always  # Política de reinicio del contenedor
```

## ⚙️ Requisitos

Para ejecutar este repositorio correctamente, es necesario contar con herramientas y configuraciones específicas. `Docker` y `Docker Compose` permiten la ejecución de los servicios en contenedores, asegurando un entorno reproducible y estable. `Python 3.x` es el lenguaje base para los scripts de procesamiento de datos. Además, las librerías listadas en `requirements.txt`, como `pandas`, `scikit-learn` e `imbalanced-learn`, proporcionan las funcionalidades necesarias para el análisis de datos y entrenamiento de modelos. Finalmente, `Apache Airflow` gestiona la ejecución de tareas automatizadas mediante flujos de trabajo definidos en DAGs.

## 🚀 Instalación y Configuración

La instalación y configuración del proyecto se realiza en pocos pasos, asegurando una rápida implementación del entorno. Primero, se clona el repositorio para obtener el código fuente y se accede al directorio del proyecto. Luego, se instalan las dependencias listadas en `requirements.txt`, garantizando que todas las herramientas necesarias estén disponibles. Posteriormente, se inician los servicios con `docker-compose`, lo que levanta los contenedores de Airflow, PostgreSQL, MySQL y Redis de manera automatizada. Finalmente, la interfaz web de Airflow puede ser accedida a través del navegador para gestionar y ejecutar los flujos de trabajo definidos.

1. Clonar el repositorio
```
git clone https://github.com/JohnSanchez27/MLOps_Taller3.git
cd MLOps_Taller3

```

2. Construir el contenedor
```
docker-compose up --build
```

3. Para detener los contenedores sin eliminarlos
```
docker-compose stop
```
4. Acceder a la interfaz de Airflow 
```
 https://localhost:8080 
```

5. Acceder a la interfaz del API
```
 https://localhost:8989/docs 
```


## 🏗️ Arquitectura y Configuración de Servicios

La arquitectura del proyecto está diseñada para garantizar la ejecución eficiente y escalable de flujos de trabajo en entornos distribuidos. Airflow gestiona la planificación y ejecución de tareas mediante `CeleryExecutor`, que permite distribuir la carga entre múltiples workers. Las bases de datos `PostgreSQL` y `MySQL` almacenan la metadata de Airflow y los datos procesados respectivamente. Redis actúa como un `broker` de mensajes, facilitando la comunicación entre los diferentes componentes del sistema. El uso de volúmenes persistentes asegura la integridad de los datos, evitando pérdidas tras reinicios del sistema.

## 🔥 Retos del Uso de Airflow
El uso de Airflow en entornos productivos conlleva varios desafíos técnicos que deben ser considerados para su correcta implementación. La configuración inicial requiere definir correctamente las variables de entorno y la conexión entre servicios. La gestión de dependencias debe ser precisa para evitar incompatibilidades con la versión de Airflow utilizada. El monitoreo y depuración de errores es esencial debido a la generación de múltiples registros de ejecución. Para manejar grandes volúmenes de datos, es necesario optimizar la configuración de `CeleryExecutor` y los recursos asignados a `Redis`, `PostgreSQL` y `MySQL`. Además, la estructuración adecuada de los DAGs permite optimizar la ejecución y reducir tiempos de procesamiento.

## 📊 Uso
El proyecto se gestiona a través de la interfaz web de Airflow, donde se pueden visualizar, programar y ejecutar flujos de trabajo. Los DAGs ubicados en `dags/` pueden ser modificados para adaptarse a nuevos requerimientos o incorporar nuevas funcionalidades. Los registros de ejecución almacenados en `logs/` proporcionan información detallada sobre el estado de cada tarea, lo que facilita la depuración y optimización del sistema.

## 🌐 Vista de DAGs en Airflow

A continuación se muestra una captura de pantalla de la interfaz de Airflow, donde se visualizan los DAGs definidos para este proyecto:

![alt text](image-1.png)
