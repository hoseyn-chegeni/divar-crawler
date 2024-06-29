from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from .database import Base
import enum
from sqlalchemy.orm import relationship

class JobStatus(enum.Enum):
    in_queue = "in_queue"
    in_progress = "in_progress"
    done = "done"
    failed = "failed"

class Job(Base):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    city = Column(String, nullable=True)
    category = Column(String, nullable=True)
    number_of_cards = Column(String, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.in_queue)
    crawled_data = relationship("CrawledData", back_populates="job")


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
    job_id = Column(Integer, ForeignKey("job.id"))

    job = relationship("Job", back_populates="crawled_data")
