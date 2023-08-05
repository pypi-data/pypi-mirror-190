# coding:utf-8
import json
import tkinter
import tkinter as tk
import tkinter.font as tkFont
import tkutils as tku
import json
from win_random import _ft,_font
import win_exam
import global_variable
class Window:
	def __init__(self, parent):
		self.root = tk.Toplevel()
		self.parent = parent
		self.root.geometry("%dx%d" % (800, 700))  # 窗体尺寸
		tku.center_window(self.root)               # 将窗体移动到屏幕中央
		self.root.resizable(False, False)
		self.old_exam = self.get_old_exam()


		self.title().pack(fill=tk.X,side=tk.TOP)
		self.body().pack(fill=tk.BOTH)
	def title(self):
		frame = tk.Frame(self.root,height=2)
		label = tk.Label(frame,text="请选择试卷",height=2,font=_ft(18,True),fg="white",bg="black").pack(side=tk.TOP,fill=tk.BOTH)
		return frame
	#选择试卷
	def select(self,i):
		self.root.destroy()
		win_exam.Window(self.parent,self.old_exam[i]["exam_id"])
	#删除试卷
	def delete(self,i):
		if tk.messagebox.askokcancel(title="提示",message="删除后无法复原，确定删除？"):
			self.old_exam.pop(i)
			with open(global_variable.exam_path,"w") as f:
				json.dump(self.old_exam,indent=1,ensure_ascii=False,fp=f)
			self.root.destroy()


	def body(self):
		# def label(parent,text=""):
		# 	return tk.Label(parent,text=text,font=_ft(12,True),bg="white",height=1,width=16)
		def button(parent,text="",width=14):
			return tk.Button(parent,text=text,font=_ft(12,True),bg="white",height=1,width=width,state="disabled",relief=tk.FLAT)

		frame = tk.Frame(self.root)
		body1 = tk.Frame(frame,bg="whitesmoke")
		body2 = tk.Frame(frame,bg="whitesmoke")
		body3 = tk.Frame(frame,bg="whitesmoke")
		body4 = tk.Frame(frame,bg="whitesmoke")
		body5 = tk.Frame(frame,bg="whitesmoke")

		button(body1,"试卷号",10).pack(side=tk.TOP,fill=tk.X,pady=5,padx=6)
		button(body2,"得分",10).pack(side=tk.TOP,fill=tk.X,pady=5,padx=6)
		button(body3,"时间",20).pack(side=tk.TOP,fill=tk.X,pady=5,padx=6)
		button(body4,"选择").pack(side=tk.TOP,fill=tk.X,pady=5,padx=6)
		button(body5,"删除").pack(side=tk.TOP,fill=tk.X,pady=5,padx=6)


		for i,exam in enumerate(self.old_exam):
			exam_id = exam["exam_id"]
			score = exam["score"]
			time = exam["time"]
			button(body1, str(exam_id)).pack(side=tk.TOP, fill=tk.X, pady=5, padx=6)
			button(body2, str(score)).pack(side=tk.TOP, fill=tk.X, pady=5, padx=6)
			button(body3, time).pack(side=tk.TOP, fill=tk.X, pady=5, padx=6)
			select_btn = button(body4, "选择")
			select_btn["command"] = lambda x=i:self.select(x)
			select_btn["state"] = "normal"
			select_btn.pack(side=tk.TOP, fill=tk.X, pady=5, padx=6)

			delete_btn = button(body5, "删除")
			delete_btn["command"] = lambda x=i: self.delete(x)
			delete_btn["state"] = "normal"
			delete_btn.pack(side=tk.TOP, fill=tk.X, pady=5, padx=6)




		body1.pack(side=tk.LEFT,fill=tk.Y)
		body2.pack(side=tk.LEFT,fill=tk.Y)
		body3.pack(side=tk.LEFT, fill=tk.Y)
		body4.pack(side=tk.LEFT, fill=tk.Y)
		body5.pack(side=tk.LEFT, fill=tk.Y)
		return frame


	def get_old_exam(self):
		exam_path = global_variable.exam_path
		from os.path import exists
		if exists(exam_path):
			with open(exam_path, encoding='utf-8') as f:
				data = json.loads(f.read())
		else:
			data = []
		return data


