from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class CrawledData(Base):
    __tablename__ = "crawled_data"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, nullable=True)
    description_text = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    district_persian = Column(String, nullable=True)
    city_persian = Column(String, nullable=True)
    category_slug_persian = Column(Boolean, default=False)
    has_chat = Column(Boolean, default=False)
    token = Column(String, nullable=True)
    category = Column(String, nullable=True)