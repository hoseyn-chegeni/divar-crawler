from sqlalchemy.orm import Session
from .models import CrawledData
from .schemas import CrawledDataCreate



def get_crawled_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CrawledData).offset(skip).limit(limit).all()


def create_crawled_data(db: Session, crawled_data: CrawledDataCreate):
    db_crawled_data = CrawledData(
        title=crawled_data.title,
        content=crawled_data.content,

    )
    db.add(db_crawled_data)
    db.commit()
    db.refresh(db_crawled_data)
    return db_crawled_data