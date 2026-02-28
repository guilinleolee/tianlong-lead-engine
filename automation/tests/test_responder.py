import pytest
from ai_responder import AIResponder

@pytest.fixture
def responder():
    return AIResponder()

def test_analyze_project(responder):
    project_text = "项目名：电商爬虫工程师招聘，需求：熟悉 Python、Scrapy、MySQL 开发电商数据采集，预算 1w-2w 元"
    analysis = responder.analyze_project(project_text)
    
    assert "Python" in analysis['tech_stack']
    assert "MySQL" in analysis['tech_stack']
    assert analysis['budget_mentioned'] == 15000 
    assert len(analysis['keywords']) > 0

def test_generate_reply(responder):
    project_text = "Python 开发，预算 10000"
    reply = responder.generate_reply(project_text, template='quick')
    
    assert "Python" in reply
    assert "15" in reply # 默认资料年限
    assert "元" in reply

def test_calculate_quote(responder):
    # 模拟复杂及预算提取
    quote = responder._calculate_quote('medium', 10000)
    assert quote['min'] < 10000
    assert quote['max'] > 10000
    assert quote['suggested'] == 10000
