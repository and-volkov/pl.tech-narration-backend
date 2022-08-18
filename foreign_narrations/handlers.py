from datetime import datetime as dt

from database import shows_collection, shows_history_collection
from models import Show, ShowHistory


def insert_new_running_show(show_name: str) -> ShowHistory:
    show = shows_collection.find_one({"name": show_name.lower()})
    show = Show(**show)
    available_languages = list(show.narrations.keys())
    show_len = show.narrations.get("eng").file_length_ms
    start_time = int(dt.timestamp(dt.now())) * 1000
    current_show = ShowHistory(
        show_name=show.name,
        available_languages=available_languages,
        start_time_ms=start_time,
        end_time_ms=start_time + show_len,  # milisecs
    )
    shows_history_collection.drop()
    shows_history_collection.insert_one(current_show.dict())
    return current_show


def get_show() -> ShowHistory | None:
    try:
        last_show = (
            shows_history_collection.find()
            .sort({"end_time": -1, "_id": -1})
            .limit(1)[0]
        )
        last_show = ShowHistory(**last_show)
        if last_show.end_time_ms > dt.now().timestamp():
            return last_show
    except IndexError:
        return None


def get_show_narration(language_tag: str) -> str:
    current_show = get_show()
    show = shows_collection.find_one({"name": current_show.show_name})
    show = Show(**show)
    if current_show:
        narration = show.narrations.get(language_tag)
        return narration.file_path
