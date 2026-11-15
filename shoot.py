import time
import os
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

# 从 GitHub 保险箱读取账号密码
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
        # 判断页面上有没有密码输入框
        if page.locator("input[type='password']").count() > 0:
            print("发现登录页面，正在自动输入账号密码...")
            # 找到输入框并填写。如果账号框自带内容，先清空
            page.locator("input").first.fill(USERNAME)
            page.get_by_placeholder("请输入密码").fill(PASSWORD)
            page.wait_for_timeout(1000)
            
            # 点击登录按钮（找文字为“登录”的按钮）
            page.get_by_text("登录", exact=True).first.click()
            print("已点击登录，等待系统加载...")
            page.wait_for_timeout(6000) # 等待登录成功后的页面加载
            
        print("第 1 步：点击顶部【末端平衡】")
        page.get_by_text("末端平衡").first.click(timeout=20000)
        page.wait_for_timeout(2500) 
        
        print("第 2 步：点击左侧【户端实时】")
        page.get_by_text("户端实时").first.click(timeout=20000)
        page.wait_for_timeout(1500) 
        
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
        # 如果出错，还是留一张现场图
        page.screenshot(path="debug.png", full_page=True)
    finally:
        browser.close()
