#!/bin/bash

# Iniciar Docker
docker start

# Ejecutar contenedor de SQL
docker run -d --name baseDatos mysql

# Cambiar al directorio "Consultas"
cd ProgramaMatrix

# Ingresar al directorio "backend"
cd backend

# Ejecutar entorno virtual de Python
source env/bin/activate

# Arrancar uvicorn
uvicorn main:app --host 192.88.1.35 --reload

# Regresar al directorio anterior
cd ..

# Cambiar al directorio "2chance"
cd webSystem

# Arrancar el servidor Angular
ng serve --host 192.88.1.35
