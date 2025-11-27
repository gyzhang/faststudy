import pytest
from playwright.sync_api import Page, expect

class TestLangChainPage:
    """LangChain 页面功能测试"""
    
    @pytest.fixture
    def setup(self, page: Page):
        """测试前的设置，导航到 LangChain 页面"""
        page.goto('http://localhost:8000/static/langchain.html')
        return page
    
    def test_page_elements(self, setup: Page):
        """测试页面基本元素是否正确显示"""
        page = setup
        
        # 检查页面标题
        expect(page).to_have_title('LangChain 交互示例 - FastAPI 学习项目')
        
        # 检查导航栏链接
        expect(page.locator('.nav a')).to_have_count(6)
        expect(page.locator('.nav a:nth-child(1)')).to_have_text('🏠 首页')
        expect(page.locator('.nav a:nth-child(2)')).to_have_text('👥 用户管理')
        expect(page.locator('.nav a:nth-child(3)')).to_have_text('📦 物品管理')
        expect(page.locator('.nav a:nth-child(4)')).to_have_text('🧠 LangChain')
        expect(page.locator('.nav a:nth-child(5)')).to_have_text('🔄 LangGraph')
        expect(page.locator('.nav a:nth-child(6)')).to_have_text('📖 API 文档')
        
        # 检查 API Key 设置区域
        expect(page.locator('h2:has-text("🔑 OpenAI API Key 设置")')).to_be_visible()
        expect(page.locator('.api-key-warning')).to_be_visible()
        expect(page.locator('#apiKey')).to_be_visible()
        expect(page.locator('button:has-text("保存")')).to_be_visible()
        
        # 检查功能选项卡
        expect(page.locator('.tabs')).to_be_visible()
        expect(page.locator('.tab')).to_have_count(3)
        expect(page.locator('.tab:nth-child(1)')).to_have_text('简单 LLM 调用')
        expect(page.locator('.tab:nth-child(2)')).to_have_text('简单链调用')
        expect(page.locator('.tab:nth-child(3)')).to_have_text('翻译功能')
        
        # 检查默认激活的选项卡内容
        expect(page.locator('#simple-llm')).to_be_visible()
        expect(page.locator('#simpleLlmPrompt')).to_be_visible()
        expect(page.locator('#simpleLlmModel')).to_be_visible()
        expect(page.locator('button:has-text("运行 LLM")')).to_be_visible()
        expect(page.locator('#simpleLlmResult')).to_be_visible()
    
    def test_tab_switching(self, setup: Page):
        """测试选项卡切换功能"""
        page = setup
        
        # 点击简单链调用选项卡
        page.click('.tab:nth-child(2)')
        # 检查选项卡内容是否可见，而不是检查类
        expect(page.locator('#simple-chain')).to_be_visible()
        
        # 点击翻译功能选项卡
        page.click('.tab:nth-child(3)')
        expect(page.locator('#translation')).to_be_visible()
        
        # 点击回简单 LLM 调用选项卡
        page.click('.tab:nth-child(1)')
        expect(page.locator('#simple-llm')).to_be_visible()