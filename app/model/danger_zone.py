"""Danger zone model"""
# pylint: disable=no-name-in-module
from typing import Optional

from pydantic import BaseModel


class DangerZone(BaseModel):  # pylint: disable=too-few-public-methods
    """Danger zone model"""

    id: int
    latitude: str
    longitude: str
    photoUrl: Optional[str]
