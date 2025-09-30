"""
大语言模型调用服务模块
"""
from typing import AsyncGenerator, List, Dict
from openai import AsyncOpenAI
import json


async def stream_llm_response(
    provider: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    messages: List[Dict[str, str]]
) -> AsyncGenerator[str, None]:
    """
    流式调用大语言模型
    
    Args:
        provider: LLM 供应商 (deepseek, qwen 等)
        api_key: API Key
        model_id: 模型 ID
        system_prompt: 系统提示词
        messages: 消息历史
        
    Yields:
        流式响应的文本片段
    """
    # 根据供应商设置 base_url
    base_url_map = {
        "deepseek": "https://api.deepseek.com",
        "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "openai": "https://api.openai.com/v1",
    }
    
    base_url = base_url_map.get(provider, "https://api.openai.com/v1")
    
    # 创建 OpenAI 客户端
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    # 构建消息列表
    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)
    
    try:
        # 流式调用
        stream = await client.chat.completions.create(
            model=model_id,
            messages=full_messages,
            stream=True,
            temperature=0.7,
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        yield f"\n\n[错误] 调用大模型失败: {str(e)}"


async def test_llm_connection(
    provider: str,
    api_key: str,
    model_id: str
) -> tuple[bool, str]:
    """
    测试大语言模型连接
    
    Args:
        provider: LLM 供应商
        api_key: API Key
        model_id: 模型 ID
        
    Returns:
        (是否成功, 消息)
    """
    # 根据供应商设置 base_url
    base_url_map = {
        "deepseek": "https://api.deepseek.com",
        "qwen": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "openai": "https://api.openai.com/v1",
    }
    
    base_url = base_url_map.get(provider, "https://api.openai.com/v1")
    
    # 创建 OpenAI 客户端
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    try:
        # 发送测试请求
        response = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=10
        )
        
        return True, "连接成功！模型响应正常。"
        
    except Exception as e:
        return False, f"连接失败: {str(e)}"

