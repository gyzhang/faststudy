# FastAPI 学习项目

这是一个用于学习 FastAPI 的完整示例项目，包含了 FastAPI 开发中常用的功能和最佳实践。

## 📋 项目特性

- ✅ **RESTful API 设计** - 完整的 CRUD 操作示例
- ✅ **数据验证** - 使用 Pydantic 进行请求/响应数据验证
- ✅ **路由组织** - 模块化的路由结构，便于维护
- ✅ **依赖注入** - 演示 FastAPI 的依赖注入系统
- ✅ **中间件** - CORS 中间件配置示例
- ✅ **静态文件服务** - 提供静态文件访问
- ✅ **自动文档** - 自动生成 Swagger UI 和 ReDoc 文档
- ✅ **错误处理** - 统一的异常处理
- ✅ **配置管理** - 使用环境变量管理配置
- ✅ **Jupyter Notebook 支持** - 集成开发环境，便于学习和调试
- ✅ **Web 界面** - 完整的 CRUD 操作页面，支持用户和物品管理

## 🚀 快速开始

### 前置要求

- **Python**: 3.11 或更高版本（当前项目在 Python 3.13 上测试）
- **Poetry**: 2.0+ （包管理工具）

**安装 Poetry**:

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

验证安装：
```bash
poetry --version
```

### 1. 安装依赖

```bash
poetry install
```

### 2. 运行项目

**方式1：使用 `poetry run`（推荐）**

无需激活虚拟环境，直接运行：

```bash
# 使用 uvicorn 启动（推荐）
poetry run uvicorn main:app --reload

# 或使用 Python
poetry run python main.py
```

**方式2：激活虚拟环境后运行**

```bash
# 获取激活命令
poetry env activate

# 复制并执行输出的激活命令（PowerShell示例）
& "C:\Users\...\virtualenvs\faststudy-...\Scripts\activate.ps1"

# 然后直接运行
python main.py
```

> **注意**: Poetry 2.0+ 已移除 `poetry shell` 命令，推荐使用 `poetry run` 或 `poetry env activate`

### 3. 访问应用

- **应用首页**: http://127.0.0.1:8000 (自动重定向到静态首页)
- **用户管理界面**: http://127.0.0.1:8000/static/users.html
- **物品管理界面**: http://127.0.0.1:8000/static/items.html
- **Swagger UI 文档**: http://127.0.0.1:8000/docs
- **ReDoc 文档**: http://127.0.0.1:8000/redoc
- **健康检查**: http://127.0.0.1:8000/health
- **Jupyter Notebook**: http://localhost:8888 (启动后访问)

### 4. Web 界面功能

项目提供了完整的 Web 操作界面：

**用户管理功能**:
- ✅ 创建新用户
- ✅ 查看用户列表（支持分页）
- ✅ 搜索用户
- ✅ 编辑用户信息
- ✅ 删除用户

**物品管理功能**:
- ✅ 创建新物品
- ✅ 查看物品列表（支持搜索和分页）
- ✅ 编辑物品信息
- ✅ 删除物品（包含权限验证）

### 5. 启动 Jupyter Notebook

项目已集成 Jupyter Notebook，便于代码学习和调试：

```bash
# 启动 Jupyter Notebook
poetry run jupyter notebook

# 或使用无浏览器模式
poetry run jupyter notebook --no-browser
```

Notebook 将自动使用项目的虚拟环境，可以访问所有已安装的依赖包。

## 📁 项目结构

```
faststudy/
├── main.py                 # 应用入口文件（包含根路径重定向）
├── config.py               # 配置管理
├── pyproject.toml          # Poetry 配置和依赖管理
├── .env                    # 环境变量配置
├── models/                 # 数据模型
│   ├── __init__.py
│   └── schemas.py          # Pydantic 模型定义
├── routers/                # 路由模块
│   ├── __init__.py
│   ├── users.py            # 用户相关路由
│   └── items.py            # 物品相关路由
└── static/                 # 静态文件
    ├── index.html          # 欢迎页面
    ├── users.html          # 用户管理界面
    └── items.html          # 物品管理界面
```

