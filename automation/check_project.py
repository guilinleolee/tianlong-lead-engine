# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

# 直接访问项目页面
url = "https://www.proginn.com/b/p1980"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    title = page.title()
    print(f"Page title: {title}")
    
    # 获取页面主要内容
    content = page.evaluate('''() => {
        const main = document.querySelector('main, .main, #main, .content, .demand-detail');
        return main ? main.innerText.substring(0, 1000) : document.body.innerText.substring(0, 1000);
    }''')
    
    print(f"\nPage content preview:\n{content}")
    
    # 截图
    page.screenshot(path="d:/工作日志/project_page.png")
    print("\nScreenshot saved!")
    
    time.sleep(2)
    browser.close()
