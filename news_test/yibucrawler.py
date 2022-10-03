#--coding:utf-8--

import Chrome
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio_file
import aiohttp
import time
import re
import random
from fake_useragent import UserAgent

zhanghaochizi = [['9fcdaba16ec0cd20ba4030b534f62e0f', '1080'],
                 ['cd380dd77a4f4f4f063f5e8a5600e835', '8060'],
                 ['962406db8702494f55199a0e5ceefc7f', '1292'],
                 ['19b6039860e7966e04c79ebe130e92dc', '1477'],
                 ['78a2244a6617131cc7bf54bb9606de45', '5840'],
                 ['4274a04f845cb65d14f50a19a445f13e', '8228'],
                 ['eb4e00370f618ca8611e1211d5b3c220', '6589'],
                 ['68a622c6ac3e21d2a18baa6425618f4e', '2533'],
                 ['a0519c78fea3819dce81e62dd5f99b4f', '1298']
                 ]
ua =UserAgent()
fake_useragent = ua.random
headers = {
    'User-Agent':fake_useragent
}
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
    async def yibu(urllist):
        start = time.time()
        async with aiohttp.ClientSession() as session:
            for url in urllist:
                id = re.findall('id=(.*?)&', url, re.S)
                rand = random.randint(0, 8)
                url = 'https://snp.tenpay.com/cgi-bin/snpgw_unified_newsinfo.fcgi'
                param = {
                    "filter": "0",
                    "news_id": id,
                    "zappid": "zxg_h5",
                    "sign": zhanghaochizi[rand][0],
                    "nonce": zhanghaochizi[rand][1],
                    "reserve": "1572995",
                    "": "",
                    "channel": "szxg",
                    "user_openid": "undefined"
                }
                async with session.get(url=url, params=param, headers=headers) as response:
                    r = await response.json()
                    m = r.get('news_info').get('content').get('data')
                    text = ''
                    for dict in m:
                        print(dict.values())
                await asyncio.sleep(random.randint(1, 3))
        end = time.time()
        print(end - start)

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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yibu(all_url))
    print('结束')
if __name__ == '__main__':
    crawler()







