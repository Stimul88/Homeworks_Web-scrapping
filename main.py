import pprint
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


def get_headers():
    return Headers(browser="chrome", os="win").generate()


adress = "https://spb.hh.ru/search/vacancy?area=1&area=2&enable_snippets=true&ored_clusters=true&text=Python" \
         "&search_period=3/"

hh_main_html = requests.get(adress, headers=get_headers()).text

hh_main_soup = BeautifulSoup(hh_main_html, "lxml")


tag_all_main = hh_main_soup.find("main", class_="vacancy-serp-content")

tag_vacansy_a= tag_all_main.find_all("a", class_="serp-item__title")

parsed_data = []

keywords = ['Django', 'Flask']

for link_vacansy in tag_vacansy_a:
    link = link_vacansy["href"]

    nextpage = requests.get(link, headers=get_headers()).text
    nextsoup = BeautifulSoup(nextpage, "lxml")

    tag_nextsoup_div = nextsoup.find("div", class_="bloko-columns-row")

    description = tag_nextsoup_div.find('div', class_='g-user-content').text



    if 'Django' and 'Flask' in description:

        salary_fork = tag_nextsoup_div.find('div', {'data-qa': 'vacancy-salary'}).text

        company_name = tag_nextsoup_div.find('a', class_='bloko-link bloko-link_kind-tertiary').text

        city = tag_nextsoup_div.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        parsed_data.append(
                    {
                        "Ссылка": link,
                        "Вилка зп": salary_fork,
                        "Название компании": company_name,
                        "Город": city
                    }
                )

final = json.dumps(parsed_data, indent=4, ensure_ascii=False)

with open('file.json', 'w', encoding='utf-8') as f:
    f.write(final)