# -*- coding: utf-8 -*-
import requests,time,os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class spider():
    def __init__(self):
        self.base_url = 'https://danbooru.donmai.us'
        if os.path.exists(os.path.join("..",'Danbooru20190704_data')) == False:
            os.makedirs(os.path.join("..",'Danbooru20190704_data'))
    def search_result(self,url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        container = soup.find_all('div',{'id':'posts-container'})[0]
        articles = container.find_all('article')
        #测试用代码块
        # for article in articles:
        #     print(article['data-file-url'])

        #exit(0)
        for article in articles:
            pic_url = article['data-file-url']
            pic_md5 = article['data-md5']
            pic_filename = '{}.jpg'.format(pic_md5)
            #判定是否下载过
            if os.path.exists(os.path.join('..','Danbooru20190704_data',pic_filename)) == False:
                self.download_pic(pic_url,pic_filename)
        try:
            next_page = soup.find_all('a',{'id':'paginator-next'})[0]
            next_page_url = urljoin(self.base_url,next_page['href'])
            self.search_result(next_page_url)
            time.sleep(10)
        except:
            print('finish')


    def download_pic(self,pic_url,pic_filename):
        r = requests.get(pic_url)
        content = r.content
        with open(os.path.join('..','Danbooru20190704_data',pic_filename),'ab+') as f:
            f.write(content)
        print('{} success'.format(pic_filename))
        time.sleep(60)


if __name__ == "__main__":
    url = 'https://danbooru.donmai.us/posts?ms=1&page=1&tags=haneru&utf8=%E2%9C%93'
    sp = spider()
    sp.search_result(url)
