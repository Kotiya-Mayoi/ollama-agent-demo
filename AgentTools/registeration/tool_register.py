from AgentTools.tools import demo
import logging
logger = logging.getLogger(__name__)

TOOLS_TO_ADDED = [
    demo
]

TOOL_MAP = {
    # "get_temperature": get_temperature,
    # "get_conditions": get_conditions,
}

AGENT_TOOL_SCHEMA = []

for mod in TOOLS_TO_ADDED:
    mod_name = mod.__name__

    if not hasattr(mod,"OUTPUT_MAPS") or not hasattr(mod,"AGENT_TOOLS"):
        logger.warning(f"{mod_name} 不存在OUTPUT_MAPS或AGENT_TOOLS，跳过。")
        continue

    for name,func in mod.OUTPUT_MAPS.items():
        if name in TOOL_MAP.keys():
            # logger.warning(f"{mod_name} Tool {name} 重复。")
            raise RuntimeError(f"{mod_name} Tool {name} 重复。")
        TOOL_MAP[name] = func

    for tool in mod.AGENT_TOOLS:
        tool_name = tool.get("function" ,{}).get("name")
        if not tool_name in mod.OUTPUT_MAPS:
            raise RuntimeError(f"{tool_name} 在模块 {mod.__name__} 未找到对应实现。")
        AGENT_TOOL_SCHEMA.append(tool)