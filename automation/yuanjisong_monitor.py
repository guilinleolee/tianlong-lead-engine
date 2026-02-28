#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
猿急送项目监控脚本 (v1.1)
功能：抓取猿急送最新项目并过滤关键词
作者：李秘 (AI Agent)
"""

import requests
from bs4 import BeautifulSoup
import time
import hashlib
from pathlib import Path
import config
from datetime import datetime
import re
from typing import List, Dict, Optional

# 数据路径
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SEEN_FILE = DATA_DIR / "yuanjisong_seen.txt"

class YuanjisongMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
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

    def fetch_jobs(self) -> List[Dict]:
        """抓取猿急送项目列表"""
        # 尝试多个可能的 URL
        urls = [
            "https://www.yuanjisong.com/job",
            "https://www.yuanjisong.com/job/all-all-all-all-all-1",
            "https://www.yuanjisong.com/index.php?m=Job&a=index"
        ]
        
        all_jobs = []
        for url in urls:
            try:
                self._log(f"正在尝试抓取: {url}")
                # 建立 Session
                self.session.get("https://www.yuanjisong.com/", timeout=10)
                
                r = self.session.get(url, timeout=15)
                if r.status_code != 200:
                    self._log(f"请求失败 ({r.status_code})")
                    continue
                
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # 寻找列表容器
                # 猿急送的结构常为 .job-list-item or .job-item or .item
                items = soup.select('.job-list-item, .job-item, .item, div.row.course-card')
                
                for item in items:
                    job = self._parse_item(item)
                    if job and job not in all_jobs:
                        all_jobs.append(job)
                
                if all_jobs:
                    break # 抓到就停
            except Exception as e:
                self._log(f"抓取异常: {e}")
        
        return all_jobs

    def _parse_item(self, item) -> Optional[Dict]:
        try:
            # 标题与链接
            title_elem = item.select_one('.job-list-item-title a, .title a, h3 a, a[href*="/job/"]')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            if not link.startswith('http'):
                link = "https://www.yuanjisong.com" + link
                
            job_id = hashlib.md5(link.encode()).hexdigest()[:12]
            
            # 描述 (描述往往在 item 的内部，不一定有专门的类)
            description = item.get_text(separator=' ', strip=True)
            
            # 简化一下，如果描述太长截断
            if len(description) > 300:
                description = description[:300] + "..."
            
            return {
                'id': job_id,
                'title': title,
                'link': link,
                'description': description,
                'budget': 0,
                'source': 'yuanjisong',
                'found_at': datetime.now().isoformat()
            }
        except:
            return None

    def filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        filtered = []
        for j in jobs:
            if j['id'] in self.seen_ids:
                continue
            
            text = f"{j['title']} {j.get('description', '')}"
            if any(kw.lower() in text.lower() for kw in config.KEYWORDS):
                filtered.append(j)
                self.seen_ids.add(j['id'])
        return filtered

    def _log(self, message: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] [Yuanjisong] {message}")

    def run_once(self):
        jobs = self.fetch_jobs()
        self._log(f"共抓取到 {len(jobs)} 条原始项目")
        new_jobs = self.filter_jobs(jobs)
        if new_jobs:
            self._save_seen_ids()
        self._log(f"筛选出 {len(new_jobs)} 条新线索")
        return new_jobs

if __name__ == "__main__":
    monitor = YuanjisongMonitor()
    monitor.run_once()
