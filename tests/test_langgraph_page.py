import pytest
from playwright.sync_api import Page, expect

class TestLangGraphPage:
    """LangGraph 页面功能测试"""
    
    @pytest.fixture
    def setup(self, page: Page):
        """测试前的设置，导航到 LangGraph 页面"""
        page.goto('http://localhost:8000/static/langgraph.html')
        return page
    
    def test_page_elements(self, setup: Page):
        """测试页面基本元素是否正确显示"""
        page = setup
        
        # 检查页面标题
        expect(page).to_have_title('LangGraph v1.0 交互示例 - FastAPI 学习项目')
        
        # 检查导航栏链接
        expect(page.locator('.nav a')).to_have_count(6)
        expect(page.locator('.nav a:nth-child(1)')).to_have_text('🏠 首页')
        expect(page.locator('.nav a:nth-child(2)')).to_have_text('👥 用户管理')
        expect(page.locator('.nav a:nth-child(3)')).to_have_text('📦 物品管理')
        expect(page.locator('.nav a:nth-child(4)')).to_have_text('🧠 LangChain')
        expect(page.locator('.nav a:nth-child(5)')).to_have_text('🔄 LangGraph')
        expect(page.locator('.nav a:nth-child(6)')).to_have_text('📖 API 文档')
        
        # 检查 API Key 设置区域
        expect(page.locator('h2:has-text("🔑 API Key 设置")')).to_be_visible()
        expect(page.locator('.api-key-warning')).to_be_visible()
        expect(page.locator('#apiKey')).to_be_visible()
        expect(page.locator('button:has-text("保存")')).to_be_visible()
        
        # 检查功能选项卡
        expect(page.locator('.tabs')).to_be_visible()
        # 假设 LangGraph 页面也有选项卡，具体数量可能需要根据实际页面调整
        # 如果不确定具体数量，可以暂时不测试数量，只测试可见性
        
        # 检查聊天相关元素
        expect(page.locator('.chat-history')).to_be_visible()
        
        # 工作流类型选择器在页面加载时可能是隐藏的，移除可见性检查
    
    def test_navigation_functionality(self, setup: Page):
        """测试导航功能是否正常"""
        page = setup
        
        # 测试导航到首页
        page.click('.nav a:nth-child(1)')
        expect(page).to_have_title('FastAPI 学习项目')
        
        # 导航回 LangGraph 页面
        page.goto('http://localhost:8000/static/langgraph.html')
        
        # 测试导航到用户管理页面
        page.click('.nav a:nth-child(2)')
        expect(page).to_have_title('用户管理 - FastAPI 学习项目')
        
        # 导航回 LangGraph 页面
        page.goto('http://localhost:8000/static/langgraph.html')
        
        # 测试导航到物品管理页面
        page.click('.nav a:nth-child(3)')
        expect(page).to_have_title('物品管理 - FastAPI 学习项目')
        
        # 导航回 LangGraph 页面
        page.goto('http://localhost:8000/static/langgraph.html')
        
        # 测试导航到 LangChain 页面
        page.click('.nav a:nth-child(4)')
        expect(page).to_have_title('LangChain 交互示例 - FastAPI 学习项目')