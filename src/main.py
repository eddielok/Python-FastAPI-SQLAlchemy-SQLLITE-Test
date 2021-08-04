from fastapi import FastAPI
import uvicorn
from loguru import logger

app = FastAPI()

@logger.catch()
def run_api():
    logger.info("Codeing Monkey Start Python!")
    uvicorn.run(
        app="api:app",
        port=8080,
        host="0.0.0.0",
        reload=True,
        workers=2,
        access_log=True,
    )

if __name__ == "__main__":
    run_api()
    