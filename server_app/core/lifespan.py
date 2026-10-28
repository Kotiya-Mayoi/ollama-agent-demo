from fastapi import FastAPI
from contextlib import asynccontextmanager
from configs.config import OLLAMA_HOST
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 超时给足：非流式模式下，响应时间 = 完整生成耗时
    http_client = httpx.AsyncClient(
        base_url=OLLAMA_HOST,
        timeout=httpx.Timeout(300.0, connect=10.0),
    )
    app.state.http_client = http_client
    yield
    await http_client.aclose()