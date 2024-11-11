# Start with the official Python image as the base
FROM python:3.11-slim

# Set environment variables to prevent Python from generating .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install netcat-openbsd to allow the entrypoint script to wait for MongoDB
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

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

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint to the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Default command will be handled by the entrypoint script
