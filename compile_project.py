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
    
    # 复制项目文件结构
    for root, dirs, files in os.walk(source_dir):
        # 跳过不需要的目录
        if '.git' in dirs: dirs.remove('.git')
        if '.venv' in dirs: dirs.remove('.venv')
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        if '.pytest_cache' in dirs: dirs.remove('.pytest_cache')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if 'reports' in dirs: dirs.remove('reports')
        if 'tests' in dirs: dirs.remove('tests')
        # 跳过输出目录，防止递归创建compiled目录
        if os.path.basename(output_dir) in dirs and root == source_dir:
            dirs.remove(os.path.basename(output_dir))
        
        # 创建对应的输出目录
        rel_path = os.path.relpath(root, source_dir)
        if rel_path != '.':
            target_dir = os.path.join(output_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)
        
        # 复制非Python文件
        for file in files:
            if not file.endswith('.py'):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(output_dir, rel_path, file)
                shutil.copy2(src_file, dst_file)
    
    # 编译Python文件为字节码，使用rx参数排除.venv目录
    import re
    venv_pattern = re.compile(r'.*\\.venv\\.*')
    compileall.compile_dir(source_dir, force=True, legacy=True, rx=venv_pattern)
    
    # 收集编译后的.pyc文件并复制到输出目录
    for root, dirs, files in os.walk(source_dir):
        if '__pycache__' in dirs:
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