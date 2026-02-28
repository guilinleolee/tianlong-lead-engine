# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/cat/"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    print("Page loaded")
    
    # 等待并观察
    time.sleep(3)
    
    # 检查是否有"发布需求"或"找项目"的按钮/链接
    tabs = page.evaluate('''() => {
        const tabs = Array.from(document.querySelectorAll('.tab-item, .tab, .filter-item, a')).map(el => ({
            text: el.innerText.substring(0, 30),
            href: el.href,
            class: el.className
        }));
        return tabs.filter(t => t.text && (t.text.includes('需求') || t.text.includes('项目') || t.text.includes('外包')));
    }''')
    
    print(f"\nRelevant tabs/links: {len(tabs)}")
    for tab in tabs[:20]:
        print(f"  {tab['text']} -> {tab['href']}")
    
    # 截图
    page.screenshot(path="d:/工作日志/cat_tabs.png")
    print("\nScreenshot saved!")
    
    time.sleep(2)
    browser.close()
