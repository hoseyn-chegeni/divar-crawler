from sqlalchemy import Column, Integer, String, Boolean, Enum
from .database import Base
import enum

class JobStatus(enum.Enum):
    in_queue = "in_queue"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"

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

class Job (Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    city = Column(String, nullable=True)
    category = Column(String, nullable=True)
    number_of_cards = Column(String, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.in_queue)