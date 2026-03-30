from fastapi import APIRouter

from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/google/configured")
def google_oauth_is_configured() -> dict[str, bool]:
	return {
		"configured": bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET),
	}