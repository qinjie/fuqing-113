from fastapi import FastAPI, Request
import logging
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router
import uvicorn
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('main')

app = FastAPI()

# origins = ["http://localhost:8000"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root(request: Request):
    logger.info(f'{str(request.url)}\t{request.headers}')
    return {"message": "Event Ops"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, log_level="info", reload = True)
    print("running...")