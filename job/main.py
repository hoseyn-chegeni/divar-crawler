from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
import requests

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, status_code=201, tags=["User"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["User"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["User"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


@app.post(
    "/users/{user_id}/items/",
    response_model=schemas.Job,
    status_code=201,
    tags=["User"],
)
def create_job_for_user(
    user_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)
):
    db_job = crud.create_user_job(db, job=job, user_id=user_id)
    return db_job


@app.get("/jobs/", response_model=list[schemas.Job], tags=["Job"])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.post("/send_job/", tags=["Job"])
def create_job(
    user_id: int,
    city: str = None,
    category: str = None,
    number_of_cards: str = None,
):
    url = "http://crawler_service:8000/jobs/"
    payload = {
        "user_id": user_id,
        "city": city,
        "category": category,
        "number_of_cards": number_of_cards,
    }
    response = requests.post(url, json=payload)

    try:
        response_json = response.json()
    except ValueError:
        raise HTTPException(
            status_code=response.status_code, detail="Invalid JSON response"
        )

    if response.status_code == 201:
        return response_json
    else:
        raise HTTPException(status_code=response.status_code, detail=response_json)


@app.get("/get_status/{job_id}", tags=["Job"])
def get_job_status(job_id: int):
    url = f"http://crawler_service:8000/jobs/{job_id}/status"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
