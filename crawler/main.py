from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from bs4 import BeautifulSoup
import requests


# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read multiple crawled data entries with pagination
@app.get(
    "/crawled_data/", response_model=list[schemas.CrawledData], tags=["Crawled Data"]
)
def read_crawled_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_crawled_data(db, skip=skip, limit=limit)


# Read a single crawled data entry by ID
@app.get(
    "/crawled_data/{crawled_data_id}/",
    response_model=schemas.CrawledData,
    tags=["Crawled Data"],
)
def read_crawled_data_by_id(crawled_data_id: int, db: Session = Depends(get_db)):
    db_crawled_data = crud.get_crawled_data_by_id(db, crawled_data_id)
    if db_crawled_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_crawled_data


##########################################
##########################################
##########################################
##########################################
##########################################
##################JOBS####################
##########################################
##########################################
##########################################
##########################################
##########################################


@app.get("/jobs/{job_id}/status", response_model=schemas.JobStatus, tags=["Jobs"])
def get_job_status(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job_status(db, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return schemas.JobStatus(job_id=job.id, status=job.status.value)


@app.get("/jobs/", response_model=list[schemas.Job], tags=["Jobs"])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_jobs(db, skip=skip, limit=limit)


@app.get("/jobs/{job_id}/", response_model=schemas.Job, tags=["Jobs"])
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.get_job_by_id(db, job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@app.get("/jobs/user/{user_id}/", response_model=list[schemas.Job], tags=["Jobs"])
def read_jobs_by_user(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_jobs_by_user_id(db, user_id=user_id, skip=skip, limit=limit)



@app.post("/jobs/", response_model=schemas.Job, status_code=201, tags=["Jobs"])
def create_job(job: schemas.JobCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_job = crud.create_job(db=db, job=job)
    background_tasks.add_task(crawl_page_and_save_data, job.city, job.category, db, db_job.id)
    return db_job

def crawl_page_and_save_data(city: str, category: str, db: Session, job_id: int):
    base_url = "https://divar.ir/s"
    url = f"{base_url}/{city}/{category}"
    response = requests.get(url)

    if response.status_code != 200:
        crud.update_job_status(db, job_id, schemas.JobStatusEnum.failed)
        print(f"Failed to crawl URL: {url} - Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article", class_="kt-post-card")
    titles = []
    for article in articles:
        title_tag = article.find("h2", class_="kt-post-card__title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            titles.append(title)
            # Create a new crawled data entry for each title
            db_crawled_data = schemas.CrawledDataCreate(title=title, url=url, job_id=job_id)
            crud.create_crawled_data(db, db_crawled_data)

    # Update job status to done if crawling is successful
    crud.update_job_status(db, job_id, schemas.JobStatusEnum.done)