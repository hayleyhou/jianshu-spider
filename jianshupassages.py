import requests
import csv
import Queue
import re
import sys
import time
import csv
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

with open('/Users/houxiaohui/Desktop/passageLink.csv','r') as s:
        Link = s.readlines()
passageLink = []
for i in Link:
    passageLink.append(i.strip('\n'))

def get_passages(num):
    try:
        url = passageLink[num]
        s = requests.Session()
        cookies = {
            'cookies':'read_mode=day; default_font=font2; remember_user_token=W1sxOTg3NjQzXSwiJDJhJDEwJGkwRVllbklHR0VLTi5NN2tUS3N1U3UiLCIxNDYzMTMwOTU0LjU2Mzk3MyJd--0570374a06095d425d4732a1ed7101c42f20a79e; __utmt=1; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1463165888,1463173013,1463173202,1463174765; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1463175621; __utma=194070582.749687443.1463130164.1463165751.1463173013.5; __utmb=194070582.10.10.1463173013; __utmc=194070582; __utmz=194070582.1463173013.5.4.utmcsr=localhost:8888|utmccn=(referral)|utmcmd=referral|utmcct=/notebooks/Untitled3.ipynb; __utmv=194070582.|2=User%20Type=Member=1; _session_id=VDdEM2RqTWplbDgvbnJjSmMyY3k1VkhqSEVDU1ZkOW0xcHU0K3M4VDBkL3BMUno1UEtlRndxSmFhNThIRVJYbmcwQXJrd1Q1TUhOSUVVd0RkZytVSElXK1d1bFd5SlMzN0M2am5oUStkOEFzRzZlRWNnaXRuRkxLZXBqVXdXQ2VoSHhTYzJvYzlKdkRmYUdNMHRtaFhiRElTUGZXZmpXSDA5aXFlU0FvY24xZ2pWSHpUb2hFYzhUVHNhYjQyVm50aUw2NGNWdE1LZkZ1NktvQ2RnZThud21Jenl3Y29UdVJhSVBGWlhnWTE5ZXAzQnRWRDVPODFFd29Kc1RGZS94TzRwSXQxVTZOSWNhaktodS9ld3Y4MkNvY21Rc28zdjRLMG1CUnc5dFVRdkcvcEE0Z3ZNd2x3ZmVrc3BHWEViT3FhTW1IUVVFMFRPZldVdmxPNWRkZFkxTXhlclU1OGUyQmlOSm15d3EvRmdJSUpEMFNONW9QeGpMQVFGOURrWWNLMTZla3Z1bFFSOENDKzN5M1VMVEg5QkNzOWpJV201UHNybmVmWHRkbjIwR0RnWWdsaHlsdjRHdkEvNFpWVGNEa0FKRGVCT1dpaFRTVGZ4LzhTSW1YMnZ6Ynh2QVlwaDUyUVRMMWFIN2hoNW9UUnJ5UFVXYVhYRWRLajl6V0d1aDgtLWlVdmxOUE9vZzFwVGUvTXRnMTZxVUE9PQ%3D%3D--13748e82499a999c5ce409babe52395edbad8183'
        }
        headers = {'Host':'www.jianshu.com',
            'If-None-Match':'W/"c5a7cec7123677ac84788d6394aef610"',
            'Referer':'http://www.jianshu.com/collections',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
            }

        r = s.get(url, cookies=cookies,headers=headers)
        content = r.content
        time.sleep(3)

        soup = BeautifulSoup(content,'lxml')
        passageWord = re.search('\d+',re.search(r'"wordage":\d+,', str(soup.select('script'))).group()).group()
        collections = soup.select('li > div > h5 > a')
        imagesNum = len(soup.select('.image-package'))
        collections_listEach = []
        for i in collections:
            collections_listEach.append(i.text)

        length = len(collections_listEach)
        while length < 5:
            collections_listEach.append(None)
            length +=1



        with open('/Users/houxiaohui/Desktop/jianshu47/jianshu47Passage/Passagesdata%d.csv'%num,'wb') as r:
            fieldnames = ['passageLink','passageWord','imagesNum','collections1','collections2','collections3','collections4','collections5']
            writer = csv.DictWriter(r, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                'passageLink':url,
                'passageWord':passageWord,
                'imagesNum':imagesNum,
                'collections1':collections_listEach[0],
                'collections2':collections_listEach[1],
                'collections3':collections_listEach[2],
                'collections4':collections_listEach[3],
                'collections5':collections_listEach[4]
            })
        r.close()
        print num
    except Exception as e:
        print '%d error'%num, e








