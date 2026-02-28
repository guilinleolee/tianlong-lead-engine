# -*- coding: utf-8 -*-
# 查找真正的需求列表页面
from playwright.sync_api import sync_playwright
import time

# 可能的项目需求 URL
urls_to_try = [
    "https://www.proginn.com/demand/list",
    "https://www.proginn.com/requirement/list", 
    "https://www.proginn.com/project/list",
    "https://www.proginn.com/cat/demand",
    "https://www.proginn.com/cat/requirement",
    "https://www.kaifain.com/",  # 开发派
    "https://www.proginn.com/b/cloud",  # 云端工作
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    
    for url in urls_to_try:
        print(f"\n{'='*70}")
        print(f"Testing: {url}")
        print('='*70)
        
        page = browser.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=15000)
            time.sleep(2)
            
            title = page.title()
            print(f"Title: {title}")
            
            # 检查是否有项目/需求卡片
            items = page.evaluate('''() => {
                const selectors = [
                    '.demand-item', '.project-item', '.requirement-item',
                    '.card', '.item-box', '[class*="demand"]', '[class*="requirement"]'
                ];
                for (const sel of selectors) {
                    const els = document.querySelectorAll(sel);
                    if (els.length > 0) return {count: els.length, selector: sel};
                }
                return {count: 0, selector: null};
            }''')
            
            print(f"Items found: {items['count']} (selector: {items['selector']})")
            
            # 如果是 404 或错误页面，跳过
            if '404' in title or '未找到' in title:
                print("SKIP: 404 or not found")
                page.close()
                continue
            
            # 截图
            page.screenshot(path=f"d:/工作日志/test_{hash(url) % 10000}.png")
            
            # 获取一些链接样本
            links = page.evaluate('''() => {
                const allLinks = Array.from(document.querySelectorAll('a[href^="/demand/"], a[href^="/project/"], a[href^="/requirement/"]'));
                return allLinks.slice(0, 5).map(a => ({
                    text: a.innerText.substring(0, 50),
                    href: a.href
                }));
            }''')
            
            if links:
                print("Sample links:")
                for link in links:
                    print(f"  {link['text']} -> {link['href']}")
            
            # 如果找到项目，停留看看
            if items['count'] > 0:
                print(">>> FOUND! <<<")
                time.sleep(3)
            
            page.close()
            
        except Exception as e:
            print(f"Error: {e}")
            page.close()
    
    browser.close()
    print("\n=== Exploration Complete ===")
