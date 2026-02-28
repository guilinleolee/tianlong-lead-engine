#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 回复生成器
功能：根据项目需求自动生成个性化回复草稿
作者：李秘
生成时间：2026-02-27
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

# ==================== 配置区 ====================

# 个人资料配置
PROFILE = {
    'name': '李凌',
    'years': 15,  # 开发年限
    'position': '全栈开发者',
    'skills': {
        'frontend': ['Vue3', 'React', 'TypeScript', 'Uni-app', 'Nuxt.js'],
        'backend': ['Node.js', 'Python', 'FastAPI', 'Spring Boot'],
        'database': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis'],
        'tools': ['Git', 'Docker', 'AI 辅助开发']
    },
    'available_hours': 20,  # 每周可投入小时数
    'location': '中国（可远程）',
}

# 代表项目（用于附带案例）
PORTFOLIO = [
    {
        'name': '天龙引擎报告系统',
        'tech': 'Python + FastAPI + Vue3',
        'desc': '自动化报告生成平台，支持多模板、批量处理',
        'link': 'https://github.com/your-repo/tianlong_report_system',
        'tags': ['Python', 'Vue', '自动化']
    },
    {
        'name': 'AI 辅助开发工具集',
        'tech': 'Node.js + React + LLM',
        'desc': '集成 AI 能力的开发效率工具',
        'link': '',
        'tags': ['AI', 'React', 'Node.js']
    },
]

# 报价参考（元/小时）
RATE_CARD = {
    'small': 300,    # 简单任务
    'medium': 400,   # 中型项目
    'large': 500,    # 复杂项目
    'expert': 800,   # 专家级咨询
}

# 数据路径
DATA_DIR = Path(__file__).parent / "data"
TEMPLATES_DIR = Path(__file__).parent / "templates"
DATA_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# ==================== 回复模板 ====================

TEMPLATES = {
    'standard': '''
Hi，我是{name}，一名{years}年的{position}。

看到您的需求「{project_title}」，非常感兴趣！

【匹配度分析】
您的需求中提到{keywords}，这正是我的核心技能方向：
- 技术栈匹配：{matched_skills}
- 类似项目经验：{portfolio_count}个相关案例

【代表案例】
{portfolio_items}

【技术方案简述】
{tech_proposal}

【交付周期】
预计 {delivery_days} 个工作日

【报价参考】
{quote_range} 元
（可根据详细需求调整，支持分阶段付款）

【可投入时间】
每周{available_hours}小时 | {location} | 即时响应

期待进一步沟通！我的微信：[您的微信号]
---
附件：作品集链接、GitHub、类似案例 Demo
''',

    'quick': '''
您好！{years}年{position}，擅长{core_skills}。

您的需求「{project_title}」我做过类似案例：
→ {portfolio_link}

预估工时：{hours}小时
报价范围：{quote}元
交付周期：{days}天

可立即开始，微信详聊：[您的微信号]
''',

    'detailed': '''
尊敬的雇主，您好！

我是{name}，{position}，{years}年开发经验。

━━━━━━━━━━━━━━━━━━━
一、需求理解
━━━━━━━━━━━━━━━━━━━

根据您的描述，我理解您需要：
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}

━━━━━━━━━━━━━━━━━━━
二、技术方案
━━━━━━━━━━━━━━━━━━━

【技术选型】
- 前端：{frontend_stack}
- 后端：{backend_stack}
- 数据库：{database}
- 部署：{deployment}

【功能实现】
{feature_details}

【性能保障】
- 响应时间 < 200ms
- 支持并发 {concurrent_users}
- 代码测试覆盖率 > 80%

━━━━━━━━━━━━━━━━━━━
三、项目计划
━━━━━━━━━━━━━━━━━━━

| 阶段 | 内容 | 时间 | 交付物 |
|------|------|------|--------|
| 1 | 需求确认 + 原型 | 第 1 周 | 原型图、接口文档 |
| 2 | 核心功能开发 | 第 2-3 周 | 可运行版本 |
| 3 | 测试优化 | 第 4 周 | 测试报告 |
| 4 | 部署上线 | 第 5 周 | 生产环境 |

━━━━━━━━━━━━━━━━━━━
四、报价明细
━━━━━━━━━━━━━━━━━━━

{quote_breakdown}

合计：{total_quote}元
付款方式：50% 预付款 + 30% 中期 + 20% 验收

━━━━━━━━━━━━━━━━━━━
五、代表案例
━━━━━━━━━━━━━━━━━━━

{portfolio_items}

━━━━━━━━━━━━━━━━━━━
六、售后承诺
━━━━━━━━━━━━━━━━━━━

- 免费维护期：30 天
- Bug 修复：7×24 小时响应
- 功能迭代：优惠价格

期待合作！
{name}
微信：[您的微信号]
邮箱：[您的邮箱]
''',
}

