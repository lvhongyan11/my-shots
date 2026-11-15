import time
from playwright.sync_api import sync_playwright

# 你的目标网址
URL = "http://111.42.63.196:50000/smart-web/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    # 加载你存放在 GitHub Secrets 里的登录状态
    context = browser.new_context(storage_state="state.json", viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=60000)
    
    # 等待页面加载完毕，寻找“查询”按钮
    print("等待查询按钮出现...")
    page.wait_for_selector("text=查询", timeout=30000)
    
    # 点击“查询”按钮
    print("点击查询...")
    page.get_by_text("查询", exact=True).last.click()
    
    # 给一点时间让表格数据刷新（如果以后发现截出来是旧数据，可以把这里的 3000 改成 5000）
    page.wait_for_timeout(3000)
    
    # 截图并保存为 latest.png（截取完整的整个长页面）
    print("开始截图...")
    page.screenshot(path="latest.png", full_page=True)
    
    print("截图成功！")
    browser.close()
