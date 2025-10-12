# FastAPI 项目功能验证指南

## 🎯 验证步骤

### 1. ✅ 验证服务已启动

**当前状态**: 服务已在 `http://127.0.0.1:8000` 运行

确认终端显示：
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

## 📱 验证界面和文档

### 2. 访问应用首页
**URL**: http://127.0.0.1:8000/static/index.html

**预期结果**: 
- 显示 FastAPI 学习项目的欢迎页面
- 包含项目介绍和快速链接

---

### 3. 访问 Swagger UI（交互式 API 文档）
**URL**: http://127.0.0.1:8000/docs

**预期结果**:
- 显示完整的 API 文档
- 可以直接测试 API 端点
- 包含以下 API 组：
  - Health Check
  - Users API
  - Items API

---

### 4. 访问 ReDoc（备用 API 文档）
**URL**: http://127.0.0.1:8000/redoc

**预期结果**:
- 更美观的 API 文档展示
- 按层级组织的 API 结构

---

## 🔧 验证 API 功能

### 5. 健康检查端点

**方法**: GET
**URL**: http://127.0.0.1:8000/health

**使用浏览器访问或在 PowerShell 中运行**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method Get
```

**预期响应**:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

## 👥 验证用户管理功能

### 6. 创建用户

在 Swagger UI (http://127.0.0.1:8000/docs) 中：

1. 找到 `POST /api/v1/users` 端点
2. 点击 "Try it out"
3. 输入测试数据：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "full_name": "Test User"
}
```
4. 点击 "Execute"

**预期响应** (状态码 201):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2025-10-08T19:00:00"
}
```

**或使用 PowerShell**:
```powershell
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "password123"
    full_name = "Test User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users" -Method Post -Body $body -ContentType "application/json"
```

---

### 7. 获取用户列表

**在 Swagger UI 中**:
1. 找到 `GET /api/v1/users` 端点
2. 点击 "Try it out"
3. 可选设置参数：
   - skip: 0
   - limit: 10
4. 点击 "Execute"

**预期响应**:
```json
[
  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "is_active": true,
    "created_at": "2025-10-08T19:00:00"
  }
]
```

**使用 PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users?skip=0&limit=10" -Method Get
```

---

### 8. 获取单个用户

**在 Swagger UI 中**:
1. 找到 `GET /api/v1/users/{user_id}` 端点
2. 输入 user_id: 1
3. 点击 "Execute"

**使用 PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users/1" -Method Get
```

---

### 9. 更新用户

**在 Swagger UI 中**:
1. 找到 `PUT /api/v1/users/{user_id}` 端点
2. 输入 user_id: 1
3. 输入更新数据：
```json
{
  "full_name": "Updated User",
  "email": "updated@example.com"
}
```

**使用 PowerShell**:
```powershell
$body = @{
    full_name = "Updated User"
    email = "updated@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/users/1" -Method Put -Body $body -ContentType "application/json"
```

---

### 10. 删除用户

**在 Swagger UI 中**:
1. 找到 `DELETE /api/v1/users/{user_id}` 端点
2. 输入 user_id: 1
3. 点击 "Execute"

**预期响应**:
```json
{
  "message": "User deleted successfully"
}
```

---

## 📦 验证物品管理功能

### 11. 创建物品

**测试数据**:
```json
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "tax": 99.99
}
```

**使用 PowerShell**:
```powershell
$body = @{
    name = "Laptop"
    description = "High-performance laptop"
    price = 999.99
    tax = 99.99
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items" -Method Post -Body $body -ContentType "application/json"
```

---

### 12. 搜索物品

**在 Swagger UI 中**:
1. 找到 `GET /api/v1/items` 端点
2. 设置参数：
   - q: "laptop" (搜索关键词)
   - skip: 0
   - limit: 10

**使用 PowerShell**:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/items?q=laptop&skip=0&limit=10" -Method Get
```

---

## 🧪 验证数据验证功能

### 13. 测试无效数据

尝试创建用户时使用无效邮箱：

```json
{
  "username": "test",
  "email": "invalid-email",
  "password": "123"
}
```

**预期结果**: 
- 状态码 422 (Unprocessable Entity)
- 详细的验证错误信息

---

## ✅ 验证清单

完成以下检查项：

- [ ] 服务成功启动
- [ ] 首页正常显示
- [ ] Swagger UI 可访问
- [ ] ReDoc 可访问
- [ ] 健康检查端点工作正常
- [ ] 创建用户成功
- [ ] 获取用户列表成功
- [ ] 获取单个用户成功
- [ ] 更新用户成功
- [ ] 删除用户成功
- [ ] 创建物品成功
- [ ] 搜索物品成功
- [ ] 数据验证正常工作
- [ ] 终端日志正常显示请求记录

---

## 📊 查看日志

在运行 `poetry run uvicorn main:app --reload` 的终端中，您应该看到所有请求的日志：

```
INFO:     127.0.0.1:xxxxx - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "POST /api/v1/users HTTP/1.1" 201 Created
INFO:     127.0.0.1:xxxxx - "GET /api/v1/users HTTP/1.1" 200 OK
```

---

## 🛑 停止服务

完成测试后，在终端按 `Ctrl+C` 停止服务。

---

## 💡 提示

1. **使用 Swagger UI**: 最简单的测试方式，无需编写代码
2. **查看响应**: 注意响应的状态码和数据格式
3. **热重载**: 修改代码后服务会自动重启
4. **错误处理**: 尝试各种边界情况，查看错误处理是否正确

祝测试愉快！🎉