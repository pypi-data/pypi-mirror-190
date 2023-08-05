import time
import requests
import re
import json
from selenium import webdriver
import threading # 导入threading模块
from queue import Queue #导入queue模块

def get_mulu(html_url,xpath,html_queue):

    #版本要合适，chromedriver与python编译器同文件夹
    #http://chromedriver.storage.googleapis.com/index.html
    driver = webdriver.Chrome()

    driver.get(html_url)
    titles = []
    chapter_urls = []
    linklist = driver.find_elements_by_xpath(xpath)
    for i,chapter in enumerate(linklist):
        title = chapter.text
        href = chapter.get_attribute('href')
        info = (i,title,href)
        html_queue.put(info)
        # titles.append(title)
        # chapter_urls.append(href)
    # return titles,chapter_urls

def get_chapter_infor(html_queue,chapter_queue):
    while not html_queue.empty():
        # if html_queue.empty():
        #     time.sleep(5)
        #     if html_queue.empty():
        #         break
        i,title,chapter_url = html_queue.get()
        content_response = requests.get(chapter_url)
        content = content_response.content.decode()

        content = content[content.find('<div id="content">')+len('<div id="content">'):]
        content = content[:content.find('</div>')]
        content = content.replace('&nbsp;',' ').replace('<br>','\n')
        print(i)
        content = (i,title+'\n\n' + content)

        chapter_queue.put(content)
    print('over')

if __name__ == "__main__":

    fic_url = r"https://www.sobiquge.com/book/44188/"
    xpath = '//*[@id="list"]/dl/dd/a'
    # titles, chapter_urls = get_mulu(fic_url, xpath)

    html_queue = Queue(maxsize=1600) #用Queue构造一个大小为1000的线程安全的先进先出队列
    chapter_queue = Queue(maxsize=1600) #用Queue构造一个大小为1000的线程安全的先进先出队列
    get_mulu(fic_url,xpath,html_queue)
    print(html_queue.empty())
    # 先创建目录线程
    # thread = threading.Thread(target=get_mulu, args=(fic_url,xpath,html_queue,)) #A线程负责抓取列表url
    thread_num = 10

    html_thread= []
    for i in range(thread_num):
        thread2 = threading.Thread(target=get_chapter_infor, args=(html_queue,chapter_queue))
        html_thread.append(thread2)#B C D 线程抓取文章详情
    start_time = time.time()
    # 启动四个线程
    # thread.start()
    for i in range(thread_num):
        html_thread[i].start()
    # 等待所有线程结束，thread.join()函数代表子线程完成之前，其父进程一直处于阻塞状态。
    # thread.join()
    for i in range(thread_num):
        html_thread[i].join()

    chapter_list = ['']*1600
    while not chapter_queue.empty():
        i,chapter_info = chapter_queue.get()
        chapter_list[i] = chapter_info
    print("bbdfdf")

    chapter_str = '\n'.join(chapter_list)
    with open('fiction.txt','w',encoding='utf-8') as f:
        f.write(chapter_str)

    print("last time: {} s".format(time.time()-start_time))#等ABCD四个线程都结束后，在主进程中计算总爬取时间。



