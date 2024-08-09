# Multilingual-e5-embedding API

This project provides a FastAPI-based service that generates embeddings for input text using a pre-trained transformer model. The service is containerized using Docker and can be deployed with `docker-compose`.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Deployment](#deployment)

## Features

- Generates text embeddings using the `intfloat/multilingual-e5-large` model.
- FastAPI provides an easy-to-use API endpoint for embedding generation.
- Containerized with Docker for easy deployment and scalability.
- Supports GPU acceleration with NVIDIA GPUs.

## Requirements

- Docker
- Docker Compose
- NVIDIA GPU (optional, but recommended for faster processing)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ammosu/e5-embedding-api.git
   cd e5-embedding-api
   ```
2. **Build and run the service using Docker Compose**:

   ```bash
   docker-compose up -d --build
   ```

  This command will build the Docker image and start the service in the background.

## Usage
Once the service is running, you can access the API at `http://localhost:8080`.

### Example: Generate Embeddings
To generate embeddings, send a POST request to the `/v1/embeddings` endpoint with a JSON payload containing the text inputs.

```bash
curl -X POST "http://localhost:8080/v1/embeddings" -H "Content-Type: application/json" -d '{
  "input": ["This is a sample sentence.", "And another one."]
}'
```
You should receive a JSON response containing the embeddings.

## Configuration
The service can be configured using environment variables:

* `MODEL_CACHE_DIR`: Directory to cache the pre-trained model (default: `/model_cache`).
These variables can be set in the `docker-compose.yml` file or overridden at runtime.

## API Reference

### POST /v1/embeddings
Generate embeddings for input text.

* **Request Body**:

  * `input`: List of strings for which embeddings need to be generated.
  * `model` (optional): Model name to use (default: intfloat/multilingual-e5-large).

* **Response**:

  * `object`: "embedding"
  * `data`: List of dictionaries, each containing an embedding vector and the corresponding index.
  * `model`: The model used for generating embeddings.
  * `usage`: Token usage statistics.

## Deployment

### Running the Service in the Background
To run the service in the background, use the following command:

```bash
docker-compose up -d
```

### Stopping the Service
To stop the running service, use:

```bash
docker-compose down
```

### Viewing Logs
To view the logs of the running service:

```bash
docker-compose logs -f
```
