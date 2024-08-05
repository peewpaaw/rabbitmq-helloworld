from fastapi import FastAPI
import asyncio

from rabbitmq import consume_messages

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())


@app.get("/")
async def root():
    return {"message": "Service B"}


@app.get("/messages")
async def get_messages():
    return {"status": "OK"}
    #message = asyncio.create_task(consume_messages())
    #return {"status": "OK", "message": message}

