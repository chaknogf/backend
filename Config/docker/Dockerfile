# Utiliza una imagen de MariaDB como base
FROM mariadb:latest

# Configura las credenciales (ajusta según tus necesidades)
ENV MYSQL_ROOT_PASSWORD=Prometeus.0
ENV MYSQL_DATABASE=test_api
ENV MYSQL_USER=magnof
ENV MYSQL_PASSWORD=yosoyIroman.0

# Copia el archivo init.sql al contenedor
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

# Instala phpMyAdmin (ajusta según la versión deseada)
RUN apt-get update && apt-get install -y phpmyadmin=4:4.7.1-1
RUN echo "Include /etc/phpmyadmin/apache.conf" >> /etc/apache2/apache2.conf
RUN a2enmod rewrite



# Copia tu aplicación FastAPI al contenedor
COPY ./backend /app/backend

# Instala las dependencias de Angular
RUN cd /app/backend

# Instala Python y crea un entorno virtual
RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instala las dependencias de FastAPI
RUN pip install -r /app/backend/requirement.txt

# Expon el puerto en el que FastAPI se ejecutará
EXPOSE 8000

#Ejecutar servidor
RUN  uvicorn main:app --reload

# Comando para ejecutar la aplicación FastAPI
#CMD ["uvicorn", "backend.main:app", "--port", "8000", "--reload"]

# Instala Node.js para Angular
RUN apt-get update && apt-get install -y nodejs npm

# Copia tu aplicación Angular al contenedor
COPY ./2chance /app/2chance

# Instala las dependencias de Angular
RUN cd /app/2chance && npm install -g @angular/cli && npm install

# Expon el puerto en el que Angular se ejecutará
EXPOSE 4200

# Comando para ejecutar la aplicación Angular
#CMD ["ng", "serve", "--host", "0.0.0.0", "--port", "4200"]
RUN ng serve
