#!/bin/bash

# Configuración
DB_CONTAINER_NAME="elSQL"  # Nombre del contenedor MySQL
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="Prometeus.0"
DB_NAME="test_api"
BASE_BACKUP_DIR="/Users/macbookairm2/Project/Consultas"
DATE=$(date +"%Y%m%d_%H%M%S")

# Códigos de escape ANSI para colores y estilos
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Color
RESALT='\033[4;33;40m'


# Crear el nombre de la carpeta de respaldo
BACKUP_DIR="$BASE_BACKUP_DIR/$DATE"
mkdir -p "$BACKUP_DIR"  # Crea la carpeta si no existe

# Obtener la lista de tablas en la base de datos
TABLES=$(docker exec "$DB_CONTAINER_NAME" mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "USE $DB_NAME; SHOW TABLES;" | tail -n +2)

# Comando para realizar la copia de seguridad dentro del contenedor Docker
for TABLE in $TABLES; do
  BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TABLE}.sql"
  docker exec "$DB_CONTAINER_NAME" mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" "$TABLE" > "$BACKUP_FILE"

  # Verificar el éxito del comando mysqldump
  if [ $? -eq 0 ]; then
    echo -e "Copia de seguridad ${GREEN}Exitosa ${NC}para la tabla ${RESALT}$TABLE${NC}. Archivo: $BACKUP_FILE"
  else
    echo -e "${RED}Error al realizar la copia de seguridad para la tabla $TABLE${NC}"
  fi
done
