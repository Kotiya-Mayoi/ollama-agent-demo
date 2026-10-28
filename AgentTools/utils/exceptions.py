class AgentBaseError(Exception):
    """Agent 业务基础异常"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        # 调用父类 Exception 的初始化，这样打印错误时能直接看到 detail
        super().__init__(detail)

class MaxIterationsError(AgentBaseError):
    """达到最大循环次数"""
    pass

class LLMConnectionError(AgentBaseError):
    """无法连接 LLM 服务"""
    pass

class LLMResponseError(AgentBaseError):
    """LLM 返回了错误数据"""
    pass