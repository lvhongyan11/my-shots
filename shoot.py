import time
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="state.json", viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=90000)
    page.wait_for_timeout(8000) # 给足8秒加载时间

    # 【关键】不管三七二十一，先在仓库里存一张图，看看它到底看到了什么
    page.screenshot(path="debug.png", full_page=True)
    print("已保存初始页面截图 debug.png")

    try:
        print("第 1 步：点击顶部【末端平衡】")
        # 去掉了 exact=True，容错率更高，也不容易超时
        page.get_by_text("末端平衡").first.click(timeout=20000)
        page.wait_for_timeout(2000) 
        
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
    finally:
        browser.close()
