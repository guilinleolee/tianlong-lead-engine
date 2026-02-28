import pytest
from unittest.mock import MagicMock, patch
from eleduck_monitor import EleDuckMonitor
from proginn_monitor import ProginnMonitor

@pytest.fixture
def mock_eleduck_html():
    return """
    <div class="job-item">
        <a class="title" href="/j/12345">【招聘】Python后端开发工程师</a>
        <div class="desc">需求：熟悉 Django，预算 10k-15k</div>
    </div>
    """

@pytest.fixture
def mock_proginn_html():
    return """
    <div class="item J_user">
        <div class="title"><a href="/u/67890">南京优软科技有限公司 Python全栈工程师</a></div>
        <div class="item-desc">多年爬虫经验，精通自动化工具。</div>
    </div>
    """

def test_eleduck_parsing(mock_eleduck_html):
    monitor = EleDuckMonitor()
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.text = mock_eleduck_html
        mock_get.return_value.status_code = 200
        
        projects = monitor.fetch_projects()
        assert len(projects) > 0
        assert "Python" in projects[0]['title']
        assert projects[0]['budget'] == 12500 # (10+15)/2 * 1000

def test_proginn_parsing(mock_proginn_html):
    monitor = ProginnMonitor()
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.text = mock_proginn_html
        mock_get.return_value.status_code = 200
        
        # 强制用 fetch_leads 进行单测
        leads = monitor.fetch_leads()
        assert len(leads) > 0
        assert "南京优软" in leads[0]['title']

def test_filter_keywords():
    monitor = ProginnMonitor()
    # 模拟数据
    leads = [
        {'id': '1', 'title': 'Python 开发', 'description': '后端开发'},
        {'id': '2', 'title': 'UI 设计', 'description': '画图设计'},
    ]
    # 已看的去重逻辑在 monitor.seen_ids 中，初始化为空
    filtered = monitor.filter_leads(leads)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'Python 开发'
