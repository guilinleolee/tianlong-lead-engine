#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天龙获客引擎 - 主控制台
集成：电鸭 + 程序员客栈全自动化监控
"""

import sys
import os
from pathlib import Path

# 强制 UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def print_banner():
    print("=" * 60)
    print("🐉 天龙获客引擎 (Tianlong Lead Engine) v2.0")
    print("=" * 60)

def main():
    print_banner()
    print("\n请选择操作：")
    print("1. 🚀 运行全平台获客流水线 (电鸭 + 程序员客栈)")
    print("2. 📊 查看 CRM 仪表盘")
    print("3. 🤖 启动 AI 回复生成器 (交互模式)")
    print("4. 📋 查看今日获客简报")
    print("0. 退出")
    
    choice = input("\n输入选择 [0-4]: ").strip()
    
    if choice == '1':
        from lead_orchestrator import run_pipeline
        report_path = run_pipeline()
        print(f"\n✅ 执行完成！简报位置：{report_path}")
        
    elif choice == '2':
        from crm_manager import SimpleCRM
        crm = SimpleCRM()
        crm.print_dashboard()
        
    elif choice == '3':
        from ai_responder import interactive_mode
        interactive_mode()
        
    elif choice == '4':
        report_dir = Path("d:/编程兼职/automation/reports")
        reports = sorted(list(report_dir.glob("*.md")), reverse=True)
        if reports:
            print(f"\n最新简报内容 ({reports[0].name}):\n")
            with open(reports[0], 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("\n❌ 尚未生成任何简报。")
            
    elif choice == '0':
        print("\n再见！")
        
    else:
        print("\n无效选择。")

if __name__ == "__main__":
    main()
