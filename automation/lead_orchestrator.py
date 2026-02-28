#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获客编排器 (Lead Orchestrator)
功能：统一运行多平台监控，自动同步 CRM，生成每日获客简报
作者：李秘 (AI Agent)
"""

import time
import os
from datetime import datetime
from pathlib import Path
from eleduck_monitor import EleDuckMonitor
from proginn_monitor import ProginnMonitor
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
        f"- **关键来源**：{', '.join(set(l['source'] for l in qualified_leads)) if qualified_leads else '无'}",
        "\n---",
        "\n## 📝 待开发线索列表"
    ]
    
    if not qualified_leads:
        lines.append("\n> 📭 今日暂未发现符合关键词的新线索。")
    else:
        for i, lead in enumerate(qualified_leads, 1):
            source_tag = "🦆" if lead['source'] == 'eleduck' else "🏨"
            lines.append(f"### {i}. {source_tag} {lead['title']}")
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
    log(">>> 启动全平台获客流水线 <<<")
    
    # 1. 初始化组件
    ele_monitor = EleDuckMonitor()
    prog_monitor = ProginnMonitor()
    crm = SimpleCRM()
    responder = AIResponder()
    
    all_qualified = []
    
    # 2. 运行电鸭监控
    try:
        log("正扫描电鸭社区...")
        ele_raw = ele_monitor.fetch_projects()
        ele_filtered = ele_monitor.filter_projects(ele_raw)
        for l in ele_filtered:
            l['source'] = 'eleduck'
        all_qualified.extend(ele_filtered)
        log(f"电鸭共发现 {len(ele_filtered)} 条新线索")
    except Exception as e:
        log(f"电鸭流水线异常: {e}")
        
    # 3. 运行程序员客栈监控
    try:
        log("正扫描程序员客栈...")
        prog_filtered = prog_monitor.run_once()
        for l in prog_filtered:
            l['source'] = 'proginn'
        all_qualified.extend(prog_filtered)
        log(f"客栈共发现 {len(prog_filtered)} 条新线索")
    except Exception as e:
        log(f"客栈流水线异常: {e}")
        
    # 4. 生成回复草稿并同步 CRM
    if all_qualified:
        log("正为新线索生成 AI 投标草稿并同步 CRM...")
        for lead in all_qualified:
            # 生成草稿
            content_to_analyze = f"{lead['title']} {lead.get('description', '')}"
            lead['reply_draft'] = responder.generate_reply(content_to_analyze, template='standard')
            
            # 检查是否已在 CRM 中
            exists = any(p['title'] == lead['title'] for p in crm.projects)
            if not exists:
                # 首先创建一个潜在客户 (占位)
                client = crm.add_client(
                    name=f"潜在雇主({lead['source']})",
                    source=lead['source'],
                    contact="待跟进",
                    notes=f"来自自动化监控：{lead['title']}"
                )
                # 添加项目
                crm.add_project(
                    client_id=client.id,
                    title=lead['title'],
                    budget=lead.get('budget', 0),
                    description=lead.get('description', ''),
                    source_url=lead['link'],
                    status='lead',
                    notes=f"AI 草稿：\n{lead['reply_draft']}"
                )
    
    # 5. 生成简报
    report_path = generate_report(all_qualified)
    log(f"全平台获客简报已生成：{report_path}")
    
    # 6. 发送飞书通知 (如有配置)
    feishu_url = config.FEISHU_WEBHOOK or os.environ.get("FEISHU_WEBHOOK")
    if feishu_url and all_qualified:
        notifier = FeishuNotifier(feishu_url)
        sources = ", ".join(set(l['source'] for l in all_qualified))
        notifier.send_lead_alert(len(all_qualified), sources)
        log("飞书获客提醒已推送。")

    # 7. 发送微信通知 (Server酱)
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
