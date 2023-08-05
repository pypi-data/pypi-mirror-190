import os
import pickle
import time

import openpyxl
from pyautocad import Autocad
import numpy as np

BIG_TABLE_TITLE = ["编号", "名称及规格", "材料", "标准型号", "数量", "单位", "备注"]
SMALL_TABLE_TITLE = ["编号", "长度", "外径"]
INSTALL_TITLE = ["行", "列", "安装图图号", "本图图号"]

DOWN_TEXT_TITLE = ['介质名称 FLUID DESCRIP.', '操作温度℃ OPE.TEMP.', '压力管道分级 PR. PIPE CL.', '绝热代号 INSU. TYPE',
                   '无损检测 NONDE. TEST', '项目名称 PROJ.',
                   '介质状态 FLUID STATE.', '设计温度℃ DESIGN TEMP.', '试验压力 TEST PRESS.', '绝热厚度mm INSU. THK.',
                   '静电接地 EARTHING',
                   '装置/主项 SUB.',
                   '管道起点 FROM', '操作压力 MPa.G  OP.PRES.', '试压介质 TEST FLUID', '是否防腐 ANTISEP.', '吹扫介质 PURGE FLUID',
                   '管线号 LINE.NO.',
                   '管道终点 TO', '设计压力 MPa.G  DE. PRES.', '泄漏性试验 LEAK TEST', '管道清洗 PIPE CLEANING', '焊后热处理 PWHT',
                   '图号 DWG.NO.']

RU_TEXT_TITLE = ["序号", "名称及规格", "标准号与图号", "材料", "数量", "备注"]

CAD_IMAGE_BOX_AREA = 124740.0
CAD_IMAGE_BOX_LENGTH = 1434.0
CAD_RU_TEXT_COORDINATE = (285, 48, 130, 228)  # x, y, width, height 不能把标题放进去
CAD_DOWN_TEXT_COORDINATE = (25, 5, 260, 24)  # x, y, width, height


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class RectangleArea:
    def __init__(self, point_left_down: Point, point_right_up: Point):
        self.point_left_down = point_left_down
        self.point_right_up = point_right_up


class BoundingBox:
    def __init__(self, point_left_down, point_left_up, point_right_up, point_right_down):
        self.point_left_down = point_left_down
        self.point_left_up = point_left_up
        self.point_right_up = point_right_up
        self.point_right_down = point_right_down


class Text:
    def __init__(self, text_string, point):
        self.point = point
        self.text_string = text_string


class NewText:
    def __init__(self, text_string, point, bbox_pos):
        self.point = point  # relative
        self.text_string = text_string
        self.bbox_pos = bbox_pos


class ObjectDataProcessor:
    def __init__(self, save_path):
        self.save_path = save_path

    def save_obj(self, objs):
        out_put = open(self.save_path, 'wb')
        objs = pickle.dumps(objs)
        out_put.write(objs)
        out_put.close()

    def load_obj(self):
        with open(self.save_path, "rb") as f:
            objs = pickle.load(f)
        return objs


