from ..registeration.tool_register import TOOL_MAP,AGENT_TOOL_SCHEMA

import logging
logger = logging.getLogger(__name__)

from domain.schemas import chat_message,ChatReply,ToolCall

import httpx,json,asyncio

from ..utils import exceptions

async def agent_main_loop(model_name,msg:chat_message,http_client:httpx.AsyncClient):
    MAX_ITERS= 7
    i =0 

    messages = [{"role": "user", "content": msg.content}]
    tools_called = []
    while i < MAX_ITERS:
        i += 1 
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "tools":AGENT_TOOL_SCHEMA
        }

        try:
            logger.info(f"{i} times to send to model.\n Message sent: {payload}")

            resp = await http_client.post("/api/chat", json=payload)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Ollama 返回的业务错误（如模型不存在）
            raise exceptions.LLMResponseError(
                status_code=e.response.status_code,
                detail=f"Ollama 返回错误: {e.response.text}",
            )
        except httpx.RequestError as e:
            # 连接失败、超时等
            raise exceptions.LLMConnectionError(
                status_code=503,
                detail=f"无法连接 Ollama 服务: {e}",
            )

        try:
            data = resp.json()
        except json.JSONDecodeError:
            raise exceptions.LLMResponseError(status_code=502, detail="Ollama 返回非 JSON 响应")

        if "error" in data:
            raise exceptions.LLMResponseError(status_code=502, detail=f"Ollama 错误: {data['error']}")
        
        message = data.get("message") or {}
        tool_calls = message.get("tool_calls")  # 正确路径

        if not tool_calls:
            return ChatReply(
                content=message.get("content") or "",
                model=data.get("model", model_name),
                tools_called=tools_called
            )

        messages.append(message)

        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            

            # 兼容部分版本返回 JSON 字符串的情况
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError as e:
                    tools_called.append(ToolCall(name=name, arguments={}))
                    messages.append({
                        "role": "tool", "tool_name": name,
                        "content": f"参数不是合法 JSON: {args!r} ({e})",
                    })
                    continue

            if not isinstance(args, dict):
                args = {}

            tools_called.append(ToolCall(name=name, arguments=args,iter_time=i))

            func = TOOL_MAP.get(name)
            if func is None:
                result = f"未知工具: {name}"
            else:
                try:
                    result = await asyncio.to_thread(func, **args)
                except Exception as e:
                    result = f"工具执行失败: {e}"

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": str(result),
            })

    raise exceptions.MaxIterationsError(
        status_code=504,
        detail=f"模型在 {MAX_ITERS} 轮工具调用后仍未给出最终回答",
    )