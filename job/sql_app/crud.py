from sqlalchemy.orm import Session
from .models import User, Job
from .schemas import UserCreate, JobCreate

def get_user(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()


def get_users(db:Session, skip:int = 0, limit:int = 100):
    return db.query(User).offset(skip).limit(limit).all()



def create_user(db:Session, user:UserCreate):
    db_user = User(email = user.email,)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_jobs(db:Session, skip:int = 0, limit:int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

def create_user_job(db: Session, job: JobCreate, user_id: int):
    db_job = Job(**job.dict(), owner_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

