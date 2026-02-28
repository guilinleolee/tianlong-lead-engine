# -*- coding: utf-8 -*-
# 测试项目对接页面
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/cat/xmjl"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(5)  # 等待动态加载
    
    # 截图
    page.screenshot(path="d:/工作日志/xmjl_page.png", full_page=True)
    print("截图已保存：d:/工作日志/xmjl_page.png")
    
    # 获取页面标题
    title = page.title()
    print(f"页面标题：{title}")
    
    # 查找项目卡片
    projects = page.evaluate('''() => {
        // 查找所有项目卡片
        const cards = document.querySelectorAll('.demand-item, .project-item, .item-box, .card, [class*="demand"], [class*="project"]');
        const results = [];
        
        cards.forEach((card, i) => {
            if (i < 15) {
                const text = card.innerText.substring(0, 150).replace(/\s+/g, ' ');
                const link = card.querySelector('a[href^="/demand/"], a[href^="/project/"]');
                results.push({
                    index: i,
                    text: text,
                    hasLink: !!link,
                    href: link ? link.href : null
                });
            }
        });
        
        return results;
    }''')
    
    print(f"\n找到 {len(projects)} 个项目卡片:")
    for proj in projects:
        print(f"  [{proj['index']}] {proj['text'][:60]}...")
        if proj['href']:
            print(f"      URL: {proj['href']}")
    
    time.sleep(3)
    browser.close()
    print("\n完成！")
