from pydantic import BaseModel
from typing import Optional

class chat_message(BaseModel):
    content:str

class ToolCall(BaseModel):
    name: str
    arguments: dict
    iter_time:int

class ChatReply(BaseModel):
    content: str
    model: str
    tools_called: Optional[list[ToolCall]] = None