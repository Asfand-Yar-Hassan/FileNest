# Start with the official Python image as the base
FROM python:3.11-slim

# Set environment variables to prevent Python from generating .pyc files and enable unbuffered logging
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install netcat-openbsd to allow the entrypoint script to wait for MongoDB
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY backend/requirements.txt /app/

# Create a virtual environment in the container
RUN python3 -m venv /app/env

# Upgrade pip and install the dependencies in the virtual environment
RUN /app/env/bin/pip install --upgrade pip && /app/env/bin/pip install -r requirements.txt

# Copy the entire backend directory into the container (this is where manage.py should be)
COPY backend/ /app/

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
