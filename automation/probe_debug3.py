# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import json

url = "https://www.proginn.com/cat/"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    print("Page loaded!")
    
    # 执行 JS 获取所有项目卡片
    projects = page.evaluate('''() => {
        const items = [];
        // 尝试多种选择器
        const selectors = [
            '.item-box',
            '.project-item', 
            '.demand-item',
            '.cat-item',
            'a[href^="/b/p"]',
            '.list-item'
        ];
        
        for (const sel of selectors) {
            const els = document.querySelectorAll(sel);
            if (els.length > 0) {
                console.log(`Found ${els.length} elements with ${sel}`);
                els.forEach((el, i) => {
                    if (i < 5) {
                        items.push({
                            selector: sel,
                            index: i,
                            text: el.innerText.substring(0, 100),
                            href: el.href || el.querySelector('a')?.href || ''
                        });
                    }
                });
            }
        }
        return items;
    }''')
    
    print(f"\nFound {len(projects)} items:")
    for item in projects:
        print(f"  [{item['selector']}] #{item['index']}: {item['text'][:50]} -> {item['href'][:50] if item['href'] else 'N/A'}")
    
    # 截图
    page.screenshot(path="d:/工作日志/proginn_debug.png", full_page=True)
    print("\nScreenshot saved!")
    
    browser.close()
