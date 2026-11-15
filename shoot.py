import time
import os
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

USERNAME = os.environ.get("SITE_USER")
PASSWORD = os.environ.get("SITE_PASS")

with sync_playwright() as p:
    # 伪装成真实的 Windows 谷歌浏览器，防止被系统识别为机器人
    browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=90000)
    page.wait_for_timeout(6000) 

    try:
        print("检查是否需要登录...")
        if page.locator("input[type='password']").count() > 0:
            print("发现登录页面，正在模拟键盘输入...")
            
            # 精准定位账号框和密码框
            pwd_input = page.locator("input[type='password']").first
            user_input = page.locator("input[type='text']").first
            
            # 1. 输入账号（先全选删掉自带的，再模拟人类敲键盘，间隔0.1秒）
            user_input.click()
            user_input.press("Control+A")
            user_input.press("Backspace")
            user_input.press_sequentially(USERNAME, delay=100)
            page.wait_for_timeout(500)
            
            # 2. 输入密码
            pwd_input.click()
            pwd_input.press_sequentially(PASSWORD, delay=100)
            page.wait_for_timeout(1000)
            
            print("尝试点击登录按钮...")
            # 尝试寻找包含“登录”字样的元素并点击
            login_btn = page.locator("text='登录'").last
            if login_btn.is_visible():
                login_btn.click(force=True)
            else:
                # 如果找不到，直接在密码框按回车
                pwd_input.press("Enter")

            print("已提交登录，等待系统加载...")
            page.wait_for_timeout(10000) # 给足10秒时间让它加载
            
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
