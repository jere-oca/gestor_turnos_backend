#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U user; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Exportar DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=gestor_turnos.settings

# Ejecutar migraciones
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Ejecutar architect para particionar el modelo Turno
echo "Running architect partition..."
architect partition --module turnos.models

# Iniciar el servidor
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000