from cian_parser import parser
import requests

def test_aggregated_list(first, last_page):
    result = parser.collect_links(first, last_page)
    print("Function returned a set with length: {}".format(len(result)))


def status():
    url = "https://spb.cian.ru/sale/flat/163166174/"
    response = requests.get(url)
    return response.status_code


if __name__ == "__main__":
    print(status())
    print(test_aggregated_list(1,2))
    print(parser.collect_flat_data('https://spb.cian.ru/sale/flat/163166174/'))
