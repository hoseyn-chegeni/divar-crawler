from sqlalchemy.orm import Session
from .models import User, Job,CrawledData
from .schemas import UserCreate, JobCreate, CrawledDataCreate,CrawledDataBase


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()


def create_user_job(db: Session, job: JobCreate, user_id: int):
    db_job = Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job



#########
#CRAWLED DATA C.R.U.D
#########

def get_crawled_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CrawledData).offset(skip).limit(limit).all()


def get_crawled_data_by_id(db: Session, data_id: int):
    return db.query(CrawledData).filter(CrawledData.id == data_id).first()


def create_crawled_data(db: Session, crawled_data: CrawledDataCreate):
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
    db_crawled_data = db.query(CrawledData).filter(CrawledData.id == data_id).first()
    if not db_crawled_data:
        return None

    for key, value in crawled_data.dict(exclude_unset=True).items():
        setattr(db_crawled_data, key, value)

    db.commit()
    db.refresh(db_crawled_data)
    return db_crawled_data


def delete_crawled_data(db: Session, data_id: int):
    db_crawled_data = db.query(CrawledData).filter(CrawledData.id == data_id).first()
    if not db_crawled_data:
        return None

    db.delete(db_crawled_data)
    db.commit()
    return db_crawled_data