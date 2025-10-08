"""
数据库配置和模型定义
使用SQLAlchemy + SQLite内存数据库
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# 创建文件数据库引擎（修复多线程问题）
engine = create_engine('sqlite:///faststudy.db', echo=True, connect_args={"check_same_thread": False})

# 创建基类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    items = relationship("Item", back_populates="owner")

class Item(Base):
    """物品模型"""
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    owner = relationship("User", back_populates="items")

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)
    
    # 创建初始数据
    db = SessionLocal()
    try:
        # 创建测试用户
        user1 = User(username="john_doe", email="john@example.com", full_name="John Doe")
        user2 = User(username="jane_smith", email="jane@example.com", full_name="Jane Smith")
        
        db.add(user1)
        db.add(user2)
        db.commit()
        
        # 创建测试物品
        item1 = Item(name="笔记本电脑", description="高性能笔记本电脑", price=5999.99, owner_id=user1.id)
        item2 = Item(name="智能手机", description="最新款智能手机", price=3999.50, owner_id=user1.id)
        item3 = Item(name="平板电脑", description="便携式平板", price=1999.00, owner_id=user2.id)
        
        db.add(item1)
        db.add(item2)
        db.add(item3)
        db.commit()
        
    finally:
        db.close()

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库并创建测试数据"""
    Base.metadata.create_all(bind=engine)
    
    # 创建初始数据
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_users = db.query(User).count()
        if existing_users == 0:
            # 创建测试用户
            user1 = User(username="john_doe", email="john@example.com", full_name="John Doe")
            user2 = User(username="jane_smith", email="jane@example.com", full_name="Jane Smith")
            
            db.add(user1)
            db.add(user2)
            db.commit()
            
            # 创建测试物品
            item1 = Item(name="笔记本电脑", description="高性能笔记本电脑", price=5999.99, owner_id=user1.id)
            item2 = Item(name="智能手机", description="最新款智能手机", price=3999.50, owner_id=user1.id)
            item3 = Item(name="平板电脑", description="便携式平板", price=1999.00, owner_id=user2.id)
            
            db.add(item1)
            db.add(item2)
            db.add(item3)
            db.commit()
            print("数据库初始化完成，已创建测试数据")
        else:
            print("数据库已存在，跳过初始化")
    finally:
        db.close()