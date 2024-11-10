# Start with the official Python image as the base
FROM python:3.11-slim

# Set environment variables to prevent Python from generating .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY backend/requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Create a directory for static files
RUN mkdir -p /app/staticfiles

# Expose the Django port
EXPOSE 8000

# Run Django migrations and start the server
CMD ["cd backend","sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
