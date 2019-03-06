from lxml import etree
import requests

class ProxiesSpider():
    def __init__(self):
        self.url = 'https://www.kuaidaili.com/free/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
        self.proxies = []
        self.pages = []

    def get_response(self,url):
        r = requests.get(url,headers=self.headers)
        return r.content.decode()

    def get_proxies(self,r):
        html = etree.HTML(r)
        tr_list = html.xpath("//tr")
        for tr in tr_list:
            proxie = {}
            ip = tr.xpath("./td[@data-title='IP']/text()")[0] if tr.xpath("./td[@data-title='IP']/text()") else None
            port = tr.xpath("./td[@data-title='PORT']/text()")[0] if tr.xpath("./td[@data-title='PORT']/text()") else None
            if ip and port:
                proxie["http"] = 'http://'+ip+':'+port
                self.proxies.append(proxie)

    def check_proxies(self):
        for proxie in self.proxies:
            try:
                response = requests.get('https://book.douban.com/tag/?view=type&icn=index-sorttags-hot',headers = self.headers,proxies=proxie,timeout = 3)
                print(response.status_code)
                assert response.status_code == 200
            except:
                print("{}此代理不可用".format(proxie["http"]))
                self.proxies.remove(proxie)

    def run(self):
        #1.url
        #2.提交请求获取响应
        #4.保存数据
        for i in range(25):
            r =  self.get_response("https://www.kuaidaili.com/free/inha/{}/".format(i+1))
            self.get_proxies(r)
        print(self.proxies)
        self.check_proxies()
        print(self.proxies)
        #检测代理的可用性

class YunProxie():
    def __init__(self):
        self.start_url = 'http://www.ip3366.net/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}
        self.proxies = []

    def get_response(self,url):
        r = requests.get(url,headers=self.headers)
        return r.content.decode("gb2312")

    def get_data(self,r):
        html=etree.HTML(r)
        ip_list = html.xpath("//tr/td[position()=1]/text()")
        port_list = html.xpath("//tr/td[position()=2]/text()")
        kind_list = html.xpath("//tr/td[position()=4]/text()")
        next_url = html.xpath("//div[@id='listnav']/ul/a[last()-1]/@href")
        next_url = "http://www.ip3366.net/"+next_url[0] if len(next_url)>0 else None
        for ip in ip_list:
            proxie = {}
            if kind_list[ip_list.index(ip)] == 'HTTP':
                proxie["http"] = "http://"+ip+':'+port_list[ip_list.index(ip)]
            else:
                proxie["https"] = "https://"+ip+':'+port_list[ip_list.index(ip)]
            self.proxies.append(proxie)
        return next_url

    def check_proxies(self):
        for proxie in self.proxies:
            try:
                response = requests.get('https://book.douban.com/tag/?view=type&icn=index-sorttags-hot',headers = self.headers,proxies=proxie,timeout = 3)
                print(response.status_code)
                assert response.status_code == 200
            except:
                print("此代理不可用")
                self.proxies.remove(proxie)

    def run(self):
        #1.发送请求获取响应
        r = self.get_response(self.start_url)
        #.获取数据
        next_url = self.get_data(r)
        while next_url:
            r = self.get_response(next_url)
            # .获取数据
            next_url = self.get_data(r)
        print(self.proxies)
        self.check_proxies()
        print(self.proxies)

if __name__ == '__main__':
    # a = ProxiesSpider()
    # a.run()
    a = YunProxie()
    a.run()
