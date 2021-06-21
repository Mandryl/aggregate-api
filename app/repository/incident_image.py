"""Incident image repository"""
import base64
import uuid
from dataclasses import dataclass
from typing import Tuple, Optional, NamedTuple, List

import boto3
from PIL import Image, ExifTags

GPS_INFO_TAG_NAME = "GPSInfo"
GPS_LATITUDE = "GPSLatitude"
GPS_LATITUDE_REF = "GPSLatitudeRef"
GPS_LONGITUDE = "GPSLongitude"
GPS_LONGITUDE_REF = "GPSLongitudeRef"


class Location(NamedTuple):
    """Location"""

    latitude: float
    longitude: float


@dataclass
class IncidentImageRepository:
    """Incident image repository"""

    s3_client = boto3.client("s3")
    boto_session = boto3.session.Session()

    def get_location_from_s3(
        self, object_name: str, bucket_name: str
    ) -> Location:
        """Get location from exif of image"""
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=object_name)[
            "Body"
        ]
        image = Image.open(obj)
        return self._get_gps(image)

    def get_object_url(self, object_name: str, bucket_name: str):
        return f"https://{bucket_name}.s3.{self.boto_session.region_name}.amazonaws.com/{object_name}"

    def upload_files(
        self, base64images: List[str], bucket_name: str
    ) -> List[str]:
        object_names = []
        for image in base64images:
            key = f"{uuid.uuid4()}.jpg"
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                ContentType="image/jpg",
                Body=self.base64_to_binary(image),
            )
            object_names.append(key)

        return object_names

    def _get_gps(self, image: Image) -> Optional[Location]:
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in image._getexif().items()
            if k in ExifTags.TAGS
        }

        if GPS_INFO_TAG_NAME not in exif:
            return None

        gps = {
            ExifTags.GPSTAGS.get(k, k): v
            for k, v in exif[GPS_INFO_TAG_NAME].items()
        }

        if (
            GPS_LATITUDE not in gps
            or GPS_LATITUDE_REF not in gps
            or GPS_LONGITUDE not in gps
            or GPS_LONGITUDE_REF not in gps
        ):
            return None

        lat = gps[GPS_LATITUDE]
        lat_ref = gps[GPS_LATITUDE_REF]
        lon = gps[GPS_LONGITUDE]
        lon_ref = gps[GPS_LONGITUDE_REF]

        return Location(
            self._get_decimal_latitude(lat, lat_ref),
            self._get_decimal_longitude(lon, lon_ref),
        )

    @staticmethod
    def base64_to_binary(base64_str: str) -> bytes:
        return base64.b64decode(base64_str.encode("UTF-8"))

    @staticmethod
    def _get_decimal_latitude(
        latitude: Tuple[float, float, float], latitude_ref: str
    ) -> float:
        if latitude_ref == "N":
            sign = 1.0
        else:
            sign = -1.0

        return sign * latitude[0] + latitude[1] / 60 + latitude[2] / 3600

    @staticmethod
    def _get_decimal_longitude(
        longitude: Tuple[float, float, float], longitude_ref: str
    ) -> float:
        if longitude_ref == "E":
            sign = 1.0
        else:
            sign = -1.0

        return sign * longitude[0] + longitude[1] / 60 + longitude[2] / 3600
