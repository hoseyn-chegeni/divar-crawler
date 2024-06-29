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



#DELETE AND READ CRAWLED DATA BY JOB ID 
@app.get("/crawled_data/by_job/{job_id}", response_model=list[schemas.CrawledData], tags=["Crawled Data By Job"])
def read_crawled_data_by_job(job_id: int, db: Session = Depends(get_db)):
    crawled_data = crud.get_crawled_data_by_job(db, job_id=job_id)
    if not crawled_data:
        raise HTTPException(status_code=404, detail="CrawledData not found")
    return crawled_data

@app.delete("/crawled_data/by_job/{job_id}", response_model=list[schemas.CrawledData], tags=["Crawled Data By Job"])
def delete_crawled_data_by_job(job_id: int, db: Session = Depends(get_db)):
    crawled_data = crud.delete_crawled_data_by_job(db, job_id=job_id)
    if not crawled_data:
        raise HTTPException(status_code=404, detail="CrawledData not found")
    return crawled_data

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
    background_tasks.add_task(crawl_page_and_save_data, job.city, job.category, db_job.id)
    return db_job

def crawl_page_and_save_data(city: str, category: str, job_id: int):
    base_url = "https://divar.ir/s"
    url = f"{base_url}/{city}/{category}"
    response = requests.get(url)

    db = SessionLocal()

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

    # Fetch crawled data and send to job_service
    send_data_to_job_service(job_id, db)

    db.close()

def send_data_to_job_service(job_id: int, db: Session):
    crawler_service_url = f"http://crawler_service:8000/crawled_data/by_job/{job_id}"

    # Fetch crawled data from crawler_service
    response = requests.get(crawler_service_url)
    if response.status_code != 200:
        print(f"Failed to fetch crawled data for job ID {job_id} - Status code: {response.status_code}")
        return

    crawled_data = response.json()
    for data in crawled_data:
        job_service_url = "http://job_service:8001/crawled_data/"
        response = requests.post(job_service_url, json=data)
        if response.status_code == 201:
            print(f"Successfully sent crawled data to job service for job ID {job_id}")
        else:
            print(f"Failed to send crawled data to job service for job ID {job_id} - Status code: {response.status_code}")

    # Now delete the crawled data from crawler_service
    delete_url = f"http://crawler_service:8000/crawled_data/by_job/{job_id}"
    response = requests.delete(delete_url)
    if response.status_code != 200:
        print(f"Failed to delete crawled data for job ID {job_id} - Status code: {response.status_code}")
    else:
        print(f"Successfully deleted crawled data for job ID {job_id}")
