from fastapi import FastAPI

app = FastAPI()

@app.get("/jobs")
def read_jobs():
    return {"message": "This is the job service"}
