# FastAPI with Dapr and Kafka

This project demonstrates the integration of FastAPI, Dapr, and Kafka, illustrating a microservices architecture that leverages Dapr for simplified distributed system capabilities and Kafka for event streaming.

## Concepts

### Dapr (Distributed Application Runtime)

Dapr is an event-driven, portable runtime for building microservices on cloud and edge environments. It abstracts common capabilities needed in microservices architectures, like:

- **State Management**: Provides stateful or stateless services with various state stores.
- **Pub/Sub Messaging**: Decouples services by providing publish and subscribe capabilities transparently.
- **Service Invocation**: Allows methods to be invoked on a remote service with built-in load balancing and retries.

### FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python, based on type hints. Its key features include:

- **Speed**: Comparable to NodeJS and Go due to Starlette for networking and Pydantic for data validation.
- **Developer Friendly**: Extensive support for editor autocompletion and type checks, reducing development time.

### Kafka

Kafka is a distributed event streaming platform capable of handling high-throughput data feeds. It is used for:

- **Stream Processing**: Processes streams of data in real time.
- **Event Storage**: Durable storage of stream data acting as a source of truth.
- **Decoupling of Data Streams**: Allows decoupling of data streams and systems.

### Docker Compose

Docker Compose is used to define and run multi-container Docker applications. In this project, it orchestrates:

- **FastAPI Application**: The core service providing the API.
- **Dapr Sidecar**: Enhances the FastAPI service with Dapr capabilities.
- **Kafka**: Manages messaging across services.

## Docker Compose Configuration

Here’s a brief look at the `docker-compose.yml`:

```yaml
version: "3.9"

services:
  fastapi:
    container_name: fastapi
    build:
      context: ./app
      dockerfile: Dockerfile
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
    ports:
      - 8000:8000

  dapr_sidecar:
    image: daprio/daprd:latest
    container_name: dapr
    command:
      [
        "./daprd",
        "-app-id",
        "fastapi",
        "-app-port",
        "8000",
        "-dapr-http-port",
        "3500",
        "-dapr-grpc-port",
        "50001",
        "-components-path",
        "/components",
      ]
    volumes:
      - "./components:/components"
    network_mode: service:fastapi
    depends_on:
      fastapi:
        condition: service_healthy
    restart: on-failure


    