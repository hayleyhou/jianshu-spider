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

authorLink = []
with open('/Users/houxiaohui/Desktop/authorLink.csv','r') as f:
    Link = f.readlines()
for i in Link:
    authorLink.append(i.strip('\n'))


def get_author(num):
    try:
        urlauthor = authorLink[num]
        jianshu47Author = {}
        s = requests.Session()
        headers = {
            'Host':'www.jianshu.com',
            'If-None-Match':'W/"d2831f35a154a1225ca4fc4a7febf264"',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'}

        r = s.get(urlauthor, headers=headers)
        print r.status_code
        content = r.content
        soup = BeautifulSoup(content,'lxml')
        time.sleep(3)

        mostread= re.search('\d+',re.search(r'阅读 \d+',str(soup.select('ul > li > div > div')[0])).group()).group()
        author_id = soup.select('div.people > div.basic-info > h3 > a')[0].get('href')
        author = soup.select('div.people > div.basic-info > h3 > a')[0].text
        toppest_articles = soup.select('ul > li > div > h4 > a')[0].text
        signed_author = soup.select('div.signed_author')
        if signed_author:
            signed_author = True
        else:
            signed_author = False
        fansNum = soup.select('div.user-stats > ul > li > a > b')[1].text
        passagesNum = soup.select('div.user-stats > ul > li > a > b')[2].text
        words = soup.select('div.user-stats > ul > li > a > b')[3].text
        likesNum = soup.select('div.user-stats > ul > li > a > b')[4].text

        jianshu47Author['mostread'] = mostread
        jianshu47Author['author_id'] = author_id
        jianshu47Author['author'] = author
        jianshu47Author['toppest_articles'] = toppest_articles
        jianshu47Author['signed_author'] = signed_author
        jianshu47Author['fansNum'] = fansNum
        jianshu47Author['passagesNum'] = passagesNum
        jianshu47Author['words'] = words
        jianshu47Author['likesNum'] = likesNum
        print 'successfully getting data from author%d'%num
        saveAuthor(num,jianshu47Author)
    except:
        pass

def saveAuthor(num,data):
    with open('/Users/houxiaohui/Desktop/jianshu47/jianshu47Author/Author%d.csv'%num,'w') as f:
        fieldnames = ['author','author_id','toppest_articles','mostread','signed_author','words','fansNum','passagesNum','likesNum']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # for i in range(0, 1):
        writer.writerow({
            'author':data['author'],
            'author_id':data['author_id'],
            'toppest_articles':data['toppest_articles'],
            'mostread':data['mostread'],
            'signed_author':data['signed_author'],
            'words':data['words'],
            'fansNum':data['fansNum'],
            'passagesNum':data['passagesNum'],
            'likesNum':data['likesNum']
        })
    f.close()
