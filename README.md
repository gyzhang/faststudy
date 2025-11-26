# FastStudy - FastAPI 学习项目

一个包含常用功能演示的 FastAPI 学习项目，涵盖 RESTful API、数据验证、路由组织、依赖注入、自动文档、数据库操作、分页功能以及最新的 LangChain 和 LangGraph v1.0 框架示例。

## 🎯 核心功能

- ✅ **RESTful API** - 完整的 CRUD 操作示例
- ✅ **数据验证** - 使用 Pydantic V2 进行数据验证和序列化
- ✅ **路由组织** - 模块化的路由结构
- ✅ **依赖注入** - 演示依赖注入的使用
- ✅ **自动文档** - Swagger UI 和 ReDoc
- ✅ **真实分页** - 基于数据库的分页实现，使用 `page/page_size` 参数
- ✅ **LangChain v1.0** - LLM 应用开发框架示例
- ✅ **LangGraph v1.0** - 工作流管理框架示例
- ✅ **交互式页面** - 美观的前端页面，支持所有功能的可视化操作
- ✅ **自动化测试** - 完整的 Playwright + Pytest 测试套件

## 📋 技术栈

- **后端框架**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.44
- **数据库**: SQLite
- **数据验证**: Pydantic V2
- **依赖管理**: Poetry
- **前端**: HTML5 + CSS3 + JavaScript
- **LLM 框架**: LangChain 1.0.0, LangGraph 1.0.0
- **测试**: Pytest + Playwright

## 🚀 快速开始

### 环境要求

- Windows 11
- Python 3.14 (64位)
- Visual C++ Build Tools
- Rust 开发环境

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

## 📖 功能使用

### 1. 用户管理

**访问地址**: http://127.0.0.1:8000/static/users.html

功能包括：
- 创建新用户
- 查看用户列表（支持分页）
- 搜索用户
- 编辑用户信息
- 删除用户

### 2. 物品管理

**访问地址**: http://127.0.0.1:8000/static/items.html

功能包括：
- 创建新物品
- 查看物品列表（支持分页）
- 搜索物品
- 编辑物品信息
- 删除物品

### 3. LangChain 示例

**访问地址**: http://127.0.0.1:8000/static/langchain.html

功能包括：
- 简单 LLM 调用
- 链调用示例
- 翻译功能

### 4. LangGraph 示例

**访问地址**: http://127.0.0.1:8000/static/langgraph.html

功能包括：
- 对话工作流
- 决策工作流（支持问题回答、翻译、总结）

## 🔌 API 示例

### 健康检查
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health -Method Get
```

### 用户列表（带分页）
```powershell
# 获取第1页，每页10条数据
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users?page=1&page_size=10" -Method Get
```

### 创建用户
```powershell
$userData = @{
    username = "testuser"
    email = "testuser@example.com"
    password = "password123"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users" -Method Post -ContentType "application/json" -Body $userData
```

### 物品列表（带分页）
```powershell
# 获取第2页，每页5条数据
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items?page=2&page_size=5" -Method Get
```

### 创建物品
```powershell
$itemData = @{
    name = "Sample Item"
    description = "This is a sample item"
    price = 9.99
    owner_id = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items" -Method Post -ContentType "application/json" -Body $itemData
```

## 🗄️ 数据库操作

### 数据库初始化

项目使用 SQLite 数据库，首次运行会自动初始化，创建 `users` 和 `items` 表，并插入测试数据：
- 10 个测试用户
- 30 个测试物品（每个用户 3 个）

### 数据库重置

如需重置数据库并重新插入测试数据，执行以下命令：

```powershell
# 方式1：删除数据库文件后重启服务
Remove-Item -Force .\faststudy.db
poetry run uvicorn main:app --reload

# 方式2：调用重置函数
poetry run python -c "from models.database import reset_db; reset_db()"
```

## 🧪 自动化测试

### 运行测试

确保服务已启动，然后在另一个终端中执行：

```powershell
# 执行所有测试
poetry run pytest tests/ -v

# 生成 HTML 测试报告
poetry run pytest tests/ -v --html=reports/test_report.html --self-contained-html
```

### 测试报告

测试报告将生成在 `reports/test_report.html` 文件中，包含详细的测试结果、执行时间等信息。

## 📁 项目结构

```
faststudy/
├── main.py                 # 应用入口
├── routers/                # 路由模块
│   ├── __init__.py
│   ├── users.py            # 用户相关路由
│   ├── items.py            # 物品相关路由
│   └── llm.py              # LangChain/LangGraph 相关路由
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── database.py         # 数据库初始化和重置
│   └── schemas.py          # Pydantic 模型
├── static/                 # 静态资源
│   ├── index.html          # 首页
│   ├── users.html          # 用户管理页面
│   ├── items.html          # 物品管理页面
│   ├── langchain.html      # LangChain 示例页面
│   └── langgraph.html      # LangGraph 示例页面
├── examples/               # 示例代码
│   ├── langchain_example.py # LangChain 示例
│   └── langgraph_example.py # LangGraph 示例
├── tests/                  # 测试文件
│   ├── test_users_page.py  # 用户页面测试
│   └── test_items_page.py  # 物品页面测试
├── config.py               # 应用配置
├── pyproject.toml          # Poetry 项目配置
├── poetry.lock             # 依赖锁定文件
└── README.md               # 项目说明文档
```

## 🔧 开发环境

### 环境要求

- Windows 11
- Python 3.14 (64位)
- Visual C++ Build Tools
- Rust 开发环境
- PowerShell 7 (推荐)

### 依赖管理

使用 Poetry 管理项目依赖：

```powershell
# 安装依赖
poetry install

# 更新依赖
poetry update

# 添加新依赖
poetry add <package-name>

# 添加开发依赖
poetry add --group dev <package-name>
```

## 🚀 项目启动

```powershell
# 开发模式启动（带热重载）
poetry run uvicorn main:app --reload

# 生产模式启动
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
