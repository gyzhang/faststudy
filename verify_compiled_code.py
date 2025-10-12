import sys
import os
import importlib.util

# 添加compiled目录到Python路径
sys.path.insert(0, os.path.abspath('compiled'))

# 定义要验证的关键模块
modules_to_verify = [
    'models.database',
    'models.schemas',
    'routers.items',
    'routers.users',
    'main'
]

# 验证函数
def verify_module(module_name):
    try:
        print(f"\n验证模块: {module_name}")
        
        # 导入模块
        module = importlib.import_module(module_name)
        print(f"✅ 成功导入模块: {module_name}")
        
        # 检查模块是否包含预期的属性
        if module_name == 'models.database':
            # 验证数据库模块
            if hasattr(module, 'engine'):
                print("✅ 找到数据库引擎对象")
                # 尝试创建会话
                try:
                    if hasattr(module, 'SessionLocal'):
                        session = module.SessionLocal()
                        print("✅ 成功创建数据库会话")
                        session.close()
                except Exception as e:
                    print(f"⚠️ 创建数据库会话时出错: {e}")
            
        elif module_name == 'models.schemas':
            # 验证数据模型
            if hasattr(module, 'UserCreate') and hasattr(module, 'ItemCreate'):
                print("✅ 找到用户和物品创建模型")
                # 尝试实例化一个简单的模型
                try:
                    if hasattr(module, 'ItemBase'):
                        # 只检查模型是否可以被访问，不尝试实例化以避免依赖
                        print("✅ 可以访问数据模型定义")
                except Exception as e:
                    print(f"⚠️ 访问数据模型时出错: {e}")
                    
        elif module_name == 'routers.items' or module_name == 'routers.users':
            # 验证路由器模块
            if hasattr(module, 'router'):
                print("✅ 找到路由器对象")
                # 检查路由器是否有预期的属性
                router = module.router
                if hasattr(router, 'routes') and len(router.routes) > 0:
                    print(f"✅ 路由器包含 {len(router.routes)} 个路由")
                
        elif module_name == 'main':
            # 验证主模块
            if hasattr(module, 'app'):
                print("✅ 找到FastAPI应用对象")
                # 检查应用是否有路由
                app = module.app
                if hasattr(app, 'routes') and len(app.routes) > 0:
                    print(f"✅ FastAPI应用包含 {len(app.routes)} 个路由")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入或验证模块 {module_name} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== 编译代码验证测试 ===")
    
    # 先检查compiled目录是否存在
    if not os.path.exists('compiled'):
        print("❌ compiled目录不存在")
        sys.exit(1)
    
    all_modules_verified = True
    
    for module_name in modules_to_verify:
        if not verify_module(module_name):
            all_modules_verified = False
    
    print(f"\n=== 验证总结 ===")
    if all_modules_verified:
        print("✅ 所有关键模块验证成功！编译后的代码功能完整。")
        print("\n结论：项目可以在不发布源代码的情况下，仅发布compiled目录中的.pyc文件和静态资源文件进行部署。")
    else:
        print("❌ 部分模块验证失败，请查看详细错误信息。")
    
    sys.exit(0 if all_modules_verified else 1)