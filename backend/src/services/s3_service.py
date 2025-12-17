import boto3
import json
import os
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL")
        self.region_name = os.getenv("S3_REGION_NAME")
        self.aws_access_key_id = os.getenv("S3_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY")
        self.bucket_name = os.getenv("S3_BUCKET_NAME")

        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

        self._ensure_bucket_exists()
        self._ensure_users_file_exists()

    def _ensure_bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            # If 404 Not Found, create it.
            # Some providers return 403 if it doesn't exist and we don't have ListBucket permission,
            # but usually we just try to create it if we can't see it.
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404 or error_code == 403:
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"Created bucket: {self.bucket_name}")
                except Exception as create_error:
                    logger.error(f"Failed to create bucket: {create_error}")
            else:
                logger.error(f"Failed to check bucket: {e}")

    def _ensure_users_file_exists(self):
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key="users.json")
        except ClientError:
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key="users.json",
                    Body=json.dumps({"users": []}),
                )
                logger.info("Created users.json in S3")
            except Exception as e:
                logger.error(f"Failed to create users.json: {e}")

    def load_users(self):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key="users.json")
            content = response["Body"].read().decode("utf-8")
            return json.loads(content)
        except Exception as e:
            logger.error(f"Failed to load users: {e}")
            return {"users": []}

    def save_users(self, users_data):
        try:
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key="users.json",
                Body=json.dumps(users_data, indent=2),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save users: {e}")
            return False

    def get_user_by_email(self, email):
        data = self.load_users()
        for user in data.get("users", []):
            if user["email"] == email:
                return user
        return None

    def get_user_by_id(self, user_id):
        data = self.load_users()
        for user in data.get("users", []):
            if user["id"] == user_id:
                return user
        return None

    def create_user(self, user_data):
        data = self.load_users()
        data["users"].append(user_data)
        if self.save_users(data):
            return user_data
        return None
