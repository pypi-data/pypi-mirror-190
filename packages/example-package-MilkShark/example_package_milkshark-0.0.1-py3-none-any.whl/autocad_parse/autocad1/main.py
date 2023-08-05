from autocad_txt_parse import Tool

'''
small:
删除除图层类型不为ISO_AUTO的
删除线段
删除倾斜角度为30的位置
删除图案

big:
删除图层不为ISO_BLOCK的
删除线段
删除方向坐标
删除样式部位ISOBOM_BODY的
剩下有多余的字体，用正常式删除含有 ：'*此处为*','*现场实际情况*' ,'*一端插入*'
'''


def save_big_table(tool):
    #处理dic
    all_dic = tool.get_all_dic(type='big')
    all_same_row_dic = tool.combine_save_y(all_dic)
    all_sorted_dic = tool.sort_all_same_row_dic(all_same_row_dic)
    all_removed_sorted_dic = tool.remove_null_over_less_title_length(all_sorted_dic)
    # 展示dic
    # tool.show_sorted_dic(all_removed_sorted_dic)

    # 生成excel 去除多余字符
    tool.generate_excel_rows(all_removed_sorted_dic)
    # 结合install_num 并且改居中，改格式
    tool.combine_install_num(excel_type='big')

def save_small_table(tool):
    tool.save_small_table()
    tool.combine_install_num(excel_type='small')

def save_install(tool):
    pass

tool = Tool(r"C:\Users\wmj\Desktop\dad1")


save_big_table(tool)

# tool.save_install_num()
# tool.process_sheet_style_install()
# tool.combine_install_num(excel_type='small')

# tool.combine_all_sheets_to_one_excel()



#
# def refactor_all_dic(big_save_json_path):
#     with open(big_save_json_path) as f:
#         all_dic = json.loads(f.read())
#     new_all_dic = {}
#     for row in all_dic.keys():
#         new_all_dic[row] = {}
#         for col in all_dic[row].keys():
#             new_all_dic[row][col] = []
#
#             for item in all_dic[row][col]:
#                 text = item[0]
#                 x = item[1][0]
#                 y = item[1][1]
#                 new_all_dic[row][col].append({
#                     'text':text,
#                     'x':x,
#                     'y':y
#                 })
#     with open(big_save_json_path, 'w',encoding='utf-8') as f:
#         json.dump(new_all_dic, fp=f, indent=1, ensure_ascii=False)
#
#
# refactor_all_dic(r"C:\Users\wmj\Desktop\dad1\big_table_py.json")

'''
把相同y的分到一组

'''