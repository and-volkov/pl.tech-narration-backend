from datetime import datetime as dt

from database import shows_collection, shows_history_collection
from models import Narration, Show, ShowHistory


def insert_new_running_show(show_name: str) -> ShowHistory:
    show = shows_collection.find_one({'name': show_name.upper()})
    show = Show(**show)
    available_languages = list(show.narrations.keys())
    show_len = show.narrations.get('eng').file_length_in_secs
    current_show = ShowHistory(
        show_name=show.name,
        available_languages=available_languages,
        end_time=int(dt.timestamp(dt.now())) + show_len,
    )
    shows_history_collection.insert_one(current_show.dict())
    return current_show


def get_show() -> ShowHistory | None:
    last_show = (
        shows_history_collection.find().sort('end_time', -1).limit(1)[0]
    )
    last_show = ShowHistory(**last_show)
    if last_show.end_time > dt.now().timestamp():
        return last_show


def get_show_narration(language_tag: str) -> str:
    current_show = get_show()
    show = shows_collection.find_one({'name': current_show.show_name})
    show = Show(**show)
    if current_show:
        narration = show.narrations.get(language_tag)
        return narration.file_path
