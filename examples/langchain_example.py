"""
LangChain 示例代码
演示基本的 LLM 调用和链功能
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage, AIMessageChunk
from langchain_core.outputs import ChatGeneration, ChatResult, ChatGenerationChunk
from langchain_core.runnables import Runnable
from typing import Optional, List, Dict, Any, Iterator, Callable
import requests
import json

# 配置常量
API_ENDPOINT = "http://10.62.79.254:31111/api/inference/v1/chat/completions"
DEFAULT_MODEL = "Qwen3-235B-MOE"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 32768
DEFAULT_VALIDATION_PROMPT = "介绍一下你自己。"


# 自定义异常类
class LLMAPIError(Exception):
    """
    LLM API 异常类
    """
    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            status_code: HTTP 状态码
        """
        super().__init__(message)
        self.status_code = status_code


# 辅助函数
def _prepare_api_request(messages: List[Dict[str, str]], auth_token: str, temperature: float = DEFAULT_TEMPERATURE, 
                        stream: bool = False, max_tokens: int = DEFAULT_MAX_TOKENS) -> Dict[str, Any]:
    """
    准备API请求
    
    Args:
        messages: 消息列表
        auth_token: 认证令牌
        temperature: 温度参数
        stream: 是否使用流式响应
        max_tokens: 最大令牌数
        
    Returns:
        Dict[str, Any]: 包含headers和data的字典，其中headers为Dict[str, str]，data为Dict[str, Any]
    """
    headers: Dict[str, str] = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    
    data: Dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }
    
    return {"headers": headers, "data": data}


def _convert_messages_to_api_format(messages: List[BaseMessage]) -> List[Dict[str, str]]:
    """
    将LangChain消息转换为API格式
    
    Args:
        messages: LangChain消息列表
        
    Returns:
        List[Dict[str, str]]: API格式的消息列表
    """
    api_messages: List[Dict[str, str]] = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            api_messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, SystemMessage):
            api_messages.append({"role": "system", "content": msg.content})
        elif isinstance(msg, AIMessage):
            api_messages.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, AIMessageChunk):
            api_messages.append({"role": "assistant", "content": msg.content})
    return api_messages


def _process_stream_response(response: requests.Response) -> Iterator[str]:
    """
    处理流式响应
    
    Args:
        response: requests响应对象
        
    Yields:
        str: 流式响应内容
    """
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
                # 检查是否有错误
                if "error" in result:
                    error_msg = result["error"].get("message", "Unknown error")
                    raise LLMAPIError(f"API returned error: {error_msg}")
                
                delta = result.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                
                if content:
                    yield content
            except json.JSONDecodeError:
                continue
            except Exception as e:
                yield f"错误: {str(e)}"


