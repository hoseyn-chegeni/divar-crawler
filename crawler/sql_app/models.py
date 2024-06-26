from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class CrawledData(Base):
    __tablename__ = "crawled_data"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String)
    description_text = Column(String)
    image_url = Column(String)
    district_persian =  Column(String)
    city_persian = Column(String)
    category_slug_persian = Column(String)
    has_chat = Column(Boolean)
    token = Column(Boolean)
    category = Column(String)