"""Incidents model"""
from pydantic import BaseModel


class Incident(BaseModel):
    """Incidents API Model"""

    object_name: str
    region: str
