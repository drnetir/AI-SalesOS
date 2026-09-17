from fastapi import FastAPI
from .database import init_db
from .config import settings
from .api.tasks import router as task_router
from .api.memory import router as memory_router
init_db()
app=FastAPI(title=settings.app_name,version="1.0.0")
app.include_router(task_router);app.include_router(memory_router)
@app.get("/health")
def health():return {"status":"ok","service":"AI-SalesOS"}
