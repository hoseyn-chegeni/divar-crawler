from sqlalchemy import  Column,  Integer, String
from .database import Base


class CrawledData(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)