class Tool:
    def __init__(self, root="", pk_dir_name="all_pk", excel_name="汇总表.xlsx"):
        self.root = root
        self.pk_save_dir = os.path.join(root, pk_dir_name)
        self.excel_save_path = os.path.join(root, excel_name)

    def open_cad(self):
        self.acad = Autocad(create_if_not_exists=True)
        self.acad.prompt(f"Hello, Autocad from Python: {self.acad.doc.Name}\n")

    def is_coorinate_match(self, pre, gt):
        if pre <= gt + 1 and pre >= gt - 1:
            return True
        else:
            return False

    def is_image_bbox(self, item):

        area = CAD_IMAGE_BOX_AREA
        length = CAD_IMAGE_BOX_LENGTH
        if self.is_coorinate_match(item.Area, area) and self.is_coorinate_match(item.Length, length):
            return True
        else:
            return False

    def parse_bbox_ordinate(self, item):
        coordinates = item.Coordinates
        point_left_down = Point(coordinates[0], coordinates[1])
        point_right_down = Point(coordinates[2], coordinates[3])
        point_right_up = Point(coordinates[4], coordinates[5])
        point_left_up = Point(coordinates[6], coordinates[7])
        bbox = BoundingBox(point_left_down=point_left_down, point_left_up=point_left_up,
                           point_right_up=point_right_up, point_right_down=point_right_down)
        return bbox

    def _get_bbox_from_autocad(self):
        objs = []
        for item in self.acad.iter_objects('AcDbPolyline'):

            if self.is_image_bbox(item):
                obj = self.parse_bbox_ordinate(item)
                objs.append(obj)
                print(f"\r已保存图像边框个数：{len(objs)}", end="")
        print("")

        return objs

    def _get_text_from_autocad(self):
        objs = []
        for item in self.acad.iter_objects('text'):
            insertion_point = item.InsertionPoint
            text_point = Point(insertion_point[0], insertion_point[1])
            text_string = item.TextString
            text = Text(text_string, text_point)
            objs.append(text)
            print(f"\r已保存text个数：{len(objs)}", end="")
        print("")
        return objs

    def get_objs(self, obj_name, exec_func):
        saved_path = os.path.join(self.pk_save_dir, obj_name + '.pk')
        odp = ObjectDataProcessor(saved_path)
        if os.path.exists(saved_path):
            print(f"{obj_name}存储在{saved_path}，直接读取")
            objs = odp.load_obj()
        else:
            self.open_cad()
            print(f"本地无可用的{obj_name}，正在遍历Autocad读取，请保持文件在Autocad打开")
            objs = exec_func()
            print(f"正在保存{obj_name}到{saved_path}")
            odp.save_obj(objs)
            print("保存成功!")
        return objs

    def is_obj_in_box(self, obj: Text, bbox: BoundingBox):
        point_left_down = bbox.point_left_down
        point_right_up = bbox.point_right_up
        point_obj = obj.point

        if point_obj.x <= point_right_up.x and point_obj.x >= point_left_down.x and point_obj.y <= point_right_up.y and point_obj.y >= point_left_down.y:
            return True
        else:
            return False

    def assign_objs_to_bboxes(self, objs):
        objs_pos = []
        new_objs = []
        for obj in objs:
            for bbox_pos, bbox in enumerate(self.bboxes):
                if self.is_obj_in_box(obj, bbox):
                    objs_pos.append(bbox_pos)
                    new_objs.append(obj)
                    break
        return new_objs, objs_pos

    def _calculate_relative_point(self, text: Text, bbox_pos):
        point = text.point
        bbox = self.bboxes[bbox_pos]
        point_left_down = bbox.point_left_down
        relative_point = Point(point.x - point_left_down.x, point.y - point_left_down.y)
        return relative_point

    def _is_in_area(self, text: NewText, area: RectangleArea):
        point_obj = text.point
        point_right_up = area.point_right_up
        point_left_down = area.point_left_down

        if point_obj.x <= point_right_up.x and point_obj.x >= point_left_down.x and point_obj.y <= point_right_up.y and point_obj.y >= point_left_down.y:
            return True
        else:
            return False

    def extract_correct_pos_texts(self, texts, texts_pos, rec_area):
        real_new_texts = np.zeros([len(self.bboxes), 1]).tolist()
        for text, bbox_pos in zip(texts, texts_pos):
            relative_point = self._calculate_relative_point(text, bbox_pos)
            new_text = NewText(text_string=self._refresh_text_string(text.text_string), point=relative_point,
                               bbox_pos=bbox_pos)
            if self._is_in_area(new_text, rec_area):
                real_new_texts[bbox_pos].append(new_text)
            # else:
            #     print(f"not in area text:{new_text.text_string}")
        real_new_texts = [rnt[1:] for rnt in real_new_texts]
        print(f"real new text:{sum([len(ts) for ts in real_new_texts])}")
        return real_new_texts

    def _refresh_text_string(self, text_string):
        text_string = text_string.replace(r"\Fgbenor.shx,gbcbig.shx;\W0.6600000000;\T1.0000000000;\o\l", "")
        text_string = text_string.replace(r"\Fgbenor.shx,gbcbig.shx;\W0.6090342679;\T1.0000000000;\o\l", "")
        text_string = text_string.replace(r"\Fgbenor.shx,gbcbig.shx;\W0.5895212966;\T1.0000000000;\o\l", "")
        text_string = text_string.replace(r"\f|b0|i0|c1|p0;\W0.6600000000;\T1.0000000000;\o\l", "")
        if '{\W0.' in text_string:
            text_string = text_string[text_string.find(';') + 1:-1]
        return text_string

    def sort_real_new_texts(self, real_new_texts, threshold=2.5):
        # 排序之前，修改坐标，将差距不超过2.5的y改成一样
        temp_sorted_texts = [sorted(rnt, key=lambda i: (-i.point.y, i.point.x)) for rnt in real_new_texts]
        modified_sorted_texts = []
        for texts in temp_sorted_texts:
            # 如果这个图里没有元素，则为空的
            if len(texts) == 0:
                modified_sorted_texts.append([])
                break

            modified_texts = [texts[0]]
            for i in range(1, len(texts)):
                text = texts[i]
                if abs(text.point.y - modified_texts[i - 1].point.y) <= threshold:
                    text.point.y = modified_texts[i - 1].point.y
                modified_texts.append(text)
            modified_sorted_texts.append(modified_texts)
        modified_sorted_texts = [sorted(rnt, key=lambda i: (-i.point.y, i.point.x)) if len(rnt) > 0 else [] for rnt in
                                 modified_sorted_texts]
        return modified_sorted_texts

    def get_ru_all_rows(self, real_new_texts):
        def condition_last_row(index, id, increment, one_image_texts):
            return index + increment == len(one_image_texts)

        def condition_middle_row(index, id, increment, one_image_texts):
            return index + increment < len(one_image_texts) and one_image_texts[index + increment].text_string == str(
                id + 1)

        all_rows = []
        for one_image_texts in real_new_texts:
            rows = []
            id = 1
            index = 0
            increments = [5, 6, 4, 7]
            while index < len(one_image_texts):
                incre = 0
                if one_image_texts[index].text_string != str(id):
                    print("Something wrong")
                else:
                    for increment in increments:
                        incre = increment
                        if condition_last_row(index, id, increment, one_image_texts):
                            row = [text.text_string for text in one_image_texts[index:index + increment]]
                            rows.append(row)
                            id += 1
                            index += incre
                            break
                        elif condition_middle_row(index, id, increment, one_image_texts):
                            row = [text.text_string for text in one_image_texts[index:index + increment]]
                            rows.append(row)
                            id += 1
                            index += incre
                            break
                        else:
                            if increment == increments[-1]:
                                print("increment something wrong")

            all_rows.append(rows)
        return all_rows

    def get_down_all_rows(self, real_new_texts):

        all_rows = []

        for one_image_texts in real_new_texts:
            row_dic = {title: "" for title in DOWN_TEXT_TITLE}
            for i, text in enumerate(one_image_texts):
                if text.text_string not in DOWN_TEXT_TITLE:
                    continue
                if i + 1 == len(one_image_texts):
                    continue
                if one_image_texts[i + 1].text_string not in DOWN_TEXT_TITLE:
                    row_dic[text.text_string] = one_image_texts[i + 1].text_string
            all_rows.append(row_dic)
        return all_rows

    def mitigate_ru_empty(self, all_rows):
        new_all_rows = []
        for i, rows in enumerate(all_rows):
            new_rows = []
            for j, row in enumerate(rows):
                if len(row) == 4:
                    new_row = [row[0], row[1], '', row[2], row[3], '']
                elif len(row) == 7:
                    new_row = [row[0], row[1], row[2], row[4], row[6], '']
                elif len(row) == 5:
                    new_row = [row[0], row[1], row[2], row[3], row[4], '']
                else:
                    new_row = row
                new_rows.append(new_row)
            new_all_rows.append(new_rows)
        return new_all_rows

    def preprocess_bboxes_to_remove_duplicated_bbox(self, bboxes):
        new_bboxes = []
        for bbox in bboxes:
            if not self.is_bbox_in_bboexes(bbox, new_bboxes):
                new_bboxes.append(bbox)
        return new_bboxes

    def is_bbox_in_bboexes(self, bbox, bboxes):
        for b in bboxes:
            if self.is_point_match(bbox.point_left_down, b.point_left_down) and self.is_point_match(bbox.point_right_up,
                                                                                                    b.point_right_up):
                return True
        return False

    def is_point_match(self, p1, p2):
        if self.is_coorinate_match(p1.x, p2.x) and self.is_coorinate_match(p1.y, p2.y):
            return True
        return False

    def run(self): # 老版
        # 保存框
        self.bboxes = self.get_objs("bbox", self._get_bbox_from_autocad)

        # 保存右上角表格
        self.ru_texts = self.get_objs("ru_text", self._get_text_from_autocad)
        print(len(self.ru_texts))
        self.ru_texts, ru_texts_pos = self.assign_objs_to_bboxes(self.ru_texts)
        x, y, width, height = 285, 48, 130, 234
        ru_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        real_ru_new_texts = self.extract_correct_pos_texts(texts=self.ru_texts, texts_pos=ru_texts_pos,
                                                           rec_area=ru_area)
        modified_sorted_texts = self.sort_real_new_texts(real_ru_new_texts)
        all_rows = self.get_ru_all_rows(modified_sorted_texts)
        all_rows = self.mitigate_ru_empty(all_rows)

        # 保存左下角表格
        self.down_texts = self.get_objs("down_text", self._get_text_from_autocad)
        print(len(self.down_texts))
        self.down_texts, down_texts_pos = self.assign_objs_to_bboxes(self.down_texts)
        print(f"down_texts_pos{len(down_texts_pos)}")
        x, y, width, height = 25, 5, 350, 24
        down_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        real_down_new_texts = self.extract_correct_pos_texts(texts=self.down_texts, texts_pos=down_texts_pos,
                                                             rec_area=down_area)
        modified_sorted_texts = self.sort_real_new_texts(real_down_new_texts)
        print([text.text_string for text in modified_sorted_texts[0]])

        all_down_rows = self.get_down_all_rows(modified_sorted_texts)
        print(len(all_down_rows))

        excel_rows = []
        for ru_rows, down_row_dic in zip(all_rows, all_down_rows):
            down_row_list = [down_row_dic[title] for title in DOWN_TEXT_TITLE]
            for i, ru_row in enumerate(ru_rows):
                ru_row.extend(down_row_list)
                excel_row = ru_row
                excel_rows.append(excel_row)

        wb = openpyxl.Workbook()
        ws = wb.active
        title_row = RU_TEXT_TITLE + DOWN_TEXT_TITLE
        ws.append(title_row)

        [ws.append(excel_row) for excel_row in excel_rows]
        wb.save(self.excel_save_path)

        from autofix_excel_column_size import CXlAutofit

        Entity = CXlAutofit()
        Entity.style_excel(self.excel_save_path, "Sheet")

    def _is_correct_deopen(self, file_name):
        # 保存框 清除掉重复的框
        self.bboxes = self.get_objs(f"{file_name}_bbox", self._get_bbox_from_autocad)
        self.bboxes = self.preprocess_bboxes_to_remove_duplicated_bbox(self.bboxes)

        # 分配框
        self.texts = self.get_objs(f"{file_name}_ru_text", self._get_text_from_autocad)
        self.texts, texts_pos = self.assign_objs_to_bboxes(self.texts)

        # 获取ru_text框
        (x, y, width, height) = CAD_RU_TEXT_COORDINATE
        ru_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        real_ru_new_texts = self.extract_correct_pos_texts(texts=self.texts, texts_pos=texts_pos,
                                                           rec_area=ru_area)

        flag = False
        for texts in real_ru_new_texts:
            if len(texts) > 0:
                flag = True
        return flag

    def _is_correct_down_text(self, file_name):
        # 保存框 清除掉重复的框
        self.bboxes = self.get_objs(f"{file_name}_bbox", self._get_bbox_from_autocad)
        self.bboxes = self.preprocess_bboxes_to_remove_duplicated_bbox(self.bboxes)

        # 分配框
        self.texts = self.get_objs(f"{file_name}_down_text", self._get_text_from_autocad)
        self.texts, texts_pos = self.assign_objs_to_bboxes(self.texts)

        if len(self.texts) == 0:
            return False
        return True

        # 获取down_text框
        # (x, y, width, height) = CAD_DOWN_TEXT_COORDINATE
        # down_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        # real_down_new_texts = self.extract_correct_pos_texts(texts=self.texts, texts_pos=texts_pos,
        #                                                      rec_area=down_area)
        #
        # flag = False
        # for texts in real_down_new_texts:
        #     if len(texts) > 0:
        #         flag = True
        # return flag

    def run_file_name(self, file_name):

        # 保存框 清除掉重复的框
        self.bboxes = self.get_objs(f"{file_name}_bbox", self._get_bbox_from_autocad)
        self.bboxes = self.preprocess_bboxes_to_remove_duplicated_bbox(self.bboxes)

        # 保存右上角表格
        self.ru_texts = self.get_objs(f"{file_name}_ru_text", self._get_text_from_autocad)
        print(len(self.ru_texts))
        self.ru_texts, ru_texts_pos = self.assign_objs_to_bboxes(self.ru_texts)
        (x, y, width, height) = CAD_RU_TEXT_COORDINATE
        ru_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        real_ru_new_texts = self.extract_correct_pos_texts(texts=self.ru_texts, texts_pos=ru_texts_pos,
                                                           rec_area=ru_area)
        modified_sorted_texts = self.sort_real_new_texts(real_ru_new_texts)
        all_ru_rows = self.get_ru_all_rows(modified_sorted_texts)
        all_ru_rows = self.mitigate_ru_empty(all_ru_rows)

        # 保存左下角表格
        self.down_texts = self.get_objs(f"{file_name}_down_text", self._get_text_from_autocad)
        print(len(self.down_texts))
        self.down_texts, down_texts_pos = self.assign_objs_to_bboxes(self.down_texts)
        (x, y, width, height) = CAD_DOWN_TEXT_COORDINATE
        down_area = RectangleArea(Point(x, y), Point(x + width, y + height))
        real_down_new_texts = self.extract_correct_pos_texts(texts=self.down_texts, texts_pos=down_texts_pos,
                                                             rec_area=down_area)
        modified_sorted_texts = self.sort_real_new_texts(real_down_new_texts)
        print([text.text_string for text in modified_sorted_texts[0]])
        all_down_rows = self.get_down_all_rows(modified_sorted_texts)
        print(len(all_down_rows))

        excel_rows = []
        for ru_rows, down_row_dic in zip(all_ru_rows, all_down_rows):
            down_row_list = [down_row_dic[title] for title in DOWN_TEXT_TITLE]
            for i, ru_row in enumerate(ru_rows):
                ru_row.extend(down_row_list)
                excel_row = ru_row
                excel_row.append(file_name)
                excel_rows.append(excel_row)

        return excel_rows

    def run_all(self, file_names):
        wb = openpyxl.Workbook()
        ws = wb.active
        title_row = RU_TEXT_TITLE + DOWN_TEXT_TITLE + ["文件名"]
        ws.append(title_row)

        for file_name in file_names:
            excel_rows = self.run_file_name(file_name)
            [ws.append(excel_row) for excel_row in excel_rows]

        wb.save(self.excel_save_path)
        print(f"保存成功：{self.excel_save_path}")

        from autofix_excel_column_size import CXlAutofit # 处理excel样式
        Entity = CXlAutofit()
        Entity.style_excel(self.excel_save_path, "Sheet")
