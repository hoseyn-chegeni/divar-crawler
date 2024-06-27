from pydantic import BaseModel
from enum import Enum


class CrawledDataBase(BaseModel):
    title: str
    url: str | None = None
    description_text: str | None = None
    image_url: str | None = None
    district_persian: str | None = None
    city_persian: str | None = None
    category_slug_persian: bool = False
    has_chat: bool = False
    token: str | None = None
    category: str | None = None

    class Config:
        orm_mode = True


class CrawledDataCreate(CrawledDataBase):
    pass


class CrawledData(CrawledDataBase):
    id: int


class JobStatus(str, Enum):
    in_queue = "in_queue"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class JobBase(BaseModel):
    user_id: int
    city: str | None = None
    category: str | None = None
    number_of_cards: str | None = None
    status: JobStatus = JobStatus.in_queue

    class Config:
        orm_mode = True


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int


class JobStatusEnum(str, Enum):
    in_queue = "in_queue"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"


class JobStatus(BaseModel):
    job_id: int
    status: JobStatusEnum

class JobUpdateStatus(BaseModel):
    status: JobStatusEnum