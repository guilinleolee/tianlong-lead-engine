# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/b/outsource"
print(f"Testing: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # 获取所有包含具体项目信息的卡片
    # 查找有"查看主页"按钮的卡片（这是程序员展示卡片）
    # 或者查找有预算信息的卡片
    
    projects = page.evaluate('''() => {
        // 查找所有可能的项目卡片
        const results = [];
        
        // 方法 1: 查找包含预算的卡片
        const priceElements = document.querySelectorAll('[class*="price"], [class*="money"], .price');
        priceElements.forEach((el, i) => {
            if (i < 10) {
                const card = el.closest('.card, .item, .item-box, .project-item, div[class]');
                results.push({
                    type: 'price-card',
                    index: i,
                    text: (card ? card.innerText : el.innerText).substring(0, 150).replace(/\s+/g, ' '),
                    price: el.innerText
                });
            }
        });
        
        // 方法 2: 查找所有项目链接
        const projectLinks = document.querySelectorAll('a[href^="/b/p"]');
        projectLinks.forEach((link, i) => {
            if (i < 10) {
                results.push({
                    type: 'project-link',
                    index: i,
                    text: link.innerText.substring(0, 100).replace(/\s+/g, ' '),
                    href: link.href
                });
            }
        });
        
        return results;
    }''')
    
    print(f"Found {len(projects)} potential items:\n")
    for item in projects:
        print(f"[{item['type']}] {item['text'][:80]}")
        if 'price' in item:
            print(f"  Price: {item['price']}")
        if 'href' in item:
            print(f"  URL: {item['href']}")
        print()
    
    browser.close()
