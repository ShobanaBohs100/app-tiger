from fastapi import FastAPI, BackgroundTasks
import os
import logging
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("python-logger")

app = FastAPI()
VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.get("/")
def read_root():
    return {"status": "healthy", "version": VERSION, "message": "ok"}

# 🔴 TRUE CRASH: The Fatal Exit
@app.get("/fatal-crash")
def fatal_crash():
    """Immediately kills the Python process, forcing a K8s Pod Restart."""
    logger.error("ERROR: Fatal system corruption detected. Process exiting immediately.")
    
    # Force the log to flush to the console before we die, so Loki catches it
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.5) 
    
    # os._exit bypasses all try/except blocks and instantly kills the container
    os._exit(1)

# 🔴 TRUE OOM: The Memory Black Hole
@app.get("/true-oom")
def true_oom(background_tasks: BackgroundTasks):
    """Allocates memory infinitely until the Linux OS kills the container."""
    logger.error("ERROR: Memory limit exceeded. Runaway memory leak initiated.")
    sys.stderr.flush()

    def black_hole():
        junk_data = []
        while True:
            # Append 100MB of string data per loop until the system kills us
            junk_data.append(' ' * 10**8) 
            time.sleep(0.1)

    # Run in the background so the HTTP request returns right as the pod starts dying
    background_tasks.add_task(black_hole)
    return {"message": "Memory leak started. Watch the pod crash in a few seconds."}

# docker build -t sre-test-app:local .
# docker run -p 8090:8090 sre-test-app:local