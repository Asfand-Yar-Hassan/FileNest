#!/bin/sh

# Wait for MongoDB to be available
while ! nc -z mongodb 27017; do
  echo "Waiting for MongoDB to be available..."
  sleep 1
done
echo "MongoDB is available"

cd app

# Activate the virtual environment
. env/bin/activate  # This should now be valid since we're creating the venv inside the container

# Run Django migrations and start the server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
