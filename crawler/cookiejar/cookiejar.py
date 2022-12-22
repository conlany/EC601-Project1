import httplib2 as httplib2
import urllib.request
import http.cookiejar
from http import cookiejar
from lxml import etree

def getAnswerfromZhiDao(question):
    """
    Scrap answers from ZhiDao
    :param question:
    :return:
    """

    ZHIDAO = 'http://zhidao.baidu.com'
    # request = urllib.request.Request(URL)
    # request.add_header("user-agent", "Mozilla/5.0")

    #tic = time.time()
    global zhidaoHeader
    URL = ZHIDAO + "/index?rn=10&word=" + question
    # print(URL)
    Answer = []
    http = httplib2.Http()
    cookie = cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    req = urllib.request.Request(URL)
    response = opener.open(req)
#    zhidaoHeader['Cookie'] = response.headers.dict['set-cookie']
    myHeader = {
        "Cookie":"set-cookie"
    }
    response, content = http.request(URL, 'GET', headers=zhidaoHeader)
    print(response)#.read().decode('utf-8', 'ignore'))
    print(content)

    search_result_list = etree.HTML(content.lower()).xpath("//div[@class='slist']/p/a")

    # time1 = time.time()
    limit_num = 3
    for index in range(min(len(search_result_list), limit_num)):
        url = search_result_list[index].attrib['href']
        url = ZHIDAO + url
        # print(url)
        response, tar_page = http.request(url, 'GET', headers=zhidaoHeader)

        if response.previous is not None:
            if response.previous['status'][0] == '3':
                url = response.previous['location']



if __name__ == "__main__":
    getAnswerfromZhiDao("name")
