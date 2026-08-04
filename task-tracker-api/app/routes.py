"""API routes for the Task Tracker application."""

from datetime import datetime, timezone

from fastapi import APIRouter, status

from app.models import HealthResponse


# Create a router that will hold the application's endpoints.
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
)
def get_health() -> HealthResponse:
    """Return the application's status and current UTC timestamp.

    Returns:
        HealthResponse: The current health status and UTC timestamp.

    Example:
        >>> response = client.get("/health")
        >>> response.status_code
        200
    """

    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc),
    )