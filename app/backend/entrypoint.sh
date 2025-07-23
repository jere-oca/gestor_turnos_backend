#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U user; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Export DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=gestor_turnos.settings

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Run partitioning for Turno
echo "Running architect partition..."
architect partition --module turnos.models

# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000