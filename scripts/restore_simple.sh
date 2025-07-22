#!/bin/bash

# Script de restore

BACKUP_DIR="/app/backups"
DB_NAME="${DATABASE_NAME:-gestor_turnos}"
DB_USER="${DATABASE_USERNAME:-postgres}"
DB_HOST="${DATABASE_HOST:-db}"
DB_PORT="${DATABASE_PORT:-5432}"

# Funcion para mostrar ayuda
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Script de Restore - Gestor de Turnos"
    echo "Uso: $0 [archivo_backup]"
    echo ""
    echo "Ejemplos:"
    echo "  $0 backup_mydatabase_20250722_025413.sql"
    echo "  $0 --list    # Listar backups disponibles"
    exit 0
fi

# Listar backups disponibles
if [ "$1" = "--list" ] || [ "$1" = "-l" ]; then
    echo "Backups disponibles en $BACKUP_DIR:"
    if [ -d "$BACKUP_DIR" ]; then
        ls -lh $BACKUP_DIR/backup_*.sql 2>/dev/null | awk '{print $9, $5, $6, $7, $8}' || echo "No hay backups disponibles"
    else
        echo "Directorio de backups no existe"
    fi
    exit 0
fi

# Verificar que se proporciono un archivo
if [ -z "$1" ]; then
    echo "Error: Debe especificar un archivo de backup"
    echo "Usa: $0 --list para ver backups disponibles"
    exit 1
fi

BACKUP_FILE="$1"

# Si no es ruta absoluta, buscar en directorio de backups
if [[ "$BACKUP_FILE" != /* ]]; then
    BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE"
fi

# Verificar que el archivo existe
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Archivo no encontrado: $BACKUP_FILE"
    echo "Usa: $0 --list para ver backups disponibles"
    exit 1
fi

echo "Iniciando restore de la base de datos..."
echo "Fecha: $(date)"
echo "Archivo: $(basename "$BACKUP_FILE")"
echo "Base de datos: $DB_NAME"

# Advertencia
echo ""
echo "ADVERTENCIA: Esta operación sobrescribirá la base de datos actual"
read -p "¿Continuar? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelado"
    exit 1
fi

# Restaurar la base de datos
echo "Restaurando base de datos..."

PGPASSWORD="$DATABASE_PASSWORD" psql \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    -d $DB_NAME \
    -f "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Restore completado exitosamente!"
else
    echo "Error durante el restore"
    exit 1
fi
