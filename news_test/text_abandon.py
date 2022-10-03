#--coding:utf-8--

import Chrome
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio_file
import aiohttp
import time


def crawler():
    driver = Chrome.Antispider_Chrome(fake_useragent=True,headless=1)
    wait = WebDriverWait(driver, 60)
    index_url = 'https://gu.qq.com/usMOGU.N/gg/news'
    driver.get(index_url)
    fp = open('./text.txt', 'a+', encoding='utf-8')
    def get_urllist():
        url_list = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="content_wrap"]/div[2]/div/div[3]/div/ul/li/a')))
        urllist = []
        for i in url_list:
            a_url = i.get_attribute('href')
            urllist.append(a_url)
        return urllist

    def get_text(url):
        driver.get(url)
        time.sleep(3)
        title_elemnt = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="news_title"]/span')))
        title = title_elemnt.text
        article_time_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="news_time"]')))
        article_time = article_time_element.text
        text_element = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="news-text"]/div[1]')))
        text = text_element.text
        head = title+' '+article_time+'\n'+text+'\n'
        return head
    def text(url_list):
        for url in url_list:
            text=get_text(url)
            fp.write(text)
            print(url+'写入完毕！')
        return 1
    all_url = []
    urllist = get_urllist()
    all_url= all_url+urllist
    xiayiye_button = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div/div[2]/span[2]')))
    class_name = xiayiye_button.get_attribute('class')
    while (class_name != 'disabled'):
        xiayiye_button.click()
        urllist=get_urllist()
        all_url = all_url+urllist
        xiayiye_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[2]/div/div[3]/div/div[2]/span[2]')))
        class_name = xiayiye_button.get_attribute('class')
    print('url截取完毕，现在开始写入text——————————————')
    constant_text = text(all_url)
    print(constant_text)


if __name__ == '__main__':
    crawler()







