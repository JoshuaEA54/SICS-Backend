from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.core.config import settings


app = FastAPI(
	title=settings.APP_NAME,
	debug=settings.DEBUG,
)

app.include_router(auth_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
	return {"status": "ok"}
