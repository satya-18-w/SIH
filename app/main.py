from fastapi import FastAPI
from app.routers import chat, ingest
from app.core.config import settings

from app.core.scheduler import start_scheduler
from app.db.init_db import initial_data_load

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

@app.on_event("startup")
def startup_event():
    initial_data_load()
    start_scheduler()


app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(ingest.router, prefix="/api", tags=["ingest"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
