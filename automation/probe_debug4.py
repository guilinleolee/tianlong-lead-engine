# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/cat/"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 有头模式看看发生了什么
    page = browser.new_page()
    
    page.goto(url, timeout=30000)
    print("Page loaded, waiting for content...")
    
    # 等待 5 秒让 JS 执行
    time.sleep(5)
    
    # 获取页面标题
    title = page.title()
    print(f"Page title: {title}")
    
    # 执行 JS 获取所有链接
    links = page.evaluate('''() => {
        const allLinks = Array.from(document.querySelectorAll('a[href^="/b/p"]'));
        return allLinks.slice(0, 20).map(a => ({
            text: a.innerText.substring(0, 80),
            href: a.href
        }));
    }''')
    
    print(f"\nFound {len(links)} project links:")
    for link in links:
        print(f"  {link['text']} -> {link['href']}")
    
    # 截图
    page.screenshot(path="d:/工作日志/proginn_visible.png")
    print("\nScreenshot saved!")
    
    time.sleep(2)
    browser.close()
