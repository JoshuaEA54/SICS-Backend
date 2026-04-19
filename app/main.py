from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api.routes.auth import router as auth_router
from app.api.routes.companies import catalog_router as companies_catalog_router
from app.api.routes.companies import router as companies_router
from app.api.routes.controls import router as controls_router
from app.api.routes.evaluations import router as evaluations_router
from app.api.routes.geography import router as geography_router
from app.api.routes.users import router as users_router
from app.core.config import settings
from app.core.exception_handlers import registrar_handlers


app = FastAPI(
	title=settings.APP_NAME,
	swagger_ui_parameters={"persistAuthorization": True},
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.CORS_ORIGINS,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

registrar_handlers(app)

app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(geography_router, prefix=settings.API_PREFIX)
app.include_router(companies_catalog_router, prefix=settings.API_PREFIX)
app.include_router(companies_router, prefix=settings.API_PREFIX)
app.include_router(controls_router, prefix=settings.API_PREFIX)
app.include_router(evaluations_router, prefix=settings.API_PREFIX)
app.include_router(users_router, prefix=settings.API_PREFIX)

add_pagination(app)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
	return {"status": "ok"}
