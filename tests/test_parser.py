import unittest
from bs4 import BeautifulSoup
from cian_parser import parser
import requests


def test_aggregated_list(first, last_page):
    result = parser.collect_links(first, last_page)
    print("Function returned a set with length: {}".format(len(result)))


def status():
    url = "https://spb.cian.ru/sale/flat/275213046/"
    response = requests.get(url)
    return response.status_code


def page_text():
    url = f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&only_flat=1&p=2&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&sort=creation_date_asc"
    headers = {'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'}
    response = requests.get(url, headers = headers)
    page_text = BeautifulSoup(response.text, "html.parser")
    return page_text


if __name__ == "__main__":
    print(status())
    print(page_text())
    print(test_aggregated_list(1,4))
    print(parser.collect_flat_data('https://spb.cian.ru/sale/flat/275213046/'))
