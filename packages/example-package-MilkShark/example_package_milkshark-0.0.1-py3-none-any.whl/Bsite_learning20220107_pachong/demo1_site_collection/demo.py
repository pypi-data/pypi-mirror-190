import requests
from strategy import user_agent,from_str_to_dict
import json
import re

def save_html(name,contents):
    with open(name,'w',encoding='utf-8') as f:
        f.write(contents)

# 爬取网页数据 结合反反爬策略
def demo_site_collection():
    url = 'https://www.baidu.com/s'
    keyword = '王梦洁'
    params = {
        'wd':keyword
    }
    headers = {
        'User-Agent': user_agent('firefox')
    }
    response = requests.get(url,params=params,headers=headers)
    print(response.text)
'''
进入开发者模式 ajax请求
network(网络)->XHR 
'''
def demo_baidu_translate():
    url = 'https://fanyi.baidu.com/sug'
    keyword = 'dog'
    data = {
        'kw':keyword
    }
    headers = {
        'User-Agent': user_agent('firefox'),
    }
    response = requests.post(url,data=data,headers=headers)

    print(response.json())

'爬取豆瓣电影'
def demo_douban():
    url='https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=40&limit=20' #根据start 和limit 找
    headers = {
        'User-Agent': user_agent('firefox'),
    }
    response = requests.get(url,headers=headers)
    a = response.json()
    print(response.json())

'化妆品药妆局'
def demo_yaojianju():
    #直接请求url访问不到企业信息
    url = 'http://scxk.nmpa.gov.cn:81/xk/' #首页
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portal/dzpz.jsp?id=173b71faa86c4c24a722f1f9f4b2db56' #详情页

    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    data = {
        "id":'173b71faa86c4c24a722f1f9f4b2db56'
    }

    headers = {
        'User-Agent': user_agent('firefox'),
    }
    contents = requests.post(url,data=data,headers=headers).json()
    print(contents)
    exit()
    with open('yaojianju.html','w',encoding='utf-8') as f:
        f.write(contents)

def demo_re():
    url = 'http://scxk.nmpa.gov.cn:81/xk/' #首页
    headers = {
        'User-Agent': user_agent('firefox'),
    }
    response = requests.get(url,headers=headers)
    contents = response.text

    #正则表达式
    pattern = '<span id="(.*?)".*?>'
    results = re.findall(pattern,contents)
    print(results)



'bs4'
def demo_bs4():
    from bs4 import BeautifulSoup
    with open('yaojianju.html',encoding='utf-8') as f:
        soup = BeautifulSoup(f,'lxml')
    meta = soup.select('meta')

'xpath'
def demo_xpath():
    from lxml import etree
    # with open('yaojianju.html') as f:
    tree = etree.parse('yaojianju.html',parser=etree.HTMLParser(encoding='utf-8'))  #需要重新解析码
    print(tree)


'''
http://www.lzsrcpx.com/reg/exam?courseId=40285c8878c4c6050178ce35f6590014&name=%EF%BC%88%E5%85%AC%E9%9C%80%E7%A7%91%E7%9B%AE%EF%BC%89%E3%80%902021%E3%80%91
http://www.lzsrcpx.com/reg/exam?courseId=40285c8878c4c6050178ce35f6590014&name=%EF%BC%88%E5%85%AC%E9%9C%80%E7%A7%91%E7%9B%AE%EF%BC%89%E3%80%902021%E3%80%91
'''

def demo_login():
    #先登录 获取cookie 用session发请求自动携带和保存cookie
    session = requests.Session()
    url = ''
    headers = {
        'User-Agent': user_agent('firefox'),
    }
    response = session.post(url,headers=headers)  #使用session进行登录

    url2 = ''
    response2 = session.get(url,headers=headers)

