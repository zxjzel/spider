from selenium import webdriver
import json
import time

class HuYa():
    def __init__(self):
        self.star_url = 'https://www.huya.com/l'
        self.driver = webdriver.Chrome()

    def get_response(self):
        li_list = self.driver.find_elements_by_xpath('//ul[@class=\'live-list clearfix\']/li')
        data = []
        for li in li_list:
            room = {}
            try:
                room['room_url'] = li.find_element_by_xpath('./a').get_attribute('href')
                room['room_pic'] = li.find_element_by_xpath('./a[@target=\'_blank\']/img').get_attribute('data-original')
                room['room_name'] = li.find_element_by_xpath('./a[@class=\'title new-clickstat\']').text
                room['auther_name'] = li.find_element_by_xpath('.//span[@class=\'avatar fl\']/i').text
                data.append(room)
            except:
                print("出现异常，重新获取")
                room['room_url'] = li.find_element_by_xpath('./a').get_attribute('href')
                room['room_pic'] = li.find_element_by_xpath('./a[@target=\'_blank\']/img').get_attribute('data-original')
                room['room_name'] = li.find_element_by_xpath('./a[@class=\'title new-clickstat\']').text
                room['auther_name'] = li.find_element_by_xpath('.//span[@class=\'avatar fl\']/i').text
                data.append(room)
        next_url = self.driver.find_elements_by_xpath('//a[@class=\'laypage_next\']')
        next_url = next_url[0] if len(next_url)>0 else None
        return data,next_url

    def save_data(self,data):
        with open(r'room.txt','a',encoding='utf8') as f:
            for data in data:
                f.write(json.dumps(data,ensure_ascii=False)+'\n')
        print('保存完成')

    def run(self):#实现主要逻辑
        #1.star_url
        #2.提交请求获取响应
        self.driver.get(self.star_url)
        #3.获取数据，和下一页url
        data,next_url = self.get_response()
        next_url.click()
        time.sleep(5)
        #4.保存数据
        self.save_data(data)
        while next_url:
            data,next_url = self.get_response()
            next_url.click()
            time.sleep(3)
            self.save_data(data)

if __name__ == '__main__':
    huya = HuYa()
    huya.run()