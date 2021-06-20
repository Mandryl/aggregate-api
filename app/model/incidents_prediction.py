"""Incident prediction model"""
# pylint: disable=no-name-in-module
from __future__ import annotations

from typing import List

from pydantic import BaseModel


class IncidentPrediction(BaseModel):  # pylint: disable=too-few-public-methods
    """Incident prediction model"""

    incidents: List[str]
    probs: List[float]


class IncidentPredictionResponse(
    BaseModel
):  # pylint: disable=too-few-public-methods
    """Incident prediction model"""

    results: IncidentPrediction
