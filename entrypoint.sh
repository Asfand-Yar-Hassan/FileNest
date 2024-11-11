#!/bin/bash

# Wait until MongoDB is up and ready
until nc -z -v -w30 mongo 27017
do
  echo "Waiting for MongoDB..."
  sleep 5
done

# Run Django migrations, collect static files, and start the server
echo "MongoDB is up. Running Django migrations..."
cd backend
python manage.py migrate
python manage.py collectstatic --noinput

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
