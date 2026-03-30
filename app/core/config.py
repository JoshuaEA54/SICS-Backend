from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=True,
		extra="ignore",
	)

	APP_NAME: str = "SICS Backend"
	API_PREFIX: str = "/api/v1"
	DEBUG: bool = False

	DATABASE_URL: str | None = None
	POSTGRES_USER: str = ""
	POSTGRES_PASSWORD: str = ""
	POSTGRES_DB: str = ""
	POSTGRES_HOST: str = "localhost"
	POSTGRES_PORT: int = 5432

	GOOGLE_CLIENT_ID: str = ""
	GOOGLE_CLIENT_SECRET: str = ""
	UPLOAD_FOLDER: str = "data/uploads"

	@computed_field
	@property
	def sqlalchemy_database_uri(self) -> str:
		if self.DATABASE_URL:
			return self.DATABASE_URL

		missing_parts = []
		if not self.POSTGRES_USER:
			missing_parts.append("POSTGRES_USER")
		if not self.POSTGRES_PASSWORD:
			missing_parts.append("POSTGRES_PASSWORD")
		if not self.POSTGRES_DB:
			missing_parts.append("POSTGRES_DB")

		if missing_parts:
			missing_as_text = ", ".join(missing_parts)
			raise ValueError(
				"DATABASE_URL is not set and required postgres variables are missing: "
				f"{missing_as_text}"
			)

		return (
			"postgresql+psycopg://"
			f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
			f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
		)


settings = Settings()