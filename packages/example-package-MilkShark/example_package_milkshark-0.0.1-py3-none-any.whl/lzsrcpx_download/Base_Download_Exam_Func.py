import json
import os
import re
import requests
from multiprocessing.dummy import Pool
from lxml import etree
from configuration import HEADERS, config
import time


# 抽取题目
def extract_ti(tree, pos=1, exam_type='exam'):  # pos:1单选 2多项 3判断  exam_type:exam test

    objs = tree.xpath('/html/body/div[3]/div/div/div[2]/div/form/div[{}]/div[@class="txbox"]'.format(pos))
    dics = {}
    for item in objs:
        # 题目
        src_ti = item.xpath('./ul/li[1]//text()')[0]
        ti = src_ti[src_ti.find('、') + len('、'):]
        # print(ti)

        # 选项
        xxs = []
        src_selects_xpath = item.xpath('./ul/li')[1:-1]
        for src_select in src_selects_xpath:
            xxs.append(src_select.xpath('.//text()')[0])

        if exam_type == 'exam':  # exam
            dics[ti] = {
                'xx': xxs,
            }
        else:  # test
            # 答案
            li_item = item.xpath('./ul/li')[-1]
            label_item = li_item.xpath('./div/label')[-1]
            answer = label_item.xpath('./@val')[0]

            dics[ti] = {
                'xx': xxs,
                'answer': answer,
            }
    return dics


# 下载一次
def download_exam(exam_type):
    response = requests.get(url=config[exam_type]['url'], headers=HEADERS)
    tree = etree.HTML(response.text)
    data = {
        "单选": extract_ti(tree, 1, exam_type),
        "多选": extract_ti(tree, 2, exam_type),
        "判断": extract_ti(tree, 3, exam_type),
    }
    return data


# 组合多个data
def combine_data(data1, data2):
    if data1 is None and data2 is not None:
        return data2
    elif data2 is None and data1 is not None:
        return data1

    # data1["单选"].extend(data2["单选"])
    # data1["多选"].extend(data2["多选"])
    # data1["判断"].extend(data2["判断"])
    # data = remove_dp(data1,'ti')
    data1["单选"].update(data2["单选"])
    data1["多选"].update(data2["多选"])
    data1["判断"].update(data2["判断"])
    return data1


# 保存
def save_data(save_path, data):
    if os.path.exists(save_path):
        with open(save_path, encoding='utf-8') as f:
            src_data = json.loads(f.read())
        src_data = combine_data(src_data, data)
    else:
        src_data = data
    # src_data = remove_dp(src_data,'ti')

    # 保存
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(src_data, fp=f, ensure_ascii=False, indent=1)


# 下载N次
def download_exams(exam_download_num, sleep_time, exam_type, config):
    data = None
    for i in range(exam_download_num):
        print('正在下载{}第{}套题'.format(exam_type, i))
        time.sleep(sleep_time)
        new_data = download_exam(exam_type)
        # 如果提取的为空，则断开报错
        if len(new_data['单选']) == 0:
            print("没有正确下载页面，请检查Cookie是否正确！")
            exit()

        data = combine_data(new_data, data)
    save_data(config[exam_type]['save_path'], data)


def get_anwser_string(anwser_results):
    anwsers_string = ''
    for k,v in anwser_results.items():
        v = [i.replace(',','') for i in v]
        anwsers = '\n'.join(['\t'.join(v[i-5:i]) for i in range(5,len(v)+1,5)])
        anwsers_string += '{}(共{}个，{}个未找到答案):\n{}\n'.format(k,len(v),v.count('N'),anwsers)
    print(anwsers_string)


    # string = '单选:(共{}个，{}个未找到答案)\n{}多选:(共{}个，{}个未找到答案)\n{}判断:(共{}个，{}个未找到答案)\n{}'
def parse_exam(save_path, exam_path):
    def parse_anwser_only(tis, pos):
        if os.path.exists(save_path):
            with open(save_path, encoding='utf-8') as f:
                test_data = json.loads(f.read())
            if pos == 1:
                anwser_list = []
                for ti in tis:
                    if ti in list(test_data["单选"].keys()):
                        anwser_list.append(test_data["单选"][ti]['answer'])
                    else:
                        anwser_list.append('N')

            elif pos == 2:
                anwser_list = []
                for ti in tis:
                    if ti in list(test_data["多选"].keys()):
                        anwser_list.append(test_data["多选"][ti]['answer'])
                    else:
                        anwser_list.append('N')

            else:
                anwser_list = []
                for ti in tis:
                    if ti in list(test_data["判断"].keys()):
                        anwser_list.append(test_data["判断"][ti]['answer'])
                    else:
                        anwser_list.append('N')
            return anwser_list
        else:
            pass

    def parse(tree, pos):
        objs = tree.xpath('/html/body/div[3]/div/div/div[2]/div/form/div[{}]/div[@class="txbox"]'.format(pos))
        tis = []
        for item in objs:
            # 题目
            src_ti = item.xpath('./ul/li[1]//text()')[0]
            ti = src_ti[src_ti.find('、') + len('、'):]
            tis.append(ti)
        return tis

    tree = etree.parse(exam_path, parser=etree.HTMLParser(encoding='utf-8'))
    # 只生成答案
    # 生成全套题目
    anwser_results = {
        "单选": parse_anwser_only(parse(tree, 1),1),
        "多选": parse_anwser_only(parse(tree, 2),2),
        "判断": parse_anwser_only(parse(tree, 3),3),
    }
    return anwser_results




def get_courseId(headers,name):
    url = 'http://www.lzsrcpx.com/reg/myExam'
    contents = requests.get(url=url, headers=headers).text
    tree = etree.HTML(contents)
    a = tree.xpath('/html/body/div[3]/div/div[3]/div[2]/div/div/div/div/table/tbody/tr[1]/td[5]/a/@href')[0]
    patters = ".*?'(.*?)',.*?{}.*?".format(name)
    courseID = re.findall(patters,a)[0]
    return courseID

get_courseId()



# anwser_results = parse_exam('examTest.json',r'C:\Users\wmj\Desktop\泸州市专业技术人员继续教育网-在线考试.html')
# get_anwser_string(anwser_results)
# 去除相同项
# def remove_dp(data,key):
#     new_data = {}
#     values = []
#     for k,v in data.items():
#         new_v = []
#         for d in v:
#             if d[key] not in values:
#                 values.append(d[key])
#                 new_v.append(d)
#         new_data[k] = new_v
#     return new_data
