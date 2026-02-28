import asyncio
from playwright.async_api import async_playwright
import time
import os

async def capture_page():
    async with async_playwright() as p:
        # 启动无头浏览器
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        url = "https://www.proginn.com/b/outsource" # 整包开发页面
        print(f"正在打开: {url}")
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            # 等待内容加载 (例如搜索框或项目列表)
            await asyncio.sleep(5) 
            
            # 截图保存以查看结构
            screenshot_path = "d:/编程兼职/automation/proginn_outsource.png"
            await page.screenshot(path=screenshot_path)
            print(f"截图已保存: {screenshot_path}")
            
            # 尝试搜索包含 "项目" 的链接
            # 程序员客栈的项目大厅通常需要登录后在 "发现项目" 菜单下
            # 我们先看看页面底部的 "更多案例" 或 "发布需求" 周围是否有线索
            
            # 提取所有链接
            links = await page.eval_on_selector_all("a", "elements => elements.map(el => ({text: el.innerText, href: el.href}))")
            for link in links:
                if "项目" in str(link['text']) or "整包" in str(link['text']):
                    print(f"发现可能路径: {link['text']} -> {link['href']}")
                    
        except Exception as e:
            print(f"Playwright 运行出错: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_page())
