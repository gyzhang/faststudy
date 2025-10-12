"""
数据库配置和模型定义
使用SQLAlchemy + SQLite内存数据库
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime, timezone, timedelta

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
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=8))))
    
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
    created_at = Column(DateTime, default=datetime.now(timezone(timedelta(hours=8))))
    
    # 关系
    owner = relationship("User", back_populates="items")

def _create_test_data(db: Session) -> None:
    """创建测试数据（10个用户和30个物品）"""
    # 创建 10 个测试用户
    base_users = [
        ("john_doe", "john@example.com", "John Doe"),
        ("jane_smith", "jane@example.com", "Jane Smith"),
        ("alice_wang", "alice@example.com", "Alice Wang"),
        ("bob_lee", "bob@example.com", "Bob Lee"),
        ("charlie_zhang", "charlie@example.com", "Charlie Zhang"),
        ("david_liu", "david@example.com", "David Liu"),
        ("eva_chen", "eva@example.com", "Eva Chen"),
        ("frank_zhao", "frank@example.com", "Frank Zhao"),
        ("grace_lin", "grace@example.com", "Grace Lin"),
        ("henry_guo", "henry@example.com", "Henry Guo"),
    ]
    users = []
    for u in base_users:
        user = User(username=u[0], email=u[1], full_name=u[2])
        db.add(user)
        users.append(user)
    db.commit()  # 提交以获取用户ID

    # 创建 30 个测试物品（每个用户分配 3 件物品）
    for idx, user in enumerate(users):
        for j in range(1, 4):
            name = f"测试物品{idx+1}-{j}"
            description = f"这是为用户 {user.username} 生成的第 {j} 个测试物品"
            # 简单的价格分布
            price = round(99.0 + (idx * 10) + j * 3.5, 2)
            db.add(Item(name=name, description=description, price=price, owner_id=user.id))
    db.commit()


def reset_db():
    """强制重置数据库并插入扩充测试数据（用户10条、物品30条）"""
    # 关闭现有连接，确保可安全重置
    try:
        engine.dispose()
    except Exception:
        pass

    # 删除并重建所有表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        _create_test_data(db)
        print("数据库已重置：创建 10 个用户、30 个物品")
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
    """初始化数据库并创建测试数据（扩充：用户10条、物品30条）"""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_users = db.query(User).count()
        if existing_users == 0:
            _create_test_data(db)
            print("数据库初始化完成：已创建 10 个用户、30 个物品")
        else:
            print("数据库已存在，跳过初始化")
    finally:
        db.close()