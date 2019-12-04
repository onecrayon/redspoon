"""Configuration settings, loaded from environment variables

`settings` instance is hoisted to the main application module; e.g.:

    from application import settings
"""
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    db_user: str
    db_password: str = ''
    db_name: str
    db_host: str = 'localhost'
    db_port: int = 5432
    db_driver: str = 'postgresql+psycopg2'

    debug: bool = False

    @property
    def db_url(self) -> str:
        return f'{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
    
    class Config:
        env_prefix = 'REDSPOON_'


# Configure settings object from environment variables
settings = ApplicationSettings()
