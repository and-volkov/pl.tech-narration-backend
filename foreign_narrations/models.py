from datetime import datetime

from pydantic import BaseModel, ValidationError, validator, FilePath
from pydantic_mongo import ObjectIdField


class Narration(BaseModel):
    file_name: str
    file_path: str
    file_size_in_mb: float
    file_length_in_secs: int
    file_extension: str
    record_created: datetime

    @validate('file_path')
    def correct_path(self, v):
        if v is not FilePath:
            raise ValidationError('Incorrect file path')
        return v


class Show(BaseModel):
    id: ObjectIdField = None
    name: str
    narrations: dict[str, Narration]

    class Config:
        json_encoders = {ObjectIdField: str}
