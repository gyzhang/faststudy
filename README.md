# FastStudy - Python、FastAPI、LangChain 和 LangGraph 学习项目

一个专为Python学习者设计的综合性学习项目，集成了FastAPI后端开发、LangChain v1.0和LangGraph v1.0大语言模型应用开发。通过实际项目结构和可运行代码，帮助开发者掌握现代Python后端开发与AI应用集成的核心技能。

## 🎯 学习目标

### Python 后端开发
- ✅ **FastAPI 核心概念** - RESTful API、路由组织、依赖注入、自动文档生成
- ✅ **数据验证与序列化** - 使用 Pydantic V2 构建强类型数据模型
- ✅ **数据库操作** - SQLAlchemy ORM 使用、数据库设计与查询优化
- ✅ **分页实现** - 基于数据库的高效分页算法
- ✅ **测试驱动开发** - Playwright + Pytest 自动化测试实践

### AI 应用开发
- ✅ **LangChain v1.0 基础** - LLM 调用、提示词工程、链结构设计
- ✅ **LangChain 高级特性** - 自定义模型集成、流式输出处理、错误处理
- ✅ **LangGraph v1.0 工作流** - 状态管理、节点定义、条件路由
- ✅ **多模态应用架构** - 结合传统后端与AI服务的架构设计
- ✅ **API 集成模式** - 外部模型服务的封装与调用模式

## 📋 技术栈与学习资源

### 核心技术
- **后端框架**: FastAPI 0.104.1 - 现代、快速的异步Web框架
- **ORM**: SQLAlchemy 2.0.44 - 功能强大的SQL工具包和ORM
- **数据库**: SQLite - 轻量级文件数据库，便于学习和开发
- **数据验证**: Pydantic V2 - 数据验证和设置管理，支持Python类型提示
- **依赖管理**: Poetry - 现代Python依赖管理和打包工具
- **LLM 框架**: 
  - LangChain 1.0.0 - 用于构建LLM应用的开发框架
  - LangGraph 1.0.0 - 基于LangChain构建的有状态多步工作流框架

