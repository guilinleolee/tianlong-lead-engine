#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电鸭社区项目监控脚本
功能：定时扫描新项目，关键词匹配，推送通知
作者：李秘
生成时间：2026-02-27
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
import config

# ==================== 配置区 ====================

# 使用集中配置
KEYWORDS = config.KEYWORDS
MIN_BUDGET = config.MIN_BUDGET

# 检查间隔（秒）
CHECK_INTERVAL = 1800  # 30 分钟

# 推送方式配置
PUSH_CONFIG = {
    'wechat': bool(config.SCTKEY),
    'feishu': bool(config.FEISHU_WEBHOOK),
    'local_log': True,
}

# 数据保存路径
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
PROJECTS_FILE = DATA_DIR / "projects.json"
SEEN_FILE = DATA_DIR / "seen_projects.txt"

# ==================== 核心类 ====================

class EleDuckMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.seen_ids = self._load_seen_ids()
        self.projects_cache = self._load_cache()
    
    def _load_seen_ids(self) -> set:
        """加载已看过的项目 ID"""
        if SEEN_FILE.exists():
            with open(SEEN_FILE, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()
    
    def _save_seen_ids(self):
        """保存已看过的项目 ID"""
        with open(SEEN_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.seen_ids))
    
    def _load_cache(self) -> Dict:
        """加载项目缓存"""
        if PROJECTS_FILE.exists():
            with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'projects': []}
    
    def _save_cache(self):
        """保存项目缓存"""
        with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.projects_cache, f, ensure_ascii=False, indent=2)
    
    def fetch_projects(self) -> List[Dict]:
        """抓取项目列表"""
        url = "https://eleduck.com/search?query=%E5%BC%80%E5%8F%91"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            projects = []
            # 注意：以下选择器需要根据实际页面结构调整
            items = soup.select('.job-item, .project-item, li')
            
            for item in items:
                try:
                    project = self._parse_item(item)
                    if project:
                        projects.append(project)
                except Exception as e:
                    continue
            
            return projects
            
        except Exception as e:
            self._log(f"抓取失败：{e}")
            return []
    
    def _parse_item(self, item) -> Optional[Dict]:
        """解析单个项目"""
        try:
            # 提取标题
            title_elem = item.select_one('a.title, h3 a, .title')
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            link = title_elem.get('href', '')
            
            # 生成项目 ID（用链接哈希）
            project_id = hashlib.md5(link.encode()).hexdigest()[:12]
            
            # 提取预算
            budget_text = item.get_text()
            budget = self._extract_budget(budget_text)
            
            # 提取发布时间
            time_elem = item.select_one('.time, .date, span:last-child')
            publish_time = time_elem.get_text(strip=True) if time_elem else ""
            
            return {
                'id': project_id,
                'title': title,
                'link': f"https://eleduck.com{link}" if link.startswith('/') else link,
                'budget': budget,
                'publish_time': publish_time,
                'found_at': datetime.now().isoformat()
            }
        except Exception as e:
            return None
    
    def _extract_budget(self, text: str) -> int:
        """从文本中提取预算"""
        patterns = [
            r'(\d+)k-(\d+)k',  # 5k-10k
            r'(\d+)-(\d+) 元',
            r'预算 [：:]\s*(\d+)',
            r'(\d+)元',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    # 取平均值
                    if 'k' in pattern:
                        return int((int(groups[0]) + int(groups[1])) * 1000 / 2)
                    return int((int(groups[0]) + int(groups[1])) / 2)
                elif len(groups) == 1:
                    return int(groups[0])
        
        return 0
    
    def filter_projects(self, projects: List[Dict]) -> List[Dict]:
        """过滤项目"""
        filtered = []
        
        for project in projects:
            # 跳过已看过的
            if project['id'] in self.seen_ids:
                continue
            
            # 预算过滤
            if project['budget'] > 0 and project['budget'] < MIN_BUDGET:
                continue
            
            # 关键词匹配
            text = f"{project['title']} {project.get('description', '')}"
            if not any(kw.lower() in text.lower() for kw in KEYWORDS):
                continue
            
            filtered.append(project)
            self.seen_ids.add(project['id'])
        
        return filtered
    
    def send_notification(self, projects: List[Dict]):
        """发送通知 (保留本地日志，详细推送由 Orchestrator 处理)"""
        if not projects:
            return
        
        if PUSH_CONFIG['local_log']:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._log(f"发现 {len(projects)} 个新项目")
    
    def _log(self, message: str):
        """本地日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] [EleDuck] {message}"
        try:
            print(log_line)
            log_file = DATA_DIR / "monitor.log"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_line + '\n')
        except:
            pass
    
    def run_once(self):
        """执行一次监控"""
        self._log("开始扫描...")
        
        projects = self.fetch_projects()
        self._log(f"抓取到 {len(projects)} 个项目")
        
        new_projects = self.filter_projects(projects)
        self._log(f"筛选出 {len(new_projects)} 个新项目")
        
        if new_projects:
            self.send_notification(new_projects)
            self._save_seen_ids()
        
        # 更新缓存
        self.projects_cache['projects'] = projects
        self.projects_cache['last_update'] = datetime.now().isoformat()
        self._save_cache()
        return new_projects
    
    def run_continuous(self):
        """持续监控"""
        self._log(f"启动持续监控 (间隔{CHECK_INTERVAL}秒)")
        
        try:
            while True:
                self.run_once()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            self._log("监控已停止")
            self._save_seen_ids()


# ==================== 入口 ====================

if __name__ == "__main__":
    import sys
    
    # 强制 UTF-8 输出
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    monitor = EleDuckMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        monitor.run_once()
    else:
        monitor.run_continuous()
