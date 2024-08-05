from fastapi import FastAPI

#from serviceA.rabbitmq import send_message
from rabbitmq import send_message

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "service A"}


@app.post("/send_message")
async def send_message_endpoint():
    await send_message("message from service A")



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
