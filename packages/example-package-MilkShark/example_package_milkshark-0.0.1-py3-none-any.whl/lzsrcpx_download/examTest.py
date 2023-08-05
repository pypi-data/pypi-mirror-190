import re
import json
import os
import requests
from multiprocessing.dummy import Pool
from lxml import etree
import time
from configuration import EXAM_DOWNLOAD_NUM,SLEEP_TIME,config
from Base_Download_Exam_Func import download_exams

EXAM_TYPE = 'test'

if __name__ == "__main__":
    download_exams(EXAM_DOWNLOAD_NUM, SLEEP_TIME, EXAM_TYPE, config)
    from util import paint_num,match_ti
    paint_num()
    match_ti()











