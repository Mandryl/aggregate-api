"""Prediction repository"""
import json
import os
import sys
from dataclasses import dataclass
from logging import getLogger, DEBUG, StreamHandler

import boto3
from fastapi import HTTPException
from mypy_boto3_sagemaker_runtime import SageMakerRuntimeClient

from app.model.incidents_prediction import IncidentPredictionResponse

JSON_CONTENT_TYPE = "application/json"
NO_INCIDENTS = "no incident"

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


@dataclass
class PredictionRepository:
    """Prediction repository"""

    endpoint_name = os.environ["SAGEMAKER_ENDPOINT_NAME"]
    client: SageMakerRuntimeClient = boto3.client("sagemaker-runtime")

    def get_prediction_from_s3(
        self, object_name: str, bucket_name: str
    ) -> IncidentPredictionResponse:
        """Get prediction of incidents from image"""
        # Get prediction of SageMaker
        body = {"s3_object_name": object_name, "s3_bucket_name": bucket_name}
        body_str = json.dumps(body)
        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            Body=body_str.encode(),
            ContentType=JSON_CONTENT_TYPE,
            Accept=JSON_CONTENT_TYPE,
        )
        response_body = json.loads(response["Body"].read())
        logger.debug(response)
        logger.debug(response_body)

        if "results" not in response_body:
            raise HTTPException(status_code=500, detail="Prediction error")

        return IncidentPredictionResponse(results=response_body["results"])

    @staticmethod
    def check_prediction(response_body: IncidentPredictionResponse) -> bool:
        """Check incident"""
        if NO_INCIDENTS in response_body.results.incidents:
            return False
        return True
