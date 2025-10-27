from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database settings
    postgres_user: str = "fastapi_user"
    postgres_password: str = "fastapi_password"
    postgres_db: str = "fastapi_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    
    # Application settings
    app_name: str = "FastAPI Project"
    debug: bool = True
    environment: str = "development"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()

