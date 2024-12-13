# FileNest

FileNest is a web application designed for efficient file management, leveraging a Django backend. The project includes integrations with MongoDB for data storage and MinIO for object storage.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Docker](#docker)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Django Backend**: Handles API logic and connects with MongoDB and MinIO.
- **MongoDB Integration**: Stores metadata and user-related data.
- **MinIO Integration**: Manages object storage for files.
- **CORS Configured**: Ensures seamless communication between backend and other services.
- **Digital Ocean**: Cloud hosting with custom security groups and firewall.

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: MongoDB
- **Object Storage**: MinIO
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/FileNest.git
   cd FileNest
   ```

2. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

3. Access the application:

   - Backend: `http://localhost:8000`

### Environment Variables

Create a `.env` file in the `backend/` directory:

#### Backend (`.env`) For Local Development Only:

```
DATABASE_URL=mongodb://mongo:27017/filenest
MINIO_ACCESS_KEY=your-access-key
MINIO_SECRET_KEY=your-secret-key
MINIO_ENDPOINT=http://storage:9000
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

## Usage
## Local Development

1. Start the backend and ensure it is accessible.
2. Use tools like Postman or cURL to interact with the API.

## Docker

- **Build and Start Containers**:

  ```bash
  docker-compose up --build
  ```

- **Stop Containers**:

  ```bash
  docker-compose down
  ```

- **View Logs**:

  ```bash
  docker-compose logs -f
  ```

## Production API URL
http://137.184.86.31:8000

## API Endpoints

### Test Endpoint

**GET** `/test`

- **Description**: Verifies the backend connection.
- **Response**:

  ```json
  {
    "message": "Backend is working!"
  }
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or fixes.

## License

This project is licensed under the [MIT License](LICENSE).

