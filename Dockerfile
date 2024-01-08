FROM pypy:3.10-7.3.14-bookworm

WORKDIR /app

# Copia solo los archivos necesarios para instalar las dependencias.
COPY requirement.txt .

# Crea y activa el entorno virtual
RUN python3 -m venv env
SHELL ["/bin/bash", "-c", "source env/bin/activate"]

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirement.txt
RUN pip install fastapi-jwt-auth

# Copia todos los archivos al directorio de trabajo en el contenedor
COPY . .

# Expone el puerto en el que tu aplicación estará escuchando (ajusta según sea necesario)
EXPOSE 8000


# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--reload", "--port", "8000"]
