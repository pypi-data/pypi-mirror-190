import json
from lxml import etree
from exam import extract_ti
exam_html_path = r'C:\Users\wmj\Desktop\泸州市专业技术人员继续教育网-在线考试.html'
EXAM_TEST_JSON_PATH = 'examTest.json'
# with open(exam_html_path,encoding='utf-8') as f:
#     exam_data = f.read()
# print(exam_data)

def get_anwser():
    #提取题
    tree = etree.parse(exam_html_path,parser=etree.HTMLParser(encoding='utf-8'))
    dics = extract_ti(tree,1)
    print(dics)
    #寻找答案
    with open(EXAM_TEST_JSON_PATH) as f:
        exam_test_data = json.loads(f.read())
    for k,v in dics:
        anwser = []
        is_find_anwser = True
        for exam_ti in v:
            exam_ti['ti']



