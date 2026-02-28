#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易 CRM 客户管理系统
功能：客户跟进、项目追踪、自动提醒
作者：李秘
生成时间：2026-02-27
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import csv

# ==================== 数据模型 ====================

@dataclass
class Client:
    """客户信息"""
    id: str
    name: str
    source: str  # 电鸭/程序员客栈/推荐/其他
    contact: str  # 微信/邮箱/电话
    company: str = ""
    position: str = ""
    budget_range: str = ""  # 5k-10k / 10k-30k / 30k+
    status: str = "potential"  # potential/contacting/negotiating/active/completed/lost
    tags: List[str] = None
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""
    last_contact: str = ""
    next_followup: str = ""

@dataclass
class Project:
    """项目信息"""
    id: str
    client_id: str
    title: str
    description: str
    budget: float
    status: str = "lead"  # lead/quoted/negotiating/active/completed/cancelled
    priority: str = "normal"  # low/normal/high/urgent
    source_url: str = ""
    quoted_at: str = ""
    started_at: str = ""
    deadline: str = ""
    completed_at: str = ""
    payment_status: str = "unpaid"  # unpaid/partial/paid
    payment_amount: float = 0
    notes: str = ""

@dataclass
class FollowUp:
    """跟进记录"""
    id: str
    client_id: str
    date: str
    summary: str
    project_id: str = ""
    type: str = "call"  # call/message/meeting/email
    next_action: str = ""
    next_date: str = ""

# ==================== CRM 管理类 ====================

