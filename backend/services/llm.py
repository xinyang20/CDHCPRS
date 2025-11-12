"""
大语言模型调用服务模块
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncGenerator, Dict, List, Optional, Tuple

from openai import AsyncOpenAI


class LLMServiceError(RuntimeError):
    """自定义异常：LLM 供应商配置错误"""


@dataclass(frozen=True)
class ProviderConfig:
    """LLM 供应商配置"""

    key: str
    default_base_url: Optional[str] = None
    requires_base_url: bool = False


_PROVIDER_REGISTRY: Dict[str, ProviderConfig] = {
    "deepseek": ProviderConfig(
        key="deepseek",
        default_base_url="https://api.deepseek.com/v1",
    ),
    "qwen": ProviderConfig(
        key="qwen",
        default_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
    "openai": ProviderConfig(
        key="openai",
        default_base_url="https://api.openai.com/v1",
    ),
    "openaiful": ProviderConfig(
        key="openaiful",
        requires_base_url=True,
    ),
    "dify": ProviderConfig(
        key="dify",
        requires_base_url=True,
    ),
}


def _normalize_base_url(raw: str) -> str:
    """清洗并标准化 Base URL"""

    cleaned = raw.strip()
    if not cleaned:
        raise LLMServiceError("Base URL 不能为空")

    cleaned = cleaned.rstrip("/")
    if not cleaned.lower().endswith("/v1"):
        cleaned = f"{cleaned}/v1"
    return cleaned


def _resolve_base_url(provider: str, override: Optional[str]) -> str:
    """获取最终使用的 Base URL"""

    normalized_provider = provider.lower().strip()

    if override and override.strip():
        return _normalize_base_url(override)

    config = _PROVIDER_REGISTRY.get(normalized_provider)
    if not config:
        raise LLMServiceError("未配置的 LLM 供应商，请在系统设置中填写完整的连接信息。")

    if config.default_base_url:
        return config.default_base_url

    if config.requires_base_url:
        raise LLMServiceError("该供应商需要填写 Base URL，请前往系统设置补全后重试。")

    raise LLMServiceError("无法解析 Base URL，请检查供应商配置。")


def _create_async_client(
    provider: str,
    api_key: str,
    base_url: Optional[str] = None,
) -> AsyncOpenAI:
    """构建异步 OpenAI 客户端"""

    resolved_base_url = _resolve_base_url(provider, base_url)
    return AsyncOpenAI(api_key=api_key, base_url=resolved_base_url)


async def stream_llm_response(
    provider: str,
    api_key: str,
    model: str,
    system_prompt: str,
    messages: List[Dict[str, str]],
    base_url: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    """流式调用大语言模型，返回内容片段"""

    full_messages = [{"role": "system", "content": system_prompt}]
    full_messages.extend(messages)

    try:
        client = _create_async_client(provider, api_key, base_url)
    except LLMServiceError as exc:
        yield f"\n\n[错误] {exc}"
        return

    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=full_messages,
            stream=True,
            temperature=0.7,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    except Exception as exc:  # noqa: BLE001
        yield f"\n\n[错误] 调用大模型失败: {exc}"


async def test_llm_connection(
    provider: str,
    api_key: str,
    model: str,
    base_url: Optional[str] = None,
) -> Tuple[bool, str]:
    """测试与 LLM 供应商的连通性"""

    try:
        client = _create_async_client(provider, api_key, base_url)
    except LLMServiceError as exc:
        return False, str(exc)

    try:
        await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "你好"}],
            max_tokens=10,
        )
        return True, "连接成功，模型响应正常。"
    except Exception as exc:  # noqa: BLE001
        return False, f"连接失败: {exc}"


async def list_llm_models(
    provider: str,
    api_key: str,
    base_url: Optional[str] = None,
) -> Tuple[bool, List[Dict[str, Optional[str]]], Optional[str]]:
    """从供应商获取模型列表"""

    try:
        client = _create_async_client(provider, api_key, base_url)
    except LLMServiceError as exc:
        return False, [], str(exc)

    try:
        response = await client.models.list()
        models: List[Dict[str, Optional[str]]] = []

        for model in response.data:
            model_id = getattr(model, "id", None)
            model_name = getattr(model, "name", None) or model_id
            models.append(
                {
                    "id": model_id,
                    "name": model_name,
                    "owned_by": getattr(model, "owned_by", None),
                }
            )

        if not models:
            return False, [], "未获取到任何模型，请检查 API Key 与权限配置。"

        return True, models, None
    except Exception as exc:  # noqa: BLE001
        return False, [], f"获取模型列表失败: {exc}"
