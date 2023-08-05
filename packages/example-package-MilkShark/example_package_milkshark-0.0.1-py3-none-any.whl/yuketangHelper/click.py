import re
import os
# from selenium import webdriver

from selenium import webdriver
import time
userid = "6018327895"
password = "779934"

# 先登录
driver = webdriver.Chrome()
driver.get('https://www.aqscmnks.com/exam/View/login.php')
# time.sleep(3)
driver.find_element_by_xpath('//*[@id="card_no"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="card_pwd"]').send_keys(password)
time.sleep(2)
driver.find_element_by_xpath('//*[@id="input1"]').click()
def execute_alert():
    time.sleep(1)
    dialog_box = driver.switch_to.alert
    print(dialog_box.text)
    dialog_box.accept()

#创建、答题等
for j in range(17,31):
    driver.get('https://www.aqscmnks.com/exam/View/shouye.php')
    driver.find_element_by_xpath('//*[@id="btn1_tjsj"]').click() #创建试卷
    execute_alert()
    driver.get('https://www.aqscmnks.com/exam/View/shouye.php')
    driver.get(driver.find_element_by_xpath('//*[@id="tabk"]/tr['+str(j)+']/td[8]/a').get_attribute('href')) #开始答题
    driver.find_element_by_xpath('//*[@id="btn1_tjsj"]').click() #提交试卷
    for i in range(3):
        execute_alert()
'//*[@id="tabk"]/tr[17]/td[8]/a'

