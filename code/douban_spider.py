import requests
from lxml import etree
import time
import re
import json
import random
from retrying import retry

class DouBan():
    def __init__(self):
        self.category_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
        self.proxies=[{'http': 'http://221.223.91.30:8060'}, {'http': 'http://60.217.155.111:8060'}, {'http': 'http://123.115.200.52:8060'}, {'http': 'http://120.210.219.74:8080'}, {'http': 'http://123.115.229.242:8060'}, {'http': 'http://118.250.2.109:8060'}, {'http': 'http://222.135.31.132:8060'}, {'http': 'http://59.49.72.136:80'}, {'http': 'http://122.138.100.2:80'}, {'http': 'http://120.210.219.66:8080'}, {'http': 'http://59.49.72.136:80'}, {'http': 'http://122.138.100.2:80'}, {'http': 'http://120.210.219.66:8080'}, {'http': 'http://111.197.167.200:8060'}, {'http': 'http://123.117.175.17:8060'}, {'http': 'http://119.180.134.41:8060'}, {'http': 'http://220.184.145.141:8060'}, {'http': 'http://123.121.104.220:8060'}, {'http': 'http://114.249.178.223:8060'}, {'http': 'http://119.51.141.66:8060'}, {'http': 'http://175.9.244.143:8060'}, {'http': 'http://39.134.67.77:8080'}, {'http': 'http://39.73.30.34:8118'}, {'http': 'http://175.10.222.55:8060'}, {'http': 'http://222.139.58.82:8060'}, {'http': 'http://60.212.192.75:8060'}, {'http': 'http://118.76.84.124:8118'}, {'https': 'https://140.250.120.78:9999'}, {'https': 'https://121.31.193.39:8123'}, {'https': 'https://171.38.90.39:8123'}, {'https': 'https://121.31.195.30:8123'}, {'http': 'http://61.219.167.50:64312'}, {'https': 'https://171.37.163.130:8123'}, {'https': 'https://103.53.110.55:44164'}, {'https': 'https://183.173.113.121:1080'}, {'http': 'http://185.132.133.180:8080'}, {'http': 'http://47.90.11.39:8118'}, {'http': 'http://123.115.131.164:8060'}, {'http': 'http://117.63.157.163:8118'}, {'https': 'https://115.46.77.179:8123'}, {'http': 'http://117.66.166.151:8118'}, {'https': 'https://115.46.64.238:8123'}, {'http': 'http://119.134.110.121:8118'}, {'https': 'https://103.74.244.177:33719'}, {'http': 'http://103.206.103.229:23500'}, {'https': 'https://112.85.128.219:9999'}, {'https': 'https://106.91.17.155:9090'}, {'https': 'https://222.208.85.119:8123'}, {'https': 'https://122.4.28.212:9999'}, {'http': 'http://221.202.143.169:80'}, {'http': 'http://185.132.178.199:8080'}, {'http': 'http://171.42.20.204:8060'}, {'http': 'http://185.132.179.107:8080'}, {'http': 'http://115.151.132.29:8888'}, {'https': 'https://112.87.69.34:9999'}, {'https': 'https://112.87.71.122:9999'}, {'https': 'https://112.87.69.56:9999'}, {'https': 'https://45.123.203.242:30620'}, {'https': 'https://114.226.83.253:8118'}, {'https': 'https://112.87.68.66:9999'}, {'http': 'http://114.107.20.133:8888'}, {'https': 'https://112.87.68.87:9999'}, {'http': 'http://120.210.219.67:8080'}, {'https': 'https://112.85.130.112:9999'}, {'http': 'http://120.210.219.67:8080'}, {'https': 'https://112.85.130.112:9999'}, {'http': 'http://112.85.131.10:9999'}, {'http': 'http://220.198.123.214:80'}, {'http': 'http://220.198.123.214:80'}, {'https': 'https://185.132.178.203:8080'}, {'http': 'http://27.203.247.243:8060'}, {'http': 'http://115.151.132.29:8888'}, {'https': 'https://112.87.69.34:9999'}, {'https': 'https://112.87.71.122:9999'}, {'https': 'https://112.87.69.56:9999'}, {'https': 'https://45.123.203.242:30620'}, {'https': 'https://114.226.83.253:8118'}, {'https': 'https://112.87.68.66:9999'}, {'http': 'http://114.107.20.133:8888'}, {'https': 'https://112.87.68.87:9999'}, {'http': 'http://120.210.219.67:8080'}, {'https': 'https://112.85.130.112:9999'}, {'http': 'http://120.210.219.67:8080'}, {'https': 'https://112.85.130.112:9999'}, {'http': 'http://112.85.131.10:9999'}, {'http': 'http://220.198.123.214:80'}, {'http': 'http://220.198.123.214:80'}, {'https': 'https://185.132.178.203:8080'}, {'http': 'http://27.203.247.243:8060'}, {'http': 'http://115.151.132.29:8888'}, {'https': 'https://112.87.69.34:9999'}, {'https': 'https://112.87.71.122:9999'}, {'https': 'https://112.87.69.56:9999'}, {'https': 'https://45.123.203.242:30620'}, {'https': 'https://114.226.83.253:8118'}, {'https': 'https://112.87.68.66:9999'}, {'http': 'http://114.107.20.133:8888'}, {'https': 'https://112.87.68.87:9999'}, {'http': 'http://120.210.219.67:8080'}, {'https': 'https://112.85.130.112:9999'}]

    @retry(stop_max_attempt_number=10)
    def get_response(self,url):
        index = random.randint(0,len(self.proxies)-1)
        r = requests.get(url,headers=self.headers,proxies=self.proxies[index])
        return r.text

    def get_category_list(self,r):
        html = etree.HTML(r)
        category_list1 = html.xpath("//table[@class='tagCol']//td/a/@href")
        category_list = []
        for url1 in category_list1:
            url = 'https://book.douban.com' + url1
            category_list.append(url)
        return category_list

    def get_book_data(self,r):
        html = etree.HTML(r)
        li_list = html.xpath("//li[@class='subject-item']")
        books = []
        for li in li_list:
            book = {}
            book["name"] = li.xpath(".//div[@class='info']/h2/a/@title")[0] if len(li.xpath(".//div[@class='info']/h2/a/@title"))>0 else None
            book["pic"] = li.xpath("./div[@class='pic']/a/img/@src")[0] if len(li.xpath("./div[@class='pic']/a/img/@src"))>0 else None
            detail = li.xpath("./div[@class='info']/div[@class='pub']/text()")[0] if len(li.xpath("./div[@class='info']/div[@class='pub']/text()")[0])>0 else None
            book["detail"] = re.sub(r"\n\n      ",'',re.sub(r"\n        \n  \n  ",'',str(detail)))
            book["abstract"] = li.xpath("./div[@class='info']/p/text()") if len(li.xpath("./div[@class='info']/p/text()"))>0 else None
            book["num"] = li.xpath("./div[@class='info']/div[@class='star clearfix']/span[@class='rating_nums']/text()")[0] if len(li.xpath("./div[@class='info']/div[@class='star clearfix']/span[@class='rating_nums']/text()"))>0 else None
            books.append(book)
        next_url = html.xpath("//span[@class='next']/link/@href")
        print(next_url)
        next_url = 'https://book.douban.com' + next_url[0] if next_url else None
        return books,next_url

    def save_date(self,books):
        with open("doubanBook1.txt","a",encoding="utf8") as f:
            for book in books:
                f.write(json.dumps(book,ensure_ascii=False))
                f.write('\n')


    def run(self):#实现主要逻辑
        r = self.get_response(self.category_url)
        #1.分类的url_list
        category_list = self.get_category_list(r)
        for url in category_list:
        #2.发送请求获取响应
            r = self.get_response(url)
            #3.获取数据及下一页url
            books,next_url = self.get_book_data(r)
            #4.保存数据
            self.save_date(books)
            while next_url:
                r = self.get_response(next_url)
                #3.获取数据及下一页url
                books,next_url = self.get_book_data(r)
                #4.保存数据
                self.save_date(books)
                print('{}保存完成'.format(next_url))
                time.sleep(3)
        with open("doubanBook.txt", "a", encoding="utf8") as f:
            f.write('------------------\n')

if __name__ == '__main__':
    douban = DouBan()
    douban.run()