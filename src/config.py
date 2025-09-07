from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str

    # CORREÇÃO AQUI: Remova o "../"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()