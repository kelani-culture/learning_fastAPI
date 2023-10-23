from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    db_password: str
    db_hostname: str
    db_port: str
    db_username: str
    secret_key: str
    algorithms: str
    access_token_expire_min: int
    
    class Config:
        env_file = '.env'

settings = Settings()