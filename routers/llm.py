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
        translate_text,
        validate_model,
        get_llm,
        simple_llm_call_stream,
        run_simple_chain_stream,
        translate_text_stream,
        validate_model_stream
    )
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    simple_llm_call = None
    run_simple_chain = None
    translate_text = None
    validate_model = None
    get_llm = None
    simple_llm_call_stream = None
    run_simple_chain_stream = None
    translate_text_stream = None
    validate_model_stream = None

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


class ModelValidationRequest(BaseModel):
    """模型验证请求模型"""
    prompt: str = Field(default="介绍一下你自己。", description="测试提示词")


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
        api_key: 认证令牌
        
    Returns:
        dict: 包含响应结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 调用LLM，直接传递auth_token
        response = simple_llm_call(request.prompt, request.model, auth_token=api_key)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM调用失败: {str(e)}"
        )


@router.post("/langchain/simple-llm-stream", tags=["LangChain"])
async def langchain_simple_llm_stream(
    request: SimpleLLMRequest,
    api_key: str = Depends(get_api_key)
):
    """
    简单LLM调用（流式输出）
    
    Args:
        request: 请求模型，包含提示词和模型名称
        api_key: 认证令牌
        
    Returns:
        StreamingResponse: 流式响应结果
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    async def stream_response():
        try:
            # 使用stream方法获取流式响应
            for chunk in simple_llm_call_stream(request.prompt, request.model, auth_token=api_key):
                # 输出chunk内容
                yield chunk
                # 短暂延迟，模拟流式效果
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/langchain/simple-chain-stream", tags=["LangChain"])
async def langchain_simple_chain_stream(
    request: SimpleChainRequest,
    api_key: str = Depends(get_api_key)
):
    """
    简单链调用（流式输出）
    
    Args:
        request: 请求模型，包含输入文本
        api_key: 认证令牌
        
    Returns:
        StreamingResponse: 流式响应结果
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    async def stream_response():
        try:
            # 使用stream方法获取流式响应
            for chunk in run_simple_chain_stream(request.input, auth_token=api_key):
                # 输出chunk内容
                yield chunk
                # 短暂延迟，模拟流式效果
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/langchain/translate-stream", tags=["LangChain"])
async def langchain_translate_stream(
    request: TranslationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    翻译功能（流式输出）
    
    Args:
        request: 请求模型，包含要翻译的文本
        api_key: 认证令牌
        
    Returns:
        StreamingResponse: 流式响应结果
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    async def stream_response():
        try:
            # 使用stream方法获取流式响应
            for chunk in translate_text_stream(request.text, auth_token=api_key):
                # 输出chunk内容
                yield chunk
                # 短暂延迟，模拟流式效果
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/model/validate-stream", tags=["模型验证"])
async def validate_llm_model_stream(
    request: ModelValidationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    验证模型是否可用（流式输出）
    
    Args:
        request: 请求模型，包含测试提示词
        api_key: 认证令牌 (API key)
        
    Returns:
        StreamingResponse: 包含验证结果的流式响应
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="模型验证功能未可用，请确保依赖已正确安装"
        )
    
    async def stream_response():
        try:
            # 使用stream方法获取流式响应
            for chunk in validate_model_stream(api_key, request.prompt):
                # 输出chunk内容
                yield chunk
                # 短暂延迟，模拟流式效果
                await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/langchain/simple-chain", tags=["LangChain"])
async def langchain_simple_chain(
    request: SimpleChainRequest,
    api_key: str = Depends(get_api_key)
):
    """
    简单链调用
    
    Args:
        request: 请求模型，包含输入文本
        api_key: 认证令牌
        
    Returns:
        dict: 包含响应结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 调用链，直接传递auth_token
        response = run_simple_chain(request.input, auth_token=api_key)
        
        return {"response": response}
    except Exception as e:
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
        api_key: 认证令牌
        
    Returns:
        dict: 包含翻译结果
    """
    if not LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangChain 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 调用翻译功能，直接传递auth_token
        translation = translate_text(request.text, auth_token=api_key)
        
        return {"translation": translation}
    except Exception as e:
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
        api_key: 认证令牌
        
    Returns:
        dict: 包含对话响应
    """
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 转换消息格式
        messages = [(msg["role"], msg["content"]) for msg in request.messages]
        
        # 创建并运行对话工作流，传递auth_token
        workflow = ConversationWorkflow(auth_token=api_key)
        result = workflow.run(messages)
        
        return {"response": result["messages"][-1].content}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"对话工作流失败: {str(e)}"
        )


@router.post("/langgraph/conversation-stream", tags=["LangGraph"])
async def langgraph_conversation_stream(
    request: ConversationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    对话工作流（流式输出）
    
    Args:
        request: 请求模型，包含对话消息列表
        api_key: 认证令牌
        
    Returns:
        StreamingResponse: 流式响应结果
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    async def stream_response():
        try:
            # 转换消息格式
            messages = [(msg["role"], msg["content"]) for msg in request.messages]
            
            # 创建并运行对话工作流，传递auth_token
            workflow = ConversationWorkflow(auth_token=api_key)
            
            # 直接使用LLM的stream方法，而不是通过workflow.stream
            llm = workflow.llm
            
            # 流式生成响应
            for chunk in llm.stream(messages):
                if hasattr(chunk, "content") and chunk.content:
                    # 确保换行符被正确处理
                    content = chunk.content
                    # 替换思考过程的标签，使其更美观
                    content = content.replace("<think>", "\n<think>")
                    content = content.replace("</think>", "</think>\n")
                    yield content
                    # 短暂延迟，模拟流式效果
                    await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


@router.post("/langgraph/decision", tags=["LangGraph"])
async def langgraph_decision(
    request: DecisionRequest,
    api_key: str = Depends(get_api_key)
):
    """
    决策工作流
    
    Args:
        request: 请求模型，包含输入内容
        api_key: 认证令牌
        
    Returns:
        dict: 包含决策结果
    """
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    try:
        # 创建并运行决策工作流，传递auth_token
        workflow = DecisionWorkflow(auth_token=api_key)
        result = workflow.run(request.input)
        
        return {"response": result["messages"][-1].content}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"决策工作流失败: {str(e)}"
        )


@router.post("/langgraph/decision-stream", tags=["LangGraph"])
async def langgraph_decision_stream(
    request: DecisionRequest,
    api_key: str = Depends(get_api_key)
):
    """
    决策工作流（流式输出）
    
    Args:
        request: 请求模型，包含输入内容
        api_key: 认证令牌
        
    Returns:
        StreamingResponse: 流式响应结果
    """
    from fastapi.responses import StreamingResponse
    import asyncio
    
    if not LANGGRAPH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LangGraph 依赖未安装，请先安装依赖：poetry install"
        )
    
    async def stream_response():
        try:
            # 创建并运行决策工作流，传递auth_token
            workflow = DecisionWorkflow(auth_token=api_key)
            
            # 直接使用LLM的stream方法，而不是通过workflow.stream
            llm = workflow.llm
            
            # 构建消息列表
            messages = [
                ("system", "你是一个 helpful 的助手。请用中文回答。"),
                ("user", request.input)
            ]
            
            # 流式生成响应
            for chunk in llm.stream(messages):
                if hasattr(chunk, "content") and chunk.content:
                    # 确保换行符被正确处理
                    content = chunk.content
                    # 替换思考过程的标签，使其更美观
                    content = content.replace("<think>", "\n<think>")
                    content = content.replace("</think>", "</think>\n")
                    yield content
                    # 短暂延迟，模拟流式效果
                    await asyncio.sleep(0.01)
        except Exception as e:
            yield f"错误: {str(e)}"
    
    return StreamingResponse(stream_response(), media_type="text/plain")


# 模型验证相关路由
@router.post("/model/validate", tags=["模型验证"])
async def validate_llm_model(
    request: ModelValidationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    验证模型是否可用
    
    Args:
        request: 请求模型，包含测试提示词
        api_key: 认证令牌 (API key)
        
    Returns:
        dict: 包含验证结果
    """
    if validate_model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="模型验证功能未可用，请确保依赖已正确安装"
        )
    
    try:
        # 直接调用模型验证函数
        result = validate_model(api_key, request.prompt)
        
        if result["success"]:
            return {
                "success": True,
                "content": result["content"],
                "message": "模型验证成功"
            }
        else:
            # 验证失败时，返回400错误，便于前端处理
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
                headers={"X-Validation-Error": result.get("content", "")}
            )
    except HTTPException:
        # 重新抛出HTTPException，保留原始状态码和详情
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"模型验证过程中发生错误: {str(e)}"
        )
