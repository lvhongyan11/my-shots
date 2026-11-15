import time
import os
import datetime
import base64
import requests
from playwright.sync_api import sync_playwright

URL = "http://111.42.63.196:50000/smart-web/index.html"

USERNAME = os.environ.get("SITE_USER")
PASSWORD = os.environ.get("SITE_PASS")
PUSHPLUS_TOKEN = os.environ.get("PUSHPLUS_TOKEN")
PUSHPLUS_TOPIC = os.environ.get("PUSHPLUS_TOPIC")

def send_to_wechat(image_path):
    if not PUSHPLUS_TOKEN:
        print("未配置 PushPlus Token，跳过推送。")
        return
        
    print("正在将图片发送到微信群...")
    # 把图片转成 Base64，直接塞进消息里，防止国内网络拦截
    with open(image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    html_content = f'<img src="data:image/png;base64,{img_base64}" style="width:100%;" />'
    
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": "供热数据整点截图",
        "content": html_content,
        "template": "html"
    }
    
    if PUSHPLUS_TOPIC:
        payload["topic"] = PUSHPLUS_TOPIC

    try:
        res = requests.post("https://www.pushplus.plus/send", json=payload, timeout=30)
        print("微信推送结果:", res.text)
    except Exception as e:
        print("微信推送失败:", e)

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        timezone_id="Asia/Shanghai"
    )
    page = context.new_page()
    
    print("正在打开网页...")
    page.goto(URL, timeout=90000)
    page.wait_for_timeout(6000) 

    try:
        print("检查是否需要登录...")
        if page.locator("input[type='password']").count() > 0:
            print("发现登录页面，正在模拟键盘输入...")
            pwd_input = page.locator("input[type='password']").first
            user_input = page.locator("input[type='text']").first
            
            user_input.click()
            user_input.press("Control+A")
            user_input.press("Backspace")
            user_input.press_sequentially(USERNAME, delay=100)
            page.wait_for_timeout(500)
            
            pwd_input.click()
            pwd_input.press_sequentially(PASSWORD, delay=100)
            page.wait_for_timeout(1000)
            
            print("尝试点击登录按钮...")
            login_btn = page.locator("text='登录'").last
            if login_btn.is_visible():
                login_btn.click(force=True)
            else:
                pwd_input.press("Enter")

            print("已提交登录，等待系统加载...")
            page.wait_for_timeout(10000)
            
        print("第 1 步：点击顶部【末端平衡】")
        page.get_by_text("末端平衡").first.click(timeout=20000)
        page.wait_for_timeout(3000) 
        
        print("第 2 步：点击左侧【户端实时】")
        page.get_by_text("户端实时").first.click(timeout=20000)
        page.wait_for_timeout(2000) 
        
        print("第 3 步：点击子菜单【室温KPI】")
        page.get_by_text("室温KPI").first.click(timeout=20000)
        page.wait_for_timeout(8000) 
        
        try:
            print("尝试点击【查询】按钮...")
            page.get_by_text("查询").last.click(timeout=5000)
            page.wait_for_timeout(3000) 
        except Exception as e:
            print("点击查询可能失败或不需要点，无视它，直接截图。")

        print("开始截取最终数据图...")
        
        page.screenshot(path="latest.png", full_page=True)
        
        beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
        now = datetime.datetime.now(beijing_tz)
        time_str = now.strftime("%Y%m%d_%H%M%S")
        filename = f"shots/{time_str}.png"
        
        if not os.path.exists("shots"):
            os.makedirs("shots")
            
        page.screenshot(path=filename, full_page=True)
        print(f"✅ 截图成功！已保存为 latest.png 以及历史图片 {filename}")
        
        # 发送到微信
        send_to_wechat("latest.png")
        
    except Exception as e:
        print(f"❌ 操作失败，原因：{e}")
        page.screenshot(path="debug.png", full_page=True)
    finally:
        browser.close()
