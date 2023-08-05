
import time
import tkinter as tk
from tkinter import ttk,messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
import json
import random

def center_window(win, width=None, height=None):
    """ 将窗口屏幕居中 """
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    if width is None:
        width, height = get_window_size(win)[:2]
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 3)
    win.geometry(size)


def get_window_size(win, update=True):
    """ 获得窗体的尺寸 """
    if update:
        win.update()
    return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()


def tkimg_resized(img, w_box, h_box, keep_ratio=True):
    """对图片进行按比例缩放处理"""
    w, h = img.size

    if keep_ratio:
        if w > h:
            width = w_box
            height = int(h_box * (1.0 * h / w))

        if h >= w:
            height = h_box
            width = int(w_box * (1.0 * w / h))
    else:
        width = w_box
        height = h_box

    img1 = img.resize((width, height), Image.ANTIALIAS)
    tkimg = ImageTk.PhotoImage(img1)
    return tkimg


def image_label(frame, img, width, height, keep_ratio=True):
    """输入图片信息，及尺寸，返回界面组件"""
    if isinstance(img, str):
        _img = Image.open(img)
    else:
        _img = img
    lbl_image = tk.Label(frame, width=width, height=height)

    tk_img = tkimg_resized(_img, width, height, keep_ratio)
    lbl_image.image = tk_img
    lbl_image.config(image=tk_img)
    return lbl_image


def _font(fname="微软雅黑", size=12, bold=tkFont.NORMAL):
    """设置字体"""
    ft = tkFont.Font(family=fname, size=size, weight=bold)
    return ft


def _ft(size=12, bold=False):
    """极简字体设置函数"""
    if bold:
        return _font(size=size, bold=tkFont.BOLD)
    else:
        return _font(size=size, bold=tkFont.NORMAL)


def h_seperator(parent, height=2):  # height 单位为像素值
    """水平分割线, 水平填充 """
    tk.Frame(parent, height=height, bg="whitesmoke").pack(fill=tk.X)


def v_seperator(parent, width, bg="whitesmoke"):  # width 单位为像素值
    """垂直分割线 , fill=tk.Y, 但如何定位不确定，直接返回对象，由容器决定 """
    frame = tk.Frame(parent, width=width, bg=bg)
    return frame


import global_variable
def get_exam_and_done(find_ti_type=0):
    #错题
    # find_ti_type = 0#-1表示没做的，0表示错误的，1表示正确
    exam_path = global_variable.data_path
    exam_done_path = global_variable.exam_path

    with open(exam_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    with open(exam_done_path, encoding='utf-8') as f:
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



class Frame_Ti(tk.Frame):
    def __init__(self, master,exam,user_anwser):
        super().__init__(master)
        self.ti = []
        self.user_anwser = user_anwser
        self.index = 1
        self.exam = exam
        self.btns = []

        self.type = tk.Label(self,bg="white", fg="green",font=_ft(12, True),padx=10,pady=10,anchor=tk.NW)
        self.type_string = tk.StringVar()
        self.timu = tk.Message(self,width=750,font=_font(size=14),anchor=tk.NW,padx=10)
        self.timu_string = tk.StringVar()
        self.xx = [self.button(self, 14, False, i) for i in range(4)]
        self.xx_string = [tk.StringVar() for i in range(4)]

        self.result = tk.Message(self,width=750,font=_font(size=14),anchor=tk.NW,padx=30,pady=20,bg="white")
        self.result_string = tk.StringVar()
        self.timu["textvariable"] = self.timu_string

        self.last_next_btns = tk.Frame(self, bg="white")
        self.last_btn = tk.Button(self.last_next_btns, text="上一题", font=_font(size=14), padx=5, bg="whitesmoke",
                                  command=self.last_ti).pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=10)
        self.next_btn = tk.Button(self.last_next_btns, text="下一题", font=_font(size=14), padx=5, bg="whitesmoke",
                                  command=self.next_ti).pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=10)

    def last_ti(self):
        if self.index == 1:
            return
        self.index -= 1
        self.refresh(self.index,self.exam[self.index-1])

    def next_ti(self):
        if self.index == len(self.exam):
            return
        self.index += 1
        self.refresh(self.index, self.exam[self.index-1])



    def button(self, frame, size,bold=False, i=0,width=200):
        btn = tk.Button(frame, bg="whitesmoke", fg="black", width=width, height=1, font=_ft(size, bold),anchor=tk.NW,padx=10,relief=tk.FLAT,state="disabled")
        return btn
    def refresh(self, index, ti,btns=None):#这个refresh做win_random里click的工作
        self.index = index
        self.ti = ti
        if btns:
            self.btns = btns

        #全部forget一下
        for xx in self.xx:
            xx.forget()
        self.result.forget()

        # 题型
        self.type_string.set(self.ti["type"])
        self.type["textvariable"] = self.type_string
        self.type["bg"] = "white"
        self.type.pack(anchor=tk.W, padx=20, pady=5)
        # 题目
        self.timu_string.set(str(self.index) + "、" + self.ti["content"])
        self.timu["bg"] = "white"
        self.timu.pack(padx=20, pady=5,fill=tk.X)
        # 选项
        for i, xx_string in enumerate(self.ti["select"]):
            xx = self.xx[i]
            self.xx_string[i].set(chr(i + 65) + "、" + self.ti["select"][i])
            xx["textvariable"] = self.xx_string[i]
            xx.pack(anchor=tk.W, padx=20, pady=5)

        #展示结果
        # print("inedx",index)
        # print(len(self.user_anwser))
        if self.ti["anwser"] == chr(self.user_anwser[self.index-1] + 65):
            self.result["fg"] = "green"
            result_string = "回答正确，正确答案:"+self.ti["anwser"]
        else:
            self.result["fg"] = "red"
            result_string = "回答错误，正确答案:" + self.ti["anwser"]
        if self.ti["anwser_explan"]!="":
            result_string = result_string+"\n答案解析："+self.ti["anwser_explan"]
        self.result_string.set(result_string)
        self.result["textvariable"] = self.result_string
        self.result.pack(fill=tk.X,side=tk.TOP)

        self.last_next_btns.forget()
        self.last_next_btns.pack(anchor=tk.W, side=tk.TOP)

