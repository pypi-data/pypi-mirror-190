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


def get_exam(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.loads(f.read())
    random_index = [random.randint(1,len(data)) for i in range(100)]
    random_data = [data[i-1] for i in random_index]
    return random_data,random_index


class Frame_Ti(tk.Frame):
    def __init__(self, master,exam):
        super().__init__(master)
        self.ti = []
        self.user_anwser = [-1 for i in range(100)]  #0表示A,1表示B，2表示C，3表示D，-1为未选择
        self.index = 1
        self.exam = exam
        self.btns = []
        self.score_label = None

        self.type = tk.Label(self,bg="white", fg="green",font=_ft(12, True),padx=10,pady=10,anchor=tk.NW)
        self.type_string = tk.StringVar()
        self.timu = tk.Message(self,width=750,font=_font(size=14),anchor=tk.NW,padx=10)
        self.timu_string = tk.StringVar()
        self.xx = [self.button(self, 14, False, i) for i in range(4)]
        self.xx_string = [tk.StringVar() for i in range(4)]

        self.last_next_btns = tk.Frame(self,bg="white")
        self.last_btn = tk.Button(self.last_next_btns, text="上一题", font=_font(size=14), padx=5, bg="whitesmoke",
                                  command=self.last_ti).pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=10)
        self.next_btn = tk.Button(self.last_next_btns, text="下一题", font=_font(size=14), padx=5, bg="whitesmoke",
                                  command=self.next_ti).pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=10)



        self.result = tk.Message(self,width=750,font=_font(size=14),anchor=tk.NW,padx=30,pady=20,bg="white")
        self.result_string = tk.StringVar()
        self.timu["textvariable"] = self.timu_string



    def last_ti(self):
        if self.index == 1:
            return
        self.index -= 1
        self.refresh(self.index,self.exam[self.index-1])

    def next_ti(self):
        if self.index == 100:
            return
        self.index += 1
        self.refresh(self.index, self.exam[self.index-1])
    def is_finish(self):
        if min(self.user_anwser) >= 0:
            return True
        else:
            return False
    def calculate_score(self):
        score = 0
        for i in range(100):
            user_anwser = chr(self.user_anwser[i] + 65)
            anwser = self.exam[i]["anwser"]
            if user_anwser == anwser:
                score += 1
        return score


    def click(self, i):#-1表示已经选过了，变换btn的颜色，更新得分
        result_string = ""
        if i == -1:
            i = self.user_anwser[self.index-1] #用户答案
        else:
            self.user_anwser[self.index-1] = i
        for xx in self.xx:#题目的选项禁用
            xx["state"] = 'disabled'

        #更新分数
        score = self.calculate_score()
        sv = tk.StringVar()
        sv.set(str(score))
        self.score_label["textvariable"] = sv



        if self.ti["anwser"] == chr(i + 65):
            self.result["fg"] = "green"
            result_string = "回答正确,正确答案:"+self.ti["anwser"]
            self.btns[self.index-1]["bg"] = "green"  # 已经做过了
        else:
            self.result["fg"] = "red"
            result_string = "回答错误,正确答案:" + self.ti["anwser"]
            self.btns[self.index-1]["bg"] = "red"  # 已经做过了
        if self.ti["anwser_explan"]!="":
            result_string = result_string+"\n答案解析："+self.ti["anwser_explan"]
        self.result_string.set(result_string)
        self.result["textvariable"] = self.result_string
        self.result.pack(fill=tk.X)
        self.last_next_btns.forget()
        self.last_next_btns.pack(anchor=tk.W,side=tk.TOP)

    def button(self, frame, size,bold=False, i=0,width=200):
        btn = tk.Button(frame, bg="whitesmoke", fg="black", width=width, height=1, font=_ft(size, bold),command=lambda x=i: self.click(x),anchor=tk.NW,padx=10,relief=tk.FLAT)
        return btn
    def refresh(self, index, ti,btns=None,score_label=None):
        self.index = index
        self.ti = ti
        if btns:
            self.btns = btns
        if score_label:
            self.score_label = score_label


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
        for xx in self.xx:
            xx.forget()
        for i, xx_string in enumerate(self.ti["select"]):
            xx = self.xx[i]
            self.xx_string[i].set(chr(i + 65) + "、" + self.ti["select"][i])
            xx["textvariable"] = self.xx_string[i]
            xx.pack(anchor=tk.W, padx=20, pady=5)

        if self.user_anwser[self.index-1] >= 0:
            self.click(-1)
        else:
            for xx in self.xx:
                xx["state"] = "normal"
        #上一题、下一题
        # self.last_btn.forget()
        # self.next_btn.forget
        # self.last_btn.pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=0)
        # self.next_btn.pack(side=tk.LEFT, anchor=tk.NW, padx=0, pady=0)
        self.last_next_btns.forget()
        self.last_next_btns.pack(anchor=tk.W,side=tk.TOP)



