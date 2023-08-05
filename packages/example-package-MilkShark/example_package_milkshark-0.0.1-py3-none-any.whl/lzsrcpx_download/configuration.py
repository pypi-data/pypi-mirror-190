

###################你需要修改的参数##########################

Cookie = 'UM_distinctid=17edc1705d2fe-099232cf872dd7-5b161d53-144000-17edc1705d354a; _gscu_761273330=44370003vei6tj19; lzrspx_front=95882B04EED30687F686802A5B009972; CNZZDATA1278655822=732529361-1644368190-%7C1644570351; _gscbrs_761273330=1; _gscs_761273330=44573115c13ouk19|pv:5'
courceID = '40285c8878c4c6050178ce35f6590014'
name = '（公需科目）【2021】'

EXAM_SAVE_PATH = 'exam.json'    #考试卷保存地址
EXAM_TEST_SAVE_PATH = 'examTest.json'       #模拟卷保存地址

###################你需要修改的参数##########################

EXAM_DOWNLOAD_NUM = 30   #一次性下载的试卷数目
SLEEP_TIME = 0  #试卷下载时间间隔

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Cookie':Cookie
}
EXAM_URL = 'http://www.lzsrcpx.com/reg/exam?courseId={}&name={}'.format(courceID,name)
EXAM_TEST_URL = 'http://www.lzsrcpx.com/reg/examTest?courseId={}&name={}'.format(courceID,name)

config = {
    "exam":{
        'url':EXAM_URL,
        'save_path':EXAM_SAVE_PATH,
    },
    "test":{
        'url': EXAM_TEST_URL,
        'save_path': EXAM_TEST_SAVE_PATH,
    }
}
