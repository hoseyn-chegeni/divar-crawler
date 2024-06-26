from sqlalchemy.orm import Session
from .models import CrawledData
from .schemas import CrawledDataCreate, CrawledDataBase


def get_crawled_data(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of crawled data from the database with optional pagination."""
    return db.query(CrawledData).offset(skip).limit(limit).all()


def get_crawled_data_by_id(db: Session, data_id: int):
    """Fetch a single crawled data entry by its ID."""
    return db.query(CrawledData).filter(CrawledData.id == data_id).first()


def create_crawled_data(db: Session, crawled_data: CrawledDataCreate):
    """Create a new crawled data entry in the database."""
    db_crawled_data = CrawledData(
        title=crawled_data.title,
        url=crawled_data.url,
        description_text=crawled_data.description_text,
        image_url=crawled_data.image_url,
        district_persian=crawled_data.district_persian,
        city_persian=crawled_data.city_persian,
        category_slug_persian=crawled_data.category_slug_persian,
        has_chat=crawled_data.has_chat,
        token=crawled_data.token,
        category=crawled_data.category,
    )
    db.add(db_crawled_data)
    db.commit()
    db.refresh(db_crawled_data)
    return db_crawled_data


def update_crawled_data(db: Session, data_id: int, crawled_data: CrawledDataBase):
    """Update an existing crawled data entry in the database."""
    db_crawled_data = db.query(CrawledData).filter(CrawledData.id == data_id).first()
    if not db_crawled_data:
        return None

    for key, value in crawled_data.dict(exclude_unset=True).items():
        setattr(db_crawled_data, key, value)

    db.commit()
    db.refresh(db_crawled_data)
    return db_crawled_data


def delete_crawled_data(db: Session, data_id: int):
    """Delete a crawled data entry from the database by its ID."""
    db_crawled_data = db.query(CrawledData).filter(CrawledData.id == data_id).first()
    if not db_crawled_data:
        return None

    db.delete(db_crawled_data)
    db.commit()
    return db_crawled_data
