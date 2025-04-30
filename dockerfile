# Usamos Python como base
FROM python:3.12

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos de dependencias
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la app
COPY ./app .

# Puerto que usará Django
EXPOSE 8000

# Comando por defecto al ejecutar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
