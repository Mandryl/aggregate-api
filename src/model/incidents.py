"""Incidents model"""
from pydantic import BaseModel


class Incident(BaseModel):
    """Incidents API Model"""

    imageUrl: str
    region: str