class SimpleCRM:
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path(__file__).parent / "crm_data"
        self.data_dir.mkdir(exist_ok=True)
        
        # 数据文件路径
        self.clients_file = self.data_dir / "clients.json"
        self.projects_file = self.data_dir / "projects.json"
        self.followups_file = self.data_dir / "followups.json"
        
        # 加载数据
        self.clients = self._load_data(self.clients_file)
        self.projects = self._load_data(self.projects_file)
        self.followups = self._load_data(self.followups_file)
    
    def _load_data(self, filepath: Path) -> List[Dict]:
        """加载 JSON 数据"""
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_data(self, filepath: Path, data: List[Dict]):
        """保存 JSON 数据"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self, prefix: str) -> str:
        """生成 ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        import random
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"{prefix}_{timestamp}_{suffix}"
    
    # ==================== 客户管理 ====================
    
    def add_client(self, name: str, source: str, contact: str, **kwargs) -> Client:
        """添加客户"""
        client = Client(
            id=self._generate_id('C'),
            name=name,
            source=source,
            contact=contact,
            tags=kwargs.get('tags', []),
            notes=kwargs.get('notes', ''),
            budget_range=kwargs.get('budget_range', ''),
            company=kwargs.get('company', ''),
            position=kwargs.get('position', ''),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        
        self.clients.append(asdict(client))
        self._save_data(self.clients_file, self.clients)
        
        print(f"[OK] 客户已添加：{name} (ID: {client.id})")
        return client
    
    def update_client_status(self, client_id: str, status: str):
        """更新客户状态"""
        for client in self.clients:
            if client['id'] == client_id:
                client['status'] = status
                client['updated_at'] = datetime.now().isoformat()
                self._save_data(self.clients_file, self.clients)
                print(f"[OK] 客户状态已更新：{client['name']} -> {status}")
                return
        print(f"❌ 客户未找到：{client_id}")
    
    def set_followup_reminder(self, client_id: str, date: str):
        """设置跟进提醒"""
        for client in self.clients:
            if client['id'] == client_id:
                client['next_followup'] = date
                client['updated_at'] = datetime.now().isoformat()
                self._save_data(self.clients_file, self.clients)
                print(f"[OK] 跟进提醒已设置：{date}")
                return
    
    def get_clients_by_status(self, status: str) -> List[Dict]:
        """按状态获取客户"""
        return [c for c in self.clients if c['status'] == status]
    
    def get_followup_due(self, days: int = 3) -> List[Dict]:
        """获取待跟进客户"""
        due_date = datetime.now() + timedelta(days=days)
        due_list = []
        
        for client in self.clients:
            if client.get('next_followup'):
                try:
                    followup_date = datetime.fromisoformat(client['next_followup'])
                    if followup_date <= due_date:
                        due_list.append(client)
                except:
                    pass
        
        return due_list
    
    # ==================== 项目管理 ====================
    
    def add_project(self, client_id: str, title: str, budget: float, **kwargs) -> Project:
        """添加项目"""
        project = Project(
            id=self._generate_id('P'),
            client_id=client_id,
            title=title,
            budget=budget,
            description=kwargs.get('description', ''),
            status=kwargs.get('status', 'lead'),
            priority=kwargs.get('priority', 'normal'),
            source_url=kwargs.get('source_url', ''),
            notes=kwargs.get('notes', ''),
            payment_amount=kwargs.get('payment_amount', 0), # Added
            payment_status=kwargs.get('payment_status', 'unpaid'), # Added
        )
        
        self.projects.append(asdict(project))
        self._save_data(self.projects_file, self.projects)
        
        print(f"[OK] 项目已添加：{title} (ID: {project.id})")
        return project
    
    def update_project_status(self, project_id: str, status: str):
        """更新项目状态"""
        for project in self.projects:
            if project['id'] == project_id:
                project['status'] = status
                if status == 'active' and not project.get('started_at'):
                    project['started_at'] = datetime.now().isoformat()
                elif status == 'completed':
                    project['completed_at'] = datetime.now().isoformat()
                self._save_data(self.projects_file, self.projects)
                print(f"[OK] 项目状态已更新：{project['title']} -> {status}")
                return
    
    def get_projects_by_status(self, status: str) -> List[Dict]:
        """按状态获取项目"""
        return [p for p in self.projects if p['status'] == status]
    
    def get_active_projects(self) -> List[Dict]:
        """获取活跃项目"""
        return self.get_projects_by_status('active')
    
    # ==================== 跟进记录 ====================
    
    def add_followup(self, client_id: str, summary: str, **kwargs) -> FollowUp:
        """添加跟进记录"""
        followup = FollowUp(
            id=self._generate_id('F'),
            client_id=client_id,
            project_id=kwargs.get('project_id', ''),
            date=datetime.now().isoformat(),
            type=kwargs.get('type', 'call'),
            summary=summary,
            next_action=kwargs.get('next_action', ''),
            next_date=kwargs.get('next_date', ''),
        )
        
        self.followups.append(asdict(followup))
        self._save_data(self.followups_file, self.followups)
        
        # 更新客户最后联系时间
        for client in self.clients:
            if client['id'] == client_id:
                client['last_contact'] = datetime.now().isoformat()
                if followup.next_date:
                    client['next_followup'] = followup.next_date
                client['updated_at'] = datetime.now().isoformat()
                self._save_data(self.clients_file, self.clients)
                break
        
        print(f"[OK] 跟进记录已添加")
        return followup
    
    def get_client_history(self, client_id: str) -> List[Dict]:
        """获取客户历史"""
        return [f for f in self.followups if f['client_id'] == client_id]
    
    # ==================== 统计报表 ====================
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        stats = {
            'total_clients': len(self.clients),
            'clients_by_status': {},
            'total_projects': len(self.projects),
            'projects_by_status': {},
            'total_revenue': 0,
            'pending_revenue': 0,
        }
        
        # 客户统计
        for client in self.clients:
            status = client['status']
            stats['clients_by_status'][status] = stats['clients_by_status'].get(status, 0) + 1
        
        # 项目统计
        for project in self.projects:
            status = project['status']
            stats['projects_by_status'][status] = stats['projects_by_status'].get(status, 0) + 1
            
            if project['status'] == 'completed':
                stats['total_revenue'] += project.get('payment_amount', 0)
            elif project['status'] in ['active', 'negotiating']:
                stats['pending_revenue'] += project.get('budget', 0)
        
        return stats
    
    def print_dashboard(self):
        """打印仪表盘"""
        stats = self.get_stats()
        due_followups = self.get_followup_due(3)
        
        print("\n" + "=" * 60)
        print("[CRM] 仪表盘")
        print("=" * 60)
        
        print(f"\n[CLIENTS] 客户概览")
        print(f"   总客户数：{stats['total_clients']}")
        for status, count in stats['clients_by_status'].items():
            print(f"   • {status}: {count}")
        
        print(f"\n[PROJECTS] 项目概览")
        print(f"   总项目数：{stats['total_projects']}")
        for status, count in stats['projects_by_status'].items():
            print(f"   - {status}: {count}")
        
        print(f"\n[REVENUE] 收入统计")
        print(f"   已完成：{stats['total_revenue']:,}元")
        print(f"   进行中：{stats['pending_revenue']:,}元")
        
        if due_followups:
            print(f"\n[FOLLOWUP] 待跟进客户 ({len(due_followups)}个)")
            for client in due_followups[:5]:
                print(f"   - {client['name']} - {client.get('next_followup', '未设置')}")
        
        print("\n" + "=" * 60)
    
    # ==================== 数据导出 ====================
    
    def export_to_csv(self, output_dir: Path = None):
        """导出为 CSV"""
        output_dir = output_dir or self.data_dir
        output_dir.mkdir(exist_ok=True)
        
        # 导出客户
        clients_csv = output_dir / "clients.csv"
        if self.clients:
            with open(clients_csv, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.clients[0].keys())
                writer.writeheader()
                writer.writerows(self.clients)
            print(f"[OK] 客户已导出：{clients_csv}")
        
        # 导出项目
        projects_csv = output_dir / "projects.csv"
        if self.projects:
            with open(projects_csv, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.projects[0].keys())
                writer.writeheader()
                writer.writerows(self.projects)
            print(f"[OK] 项目已导出：{projects_csv}")
        
        # 导出跟进记录
        followups_csv = output_dir / "followups.csv"
        if self.followups:
            with open(followups_csv, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.followups[0].keys())
                writer.writeheader()
                writer.writerows(self.followups)
            print(f"[OK] 跟进记录已导出：{followups_csv}")


# ==================== 命令行交互 ====================

def interactive_mode():
    """交互模式"""
    crm = SimpleCRM()
    
    print("=" * 60)
    print("简易 CRM 客户管理系统")
    print("=" * 60)
    
    while True:
        print("\n主菜单:")
        print("1. 查看仪表盘")
        print("2. 添加客户")
        print("3. 添加项目")
        print("4. 添加跟进记录")
        print("5. 查看待跟进")
        print("6. 更新客户状态")
        print("7. 更新项目状态")
        print("8. 导出数据")
        print("9. 客户列表")
        print("0. 退出")
        
        choice = input("\n选择 [0-9]: ").strip()
        
        if choice == '1':
            crm.print_dashboard()
        
        elif choice == '2':
            name = input("客户名称：").strip()
            source = input("来源 [电鸭/推荐/其他]: ").strip() or "电鸭"
            contact = input("联系方式 [微信/邮箱]: ").strip()
            crm.add_client(name, source, contact)
        
        elif choice == '3':
            client_id = input("客户 ID: ").strip()
            title = input("项目名称：").strip()
            budget = float(input("预算 [元]: ").strip() or 0)
            crm.add_project(client_id, title, budget)
        
        elif choice == '4':
            client_id = input("客户 ID: ").strip()
            summary = input("跟进摘要：").strip()
            next_date = input("下次跟进日期 [YYYY-MM-DD]: ").strip()
            crm.add_followup(client_id, summary, next_date=next_date)
        
        elif choice == '5':
            due = crm.get_followup_due()
            if due:
                print(f"\n待跟进客户 ({len(due)}个):")
                for c in due:
                    print(f"  • {c['name']} - {c.get('next_followup', '未设置')}")
            else:
                print("\n✅ 暂无待跟进客户")
        
        elif choice == '6':
            client_id = input("客户 ID: ").strip()
            print("状态选项：potential/contacting/negotiating/active/completed/lost")
            status = input("新状态：").strip()
            crm.update_client_status(client_id, status)
        
        elif choice == '7':
            project_id = input("项目 ID: ").strip()
            print("状态选项：lead/quoted/negotiating/active/completed/cancelled")
            status = input("新状态：").strip()
            crm.update_project_status(project_id, status)
        
        elif choice == '8':
            crm.export_to_csv()
        
        elif choice == '9':
            print("\n客户列表:")
            for c in crm.clients[-10:]:  # 最近 10 个
                print(f"  {c['id']}: {c['name']} ({c['status']}) - {c['contact']}")
        
        elif choice == '0':
            print("\n👋 再见!")
            break
        
        else:
            print("无效选择，请重试")


# ==================== 入口 ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        interactive_mode()
    else:
        # 默认显示仪表盘
        crm = SimpleCRM()
        crm.print_dashboard()
