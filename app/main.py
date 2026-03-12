from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    message = f"test"
    version = f"1.0.0"
    return {"message": "Welcome to FastAPI Project by python by sp " }
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
