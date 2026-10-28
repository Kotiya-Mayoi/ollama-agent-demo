import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    # filename="test.log",
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%d-%M-%Y %H:%M:%S", 
    level=logging.INFO
)

from fastapi import FastAPI
from server_app.core.lifespan import lifespan
from server_app.api.v1 import chat_api

app = FastAPI(lifespan=lifespan)
app.include_router(chat_api.router)

