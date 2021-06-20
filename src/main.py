"""FastAPI main"""
from fastapi import FastAPI

from src.router import incidents

app = FastAPI()

app.include_router(incidents.router)
