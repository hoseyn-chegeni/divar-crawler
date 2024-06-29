from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

    jobs = relationship("Job", back_populates="owner")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="jobs")

class CrawledData(Base):
    __tablename__ = 'crawled_data'
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
