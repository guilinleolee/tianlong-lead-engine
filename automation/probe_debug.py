# -*- coding: utf-8 -*-
# 调试脚本：查看实际抓取内容

from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/cat/"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    print("Page loaded!")
    
    # 截图看看
    page.screenshot(path="d:/工作日志/debug_snapshot.png")
    print("Screenshot saved to d:/工作日志/debug_snapshot.png")
    
    # 获取所有链接
    links = page.query_selector_all("a")
    print(f"\nTotal links found: {len(links)}")
    
    # 打印包含 project 的链接
    for i, link in enumerate(links[:50]):
        try:
            href = link.get_attribute("href") or ""
            text = link.inner_text().strip()[:50]
            if href and ('project' in href.lower() or '需求' in text):
                print(f"  [{i}] {text} -> {href}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")
    
    # 尝试找项目卡片
    items = page.query_selector_all(".item-box, .item, .project-card, .需求-item")
    print(f"\nItem boxes found: {len(items)}")
    
    for i, item in enumerate(items[:10]):
        try:
            text = item.inner_text().strip()[:100]
            print(f"  [{i}] {text}")
        except Exception as e:
            print(f"  [{i}] Error: {e}")
    
    browser.close()

print("\nDone!")