class CustomChatModel(BaseChatModel):
    """
    自定义 ChatModel，用于调用外部 API
    """
    
    def __init__(self, temperature: float = DEFAULT_TEMPERATURE, auth_token: Optional[str] = None):
        """
        初始化自定义 ChatModel
        
        Args:
            temperature: 温度参数
            auth_token: 认证令牌
        """
        super().__init__()
        self._temperature = temperature
        self._auth_token = auth_token
    
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
        
        Raises:
            LLMAPIError: 如果API请求失败
        """
        # 转换消息格式
        api_messages = _convert_messages_to_api_format(messages)
        
        # 准备API请求
        request_data = _prepare_api_request(
            api_messages, 
            self.auth_token, 
            temperature=self.temperature,
            stream=False
        )
        
        try:
            # 发送请求
            response = requests.post(
                API_ENDPOINT,
                headers=request_data["headers"],
                data=json.dumps(request_data["data"]),
                timeout=30  # 添加超时设置
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                # 检查是否有错误
                if "error" in result:
                    error_msg = result["error"].get("message", "Unknown error")
                    raise LLMAPIError(f"API returned error: {error_msg}")
                
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # 创建 ChatResult
                chat_generation = ChatGeneration(
                    message=AIMessage(content=content),
                    generation_info={"finish_reason": result.get("choices", [{}])[0].get("finish_reason", "stop")}
                )
                
                return ChatResult(generations=[chat_generation])
            else:
                raise LLMAPIError(
                    f"API请求失败: {response.status_code} - {response.text}",
                    status_code=response.status_code
                )
        except requests.RequestException as e:
            raise LLMAPIError(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise LLMAPIError(f"响应解析失败: {str(e)}")
    
    def _stream(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs: Any) -> Iterator[ChatGenerationChunk]:
        """
        流式生成响应
        
        Args:
            messages: 消息列表
            stop: 停止词列表
            **kwargs: 其他参数
            
        Yields:
            ChatGenerationChunk: 流式响应块
        
        Raises:
            LLMAPIError: 如果API请求失败
        """
        # 转换消息格式
        api_messages = _convert_messages_to_api_format(messages)
        
        # 准备API请求
        request_data = _prepare_api_request(
            api_messages, 
            self.auth_token, 
            temperature=self.temperature,
            stream=True
        )
        
        try:
            # 发送请求
            response = requests.post(
                API_ENDPOINT,
                headers=request_data["headers"],
                data=json.dumps(request_data["data"]),
                stream=True,
                timeout=30  # 添加超时设置
            )
            
            # 处理响应
            if response.status_code == 200:
                # 逐行处理流式响应
                for content in _process_stream_response(response):
                    # 创建 ChatGenerationChunk
                    chunk = ChatGenerationChunk(
                        message=AIMessageChunk(content=content),
                        generation_info={}
                    )
                    yield chunk
            else:
                raise LLMAPIError(
                    f"API请求失败: {response.status_code} - {response.text}",
                    status_code=response.status_code
                )
        except requests.RequestException as e:
            raise LLMAPIError(f"网络请求失败: {str(e)}")
    
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


def get_llm(model_name: str = "gpt-3.5-turbo", temperature: float = DEFAULT_TEMPERATURE, auth_token: Optional[str] = None) -> CustomChatModel:
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


def create_chain(system_prompt: str, input_key: str, auth_token: Optional[str] = None) -> Runnable:
    """
    创建通用链
    
    Args:
        system_prompt: 系统提示词
        input_key: 输入键名
        auth_token: 认证令牌
        
    Returns:
        Runnable: 链实例
    """
    # 定义提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", f"{{{input_key}}}")
    ])
    
    # 获取 LLM
    llm = get_llm(auth_token=auth_token)
    
    # 定义输出解析器
    output_parser = StrOutputParser()
    
    # 创建链
    chain = prompt | llm | output_parser
    
    return chain


def create_simple_chain(auth_token: Optional[str] = None):
    """
    创建简单的链
    
    Args:
        auth_token: 认证令牌
        
    Returns:
        Runnable: 链实例
    """
    return create_chain(
        system_prompt="你是一个 helpful 的助手。请用中文回答。",
        input_key="input",
        auth_token=auth_token
    )


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
    return create_chain(
        system_prompt="你是一个专业的翻译助手。请将用户输入的文本翻译成英文。",
        input_key="text",
        auth_token=auth_token
    )


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


def validate_model(auth_token: str, prompt: str = DEFAULT_VALIDATION_PROMPT) -> dict:
    """
    验证模型是否可用
    
    Args:
        auth_token: 认证令牌 (API key)
        prompt: 测试提示词
        
    Returns:
        dict: 包含响应结果和状态信息
    """
    try:
        # 准备API请求
        messages = [{"role": "user", "content": prompt}]
        request_data = _prepare_api_request(messages, auth_token, stream=False)
        
        # 发送请求
        response = requests.post(
            API_ENDPOINT,
            headers=request_data["headers"],
            data=json.dumps(request_data["data"])
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


def validate_model_stream(auth_token: str, prompt: str = DEFAULT_VALIDATION_PROMPT) -> Iterator[str]:
    """
    验证模型是否可用（流式输出）
    
    Args:
        auth_token: 认证令牌 (API key)
        prompt: 测试提示词
        
    Yields:
        str: 模型响应的流式输出
    """
    try:
        # 准备API请求
        messages = [{"role": "user", "content": prompt}]
        request_data = _prepare_api_request(messages, auth_token, stream=True)
        
        # 发送请求
        response = requests.post(
            API_ENDPOINT,
            headers=request_data["headers"],
            data=json.dumps(request_data["data"]),
            stream=True
        )
        
        # 处理响应
        if response.status_code == 200:
            # 使用辅助函数处理流式响应
            for content in _process_stream_response(response):
                yield content
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
