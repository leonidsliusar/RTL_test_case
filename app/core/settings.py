from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = '27017'
    TG_TOKEN: str = '...'


settings = Settings()
