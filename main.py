from fastapi import FastAPI
import os

app = FastAPI()
VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.get("/")
def read_root():
    return {"status": "healthy", "version": VERSION, "message": "All systems nominal."}

# docker build -t sre-test-app:local .
# docker run -p 8090:8090 sre-test-app:local