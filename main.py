import uvicorn
from fastapi import FastAPI
from endpoints import endpoints_register
from db import create_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def main(app: FastAPI):
    await create_db()
    yield

app = FastAPI(lifespan=main)

endpoints_register(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)