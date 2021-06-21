"""Incidents router"""
import logging
import os
import sys
from logging import getLogger, DEBUG

import fastapi
from fastapi import APIRouter

from app.model.incidents import Incident
from app.model.raw_incidents import RawIncident
from app.repository.danger_zone import DangerZoneRepository
from app.repository.incident_image import IncidentImageRepository
from app.repository.prediction import PredictionRepository
from app.service.incidents import IncidentsService

logger = getLogger("router")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


def _incidents_service_factory() -> IncidentsService:
    return IncidentsService()


def _prediction_repository_factory() -> PredictionRepository:
    return PredictionRepository()


def _incident_image_repository_factory() -> IncidentImageRepository:
    return IncidentImageRepository()


def _danger_zone_repository_factory() -> DangerZoneRepository:
    return DangerZoneRepository()


router = APIRouter()


@router.post("/incidents", status_code=204, tags=["incidents"])
async def create_incidents(
    incident: Incident,
    incidents_service: IncidentsService = fastapi.Depends(
        _incidents_service_factory
    ),
    prediction_repo: PredictionRepository = fastapi.Depends(
        _prediction_repository_factory
    ),
    incident_image_repo: IncidentImageRepository = fastapi.Depends(
        _incident_image_repository_factory
    ),
    danger_zone_repo: DangerZoneRepository = fastapi.Depends(
        _danger_zone_repository_factory
    ),
) -> None:
    """Create incident records"""
    logger.debug("START router")
    incidents_service.create_incidents(
        object_name=incident.object_name,
        bucket_name=os.environ["BUCKET_NAME"],
        region=incident.region,
        prediction_repo=prediction_repo,
        incident_image_repo=incident_image_repo,
        danger_zone_repo=danger_zone_repo,
    )


@router.post("/raw-incidents", status_code=204, tags=["incidents"])
async def create_incidents(
    incident: RawIncident,
    incidents_service: IncidentsService = fastapi.Depends(
        _incidents_service_factory
    ),
    prediction_repo: PredictionRepository = fastapi.Depends(
        _prediction_repository_factory
    ),
    incident_image_repo: IncidentImageRepository = fastapi.Depends(
        _incident_image_repository_factory
    ),
    danger_zone_repo: DangerZoneRepository = fastapi.Depends(
        _danger_zone_repository_factory
    ),
) -> None:
    """Create incident records"""
    logger.debug("START router")
    incidents_service.create_incidents_from_raw_image(
        images=incident.images,
        bucket_name=os.environ["BUCKET_NAME"],
        region=incident.region,
        prediction_repo=prediction_repo,
        incident_image_repo=incident_image_repo,
        danger_zone_repo=danger_zone_repo,
    )
