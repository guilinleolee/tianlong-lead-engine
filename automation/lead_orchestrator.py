#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获客编排器 (Lead Orchestrator) v2.5
功能：集成电鸭、程序员客栈、猿急送、实现网全平台监控
作者：李秘 (AI Agent)
"""

import time
import os
from datetime import datetime
from pathlib import Path
from eleduck_monitor import EleDuckMonitor
from proginn_monitor import ProginnMonitor
from shixian_monitor import ShixianMonitor
from yuanjisong_monitor import YuanjisongMonitor
from crm_manager import SimpleCRM
from ai_responder import AIResponder
from feishu_notifier import FeishuNotifier
from serverchan_notifier import ServerChanNotifier
import config
import sys

# 强制 UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [Orchestrator] {message}")

def generate_report(qualified_leads):
    """生成每日获客简报 Markdown"""
    report_dir = Path("d:/编程兼职/automation/reports")
    report_dir.mkdir(exist_ok=True)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    report_file = report_dir / f"lead_report_{date_str}.md"
    
    lines = [
        f"# 🎯 获客自动化执行简报 ({date_str})",
        f"\n> 执行时间：{datetime.now().strftime('%H:%M:%S')}",
        "\n## 📈 获客概览",
        f"- **总计线索**：{len(qualified_leads)} 条",
        f"- **平台分布**：{', '.join(set(l['source'] for l in qualified_leads)) if qualified_leads else '无'}",
        "\n---",
        "\n## 📝 待开发线索列表"
    ]
    
    if not qualified_leads:
        lines.append("\n> 📭 今日暂未发现符合关键词的新线索。")
    else:
        # 定义平台的图标
        source_icons = {
            'eleduck': '🦆',
            'proginn': '🏨',
            'yuanjisong': '🐒',
            'shixian': '🚀'
        }
        
        for i, lead in enumerate(qualified_leads, 1):
            icon = source_icons.get(lead['source'], '📌')
            lines.append(f"### {i}. {icon} {lead['title']}")
            lines.append(f"- **来源**：{lead['source']}")
            lines.append(f"- **简述**：{lead.get('description', '无描述')}")
            if lead.get('reply_draft'):
                # 保持换行
                clean_reply = lead['reply_draft'].replace('\n', '\n> ')
                lines.append(f"\n> **🤖 AI 推荐投标词**：\n> {clean_reply}")
            lines.append(f"\n- **行动**：[点击查看/投标]({lead['link']})")
            lines.append("")
            
    lines.append("\n---")
    lines.append("\n*本简报由天龙获客引擎自动生成。请尽快前往各平台进行深度沟通！*")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return report_file

def run_pipeline():
    log(">>> 启动全平台获客流水线 (V2.5) <<<")
    
    # 1. 初始化组件
    ele_monitor = EleDuckMonitor()
    prog_monitor = ProginnMonitor()
    shixian_monitor = ShixianMonitor()
    yuan_monitor = YuanjisongMonitor()
    crm = SimpleCRM()
    responder = AIResponder()
    
    all_qualified = []
    
    # 2. 运行监控任务
    log("正扫描各平台...")
    
    # 电鸭
    try:
        log("扫描电鸭社区...")
        new_ele = ele_monitor.run_once() or []
        for l in new_ele: l['source'] = 'eleduck'
        all_qualified.extend(new_ele)
        log(f"电鸭共发现 {len(new_ele)} 条新线索")
    except Exception as e: log(f"电鸭流水线异常: {e}")
        
    # 程序员客栈
    try:
        log("扫描程序员客栈...")
        new_prog = prog_monitor.run_once() or []
        # proginn_monitor 默认已加 source
        all_qualified.extend(new_prog)
        log(f"客栈共发现 {len(new_prog)} 条新线索")
    except Exception as e: log(f"客栈流水线异常: {e}")

    # 实现网
    try:
        log("扫描实现网...")
        new_shixian = shixian_monitor.run_once() or []
        all_qualified.extend(new_shixian)
        log(f"实现网共发现 {len(new_shixian)} 条新线索")
    except Exception as e: log(f"实现网流水线异常: {e}")

    # 猿急送
    try:
        log("扫描猿急送...")
        new_yuan = yuan_monitor.run_once() or []
        all_qualified.extend(new_yuan)
        log(f"猿急送共发现 {len(new_yuan)} 条新线索")
    except Exception as e: log(f"猿急送流水线异常: {e}")
        
    # 3. 生成回复草稿并同步 CRM
    if all_qualified:
        log("正处理新线索（AI 拟稿 + CRM 同步）...")
        for lead in all_qualified:
            # 生成草稿
            content_to_analyze = f"{lead['title']} {lead.get('description', '')}"
            lead['reply_draft'] = responder.generate_reply(content_to_analyze, template='standard')
            
            # 检查是否已在 CRM 中
            exists = any(p['title'] == lead['title'] for p in crm.projects)
            if not exists:
                client = crm.add_client(
                    name=f"潜在雇主({lead['source']})",
                    source=lead['source'],
                    contact="待跟进",
                    notes=f"自动化监控：{lead['title']}"
                )
                crm.add_project(
                    client_id=client.id,
                    title=lead['title'],
                    budget=lead.get('budget', 0),
                    description=lead.get('description', ''),
                    source_url=lead['link'],
                    status='lead',
                    notes=f"AI 草稿：\n{lead['reply_draft']}"
                )
    
    # 4. 生成简报
    report_path = generate_report(all_qualified)
    log(f"全平台获客简报已生成：{report_path}")
    
    # 5. 发送通知 (如有配置)
    feishu_url = config.FEISHU_WEBHOOK or os.environ.get("FEISHU_WEBHOOK")
    if feishu_url and all_qualified:
        notifier = FeishuNotifier(feishu_url)
        sources = ", ".join(set(l['source'] for l in all_qualified))
        notifier.send_lead_alert(len(all_qualified), sources)
        log("飞书获客提醒已推送。")

    sct_key = config.SCTKEY or os.environ.get("SCTKEY")
    if sct_key and all_qualified:
        sct_notifier = ServerChanNotifier(sct_key)
        sources = ", ".join(set(l['source'] for l in all_qualified))
        sct_notifier.send_lead_report(len(all_qualified), sources)
        log("微信 (Server酱) 获客提醒已推送。")

    log(">>> 流水线执行完毕 <<<")
    return report_path

if __name__ == "__main__":
    run_pipeline()
