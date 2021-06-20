"""Incidents router"""
from fastapi import APIRouter

from app.model.incidents import Incident

router = APIRouter()


@router.post("/incidents", status_code=204, tags=["incidents"])
async def create_incidents(incident: Incident):
    """Create incident records"""
