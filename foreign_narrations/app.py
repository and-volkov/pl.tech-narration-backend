from datetime import datetime as dt

import uvicorn
from fastapi import FastAPI, status, Response
from fastapi.responses import FileResponse

from settings import api_settings
from database import shows_history_collection, shows_collection
from models import ShowHistory, Show, Narration


app = FastAPI(title=api_settings.title)


@app.get('/')
async def test():
    return status.HTTP_200_OK


@app.post('/start/{show_name}', response_model=ShowHistory)
def get_current_show(show_name: str) -> Response:
    show = shows_collection.find_one({'name': show_name.upper()})
    show = Show(**show)
    available_languages = list(show.narrations.keys())
    print(available_languages)
    print(show)
    show_len = show.narrations.get('eng').file_length_in_secs
    current_show = ShowHistory(
        show_name=show.name,
        available_languages=available_languages,
        end_time=int(dt.timestamp(dt.now())) + show_len,
    )
    # shows_history_collection.insert_one(current_show.dict())
    return Response(current_show.json(), status_code=200)


@app.get(
    '/narrations/{language_tag}',
    responses={
        200: {
            "content": {"audio/mp3": {}},
            "description": "Return narration audio file",
        },
        403: {"description": "Nothing to return. You die alone"},
    },
)
async def send_narration_file(
    language_tag: str = 'eng',
) -> FileResponse | Response:

    last_show = (
        shows_history_collection.find().sort('end_time', -1).limit(1)[0]
    )
    if last_show.get('end_time') > dt.now().timestamp():
        show = shows_collection.find_one({'name': last_show.get('show_name')})
        narration = show.get('narrations').get(language_tag)
        file = narration.get('file_path')
        return FileResponse(file, media_type='audio/mp3')
    return Response(
        'No show currently running', status_code=status.HTTP_403_FORBIDDEN
    )


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
