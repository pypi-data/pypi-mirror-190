#删除重复的
import json
import os

from configuration import EXAM_SAVE_PATH,EXAM_TEST_SAVE_PATH

def paint_num():
    for save_path in [EXAM_SAVE_PATH,EXAM_TEST_SAVE_PATH]:
        if os.path.exists(save_path):
            print(save_path)
            with open(save_path, encoding='utf-8') as f:
                src_data = json.loads(f.read())
            print('单选数目',len(src_data["单选"]))
            print('多选数目',len(src_data["多选"]))
            print('判断数目',len(src_data["判断"]))
        else:
            print('路径不存在：',save_path)




def match_ti():
    def remove_item(a,b): #从a中去除掉b
        c = a + b
        c = set(c)
        for i in b:
            c.remove(i)
        return c


    with open(EXAM_TEST_SAVE_PATH, encoding='utf-8') as f:
        test_data = json.loads(f.read())
    with open(EXAM_SAVE_PATH, encoding='utf-8') as f:
        exam_data = json.loads(f.read())

    for key,value in exam_data.items():
        exam_tis = list(value.keys())
        test_tis = list(test_data[key].keys())

        exam_without_exists = remove_item(exam_tis,test_tis)
        print("{} 已检测个数：{}，未检测个数：{}".format(key,len(exam_data[key])-len(exam_without_exists),len(exam_without_exists)))

if __name__ == "__main__":
    paint_num()
    match_ti()

