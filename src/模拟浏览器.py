from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

path = Service(executable_path="C:/Users/13115925968/AppData/Local/Programs/Python/Python39/Lib/geckodriver.exe")
driver = webdriver.Firefox(service=path)  # Firefox浏览器
driver.get("http://q.10jqka.com.cn/gn/")
# last_height = driver.execute_script("return document.body.scrollHeight")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到底部

# cookie=driver.get_cookies()
# print(cookie)
# print(cookie[0]['value'])
# driver.refresh()
# print(driver.get_cookies())

above = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/a")
ActionChains(driver).click(above).perform()

html = BeautifulSoup(driver.page_source, "html.parser")  # 获取源码
body = html.find("div", attrs={"class": "cate_inner visible"})
a = body.find_all('a')
for i in a:
    print(i['href'], i.string)
