"""connect to site, return soup."""
import requests
from bs4 import BeautifulSoup

import logging
logging.basicConfig(format='%(asctime)s - %(module)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger("fetch_bs")

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
#user_agent = 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1' # андроид

headers = {
           'User-Agent': user_agent,
           'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
          }

def get_page(url):
    #print (url)
    """return requests.get object"""
    try:
        answer = requests.get(url,headers=headers,timeout=4)
        if answer.status_code == 200:
            return answer
    except Exception as e:
        logger.error(e)

def make_soup(page):
    return BeautifulSoup(page, 'html.parser')

def ordhash(string):
    ord_lst = [ord(x) for x in string]
    sum = sum1 = sum2 = 0
    for index,item in enumerate(ord_lst):
        if (index // 2) == 0:        
            sum1 -= item**2 + index
        else:
            sum2 += item**2 + index
        sum += sum1+sum2
    return sum
