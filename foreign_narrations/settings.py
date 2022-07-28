import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = '.env'


class ApiSettings(BaseSettings):
    title: str = 'Planetarium Foreign Narrations API'
    host: str = '0.0.0.0'
    port: int = 5000
    log_level: str = 'INFO'

    class Config:
        env_prefix = 'API_'


class MongoSettings(BaseSettings):
    uri: str = "mongodb://127.0.0.1:27017"
    database: str = "foreign-narrations"
    collection: str = "shows"

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


api_settings = ApiSettings()
mongo_settings = MongoSettings()
