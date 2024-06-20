from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/crawled_data/", response_model=schemas.CrawledData, status_code=201)
def create_crawled_data(crawled_data: schemas.CrawledDataCreate, db: Session = Depends(get_db)):
    return crud.create_crawled_data(db=db, crawled_data=crawled_data)


@app.get("/crawled_data/", response_model=list[schemas.CrawledData])
def read_crawled_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crawled_data = crud.get_crawled_data(db, skip=skip, limit=limit)
    return crawled_data


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="user not found")
#     return db_user
