#!/bin/bash

# Script de backup

# Configuracion basica
BACKUP_DIR="/app/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="${DATABASE_NAME:-gestor_turnos}"
DB_USER="${DATABASE_USERNAME:-postgres}"
DB_HOST="${DATABASE_HOST:-db}"
DB_PORT="${DATABASE_PORT:-5432}"

echo "Iniciando backup de la base de datos..."
echo "Fecha: $(date)"
echo "Base de datos: $DB_NAME"

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Crear backup
BACKUP_FILE="$BACKUP_DIR/backup_${DB_NAME}_${DATE}.sql"

PGPASSWORD="$DATABASE_PASSWORD" pg_dump \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    -d $DB_NAME \
    --clean \
    --no-owner \
    > $BACKUP_FILE

# Verificar que se creo el backup
if [ -f "$BACKUP_FILE" ]; then
    echo "Backup creado exitosamente: $(basename $BACKUP_FILE)"
    echo "Tamaño: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo "Error: No se pudo crear el backup"
    exit 1
fi

echo "Backup completado!"
