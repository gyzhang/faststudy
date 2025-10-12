#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目编译脚本
将Python源码编译为字节码(.pyc)文件，用于发布时隐藏源码
"""

import os
import sys
import compileall
import shutil
import argparse


def compile_project(source_dir: str, output_dir: str) -> None:
    """将项目源码编译为字节码文件

    Args:
        source_dir: 源代码目录
        output_dir: 输出目录，用于存放编译后的字节码文件
    """
    print(f"开始编译项目: {source_dir}")
    print(f"输出目录: {output_dir}")
    
    # 确保输出目录存在
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # 定义要排除的目录和文件列表
    excluded_dirs = [
        '.git', '.venv', '__pycache__', '.pytest_cache', 
        'node_modules', 'reports', 'tests', 
        '.idea', '.trae',  # 添加.idea和.trae目录到排除列表
        os.path.basename(output_dir)  # 避免递归创建compiled目录
    ]
    
    # 定义要排除的文件列表
    excluded_files = [
        '.gitignore', 'compile_project.pyc', 'verify_compiled_code.pyc',
        'package.json', 'package-lock.json', 'pyproject.toml', 'poetry.lock', 'pytest.ini'
    ]
    
    print(f"将排除以下开发环境目录: {', '.join(excluded_dirs)}")
    
    # 复制非Python文件和创建目录结构
    for root, dirs, files in os.walk(source_dir):
        # 创建一个列表用于保存需要删除的目录（避免在遍历时修改列表）
        dirs_to_remove = []
        
        # 检查哪些目录需要被排除
        for dir_name in dirs:
            if dir_name in excluded_dirs:
                dirs_to_remove.append(dir_name)
                print(f"  排除目录: {os.path.join(root, dir_name)}")
        
        # 从dirs中移除需要排除的目录
        for dir_name in dirs_to_remove:
            dirs.remove(dir_name)
        
        # 创建对应的输出目录
        rel_path = os.path.relpath(root, source_dir)
        if rel_path != '.':
            target_dir = os.path.join(output_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)
        
        # 复制非Python文件
        for file in files:
            # 确保文件不是Python文件
            if not file.endswith('.py'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(output_dir, rel_path, file)
                
                # 检查文件是否在排除目录内或文件名在排除列表中
                should_copy = True
                
                # 检查文件是否在排除目录内
                for excluded_dir in excluded_dirs:
                    if excluded_dir in src_file:
                        should_copy = False
                        print(f"  排除文件: {src_file}")
                        break
                
                # 检查文件名是否在排除文件列表中
                if should_copy and file in excluded_files:
                    should_copy = False
                    print(f"  排除文件: {src_file}")
                
                if should_copy:
                    shutil.copy2(src_file, dst_file)
    
    # 编译Python文件为字节码
    # 先创建一个临时目录用于编译
    import tempfile
    temp_compile_dir = tempfile.mkdtemp()
    
    print("开始编译Python文件为字节码...")
    
    try:
        # 编译所有Python文件到临时目录
        for root, _, files in os.walk(source_dir):
            # 检查当前目录是否是排除目录
            should_compile = True
            for excluded_dir in excluded_dirs:
                if excluded_dir in root:
                    should_compile = False
                    break
            
            if should_compile:
                for file in files:
                    if file.endswith('.py'):
                        src_file = os.path.join(root, file)
                        # 编译单个文件
                        compileall.compile_file(src_file, legacy=True)
    finally:
        # 不需要清理临时目录，因为我们只需要.pyc文件
        pass
    
    # 收集编译后的.pyc文件并复制到输出目录
    for root, _, files in os.walk(source_dir):
        # 检查当前目录是否是排除目录
        should_collect = True
        for excluded_dir in excluded_dirs:
            if excluded_dir in root:
                should_collect = False
                break
        
        if should_collect and '__pycache__' in os.listdir(root):
            pycache_dir = os.path.join(root, '__pycache__')
            rel_path = os.path.relpath(root, source_dir)
            
            for file in os.listdir(pycache_dir):
                if file.endswith('.pyc'):
                    # 提取原始模块名
                    module_name = file.split('.')[0]
                    src_pyc = os.path.join(pycache_dir, file)
                    dst_pyc = os.path.join(output_dir, rel_path, f'{module_name}.pyc')
                    
                    # 创建目标目录（如果不存在）
                    os.makedirs(os.path.dirname(dst_pyc), exist_ok=True)
                    
                    # 复制.pyc文件并重命名
                    shutil.copy2(src_pyc, dst_pyc)
    
    print("编译完成！")
    print(f"编译后的文件已保存到: {output_dir}")


def create_release_package(output_dir: str, release_name: str) -> None:
    """创建发布包

    Args:
        output_dir: 编译后的文件目录
        release_name: 发布包名称
    """
    import zipfile
    import datetime
    
    # 创建发布包名称（包含日期）
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    release_filename = f"{release_name}_{timestamp}.zip"
    
    print(f"正在创建发布包: {release_filename}")
    
    # 创建ZIP文件
    with zipfile.ZipFile(release_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    
    print(f"发布包创建完成: {release_filename}")


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Python项目编译脚本')
    parser.add_argument('--source', default='.', help='源代码目录')
    parser.add_argument('--output', default='compiled', help='编译输出目录')
    parser.add_argument('--package', action='store_true', help='是否创建发布包')
    
    args = parser.parse_args()
    
    # 执行编译
    compile_project(args.source, args.output)
    
    # 可选：创建发布包
    if args.package:
        # 从pyproject.toml获取项目名称（如果存在）
        try:
            import tomli
            with open(os.path.join(args.source, 'pyproject.toml'), 'rb') as f:
                pyproject = tomli.load(f)
                project_name = pyproject.get('tool', {}).get('poetry', {}).get('name', 'project')
        except:
            project_name = 'project'
        
        create_release_package(args.output, project_name)