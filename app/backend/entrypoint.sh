#!/bin/sh

# Wait for database to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h db -p 5432 -U user; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# Load initial data if needed
echo "Loading initial data..."
python manage.py loaddata /app/backend/fixtures/initial_data.json || echo "Fixtures already loaded or not needed"

# Setup passwords (hash them if they're in plain text)
echo "Setting up user passwords..."
python manage.py setup_passwords

# Collect static files (if needed)
# python manage.py collectstatic --noinput

# Start the server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:8000