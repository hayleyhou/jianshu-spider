#!/usr/bin/python
#-*- coding: utf-8 -*-

import requests
import csv
import re
import sys
import time
import csv
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

def get_front_page(page):
    try:
        s = requests.Session()
        cookies = {
            'cookies':'read_mode=day; default_font=font2; remember_user_token=W1sxOTg3NjQzXSwiJDJhJDEwJGkwRVllbklHR0VLTi5NN2tUS3N1U3UiLCIxNDYyMjc0OTgxLjc5MTAyOTUiXQ%3D%3D--d27c8ff1f633ddb00dd6447d100a8eaf687b3dae; __utmt=1; __utma=194070582.1749276410.1462053333.1462984876.1462999828.31; __utmb=194070582.14.10.1462999828; __utmc=194070582; __utmz=194070582.1462825412.22.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=194070582.|2=User%20Type=Member=1; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1462649151,1462652683,1462738751,1462825412; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1463001018; _session_id=d3BuK01RNFBkbFBNWGt5K1BvQ3h1Yk4wNzMxczF4UW9MNVdEaGgzRk1QTVI0ckNVRUdKT01ESEgvVVM1R1dIQk5mU1FrRGRRMHRBQ2dxeVYrRG1iYmhKOGp6eEFyY3NBWklKdko4SFFPRzBiL2lRMCthYmJ3K1Y2M3k4NzdTbDM5NFhWdi94bThpOVZrYjU4cG1HbjdRWmZiMytSREg2ejV3VjNZczBvRHpEdktPSUFJSXliY3JEbGxVSU9DbWpQbjRkdmhvTG8rTi9iNStLTFVZQWpDaVNyVWVJM0NLMDRhdzdsdTR0MkQ5SFVJMU1tekFvRzFRR1RxMkE2TSt2R3FvL083Yk5pVEZPc2kremd4ZUJQdytxeHlRRTRVeFYzYTVyMnFUTjFmY0cveSs2NzVwZzhuSjFsOTBsSHZkMDZibjhvZUpGOTVsaTdiNk5kWjJlSU41M09WRmlZaVp5cEZqeTlZMkNxMS8xWXVJOVo2TE5vOHdWY3J1VXRncHh1bHJQT25iOTM0YmJQTkJneld4V0FJMlZ4eTlUMEZGOG91eFJlVnJXazloNzN3WEZibVNwK1FraE53UHpRczJubjJoZlNtTzZsOTRzM3djdGthbzZxWmZHbmpCK0tvQTh5OVJCejgvTHhxOHJieUx3OS8rYm1HcUZXcm1kU1d6QjUtLVhwaENNalBhRWdoNnhJb0hSczM5Z3c9PQ%3D%3D--57196fb98abe311c481d8eaa3f8e25c91f4de136'
        }
        headers = {

            'Host':'www.jianshu.com',
            'If-None-Match':'W/"f7539a5bdd551c9e7f417d4835e440f1"',
            'Referer':'http://www.jianshu.com/collection/bDHhpK',
            'X-CSRF-Token':'blfTaMRh6KY/ujt5A8cAHIqpp6j1mf0znwtC4tBtgK6mQf+DViaGIiFGen1c7Xiy61CGhAuBeiLnrgkSDY01lw==',
            'X-INFISCROLL':'true',
            'X-Requested-With':'XMLHttpRequest',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'    }


        url = 'http://www.jianshu.com/collections/47/notes?order_by=added_at&page=%d'%page
        print 'getting data from page %d now...........'%page
        r = s.get(url, headers=headers,cookies=cookies)
        print r.status_code
        content = r.content

        time.sleep(3)

        #阅读的select列表最后两个数字可能是20 23  or select =[0, 3, 5, 8 , 11 ,14 ,17 ,20, 23]
        select =[0, 3, 6, 9 , 12 ,15 ,18 ,21, 24]
        soup = BeautifulSoup(content,'lxml')
        title = (map(lambda x:x.text,[i for i in soup.select('div > h4 > a')]))
        postdate = (map(lambda x:re.search('t="(.*?)T(.*?)\+08:00',str(i)).group(1),[i for i in soup.select('div > p > span')]))
        posttime = (map(lambda x:re.search('t="(.*?)T(.*?)\+08:00',str(i)).group(2),[i for i in soup.select('div > p > span')]))
        read = (map(lambda i:int(re.search('\d+',re.search(r'阅读 \d+',str(soup.select('li > div > div > a')[i])).group()).group()),[i for i in select]))
        author = (map(lambda x:x.text,[x for x in soup.select('li > div > p > a')]))
        passagesLink = (map(lambda x:'http://www.jianshu.com/'+x.get('href'),[x for x in soup.select('div > h4 > a')]))
        author_id = (map(lambda x:x.get('href'),[x for x in soup.select('li > div > p > a')]))

        with open('/Users/houxiaohui/Desktop/jianshu47/jianshu47FrontPage/Passages%d.csv'%page,'w') as f:
            print 'opening'
            fieldnames = ['author','author_id','title','postdate','posttime','read','passageLink','AuthorLink']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(0, 9):
                writer.writerow({
                    'author':author[i],
                    'author_id':author_id[i],
                    'title':title[i],
                    'postdate':postdate[i],
                    'posttime':posttime[i],
                    'read':read[i],
                    'passageLink':passagesLink[i],
                    'AuthorLink':author_id[i]
                    # 'collections0':collections[i][0],
                    # 'collections1':collections[i][1],
                    # 'collections2':collections[i][2],
                    # 'collections3':collections[i][3],
                    # 'collections4':collections[i][4],
                })
        f.close()
    except:
        pass



