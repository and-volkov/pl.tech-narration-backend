import os
from datetime import datetime as dt

import audioread

from database import shows_collection
from models import Narration, Show

DATA_DIR = '../data/'

sub_folders = [f.path for f in os.scandir(DATA_DIR) if f.is_dir()]

for folder in sub_folders:
    filenames = next(os.walk(folder), (None, None, []))[2]  # files
    narrations = dict()
    for file in filenames:
        f = file.split('_')[-1]
        language_tag = f.split('.')[0].strip()
        file_extension = f.split('.')[1].strip()
        file_path = os.path.abspath(folder) + '/' + file
        file_size_in_mb = round(os.stat(file_path).st_size / 1024**2, 2)
        with audioread.audio_open(file_path) as audio:
            file_length_in_secs = round(audio.duration)
        narrations[language_tag] = Narration(
            file_name=file,
            file_path=file_path,
            file_size_in_mb=file_size_in_mb,
            file_length_in_secs=file_length_in_secs,
            file_extension=file_extension,
            record_created=dt.today(),
        )
    record = Show(
        name=folder.split('/')[-1].lower(), narrations=narrations
    ).dict()
    shows_collection.replace_one(
        filter={'name': record.get('name')}, replacement=record, upsert=True
    )
