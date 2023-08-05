import pyautogui as gui
import time
import os
import sys
import xlrd  #读取xls
import openpyxl #excel 不能读取xls
from pynput.keyboard import Controller
import win32gui

keyboard = Controller()

# DATA_PATH=  os.path.join(r"C:\Users\wmj\Desktop\daka","daka.xls")    #需要打卡的文件路径
# EXCEPTION_PATH = os.path.join(r"C:\Users\wmj\Desktop\daka","except.xlsx")  #无需打卡名单的文件路径
DATA_PATH=  os.path.join(sys.path[0],"daka.xls")    #需要打卡的文件路径
EXCEPTION_PATH = os.path.join(sys.path[0],"except.xlsx")  #无需打卡名单的文件路径
GROUP_QQ_NAME = {'2019':'2019计算机研究生','2020':'2020计算机研究生'}


def get_exception_names(nianji):
    path = EXCEPTION_PATH
    names = []
    wb = openpyxl.load_workbook(path)
    sheet = wb[nianji]
    names_col = sheet['A']
    for cell in names_col:
        name = cell.value
        names.append(name)
    return names

def remove_names(names,nianji):
    except_names = get_exception_names(nianji)
    names.extend(except_names)
    names = list(set(names))
    for i in except_names:
        names.remove(i)
    return names

def get_daka_names_standard(path,nianji=None):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_name("sheet")
    list_2019 = []
    list_2020 = []
    list_2021 = []
    list_phd = []

    #找到对应列
    id_col_num = 0   #学号列
    name_col_num = 1 #姓名列
    type_col_num = 3 #学生类别列
    for i,first_row_data in enumerate(sheet.row_values(0)):
        if  first_row_data == '学号':
            id_col_num = i
        elif first_row_data == '姓名':
            name_col_num = i
        elif first_row_data == '学生类别':
            type_col_num = i

    for i,(type_value,id_value) in enumerate(zip(sheet.col_values(type_col_num),sheet.col_values(id_col_num))):
        if str(type_value).find('博士') >= 0 or str(type_value).find('直博') >= 0:
            list_phd.append(sheet.cell_value(i,name_col_num))
        elif str(id_value)[:4] == '2019':
            list_2019.append(sheet.cell_value(i,name_col_num))
        elif str(id_value)[:4] == '2020':
            list_2020.append(sheet.cell_value(i,name_col_num))
        elif str(id_value)[:4] == '2021':
            list_2021.append(sheet.cell_value(i,name_col_num))
        # else:
        #     print("奇怪的值!")
        #     print(sheet.cell_value(i,id_col_num))
    list_dict = {'2019':list_2019,'2020':list_2020,'2021':list_2021,'博士':list_phd}
    if nianji:
        names = list_dict[nianji]
        names = remove_names(names, nianji)
        return names
    else:
        nianjis = list_dict.keys()
        for nianji in nianjis:
            names = list_dict[nianji]
            names = remove_names(names, nianji)
            list_dict[nianji] = names
    return list_dict

def get_daka_names(path,nianji):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_name(nianji)
    #找姓名列
    row_num = 1
    for i,first_row_data in enumerate(sheet.row_values(0)):
        if  first_row_data == '姓名':
            row_num = i
            break
    names = sheet.col_values(row_num)
    names = names[1:]
    #去除掉不要打卡的名字
    names = remove_names(names,nianji)
    return names
def weixin_daka(names):
    gui.hotkey('ctrl', 'alt', 'w')  # 模拟组合键 打开QQ快捷键
    for user in names:
        str = "@" + user
        keyboard.type(str)
        time.sleep(0.2)
        gui.hotkey('enter')
def qq_daka(names,nianji='2020'):
    # gui.hotkey('ctrl', 'alt', 'z')  # 模拟组合键 打开QQ快捷键
    win32gui.SetForegroundWindow(win32gui.FindWindow("TXGuiFoundation", GROUP_QQ_NAME[nianji]))
    iter_num = 20 # 一轮最多艾特20个
    for i,user in enumerate(names):
        # gui.typewrite(message='@tes')
        iter_num -= 1
        str = "@" + user
        keyboard.type(str)
        time.sleep(0.2)
        gui.hotkey('enter')
        if iter_num <= 0:
            print("总人数：{}，已完成：{}，剩余：{}，输入n终止,其他键继续".format(len(names),i+1,len(names)-1-i))
            a = input()
            if a == 'n':  # 终止
                break
            iter_num = 20
            # gui.hotkey('ctrl', 'alt', 'z')  # 模拟组合键 打开QQ快捷键
            win32gui.SetForegroundWindow(win32gui.FindWindow("TXGuiFoundation", GROUP_QQ_NAME[nianji]))

def main():
    print('''
    Tips:
    {}
    1.默认文件路径为:{}
      默认采用输入的年级表:如2020
      默认姓名列存在,并使用该列全部！
    2.请修改发送方式为Ctrl+Enter!!!!
    3.确认微信或者QQ的聊天框是开启的
    4.微信开启热键为ctrl+alt+w,QQ开启热键为ctrl+alt+z
    5.需要输入：a.打卡方式为QQ还是微信。b.打卡年级(用于排除不打卡的名单）
    {}
    '''.format('*' * 60, DATA_PATH, '*' * 60))
    print('''
    {}
    请选择打卡方式：
    1.QQ
    2.微信
    {}
    '''.format('*' * 60, '*' * 60))
    method_num = input()
    print('''
    {}
    请选择打卡年级：
    1.2019
    2.2020
    3.博士
    {}
    '''.format('*' * 60, '*' * 60))
    nianji_num = input()
    nianji = {'1':'2019','2':'2020','3':'博士'}
    method = {'1':'QQ','2':'微信'}

    print('''
    打卡方式为：{}，打卡年级为：{}
    按任意键继续
    '''.format(method[method_num], nianji[nianji_num]))
    input()
    names = get_daka_names_standard(DATA_PATH,nianji[nianji_num])
    # names = get_daka_names_standard(DATA_PATH)
    if method_num == '1':#QQ
        qq_daka(names,nianji[nianji_num])
    else:
        weixin_daka(names)
    print("打卡人数为：{}".format(len(names)))
    print("打卡结束！！！")

if __name__ == '__main__':
    main()



