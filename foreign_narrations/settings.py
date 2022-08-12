import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = 'development.env'
        env_file_encoding = 'utf-8'


class ApiSettings(BaseSettings):
    title: str = 'Planetarium Foreign Narrations API'
    host = 'HOST'
    port = 5010
    log_level: str = 'INFO'

    class Config:
        env_prefix = 'API_'


class MongoSettings(BaseSettings):
    host = 'HOST'
    port = 27017
    username: str = 'USERNAME'
    password: str = 'PASSWORD'
    auth_source = 'AUTH_SOURCE'
    auth_mechanism = 'AUTH_MECHANISM'
    database: str = 'foreign-narrations'
    shows_collection: str = 'shows'
    shows_history_collection: str = 'shows_history'

    class Config(BaseSettings.Config):
        env_prefix = 'MONGO_'


api_settings = ApiSettings()
mongo_settings = MongoSettings()
