import asyncio

import uvicorn
from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from handlers import (get_show, get_show_narration, insert_new_running_show,
                      remove_running_show)
from models import ShowHistory
from settings import api_settings

app = FastAPI(title=api_settings.title)


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO separate manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        await get_current_show()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, show: ShowHistory):
        for connection in self.active_connections:
            await asyncio.sleep(0.001)
            await connection.send_json(show.json(), mode="text")


manager = ConnectionManager()


@app.websocket("/api/ws")
async def send_show_notification(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            if msg.lower() == "close":
                await manager.disconnect(websocket)
                await websocket.close()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.post(
    "/api/start/{show_name}",
    responses={200: {"description": "Running show accepted"}},
)
async def get_start_command(show_name: str) -> Response:
    insert_new_running_show(show_name=show_name)
    await manager.broadcast(get_show())
    return status.HTTP_201_CREATED


@app.post("/api/stop/", responses={204: {"description": "Show stopped"}})
async def get_stop_command() -> Response:
    remove_running_show()
    return status.HTTP_204_NO_CONTENT


@app.get(
    "/api/narrations",
    response_model=ShowHistory,
    response_class=Response,
)
async def get_current_show():
    show = get_show()
    if show:
        return Response(
            show.json(),
            status_code=200,
            headers={
                "Cache-Control": "max-age=10",
                "Age": "10",
            },
        )
    return Response("No show running now", status_code=204)


@app.get(
    "/api/narrations/{language_tag}",
    responses={
        403: {"description": "Nothing to return. You die alone"},
    },
)
async def send_narration_file(
    language_tag: str = "eng",
) -> FileResponse | Response:
    file = get_show_narration(language_tag)
    return FileResponse(
        file,
        media_type="audio/mp3",
        headers={
            "content": "audio/mp3",
            "description": "Return narration audio file",
            "Cache-Control": "max-age=10",
            "Age": "10",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=api_settings.host,
        port=api_settings.port,
        log_level=api_settings.log_level.lower(),
        reload=True,
    )
