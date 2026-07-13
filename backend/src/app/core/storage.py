import boto3
from botocore.client import BaseClient

from app.core.config import settings


class StorageService:
    def __init__(self) -> None:
        self.client: BaseClient = boto3.client(
            service_name="s3",
            endpoint_url=settings.B2_ENDPOINT,
            aws_access_key_id=settings.B2_ACCESS_KEY,
            aws_secret_access_key=settings.B2_SECRET_KEY,
            region_name=settings.B2_REGION,
        )

    @property
    def bucket(self) -> str:
        return settings.B2_BUCKET_NAME


storage = StorageService()