class Window:
    def __init__(self,parent):
        self.root = tk.Toplevel()
        self.parent = parent
        self.frame_ti = None
        self.exam,self.tihao = get_exam(r"data\data.json")
        self.root.geometry("%dx%d" % (1200, 800))  # 窗体尺寸
        center_window(self.root)  # 将窗体移动到屏幕中央
        self.root.title("危险化学品经营考试")  # 窗体标题
        self.root.iconbitmap("images\\Money.ico")  # 窗体图标
        # self.root.grab_set()
        self.body()  # 绘制窗体组件
        self.score_label = None
        self.btns = []

    # 绘制窗体组件
    def body(self):
        self.title(self.root).pack(fill=tk.X)

        self.main(self.root).pack(expand=tk.YES, fill=tk.BOTH)

        self.bottom(self.root).pack(fill=tk.X)

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
        self.main_left(frame).pack(side=tk.LEFT, fill=tk.Y, padx=30)
        v_seperator(frame, 30).pack(side=tk.RIGHT, fill=tk.Y)
        self.main_right(frame).pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

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
            if self.frame_ti.is_finish():
                message = "您已完成所有问题，确定交卷？"
            else:
                message = "还有问题没有做答，确定交卷？"
            is_submit = messagebox.askokcancel(title='交卷提示', message=message)
            if is_submit:
                # 计算得分
                score = self.frame_ti.calculate_score()

                #把试卷答案存下来。
                exam_path = r"data\exam.json"
                from os.path import exists
                id = 1
                data = []
                if exists(exam_path):
                    with open(exam_path,encoding='utf-8') as f:
                        data = json.loads(f.read())
                    if not data and len(data)>0:
                        id = max([d["exam_id"] for d in data])+1
                else:
                    data = []
                    id = 1
                item ={
                    "exam_id":id,
                    "tihao":self.tihao,
                    "user_anwser":self.frame_ti.user_anwser,
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
        v_seperator(f2, 10, "whitesmoke").pack(fill=tk.Y, side=tk.LEFT, )
        score_label = label(f2, "")
        score_label.pack(side=tk.LEFT, anchor=tk.W, padx=30, pady=5)
        sv = tk.StringVar()
        sv.set("0")
        score_label["textvariable"] = sv
        f2.pack(fill=tk.X, pady=5)
        self.score_label = score_label


        h_seperator(frame, 10)
        self.Frame_Tihao(frame,score_label)

        frame.propagate(False)
        return frame

    def Frame_Tihao(self, parent,score_label):
        def button(frame, text, size, bold=False):
            btn = tk.Button(frame, text=text, bg="#d3d7d4", fg="black", width=2, height=1, font=_ft(size, bold))
            btn.config(relief=tk.FLAT)
            return btn
        self.btns = []
        for i in range(10):
            btn_frame = tk.Frame(parent, bg="white")
            for j in range(10):
                k = i * 10 + j + 1
                btn = button(btn_frame, k, 8)
                btn["command"] = lambda x=k: self.frame_ti.refresh(x, self.exam[x-1],self.btns,score_label)
                btn.pack(side=tk.LEFT, padx=2, pady=2)
                self.btns.append(btn)
            btn_frame.pack(fill=tk.X)


    def main_right(self, parent):
        frame_ti = Frame_Ti(parent,self.exam)
        frame_ti["bg"] = "white"
        frame_ti["width"] = 200
        self.frame_ti = frame_ti
        self.frame_ti.refresh(1,self.exam[0],self.btns,self.score_label)
        return frame_ti