class Window:
    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.parent = parent
        self.frame_ti = None
        self.find_ti_type = 0

        self.user_anwser, self.exam =get_exam_and_done(self.find_ti_type)
        self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
        center_window(self.root)  # 将窗体移动到屏幕中央
        self.root.title("危险化学品经营考试")  # 窗体标题
        self.root.iconbitmap("images\\Money.ico")  # 窗体图标
        # self.root.grab_set()
        self.btns = None


        self.main_left_frame = None
        self.bottom_frame = None
        self.main_frame = None
        self.v_seperator_frame = None
        self.main_right_frame = None


        self.body()  # 绘制窗体组件

    # 绘制窗体组件
    def body(self):
        self.title(self.root).pack(fill=tk.X)

        self.main_frame = self.main(self.root)
        self.main_frame.pack(expand=tk.YES, fill=tk.BOTH)

        self.bottom_frame = self.bottom(self.root)
        self.bottom_frame.pack(fill=tk.X)

    def title(self, parent):
        """ 标题栏 """

        def label(frame, text, size, bold=False):
            return tk.Label(frame, text=text, bg="black", fg="white", height=2, font=_ft(size, bold))

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

        self.main_top(frame).pack(fill=tk.X, padx=30, pady=15)

        # self.main_middle_frame = tk.Frame(frame,bg="red",height=200)

        self.main_left_frame =self.main_left(frame)
        self.main_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=30)

        self.v_seperator_frame = v_seperator(frame, 30)
        self.v_seperator_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_right_frame = self.main_right(frame)
        self.main_right_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        # self.main_middle_frame.pack(fill=tk.X)
        frame.propagate(True)

        return frame

    def change_ti_type(self,i):

        self.find_ti_type = i
        self.user_anwser, self.exam = get_exam_and_done(self.find_ti_type)
        print(len(self.exam))
        self.main_left_frame.destroy()
        self.main_right_frame.destroy()
        self.bottom_frame.forget()
        self.v_seperator_frame.forget()

        self.main_left_frame = self.main_left(self.main_frame)
        self.main_right_frame = self.main_right(self.main_frame)

        self.main_left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=30)
        self.v_seperator_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_right_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)
        self.bottom_frame.pack(fill=tk.X)

        self.frame_ti.refresh(1, self.exam[0])

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

    def main_top_middle(self, parent):
        str1 = "定制图像分类模型，可以识别一张图整体是什么物体/状态/场景。"
        str2 = "在各分类图片之间差异明显的情况下，训练数据每类仅需20-100张，最快10分钟可训练完毕"

        def label(frame, text):
            return tk.Label(frame, bg="white", fg="gray", text=text, font=_ft(12))

        frame = tk.Frame(parent, bg="white")

        self.main_top_middle_top(frame).pack(anchor=tk.NW)

        label(frame, str1).pack(anchor=tk.W, padx=10, pady=2)
        label(frame, str2).pack(anchor=tk.W, padx=10)

        return frame

    def main_top_middle_top(self, parent):
        def label(frame, text, size=12, bold=True, fg="blue"):
            return tk.Label(frame, text=text, bg="white", fg=fg, font=_ft(size, bold))

        frame = tk.Frame(parent, bg="white")

        label(frame, "图像分类模型", 20, True, "black").pack(side=tk.LEFT, padx=10)
        label(frame, "操作文档").pack(side=tk.LEFT, padx=10)
        label(frame, "教学视频").pack(side=tk.LEFT, padx=10)
        label(frame, "常见问题").pack(side=tk.LEFT, padx=10)

        return frame

    def main_left(self, parent):
        def label(frame, text, size=10, bold=False, bg="white"):
            return tk.Label(frame, text=text, bg=bg, font=_ft(size, bold))

        def button(frame, text, size, bold=False):
            btn = tk.Button(frame, text=text, bg="#d3d7d4", fg="black", width=2, height=1, font=_ft(size, bold))
            btn.config(relief=tk.FLAT)
            return btn

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

        score_label = label(f2, "")
        score_label.pack(side=tk.LEFT, anchor=tk.W, padx=30, pady=5)
        sv = tk.StringVar()
        sv.set("0")
        score_label["textvariable"] = sv
        f2.pack(fill=tk.X, pady=5)
        self.score_label = score_label


        h_seperator(frame, 10)
        self.Frame_Tihao(frame)

        frame.propagate(False)
        return frame

    def Frame_Tihao(self, parent):
        def button(frame, text, size, bold=False):
            btn = tk.Button(frame, text=text, bg="#d3d7d4", fg="black", width=2,height=1, font=_ft(size, bold))
            btn.config(relief=tk.FLAT)
            return btn

        self.btns = []
        btn_frames = []
        last_btns = []
        next_btns = []
        def refresh_tihao(i,j):
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
                refresh_tihao((i-1)*10,i*10)
        def next_btn_click(i):
            totol_ye = ceil(len(btn_frames) / 10)
            if i+1 == totol_ye:
                return
            elif i+1 == totol_ye-1:
                refresh_tihao((i+1)*10,len(btn_frames))
            else:
                refresh_tihao((i+1)*10,(i+2)*10)

        for i in range(ceil(len(self.exam) / 10)):
            btn_frame = tk.Frame(parent, bg="white")
            for j in range(10):
                k = i * 10 + j + 1
                if k > len(self.exam):
                    break
                btn = button(btn_frame, k, 8)
                btn["command"] = lambda x=k: self.frame_ti.refresh(x, self.exam[x - 1], self.btns)
                if self.find_ti_type == -1:
                    btn["bg"] = "gray"
                elif self.find_ti_type == 1:
                    btn["bg"] = "green"
                else:
                    btn["bg"] = "red"
                btn.pack(side=tk.LEFT, padx=2, pady=1)
                self.btns.append(btn)

            btn_frames.append(btn_frame)
        for i in range(ceil(len(self.exam) / 100)):
            last_btn = tk.Button(parent, text="上一页", width=15, height=2, command=lambda x=i: last_btn_click(x))
            last_btns.append(last_btn)
            next_btn = tk.Button(parent, text="下一页", width=15, height=2, command=lambda x=i: next_btn_click(x))
            next_btns.append(next_btn)

        # print(len(self.exam))
        # print(len(btn_frames))

        refresh_tihao(0, min(10,len(btn_frames)))

    def main_right(self, parent):
        frame_ti = Frame_Ti(parent,self.exam,self.user_anwser)
        frame_ti["bg"] = "white"
        frame_ti["width"] = 200
        self.frame_ti = frame_ti
        self.frame_ti.refresh(1,self.exam[0],self.btns)
        return frame_ti


