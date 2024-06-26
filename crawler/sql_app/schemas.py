from pydantic import BaseModel

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
