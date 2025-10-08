from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from models.schemas import User, UserCreate
from datetime import datetime

router = APIRouter()

# 模拟数据库
fake_users_db = {}
user_id_counter = 1


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """创建新用户"""
    global user_id_counter
    
    # 检查用户名是否已存在
    for existing_user in fake_users_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
    
    user_dict = user.model_dump()
    user_dict["id"] = user_id_counter
    user_dict["is_active"] = True
    user_dict["created_at"] = datetime.now()
    user_dict.pop("password")  # 不返回密码
    
    fake_users_db[user_id_counter] = user_dict
    user_id_counter += 1
    
    return user_dict


@router.get("/users", response_model=List[User])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回的最大记录数")
):
    """获取用户列表（支持分页）"""
    users = list(fake_users_db.values())
    return users[skip : skip + limit]


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据ID获取用户信息"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return fake_users_db[user_id]


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    """更新用户信息"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    user_dict = user.model_dump()
    user_dict["id"] = user_id
    user_dict["is_active"] = fake_users_db[user_id]["is_active"]
    user_dict["created_at"] = fake_users_db[user_id]["created_at"]
    user_dict.pop("password")
    
    fake_users_db[user_id] = user_dict
    return user_dict


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """删除用户"""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    del fake_users_db[user_id]