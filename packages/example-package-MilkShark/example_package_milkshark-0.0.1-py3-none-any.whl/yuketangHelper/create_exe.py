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
        self.grid(column=1,row=2)
        self.btns = []
        self.frame_ti = Frame_Ti(master)
        self.exam = exam

        for i in range(100):
            tihao = tkinter.Button(self, text=str(i+1),command=lambda x=i:self.frame_ti.refresh(x,exam[x]),bg="red")
            tihao.grid(column = i%10, row = i//10)
            tihao["width"] = 2
            tihao["height"] = 1
            self.btns.append(tihao)

class Frame_Ti(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(column=2,row=2)
        self.ti = []
        self.user_anwser = ""
        self.index = 0

        self.type = tkinter.Label(self)
        self.type_string = tkinter.StringVar()
        # self.timu = tkinter.Label(self, text=str(self.index) + "、" + self.ti["content"])
        self.timu = tkinter.Label(self,width=20,height=10)
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
        self.result.grid(column=0,row=18,rowspan=3,columnspan=5,sticky="W")

    def refresh(self, index, ti):
        self.index = index
        self.ti = ti
        print(index,ti)
        self.result.grid_forget()
        #题型
        self.type_string.set(self.ti["type"])
        self.type["textvariable"] = self.type_string
        self.type["bg"] = "blue"
        self.type.grid(column=0,row=0,rowspan=2,columnspan=5,sticky="W")
        # 题目
        self.timu_string.set(str(self.index) + "、" + self.ti["content"])
        self.timu["bg"] = "blue"
        self.timu.grid(column=0,row=2,rowspan=3,columnspan=5,sticky="W")
        # 选项
        for xx in self.xx:
            xx.forget()
        for i, xx_string in enumerate(self.ti["select"]):
            xx = self.xx[i]
            self.xx_string[i].set(chr(i + 65) + "、" + self.ti["select"][i])
            xx["textvariable"] = self.xx_string[i]
            xx.grid(column=0,row=5+i*3,rowspan=3,columnspan=5,sticky="W")

def get_exam(file_path):
    with open(file_path,encoding='utf-8') as f:
        data = json.loads(f.read())
    random_data = random.sample(data,100)
    return random_data

def ccc(root):
    print(root["width"])
    print(root["height"])
    print("hello")


def start_game():

    exam = get_exam(r"C:\Users\wmj\Desktop\html\view\data.json")
    root = tkinter.Tk()
    root.geometry('600x400+30+40')
    root.attributes("-fullscreen", True)
    print(exam[0])

    frame_tihao = Frame_Tihao(root,exam)
    #上一题、下一题
    # last = tkinter.Button(root, text="上一题",command=lambda:click(root,exam[0],'A'))
    # next = tkinter.Button(root, text="下一题",command=lambda:click(root,exam[0],'A'))

    #题号
    btn = tkinter.Button(root,text="anyixia",command=lambda:ccc(root))
    btn.grid(column=1,row=13)

    root.mainloop()


if __name__ == '__main__':
    start_game()
