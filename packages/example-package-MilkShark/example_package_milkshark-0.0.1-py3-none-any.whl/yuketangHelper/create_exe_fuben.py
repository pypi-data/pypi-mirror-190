# -*- coding:utf-8 -*-
# 摇3次骰子，当总数total，3<=total<=10时为小，11<=total<=18为大
__author__ = 'zhou'

import random
import time
import tkinter
import json



class Frame_Tihao(tkinter.Frame):
    def __init__(self, master,exam):
        super().__init__(master)
        self["bg"] = "yellow"
        self.pack(side="left")
        self.frame_ti = Frame_Ti(master)
        self.exam = exam

        for i in range(100):
            tihao = tkinter.Button(self, text=str(i+1),command=lambda x=i:self.frame_ti.refresh(x,exam[x]),bg="red")
            tihao.pack()

class Frame_Ti(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side="right")
        self.ti = []
        self.user_anwser = ""
        self.index = 0

        self.type = tkinter.Label(self)
        self.type_string = tkinter.StringVar()
        # self.timu = tkinter.Label(self, text=str(self.index) + "、" + self.ti["content"])
        self.timu = tkinter.Label(self)
        self.timu_string = tkinter.StringVar()
        self.xx =[tkinter.Button(self, command=lambda x=i:self.click(x)) for i in range(4)]
        self.xx_string = [tkinter.StringVar() for i in range(4)]

        self.result = tkinter.Label(self)
        self.result_string = tkinter.StringVar()
        self.timu["textvariable"] = self.timu_string


    def click(self,i):
        if self.ti["anwser"] == chr(i+65):
            print("there")
            self.result_string.set("回答正确")
        else:
            self.result_string.set("回答错误")
        self.result["textvariable"] = self.result_string
        self.result.pack()

    def refresh(self, index, ti):
        self.index = index
        self.ti = ti
        print(index,ti)
        self.result.forget()
        #题型
        self.type_string.set(self.ti["type"])
        self.type["textvariable"] = self.type_string
        self.type["bg"] = "blue"
        self.type.pack()
        # 题目
        self.timu_string.set(str(self.index) + "、" + self.ti["content"])
        self.timu["bg"] = "blue"
        self.timu.pack()
        # 选项
        for xx in self.xx:
            xx.forget()
        for i, xx_string in enumerate(self.ti["select"]):
            xx = self.xx[i]
            self.xx_string[i].set(chr(i + 65) + "、" + self.ti["select"][i])
            xx["textvariable"] = self.xx_string[i]
            xx.pack()

def get_exam(file_path):
    with open(file_path,encoding='utf-8') as f:
        data = json.loads(f.read())
    random_data = random.sample(data,100)
    return random_data



def start_game():

    exam = get_exam(r"C:\Users\wmj\Desktop\html\view\data.json")
    root = tkinter.Tk()
    root.geometry('600x400+30+40')
    print(exam[0])

    frame_tihao = Frame_Tihao(root,exam)
    #上一题、下一题
    # last = tkinter.Button(root, text="上一题",command=lambda:click(root,exam[0],'A'))
    # next = tkinter.Button(root, text="下一题",command=lambda:click(root,exam[0],'A'))

    #题号
    frame = ""
    root.mainloop()


if __name__ == '__main__':
    start_game()
