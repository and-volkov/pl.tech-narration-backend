import os
from datetime import datetime as dt

import audioread

from database import shows_collection
from models import Narration, Show

DATA_DIR = "../data/"


def prepare_record(filenames: list[str]) -> dict:
    narrations = dict()

    for file in filenames:
        language_tag = file.split("_")[1].split(".")[0].strip()
        file_extension = file.split(".")[1].strip()
        file_path = os.path.abspath(dirpath) + "/" + file
        file_size_in_mb = round(os.stat(file_path).st_size / 1024**2, 2)
        with audioread.audio_open(file_path) as audio:
            file_length_in_ms = audio.duration * 1000

        narrations[language_tag] = Narration(
            file_name=file,
            file_path=file_path,
            file_size_in_mb=file_size_in_mb,
            file_length_ms=file_length_in_ms,
            file_extension=file_extension,
            record_created=dt.strftime(dt.now(), "%d.%m.%y - %H:%M"),
        )
    show_name = filenames[0].split("_")[0].lower()
    return Show(name=show_name, narrations=narrations).dict()


for dirpath, dirname, filenames in os.walk(DATA_DIR):
    if filenames:
        record = prepare_record(filenames)
        shows_collection.replace_one(
            filter={
                'name': record.get('name'),
            },
            replacement=record,
            upsert=True,
        )
