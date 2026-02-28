#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
程序员客栈项目监控脚本 (v2.0)
功能：定时扫描新项目/线索，关键词匹配，推送通知
作者：李秘 (AI Agent 优化)
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from pathlib import Path
import re
from typing import List, Dict, Optional
import hashlib
import sys

# ==================== 配置区 ====================
# 继承 eleduck_monitor 的配置逻辑
KEYWORDS = [
    'Python', '后端', '爬虫', '数据', '自动化', 'FastAPI', 'Django', 'Flask',
    'AI', 'LLM', '大模型', 'Web3', 'Node.js'
]

MIN_BUDGET = 3000
CHECK_INTERVAL = 1800 

PUSH_CONFIG = {
    'wechat': False,
    'dingtalk': False,
    'local_log': True,
}

# 数据保护区
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SEEN_FILE = DATA_DIR / "proginn_seen.txt"

# 强制 UTF-8 输出
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ==================== 核心类 ====================

class ProginnMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        })
        self.seen_ids = self._load_seen_ids()
        
    def _load_seen_ids(self) -> set:
        if SEEN_FILE.exists():
            with open(SEEN_FILE, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    
    def _save_seen_ids(self):
        with open(SEEN_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.seen_ids))
            
    def fetch_leads(self) -> List[Dict]:
        """抓取线索。目前从搜索页获取项目/用户动态作为初步线索"""
        # 注意：程序员客栈项目大厅通常需要登录
        # 这里的 URL 可以扩展为包含 Cookie 的深层抓取
        urls = [
            "https://www.proginn.com/search?keyword=Python&type=user",
            "https://www.proginn.com/search?keyword=后端&type=user"
        ]
        
        all_leads = []
        for url in urls:
            try:
                self._log(f"请求搜索列表: {url}")
                r = self.session.get(url, timeout=15)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # 寻找线索项 (这里根据之前观察到的 J_user 结构)
                items = soup.select(".item.J_user")
                for item in items:
                    lead = self._parse_item(item)
                    if lead:
                        all_leads.append(lead)
            except Exception as e:
                self._log(f"抓取出错 ({url}): {e}")
        
        return all_leads

    def _parse_item(self, item) -> Optional[Dict]:
        try:
            title_elem = item.select_one(".title a")
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if not link.startswith("http"):
                link = "https://www.proginn.com" + link
                
            # ID 生成 (链接哈希)
            lead_id = hashlib.md5(link.encode()).hexdigest()[:12]
            
            # 简述/描述
            desc_elem = item.select_one(".item-desc, .desc")
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            return {
                'id': lead_id,
                'title': title,
                'link': link,
                'description': description,
                'source': 'proginn',
                'found_at': datetime.now().isoformat()
            }
        except:
            return None

    def filter_leads(self, leads: List[Dict]) -> List[Dict]:
        filtered = []
        for lead in leads:
            if lead['id'] in self.seen_ids:
                continue
            
            # 关键词匹配
            text = f"{lead['title']} {lead['description']}"
            if any(kw.lower() in text.lower() for kw in KEYWORDS):
                filtered.append(lead)
                self.seen_ids.add(lead['id'])
        return filtered

    def _log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] [Proginn] {message}"
        try:
            print(log_line)
            log_file = DATA_DIR / "monitor.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
        except:
            pass

    def run_once(self):
        self._log("开始 Proginn 扫描...")
        leads = self.fetch_leads()
        self._log(f"抓取到 {len(leads)} 条初始线索")
        
        new_leads = self.filter_leads(leads)
        self._log(f"筛选出 {len(new_leads)} 条符合关键词的项目/机会")
        
        if new_leads:
            self._save_seen_ids()
            return new_leads
        return []

if __name__ == "__main__":
    monitor = ProginnMonitor()
    monitor.run_once()
