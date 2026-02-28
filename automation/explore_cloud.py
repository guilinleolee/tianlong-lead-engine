# -*- coding: utf-8 -*-
# 深入探索云端工作页面
from playwright.sync_api import sync_playwright
import time

url = "https://www.proginn.com/b/cloud"
print(f"Exploring: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # 向下滚动加载内容
    print("滚动页面...")
    for i in range(3):
        page.evaluate(f"window.scrollTo(0, { (i+1) * 500 })")
        time.sleep(1)
    
    # 截图
    page.screenshot(path="d:/工作日志/cloud_scrolled.png", full_page=True)
    print("已保存滚动截图")
    
    # 获取页面所有卡片
    cards = page.evaluate('''() => {
        const allCards = document.querySelectorAll('.card, .item, .position-item, .job-item, [class*="job"], [class*="position"]');
        return Array.from(allCards).slice(0, 20).map((card, i) => ({
            index: i,
            text: card.innerText.substring(0, 150).replace(/\s+/g, ' '),
            hasLink: !!card.querySelector('a'),
            href: card.querySelector('a')?.href || null
        }));
    }''')
    
    print(f"\n找到 {len(cards)} 个卡片:")
    for card in cards[:10]:
        print(f"  [{card['index']}] {card['text'][:80]}...")
        if card['href']:
            print(f"      -> {card['href']}")
    
    # 查找所有链接
    links = page.evaluate('''() => {
        const allLinks = Array.from(document.querySelectorAll('a[href]'));
        return allLinks.filter(a => {
            const href = a.href;
            const text = a.innerText;
            return href && (href.includes('/job/') || href.includes('/position/') || href.includes('/cloud/'));
        }).slice(0, 15).map(a => ({
            text: a.innerText.substring(0, 40),
            href: a.href
        }));
    }''')
    
    print(f"\n相关链接:")
    for link in links:
        print(f"  {link['text']} -> {link['href']}")
    
    # 保存完整 HTML 用于分析
    html = page.content()
    with open("d:/工作日志/cloud_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("\nHTML 已保存到：d:/工作日志/cloud_page.html")
    
    time.sleep(2)
    browser.close()
    print("\n完成！")
