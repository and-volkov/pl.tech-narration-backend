import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = 'development.env'


class ApiSettings(BaseSettings):
    title: str = 'Planetarium Foreign Narrations API'
    host: str = 'HOST'
    port: int = 'PORT'
    log_level: str = 'INFO'

    class Config:
        env_prefix = 'API_'


class MongoSettings(BaseSettings):
    host = 'HOST'
    port: int = 'PORT'
    username: str = 'USERNAME'
    password: str = 'PASSWORD'
    auth_source = 'AUTH_SOURCE'
    auth_mechanism = 'AUTH_MECHANISM'
    database: str = 'foreign-narrations'
    collection: str = 'shows'

    class Config(BaseSettings.Config):
        env_prefix = 'MONGO_'


api_settings = ApiSettings()
mongo_settings = MongoSettings()
