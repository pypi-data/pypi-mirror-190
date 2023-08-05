# coding:utf-8

import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk
import tkutils as tku
import win_random
import win_order
import win_select_exam
import global_variable
import win_wrong
from PIL import Image
class App:
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("%dx%d" % (700, 400))   # 窗体尺寸
		tku.center_window(self.root)               # 将窗体移动到屏幕中央
		self.root.iconbitmap("images\\Money.ico")  # 窗体图标
		self.root.title("做题系统")
		self.root.resizable(False, False)          # 设置窗体不可改变大小
		self.body()

	def body(self):
		# ---------------------------------------------------------------------
		# 背景图片
		# ---------------------------------------------------------------------
		self.img = ImageTk.PhotoImage(file="images/bg2.jpg")
		canvas = tk.Canvas(self.root, width=720, height=420)
		canvas.create_image(300, 200, image=self.img)
		canvas.pack(expand=tk.YES, fill=tk.BOTH)

		# ---------------------------------------------------------------------
		# 标题栏
		# ---------------------------------------------------------------------
		f1 = tk.Frame(canvas)
		ft1 = tkFont.Font(family="微软雅黑", size=24, weight=tkFont.BOLD)
		tk.Label(f1, text="做题系统", height=2, fg="white", font=ft1, bg="Teal")\
			.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
		f1.pack(fill=tk.X)

		# ---------------------------------------------------------------------
		# 功能按钮组
		# ---------------------------------------------------------------------



		ft2 = tkFont.Font(family="微软雅黑", size=14, weight=tkFont.BOLD)
		# f1 = tk.Canvas(canvas,width=100,height=50)
		# f1.create_image(100, 50, image=ImageTk.PhotoImage(file=r"images\study.bmp"))
		# f2 = tk.Canvas(canvas)
		# f2.create_image(100, 50, image=ImageTk.PhotoImage(file=r"images\alpha.png"))

		tk.Button(canvas, text="模拟考试", command=self.show_random, font=ft2, height=20, fg="white", width=12)\
			.pack(side=tk.LEFT,expand=tk.YES ,anchor=tk.CENTER)
		tk.Button(canvas, text="顺序做题", command=self.show_order, font=ft2, height=2, fg="white", width=12)\
			.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.CENTER)
		tk.Button(canvas, text="错题集", bg="cadetblue", command=self.show_wrong, font=ft2, height=2, fg="white",width=12) \
			.pack(side=tk.LEFT, expand=tk.YES, anchor=tk.CENTER, padx=5,pady=5)
		tk.Button(canvas, text="已做试卷", bg="cadetblue", command=self.show_select_exam, font=ft2, height=2, fg="white", width=12)\
			.pack(side=tk.RIGHT, expand=tk.YES, anchor=tk.CENTER, padx=5)
		# f1.pack(side = tk.TOP,padx=20,pady=30)
		# f2.pack(side = tk.TOP,padx=20,pady=10)


	def show_title(self, *args):
		self.root.overrideredirect(self.no_title)
		self.no_title = not self.no_title

	def show_random(self):
		win_random.Window(self.root)

	def show_order(self):
		win_order.Window(self.root)

	def show_wrong(self):
		win_wrong.Window(self.root)

	def show_select_exam(self):
		win_select_exam.Window(self.root)



if __name__ == "__main__":
	app = App()
	app.root.mainloop()
