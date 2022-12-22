import http
import re
import urllib.request,urllib.error
from selenium import webdriver
# import httplib2
import xlwt
#import sqlite3
import urllib.parse
from lxml import etree
import requests
#from lxml import webdriver
import selenium.webdriver
location = 'https://www.mayoclinic.org/diseases-conditions/heart-attack/symptoms-causes/syc-20373106'

def getUrl(html):
    reg = r'<h3?href="(.+?)"'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,html)
    return urllist

def getAnswer(question):

    google = "https://www.mayoclinic.org/diseases-conditions/"
    oriG = "https://www.google.com.hk/search?q="
    ZHIDAO = 'http://zhidao.baidu.com'  # baidu知道不支持post获取方式
    url = oriG + question
    url = ZHIDAO + "/index?rn=10&word=" + question
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\Google\Chrome Dev\Application\chrome.exe"
    path = r'C:\Users\Yang Shu\Desktop\driver2\chromedriver2.exe'
    driver = selenium.webdriver.Chrome(path,chrome_options=options)
    # driver.implicitly_wait(10)
    driver.get(google)
    element = driver.find_element('id','azureSiteSearchTerm')
    element.send_keys('heart attack\n')
    import time
    time.sleep(5)
    data = driver.page_source
    myLink = driver.find_element('id','b7b1c41a35e845c7afa0570b78c9ea93')
    # mylist = driver.find_element('class_name','noimg')
    # myLink = driver.find_element('xpath','//h3//a')
    myLink = driver.find_element('xpath', '//h3//a')
    myLink.click()
    data = driver.page_source
    introduction = driver.find_element('xpath','//div[contains(@class,"content")]//div//p')
    list1 = getUrl(driver.page_source)
    file_path="D:/helloworld2.html "
    with open(file_path,'w',encoding="utf-8") as f:
        f.write(data)


    # # param = {
    # #     'type': '24',
    # #     'interval_id': '100:90',
    # #     'action': '',
    # #     'start': '0',
    # #     'limit': '20'
    # # }
    # header = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    #     "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    #     "accept-encoding": "gzip, deflate, br",
    #     "cache-control": "max-age=0",
    #     "referer": "https://www.google.com.hk/",
    #     'sec-ch-ua': 'Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-fetch-dest": "document",
    #     'cookie': 'AKA_A2=A; 45293=; TiPMix=35.0814179215028; x-ms-routing-name=self; patientconsumer#lang=en; ARRAffinity=acd238d147a0b70274b769a1815efd41db1a6c1460dbcd848ef34755d1e6a7a0; ARRAffinitySameSite=acd238d147a0b70274b769a1815efd41db1a6c1460dbcd848ef34755d1e6a7a0; ApplicationGatewayAffinity=59eee80334fb3f5bcf14d4d2138390fa901ba98788ff036a636e71820759d479; ApplicationGatewayAffinityCORS=59eee80334fb3f5bcf14d4d2138390fa901ba98788ff036a636e71820759d479; _uetsid=e8ea5fa0bad311eb974ef795241d90a5; _uetvid=e8ea8720bad311eb9fee132a3c9bad63; _ga=GA1.2.1559892176.1621670487; _gid=GA1.2.1570240729.1621670487; _gcl_au=1.1.2040041791.1621670488; _gat=1; _sess=23929ef8-dfed-4e0d-9353-2d8bf25ef5b5.6838df30-e504-497d-aa8e-1f86ac3619c6.1621670488.1; dmd-vid=6838df30-e504-497d-aa8e-1f86ac3619c6; dmd-sid=23929ef8-dfed-4e0d-9353-2d8bf25ef5b5; dmd-ahk=93bfa99412; dmd-signal-105-478-061A5F57-23929ef8-dfed-4e0d-9353-2d8bf25ef5b5=e30=; __gads=ID=090aa2da27c7c847:T=1621670488:S=ALNI_Ma3ZYINHFkRFtkaJBi7m2LzfyYfwA; RT="z=1&dm=www.mayoclinic.org&si=a2000495-8c45-4f60-aba2-e0e618465195&ss=kozgqhro&sl=1&tt=7hu&bcn=%2F%2F684fc53e.akstat.io%2F&ld=7hx&ul=yvw"; ADRUM=s=1621670529313&r=https%3A%2F%2Fwww.mayoclinic.org%2Fdiseases-conditions%2Flung-cancer%2Fsymptoms-causes%2Fsyc-20374620%3F0'
    #
    #
    # }
    # # resp = requests.get(url=url,  headers=header)
    # print(resp)
    # page_content = resp.text
    # print(resp.text) #.json())
    # it3 = re.finditer(r"\d+", page_content)
    # for i in it3:
    #     print(i.group())
    # print("finish5")
    #
    # http = httplib2.Http()
    # nResponse, content = http.request(url, 'GET', headers=header)
    # search_result_list = etree.HTML(content.lower()).xpath("//div[@class='slist']/p/a")
    # # time1 = time.time()
    # limit_num = 3
    # # for index in range(min(len(search_result_list), limit_num)):
    # #     url = search_result_list[index].attrib['href']
    # #     url = ZHIDAO + url
    # #     print(url)
import datetime
import time
if __name__ == "__main__":
    # import time
    # from selenium import webdriver
    # from selenium.webdriver.common.by import By
    # from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
    # from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
    #
    # driver = webdriver.Firefox()
    # driver.get("https://www.baidu.com")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "kw")))
    # driver.find_element_by_id("kw").clear()  # 清空里面已有的输入
    # driver.find_element_by_id("kw").send_keys("P2P")  # 在里面输入P2P搜索词
    # driver.find_element_by_id("su").click()  # 点击搜索按钮
    #
    # for i in range(2, 5, 1):
    #     time.sleep(1)
    #     e_item = driver.find_elements_by_xpath('//div[@class="result c-container "]')
    #     print('\n'.join([e.find_element_by_tag_name('a').text for e in e_item]))
    #     driver.find_element_by_xpath(f"//div[@id='page']/descendant::span[text()='{i}']").click()
    #


    getAnswer('heart attack')