## 🔧 API 端点

### 用户管理 (Users)

- `POST /api/v1/users` - 创建用户
- `GET /api/v1/users` - 获取用户列表（支持分页）
- `GET /api/v1/users/{user_id}` - 获取单个用户
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 物品管理 (Items)

- `POST /api/v1/items` - 创建物品
- `GET /api/v1/items` - 获取物品列表（支持搜索和分页）
- `GET /api/v1/items/{item_id}` - 获取单个物品
- `PUT /api/v1/items/{item_id}` - 更新物品信息
- `DELETE /api/v1/items/{item_id}` - 删除物品

## 📖 学习要点

### 1. Pydantic 数据验证

项目使用 Pydantic 模型进行数据验证，参见 `models/schemas.py`：

```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
```

### 2. 路由组织

使用 APIRouter 组织路由，保持代码模块化：

```python
router = APIRouter()

@router.post("/users")
async def create_user(user: UserCreate):
    ...
```

### 3. 依赖注入

FastAPI 的依赖注入系统示例（见 `routers/items.py`）：

```python
def get_current_user_id():
    return 1

@router.post("/items")
async def create_item(
    item: ItemCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    ...
```

### 4. 查询参数和分页

支持查询参数和分页：

```python
@router.get("/users")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    ...
```

## 📦 Poetry 常用命令

```bash
# 安装依赖
poetry install

# 添加新依赖
poetry add package-name

# 添加开发依赖
poetry add --group dev package-name

# 移除依赖
poetry remove package-name

# 更新所有依赖
poetry update

# 更新指定依赖
poetry update package-name

# 查看依赖列表
poetry show

# 查看依赖树
poetry show --tree

# 查看过期的依赖
poetry show --outdated

# 获取虚拟环境激活命令
poetry env activate

# 查看虚拟环境信息
poetry env info

# 运行命令（不激活环境，推荐）
poetry run python main.py
poetry run uvicorn main:app --reload
poetry run jupyter notebook
poetry run pytest

# 导出依赖到 requirements.txt
poetry export -f requirements.txt --output requirements.txt
```

> **提示**: Poetry 2.0+ 推荐使用 `poetry run` 来执行命令，无需手动激活虚拟环境

## 🎯 下一步学习建议

1. **数据库集成** - 集成 SQLAlchemy 或 Tortoise ORM
2. **认证授权** - 实现 JWT 认证和权限控制
3. **异步操作** - 学习异步数据库操作
4. **测试** - 使用 pytest 编写单元测试和集成测试（已包含测试依赖）
5. **部署** - 学习 Docker 容器化和云部署
6. **Notebook 实验** - 使用 Jupyter Notebook 进行 API 测试和数据分析

## 🔬 Jupyter Notebook 使用指南

项目已配置 Jupyter Notebook 开发环境，支持：

### 在 Notebook 中测试 FastAPI

```python
# 在 notebook 中导入项目模块
from main import app
from routers.users import router as users_router
from models.schemas import UserCreate

# 测试 API 功能
import httpx

# 创建测试客户端
client = httpx.Client(base_url="http://127.0.0.1:8000")

# 测试用户创建
response = client.post("/api/v1/users", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
})
print(response.json())
```

### 利用虚拟环境优势

- Notebook 自动使用项目的 Poetry 虚拟环境
- 可以直接导入项目中的所有模块和依赖
- 便于进行 API 测试、数据分析和学习实验

## 📚 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Uvicorn 文档](https://www.uvicorn.org/)

## ⚡ 提示

- 所有数据目前存储在内存中（字典），重启后会丢失
- 这是一个学习项目，实际生产环境需要使用真实数据库
- 密码处理过于简单，实际应用需要加密存储

祝学习愉快！🎉