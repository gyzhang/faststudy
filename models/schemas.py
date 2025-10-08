from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")


class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., min_length=6, description="密码")


class User(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    is_active: bool = Field(True, description="是否激活")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")

    class Config:
        from_attributes = True


class ItemBase(BaseModel):
    """物品基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="物品名称")
    description: Optional[str] = Field(None, max_length=500, description="物品描述")
    price: float = Field(..., gt=0, description="价格")
    tax: Optional[float] = Field(None, ge=0, description="税费")


class ItemCreate(ItemBase):
    """创建物品模型"""
    pass


class Item(ItemBase):
    """物品响应模型"""
    id: int = Field(..., description="物品ID")
    owner_id: int = Field(..., description="拥有者ID")

    class Config:
        from_attributes = True