import json
from pypinyin import lazy_pinyin


def sort_json(path):
    path = r'C:\Users\wmj\Desktop\lzsrcpx\（公需科目）【2021】_examTest.json'
    # new_path = r'C:\Users\wmj\Desktop\lzsrcpx\（公需科目）人工智能与健康【2020】_examTest.json'

    with open(path,encoding='utf-8') as f:
        data = json.loads(f.read())
    new_data = {}
    for k,v in data.items():
        new_dic = {}
        d = data[k]
        x = list(d.keys())
        d_order = sorted(x, key=lambda i:lazy_pinyin(i))
        for i in d_order:
            new_dic[i] = data[k][i]
        new_data[k] = new_dic.copy()
    with open(path,'w',encoding='utf-8') as f:
        json.dump(new_data,fp=f,indent=1,ensure_ascii=False)

sort_json('')