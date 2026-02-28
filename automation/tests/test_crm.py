import pytest
import os
import shutil
from pathlib import Path
import json
from crm_manager import SimpleCRM

# 使用临时测试目录
TEST_DATA_DIR = Path("d:/编程兼职/automation/tests/test_crm_data")

@pytest.fixture
def crm():
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)
    TEST_DATA_DIR.mkdir(parents=True)
    crm_instance = SimpleCRM(data_dir=TEST_DATA_DIR)
    yield crm_instance
    # 清理
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

def test_add_client(crm):
    name = "测试客户"
    source = "电鸭"
    contact = "wx_test"
    client = crm.add_client(name, source, contact)
    
    assert client.name == name
    assert client.source == source
    assert len(crm.clients) == 1
    assert crm.clients[0]['name'] == name

def test_add_project(crm):
    client = crm.add_client("甲方", "客栈", "contact")
    project = crm.add_project(client.id, "Python项目", 5000)
    
    assert project.title == "Python项目"
    assert project.budget == 5000
    assert len(crm.projects) == 1
    assert crm.projects[0]['client_id'] == client.id

def test_update_status(crm):
    client = crm.add_client("甲方", "客栈", "contact")
    crm.update_client_status(client.id, "active")
    assert crm.clients[0]['status'] == "active"

def test_stats(crm):
    c1 = crm.add_client("C1", "S1", "C1")
    crm.add_project(c1.id, "P1", 1000, status="completed", payment_amount=1000)
    
    stats = crm.get_stats()
    assert stats['total_clients'] == 1
    assert stats['total_revenue'] == 1000
