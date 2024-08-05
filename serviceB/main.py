from fastapi import FastAPI
import asyncio

from rabbitmq import consume_messages

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Service B"}


@app.get("/messages")
async def get_messages():
    asyncio.create_task(consume_messages())


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
