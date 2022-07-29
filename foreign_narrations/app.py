import uvicorn
from fastapi import FastAPI
from fastapi import status

from settings import api_settings


app = FastAPI(
    title=api_settings.title
)


@app.get('/')
async def test():
    return status.HTTP_200_OK


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower()
    )
