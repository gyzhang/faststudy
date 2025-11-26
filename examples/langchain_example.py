"""
LangChain 示例代码
演示基本的 LLM 调用和链功能
"""

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from typing import Optional


def get_llm(model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
    """
    获取 LLM 实例
    
    Args:
        model_name: 模型名称
        temperature: 温度参数
        
    Returns:
        ChatOpenAI: LLM 实例
    """
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature
    )


def simple_llm_call(prompt: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    简单的 LLM 调用
    
    Args:
        prompt: 提示词
        model_name: 模型名称
        
    Returns:
        str: LLM 响应
    """
    llm = get_llm(model_name)
    return llm.invoke(prompt)


def create_simple_chain():
    """
    创建简单的链
    
    Returns:
        Runnable: 链实例
    """
    # 定义提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 helpful 的助手。请用中文回答。"),
        ("user", "{input}")
    ])
    
    # 获取 LLM
    llm = get_llm()
    
    # 定义输出解析器
    output_parser = StrOutputParser()
    
    # 创建链
    chain = prompt | llm | output_parser
    
    return chain


def run_simple_chain(input_text: str) -> str:
    """
    运行简单的链
    
    Args:
        input_text: 输入文本
        
    Returns:
        str: 链的输出
    """
    chain = create_simple_chain()
    return chain.invoke({"input": input_text})


def create_translation_chain():
    """
    创建翻译链
    
    Returns:
        Runnable: 翻译链实例
    """
    # 定义翻译提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的翻译助手。请将用户输入的文本翻译成英文。"),
        ("user", "{text}")
    ])
    
    # 获取 LLM
    llm = get_llm()
    
    # 定义输出解析器
    output_parser = StrOutputParser()
    
    # 创建翻译链
    translation_chain = prompt | llm | output_parser
    
    return translation_chain


def translate_text(text: str) -> str:
    """
    翻译文本
    
    Args:
        text: 要翻译的文本
        
    Returns:
        str: 翻译后的文本
    """
    translation_chain = create_translation_chain()
    return translation_chain.invoke({"text": text})


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
