#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书机器人通知助手
功能：发送富文本/Markdown 消息至飞书群机器人
作者：李秘 (AI Agent)
"""

import requests
import json
from datetime import datetime

class FeishuNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_text(self, content: str):
        """发送纯文本消息"""
        if not self.webhook_url:
            return
        
        data = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        try:
            response = requests.post(self.webhook_url, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"飞书消息发送失败: {e}")
            return None

    def send_lead_alert(self, lead_count: int, sources: str, report_link: str = ""):
        """发送获客快报卡片"""
        if not self.webhook_url:
            return

        title = "🎯 天龙获客引擎 - 发现新线索"
        content = [
            [{"tag": "text", "text": f"📅 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"}],
            [{"tag": "text", "text": f"📈 线索概览: 发现 {lead_count} 条符合关键词的新项目\n"}],
            [{"tag": "text", "text": f"🌐 线索来源: {sources}\n"}],
            [{"tag": "text", "text": "\n立即前往 CRM 或报表查看详情并进行投标。"}]
        ]

        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            }
        }
        
        try:
            requests.post(self.webhook_url, json=data, timeout=10)
        except:
            pass
