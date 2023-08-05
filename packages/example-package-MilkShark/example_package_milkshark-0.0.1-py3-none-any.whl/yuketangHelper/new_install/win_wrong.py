
import time
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import json
from tkutils import _ft,_font,v_seperator,h_seperator,image_label,center_window
from  utils import get_wrong_ti
from win import BaseWindow

class Window(BaseWindow):
    def __init__(self,parent):
        super(Window, self).__init__(BaseWindow)
        # 数据
        self.index = 1
        self.find_ti_type = 0
        self.user_anwser, self.exam = get_wrong_ti(self.find_ti_type)
        self.body()  # 绘制窗体组件

    def change_ti_type(self,i):

        self.find_ti_type = i
        self.user_anwser, self.exam = get_wrong_ti(self.find_ti_type)
        self.main_left_frame.destroy()
        self.main_left_frame = self.main_left(self.main_frame)
        self.pack_all()

        self.index = 1
        self.refresh_main_right_content()

    #不一样的点在于需要重新读取数据，改变错题类型
    def main_top(self, parent):

        def button(frame, text,i, bg="gray",size=11):
            return tk.Button(frame, bg=bg, fg="black",text=text, width=20,height=1,font=_ft(size),relief=tk.FLAT,command=lambda x=i:self.change_ti_type(x))

        frame = tk.Frame(parent, bg="white", height=130)

        image_label(frame, "images\\study1.bmp", width=150, height=120, keep_ratio=False) \
            .pack(side=tk.LEFT, padx=10, pady=10)
        image_label(frame, "images\\study2.bmp", width=150, height=120, keep_ratio=False) \
            .pack(side=tk.LEFT, padx=10, pady=10)
        image_label(frame, "images\\study3.bmp", width=150, height=120, keep_ratio=False) \
            .pack(side=tk.LEFT, padx=10, pady=10)
        image_label(frame, "images\\study4.bmp", width=120, height=120, keep_ratio=False) \
            .pack(side=tk.LEFT, padx=10, pady=10)
        image_label(frame, "images\\study5.bmp", width=150, height=120, keep_ratio=False) \
            .pack(side=tk.LEFT, padx=10, pady=10)
        explain_frame = tk.Frame(frame,bg="white",height=150)
        button(explain_frame,"正确",1,"green").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        button(explain_frame,"错误",0,"red").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        button(explain_frame,"未填",-1,"gray").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        explain_frame.pack(side=tk.LEFT,fill=tk.Y)

        return frame

    #与win_random最大区别就在于需要翻页
    def main_left_tihao(self, parent):
        def button(frame, text, size, bold=False):
            btn = tk.Button(frame, text=text, bg="#d3d7d4", fg="black", width=2, height=1, font=_ft(size, bold))
            btn.config(relief=tk.FLAT)
            return btn
        self.btns = []
        btn_frames = []
        last_btns = []
        next_btns = []

        def refresh_yema_tihao(i,j):
            if i>=j:
                return
            #其他的关掉
            for btn in last_btns+next_btns+btn_frames:
                btn.forget()
            #显示新的btn
            for k in range(i,j):
                btn_frames[k].pack(side=tk.TOP,fill=tk.X)
            #上一页下一页
            yeshu = int(i/10)
            last_btns[yeshu].pack(side=tk.LEFT,padx=8,pady=5)
            next_btns[yeshu].pack(side=tk.RIGHT,padx=8,pady=5)
        from math import ceil
        def last_btn_click(i):
            if i == 0:
                return
            else:
                refresh_yema_tihao((i-1)*10,i*10)

        def next_btn_click(i):
            totol_ye = ceil(len(btn_frames) / 10)
            if i+1 == totol_ye:
                return
            elif i+1 == totol_ye-1:
                refresh_yema_tihao((i+1)*10,len(btn_frames))
            else:
                refresh_yema_tihao((i+1)*10,(i+2)*10)

        for i in range(ceil(len(self.exam)/10)):
            btn_frame = tk.Frame(parent, bg="white")
            for j in range(10):
                k = i * 10 + j + 1
                if k > len(self.exam):
                    break
                btn = button(btn_frame, k, 8)

                if self.exam[k-1]['anwser'] == (chr(self.user_anwser[k-1]+65)):
                    btn["bg"] = "green"
                elif self.user_anwser[k-1] ==-1:
                    btn["bg"] = "gray"
                else:
                    btn["bg"] = "red"

                btn["command"] = lambda x=k: self.change_ti_button_click(x)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.btns.append(btn)
            btn_frames.append(btn_frame)

        for i in range(ceil(len(self.exam)/100)):
            last_btn = tk.Button(parent,text="上一页",width=15,height=2,command=lambda x = i:last_btn_click(x))
            last_btns.append(last_btn)
            next_btn = tk.Button(parent,text="下一页",width=15,height=2,command=lambda x = i:next_btn_click(x))
            next_btns.append(next_btn)

        refresh_yema_tihao(0,min(10,len(btn_frames)))

    def refresh_main_right_content(self):#一种是点击了上一题和下一题，一种是点击了题号
        # 题型
        ti = self.exam[self.index-1]
        self.set_string(self.main_right_type,ti["type"])
        # 题目
        self.set_string(self.main_right_timu,str(self.index) + "、" + ti["content"])
        # 选项
        for i, xx_string in enumerate(ti["select"]):
            self.set_string(self.main_right_xx[i],chr(i + 65) + "、" + xx_string)
            self.main_right_xx[i]["state"] = "disabled"

        #结果
        ti = self.exam[self.index - 1]
        if ti["anwser"] == chr(self.user_anwser[self.index - 1] + 65):
            self.main_right_result["fg"] = "green"
            result_string = "回答正确,正确答案:" + ti["anwser"]
        else:
            self.main_right_result["fg"] = "red"
            result_string = "回答错误,正确答案:" + ti["anwser"]

        if ti["anwser_explan"] != "":
            result_string = result_string + "\n答案解析：" + ti["anwser_explan"]

        self.set_string(self.main_right_result, result_string)
        self.pack_main_right(True)
