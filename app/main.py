from fastapi import FastAPI

app = FastAPI(
    title="TaskQ",
    description="A Celery-inspired distributed background job processing system",
    version="0.1.0"
)


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