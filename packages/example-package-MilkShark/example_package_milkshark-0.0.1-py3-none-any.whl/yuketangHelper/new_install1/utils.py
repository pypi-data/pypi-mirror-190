import os
import json
from global_variable import data_path,exam_path
import random

#win_random
def get_radom_exam():
    with open(data_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    data_judge = []
    data_judge_index = []
    data_select = []
    data_select_index = []

    for i,item in enumerate(data):
        if item["type"].find("判断题")!=-1:
            data_judge.append(item)
            data_judge_index.append(i+1)
        elif item["type"].find("单选题")!=-1:
            data_select.append(item)
            data_select_index.append(i+1)
        else:

            print("题型不对头！！！")

    random_judge_index = [random.randint(0,(len(data_judge_index)-1)) for i in range(70)]
    random_select_index = [random.randint(0,(len(data_select_index)-1)) for i in range(30)]
    random_index = [data_judge_index[i] for i in random_judge_index]+[data_select_index[i] for i in random_select_index]

    random_data = [data[i-1] for i in random_index]

    return random_data,random_index
#win_order
def get_order_exam():
    with open(data_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    return data

#win_select_exam
def get_old_exam():
    from os.path import exists
    if exists(exam_path):
        with open(exam_path, encoding='utf-8') as f:
            data = json.loads(f.read())
    else:
        data = []
    return data
#win_exam
def get_exam_and_done(i):
    with open(data_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    with open(exam_path, encoding='utf-8') as f:
        result = json.loads(f.read())

    for r in result:
        if r["exam_id"] == i:
            user_anwser = r["user_anwser"]
            exam = [data[i-1] for i in r["tihao"]]
            score = r["score"]
    return user_anwser,exam,score


#win_wrong
def get_wrong_ti(find_ti_type=0):
    #错题
    # find_ti_type = 0#-1表示没做的，0表示错误的，1表示正确

    with open(data_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    with open(exam_path, encoding='utf-8') as f:
        result = json.loads(f.read())

    exam = []
    user_anwsers = []
    tihaos = set()

    for r in result:
        if find_ti_type == 0:#错题
            for i,(user_anwser,tihao) in enumerate(zip(r["user_anwser"],r["tihao"])):
                correct_anwser = data[tihao-1]["anwser"]
                if user_anwser!=-1 and correct_anwser != chr(user_anwser+65):#错题
                    tihaos.add(tihao)
                    if len(tihaos) > len(exam):
                        exam.append(data[tihao-1])
                        user_anwsers.append(user_anwser)
        elif find_ti_type == -1:#没做的
            for i,(user_anwser,tihao) in enumerate(zip(r["user_anwser"],r["tihao"])):
                if user_anwser == -1:
                    tihaos.add(tihao)
                    if len(tihaos) > len(exam):
                        exam.append(data[tihao - 1])
                        user_anwsers.append(user_anwser)
        else:#正确的
            for i, (user_anwser, tihao) in enumerate(zip(r["user_anwser"], r["tihao"])):
                correct_anwser = data[tihao - 1]["anwser"]
                if correct_anwser == chr(user_anwser + 65):  # 正确
                    tihaos.add(tihao)
                    if len(tihaos) > len(exam):
                        exam.append(data[tihao - 1])
                        user_anwsers.append(user_anwser)
    return user_anwsers,exam