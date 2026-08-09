from typing import Any

import boto3
from botocore.client import BaseClient

from app.core.config import settings
from collections.abc import Iterator
from hashlib import sha256

from botocore.exceptions import ClientError

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

    def generate_upload_url(
        self,
        object_key: str,
        content_type: str,
        expires_in: int = 900,
    ) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )
    def object_exists(self, object_key: str) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket,
                Key=object_key,
            )
            return True
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return False

            raise


    def calculate_sha256(self, object_key: str) -> str:
        response = self.client.get_object(
            Bucket=self.bucket,
            Key=object_key,
        )

        body = response["Body"]
        digest = sha256()

        try:
            while True:
                chunk = body.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)
        finally:
            body.close()

        return digest.hexdigest()


    def delete_object(self, object_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket,
            Key=object_key,
        )

storage = StorageService()