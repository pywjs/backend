# main.py

from fastapi import FastAPI
from utils.version import get_version
from utils.logging import setup_logging
from apps.auth.routes.v1 import router as auth_router_v1
from apps.users.routes.v1 import router as users_router_v1

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
app.include_router(auth_router_v1)
app.include_router(users_router_v1)


# Health Check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
