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

## 七、项目结构（简要）

- main.py：应用入口与路由挂载、静态资源
- routers/：用户与物品相关路由
- models/：SQLAlchemy 模型与数据库初始化/重置
- static/：静态资源（首页、图标等）
- config.py：应用配置（HOST、PORT 等）
- pyproject.toml：Poetry 项目配置与依赖

## 八、许可证

MIT License