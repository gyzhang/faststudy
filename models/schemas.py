"""
Pydantic模型定义
用于请求和响应数据验证
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# 用户相关的Pydantic模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 物品相关的Pydantic模型
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(ItemBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 包含关系的响应模型
class UserWithItems(UserResponse):
    items: List[ItemResponse] = []

class ItemWithOwner(ItemResponse):
    owner: UserResponse