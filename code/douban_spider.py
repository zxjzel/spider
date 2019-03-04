import requests
from lxml import etree
import time
import re
import json

class DouBan():
    def __init__(self):
        self.category_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

    def get_response(self,url):
        r = requests.get(url,headers=self.headers)
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
        next_url = 'https://book.douban.com' + str(next_url[0]) if next_url else None
        return books,next_url

    def save_date(self,books):
        with open("doubanBook.txt","a",encoding="utf8") as f:
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
        with open("doubanBook.txt", "a", encoding="utf8") as f:
            f.write('------------------\n')

if __name__ == '__main__':
    douban = DouBan()
    douban.run()