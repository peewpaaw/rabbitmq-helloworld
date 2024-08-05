import asyncio
import uuid

from fastapi import FastAPI, HTTPException, BackgroundTasks

from rabbitmq import send_message, receive_response
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    message: str

responses = {}

@app.get("/")
async def root():
    return {"message": "service A"}


@app.post("/send_message")
async def send_message_endpoint(body: Message, background_tasks: BackgroundTasks):
    correlation_id = str(uuid.uuid4())
    responses[correlation_id] = asyncio.Future()
    await send_message(body.message, correlation_id)
    background_tasks.add_task(receive_response, correlation_id)
    return {"message": "processing started", "correlation_id": correlation_id}
    # try:
    #     await send_message(body.message)
    # except Exception as e:
    #     raise HTTPException(status_code=503, detail="Something went wrong")
    # return {"status": "OK"}


@app.get("/result")
async def get_result(correlation_id: str):
    if correlation_id in responses:
        response = await responses[correlation_id]
        return response
    return {"message": "Invalid correlation ID"}