### 推荐学习资源
- [Python官方文档](https://docs.python.org/3/)
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [LangChain官方文档](https://python.langchain.com/)
- [LangGraph官方文档](https://langchain-ai.github.io/langgraph/)
- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)

## 🚀 快速开始 - 学习路径

### 环境准备

要开始学习这个项目，您需要准备以下环境：

- Windows 11
- Python 3.14 (64位) - 推荐使用conda虚拟环境
- Visual C++ Build Tools - 用于某些Python包的编译
- Rust 开发环境 - 安装LangChain相关依赖时需要

### 安装步骤

1. **安装 Visual C++ Build Tools**
   - 下载并运行 [Build Tools for Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - 勾选：
     - "Desktop development with C++"
     - "MSVC v143 - VS 2022 C++ x64/x86 build tools"
     - "Windows 11 SDK"
   - 安装完成后重启电脑

2. **安装 Rust 开发环境**
   - 下载并运行 [Rust Windows 安装程序](https://www.rust-lang.org/tools/install)
   - 使用默认选项完成安装
   - 安装后关闭并重新打开命令行窗口

3. **安装 Poetry**
   ```powershell
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   ```

4. **克隆项目并安装依赖**
   ```powershell
   # 切换到工作目录
   cd D:\Kevin\AI
   
   # 进入项目目录
   cd .\faststudy
   
   # 安装依赖
   poetry install
   ```

### 启动服务

```powershell
poetry run uvicorn main:app --reload
```

服务启动后，访问以下地址：
- 首页: http://127.0.0.1:8000
- API 文档: http://127.0.0.1:8000/docs
- ReDoc 文档: http://127.0.0.1:8000/redoc

## 📖 学习模块详解

### 1. FastAPI 后端开发学习

**示例页面**: http://127.0.0.1:8000/static/users.html 和 http://127.0.0.1:8000/static/items.html

**学习要点**:
- 模块化路由设计 (`routers/` 目录)
- Pydantic模型定义与验证 (`models/schemas.py`)
- 数据库操作与关系映射 (`models/database.py`)
- 分页实现原理与性能优化
- RESTful API 最佳实践

### 2. LangChain v1.0 学习模块

**示例页面**: http://127.0.0.1:8000/static/langchain.html

**核心示例代码**: `examples/langchain_example.py`

**学习要点**:
- **自定义LLM集成**: 学习如何封装外部API为LangChain兼容的模型
- **提示词工程**: 系统提示词设计与优化
- **链结构设计**: 构建可复用的处理链
- **流式输出处理**: 实现实时响应流
- **错误处理机制**: 健壮的API调用错误处理

**主要功能示例**:
- `simple_llm_call`: 基础LLM调用，展示如何发送提示并获取响应
- `create_chain`: 链创建模式，封装提示词模板与模型调用
- `translate_text`: 专用链实现，展示领域特定功能封装
- `validate_model`: 模型验证机制，展示API健康检查实现

### 3. LangGraph v1.0 工作流学习

**示例页面**: http://127.0.0.1:8000/static/langgraph.html

**核心示例代码**: `examples/langgraph_example.py`

**学习要点**:
- **状态管理**: 使用TypedDict定义工作流状态结构
- **节点设计**: 创建可复用的工作流节点
- **图结构构建**: 使用StateGraph组织处理流程
- **条件路由**: 实现智能工作流分支
- **流式执行**: 支持工作流的渐进式输出

**主要工作流示例**:
- `SimpleWorkflow`: 基础工作流，展示顺序节点执行
- `DecisionWorkflow`: 决策工作流，展示基于输入类型的动态路由
- 条件边实现: 通过分类模型自动选择处理路径

### 4. 集成架构学习

**学习要点**:
- 后端API与AI服务的桥接模式 (`routers/llm.py`)
- 环境变量与配置管理 (`config.py`)
- 优雅降级机制: 处理LangChain/LangGraph不可用时的情况
- 前端与AI模型的交互模式

## 🔌 学习API示例

### 基础API调用示例

#### 健康检查
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health -Method Get
```

#### 用户管理API
```powershell
# 获取用户列表（带分页）
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users?page=1&page_size=10" -Method Get

# 创建用户
$userData = @{
    username = "testuser"
    email = "testuser@example.com"
    password = "password123"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users" -Method Post -ContentType "application/json" -Body $userData
```

#### 物品管理API
```powershell
# 获取物品列表（带分页）
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items?page=2&page_size=5" -Method Get

# 创建物品
$itemData = @{
    name = "Sample Item"
    description = "This is a sample item"
    price = 9.99
    owner_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items" -Method Post -ContentType "application/json" -Body $itemData
```

### LangChain API示例

```powershell
# LLM 模型验证
$validationData = @{
    auth_token = "your_api_key_here"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/model/validate" -Method Post -ContentType "application/json" -Body ($validationData | ConvertTo-Json)

# 简单LLM调用
$llmData = @{
    prompt = "什么是LangChain？"
    auth_token = "your_api_key_here"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/langchain/simple-llm" -Method Post -ContentType "application/json" -Body ($llmData | ConvertTo-Json)
```

## 🗄️ 数据库操作学习

### 数据库初始化

项目使用 SQLite 数据库，首次运行会自动初始化，这是学习SQLAlchemy ORM工作原理的好机会：
- 创建 `users` 和 `items` 表（通过SQLAlchemy模型）
- 插入10个测试用户
- 插入30个测试物品（每个用户3个）

### 数据库重置

学习数据库管理的重要一步是了解如何重置数据库：

```powershell
# 方式1：删除数据库文件后重启服务
Remove-Item -Force .\faststudy.db
poetry run uvicorn main:app --reload

# 方式2：调用重置函数
poetry run python -c "from models.database import reset_db; reset_db()"
```

### 数据库文件

SQLite数据库文件位于项目根目录：`faststudy.db`，可以使用SQLite工具直接打开查看数据，这对于学习数据库操作非常有帮助。

## 📚 总结

这个项目是学习Python后端开发和AI集成的综合练习环境，通过实际的代码实现和功能演示，帮助学习者掌握：

1. **现代Python开发**：FastAPI框架、Pydantic数据验证、SQLAlchemy ORM
2. **AI框架应用**：LangChain v1.0和LangGraph v1.0的实际应用
3. **全栈开发基础**：前后端交互、API设计、数据库管理
4. **软件工程实践**：测试、配置管理、依赖管理

按照推荐的学习路径逐步深入，结合动手实践，能够系统地掌握这些现代Python和AI技术。

## 🔮 后续学习方向

完成本项目学习后，您可以考虑以下进阶方向：

- 部署FastAPI应用到云服务器
- 集成更多LLM模型和AI功能
- 构建更复杂的LangGraph工作流
- 添加用户认证和授权功能
- 实现更完善的前端界面
- 学习Docker容器化部署

## 🧪 项目测试

测试是学习软件质量保证的重要部分：

### 测试流程
1. **启动FastAPI服务**（在一个终端中）
   ```powershell
   poetry run uvicorn main:app --reload
   ```

2. **运行测试**（在另一个终端中）
   ```powershell
   # 执行所有测试
   poetry run pytest tests/ -v
   
   # 生成 HTML 测试报告
   poetry run pytest tests/ -v --html=reports/test_report.html --self-contained-html
   ```

### 测试学习要点
- 了解如何编写针对Web应用的自动化测试
- 学习测试驱动开发(TDD)的基本概念
- 分析测试报告，理解测试覆盖范围

测试报告将生成在 `reports/test_report.html` 文件中，包含详细的测试结果和执行时间等信息。

## 📝 学习建议

1. **循序渐进**：按照推荐学习路径，从基础API开发开始，逐步掌握AI功能集成

2. **动手实践**：不要只是阅读代码，尝试修改和扩展功能来加深理解

3. **查阅文档**：结合项目代码学习，查阅相关技术的官方文档
   - [FastAPI文档](https://fastapi.tiangolo.com/)
   - [LangChain文档](https://python.langchain.com/docs/get_started/introduction)
   - [LangGraph文档](https://langchain-ai.github.io/langgraph/tutorials/quickstart/)
   - [SQLAlchemy文档](https://docs.sqlalchemy.org/)

4. **调试技巧**：利用`--reload`模式进行实时调试，修改代码后观察服务变化

5. **问题解决**：遇到错误时，查看服务日志，使用调试工具分析问题

## 📁 项目学习结构

```
faststudy/
├── main.py                 # 应用入口 - 学习FastAPI应用初始化
├── routers/                # 路由模块 - 学习模块化API设计
│   ├── __init__.py
│   ├── users.py            # 用户相关路由
│   ├── items.py            # 物品相关路由
│   └── llm.py              # LangChain/LangGraph 相关路由 - 学习AI服务集成
├── models/                 # 数据模型 - 学习ORM和数据验证
│   ├── __init__.py
│   ├── database.py         # 数据库初始化和重置 - 学习数据库管理
│   └── schemas.py          # Pydantic 模型 - 学习数据验证
├── static/                 # 静态资源 - 学习前后端交互
│   ├── index.html          # 首页
│   ├── users.html          # 用户管理页面
│   ├── items.html          # 物品管理页面
│   ├── langchain.html      # LangChain 示例页面 - 学习前端调用LLM API
│   └── langgraph.html      # LangGraph 示例页面 - 学习前端调用工作流API
├── examples/               # 核心学习代码 - AI框架实践
│   ├── langchain_example.py # LangChain 示例 - 重点学习文件
│   └── langgraph_example.py # LangGraph 示例 - 重点学习文件
├── tests/                  # 测试文件 - 学习自动化测试
│   ├── test_users_page.py  # 用户页面测试
│   └── test_items_page.py  # 物品页面测试
├── config.py               # 应用配置 - 学习配置管理
├── pyproject.toml          # Poetry 项目配置 - 学习依赖管理
├── poetry.lock             # 依赖锁定文件
└── README.md               # 项目说明文档
```

## 📚 推荐学习路径

### 初级阶段：FastAPI基础
1. 熟悉项目结构和运行环境
2. 学习`main.py`中的应用初始化过程
3. 研究`models/`目录下的数据模型设计
4. 分析`routers/`目录中的API路由实现
5. 运行项目并通过Web界面体验功能

### 中级阶段：LangChain学习
1. 阅读`examples/langchain_example.py`，理解核心概念
2. 重点学习`CustomChatModel`类的实现，了解如何集成自定义模型
3. 研究`simple_llm_call`和`create_chain`函数，掌握基础使用方法
4. 分析`routers/llm.py`，了解如何将LangChain功能暴露为API
5. 通过Web界面测试LangChain功能并查看网络请求

### 高级阶段：LangGraph工作流
1. 阅读`examples/langgraph_example.py`，理解工作流概念
2. 学习`State`定义和节点实现方法
3. 研究`SimpleWorkflow`和`DecisionWorkflow`类的设计
4. 重点分析条件路由的实现方式
5. 通过Web界面测试工作流功能，观察不同输入的路由结果

### 综合阶段：项目扩展
1. 尝试添加新的LangChain链功能
2. 设计并实现自定义的LangGraph工作流
3. 添加新的API端点和前端界面
4. 编写自动化测试验证新功能
5. 优化现有代码，应用最佳实践

## 🔧 开发环境设置

### 环境要求
- Python 3.14+ (64位)
- Poetry (依赖管理)
- Conda (虚拟环境管理)
- Windows 11 (开发环境)
- Visual C++ Build Tools (用于部分Python包编译)
- Rust 开发环境 (安装LangChain相关依赖时需要)

### 学习环境搭建步骤
1. **创建并激活虚拟环境**
   ```powershell
   conda create -n faststudy python=3.14
   conda activate faststudy
   ```

2. **安装项目依赖**
   ```powershell
   poetry install
   ```

3. **修改配置文件（可选）**
   配置文件位于 `config.py`，学习者可以修改数据库路径、API密钥等配置信息来实验不同设置的影响。

## 🏗️ 项目编译

编译项目是学习Python项目构建过程的重要环节：

```powershell
poetry run python compile_project.py
```

编译过程会执行依赖检查、代码优化和部署准备，这是理解Python项目生命周期的好机会。

## 🚀 项目启动

### 启动FastAPI服务

```powershell
# 确保已激活虚拟环境
conda activate faststudy

# 启动服务（带热重载功能）
poetry run uvicorn main:app --reload
```

### 学习访问路径

服务启动后，可以通过以下路径访问和学习：
- **首页**：http://127.0.0.1:8000/ - 了解项目概览
- **用户管理**：http://127.0.0.1:8000/static/users.html - 学习基本CRUD操作
- **物品管理**：http://127.0.0.1:8000/static/items.html - 学习关系型数据操作
- **LangChain示例**：http://127.0.0.1:8000/static/langchain.html - 学习LLM模型集成
- **LangGraph示例**：http://127.0.0.1:8000/static/langgraph.html - 学习工作流设计
- **API文档**：http://127.0.0.1:8000/docs - 学习OpenAPI自动生成文档
- **ReDoc文档**：http://127.0.0.1:8000/redoc - 学习API文档的另一种呈现方式

### 生产模式启动

```powershell
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔍 常见问题

### 1. 服务启动失败

- 确保已安装所有依赖：`poetry install`
- 检查端口是否被占用
- 确保 Python 版本为 3.14 (64位)

### 2. 缺少编译工具

- 确保已安装 Visual C++ Build Tools 和 Rust
- 安装后重启电脑使环境变量生效

### 3. LangChain/LangGraph 功能不可用

- 确保已正确设置 OpenAI API Key
- 检查网络连接是否正常

### 4. 测试失败

- 确保服务已启动
- 确保浏览器驱动已正确安装
- 检查测试文件中的 URL 是否正确

## 📄 许可证

MIT License

Copyright (c) 2025 Kevin Zhang <xprogrammer@163.com>

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题或建议，请联系：
- Email: xprogrammer@163.com
- GitHub: https://github.com/gyzhang/faststudy
