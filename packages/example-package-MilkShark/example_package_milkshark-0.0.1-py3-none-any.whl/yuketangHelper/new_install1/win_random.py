# coding:utf-8

# *****************************************************************************
# 模块说明：利用 pack 方法，模拟构建人工智能的定制平台界面，只用于界面制作的学习参考
#          界面代码进行了分层编写，在容器层，设置子组件的pack()，
#          在子组件层， 创建自身框架，布局自己的子组件， 并返回自身，供容器布局
#          界面的结构层次比较清晰，修改调整会方便些
# 开发人员: Edwin.Zhang
# 开发时间: 2018-09-28
# *****************************************************************************
import time
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import json
import random
from tkutils import _ft,_font,v_seperator,h_seperator,image_label,center_window
from utils import get_radom_exam




class Window:
    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.parent = parent


        self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
        center_window(self.root)  # 将窗体移动到屏幕中央
        self.root.title("危险化学品经营考试")  # 窗体标题
        self.root.iconbitmap("images\\Money.ico")  # 窗体图标

        #数据
        self.index = 1
        self.exam, self.tihao = get_radom_exam()
        self.user_anwser = [-1 for i in range(len(self.exam))]  # 0表示A,1表示B，2表示C，3表示D，-1为未选择

        #所有需要组装的大控件
        self.title_frame = None
        self.main_frame = None
        self.main_top_frame = None
        self.main_left_frame = None
        self.main_v_seperator_frame = None
        self.main_right_frame = None
        self.bottom_frame = None

        #显示题的小控件,在main_right里面
        self.main_right_type = None
        self.main_right_timu = None
        self.main_right_xx = None
        self.main_rifht_last_next_btns = None
        self.main_right_result = None

        self.score_label = None
        self.btns = []

        self.body()  # 绘制窗体组件


    #重新组装
    def pack_all(self):
        self.title_frame.forget()
        self.main_top_frame.forget()
        self.main_left_frame.forget()
        self.main_v_seperator_frame.forget()
        self.main_frame.forget()
        self.main_right_frame.forget()
        self.bottom_frame.forget()

        self.title_frame.pack(fill=tk.X)
        self.main_top_frame.pack(fill=tk.X, padx=30, pady=15)
        self.main_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=30)
        self.main_v_seperator_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_right_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        self.main_frame.pack(expand=tk.YES, fill=tk.BOTH)
        self.bottom_frame.pack(fill=tk.X)
    #计算分数
    def calculate_score(self):
        score = 0
        for i in range(100):
            user_anwser = chr(self.user_anwser[i] + 65)
            anwser = self.exam[i]["anwser"]
            if user_anwser == anwser:
                score += 1
        return score
    #是否完成所有问题
    def is_finish(self):
        if min(self.user_anwser) >= 0:
            return True
        else:
            return False
    #这道题是否已经被做过了
    def is_done(self):
        return  self.user_anwser[self.index - 1] >= 0
    #为控件更换文字
    def set_string(self,frame,s):
        sv = tk.StringVar()
        sv.set(s)
        frame["textvariable"] = sv
    #点击更换题
    def change_ti_button_click(self,i):
        self.index = i
        self.refresh_main_right_content()
    # 绘制窗体组件
    def body(self):
        self.title_frame = self.title(self.root)
        self.main_frame = self.main(self.root)
        self.bottom_frame = self.bottom(self.root)
        self.pack_all()

    def title(self, parent):
        """ 标题栏 """
        def button(frame, text, size, bold=False):
            return tk.Label(frame, text=text, bg="black", fg="white", height=2, font=_ft(size, bold), relief=tk.FLAT)
        frame = tk.Frame(parent, bg="black")
        button(frame, "危险化学品经营单位初训系统", 16, True).pack(side=tk.LEFT, padx=10)
        return frame
    def bottom(self, parent):
        """ 窗体最下面留空白 """
        frame = tk.Frame(parent, height=10, bg="whitesmoke")
        frame.propagate(True)
        return frame
    def main(self, parent):
        """ 窗体主体 """
        frame = tk.Frame(parent, bg="whitesmoke")

        self.main_top_frame = self.main_top(frame)
        self.main_left_frame = self.main_left(frame)
        self.main_v_seperator_frame = v_seperator(frame, 30)
        self.main_right_frame = self.main_right(frame)

        return frame
    def main_top(self, parent):
        def label(frame, text, size=12):
            return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(size))

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

        # self.main_top_middle(frame).pack(side=tk.LEFT)

        def submit():
            if self.is_finish():
                message = "您已完成所有问题，确定交卷？"
            else:
                message = "还有问题没有做答，确定交卷？"
            is_submit = messagebox.askokcancel(title='交卷提示', message=message)
            if is_submit:
                # 计算得分
                score = self.calculate_score()

                #把试卷答案存下来。
                exam_path = r"data\exam.json"
                from os.path import exists
                id = 1
                data = []
                if exists(exam_path):
                    with open(exam_path,encoding='utf-8') as f:
                        data = json.loads(f.read())
                    if data and len(data)>0:
                        id = max([d["exam_id"] for d in data])+1
                else:
                    data = []
                    id = 1
                item ={
                    "exam_id":id,
                    "tihao":self.tihao,
                    "user_anwser":self.user_anwser,
                    "score":score,
                    "time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
                data.append(item)
                with open(exam_path,"w") as f:
                    json.dump(data,fp=f,indent=1,ensure_ascii=False)
                messagebox.showinfo(title="交卷成功",message="您最后得分为："+str(score)+"分")
                self.root.destroy()

        tk.Button(frame,text="交卷",bg="red", width=30,height=2,font=_ft(14,True),relief=tk.FLAT,command=lambda:submit()).pack(side=tk.RIGHT,fill=tk.BOTH, padx=10)


        frame.propagate(False)
        return frame
    def main_left(self, parent):
        def label(frame, text, size=10, bold=False, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

        frame = tk.Frame(parent, width=280, bg="whitesmoke")
        f3 = tk.Frame(frame, bg="white")
        label(f3, "试卷信息", 12, True, "whitesmoke").pack(anchor=tk.W, padx=20, pady=10)
        f3.pack(fill=tk.X, pady=5)

        f1 = tk.Frame(frame, bg="white")
        label(f1, "试卷编号", 12).pack(side=tk.LEFT, fill=tk.Y, anchor=tk.W, padx=30, pady=5)
        v_seperator(f1, 10, "whitesmoke").pack(fill=tk.Y, side=tk.LEFT, )
        label(f1, "无").pack(side=tk.LEFT, anchor=tk.W, padx=30, pady=5)
        f1.pack(fill=tk.X, pady=5)

        f2 = tk.Frame(frame, bg="white")
        label(f2, "考试成绩", 12).pack(side=tk.LEFT, fill=tk.Y, anchor=tk.W, padx=30, pady=5)
        v_seperator(f2, 10, "whitesmoke").pack(fill=tk.Y, side=tk.LEFT, )
        self.score_label = label(f2, "")
        self.score_label.pack(side=tk.LEFT, anchor=tk.W, padx=30, pady=5)
        f2.pack(fill=tk.X, pady=5)
        self.set_string(self.score_label,"0")

        h_seperator(frame, 10)
        self.main_left_tihao(frame)

        frame.propagate(False)
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
                btn["command"] = lambda x=k:self.change_ti_button_click(x)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.btns.append(btn)
            btn_frame.pack(fill=tk.X)
    def pack_main_right(self,is_put_result):
        self.main_right_type.forget()
        self.main_right_timu.forget()
        for xx in self.main_right_xx:
            xx.forget()
        self.main_right_last_next_btns.forget()
        self.main_right_result.forget()

        self.main_right_type.pack(anchor=tk.W, padx=20, pady=5)
        self.main_right_timu.pack(padx=20, pady=5, fill=tk.X)
        ti = self.exam[self.index-1]
        for i in range(len(ti["select"])):
            self.main_right_xx[i].pack(anchor=tk.W, padx=20, pady=5)
        if is_put_result:
            self.main_right_result.pack(fill=tk.X)
        self.main_right_last_next_btns.pack(anchor=tk.W, side=tk.TOP)
    def refresh_main_right_content(self):#一种是点击了上一题和下一题，一种是点击了题号
        # 题型
        ti = self.exam[self.index-1]
        self.set_string(self.main_right_type,ti["type"])
        # 题目
        self.set_string(self.main_right_timu,str(self.index) + "、" + ti["content"])
        # 选项
        for i, xx_string in enumerate(ti["select"]):
            self.set_string(self.main_right_xx[i],chr(i + 65) + "、" + xx_string)
        #结果
        is_put_result = False
        if self.is_done():
            self.btns[self.index - 1]["bg"] = "gray"
            self.set_string(self.main_right_result, "您选择的答案是：  " + chr(self.user_anwser[self.index-1]+65))
            is_put_result = True
        self.pack_main_right(is_put_result)

    def xx_button(self, frame, size, i=0, bold=False, width=200):
        def xx_button_click(k):
            self.user_anwser[self.index-1] = k
            self.refresh_main_right_content()
        btn = tk.Button(frame, bg="whitesmoke", fg="black", width=width, height=1, font=_ft(size, bold),
                        command=lambda x=i:xx_button_click(x), anchor=tk.NW, padx=10, relief=tk.FLAT)
        return btn

    def main_right(self, parent):
        frame = tk.Frame(parent,bg="white",width=200)

        #点击上一题
        def click_last_ti():
            if self.index == 1:
                return
            self.index -= 1
            self.refresh_main_right_content()
        #点击下一题
        def click_next_ti():
            if self.index == len(self.exam):
                return
            self.index += 1
            self.refresh_main_right_content()

        self.main_right_type = tk.Label(frame, bg="white", fg="green", font=_ft(12, True), padx=10, pady=10, anchor=tk.NW)
        self.main_right_timu = tk.Message(frame, bg="white",width=750, font=_font(size=14), anchor=tk.NW, padx=10)
        self.main_right_xx = [self.xx_button(frame, 14, i) for i in range(4)]
        self.main_right_last_next_btns = tk.Frame(frame, bg="white")
        tk.Button(self.main_right_last_next_btns, text="上一题", font=_font(size=14), padx=5, bg="whitesmoke",
                             command=lambda :click_last_ti()).pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=10)
        tk.Button(self.main_right_last_next_btns, text="下一题", font=_font(size=14), padx=5, bg="whitesmoke",
                             command=lambda :click_next_ti()).pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=10)
        self.main_right_result = tk.Message(frame, width=750, font=_font(size=14), anchor=tk.NW, padx=30, pady=20, bg="white")

        #设置当前的题和标号为第一道题
        self.index = 1
        self.refresh_main_right_content()
        return frame





