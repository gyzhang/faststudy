# 项目规则
## 这是一个Python项目
- 项目只在Windows11下开发测试运行
- 项目使用Python 3.14
- 项目的虚拟环境为 .venv
- 项目使用Poetry作为依赖管理工具
- 项目使用SQLAlchemy作为ORM
- 项目使用SQLite作为数据库
  - 数据库文件为 faststudy.db
  - 数据库初始化时会自动创建表结构
  - 数据库初始化时会自动插入测试数据（约 10 个用户、30 个物品）
  - 数据库初始化时会自动设置时区为 UTC+8
- 项目使用Pydantic作为数据验证与序列化
- 项目使用FastAPI作为Web框架
## 项目运行的命令
- 项目运行时，需要启动FastAPI服务：`poetry run uvicorn main:app --reload`
- 严格限制运行项目的命令是：`poetry run uvicorn main:app --reload`
- 严格限制启动服务的命令是：`poetry run uvicorn main:app --reload`
- 限制：
  - 项目只在Windows11下开发测试运行
  - 项目不支持在其他操作系统下运行
  - 只是用Windows11下的Powershell命令，不要用其他操作系统下的命令，特别是不要用Linux的命令
  - 项目的虚拟环境必须为 .venv
  - 不要自作主张尝试其他命令启动项目或服务
