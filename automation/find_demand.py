# -*- coding: utf-8 -*-
# 查找程序员客栈需求页面
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    # 启动有头浏览器（可以看到发生了什么）
    browser = p.chromium.launch(headless=False)
    
    # 创建新页面
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    
    # 访问首页
    print("访问首页...")
    page.goto("https://www.proginn.com/", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # 截图看看
    page.screenshot(path="d:/工作日志/homepage.png")
    print("首页截图已保存")
    
    # 查找所有导航链接
    print("\n查找导航链接...")
    nav_links = page.evaluate('''() => {
        const links = Array.from(document.querySelectorAll('a[href]'));
        const keywords = ['需求', '项目', '外包', '接单', '整包', '派单'];
        return links.filter(a => {
            const text = a.innerText;
            const href = a.href;
            return keywords.some(k => text.includes(k) || href.includes(k));
        }).map(a => ({
            text: a.innerText.trim(),
            href: a.href
        })).slice(0, 20);
    }''')
    
    print(f"找到 {len(nav_links)} 个相关链接:")
    for link in nav_links:
        print(f"  {link['text']} -> {link['href']}")
    
    # 尝试访问工作台
    print("\n访问工作台...")
    page.goto("https://www.proginn.com/user/work", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    page.screenshot(path="d:/工作日志/workbench.png")
    print("工作台截图已保存")
    
    # 查找接单相关按钮
    print("\n查找接单按钮...")
    buttons = page.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('a, button'));
        return btns.filter(b => {
            const text = b.innerText;
            return text && (text.includes('接单') || text.includes('项目') || text.includes('需求'));
        }).map(b => ({
            text: b.innerText.trim(),
            href: b.href || null,
            tag: b.tagName
        })).slice(0, 20);
    }''')
    
    print(f"找到 {len(buttons)} 个接单按钮:")
    for btn in buttons:
        print(f"  <{btn['tag']}> {btn['text']} -> {btn['href']}")
    
    time.sleep(2)
    browser.close()
    print("\n完成！")
