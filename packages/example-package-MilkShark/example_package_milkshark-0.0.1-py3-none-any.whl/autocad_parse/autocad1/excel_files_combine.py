# https://blog.csdn.net/xili1342/article/details/124983308
import pandas as pd
import os


class CombineExcelFile:

    def append_by_root(self, path):  # path：所有需要合并的excel文件所在的文件夹
        filename_excel = []  # 建立一个空list,用于储存所有需要合并的excel名称
        frames = []  # 建立一个空list,用于储存dataframe
        for root, dirs, files in os.walk(path):
            for file in files:
                file_with_path = os.path.join(root, file)
                filename_excel.append(file_with_path)
                df = pd.read_excel(file_with_path, engine='openpyxl')
                frames.append(df)
        df = pd.concat(frames, axis=0)
        return df

    def append_by_paths(self, paths):  # path：所有需要合并的excel文件所在的文件夹
        frames = []  # 建立一个空list,用于储存dataframe
        for path in paths:
            df = pd.read_excel(path, engine='openpyxl')
            frames.append(df)
        df = pd.concat(frames, axis=0)
        return df

    def combine_by_root(self, path, combine_excel_name="合并的excel.xlsx"):
        with pd.ExcelWriter(combine_excel_name) as writer:
            for root, dirs, files in os.walk(path):
                for file in files:
                    filename = os.path.join(root, file)
                    df = pd.read_excel(filename, engine='openpyxl')
                    df.to_excel(writer, sheet_name=file.strip('.xls'))  # 删除文件名的后缀，有时候是.csv/.xlsx
            return df

    def combine_by_paths(self, paths, sheet_names,combine_excel_path):
        with pd.ExcelWriter(combine_excel_path) as writer:
            for path,sheet_name in zip(paths,sheet_names):
                df = pd.read_excel(path, engine='openpyxl')
                df.to_excel(writer, sheet_name= sheet_name)  # 删除文件名的后缀，有时候是.csv/.xlsx
