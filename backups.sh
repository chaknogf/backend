#!/bin/bash

# Configuración
DB_CONTAINER_NAME="elSQL"  # Nombre del contenedor MySQL
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="Prometeus.0"
DB_NAME="test_api"
BACKUP_DIR="/Users/macbookairm2/Project/Consultas"
DATE=$(date +"%Y%m%d_%H%M%S")

# Obtener la lista de tablas en la base de datos
TABLES=$(docker exec "$DB_CONTAINER_NAME" mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "USE $DB_NAME; SHOW TABLES;" | tail -n +2)

# Comando para realizar la copia de seguridad dentro del contenedor Docker
for TABLE in $TABLES; do
  BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TABLE}-$DATE.sql"
  docker exec "$DB_CONTAINER_NAME" mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" "$TABLE" > "$BACKUP_FILE"

  # Verificar el éxito del comando mysqldump
  if [ $? -eq 0 ]; then
    echo "Copia de seguridad exitosa para la tabla $TABLE. Archivo: $BACKUP_FILE"
  else
    echo "Error al realizar la copia de seguridad para la tabla $TABLE"
  fi
done
