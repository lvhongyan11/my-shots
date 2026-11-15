import time
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="state.json", viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=90000)
    
    print("等待初始页面加载...")
    page.wait_for_timeout(6000) # 给主页足够的加载时间

    try:
        print("第 1 步：点击顶部【末端平衡】")
        # 等待“末端平衡”可见后再点击
        page.get_by_text("末端平衡", exact=True).first.wait_for(state="visible", timeout=15000)
        page.get_by_text("末端平衡", exact=True).first.click()
        page.wait_for_timeout(3000) # 点击后等待页面响应
        
        print("第 2 步：点击左侧【户端实时】")
        page.get_by_text("户端实时", exact=True).first.wait_for(state="visible", timeout=15000)
        page.get_by_text("户端实时", exact=True).first.click()
        page.wait_for_timeout(2000) # 等子菜单展开
        
        print("第 3 步：点击子菜单【室温KPI】")
        page.get_by_text("室温KPI", exact=True).first.wait_for(state="visible", timeout=15000)
        page.get_by_text("室温KPI", exact=True).first.click()
        page.wait_for_timeout(6000) # 这个页面数据较多，等待加载图表和表格
        
        print("第 4 步：寻找并点击【查询】按钮")
        page.get_by_text("查询", exact=True).last.wait_for(state="visible", timeout=15000)
        page.get_by_text("查询", exact=True).last.click()
        page.wait_for_timeout(5000) # 等待最新数据刷新
        
        print("开始截取最终数据图...")
        page.screenshot(path="latest.png", full_page=True)
        print("✅ 截图成功！已保存为 latest.png")
        
    except Exception as e:
        print(f"❌ 操作失败，原因：{e}")
        print("正在保存诊断截图...")
        page.screenshot(path="debug.png", full_page=True)
        print("诊断截图已保存为 debug.png")
    finally:
        browser.close()
