import dataclasses
import datetime

import rio


@dataclasses.dataclass
class TodoItem:
    title: str
    creation_time: datetime.datetime
    completed: bool = False


@dataclasses.dataclass
class JobListing:
    job_id: str
    position: str
    company: str
    location: str
    salary_min: int | None
    salary_max: int | None
    date: str
    url: str
    tags: str


class TodoAppSettings(rio.UserSettings):
    todo_items: list[TodoItem] = [
        TodoItem(
            title="write the code",
            creation_time=datetime.datetime.now(),
        ),
    ]