from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    mode: Literal["dev", "test", "prod"]  # Фиксированное множество 1 из значений

    db_host: str
    db_port: int
    db_user: str
    db_name: str
    db_pass: str

    db_host_test: str
    db_port_test: int
    db_user_test: str
    db_name_test: str
    db_pass_test: str

    jwt_secret_key: str
    jwt_algorithm: str

    redis_host: str
    redis_port: int

    smtp_host: str
    smtp_user: str
    smtp_password: str
    smtp_port: int

    @property
    def databse_url(self):
        users = f"{self.db_user}:{self.db_pass}"
        db = f"{self.db_host}:{self.db_port}/{self.db_name}"
        return f"postgresql+asyncpg://{users}@{db}"

    @property
    def databse_test_url(self):
        users = f"{self.db_user_test}:{self.db_pass_test}"
        db = f"{self.db_host_test}:{self.db_port_test}/{self.db_name_test}"
        return f"postgresql+asyncpg://{users}@{db}"

    @property
    def redis_url(self):
        redis = f"redis://{self.redis_host}:{self.redis_port}"
        return redis

    class Config:
        env_file = ".env"


settings = Settings()
