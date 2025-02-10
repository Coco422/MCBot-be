import asyncio
from typing import Dict, Any
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import os
from pydantic import BaseModel, Field
from dotenv import load_dotenv
# 在程序启动时加载 .env 文件
load_dotenv(override=True)

# Note that the docstrings here are crucial, as they will be passed along
# to the model along with the class name.
class Add(BaseModel):
    """Add two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class Multiply(BaseModel):
    """Multiply two integers together."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b



tools = [Add, Multiply]

# 初始化 ChatOpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("ray_ai_api_key_default"),
    base_url=os.getenv("ray_ai_base_url"),
)

# 创建 Agent
llm_with_tools = llm.bind_tools(tools)

query = "What is 3 * 12? Also, what is 11 + 49? Do not calculate by your self,use tools"

from langchain_core.output_parsers.openai_tools import PydanticToolsParser

chain = llm_with_tools | PydanticToolsParser(tools=[Multiply, Add])


async def test():
    async for chunk in llm_with_tools.astream(query):
        print(chunk.tool_call_chunks)
    # llm.invoke("hello word")
    
if __name__ == "__main__":
    asyncio.run(test())