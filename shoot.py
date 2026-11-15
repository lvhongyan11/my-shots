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
    page.wait_for_timeout(5000) # 给基础页面5秒钟加载时间
    
    try:
        print("第 1 步：点击顶部【末端平衡】")
        page.get_by_text("末端平衡", exact=True).first.click()
        page.wait_for_timeout(2000) # 等2秒让页面响应
        
        print("第 2 步：点击左侧【户端实时】")
        page.get_by_text("户端实时", exact=True).first.click()
        page.wait_for_timeout(1000) # 等1秒让子菜单展开
        
        print("第 3 步：点击子菜单【室温KPI】")
        page.get_by_text("室温KPI", exact=True).first.click()
        page.wait_for_timeout(5000) # 这个页面数据多，给它5秒钟加载图表和表格
        
        print("第 4 步：寻找并点击【查询】按钮")
        # 用 .last 是因为页面上可能有多个包含“查询”字样的元素，点最后一个通常最准
        page.get_by_text("查询", exact=True).last.click()
        page.wait_for_timeout(4000) # 点击查询后，等4秒让最新数据刷新
        
        print("开始截取最终数据图...")
        page.screenshot(path="latest.png", full_page=True)
        print("✅ 截图成功！已保存为 latest.png")
        
    except Exception as e:
        print(f"❌ 出错了！原因：{e}")
        print("正在保存诊断截图，看看卡在哪一步...")
        page.screenshot(path="debug.png", full_page=True)
        print("诊断截图已保存为 debug.png")
    finally:
        browser.close()
