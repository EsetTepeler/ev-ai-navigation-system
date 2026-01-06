"""Status check endpoints for database and Redis services."""

# Standard library imports
import logging

# Third-party imports
from fastapi import APIRouter

# Local imports (services initialized in orchestrator)
from src.services.service_container import services

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/test-db")
async def test_database():
    """
    Test database connection.

    Returns:
        Connection status and details

    Raises:
        DatabaseException: If connection fails
    """
    try:
        return await services.database_service.test_connection()
    except Exception as e:
        from src.exceptions.custom_exceptions import DatabaseException

        raise DatabaseException(
            message="Failed to connect to database", details={"error": str(e)}
        )


@router.get("/redis-status")
async def get_redis_status():
    """
    Get Redis connection status.

    Returns:
        Redis connection information

    Raises:
        RedisException: If status check fails
    """
    try:
        return await services.redis_service.get_connection_status()
    except Exception as e:
        from src.exceptions.custom_exceptions import RedisException

        raise RedisException(
            message="Failed to get Redis status", details={"error": str(e)}
        )
