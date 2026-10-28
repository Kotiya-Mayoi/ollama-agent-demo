import logging
from functools import wraps

logger = logging.getLogger(__name__)

cities_map = {
    "伦敦":"London",
    "纽约":"New York",
    "东京":"Tokyo",
}

def wrapper_normalize_city_names(func):
    @wraps(func)
    def wrapper(city,*args,**kwargs):
        if isinstance(city, dict):
            city = city.get("value", "")
        city_str = str(city).strip()
        city_str = cities_map.get(city_str, city_str)
        return func(city_str, *args, **kwargs)
    return wrapper

@wrapper_normalize_city_names
def get_temperature(city: str) -> str:
    """获取指定城市的当前温度"""

    logger.info(f"get_temperature arg: {city}")
    
    return {
        "New York": "22°C",
        "London": "15°C",
        "Tokyo": "18°C",
    }.get(city, "未收录 仅支持 New York,London,Tokyo 请检查拼写是否使用了同义词或未翻译？")

@wrapper_normalize_city_names
def get_conditions(city: str) -> str:
    """获取指定城市的天气状况"""
    logger.info(f"get_conditions arg: {city}")
    return {
        "New York": "Partly cloudy",
        "London": "Rainy",
        "Tokyo": "Sunny",
    }.get(city, "未收录 仅支持 New York,London,Tokyo 请检查拼写是否使用了同义词或未翻译？")

# 工具清单（JSON Schema），传给 Ollama 的 tools 参数
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_temperature",
            "description": "获取指定城市的当前温度",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {"type": "string", "description": "城市名称，如 'New York'"}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_conditions",
            "description": "获取指定城市的天气状况",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
            },
        },
    },
]

OUTPUT_MAPS = {
    "get_temperature": get_temperature,
    "get_conditions": get_conditions,
}

if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    c = get_conditions("伦敦")
    pass