from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from models.schemas import Item, ItemCreate

router = APIRouter()

# 模拟数据库
fake_items_db = {}
item_id_counter = 1


def get_current_user_id():
    """依赖注入示例 - 获取当前用户ID（模拟）"""
    # 实际应用中这里会验证token并返回真实用户ID
    return 1


@router.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    """创建新物品（演示依赖注入）"""
    global item_id_counter
    
    item_dict = item.model_dump()
    item_dict["id"] = item_id_counter
    item_dict["owner_id"] = current_user_id
    
    fake_items_db[item_id_counter] = item_dict
    item_id_counter += 1
    
    return item_dict


@router.get("/items", response_model=List[Item])
async def get_items(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
):
    """获取物品列表（支持搜索和分页）"""
    items = list(fake_items_db.values())
    
    # 搜索过滤
    if search:
        items = [
            item for item in items
            if search.lower() in item["name"].lower()
            or (item["description"] and search.lower() in item["description"].lower())
        ]
    
    return items[skip : skip + limit]


@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """根据ID获取物品信息"""
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    return fake_items_db[item_id]


@router.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item: ItemCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    """更新物品信息"""
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    # 检查权限
    if fake_items_db[item_id]["owner_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限修改此物品"
        )
    
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    item_dict["owner_id"] = current_user_id
    
    fake_items_db[item_id] = item_dict
    return item_dict


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    current_user_id: int = Depends(get_current_user_id)
):
    """删除物品"""
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物品不存在"
        )
    
    if fake_items_db[item_id]["owner_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限删除此物品"
        )
    
    del fake_items_db[item_id]