# ==================== 核心类 ====================

class AIResponder:
    def __init__(self):
        self.profile = PROFILE
        self.portfolio = PORTFOLIO
        self.rate_card = RATE_CARD
    
    def analyze_project(self, project_text: str) -> Dict:
        """分析项目需求"""
        analysis = {
            'title': self._extract_title(project_text),
            'keywords': self._extract_keywords(project_text),
            'tech_stack': self._detect_tech(project_text),
            'complexity': self._estimate_complexity(project_text),
            'budget_mentioned': self._extract_budget(project_text),
            'requirements': self._extract_requirements(project_text),
        }
        return analysis
    
    def _extract_title(self, text: str) -> str:
        """提取项目标题"""
        lines = text.strip().split('\n')
        return lines[0][:50] if lines else "未命名项目"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单实现，可优化为 TF-IDF 或 AI 提取
        common_keywords = ['开发', '设计', '小程序', '网站', '系统', 'APP', '功能', '页面']
        found = [kw for kw in common_keywords if kw in text]
        return found[:5]
    
    def _detect_tech(self, text: str) -> List[str]:
        """检测技术栈"""
        tech_list = [
            'Vue', 'React', 'Angular', 'TypeScript', 'JavaScript',
            'Python', 'Java', 'Node.js', 'Go', 'PHP',
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'Docker', 'Kubernetes', 'AWS', '阿里云',
            '小程序', 'Uni-app', 'Flutter', 'React Native',
            'AI', 'LLM', '大模型', '机器学习'
        ]
        found = [tech for tech in tech_list if tech.lower() in text.lower()]
        return found
    
    def _estimate_complexity(self, text: str) -> str:
        """估算项目复杂度"""
        text_len = len(text)
        if text_len < 200:
            return 'small'
        elif text_len < 500:
            return 'medium'
        else:
            return 'large'
    
    def _extract_budget(self, text: str) -> Optional[int]:
        """提取预算"""
        patterns = [
            r'预算\s*[：:]\s*(\d+)',
            r'(\d+)[kK]-(\d+)[kK]',
            r'(\d+)[wW]-(\d+)[wW]', # Added w support
            r'(\d+)-(\d+)\s*元',
            r'(\d+)\s*元',
        ]
        text = text.replace('\xa0', ' ') # Fix non-breaking space
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    val1, val2 = int(groups[0]), int(groups[1])
                    if 'k' in pattern.lower():
                        return int((val1 + val2) * 1000 / 2)
                    if 'w' in pattern.lower():
                        return int((val1 + val2) * 10000 / 2)
                    return int((val1 + val2) / 2)
                return int(groups[0])
        return None
    
    def _extract_requirements(self, text: str) -> List[str]:
        """提取需求列表"""
        lines = text.strip().split('\n')
        requirements = []
        for line in lines[1:6]:  # 跳过标题，取前 5 行
            if line.strip() and len(line.strip()) > 5:
                requirements.append(line.strip()[:100])
        return requirements[:3]
    
    def _match_skills(self, tech_stack: List[str]) -> List[str]:
        """匹配技能"""
        matched = []
        all_skills = (
            self.profile['skills']['frontend'] +
            self.profile['skills']['backend'] +
            self.profile['skills']['database'] +
            self.profile['skills']['tools']
        )
        for tech in tech_stack:
            for skill in all_skills:
                if tech.lower() in skill.lower():
                    matched.append(skill)
        return list(set(matched))[:5]
    
    def _select_portfolio(self, tech_stack: List[str]) -> List[Dict]:
        """选择相关案例"""
        scored = []
        for item in self.portfolio:
            score = sum(1 for tag in item['tags'] if any(t.lower() in tag.lower() for t in tech_stack))
            scored.append((score, item))
        scored.sort(key=lambda x: x[0], reverse=True) # Fix: sort by score only
        return [item for _, item in scored[:2]]
    
    def _estimate_hours(self, complexity: str) -> int:
        """估算工时"""
        hours_map = {'small': 8, 'medium': 40, 'large': 120}
        return hours_map.get(complexity, 40)
    
    def _calculate_quote(self, complexity: str, budget_mentioned: Optional[int]) -> Dict:
        """计算报价"""
        hours = self._estimate_hours(complexity)
        rate = self.rate_card.get(complexity, 400)
        base_quote = hours * rate
        
        # 如果客户提到预算，适当调整
        if budget_mentioned:
            # 在客户预算基础上浮动±20%
            min_quote = int(budget_mentioned * 0.8)
            max_quote = int(budget_mentioned * 1.2)
        else:
            min_quote = int(base_quote * 0.8)
            max_quote = int(base_quote * 1.2)
        
        return {
            'hours': hours,
            'rate': rate,
            'min': min_quote,
            'max': max_quote,
            'suggested': int((min_quote + max_quote) / 2)
        }
    
    def generate_reply(self, project_text: str, template: str = 'standard') -> str:
        """生成回复草稿"""
        analysis = self.analyze_project(project_text)
        
        # 匹配技能
        matched_skills = self._match_skills(analysis['tech_stack'])
        
        # 选择案例
        portfolio_items = self._select_portfolio(analysis['tech_stack'])
        
        # 计算报价
        quote = self._calculate_quote(analysis['complexity'], analysis['budget_mentioned'])
        
        # 估算交付时间
        delivery_days = self._estimate_hours(analysis['complexity']) // 8
        
        # 填充模板
        if template == 'quick':
            reply = TEMPLATES['quick'].format(
                years=self.profile['years'],
                position=self.profile['position'],
                core_skills='、'.join(self.profile['skills']['frontend'][:3]),
                project_title=analysis['title'],
                portfolio_link=portfolio_items[0]['link'] if portfolio_items else '私信发送',
                hours=quote['hours'],
                quote=f"{quote['min']}-{quote['max']}",
                days=delivery_days
            )
        elif template == 'detailed':
            reply = self._generate_detailed(analysis, matched_skills, portfolio_items, quote)
        else:
            reply = self._generate_standard(analysis, matched_skills, portfolio_items, quote, delivery_days)
        
        return reply.strip()
    
    def _generate_standard(self, analysis, matched_skills, portfolio_items, quote, delivery_days) -> str:
        """生成标准回复"""
        portfolio_text = '\n'.join([
            f"- {p['name']} - {p['tech']}\n  {p['desc']}"
            for p in portfolio_items
        ]) or "多个相关案例，私信发送"
        
        tech_proposal = self._generate_tech_proposal(analysis['tech_stack'])
        
        return TEMPLATES['standard'].format(
            name=self.profile['name'],
            years=self.profile['years'],
            position=self.profile['position'],
            project_title=analysis['title'],
            keywords='、'.join(analysis['keywords']) or '相关技术需求',
            matched_skills='、'.join(matched_skills) or '全栈开发能力',
            portfolio_count=len(portfolio_items),
            portfolio_items=portfolio_text,
            tech_proposal=tech_proposal,
            delivery_days=delivery_days,
            quote_range=f"{quote['min']}-{quote['max']}",
            available_hours=self.profile['available_hours'],
            location=self.profile['location']
        )
    
    def _generate_detailed(self, analysis, matched_skills, portfolio_items, quote) -> str:
        """生成详细回复"""
        reqs = analysis['requirements']
        portfolio_text = '\n'.join([
            f"【{p['name']}】\n技术：{p['tech']}\n描述：{p['desc']}\n链接：{p['link'] or '私信'}\n"
            for p in portfolio_items
        ]) or "多个相关案例可供参考"
        
        quote_breakdown = f"""
- 需求分析与设计：{int(quote['hours'] * 0.1 * self.rate_card['medium'])}元
- 前端开发：{int(quote['hours'] * 0.4 * self.rate_card['medium'])}元
- 后端开发：{int(quote['hours'] * 0.4 * self.rate_card['medium'])}元
- 测试与部署：{int(quote['hours'] * 0.1 * self.rate_card['medium'])}元
"""
        
        return TEMPLATES['detailed'].format(
            name=self.profile['name'],
            years=self.profile['years'],
            position=self.profile['position'],
            requirement_1=reqs[0] if reqs else '核心功能开发',
            requirement_2=reqs[1] if len(reqs) > 1 else '界面设计与优化',
            requirement_3=reqs[2] if len(reqs) > 2 else '测试与部署',
            frontend_stack='、'.join(self.profile['skills']['frontend'][:3]),
            backend_stack='、'.join(self.profile['skills']['backend'][:3]),
            database='、'.join(self.profile['skills']['database'][:2]),
            deployment='Docker + 云服务器',
            feature_details='• 模块化设计，便于扩展\n• RESTful API 接口\n• 响应式布局',
            concurrent_users=1000,
            quote_breakdown=quote_breakdown,
            total_quote=quote['suggested'],
            portfolio_items=portfolio_text,
        )
    
    def _generate_tech_proposal(self, tech_stack: List[str]) -> str:
        """生成技术方案简述"""
        if not tech_stack:
            return "根据您的具体需求，我会采用最适合的技术栈进行开发。"
        
        tech_str = '、'.join(tech_stack[:4])
        return f"基于您的需求，我将采用 {tech_str} 等技术，确保项目高效、稳定交付。"
    
    def save_reply(self, reply: str, project_title: str):
        """保存回复草稿"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = re.sub(r'[^\w\u4e00-\u9fff]', '_', project_title)[:30]
        filename = f"reply_{timestamp}_{safe_title}.txt"
        filepath = DATA_DIR / "replies" / filename
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(reply)
        
        return filepath
    
    def save_to_cache(self, project_text: str, reply: str, analysis: Dict):
        """保存到缓存"""
        cache_file = DATA_DIR / "reply_cache.json"
        cache = []
        
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        
        cache.append({
            'timestamp': datetime.now().isoformat(),
            'project_text': project_text[:500],
            'analysis': analysis,
            'reply': reply
        })
        
        # 只保留最近 50 条
        cache = cache[-50:]
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)


# ==================== 命令行交互 ====================

def interactive_mode():
    """交互模式"""
    responder = AIResponder()
    
    print("=" * 60)
    print("AI 回复生成器 - 电鸭社区项目自动回复")
    print("=" * 60)
    print("\n模板选择:")
    print("1. 标准版 (推荐)")
    print("2. 快速版 (适合小项目)")
    print("3. 详细版 (适合大项目)")
    print("\n输入 'q' 退出\n")
    
    template_map = {'1': 'standard', '2': 'quick', '3': 'detailed'}
    
    while True:
        print("-" * 40)
        template_input = input("选择模板 [1/2/3，默认 1]: ").strip() or '1'
        template = template_map.get(template_input, 'standard')
        
        print("\n粘贴项目需求（粘贴后按 Ctrl+Z+Enter 结束）:")
        lines = []
        try:
            while True:
                line = input()
                if line == 'q':
                    return
                lines.append(line)
        except EOFError:
            pass
        
        project_text = '\n'.join(lines)
        if not project_text.strip():
            continue
        
        print("\n[INFO] 正在生成回复...\n")
        reply = responder.generate_reply(project_text, template)
        
        print("=" * 60)
        print("[RESULT] 生成的回复草稿:")
        print("=" * 60)
        print(reply)
        print("=" * 60)
        
        # 保存
        analysis = responder.analyze_project(project_text)
        responder.save_reply(reply, analysis['title'])
        responder.save_to_cache(project_text, reply, analysis)
        
        print(f"\n💾 已保存到：D:\\编程兼职\\automation\\data\\replies\\")
        print("\n继续生成下一个回复，或输入 'q' 退出\n")


# ==================== 入口 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 从文件读取项目需求
        input_file = sys.argv[1]
        template = sys.argv[2] if len(sys.argv) > 2 else 'standard'
        
        with open(input_file, 'r', encoding='utf-8') as f:
            project_text = f.read()
        
        responder = AIResponder()
        reply = responder.generate_reply(project_text, template)
        print(reply)
    else:
        # 交互模式
        interactive_mode()
