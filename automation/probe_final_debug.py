# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/b/outsource"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    print("Page loaded")
    time.sleep(3)
    
    # 获取页面标题
    title = page.title()
    print(f"Page title: {title}")
    
    # 获取所有链接并分类
    all_links = page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a[href]')).slice(0, 100);
        const categorized = {
            'b/p': [],
            'w/': [],
            'cat/': [],
            'type/': [],
            'other': []
        };
        
        links.forEach(a => {
            const href = a.href;
            const text = a.innerText.substring(0, 50).replace(/\s+/g, ' ');
            if (href.includes('/b/p')) categorized['b/p'].push({text, href});
            else if (href.includes('/w/')) categorized['w/'].push({text, href});
            else if (href.includes('/cat/')) categorized['cat/'].push({text, href});
            else if (href.includes('/type/')) categorized['type/'].push({text, href});
            else if (href.startsWith('https://www.proginn.com/') && !href.includes('login') && !href.includes('register')) {
                categorized['other'].push({text, href});
            }
        });
        
        return categorized;
    }''')
    
    for category, links in all_links.items():
        if links:
            print(f"\n{category} ({len(links)} links):")
            for link in links[:5]:
                print(f"  {link['text']} -> {link['href']}")
    
    # 截图
    page.screenshot(path="d:/工作日志/outsource_page.png", full_page=True)
    print("\nScreenshot saved!")
    
    time.sleep(2)
    browser.close()
