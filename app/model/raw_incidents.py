"""Incidents model"""
from typing import List

from pydantic import BaseModel


class RawIncident(BaseModel):
    """Incidents API Model"""

    images: List[str]
    region: str
