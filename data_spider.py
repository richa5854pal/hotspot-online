# -*- coding:utf-8 -*-
import os
import time
import requests
from lxml import etree

str1 ='''{"name":"'''
str2 ='''","url": "'''
str3 ='''"},'''
try:
    os.mkdir("json")
except:
    print("json文件夹已经存在！")
#百度今日热点事件排行榜
baidu_today = "http://top.baidu.com/buzz?b=341"
#实时热点排行榜
baidu_ssrd = "http://top.baidu.com/buzz?b=1"
def parse_baidu(baidu_url,fname):
    fname = os.getcwd()+"\\json\\" +fname
    r = requests.get(baidu_url)
    r.encoding='gb2312'
    soup = etree.HTML(r.text)
    str_list = ""
    for soup_a in soup.xpath("//a[@class='list-title']"):
        hot_name = soup_a.text
        hot_url = soup_a.get('href')
        str_list = str_list + str1 + hot_name + str2+ hot_url+ str3 + "\n"
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(str_list) 

#也可以使用https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true  获取知乎热榜

#知乎全站热榜
def zhihu_rb():
    fname = os.getcwd()+"\\json\\" +"zhihu.json"
    zhihu_all = "https://www.zhihu.com/hot"
    headers = {'user-agent':'Baiduspider',
               'cookie':'此处用你自己的cookie'          
    }
    r = requests.get(zhihu_all,headers=headers)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    str_list=""
    for soup_a in soup.xpath("//div[@class='HotItem-content']/a"):
        zhihu_title = soup_a.get('title')
        zhihu_url = soup_a.get('href')
        str_list = str_list + str1 + zhihu_title + str2+ zhihu_url+ str3 + "\n"
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(str_list) 

#微博热点排行榜
def parse_weibo():
    fname = os.getcwd()+"\\json\\" +"weibo.json"
    weibo_ssrd = "https://s.weibo.com/top/summary?cate=realtimehot"
    weibo = "https://s.weibo.com"
    r = requests.get(weibo_ssrd)
    r.encoding='utf-8'
    soup = etree.HTML(r.text)
    str_list=""
    for soup_a in soup.xpath("//td[@class='td-02']/a"):
        wb_title = soup_a.text
        wb_url = weibo + soup_a.get('href')
        #过滤微博的广告，做个判断
        if "javascript:void(0)" in wb_url:
            str_list = str_list
        else:
            str_list = str_list + str1 + wb_title + str2+ wb_url+ str3 + "\n"
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(str_list)
#贴吧热度榜单
def parse_tieba():
    fname = os.getcwd()+"\\json\\" +"tieba.json"
    tb_url = "http://tieba.baidu.com/hottopic/browse/topicList?res_type=1"
    r = requests.get(tb_url)
    soup = etree.HTML(r.text)
    str_list=""
    for soup_a in soup.xpath("//a[@class='topic-text']"):
        tieba_name = soup_a.text
        tieba_url = soup_a.get('href')
        str_list = str_list + str1 + tieba_name + str2+ tieba_url+ str3 + "\n"
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(str_list)

#V2EX热度榜单
def parse_vsite():
    vsite_hoturl = "https://www.v2ex.com/?tab=hot"
    vsite ="https://www.v2ex.com"
    fname = os.getcwd()+"\\json\\" +"vsite.json"
    r = requests.get(vsite_hoturl)
    soup = etree.HTML(r.text)
    str_list=""
    for soup_a in soup.xpath("//span[@class='item_title']/a"):
        vsite_name = soup_a.text
        vsite_url = vsite+soup_a.get('href')
        str_list = str_list + str1 + vsite_name + str2+ vsite_url+ str3 + "\n"
    with open(fname,"w+",encoding='utf-8') as f:
        f.write(str_list)
    


if __name__ == "__main__":
    while True:
        try:
            parse_vsite()
            parse_tieba()
            parse_weibo()
            parse_baidu(baidu_ssrd,"baidurd.json")
            parse_baidu(baidu_today,"baidusj.json")
            zhihu_rb()
        except:
            print("采集出现一个错误，请及时更新规则！")
        time.sleep(600) #每隔600秒也即十分钟更新一次
