import requests


class tiebaSpider():
    def __init__(self, name):
        self.name = name
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8&pn='.format(name)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"}

    def get_url_list(self):
        return [self.url + str(i * 50) for i in range(10)]

    def get_response(self, url):
        r = requests.get(url, headers=self.headers)
        return r.content.decode()

    def save_html(self, response, name, page):
        file_path = '{}吧-第{}页.html'.format(name, page)
        with open(file_path, 'w', encoding='utf8') as f:
            f.write(response)

    def run(self):
        # 1.获取url list
        url_list = self.get_url_list()
        for url in url_list:
            # 2.提交请求,获取响应
            r = self.get_response(url)
            page = url_list.index(url) + 1
            # 3.保存网页
            self.save_html(r, self.name, page)
            print('第{}页保存完成.......'.format(page))


if __name__ == '__main__':
    Spider = tiebaSpider('李毅')
    Spider.run()