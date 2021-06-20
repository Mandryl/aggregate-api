"""FastAPI main"""
from fastapi import FastAPI

from app.router import incidents

app = FastAPI()

app.include_router(incidents.router)
