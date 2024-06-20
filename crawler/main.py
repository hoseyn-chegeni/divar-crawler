from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/crawls")
def read_crawls():
    response = requests.get("http://job_service:8001/jobs")
    return {"message": "This is the crawler service", "jobs_response": response.json()}
