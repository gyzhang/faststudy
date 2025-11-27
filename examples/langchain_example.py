"""
LangChain 示例代码
演示基本的 LLM 调用和链功能
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatResult, ChatGenerationChunk
from typing import Optional, List, Dict, Any, Iterator
import requests
import json


class CustomChatModel(BaseChatModel):
    """
    自定义 ChatModel，用于调用外部 API
    """
    
    def __init__(self, temperature: float = 0.7, auth_token: Optional[str] = None):
        """
        初始化自定义 ChatModel
        
        Args:
            temperature: 温度参数
            auth_token: 认证令牌
        """
        super().__init__()
        self.temperature = temperature
        self.auth_token = auth_token
    
    @property
    def temperature(self) -> float:
        """
        温度参数
        
        Returns:
            float: 温度参数
        """
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        """
        设置温度参数
        
        Args:
            value: 温度参数
        """
        self._temperature = value
    
    @property
    def auth_token(self) -> Optional[str]:
        """
        认证令牌
        
        Returns:
            Optional[str]: 认证令牌
        """
        return self._auth_token
    
    @auth_token.setter
    def auth_token(self, value: Optional[str]) -> None:
        """
        设置认证令牌
        
        Args:
            value: 认证令牌
        """
        self._auth_token = value
    
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> ChatResult:
        """
        生成响应
        
        Args:
            messages: 消息列表
            stop: 停止词列表
            **kwargs: 其他参数
            
        Returns:
            ChatResult: 响应结果
        """
        # 设置API端点
        url = "http://10.62.79.254:31111/api/inference/v1/chat/completions"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # 转换消息格式
        api_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                api_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                api_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, AIMessage):
                api_messages.append({"role": "assistant", "content": msg.content})
        
        # 准备请求体
        data = {
            "model": "Qwen3-235B-MOE",
            "messages": api_messages,
            "temperature": self.temperature,
            "max_tokens": 32768
        }
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data)
        )
        
        # 处理响应
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            # 创建 ChatResult
            chat_generation = ChatGeneration(
                message=AIMessage(content=content),
                generation_info={"finish_reason": result.get("choices", [{}])[0].get("finish_reason", "stop")}
            )
            
            return ChatResult(generations=[chat_generation])
        else:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
    
    def _stream(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> Iterator[ChatGenerationChunk]:
        """
        流式生成响应
        
        Args:
            messages: 消息列表
            stop: 停止词列表
            **kwargs: 其他参数
            
        Yields:
            ChatGenerationChunk: 流式响应块
        """
        # 设置API端点
        url = "http://10.62.79.254:31111/api/inference/v1/chat/completions"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # 转换消息格式
        api_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                api_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                api_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, AIMessage):
                api_messages.append({"role": "assistant", "content": msg.content})
        
        # 准备请求体
        data = {
            "model": "Qwen3-235B-MOE",
            "messages": api_messages,
            "temperature": self.temperature,
            "max_tokens": 32768,
            "stream": True
        }
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            stream=True
        )
        
        # 处理响应
        if response.status_code == 200:
            # 逐行处理流式响应
            for line in response.iter_lines():
                if line:
                    # 移除 "data: " 前缀
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                    
                    # 检查是否是结束标记
                    if line == "[DONE]":
                        break
                    
                    try:
                        # 解析JSON
                        result = json.loads(line)
                        delta = result.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        
                        if content:
                            # 创建 ChatGenerationChunk
                            chunk = ChatGenerationChunk(
                                message=AIMessageChunk(content=content),
                                generation_info={"finish_reason": delta.get("finish_reason")}
                            )
                            yield chunk
                    except json.JSONDecodeError:
                        continue
        else:
            raise Exception(f"API请求失败: {response.status_code} - {response.text}")
    
    @property
    def _llm_type(self) -> str:
        """
        LLM 类型
        
        Returns:
            str: LLM 类型
        """
        return "custom_chat_model"
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """
        识别参数
        
        Returns:
            Dict[str, Any]: 识别参数
        """
        return {
            "temperature": self.temperature
        }


def get_llm(model_name: str = "gpt-3.5-turbo", temperature: float = 0.7, auth_token: Optional[str] = None):
    """
    获取 LLM 实例
    
    Args:
        model_name: 模型名称（仅用于兼容，实际使用自定义模型）
        temperature: 温度参数
        auth_token: 认证令牌
        
    Returns:
        CustomChatModel: LLM 实例
    """
    return CustomChatModel(
        temperature=temperature,
        auth_token=auth_token
    )


def simple_llm_call(prompt: str, model_name: str = "gpt-3.5-turbo", auth_token: Optional[str] = None) -> str:
    """
    简单的 LLM 调用
    
    Args:
        prompt: 提示词
        model_name: 模型名称
        auth_token: 认证令牌
        
    Returns:
        str: LLM 响应
    """
    llm = get_llm(model_name, auth_token=auth_token)
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)


def simple_llm_call_stream(prompt: str, model_name: str = "gpt-3.5-turbo", auth_token: Optional[str] = None) -> Iterator[str]:
    """
    简单的 LLM 调用（流式输出）
    
    Args:
        prompt: 提示词
        model_name: 模型名称
        auth_token: 认证令牌
        
    Yields:
        str: LLM 响应的流式输出
    """
    llm = get_llm(model_name, auth_token=auth_token)
    for chunk in llm.stream(prompt):
        yield chunk.content if hasattr(chunk, "content") else str(chunk)


def create_simple_chain(auth_token: Optional[str] = None):
    """
    创建简单的链
    
    Args:
        auth_token: 认证令牌
        
    Returns:
        Runnable: 链实例
    """
    # 定义提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 helpful 的助手。请用中文回答。"),
        ("user", "{input}")
    ])
    
    # 获取 LLM
    llm = get_llm(auth_token=auth_token)
    
    # 定义输出解析器
    output_parser = StrOutputParser()
    
    # 创建链
    chain = prompt | llm | output_parser
    
    return chain


def run_simple_chain(input_text: str, auth_token: Optional[str] = None) -> str:
    """
    运行简单的链
    
    Args:
        input_text: 输入文本
        auth_token: 认证令牌
        
    Returns:
        str: 链的输出
    """
    chain = create_simple_chain(auth_token=auth_token)
    return chain.invoke({"input": input_text})


def run_simple_chain_stream(input_text: str, auth_token: Optional[str] = None) -> Iterator[str]:
    """
    运行简单的链（流式输出）
    
    Args:
        input_text: 输入文本
        auth_token: 认证令牌
        
    Yields:
        str: 链的输出的流式输出
    """
    chain = create_simple_chain(auth_token=auth_token)
    for chunk in chain.stream({"input": input_text}):
        yield chunk


def create_translation_chain(auth_token: Optional[str] = None):
    """
    创建翻译链
    
    Args:
        auth_token: 认证令牌
        
    Returns:
        Runnable: 翻译链实例
    """
    # 定义翻译提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的翻译助手。请将用户输入的文本翻译成英文。"),
        ("user", "{text}")
    ])
    
    # 获取 LLM
    llm = get_llm(auth_token=auth_token)
    
    # 定义输出解析器
    output_parser = StrOutputParser()
    
    # 创建翻译链
    translation_chain = prompt | llm | output_parser
    
    return translation_chain


def translate_text(text: str, auth_token: Optional[str] = None) -> str:
    """
    翻译文本
    
    Args:
        text: 要翻译的文本
        auth_token: 认证令牌
        
    Returns:
        str: 翻译后的文本
    """
    translation_chain = create_translation_chain(auth_token=auth_token)
    return translation_chain.invoke({"text": text})


def translate_text_stream(text: str, auth_token: Optional[str] = None) -> Iterator[str]:
    """
    翻译文本（流式输出）
    
    Args:
        text: 要翻译的文本
        auth_token: 认证令牌
        
    Yields:
        str: 翻译后的文本的流式输出
    """
    translation_chain = create_translation_chain(auth_token=auth_token)
    for chunk in translation_chain.stream({"text": text}):
        yield chunk


def validate_model(auth_token: str, prompt: str = "介绍一下你自己。") -> dict:
    """
    验证模型是否可用
    
    Args:
        auth_token: 认证令牌 (API key)
        prompt: 测试提示词
        
    Returns:
        dict: 包含响应结果和状态信息
    """
    try:
        # 设置API端点
        url = "http://10.62.79.254:31111/api/inference/v1/chat/completions"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        # 准备请求体
        data = {
            "model": "Qwen3-235B-MOE",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 32768
        }
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data)
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "content": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "response": result
            }
        else:
            return {
                "success": False,
                "error": f"API请求失败: {response.status_code}",
                "content": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"请求过程中发生错误: {str(e)}",
            "content": str(e)
        }


def validate_model_stream(auth_token: str, prompt: str = "介绍一下你自己。") -> Iterator[str]:
    """
    验证模型是否可用（流式输出）
    
    Args:
        auth_token: 认证令牌 (API key)
        prompt: 测试提示词
        
    Yields:
        str: 模型响应的流式输出
    """
    try:
        # 设置API端点
        url = "http://10.62.79.254:31111/api/inference/v1/chat/completions"
        
        # 准备请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        # 准备请求体
        data = {
            "model": "Qwen3-235B-MOE",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 32768,
            "stream": True
        }
        
        # 发送请求
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            stream=True
        )
        
        # 处理响应
        if response.status_code == 200:
            # 逐行处理流式响应
            for line in response.iter_lines():
                if line:
                    # 移除 "data: " 前缀
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        line = line[6:]
                    
                    # 检查是否是结束标记
                    if line == "[DONE]":
                        break
                    
                    try:
                        # 解析JSON
                        result = json.loads(line)
                        delta = result.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue
        else:
            yield f"错误: API请求失败: {response.status_code} - {response.text}"
    except Exception as e:
        yield f"错误: 请求过程中发生错误: {str(e)}"


if __name__ == "__main__":
    # 示例用法
    print("=== LangChain 示例 ===")
    print("1. 简单 LLM 调用:")
    try:
        result = simple_llm_call("你好，世界！")
        print(f"输入: 你好，世界！")
        print(f"输出: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n2. 简单链调用:")
    try:
        result = run_simple_chain("什么是 LangChain？")
        print(f"输入: 什么是 LangChain？")
        print(f"输出: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n3. 翻译功能:")
    try:
        result = translate_text("这是一个 LangChain 示例")
        print(f"输入: 这是一个 LangChain 示例")
        print(f"输出: {result}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n4. 模型验证功能:")
    try:
        # 注意：在实际使用时，应从环境变量或配置文件获取API key
        # 这里仅作为示例，不要在实际代码中硬编码API key
        auth_token = "ccc0f8df-cff1-42b8-97bc-10215051a500"  # 示例token
        result = validate_model(auth_token)
        if result["success"]:
            print(f"模型验证成功！")
            print(f"响应内容: {result['content'][:100]}...")
        else:
            print(f"模型验证失败: {result['error']}")
    except Exception as e:
        print(f"错误: {e}")
