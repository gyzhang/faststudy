from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models.database import get_db
from models.schemas import ItemCreate, ItemResponse, ItemUpdate, PaginatedResponse
from models.database import Item, User

router = APIRouter()

def get_current_user_id(db: Session = Depends(get_db)):
    """依赖注入示例 - 获取当前用户ID（模拟）"""
    # 实际应用中这里会验证token并返回真实用户ID
    # 这里返回第一个活跃用户作为示例
    user = db.query(User).filter(User.is_active == True).first()
    return user.id if user else 1


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """创建新物品（演示依赖注入）"""
    # 检查用户是否存在
    user = db.query(User).filter(User.id == current_user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 创建新物品
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        owner_id=current_user_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/items", response_model=PaginatedResponse[ItemResponse])
async def get_items(
    page: int = Query(1, ge=1, description="当前页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """获取物品列表（支持搜索和分页）"""
    query = db.query(Item)
    
    # 搜索过滤
    if search:
        query = query.filter(
            (Item.name.ilike(f"%{search}%")) |
            (Item.description.ilike(f"%{search}%"))
        )
    
    # 计算总记录数
    total = query.count()
    
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size
    
    # 计算跳过的记录数
    skip = (page - 1) * page_size
    
    # 查询数据
    items = query.offset(skip).limit(page_size).all()
    
    # 返回包含分页信息的响应
    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        data=items
    )


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """根据ID获取物品信息"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    return item


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """更新物品信息"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    # 检查权限
    if item.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此物品"
        )
    
    # 更新字段
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """删除物品"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    if item.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此物品"
        )
    
    db.delete(item)
    db.commit()