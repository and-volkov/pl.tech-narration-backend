from datetime import datetime as dt

from pydantic import BaseModel, ValidationError, validator, FilePath
from pydantic_mongo import ObjectIdField


class Narration(BaseModel):
    file_name: str
    file_path: str
    file_size_in_mb: float
    file_length_in_secs: int
    file_extension: str
    record_created: dt

    # @validator('file_path')
    # def correct_path(self, v):
    #     if v is not FilePath:
    #         raise ValidationError('Incorrect file path')
    #     return v
    class Config:
        orm_mode = True


class Show(BaseModel):
    id: ObjectIdField = None
    name: str
    narrations: dict[str, Narration]

    class Config:
        json_encoders = {ObjectIdField: str}
        orm_mode = True


class ShowHistory(BaseModel):
    show_name: str
    available_languages: list[str]
    start_time: int = int(dt.timestamp(dt.now()))
    end_time: int = start_time

    class Config:
        orm_mode = True
