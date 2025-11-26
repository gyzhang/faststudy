"""
LangGraph v1.0 示例代码
演示基本的工作流功能
"""

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict


# 定义状态结构
class State(TypedDict):
    """工作流状态定义"""
    messages: Annotated[list, add_messages]


# 定义工作流节点
class SimpleWorkflow:
    """简单的LangGraph工作流示例"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        初始化工作流
        
        Args:
            model_name: 模型名称
        """
        self.llm = ChatOpenAI(model_name=model_name)
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self):
        """
        构建工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        graph = StateGraph(State)
        
        # 添加节点
        graph.add_node("generate", self._generate_response)
        graph.add_node("summarize", self._summarize_conversation)
        
        # 设置入口点
        graph.set_entry_point("generate")
        
        # 添加边
        graph.add_edge("generate", "summarize")
        graph.add_edge("summarize", END)
        
        return graph
    
    def _generate_response(self, state: State):
        """
        生成响应节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 获取最新的用户消息
        user_message = state["messages"][-1]
        
        # 生成响应
        response = self.llm.invoke([
            ("system", "你是一个 helpful 的助手。请用中文回答。"),
            user_message
        ])
        
        # 返回更新后的状态
        return {"messages": [response]}
    
    def _summarize_conversation(self, state: State):
        """
        总结对话节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 生成对话总结
        summary = self.llm.invoke([
            ("system", "请总结以下对话，保持简洁明了。"),
            ("user", "\n".join([msg.content for msg in state["messages"]]))
        ])
        
        # 返回更新后的状态
        return {"messages": [summary]}
    
    def run(self, user_input: str):
        """
        运行工作流
        
        Args:
            user_input: 用户输入
            
        Returns:
            dict: 工作流执行结果
        """
        # 运行工作流
        result = self.app.invoke({
            "messages": [("user", user_input)]
        })
        
        return result


# 定义一个更复杂的工作流示例
class DecisionWorkflow:
    """包含决策节点的LangGraph工作流示例"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        初始化决策工作流
        
        Args:
            model_name: 模型名称
        """
        self.llm = ChatOpenAI(model_name=model_name)
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self):
        """
        构建决策工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        graph = StateGraph(State)
        
        # 添加节点
        graph.add_node("classify", self._classify_input)
        graph.add_node("answer_question", self._answer_question)
        graph.add_node("translate", self._translate_text)
        graph.add_node("summarize", self._summarize_text)
        
        # 设置入口点
        graph.set_entry_point("classify")
        
        # 添加条件边
        graph.add_conditional_edges(
            "classify",
            self._route_based_on_classification,
            {
                "question": "answer_question",
                "translate": "translate",
                "summarize": "summarize"
            }
        )
        
        # 添加结束边
        graph.add_edge("answer_question", END)
        graph.add_edge("translate", END)
        graph.add_edge("summarize", END)
        
        return graph
    
    def _classify_input(self, state: State):
        """
        分类输入节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态，包含分类结果
        """
        # 获取用户输入
        user_message = state["messages"][-1].content
        
        # 分类输入类型
        classification = self.llm.invoke([
            ("system", "请将用户输入分类为以下类型之一：question（问题）、translate（翻译请求）、summarize（总结请求）。只返回类型名称，不要返回其他内容。"),
            ("user", user_message)
        ])
        
        # 返回分类结果
        return {
            "messages": [classification]
        }
    
    def _route_based_on_classification(self, state: State):
        """
        根据分类结果路由到不同节点
        
        Args:
            state: 当前状态
            
        Returns:
            str: 下一个节点名称
        """
        # 获取分类结果
        classification = state["messages"][-1].content.lower().strip()
        
        # 返回对应的节点名称
        return classification
    
    def _answer_question(self, state: State):
        """
        回答问题节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 获取用户问题
        user_question = state["messages"][0].content
        
        # 回答问题
        answer = self.llm.invoke([
            ("system", "你是一个 helpful 的助手。请用中文回答用户的问题。"),
            ("user", user_question)
        ])
        
        return {"messages": [answer]}
    
    def _translate_text(self, state: State):
        """
        翻译文本节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 获取用户输入的文本
        user_text = state["messages"][0].content
        
        # 提取需要翻译的文本（移除"翻译"等关键词）
        import re
        text_to_translate = re.sub(r'^(翻译|translate)[:：]?\s*', '', user_text, flags=re.IGNORECASE)
        
        # 翻译文本
        translation = self.llm.invoke([
            ("system", "请将用户输入的文本翻译成英文。"),
            ("user", text_to_translate)
        ])
        
        return {"messages": [translation]}
    
    def _summarize_text(self, state: State):
        """
        总结文本节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 获取用户输入的文本
        user_text = state["messages"][0].content
        
        # 提取需要总结的文本（移除"总结"等关键词）
        import re
        text_to_summarize = re.sub(r'^(总结|summarize)[:：]?\s*', '', user_text, flags=re.IGNORECASE)
        
        # 总结文本
        summary = self.llm.invoke([
            ("system", "请总结用户输入的文本，保持简洁明了。"),
            ("user", text_to_summarize)
        ])
        
        return {"messages": [summary]}
    
    def run(self, user_input: str):
        """
        运行决策工作流
        
        Args:
            user_input: 用户输入
            
        Returns:
            dict: 工作流执行结果
        """
        # 运行工作流
        result = self.app.invoke({
            "messages": [("user", user_input)]
        })
        
        return result


# 简单的对话工作流
class ConversationWorkflow:
    """简单的对话工作流示例"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        初始化对话工作流
        
        Args:
            model_name: 模型名称
        """
        self.llm = ChatOpenAI(model_name=model_name)
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self):
        """
        构建对话工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        graph = StateGraph(State)
        
        # 添加对话节点
        graph.add_node("chat", self._chat)
        
        # 设置入口点和循环
        graph.set_entry_point("chat")
        graph.add_edge("chat", END)
        
        return graph
    
    def _chat(self, state: State):
        """
        对话节点
        
        Args:
            state: 当前状态
            
        Returns:
            dict: 更新后的状态
        """
        # 生成响应
        response = self.llm.invoke(state["messages"])
        
        return {"messages": [response]}
    
    def run(self, messages: list):
        """
        运行对话工作流
        
        Args:
            messages: 对话消息列表
            
        Returns:
            dict: 工作流执行结果
        """
        # 运行工作流
        result = self.app.invoke({
            "messages": messages
        })
        
        return result


