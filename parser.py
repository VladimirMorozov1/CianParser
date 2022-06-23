import requests
from bs4 import BeautifulSoup
import time


def pages(number):
    url = "https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={}&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&sort=creation_date_asc".format(number)
    response = requests.get(url)
    page_text = BeautifulSoup(response.text, "html.parser")
    links = page_text.find_all('article')
    link_list = list()
    for link in links:
        link_list.append(link.a['href'])
    return link_list


for i in range(1,3):
    print(pages(i))
    time.sleep(5)

    

