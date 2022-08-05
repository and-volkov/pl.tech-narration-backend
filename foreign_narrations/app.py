import asyncio
from pathlib import Path

import uvicorn
from fastapi import FastAPI, status, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse

from settings import api_settings
from models import ShowHistory
from handlers import get_show, get_show_narration, insert_new_running_show

app = FastAPI(title=api_settings.title)


html_path = Path(__file__).with_name('test.html')
with open(html_path, 'r') as f:
    test_html = f.read()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, show: ShowHistory):
        for connection in self.active_connections:
            await asyncio.sleep(0.001)
            await connection.send_json(show.json())


manager = ConnectionManager()


@app.websocket('/ws/{client_id}')
async def send_show_notification(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            if msg.lower() == 'close':
                await manager.disconnect(websocket)
                await websocket.close()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.post(
    '/start/{show_name}',
    responses={200: {'description': 'Running show accepted'}},
)
async def get_start_command(show_name: str) -> Response:
    insert_new_running_show(show_name=show_name)
    await manager.broadcast(get_show())
    return status.HTTP_201_CREATED


@app.get('/narrations', response_model=ShowHistory)
async def get_current_show():
    show = get_show()
    if show:
        return Response(show.json(), status_code=200)
    return Response('No show running now', status_code=204)


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
    file = get_show_narration(language_tag)
    return FileResponse(file, media_type='audio/mp3')


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
