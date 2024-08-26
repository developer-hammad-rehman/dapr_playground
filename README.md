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

  broker:
    image: apache/kafka:3.7.0
    hostname: broker
    container_name: broker
    ports:
      - "9092:9092"
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
      KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT_HOST://localhost:9092,PLAINTEXT://broker:19092"
      KAFKA_PROCESS_ROLES: "broker,controller"
      KAFKA_CONTROLLER_QUORUM_VOTERS: "1@broker:29093"
      KAFKA_LISTENERS: "CONTROLLER://:29093,PLAINTEXT_HOST://:9092,PLAINTEXT://:19092"
      KAFKA_INTER_BROKER_LISTENER_NAME: "PLAINTEXT"
      KAFKA_CONTROLLER_LISTENER_NAMES: "CONTROLLER"
      CLUSTER_ID: "4L6g3nShT-eMCtK--X86sw"
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_LOG_DIRS: "/tmp/kraft-combined-logs"
    
  kafka-ui:
    image: provectuslabs/kafka-ui
    container_name: kafka-ui
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: "Local Kafka Cluster"
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: "broker:19092"
      DYNAMIC_CONFIG_ENABLED: "true"
    depends_on:
      - broker      

networks:
  default:
    driver: bridge

```
```bash
docker compose up --build
```

This README provides a clear overview of the technology stack and setup instructions while keeping the focus on the conceptual benefits and configurations.