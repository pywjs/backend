# main.py

from fastapi import FastAPI
from utils.version import get_version
from utils.logging import setup_logging
from apps.auth.endpoints import router as auth_router
from apps.users.endpoints import router as users_router


# ------------------------------------------
# Logging Configuration
# ------------------------------------------
setup_logging()


# ------------------------------------------
# FastAPI App Definition
# ------------------------------------------
app = FastAPI(
    title="pywjs API",
    description="pywjs API documentation",
    version=get_version(),
)


# ------------------------------------------
# Routers
# ------------------------------------------
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])


# Health Check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
