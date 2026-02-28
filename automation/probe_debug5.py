# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

# 尝试不同的 URL
urls = [
    "https://www.proginn.com/requirement/",  # 需求页面
    "https://www.proginn.com/project/",      # 项目页面
    "https://www.proginn.com/cat/requirement/",  # 需求分类
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for url in urls:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print('='*60)
        
        page = browser.new_page()
        try:
            page.goto(url, timeout=15000)
            time.sleep(3)
            
            title = page.title()
            print(f"Title: {title}")
            
            # 查找项目/需求卡片
            items = page.evaluate('''() => {
                const selectors = ['.item-box', '.project-item', '.demand-item', '.requirement-item'];
                for (const sel of selectors) {
                    const els = document.querySelectorAll(sel);
                    if (els.length > 0) return els.length;
                }
                return 0;
            }''')
            
            print(f"Items found: {items}")
            
            # 获取一些链接
            links = page.evaluate('''() => {
                const allLinks = Array.from(document.querySelectorAll('a')).slice(0, 30);
                return allLinks.filter(a => {
                    const href = a.href;
                    return href && (href.includes('/project/') || href.includes('/requirement/') || href.includes('/p/'));
                }).map(a => ({
                    text: a.innerText.substring(0, 50),
                    href: a.href
                })).slice(0, 10);
            }''')
            
            if links:
                print("Sample links:")
                for link in links:
                    print(f"  {link['text']} -> {link['href']}")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            page.close()
    
    browser.close()
