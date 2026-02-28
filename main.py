#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天龙获客引擎 - 根目录入口
"""

import sys
import os

# 自动处理路径：将 automation 文件夹加入搜索路径并切换工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
automation_dir = os.path.join(current_dir, "automation")

if os.path.exists(automation_dir):
    sys.path.append(automation_dir)
    os.chdir(automation_dir)
    
    try:
        from console import main as start_console
        if __name__ == "__main__":
            start_console()
    except ImportError as e:
        print(f"❌ 启动失败：无法加载自动化模块。请确保 {automation_dir} 目录完整。")
        print(f"错误详情: {e}")
else:
    print(f"❌ 错误：找不到自动化目录 {automation_dir}")
