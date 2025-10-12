# FastStudy (Windows 环境指南)

本项目为 FastAPI 学习项目，演示常用功能（静态资源、路由、数据库、分页、依赖注入等）。本指南仅针对 Windows 环境（建议使用 PowerShell 7）。

## 一、准备环境（必须先安装）

1) 安装微软 Visual C++ Build Tools
- 打开: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- 下载并运行 "Build Tools for Visual Studio"
- 在安装界面勾选:
  - "Desktop development with C++"
  - "MSVC v143 - VS 2022 C++ x64/x86 build tools"（版本号可能略有不同）
  - "Windows 11 SDK"（或与你系统版本匹配的 SDK）
- 点击 "安装" 或 "修改"，等待完成（可能需要数 GB）
- 完成后重启电脑

2) 安装 Rust 开发环境
- 打开: https://www.rust-lang.org/tools/install
- 下载并运行 Windows 安装程序
- 使用默认选项完成安装
- 安装后关闭并重新打开命令行窗口，使环境变量生效

3) 安装 Python 与 PowerShell（建议）
- Python 版本：3.14（64 位）
- 终端建议：PowerShell 7（https://aka.ms/PSWindows）

## 二、获取项目并安装依赖

在 PowerShell 中执行：

```powershell
# 切换到你的工作目录
cd D:\Kevin\AI

# 克隆或确保项目目录存在后进入
cd .\faststudy

# 安装 Poetry（如未安装）
# 官方安装脚本（适用于 Windows）
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# 确认 Poetry 可用（需要重开终端或执行以下命令刷新环境变量）
poetry --version

# 创建并安装项目依赖
poetry install
```

## 三、启动服务

**注意：请严格使用以下命令启动项目：**

```powershell
poetry run uvicorn main:app --reload
```

成功后你会看到类似日志：
- Uvicorn running on http://127.0.0.1:8000
- Started reloader process using WatchFiles

访问：
- 首页: http://127.0.0.1:8000/
- 文档: http://127.0.0.1:8000/docs

## 四、快速接口测试（PowerShell）

```powershell
# 健康检查
irm http://127.0.0.1:8000/health

# 用户列表（分页参数）
irm "http://127.0.0.1:8000/api/v1/users?skip=0&limit=10"

# 创建用户
$u = @{ username="testuser"; email="testuser@example.com"; full_name="Test User" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users" -Method Post -ContentType "application/json" -Body $u

# 物品列表
irm "http://127.0.0.1:8000/api/v1/items?skip=0&limit=10"

# 创建物品（将 owner_id 替换为实际用户 id）
$item = @{ name="Sample Item"; description="demo"; price=9.99; owner_id=1 } | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items" -Method Post -ContentType "application/json" -Body $item
```

## 五、数据库初始化与重置

项目使用 SQLite（faststudy.db）。首次运行会自动初始化。若需要重置并插入更多测试数据（约 10 个用户、30 个物品），有两种方式：

- 方式 A：删除数据库文件后重启（触发自动初始化）
```powershell
# 停止服务后执行
Remove-Item -Force .\faststudy.db
poetry run uvicorn main:app --reload
```

- 方式 B：调用重置函数（无需手动删库文件）
```powershell
poetry run python -c "from models.database import reset_db; reset_db()"
```

重置完成后验证数据量：
```powershell
$u = irm "http://127.0.0.1:8000/api/v1/users?limit=100"; "users: $($u.Count)"
$it = irm "http://127.0.0.1:8000/api/v1/items?limit=100"; "items: $($it.Count)"
```

## 六、常见问题排查（Windows）

- 页面打不开或连接被拒绝
  - 确保服务已启动并在日志中显示 `Uvicorn running on http://127.0.0.1:8000`
  - 检查是否被防火墙拦截，或端口被占用

- 缺少编译工具或构建失败
  - 请先完成“Visual C++ Build Tools”安装并重启电脑
  - 确认已安装 Windows SDK 与 MSVC v143

- 缺少 Rust 或某些依赖需要 Rust
  - 按前述步骤安装 Rust，并重启命令行窗口

- 依赖安装异常
  - 尝试 `poetry install`，确保安装完整依赖
  - 使用 64 位 Python 3.14，避免混杂多版本 Python

## 七、自动化测试

项目包含完整的自动化测试套件，使用 Playwright 和 Pytest 实现，支持生成HTML格式的测试报告。测试文件位于 `tests/` 目录下：

- `test_users_page.py`：用户管理页面的自动化测试
- `test_items_page.py`：物品管理页面的自动化测试

**测试先决条件：**

自动化测试需要以下环境：
- Node.js（最新LTS版本）
- npm依赖（包含Playwright）
- Playwright浏览器
- pytest-html（用于生成HTML格式的测试报告）

具体安装步骤请参考 `doc/AUTOMATED_TESTING_GUIDE.md` 文件。

**运行测试前请确保服务已启动**，然后在另一个终端中执行以下命令运行测试并生成HTML格式的测试报告：

```powershell
# 执行测试并生成HTML格式的测试报告
poetry run pytest tests/ -v --html=reports/test_report.html --self-contained-html

# 或使用配置文件（简化命令）
poetry run pytest tests/
```

测试报告将生成在 `reports/test_report.html` 文件中，可以使用浏览器打开查看详细的测试结果，包括测试总数、通过/失败情况、执行时间等信息。

## 八、项目结构（简要）

- main.py：应用入口与路由挂载、静态资源
- routers/：用户与物品相关路由
- models/：SQLAlchemy 模型与数据库初始化/重置
- static/：静态资源（首页、图标等）
- config.py：应用配置（HOST、PORT 等）
- tests/：自动化测试文件
- doc/：项目文档文件（测试指南、发布指南等）
- pyproject.toml：Poetry 项目配置与依赖

## 九、项目发布

### 9.1 发布时隐藏源代码

如果您需要在发布项目时不包含源代码，可以使用项目中提供的编译脚本将Python代码编译为字节码(.pyc)文件。

编译步骤：

```powershell
# 在项目根目录下执行
poetry run python compile_project.py

# 可选：创建发布包
poetry run python compile_project.py --package
```

编译后的文件将保存在`compiled`目录中，编译后的目录结构包含：
- 所有必要的配置文件（.env, pyproject.toml, pytest.ini等）
- 静态资源文件（static/目录）
- 文档文件（README.md, TESTING_GUIDE.md等）
- 编译后的Python字节码文件（以.pyc格式存在）

编译过程会移除源代码文件，仅保留编译后的字节码文件，提高代码安全性。

### 9.2 验证编译后的代码

项目提供了一个验证脚本来确保编译后的代码功能完整：

```powershell
# 在项目根目录下执行验证
poetry run python verify_compiled_code.py
```

验证脚本会检查以下关键模块是否正常工作：
- 数据库模块（models.database）
- 数据模型（models.schemas）
- 路由模块（routers.items, routers.users）
- 主应用模块（main）

如果所有模块验证成功，输出将显示"所有关键模块验证成功！编译后的代码功能完整。"

### 9.3 运行编译后的项目

编译后的项目可以在项目根目录下使用Python模块方式运行：

```powershell
# 在项目根目录下运行服务
poetry run python -m uvicorn --app-dir=compiled main:app --reload
```

编译后的项目不需要源代码文件即可正常运行，功能与原始项目完全一致。

### 9.4 详细信息

关于项目发布的更多详细信息，请参考`doc/PROJECT_RELEASE_GUIDE.md`文件，其中包含编译原理、增强安全性建议和完整发布流程。

## 十、许可证

MIT License

Copyright (c) 2025 Kevin Zhang <xprogrammer@163.com>