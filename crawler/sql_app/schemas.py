from pydantic import BaseModel


class CrawledDataBase(BaseModel):
    title: str
    content: str


class CrawledDataCreate(CrawledDataBase):
    pass


class CrawledData(CrawledDataBase):
    id: int

    class Config:
        orm_mode = True
