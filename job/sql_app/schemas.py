from pydantic import BaseModel
from typing import List, Optional

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
    job_id: Optional[int] = None

    class Config:
        orm_mode = True


class CrawledDataCreate(CrawledDataBase):
    pass


class CrawledData(CrawledDataBase):
    id: int



class JobBase(BaseModel):
    title: str
    description: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    user_id: int
    crawled_data: List[CrawledData] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    jobs: list[Job] = []

    class Config:
        orm_mode = True

