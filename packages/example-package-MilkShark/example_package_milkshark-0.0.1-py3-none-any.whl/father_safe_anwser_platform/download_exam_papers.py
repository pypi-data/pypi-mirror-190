#!/usr/bin/env Python
# coding=utf-8
import json

import requests
from lxml import etree
import yaml


COOKIE = "__utma=61448764.398921480.1658497006.1658497006.1658497006.1; __utmz=61448764.1658497006.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); username=6024622392; password=NjYzMTA2; __utmt=1; Hm_lvt_5aaa8639bed59dc2da01dde8c930508f=1658497004,1658497797; Hm_lpvt_5aaa8639bed59dc2da01dde8c930508f=1658497797; __utmc=61448764; user_session=6024622392_true%26%261658497798%26%265400%26%264%26%26ceshi; g=c81263bd3a7f3bb70cddff3643c5b314; __utmb=61448764.7.10.1658497006"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    'Cookie': COOKIE,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Host': 'www.aqscmnks.com',

}
EXAM_PAPER_NAME = 'lishijilu.php'

BASE_URL = "https://www.aqscmnks.com/exam/View"
DIRECTORY_URL = f"{BASE_URL}/shouye.php?t=1658494924290"

RESULT_SAVED_PATH = "results"
DATA_SAVED_PATH = "data.json"


# DIRECTORY_URL = f"https://www.aqscmnks.com/exam/View/shouye.php?t=1658494924290"

class ExamDownloader:
    def download_exam_paper_urls(self, tree):
        xpath = f'//*[@id="tabk"]/tr/td[8]/div'
        # xpath = f"/html/body/div/table/tbody/tr[2]/td/table[2]/tbody[2]/tr[{paper_id}]/td[8]/div"
        exam_papers = tree.xpath(xpath)
        exam_paper_urls = []

        for exam_paper in exam_papers:
            onclick_text = exam_paper.attrib['onclick'].split('(')[1].split(')')[0]
            onclick_text = onclick_text.replace('"', '').replace("'", '')
            start_index = onclick_text.find(EXAM_PAPER_NAME)
            exam_paper_url = f"{BASE_URL}/{onclick_text[start_index:]}"
            exam_paper_urls.append(exam_paper_url)
        return exam_paper_urls

    def download_exam_paper(self, exam_paper_urls):
        results = {}
        for exam_paper_url in exam_paper_urls:
            print(f"Begin to execute url: {exam_paper_url}")
            tree = self.connect_for_tree(exam_paper_url)
            ti_xpath = f'//*[@id]/div[2]/div[1]/p/text()'
            ti_type_xpath = f'//*[@id]/div[2]/div[1]/p/span/text()'
            xx_xpath = f'//*[@id]/div[2]/div[1]/ul'
            anwser_xpath = f'//*[@id]/div[2]/div[2]/span[3]'

            ti_list = tree.xpath(ti_xpath)
            ti_type_list = tree.xpath(ti_type_xpath)
            xx_list = tree.xpath(xx_xpath)
            anwser_list = tree.xpath(anwser_xpath)

            for ti, ti_type, xx, anwser in zip(ti_list, ti_type_list, xx_list, anwser_list):
                refresh_ti = ti[ti.find('、') + 1:].replace(' ', '')
                refresh_ti_type = ti_type.replace('\r', '').replace('\n', '').replace(' ', '')

                # 处理正确答案
                anwser_text = anwser.text
                anwser_remove_string = '正确答案：'
                refresh_anwser = anwser_text.replace(anwser_remove_string, '').replace(' ', '')

                try:
                    xx_item_xpath = 'li/input'
                    refresh_xx = [xx_item.tail.replace(' ', '') for xx_item in xx.xpath(xx_item_xpath)]
                except AttributeError as e:
                    # 说明有图片
                    xx_item_li_xpath = 'li'
                    xx_item_img_xpath = 'img'
                    xx_item_input_xpath = 'input'

                    refresh_xx = []

                    for xx_item in xx.xpath(xx_item_li_xpath):
                        img = xx_item.xpath(xx_item_img_xpath)[0]
                        input = xx_item.xpath(xx_item_input_xpath)[0]

                        start_string = input.tail if input.tail is not None else ''
                        import os
                        middle_string = os.path.basename(img.attrib['src'])
                        end_string = img.tail if img.tail is not None else ''

                        xx = f"{start_string}【{middle_string}】{end_string}"
                        refresh_xx.append(xx)

                    print(e)

                results[refresh_ti] = {
                    "content": refresh_ti,
                    "type": refresh_ti_type,
                    "select": refresh_xx,
                    "anwser": refresh_anwser,
                    "anwser_explan": ""
                }
        return results

    def save_results(self, results, path=RESULT_SAVED_PATH):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(results, fp=f, indent=1, ensure_ascii=False)

    def load_results(self):
        with open(RESULT_SAVED_PATH, encoding='utf-8') as f:
            results = json.loads(f.read())
        return results

    def modify_result_add_id(self, results):
        new_results = []
        for id, item in enumerate(results.values()):
            id = id + 1
            item["id"] = id
            new_results.append(item)
        return new_results

    def connect_for_tree(self, url):
        response = requests.get(url=url, headers=HEADERS)
        tree = etree.HTML(response.text)

        return tree

    def run(self):
        tree = self.connect_for_tree(DIRECTORY_URL)
        exam_paper_urls = self.download_exam_paper_urls(tree)
        results = self.download_exam_paper(exam_paper_urls)
        self.save_results(results)


if __name__ == "__main__":
    ed = ExamDownloader()
    ed.run()

    results = ed.load_results()
    new_results = ed.modify_result_add_id(results)
    ed.save_results(new_results, path=DATA_SAVED_PATH)
