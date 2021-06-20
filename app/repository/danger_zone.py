"""Danger zone repository"""
import os
import sys
from dataclasses import dataclass
from decimal import Decimal
from logging import getLogger, DEBUG, StreamHandler

import boto3

from app.repository.incident_image import IncidentImageRepository, Location

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


@dataclass
class DangerZoneRepository:
    """Danger zone repository"""

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DANGER_ZONE_TABLE_NAME"])
    sequence = dynamodb.Table(os.environ["SEQUENCE_TABLE_NAME"])

    def get_next_id(self) -> int:
        """Get max id of table"""
        return self.sequence.update_item(
            Key={"sequence_key": os.environ["SEQUENCE_KEY"]},
            UpdateExpression="ADD #name :increment",
            ExpressionAttributeNames={"#name": "sequence"},
            ExpressionAttributeValues={":increment": int(1)},
            ReturnValues="UPDATED_NEW",
        )["Attributes"]["sequence"]

    def create_danger_zone(
        self,
        location: Location,
        object_name: str,
        bucket_name: str,
        region: str,
        photo_url: str = None,
        incident_image_repo: IncidentImageRepository = None,
    ) -> None:
        """Create danger zone"""
        logger.debug("START create_danger_zone")
        if photo_url is None and incident_image_repo is not None:
            photo_url = incident_image_repo.get_object_url(
                object_name=object_name, bucket_name=bucket_name
            )
            logger.debug("Photo url: %s", photo_url)

        response = self.table.put_item(
            Item={
                "ID": str(self.get_next_id()),
                "Latitude": Decimal(location.latitude),
                "Longitude": Decimal(location.longitude),
                "PhotoUrl": photo_url,
                "Code": region,
            },
        )
        logger.debug(response)
