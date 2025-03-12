FROM python:3.7

WORKDIR /app

# Copiar solo los archivos de requerimientos primero
COPY requirements.txt .

# Instalar las dependencias (aprovechando el caché)
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Copiar el resto del código fuente después de instalar las dependencias
COPY . .
