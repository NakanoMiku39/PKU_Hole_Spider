# -*- encoding:utf-8 -*-
#@Time		:	2021/11/23 22:21:52
#@File		:	SpiderForPKUHole.py
#@Author	:	Arthals
#@Contact	:	zhuozhiyongde@126.com
#@Software	:	Visual Studio Code

from selenium import webdriver
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import sqlite3
import configparser
import time

########## SETUPS ##########
# 创建或打开数据库
conn = sqlite3.connect('forum.db')
c = conn.cursor()

# 创建topics表
c.execute('''CREATE TABLE IF NOT EXISTS topics
             (id INTEGER PRIMARY KEY, content TEXT)''')

# 创建replies表，包含一个外键指向topics的id
c.execute('''CREATE TABLE IF NOT EXISTS replies
             (id INTEGER PRIMARY KEY, content TEXT, topic_id INTEGER,
             FOREIGN KEY(topic_id) REFERENCES topics(id))''')

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read('config.ini')

# 读取特定节（section）的配置信息
username = config['User']['username'] # 学号
password = config['User']['password'] # 密码
entries = config['User']['entries'] # # 希望爬取的树洞数

# 需安装selenium库4.0.0以上版本
# 需配置webdriver(chromedriver)文件，可自行按照chrome版本下载之后拖入/usr/local/bin
# 终端输入pip3 install selenium或者升级:pip3 install selenium --upgrade
options = Options()
options.add_argument(r"user-data-dir=/home/nakanomiku/.config/google-chrome") # 请更改为自己的cache路径
google = webdriver.Chrome(options=options)

url = "https://treehole.pku.edu.cn/web/"

############################

google.get(url)
time.sleep(5)
# 伪造人工登陆
if "login" in google.current_url: 
    print("Login required")
# 定位账号输入框
    username_input = google.find_element(By.XPATH, "//input[@type='text']")
    # 定位密码输入框
    password_input = google.find_element(By.XPATH, "//input[@type='password']")

    # 输入账号和密码
    if not username_input.get_attribute("value"):
        username_input.send_keys(username)
    if not password_input.get_attribute("value"):
        password_input.send_keys(password)
    # 定位到同意服务协议的复选框并点击以打勾
    # 注意，这里假设页面上只有这一个复选框
    google.find_element(By.XPATH, "//input[@type='checkbox']").click()

    # 定位登录按钮并点击
    # 这里假设登录按钮是页面上唯一的按钮元素，或者是文本明确标识为“登录”的唯一按钮
    google.find_element(By.XPATH, "//button[contains(text(),'登录')]").click()
    time.sleep(5)
    # 为输入验证码空出时间
    if "login" in google.current_url:
        time.sleep(30)
        
print("Logged in")

# 定位所有的 flow-item-row flow-item-row-with-prompt 元素
# 也就是树洞
flow_items = google.find_elements(By.XPATH, "//div[contains(@class,'flow-item-row flow-item-row-with-prompt')]")
action = ActionChains(google)
# 点击是为了确保之后的ARROW_DOWN能正常下滑窗口
google.find_element(By.XPATH, "//div[contains(@class,'title-bar')]").click()
# 判断是否能爬取到指定数量的树洞，如果不能就继续往下滑动
while len(flow_items) < int(entries):
    google.execute_script("window.scrollBy(0, 1000);")
    action.send_keys(Keys.ARROW_DOWN).perform()  # 模拟按下 Page Down 键
    flow_items = google.find_elements(By.XPATH, "//div[contains(@class,'flow-item-row flow-item-row-with-prompt')]")

# 爬取
for flow_item in flow_items:
    # 打开每一条树洞的sidebar
    flow_item.click()
    # 等待sidebar加载出来
    time.sleep(1)
    sidebar = WebDriverWait(google, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sidebar')]"))
    )
    
    # 获取指定数量树洞
    box_headers_in_sidebar = sidebar.find_elements(By.XPATH, "//div[contains(@class,'box-header box-header-top-icon')]")
    codes_in_sidebar = sidebar.find_elements(By.CLASS_NAME, "box-id")
    box_contents_in_sidebar = sidebar.find_elements(By.XPATH, "//div[contains(@class,'box-content box-content-detail')]")
    # 迭代洞中的每一条内容
    for index, (code, box_content) in enumerate(zip(codes_in_sidebar, box_contents_in_sidebar)):
        # 当前洞/回复号
        code = int(code.text[1:])
        if index == 0:
            c.execute("INSERT INTO topics (id, content) VALUES (?, ?)", (code, box_content.text))
        else:
            c.execute("INSERT INTO replies (id, content, topic_id) VALUES (?, ?, ?)", (code, box_content.text, int(codes_in_sidebar[0].text[1:])))
        
        # print(f"Header Text: {code}")
        # print(f"Content Text: {box_content.text}")    
            
    # 关闭sidebar
    close = sidebar.find_element(By.CSS_SELECTOR, "span.icon.icon-close") 
    close.click()
    time.sleep(1)
    
print("Total entries: %d" % len(flow_items))

# 此处填入目标txt文件地址,Ex."/Users/zhuozhiyongde/Desktop/Essay.txt"
    # for option in range(len(box_header_in_flow_item)):
        
    #     # 插入一个主题
    #     c.execute("INSERT INTO topics (id, content) VALUES (?, ?)", (code.group(1), main_text))
    #     replies = [i for i in reply_text]
    # c.executemany("INSERT INTO replies (id, content, topic_id) VALUES (?, ?, ?)", (replies, code.group(1)))
    
    #匹配树洞编号
    # num = re.search("#2\d+", header)
    # if num:
    #     # 判断是否需要抓取树洞编号
    #     if numLog == "y":
    #         serial = num.group()
    #         log.write("--------\n" + serial + "\n")
    #     # 不抓取的时，仅录入分隔符
    #     # 某些远古洞可能误判为包含原始树洞号，被误加分隔符，但整体错误率较低
    #     else:
    #         log.write("--------\n")
    # # 判断是否需要删去代称
    # if nameLog == "n":
    #     text = box_content[option].get_attribute('textContent')

    #     # 匹配第一个代称
    #     nameRe = re.match("\[\S+\] ", text)
    #     if nameRe:
    #         text = text.lstrip(nameRe.group())
    #     # 匹配Re代称
    #     reRe = re.match("Re \S+ ", text)
    #     if reRe:
    #         text = text.lstrip(reRe.group())
    # else:
    #     text = box_content[option].get_attribute('textContent')
    # log.write(text + "\n")
    # sum = sum + 1
    # 打印录入条目，每一百条打印一次
    # if sum % 100 == 0:
    #     print("当前已录入：", sum, "条\t进度：",
    #           "%.2f" % (sum / (len(box_content)) * 100), "%")
# print("总计录入：", sum, "条")

# 提交事务
conn.commit()
# 关闭连接
conn.close()

# 退出程序
# log.close()
google.quit()