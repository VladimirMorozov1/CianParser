import requests
from bs4 import BeautifulSoup
import time
#import re


def pages(page_number: int) -> list:
    url = f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&only_flat=1&p={page_number}&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&sort=creation_date_asc"
    headers = {'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    response = requests.get(url, headers = headers)
    page_text = BeautifulSoup(response.text, "html.parser")
    links = page_text.find_all('article')

    link_list = list()
    for link in links:
        link_list.append(link.a['href'])

    return link_list



def collect_links(first_page: int, last_page: int) -> set:
    set_of_links = set()
    for current_page in range(first_page,last_page):
        set_of_links.update(pages(current_page))
        time.sleep(2) # implement this line to avoid getting blocked on a website
    
    return set_of_links



def collect_flat_data(link: str) -> dict:
    headers = {'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    response = requests.get(link, headers = headers)
    text = BeautifulSoup(response.text, "html.parser")
    
    flat_data = dict()

    flat_data["Link"] = link
    flat_data["Name"] = text.find("h1", attrs = {'class': 'a10a3f92e9--title--UEAG3'}).string

    flat_data["address"] = text.find_all("a", attrs = {'class': 'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})
    # flat_data["Region"] = address[0].string
    # flat_data["Area"] = address[1].string
    # flat_data["District"] = address[2].string
    # flat_data["Street"] = address[3].string
    # flat_data["House_number"] = address[4].string

    flat_data["main_attributes"] = text.find_all("div", attrs = {'class': 'a10a3f92e9--info-value--bm3DC'})
    # flat_data["Total_S"] = main_attributes[0].string[:-3].replace(',', '.') # could be converted to float
    # flat_data["Living_S"] = main_attributes[1].string[:-3].replace(',', '.') # could be converted to float
    # flat_data["Kitchen_S"] = main_attributes[2].string[:-3].replace(',', '.') # could be converted to float
    # flat_data["Floor"] = main_attributes[3].string.split()[0] # could be converted to int
    # flat_data["Number_of_floors"] = main_attributes[3].string.split()[2] # could be converted to int
    # flat_data["Construction_year"] = main_attributes[4].string # could be converted to int

    flat_data["Description"] = text.find('p', attrs = {'class': 'a10a3f92e9--description-text--YNzWU'}).string

    additional_names = [attr_name.string for attr_name in text.find_all("span", attrs = {'class': 'a10a3f92e9--name--x7_lt'})]
    additioinal_values = [attr_value.string for attr_value in text.find_all("span", attrs = {'class': 'a10a3f92e9--value--Y34zN'})]
    additional_attributes = dict()
    for i in range(len(additional_names)):
        additional_attributes[additional_names[i]] = additioinal_values[i]
    flat_data["Additional_attributes"] =  additional_attributes

    house_info_names = [house_name.string for house_name in text.find_all("div", attrs = {'class': 'a10a3f92e9--name--pLPu9'})]
    house_info_values = [house_value.string for house_value in text.find_all("div", attrs = {'class': 'a10a3f92e9--value--G2JlN'})]
    house_attributes = dict()
    for i in range(len(house_info_names)):
        house_attributes[house_info_names[i]] = house_info_values[i]
    flat_data["House_attributes"] = house_attributes
    
    return flat_data
