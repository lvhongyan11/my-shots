import time
import os
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

USERNAME = os.environ.get("SITE_USER")
PASSWORD = os.environ.get("SITE_PASS")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=90000)
    page.wait_for_timeout(5000) 

    try:
        print("检查是否需要登录...")
        if page.locator("input[type='password']").count() > 0:
            print("发现登录页面，正在自动输入账号密码...")
            
            # 使用更精准的 input 索引来输入（第一个是账号，第二个是密码）
            inputs = page.locator("input")
            inputs.nth(0).fill(USERNAME)
            inputs.nth(1).fill(PASSWORD)
            page.wait_for_timeout(1500)
            
            print("尝试点击登录按钮...")
            # 方法1：尝试点击按钮
            try:
                page.locator("button:has-text('登录')").first.click(timeout=5000, force=True)
            except:
                print("点击按钮失败，尝试按回车键...")
                # 方法2：如果按钮点不动，直接在密码框按回车键（最管用）
                inputs.nth(1).press("Enter")

            print("已提交登录，等待系统加载...")
            page.wait_for_timeout(8000) # 给8秒时间让页面跳转加载
            
        print("第 1 步：点击顶部【末端平衡】")
        page.get_by_text("末端平衡").first.click(timeout=20000)
        page.wait_for_timeout(3000) 
        
        print("第 2 步：点击左侧【户端实时】")
        page.get_by_text("户端实时").first.click(timeout=20000)
        page.wait_for_timeout(2000) 
        
        print("第 3 步：点击子菜单【室温KPI】")
        page.get_by_text("室温KPI").first.click(timeout=20000)
        page.wait_for_timeout(6000) 
        
        print("第 4 步：寻找并点击【查询】按钮")
        page.get_by_text("查询").last.click(timeout=20000)
        page.wait_for_timeout(5000) 
        
        print("开始截取最终数据图...")
        page.screenshot(path="latest.png", full_page=True)
        print("✅ 截图成功！已保存为 latest.png")
        
    except Exception as e:
        print(f"❌ 操作失败，原因：{e}")
        page.screenshot(path="debug.png", full_page=True)
    finally:
        browser.close()
