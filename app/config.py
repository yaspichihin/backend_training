from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host:        str
    db_port:        int
    db_user:        str
    db_name:        str
    db_pass:        str
    jwt_secret_key: str
    jwt_algorithm:  str

    @property
    def databse_url(self):
        users = f"{self.db_user}:{self.db_pass}"
        db    = f"{self.db_host}:{self.db_port}/{self.db_name}"
        return f"postgresql+asyncpg://{users}@{db}"
    
    class Config:
        env_file = ".env"

settings = Settings()