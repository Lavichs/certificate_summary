from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str

    CACHE_LIFETIME: int     # seconds

    DOMAIN: str

    ADMIN_PASSWORD: str

    GRAFANA_ADMIN_LOGIN: str
    GRAFANA_ADMIN_PASSWORD: str

    COOKIE_SESSION_ID_KEY: str = "web-app-session-id"

    @property
    def DB_URL_ASYNC(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # @property
    # def DB_URL_SYNC(self) -> str:
    #     return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
