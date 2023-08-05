import requests
import re
import time
from bs4 import BeautifulSoup
import json
from functools import reduce
#下载、删除重复、生成全部的json文件
'''
requests 基本使用
1.导入模块
2.发送请求
3.获取响应数据

BeautifulSoup：标签
bs4 和 lxml
1.导入模块
2.创建对象
'''

# sessionid = "u3hx8efc9oh9optqb2q2syewkfjfj95c"
# csrftoken = "Fx5nVfjjgAjc1HWyBsqjj5EwdhN7gkh8"

# user_session = "6018259341_true%26%261632800553%26%265400%26%264%26%26ceshi"
# password = "NjU5Njky"
# g = "4d71f92b38a60b812c3f7c629858af57"
# username = "6018259341"

user_session = "6018327895_true%26%261632895774%26%265400%26%264%26%26ceshi"
password = "Nzc5OTM0"
g = "532a612d4b6b38a43c4198f199af28e5"
username = "6018327895"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'Content-Type': 'application/json',
    'Cookie': 'user_session=' + user_session + '; password=' + password +';g='+g,
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'xtbz': 'cloud'
}


# print(response.encoding)  #编码方式
# response.encoding = 'utf-8' #指定编码方法
# print(response.text)  #打印数据，有时候编码会出错

# print(response.content.decode()) #content为二进制

def get_exam(url):
    response = requests.get(url = url,headers=headers)
    html = response.content.decode()
    html = html.split("SD_")[1:101]
    # for i in range(1,100):
    #     find_str = "SD_"+i
    #     html = html.find(find_str)
    data = []
    for item in html:
        item = item[item.find("<div class=\"exam-content\">"):]

        # 题型
        type = item[item.find("bold;\">")+len("bold;\">"):item.find("</span>")]
        pattern = re.compile(r'[^\u4e00-\u9fa5]')
        type = re.sub(pattern, '', type)


        # 题目
        content = item[item.find("</span>")+len("</span>"):item.find("</p>")]
        content = content[content.find("、")+1:]

        # 选项
        xuanxiang = item.split("</li>")[:-1]
        xx = []
        for index, i in enumerate(xuanxiang):
            i = i[i.rfind('>') + 1:]
            xx.append(i)

        # 答案
        anwser = item[item.find("正确答案："):]
        anwser = anwser[:anwser.find("</span>")]

        if item.find("答案解析") != -1:#可能存在答案解析
            anwser_explan = item[item.find("答案解析"):]
            anwser_explan = anwser_explan[anwser_explan.find("<span>")+len("<span>"):]
            anwser_explan = anwser_explan[:anwser_explan.find("</span>")]
        else:
            anwser_explan = ""

        d = {
            "type":type,
            "content":content,
            "select":xx,
            "anwser":anwser,
            "anwser_explan":anwser_explan
        }
        data.append(d)
    return data

wangzhi = r"https://www.aqscmnks.com/exam/View/shouye.php"
# wangzhi = 'https://www.aqscmnks.com/exam/View/lishijilu.php?type=adb1e8dfd8b46dabdd02bc798b490c40&xuHao=1&UUID=20518848'
response = requests.get(url = wangzhi,headers=headers)
html = response.content.decode()
html = html.split("lishijilu.php?")[1:-1]
data = []
for i,h in enumerate(html):
    new_url = "https://www.aqscmnks.com/exam/View/lishijilu.php?"+h[:h.find("\'")]
    data.extend(get_exam(new_url))

#去除重复的
run_function = lambda x, y: x if y in x else x + [y]
data = reduce(run_function, [[], ] + data)



with open(r"C:\Users\wmj\Desktop\exam_download\data_json.json","w",encoding='utf-8') as f:
    json.dump(data, ensure_ascii=False,indent=1,fp=f)





# soup = BeautifulSoup(response.content.decode(),"lxml") #lxml解析工具
# title = soup.find_all('div')
# print(title)