"""Incidents services"""
import sys
from dataclasses import dataclass
from logging import getLogger, DEBUG, StreamHandler


from app.model.incidents_prediction import IncidentPredictionResponse
from app.repository.danger_zone import DangerZoneRepository
from app.repository.incident_image import IncidentImageRepository, Location
from app.repository.prediction import PredictionRepository

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


@dataclass
class IncidentsService:
    """Incidents service"""

    prediction_repository = PredictionRepository()

    @staticmethod
    def create_incidents(
        object_name: str,
        bucket_name: str,
        region: str,
        prediction_repo: PredictionRepository,
        incident_image_repo: IncidentImageRepository,
        danger_zone_repo: DangerZoneRepository,
    ) -> None:
        """Get image from image url"""
        logger.debug("START service")
        # Get prediction
        prediction = prediction_repo.get_prediction_from_s3(
            object_name, bucket_name
        )
        logger.debug("Prediction result: %s", prediction)
        # for test
        prediction = IncidentPredictionResponse(
            results={
                "incidents": ["wildfire", "on fire", "fire whirl"],
                "probs": [
                    0.7944601774215698,
                    0.14855162799358368,
                    0.032775163650512695,
                ],
            }
        )

        # if prediction is not incident, do not register incidents
        if not prediction_repo.check_prediction(prediction):
            return

        # Get location
        location: Location = incident_image_repo.get_location_from_s3(
            object_name, bucket_name
        )
        logger.debug("Location: %s", location)

        # Create danger zone
        danger_zone_repo.create_danger_zone(
            location,
            object_name,
            bucket_name,
            region,
            incident_image_repo=incident_image_repo,
        )

        logger.debug("END service")
