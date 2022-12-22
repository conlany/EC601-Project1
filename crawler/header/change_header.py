# -*- coding: utf-8 -*-
import re
import urllib.request,urllib.error
from imp import reload

import xlwt
#import sqlite3
import urllib.parse

import sys
reload(sys)


################
#无反爬
# def getAnswer(question):
#     ZHIDAO = 'http://zhidao.baidu.com'
#     url = ZHIDAO + "/index?rn=10&word=" + question
#     try:
#         response = urllib.request.urlopen(url,timeout=3)
#         print(response.read().decode('utf-8'))
#         print(response.status)
#         print(response.getheaders())
#     except urllib.error.URLError as e:
#         print("time out")
#
# if __name__ == "__main__":
#     getAnswer('name')
##############

###########
##有反爬
def getAnswer(question):
    ZHIDAO = 'http://zhidao.baidu.com' #baidu知道不支持post获取方式
    SOUGOU = "https://www.sogou.com/sogou?query="
    TAIL = "&ie=utf8&insite=wenwen.sogou.com&pid=sogou-wsse-a9e18cb5dd9d3ab4&rcer="
    AllSOUGOU = SOUGOU + question + TAIL
    url = ZHIDAO + "/index?rn=10&word=" + question

    data = bytes(urllib.parse.urlencode({"name":"conlan"}),encoding = "utf-8")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID=364E4FED3C507CFB2D9CFD0C0077478B:FG=1; "
        "BIDUPSID=364E4FED3C507CFB2D9CFD0C0077478B; PSTM=1608704630; "
        "BAIDUID_BFESS=364E4FED3C507CFB2D9CFD0C0077478B:FG=1; "
        "BDUSS=1LRkljeTZLd1ltflNDeUp2fmtqZFEtVGtRWXA3cloxa0RxcmlyTVNDZGNhSjVnSVFBQUFBJC"
        "QAAAAAAAAAAAEAAAAXOOA6ztLQxLu2wMoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAFzbdmBc23Zgfk; "
        "BDUSS_BFESS=1LRkljeTZLd1ltflNDeUp2fmtqZFEtVGtRWXA3cloxa0RxcmlyTVNDZGNhSjVnSVFBQUFBJCQAAAAAAAA"
        "AAAEAAAAXOOA6ztLQxLu2wMoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFzbdmBc23Zgfk;"
        " __yjs_duid=1_04db8f0392ef254b3369c055f5202d7c1619861633155; Hm_lvt_16bc67e4f6394c05d03992ea0a0e9123=1619887199; "
        "Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1620201807,1620216458,1620479428,1620483618; shitong_key_id=2; ZD_ENTRY=empty; "
        "Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1620487923; "
        "ab_sr=1.0.0_ZGE0YTMzMWFiOTZmYjEzZjZjNzE1ZGI0YmUyZmE4MDVjMjdmNTc4MWQ1NWNlZDU4MDQyODFjOTY2M2VhYzVmZDdiNWEzMWE3MzA5Nz"
        "YxNzIzMmM3NWEzMWI2ZDQwNjIx; "
        "shitong_data=9f16d48ea687b72ad81d7adbc4a923448b55fa5436a9b6004c28216241615016094a308094f8e5828f356bca1f1c1e7156d2f48"
        "a943dd7ae8bf4384d38d6aac1044612b23b76ebfa410cac7d9c17bcf29ddefdb175c115bbf44b55209dc17ee8b0e98ed54837b476f3fa0d24ff8ca8b"
        "0a22f8a9046aa99cec5bec7cabc9e1dc5; shitong_sign=99b7c989",
        "Host": "zhidao.baidu.com",
        "Referer": "https://zhidao.baidu.com/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    try:

        req = urllib.request.Request(url=url,data=data,headers=headers,method="POST")
        response = urllib.request.urlopen(req)  #注意urlopen是根据请求获得相应，未反爬是url，而反爬之后的请求是Request对象
        print(response.read().decode('utf-8', 'ignore')) #ignore的问题
        print(response.status)
        print(response.getheaders())


        obj = re.compile(r'<dt class="dt mb-3 line" alog-alias="result-title-0">[\s\S]<a href="(?P<aaa>.*?)"', re.S)
        obj = re.compile(r'<a href="(?P<aaa>.*?)"', re.S)

        result = obj.finditer(response.read().decode('utf-8', 'ignore'))
        for i in result:
            print(i.group("aaa"))
        print("finish5")

    except urllib.error.URLError as e:
        print(e.reason)



if __name__ == "__main__":
    getAnswer('cancer')

