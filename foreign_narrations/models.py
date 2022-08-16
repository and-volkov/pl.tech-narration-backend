from datetime import datetime as dt

from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class Narration(BaseModel):
    file_name: str
    file_path: str
    file_size_in_mb: float
    file_length_miliseconds: int
    file_extension: str
    record_created: dt


class Show(BaseModel):
    id: ObjectIdField = None
    name: str
    narrations: dict[str, Narration]

    class Config:
        json_encoders = {ObjectIdField: str}


class ShowHistory(BaseModel):
    show_name: str
    available_languages: list[str]
    start_time: int = int(dt.timestamp(dt.now()))
    end_time: int = start_time
