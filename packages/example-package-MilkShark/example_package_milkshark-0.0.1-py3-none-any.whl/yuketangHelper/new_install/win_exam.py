
import time
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import json
from tkutils import _ft,_font,v_seperator,h_seperator,image_label,center_window
from  utils import get_exam_and_done
from win import BaseWindow


class Window(BaseWindow):
    def __init__(self,parent,i):
        super(Window, self).__init__(parent)

        self.user_anwser, self.exam, self.score = get_exam_and_done(i)
        self.exam_id = i

        self.body()  # 绘制窗体组件
        self.set_score_label()

        self.set_string(self.score_label,self.score)
    def main_top(self, parent):
        def label(frame, text, bg="gray",size=12):
            return tk.Label(frame, bg=bg, fg="black",text=text, width=20,height=2,font=_ft(size))

        frame = tk.Frame(parent, bg="white", height=150)

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
        label(explain_frame,"正确","green").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        label(explain_frame,"错误","red").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        label(explain_frame,"未填","gray").pack(side=tk.TOP,fill=tk.X,padx=15,pady=5)
        explain_frame.pack(side=tk.LEFT,fill=tk.Y)

        return frame

    def main_left_tihao(self, parent):
        def button(frame, text, size, bold=False):
            btn = tk.Button(frame, text=text, bg="#d3d7d4", fg="black", width=2, height=1, font=_ft(size, bold))
            btn.config(relief=tk.FLAT)
            return btn
        for i in range(10):
            btn_frame = tk.Frame(parent, bg="white")
            for j in range(10):
                k = i * 10 + j + 1
                btn = button(btn_frame, k, 8)
                if self.exam[k-1]['anwser'] == (chr(self.user_anwser[k-1]+65)):
                    btn["bg"] = "green"
                elif self.user_anwser[k-1] ==-1:
                    btn["bg"] = "gray"
                else:
                    btn["bg"] = "red"
                btn["command"] = lambda x=k:self.change_ti_button_click(x)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.btns.append(btn)
            btn_frame.pack(fill=tk.X)

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
        #与win_order和win_random不一样，全部都要显示答案,不更改btns的颜色
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



