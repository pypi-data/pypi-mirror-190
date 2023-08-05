import shutil
import pyautogui as gui
from autocad_txt_parse import Tool
from WinowsPoint import WindowsPoint
import os
import time

SUBFIX = '.DWG'
CAD_PATHS = r"C:\Users\wmj\Desktop\炔化加氢轴测图0706\ISO"
ROOT_DIR = r"C:\Users\wmj\Desktop\dad1\cads_result"
PK_SAVE_DIR = os.path.join(ROOT_DIR, "all_pk")
EXCEL_SAVE_PATH = os.path.join(ROOT_DIR, "汇总表.xlsx")


class CADArtificialOperation:
    @classmethod
    def operate_deopen(cls):
        # 炸开
        gui.hotkey('ctrl', 'a')
        gui.hotkey('x')
        gui.hotkey('enter')
        gui.hotkey('ctrl', 's')

    @classmethod
    def operate_delete(cls):
        # 删除 其他图层
        sleep_time = 1

        time.sleep(sleep_time)
        gui.hotkey('q')
        gui.hotkey('shift', '_')
        gui.hotkey('s')
        gui.hotkey('e')
        gui.hotkey('l')
        gui.hotkey('e')
        gui.hotkey('c')
        gui.hotkey('t')
        gui.hotkey('enter')
        time.sleep(sleep_time)

        gui.moveTo(950, 380)  # 图层
        time.sleep(sleep_time)
        gui.leftClick()
        gui.moveTo(950, 380)  # 图层 来两次
        time.sleep(sleep_time)
        gui.leftClick()

        gui.moveTo(950, 570)  # 不等于
        time.sleep(sleep_time)
        gui.leftClick()
        time.sleep(sleep_time / 2)

        gui.moveTo(950, 600)  # 不等于
        time.sleep(sleep_time)
        gui.leftClick()
        time.sleep(sleep_time / 2)

        gui.moveTo(950, 600)  # iso_auto
        time.sleep(sleep_time)
        gui.leftClick()
        time.sleep(sleep_time)
        gui.hotkey('i')
        # gui.hotkey('s')
        # gui.hotkey('o')
        # gui.hotkey('shift','_')
        # gui.hotkey('a')
        # gui.hotkey('u')
        time.sleep(sleep_time)
        gui.hotkey('enter')  # select iso_auto
        time.sleep(sleep_time)

        gui.hotkey('enter')
        time.sleep(sleep_time * 2)  # ok

        # focus
        gui.moveTo(950, 10)  # iso_auto
        gui.leftClick()

        gui.hotkey('delete')
        time.sleep(sleep_time)
        gui.hotkey('ctrl', 's')


# 保存bbox 和 down_text,没有炸开（right_up_text需要炸开才能提取）
def save_down_texts_and_bboxes():
    g = os.walk(CAD_PATHS)
    for path, dirs, files in g:
        files = [file for file in files if file[-4:] == SUBFIX]
        for k, file in enumerate(files):
            if file[-4:] == SUBFIX:
                start_time = time.time()
                print(f"Try to get {file}")

                # bbox
                bbox_name = os.path.basename(file)[:-4] + "_bbox"
                bbox_save_path = os.path.join(PK_SAVE_DIR, bbox_name + '.pk')

                # down text
                down_text_name = os.path.basename(file)[:-4] + "_down_text"
                down_text_path = os.path.join(PK_SAVE_DIR, down_text_name + '.pk')

                if os.path.exists(bbox_save_path) and os.path.exists(down_text_path):
                    continue

                cad_path = os.path.join(path, file)
                os.startfile(cad_path)  # 双击打开cad文件
                tool = Tool(root=ROOT_DIR)

                # 保存
                while (True):
                    try:
                        time.sleep(3)
                        if not os.path.exists(bbox_save_path):
                            tool.get_objs(obj_name=bbox_name, exec_func=tool._get_bbox_from_autocad)

                        if not os.path.exists(down_text_path):
                            tool.get_objs(obj_name=down_text_name, exec_func=tool._get_text_from_autocad)
                        break
                    except Exception as e:
                        print(e)

                end_time = time.time()
                print(f"耗时：{end_time - start_time} s \n总计：{len(files)},now:{k + 1}")

# save_ru_texts 后 cad文件会修改，save_down_text_and_bbox 会不可用
def save_ru_texts():
    g = os.walk(CAD_PATHS)
    wp = WindowsPoint()
    for path, dirs, files in g:
        files = [file for file in files if file[-4:] == SUBFIX]
        for k, file in enumerate(files):
            if file[-4:] == SUBFIX:
                start_time = time.time()
                print(f"Try to get {file}")
                # text
                ru_text_name = os.path.basename(file)[:-4] + "_ru_text"
                ru_text_path = os.path.join(PK_SAVE_DIR, ru_text_name + '.pk')

                if os.path.exists(ru_text_path):
                    continue

                cad_path = os.path.join(path, file)
                os.startfile(cad_path)
                tool = Tool(root=ROOT_DIR)

                while (True):
                    try:
                        time.sleep(3)
                        tool.open_cad()  # 先保证正常开启，然后再进行鼠标操作
                        break
                    except Exception as e:
                        print(e)

                while (True):
                    try:
                        wp.focus_windows(wp.get_hwnd([os.path.basename(file)[:-4], "Autodesk"]))
                        time.sleep(1)
                        CADArtificialOperation.operate_deopen()
                        time.sleep(3)
                        tool.open_cad()
                        break
                    except Exception as e:
                        print(e)

                CADArtificialOperation.operate_delete() #删除非ISO_AUTO图层类型的对象
                time.sleep(2)

                # 提取对象
                while (True):
                    try:
                        tool.open_cad()
                        tool.get_objs(obj_name=ru_text_name, exec_func=tool._get_text_from_autocad)
                        break
                    except Exception as e:
                        print(e)

                end_time = time.time()
                print(f"耗时：{end_time - start_time} s \n总计：{len(files)},now:{k + 1}")
                # exit()


def extract_from_pks():
    g = os.walk(PK_SAVE_DIR)
    file_names = []
    for path, dirs, files in g:
        content_str = "_ru_text"
        file_names.extend([file[:file.find(content_str)] for file in files if content_str in file])
    tool = Tool(ROOT_DIR)
    tool.run_all(file_names)


# 先把down_text,ru_text和bbox从CAD提取出来，然后去解析
# extract_from_pks解析

# save_down_texts_and_bboxes()  # 保证autocad是打开状态，显示代理关闭
# save_ru_texts() # 保证autocad是打开状态，显示代理关闭，输入法为英语(美国)或者英语(英国）
extract_from_pks()
