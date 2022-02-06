from pydantic import BaseSettings


class Settings(BaseSettings):
    database_port: int
    database_hostname: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    expiration_time_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()
