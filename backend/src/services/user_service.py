"""
User Service - User management and authentication logic (S3 Based)
"""

import logging
from typing import Dict, Optional, Any
from datetime import datetime
import uuid

from src.services.auth_service import AuthService
from src.services.s3_service import S3Service

logger = logging.getLogger(__name__)


class UserService:
    """Handle user-related operations using S3 storage."""

    def __init__(self) -> None:
        """Initialize user service with auth and s3 services."""
        self.auth_service = AuthService()
        self.s3_service = S3Service()

    async def create_user(
        self, email: str, password: str, username: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new user account in S3.

        Args:
            email: User's email address
            password: Plain text password
            username: Optional username

        Returns:
            User data dict if successful, None if user exists
        """
        # Check if user already exists
        if self.s3_service.get_user_by_email(email):
            logger.warning(f"User registration failed: {email} already exists")
            return None

        # Hash password
        password_hash = self.auth_service.hash_password(password)

        # Create user object
        new_user = {
            "id": str(uuid.uuid4()),  # Use UUID for S3 JSON
            "email": email,
            "username": username or email.split("@")[0],
            "password_hash": password_hash,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None,
        }

        # Save to S3
        saved_user = self.s3_service.create_user(new_user)

        if saved_user:
            logger.info(f"New user created: {email}")
            return {
                "id": saved_user["id"],
                "email": saved_user["email"],
                "username": saved_user["username"],
                "created_at": saved_user["created_at"],
            }
        return None

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password against S3 data.
        """
        user = self.s3_service.get_user_by_email(email)

        if not user:
            logger.warning(f"Login failed: user {email} not found")
            return None

        if not user.get("is_active", True):
            logger.warning(f"Login failed: user {email} is inactive")
            return None

        # Verify password
        if not self.auth_service.verify_password(password, user["password_hash"]):
            logger.warning(f"Login failed: incorrect password for {email}")
            return None

        # Update last login (In a real DB we would update this, but for JSON/S3
        # doing a full write just for last_login might be expensive/slow.
        # Let's skip updating last_login on S3 for performance, or do it async)
        # For now, we'll skip saving it back to avoid S3 write latency on every login.

        # Generate tokens
        access_token = self.auth_service.create_access_token(user["id"], user["email"])
        refresh_token = self.auth_service.create_refresh_token(user["id"])

        logger.info(f"User logged in: {email}")

        return {
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information by ID."""
        user = self.s3_service.get_user_by_id(user_id)

        if user:
            return {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"],
                "created_at": user["created_at"],
                "last_login": user.get("last_login"),
            }
        return None

    async def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Generate new access token from refresh token."""
        payload = self.auth_service.verify_token(refresh_token)

        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")  # ID is string now
        user_data = await self.get_user_by_id(user_id)

        if not user_data:
            return None

        new_access_token = self.auth_service.create_access_token(
            user_id, user_data["email"]
        )

        return new_access_token
