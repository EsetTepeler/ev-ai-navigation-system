"""
Service Container - Global access to initialized services
"""

from typing import Optional, Any


class ServiceContainer:
    database_service: Optional[Any] = None
    redis_service: Optional[Any] = None


# Global instance
services = ServiceContainer()
