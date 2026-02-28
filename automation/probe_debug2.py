# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

url = "https://www.proginn.com/cat/"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    print("Page loaded!")
    
    # 获取页面 HTML 前 2000 字符
    html = page.content()
    print(f"\nPage HTML length: {len(html)}")
    print("\nFirst 2000 chars of HTML:")
    print(html[:2000])
    
    browser.close()
