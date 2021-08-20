import json
import os
import random
import sys
import traceback
from time import sleep

import requests
from lxml import etree
from tqdm import tqdm


class Spider:
    def __init__(self, scaned_userid, toscan_userid):
        self.headers = {
            'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Cookie': "",
            'Connection': 'close'
        }
        self.scaned_userid = scaned_userid
        self.toscan_userid = toscan_userid

    def get_page_num(self, userid):
        url = f"https://weibo.cn/{userid}/follow"
        html = requests.get(url, headers=self.headers).content
        selector = etree.HTML(html)
        if selector.xpath("//input[@name='mp']") == []:
            page_num = 1
        else:
            page_num = (int)(
                selector.xpath("//input[@name='mp']")[0].attrib['value'])
        return page_num

    def crawl(self, userid):
        page_num = self.get_page_num(userid)

        page1 = 0
        random_pages = random.randint(1, 5)
        follow_userids = set()
        nicknames = set()
        for page in tqdm(range(1, page_num + 1)):
            url = f'https://weibo.cn/{userid}/follow?page={page}'
            try:
                html = requests.get(url, headers=self.headers).content
            except Exception as e:
                print(e)
                continue

            selector = etree.HTML(html)
            table_list = selector.xpath('//table')
            if (page == 1 and len(table_list) == 0):
                print(u'cookie无效或提供的user_id无效')
            else:
                for t in table_list:
                    im = t.xpath('.//a/@href')[-1]
                    follow_userids.add(im.split('uid=')[-1].split('&')[0].split('/')[-1])
                    nicknames.add(t.xpath('.//a/text()')[0])

            if page - page1 == random_pages and page < page_num:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 5)
        return follow_userids, nicknames

    def run(self):
        for e, userid in enumerate(self.toscan_userid, 1):
            print(f'爬取第{e}个user id: {userid}')
            if userid in self.scaned_userid or not userid.isdigit():
                continue

            self.scaned_userid.add(userid)
            try:
                follow_userids, nicknames = self.crawl(userid)
            except:
                traceback.print_exc()
                continue
            with open('toscan_userid_new.txt', 'a') as f:
                for i in follow_userids:
                    f.write(i.strip()+'\n')
            with open('username.txt', 'a', encoding='utf-8') as f:
                for i in nicknames:
                    f.write(i.strip()+'\n')
            with open('scaned_userid.txt', 'a') as f:
                f.write(userid + '\n')

if __name__ == '__main__':
    # with open('user_id_list.txt', encoding='utf-8') as f1, \
    #         open('username.txt', 'w', encoding='utf-8') as f2, \
    #         open('toscan_userid.txt', 'w') as f3:
    #     for line in f1:
    #         id, name = line.strip().split()
    #         f2.write(name + '\n')
    #         f3.write(id + '\n')

    scaned_ids = set()
    with open('scaned_userid.txt') as f:
        for line in f:
            scaned_ids.add(line.strip())

    toscan_ids = set()
    with open('toscan_userid.txt') as f:
        for line in f:
            toscan_ids.add(line.strip())

    Spider(scaned_ids, toscan_ids).run()
