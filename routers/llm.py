"""
LangChain 和 LangGraph 相关路由
"""

from fastapi import APIRouter, HTTPException, status, Depends, Header
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os

router = APIRouter()

# 尝试导入依赖，失败则设置为None
try:
    from examples.langchain_example import (
        simple_llm_call,
        run_simple_chain,
        translate_text
    )
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    simple_llm_call = None
    run_simple_chain = None
    translate_text = None

try:
    from examples.langgraph_example import (
        ConversationWorkflow,
        DecisionWorkflow
    )
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    ConversationWorkflow = None
    DecisionWorkflow = None


# 定义请求模型
class SimpleLLMRequest(BaseModel):
    """简单LLM调用请求模型"""
    prompt: str = Field(..., description="提示词")
    model: str = Field(default="gpt-3.5-turbo", description="模型名称")


class SimpleChainRequest(BaseModel):
    """简单链调用请求模型"""
    input: str = Field(..., description="输入文本")


class TranslationRequest(BaseModel):
    """翻译请求模型"""
    text: str = Field(..., description="要翻译的文本")


class ConversationRequest(BaseModel):
    """对话请求模型"""
    messages: List[Dict[str, str]] = Field(..., description="对话消息列表")


class DecisionRequest(BaseModel):
    """决策请求模型"""
    input: str = Field(..., description="输入内容")


# 辅助函数：获取API Key
def get_api_key(authorization: str = Header(...)):
    """
    从Authorization头中获取API Key
    
    Args:
        authorization: Authorization头
        
    Returns:
        str: API Key
        
    Raises:
        HTTPException: 如果Authorization头格式不正确或缺少API Key
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Authorization头格式，应为Bearer {api_key}"
        )
    return authorization[7:]


# LangChain 相关路由
@router.post("/langchain/simple-llm", tags=["LangChain"])
async def langchain_simple_llm(
    request: SimpleLLMRequest,
    api_key: str = Depends(get_api_key)
):
    """
    简单LLM调用
    
    Args:
        request: 请求模型，包含提示词和模型名称
        api_key: OpenAI API Key
        
    Returns:
        dict: 包含响应结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 设置环境变量
        original_api_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # 调用LLM
        response = simple_llm_call(request.prompt, request.model)
        
        # 恢复原始环境变量
        if original_api_key is not None:
            os.environ["OPENAI_API_KEY"] = original_api_key
        else:
            del os.environ["OPENAI_API_KEY"]
        
        return {"response": response.content if hasattr(response, "content") else str(response)}
    except Exception as e:
        # 恢复原始环境变量
        if "OPENAI_API_KEY" in os.environ:
            if original_api_key is not None:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                del os.environ["OPENAI_API_KEY"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM调用失败: {str(e)}"
        )


@router.post("/langchain/simple-chain", tags=["LangChain"])
async def langchain_simple_chain(
    request: SimpleChainRequest,
    api_key: str = Depends(get_api_key)
):
    """
    简单链调用
    
    Args:
        request: 请求模型，包含输入文本
        api_key: OpenAI API Key
        
    Returns:
        dict: 包含响应结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 设置环境变量
        original_api_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # 调用链
        response = run_simple_chain(request.input)
        
        # 恢复原始环境变量
        if original_api_key is not None:
            os.environ["OPENAI_API_KEY"] = original_api_key
        else:
            del os.environ["OPENAI_API_KEY"]
        
        return {"response": response}
    except Exception as e:
        # 恢复原始环境变量
        if "OPENAI_API_KEY" in os.environ:
            if original_api_key is not None:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                del os.environ["OPENAI_API_KEY"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"链调用失败: {str(e)}"
        )


@router.post("/langchain/translate", tags=["LangChain"])
async def langchain_translate(
    request: TranslationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    翻译功能
    
    Args:
        request: 请求模型，包含要翻译的文本
        api_key: OpenAI API Key
        
    Returns:
        dict: 包含翻译结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 设置环境变量
        original_api_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # 调用翻译功能
        translation = translate_text(request.text)
        
        # 恢复原始环境变量
        if original_api_key is not None:
            os.environ["OPENAI_API_KEY"] = original_api_key
        else:
            del os.environ["OPENAI_API_KEY"]
        
        return {"translation": translation}
    except Exception as e:
        # 恢复原始环境变量
        if "OPENAI_API_KEY" in os.environ:
            if original_api_key is not None:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                del os.environ["OPENAI_API_KEY"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"翻译失败: {str(e)}"
        )


# LangGraph 相关路由
@router.post("/langgraph/conversation", tags=["LangGraph"])
async def langgraph_conversation(
    request: ConversationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    对话工作流
    
    Args:
        request: 请求模型，包含对话消息列表
        api_key: OpenAI API Key
        
    Returns:
        dict: 包含对话响应
    """
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 设置环境变量
        original_api_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # 转换消息格式
        messages = [(msg["role"], msg["content"]) for msg in request.messages]
        
        # 创建并运行对话工作流
        workflow = ConversationWorkflow()
        result = workflow.run(messages)
        
        # 恢复原始环境变量
        if original_api_key is not None:
            os.environ["OPENAI_API_KEY"] = original_api_key
        else:
            del os.environ["OPENAI_API_KEY"]
        
        return {"response": result["messages"][-1].content}
    except Exception as e:
        # 恢复原始环境变量
        if "OPENAI_API_KEY" in os.environ:
            if original_api_key is not None:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                del os.environ["OPENAI_API_KEY"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"对话工作流失败: {str(e)}"
        )


@router.post("/langgraph/decision", tags=["LangGraph"])
async def langgraph_decision(
    request: DecisionRequest,
    api_key: str = Depends(get_api_key)
):
    """
    决策工作流
    
    Args:
        request: 请求模型，包含输入内容
        api_key: OpenAI API Key
        
    Returns:
        dict: 包含决策结果
    """
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 设置环境变量
        original_api_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        
        # 创建并运行决策工作流
        workflow = DecisionWorkflow()
        result = workflow.run(request.input)
        
        # 恢复原始环境变量
        if original_api_key is not None:
            os.environ["OPENAI_API_KEY"] = original_api_key
        else:
            del os.environ["OPENAI_API_KEY"]
        
        return {"response": result["messages"][-1].content}
    except Exception as e:
        # 恢复原始环境变量
        if "OPENAI_API_KEY" in os.environ:
            if original_api_key is not None:
                os.environ["OPENAI_API_KEY"] = original_api_key
            else:
                del os.environ["OPENAI_API_KEY"]
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"决策工作流失败: {str(e)}"
        )
