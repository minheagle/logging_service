from fastapi import FastAPI, Request, HTTPException
import uvicorn
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from model.log import Log

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

current_date = datetime.now().strftime("%Y-%m-%d")
log_file_name = f"logs/{current_date}.log"

file_handler = TimedRotatingFileHandler(log_file_name, when="midnight", backupCount=7, encoding="utf-8")
file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Logging service !"}

@app.post("/logs")
async def create_log(log: Log):    
    try:        
        if log:
            logger.info(f"\"Method : {log.method} , Path : {log.path}\"")
            return {"status": "success", "message": "Log created successfully"}
        else:
            raise HTTPException(status_code=400, detail="Log message is missing")
    except Exception as e:
        logger.error(f"Error while processing log request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def run():
    uvicorn.run(
        app="app:app",
        host="127.0.0.1",
        port=4567,
        reload=True
    )

if __name__ == "__main__":
    run()