import requests
from bs4 import BeautifulSoup


def pages(page_number: int) -> list:
    url = f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&only_flat=1&p={page_number}&region=2&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&sort=creation_date_asc"
    headers = {'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'}
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
        # time.sleep(2) # implement this line to avoid getting blocked on cian
    
    return set_of_links



def collect_flat_data(link: str) -> dict:
    headers = {'user-agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'}
    response = requests.get(link, headers = headers)
    text = BeautifulSoup(response.text, "html.parser")
    
    flat_data = dict()

    flat_data["Link"] = link
    flat_data["Name"] = text.find("h1", attrs = {'class': 'a10a3f92e9--title--UEAG3'}).string

    flat_data["Address"] = ",".join([ad.string for ad in text.find_all("a", attrs = {'class': 'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})])

    main_attribute_names = [main_name.string for main_name in text.find_all("div", attrs = {'class': 'a10a3f92e9--info-title--JWtIm'})]
    main_attribute_values = [main_value.string for main_value in text.find_all("div", attrs = {'class': 'a10a3f92e9--info-value--bm3DC'})]
    main_attributes = dict()
    for i in range(len(main_attribute_names)):
        main_attributes[main_attribute_names[i]] = main_attribute_values[i]
    flat_data["Main_attributes"] = main_attributes

    flat_data["Description"] = text.find('p', attrs = {'class': 'a10a3f92e9--description-text--YNzWU'}).string.replace("'", " ")

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

    for key, value in flat_data.items():
        if type(value) == None:
             flat_data[key] = "UNSPECIFIED"
    
    return flat_data