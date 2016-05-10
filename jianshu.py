#!/usr/bin/python
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

def get_jianshu_data(page):

    s = requests.Session()
    headers = {
        'Host':'www.jianshu.com',
        'If-None-Match':'W/"cbf89c1521bca87c637f386f1c5daf62"',
        'Referer':'http://www.jianshu.com/collections',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
    }

    with open ('/Users/houxiaohui/Desktop/jianshu627/jianshu_627_%d.csv'%page, 'w') as f:

        url = 'http://www.jianshu.com/collections/627/notes?order_by=added_at&page=%d'%page
        print 'getting data from page %d now...........'%page

        try:
            r = s.get(url, headers=headers,timeout=10)
            content = r.content
            time.sleep(1)


            soup = BeautifulSoup(content,'lxml')
            title = (map(lambda x:x.text,[i for i in soup.select('div > h4 > a')]))
            postdate = (map(lambda x:re.search('t="(.*?)T(.*?)\+08:00',str(i)).group(1),[i for i in soup.select('div > p > span')]))
            posttime = (map(lambda x:re.search('t="(.*?)T(.*?)\+08:00',str(i)).group(2),[i for i in soup.select('div > p > span')]))
            read = (map(lambda i:int(re.search('\d+',re.search(r'阅读 \d+',str(i)).group()).group()),[i for i in soup.select('ul > li > div > div')]))
            comment = (map(lambda i:int(re.search('\d+',re.search(r'评论 \d+',str(i)).group()).group()),[i for i in soup.select('ul > li > div > div')]))
            like = (map(lambda i:int(re.search('\d+',re.search(r'喜欢 \d+',str(i)).group()).group()),[i for i in soup.select('ul > li > div > div')]))
            author = (map(lambda x:x.text,[x for x in soup.select('ul > li > div > p > a')]))



            fieldnames = ['author','title','postdate','posttime','read','like','comment']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            quanity = len(author)
            for i in range(0, quanity):
                writer.writerow({
                    'author':author[i],
                    'title':title[i],
                    'postdate':postdate[i],
                    'posttime':posttime[i],
                    'read':read[i],
                    'like':like[i],
                    'comment':comment[i]})
        except:
            pass
    f.close()


