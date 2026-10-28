from fastapi import APIRouter,HTTPException,Request

from AgentTools.core_loop.agent_loop import agent_main_loop
router = APIRouter()

from domain.schemas import chat_message
from AgentTools.utils.exceptions import LLMConnectionError,LLMResponseError,MaxIterationsError
from configs.config import MODEL_NAME

@router.post("/chat_with_model")
async def chat_with_model(request:Request, msg:chat_message):
    try:
        # 调用纯业务核心
        return await agent_main_loop(MODEL_NAME,msg,request.app.state._state["http_client"])
    except LLMConnectionError as e:
        # 在这里转成 HTTP 503
        raise HTTPException(status_code=503, detail=str(e))
    except LLMResponseError as e:
        # 在这里转成 HTTP 502
        raise HTTPException(status_code=502, detail=str(e))
    except MaxIterationsError as e:
        # 在这里转成 HTTP 504
        raise HTTPException(status_code=504, detail=str(e))