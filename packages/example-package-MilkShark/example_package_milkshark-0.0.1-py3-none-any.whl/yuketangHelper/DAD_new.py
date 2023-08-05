import re
import os
def remove_repeat(content_path_list,anwser_path_list):
    content_dic = {}
    des_content = ""
    des_anwser = ""
    all_exam = ""
    for content_path,anwser_path in zip(content_path_list,anwser_path_list):
        with open(content_path) as f:
            content = f.read()
        with open(anwser_path) as f:
            anwser = f.read()
        content_list = content.split("\n\n\n")
        anwser_list = anwser.split("\n\n")

        for c,a in zip(content_list,anwser_list):
            new_c = c[c.find('、')+1:c.find('A')]
            content_dic[new_c] = (c,a)
    for i, (c, a) in enumerate(content_dic.values()):
        try:
            tihao = c[c.find(re.findall("\d+", c)[0]):c.find('、') + 1]
        except BaseException:
            print(c)
        else:

            new_tihao = str(i + 1) + "、"
            c = c.replace(tihao, new_tihao)
            a = new_tihao + a[a.find("正确"):]
            des_content += c + "\n\n"
            des_anwser += a + "\n\n"
            all_exam += c + "\n" + a + "\n\n"

    # des_exam_without_anwser_path = r"C:\Users\wmj\Desktop\exam\all_exam_without_anwser.txt"
    # des_anwser_path = r"C:\Users\wmj\Desktop\exam\all_anwser.txt"
    # des_exam_path = r"C:\Users\wmj\Desktop\exam\all_exam.txt"

    # with open(des_exam_without_anwser_path,"w") as f:
    #     f.write(des_content)
    # with open(des_anwser_path,"w") as f:
    #     f.write(des_anwser)
    # with open(des_exam_path,"w") as f:
    #     f.write(all_exam)
    return  des_content,des_anwser,all_exam

content_path = r"C:\Users\wmj\Desktop\exam_download\all_exam_without_anwser.txt"
anwser_path = r"C:\Users\wmj\Desktop\exam_download\all_anwser.txt"
des_exam_without_anwser_path = r"C:\Users\wmj\Desktop\exam\all_exam_without_anwser.txt"
des_anwser_path = r"C:\Users\wmj\Desktop\exam\all_anwser.txt"
des_exam_path = r"C:\Users\wmj\Desktop\exam\all_exam.txt"
exam_dir = r"C:\Users\wmj\Desktop\exam"
content_path_list = []
anwser_path_list = []
des_content,des_anwser,all_exam = remove_repeat(content_path_list,anwser_path_list)

with open(des_exam_without_anwser_path, "w") as f:
    f.write(des_content)
with open(des_anwser_path, "w") as f:
    f.write(des_anwser)
with open(des_exam_path, "w") as f:
    f.write(all_exam)
