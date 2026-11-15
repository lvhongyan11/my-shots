import time
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(storage_state="state.json", viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    
    print("正在打开网页...")
    # 把超时时间从 60 秒延长到 90 秒，防止它没加载完
    page.goto(URL, timeout=90000)
    
    print("等待页面加载...")
    # 强行等 5 秒，让页面里的 JS 跑完
    page.wait_for_timeout(5000)
    
    try:
        print("寻找查询按钮...")
        # 换一种更聪明的寻找方式，包容性更强
        page.wait_for_selector("text=查询", timeout=20000)
        print("点击查询...")
        page.get_by_text("查询", exact=True).last.click()
        page.wait_for_timeout(3000) # 等数据刷新
    except Exception as e:
        print(f"出错了！没找到查询按钮，原因：{e}")
        print("正在保存诊断截图...")
        # 如果找不到按钮，或者跳回了登录页，先截一张图！存为 debug.png
        page.screenshot(path="debug.png", full_page=False)
        print("诊断截图已保存，程序退出。")
        browser.close()
        exit(1) # 故意报错，让 GitHub 变红叉，提醒我们去看诊断图

    print("开始截取最终数据图...")
    page.screenshot(path="latest.png", full_page=True)
    print("截图成功！")
    browser.close()
