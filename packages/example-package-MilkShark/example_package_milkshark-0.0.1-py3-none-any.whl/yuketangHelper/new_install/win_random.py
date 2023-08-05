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
from win import BaseWindow



class Window(BaseWindow):
    def __init__(self,parent):
        super(Window, self).__init__(parent)
        #数据
        self.index = 1
        self.exam, self.tihao = get_radom_exam()
        self.user_anwser = [-1 for i in range(len(self.exam))]  # 0表示A,1表示B，2表示C，3表示D，-1为未选择
        self.body()  # 绘制窗体组件

