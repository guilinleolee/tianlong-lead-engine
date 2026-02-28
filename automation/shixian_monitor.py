#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实现网项目监控脚本 (v1.0)
功能：抓取实现网最新项目并过滤关键词
作者：李秘 (AI Agent)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import hashlib
import config
from typing import List, Dict, Optional

# 路径设置
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SEEN_FILE = DATA_DIR / "shixian_seen.txt"

class ShixianMonitor:
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

    def fetch_projects(self) -> List[Dict]:
        url = "https://shixian.com/projects"
        try:
            self._log(f"正在抓取实现网: {url}")
            r = self.session.get(url, timeout=15)
            r.raise_for_status()
            r.encoding = 'utf-8' # 强制 utf-8
            soup = BeautifulSoup(r.text, 'html.parser')
            
            items = soup.select('li.media.project')
            projects = []
            
            for item in items:
                proj = self._parse_item(item)
                if proj:
                    projects.append(proj)
            return projects
        except Exception as e:
            self._log(f"抓取实现网失败: {e}")
            return []

    def _parse_item(self, item) -> Optional[Dict]:
        try:
            title_elem = item.select_one('h1.media-heading a')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if not link.startswith('http'):
                link = "https://shixian.com" + link
                
            project_id = hashlib.md5(link.encode()).hexdigest()[:12]
            
            # 描述
            desc_elem = item.select_one('.media-body')
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # 预算 (实现网通常在标题或描述中，或者有特殊的 label)
            budget = 0 # 默认 0
            
            return {
                'id': project_id,
                'title': title,
                'link': link,
                'description': description,
                'budget': budget,
                'source': 'shixian',
                'found_at': datetime.now().isoformat()
            }
        except:
            return None

    def filter_projects(self, projects: List[Dict]) -> List[Dict]:
        filtered = []
        for p in projects:
            if p['id'] in self.seen_ids:
                continue
            
            text = f"{p['title']} {p.get('description', '')}"
            if any(kw.lower() in text.lower() for kw in config.KEYWORDS):
                filtered.append(p)
                self.seen_ids.add(p['id'])
        return filtered

    def _log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [Shixian] {message}")

    def run_once(self):
        projs = self.fetch_projects()
        self._log(f"发现 {len(projs)} 条原始项目")
        new_projs = self.filter_projects(projs)
        if new_projs:
            self._save_seen_ids()
        self._log(f"筛选出 {len(new_projs)} 条新线索")
        return new_projs

if __name__ == "__main__":
    monitor = ShixianMonitor()
    monitor.run_once()
