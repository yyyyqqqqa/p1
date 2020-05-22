import time
import requests
import json
from lxml.html import etree
import pandas as pd,csv


class HanFengSpider:
    def __init__(self):

        self.start_url = "http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do"
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Referer': 'http://www.ccgp-hunan.gov.cn/page/notice/more.jsp?prcmMode=01'
        }
        self.data = {
            'pType':'01',
            'page':'1',
            'pageSize':'18',
            'startDate':'2020-01-01',
            'endDate':'2020-04-19',
            'nType':'prcmNotices'
        }
        self.first = True

    def parse_html(self,data):
        data = requests.post(self.start_url, data=data, headers=self.headers)
        data = json.loads(data.text)
        return data["rows"]


    def run(self):

        count = 1
        while True:

            time.sleep(1)

            data = self.data
            print(count)

            data['page'] = str(count)

            count += 1

            infos = self.parse_html(data)

            for i in range(len(infos)):
                NOTICE_ID = infos[i]["NOTICE_ID"]

                cont_url  = "http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId={}&area_id=".format(NOTICE_ID)

                self.all_xiangmu(cont_url)

            if len(infos) < 18:
                break

    def all_xiangmu(self,cont_url):
        response = requests.get(cont_url, headers=self.headers).text
        selector = etree.HTML(response)
        if not selector:
            return

        data = {}
        data['开标时间'] = self.get_content(selector, '开标时间')
        if data['开标时间'] is None:
            return

        data['开标地点'] = self.get_content(selector, '开标地点')
        data['项目名称'] = self.get_content(selector, '项目名称')
        data['政府采购计划编号'] = self.get_content(selector, '政府采购计划编号')
        data['项目负责人'] = self.get_content(selector, '项目负责人')
        data['联系电话'] = self.get_content(selector, '联系电话')
        data['采购方式'] = self.get_content(selector, '采购方式')
        data['采购预算'] = self.get_content(selector, '采购预算')
        data['投标截止时间'] = self.get_content(selector, '投标截止时间')

        if len( data['投标截止时间']) > 30:
            print(cont_url)

        try:
            dizhi = self.get_content_double(selector, '地  址')
            data["采购地址"], data["采购代理地址"] = dizhi[0], dizhi[1]
        except:
            dizhi = self.get_content_double(selector, '地 址')
            data["采购地址"], data["采购代理地址"] = dizhi[0], dizhi[1]

        lianxiren = self.get_content_double(selector, '联系人')
        data["采购联系人"], data["采购代理联系人"] = lianxiren[0], lianxiren[1]
        data["采购电话"] = self.get_content(selector, '电话')
        data["采购代理电话"] = self.get_content(selector, '电  话')
        if not data["采购代理电话"]:
            data["采购代理电话"] = self.get_content(selector, '电 话')

        if not data['开标地点']:
            print(cont_url)
            print(data)
        # self.save(data)

    def get_content_double(self, selector, name):
        ele = selector.xpath("//span[contains(text(),'%s')]" % name)
        if len(ele) >2 :
            ele = ele[-2:]
        return ele[0].xpath("./text()")[0].split("：")[1] , ele[1].xpath("./text()")[0].split("：")[1]

    def get_content(self,selector, name):
        ele = selector.xpath("//span[contains(text(),'%s')]" %name)
        if name == '电话':
            return ele[-1].xpath("./text()")[0].split("：")[1] if ele else " "
        else:
            a = ''
            for i in ele:
                 try:
                     i.xpath("./text()")[0].split("：")[1]
                     a = i
                     break
                 except:
                     continue

            if a!='':
                return a.xpath("./text()")[0].split("：")[1] if ele else " "

    def save(self,data):

        h = list(data.keys())

        with open('湖南2.csv','a',encoding='utf8',newline='') as f:

            w = csv.DictWriter(f,h)
            if self.first:
                w.writeheader()
                self.first = False

            w.writerow(data)


if __name__ == '__main__':

    hanfeng = HanFengSpider()
    hanfeng.run()



