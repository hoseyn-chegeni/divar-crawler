from fastapi import FastAPI, Depends, HTTPException
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

# Create a new crawled data entry
@app.post("/crawled_data/", response_model=schemas.CrawledData, status_code=201)
def create_crawled_data(crawled_data: schemas.CrawledDataCreate, db: Session = Depends(get_db)):
    return crud.create_crawled_data(db=db, crawled_data=crawled_data)

# Read multiple crawled data entries with pagination
@app.get("/crawled_data/", response_model=list[schemas.CrawledData])
def read_crawled_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_crawled_data(db, skip=skip, limit=limit)

# Read a single crawled data entry by ID
@app.get("/crawled_data/{crawled_data_id}/", response_model=schemas.CrawledData)
def read_crawled_data_by_id(crawled_data_id: int, db: Session = Depends(get_db)):
    db_crawled_data = crud.get_crawled_data_by_id(db, crawled_data_id)
    if db_crawled_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_crawled_data

# Crawl a title from a given URL
@app.get("/crawl-title/")
def crawl_title(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    
    return {"url": url, "title": title}

# Crawl and store titles from articles on a given URL
@app.get("/crawl/")
def crawl_and_store_titles(url: str, db: Session = Depends(get_db)):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all("article", class_="kt-post-card")
    titles = []
    for article in articles:
        title_tag = article.find("h2", class_="kt-post-card__title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            titles.append(title)
            # Create a new crawled data entry for each title
            crud.create_crawled_data(db, schemas.CrawledDataCreate(title=title))
    
    return {"url": url, "title_count": len(titles), "titles": titles}
