#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U user; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# Start the server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000