from fastapi import FastAPI
from app.core.redis_client import redis_client
from app.api.routes import router

app = FastAPI(
    title="TaskQ",
    description="A Celery-inspired distributed background job processing system",
    version="0.1.0"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TaskQ!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
    
@app.get("/redis-test")
def redis_test():
    redis_client.set("hello", "TaskQ")
    value = redis_client.get("hello")

    return {
        "redis_value": value
    }