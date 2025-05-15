# main.py

from fastapi import FastAPI
from utils.version import get_version


# ------------------------------------------
# FastAPI App Definition
# ------------------------------------------
app = FastAPI(
    title="pywjs API",
    description="pywjs API documentation",
    version=get_version(),
)