'代理'
def demo_agent():
    url = 'https://www.baidu.com/s'
    #加上accept  ，否则会返回百度安全验证 也不行
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'User-Agent': user_agent('firefox'),
        # 'Cookie':'BIDUPSID=1F19FABC9435B0E4FE9201FA690C14B8; PSTM=1588665347; MCITY=-75%3A; BD_UPN=13314752; __yjs_duid=1_4f312003a0de1c63c09e975f5f5e39ad1619450140454; BAIDUID=620ECE2AEE95231991B1500A1645ACE1:FG=1; BDUSS=F4RVV2RkJsNWdHRDlKTFk3b3FXTWJCMkpjRW5SbDJUTjRuOTNHZ240NDBoNmRoRVFBQUFBJCQAAAAAAAAAAAEAAADwAWKmxrbJrreousW08sTPuc8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADT6f2E0-n9hSG; H_PS_PSSID=35412_35105_31253_35829_35489_34584_35490_35802_26350_35724_35761_35757; BDORZ=FFFB88E999055A3F8A630C64…M3mVXurUvdTTH6ao4DmCarcdlflTL5dQEG0Phx8g0Kubo7k0ogKKXgOTHwAF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR-tVCtatCI3HnRv5t8_5-LH-UoX-I62aKDsotocBhcqEIL45nJz5fFuQa3xt-nutKjphP5-Q4QfSMbSj4QojM0DLUQH5-3Q5DJn2I5eLl5nhMJd257JDMP0-xPfa5Oy523ihn3vQpnbEqQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0-nDSHHDjt6_H3f; sugstore=1; delPer=0; BD_CK_SAM=1; PSINO=1; BA_HECTOR=2lag84ag210gahak261h04f9n0r; COOKIE_SESSION=300_1_7_9_5_8_1_0_7_4_273_4_64_0_342_0_1644313862_1644310908_1644313520%7C9%231610309_46_1644310906%7C9; BDSVRTM=0',
    }
    params = {
        'wd':'ip',
    }
    response = requests.get(url,params=params,headers=headers)
    response.encoding = 'utf-8'
    print(response.status_code)
    contents = response.text
    with open('ip.html','w',encoding='utf-8') as f:
        f.write(contents)

'异步：线程池'
def demo_pool_threading():
    import time
    from multiprocessing.dummy import Pool #线程池
    objs_num = 5
    def exe_obj(i):
        print('正在下载',i)
        time.sleep(2)
        print('下载成功',i)

    def without_threading(objs_num):
        start_time = time.time()
        for i in range(objs_num):
            exe_obj(i)
        end_time = time.time()
        print("非线程方式耗时:{}".format(end_time-start_time))
    def with_threading(objs_num):
        start_time = time.time()
        pool = Pool(objs_num)
        objs_nums = [i for i in range(objs_num)]
        pool.map(exe_obj,objs_nums)
        end_time = time.time()
        print("线程方式耗时:{}".format(end_time-start_time))

    without_threading(objs_num)
    with_threading(objs_num)

'异步应用：下载梨视频'
def demo_pear_video():
    from lxml import etree

    home_url = 'https://www.pearvideo.com/category_9'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        # 'Referer':'https://www.pearvideo.com/video_1751293',
        # 'Host':'www.pearvideo.com',
    }

    home_conts = requests.get(url=home_url,headers=headers).text
    # save_html('home_pear.html',home_conts)

    tree = etree.HTML(home_conts)
    li_list = tree.xpath("/html/body/div[2]/ul/li")

    detail_dics = []
    for li_item in li_list:
        #单个视频的title he 页面
        title = li_item.xpath('./div/a/div[2]/text()')[0]
        href = li_item.xpath('./div/a/@href')[0]

        #每个pearvideo子页面获取
        def get_piece_video(id):
            contID = id[len('video_'):]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
                'Referer':'https://www.pearvideo.com/{}'.format(id),
                # 'Host':'www.pearvideo.com',
            }
            url = 'https://www.pearvideo.com/videoStatus.jsp?contId={}&mrd=0.10993652938990894'.format(contID)
            contents = requests.get(url=url,headers=headers).json()
            #需要重新拼接
            systemTime = contents['systemTime']
            srcUrl = contents['videoInfo']['videos']['srcUrl']
            mp4_url = srcUrl.replace(systemTime,'cont-{}'.format(contID))
            print(mp4_url)
            result = {
                'url':mp4_url,
                'title':title
            }
            return result

        detail_dics.append(get_piece_video(href))

    def download_mp4(dic):
        url = dic['url']
        title = dic['title']
        print('开始下载：{}'.format(title))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        }
        response = requests.get(url=url,headers=headers)
        video_data= response.content
        with open('{}.mp4'.format(title),'wb') as f:
            f.write(video_data)
        print('结束下载：{}'.format(title))


    # 开启线程下载
    from multiprocessing.dummy import Pool
    pool = Pool(4)
    pool.map(download_mp4,detail_dics)


demo_pear_video()