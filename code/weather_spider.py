import requests
import re
from retrying import retry
from lxml import etree
import time


class someERROR(Exception):
    pass

class weather_spider():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

    @retry(stop_max_attempt_number=10)
    def get_response(self,url):
        r = requests.get(url,headers=self.headers)
        if len(r.text)<500:
            raise someERROR
        else:
            return r.text

    def get_url_list(self):
        r = self.get_response('http://www.tianqihoubao.com/lishi/beijing.html')
        html = etree.HTML(r)
        url_list1 = html.xpath('//div[@class=\'box pcity\']//li/a/@href')[:99]
        url_list = []
        for url in url_list1:
            url_list.append('http://www.tianqihoubao.com' + url)
        return url_list

    def get_data(self,html_str):
        html = etree.HTML(html_str)
        data_list1 = html.xpath('//td/a/text()')
        data_list = []
        for data1 in data_list1:
            data = data1[45:56]
            data_list.append(data)
        detail_list1 = html.xpath('//tr[position()>1]/td[position()>1]/text()')
        detail_list=[]
        for detail1 in detail_list1:
            detail_list.append(re.sub(r'\r\n                                    ','',re.sub('\\r\\n                                        ','',detail1)))
        return data_list,detail_list

    def save_data(self,data_list,detail_list):
        detail1 = detail_list[::3]
        detail2 = detail_list[1::3]
        detail3 = detail_list[2::3]
        with open('weather.txt','a',encoding='utf8') as f:
            for i in range(len(data_list)):
                f.write(data_list[i]+' '+detail1[i] + ' ' +detail2[i]+' '+detail3[i]+' ')
                f.write('\n')

    def run(self):#实现主要逻辑
        #1.url_list
        url_list = self.get_url_list()
        for url in url_list:
            #2.提交请求，获取响应
            r = self.get_response(url)
            #3.提取数据
            data,detail = self.get_data(r)
            #4.保存数据
            self.save_data(data,detail)
            print(url+'保存完成')
            time.sleep(3)


if __name__ == '__main__':
    tianqi = weather_spider()
    tianqi.run()
