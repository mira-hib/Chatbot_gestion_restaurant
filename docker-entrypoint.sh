#!/bin/bash
set -e

echo "==================================="
echo "Starting Django Restaurant API"
echo "==================================="

# Wait for database to be ready (if using PostgreSQL)
echo "Waiting for database..."
sleep 3

# Run migrations
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if not exists
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@restaurant.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
END

# Load initial data
echo "Loading initial data..."
python manage.py shell < setup_initial_data.py || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "==================================="
echo "Starting Django server..."
echo "==================================="

# Start server
exec python manage.py runserver 0.0.0.0:8000
