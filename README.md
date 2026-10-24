# TaskQ

**TaskQ** is a Celery-inspired background job processing system built with **FastAPI, Redis, and Docker Compose**. It exposes a REST API for submitting jobs, uses Redis as a shared queue and job-state store, and runs jobs in separate worker processes that can be scaled horizontally.

The project focuses on practical background-processing concerns: job lifecycle tracking, retries, failure handling, and running multiple workers.

## Architecture

```text
                 POST /jobs
Client  ---------------------------->  FastAPI API
                                          |
                                          | enqueue job
                                          v
                                    Redis queue/store
                                          |
                                  workers consume jobs
                                    /      |      \
                                   v       v       v
                               Worker 1 Worker 2 Worker N
                                    \      |      /
                                          |
                                    update job state
                                          v
                                         Redis

Client  <----------------------------  GET /jobs/{id}
                 job status
```

- **FastAPI** exposes endpoints for submitting jobs, checking job status, and viewing job statistics.
- **Redis** backs the queue and stores job metadata/state.
- **Workers** execute queued tasks independently of the API process.
- **Docker Compose** runs the application services and supports running multiple worker containers.

## Features

- **REST API for jobs** — submit work and retrieve job status.
- **Redis-backed queue** — decouples job submission from execution.
- **Separate worker processes** — API requests do not need to execute background tasks themselves.
- **Concurrent processing** — multiple workers can consume jobs from the shared queue.
- **Job lifecycle tracking** — tracks states such as `PENDING`, `RUNNING`, `RETRYING`, `COMPLETED`, and `FAILED`.
- **Retry handling** — retries failed jobs with exponential backoff.
- **Dead Letter Queue (DLQ)** — retains jobs that exhaust their retry attempts for later inspection.
- **Job statistics** — summarizes counts across job states.
- **Containerized setup** — runs the API, Redis, and workers with Docker Compose.

## Tech Stack

- **Python**
- **FastAPI** — REST API
- **Redis** — queue backend and job state
- **Docker & Docker Compose** — containerized services and multi-worker execution

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Run the application

Clone the repository and enter the project directory:

```bash
git clone https://github.com/sid-x0/TaskQ.git
cd TaskQ
```

Start the services:

```bash
docker compose up --build
```

The API should be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

### Scale workers

To run multiple worker containers, use Docker Compose's service scaling:

```bash
docker compose up --build --scale worker=3
```

Use the worker service name defined in your `compose.yaml` or `docker-compose.yml` if it differs from `worker`.

## API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/jobs` | Submit a job for background processing |
| `GET` | `/jobs/{id}` | Retrieve a job's status and details |
| `GET` | `/stats` | View job counts by state |

Check `/docs` on a running instance for the exact request schemas and response formats supported by the current implementation.

## Example Workflow

1. A client submits a job to `POST /jobs`.
2. FastAPI validates the request and places the job in Redis.
3. An available worker consumes the job and executes it.
4. The worker updates the job's state in Redis.
5. The client polls `GET /jobs/{id}` to check progress and the final result.
6. If execution fails, the retry policy handles subsequent attempts; jobs that exhaust retries are moved to the Dead Letter Queue.

## Project Scope

TaskQ demonstrates background job processing with concurrent workers and failure handling using a shared Redis instance. It is inspired by systems such as Celery and Sidekiq, but it is **not intended to implement distributed consensus or provide multi-node fault tolerance**.

## Future Improvements

Potential extensions include:

- Priority queues
- Worker health and heartbeat tracking
- Idempotent job execution and stronger crash recovery guarantees
- A dashboard for queue depth, throughput, and success/failure rates


