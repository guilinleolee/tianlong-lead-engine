#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Server酱 (ServerChan) 微信通知助手
功能：发送 1 对 1 微信通知
作者：李秘 (AI Agent)
"""

import requests
import json
from datetime import datetime

class ServerChanNotifier:
    def __init__(self, send_key: str):
        self.send_key = send_key

    def send_alert(self, title: str, content: str):
        """发送消息"""
        if not self.send_key:
            return
        
        url = f"https://sctapi.ftqq.com/{self.send_key}.send"
        data = {
            "title": title,
            "desp": content
        }
        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"微信通知发送失败: {e}")
            return None

    def send_lead_report(self, lead_count: int, sources: str):
        """发送获客总结"""
        title = f"🐉 天龙引擎：发现 {lead_count} 条新项目"
        content = f"""
### 获客流水线报告 ({datetime.now().strftime('%m-%d %H:%M')})

- **新线索总数**：{lead_count} 条
- **来源分布**：{sources}
- **详细信息**：已同步至 CRM 并生成每日 Markdown 简报。

> 💡 提示：请尽快检查并开始回复/投标。
        """
        return self.send_alert(title, content)
