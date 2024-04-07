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

import spider

########## SETUPS ##########
# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read('config.ini')

# 读取特定节（section）的配置信息
# username = config['User']['username'] # 学号
# password = config['User']['password'] # 密码
# entries = config['User']['entries'] # 希望爬取的树洞数
mode = config['User']['mode'] # 爬虫运行模式

# 需安装selenium库4.0.0以上版本
# 需配置webdriver(chromedriver)文件，可自行按照chrome版本下载之后拖入/usr/local/bin
# 终端输入pip3 install selenium或者升级:pip3 install selenium --upgrade
options = Options()
options.add_argument(r"user-data-dir=/home/nakanomiku/.config/google-chrome") # 请更改为自己的cache路径
# google = webdriver.Chrome(options=options)

url = "https://treehole.pku.edu.cn/web/"

############################

# 创建爬虫对象
s = spider.spider(config, url, "forum.db", options)
#登录
s.login()
time.sleep(5)

if mode == "crawl":
    s.crawl()
elif mode == "realtime":
    s.realtime()
else:
    print("Undefined mode")
    
# 提交事务
# conn.commit()
# 关闭连接
# conn.close()

# 退出程序
# log.close()
# google.quit()
# 定位所有的 flow-item-row flow-item-row-with-prompt 元素
# 也就是树洞

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