if __name__ == "__main__":
    print("=== LangGraph v1.0 示例 ===")
    
    # 示例1: 简单对话工作流
    print("\n1. 简单对话工作流:")
    try:
        workflow = ConversationWorkflow()
        result = workflow.run([("user", "你好，世界！")])
        print(f"输入: 你好，世界！")
        print(f"输出: {result['messages'][-1].content}")
    except Exception as e:
        print(f"错误: {e}")
    
    # 示例2: 决策工作流
    print("\n2. 决策工作流 - 回答问题:")
    try:
        workflow = DecisionWorkflow()
        result = workflow.run("什么是 LangGraph？")
        print(f"输入: 什么是 LangGraph？")
        print(f"输出: {result['messages'][-1].content}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n3. 决策工作流 - 翻译请求:")
    try:
        workflow = DecisionWorkflow()
        result = workflow.run("翻译：这是一个 LangGraph 示例")
        print(f"输入: 翻译：这是一个 LangGraph 示例")
        print(f"输出: {result['messages'][-1].content}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n4. 决策工作流 - 总结请求:")
    try:
        workflow = DecisionWorkflow()
        long_text = """LangGraph 是一个用于构建多智能体工作流的框架。它基于 LangChain，
        提供了更强大的工作流编排能力。使用 LangGraph，你可以轻松构建复杂的多智能体系统，
        实现任务分配、协作和结果整合。LangGraph 支持状态管理、条件分支、循环等高级功能，
        适合构建各种复杂的 AI 应用。"""
        result = workflow.run(f"总结：{long_text}")
        print(f"输入: 总结：{long_text[:50]}...")
        print(f"输出: {result['messages'][-1].content}")
    except Exception as e:
        print(f"错误: {e}")
