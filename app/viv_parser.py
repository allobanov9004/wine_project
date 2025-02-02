import requests
from bs4 import BeautifulSoup
from time import sleep

from models import Wine
from db import db_session



wines_to_db = []

headers = {"User-Agent":
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091101 Firefox/3.5.5 (.NET CLR 3.5.30729)"}


def get_url():
    for c in range(1, 8):
        url = f"https://www.vivino.com/explore?currency_code=RUB&min_rating=1&order_by=ratings_average&order=desc&page={c}&price_range_max=12500&price_range_min=0&vc_only=&wsa_year=null&discount_prices=false&country_codes[]=ru&country_codes[]=ge&wine_type_ids[]=1&wine_type_ids[]=2&wine_type_ids[]=3&wine_type_ids[]=4&wine_type_ids[]=7&wine_type_ids[]=24" #russia and georgia

        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("div", class_="wineCard__wineCard--2dj2T wineCard__large--1tkVl")
        for i in data:
            card_url = "https://vivino.com" + i.find("a").get("href")
            print(card_url)
            yield card_url

for card_url in get_url():
    response = requests.get(card_url, headers=headers)
    sleep(1)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find("div", class_="grid topSection")
    # print(data)
    name = data.find("a", {"data-cartitemsource":"wine-page-master-link"}).text.strip()
    year = data.find("div", class_="wineHeadline-module__vintage--1UHSo").text.split()[-1].strip()
    winery = data.find("a", {'data-cy':"breadcrumb-winery"}).text
    wine_type = data.find("a", {'data-cy':"breadcrumb-winetype"}).text
    country = data.find("a", {'data-cy':"breadcrumb-country"}).text
    region = data.find("a", {'data-cy':"breadcrumb-region"}).text
    grape = data.find("a", {'data-cy': "breadcrumb-grape"}).text
    viv_rating = data.find("div", class_="vivinoRating_averageValue__uDdPM").text
    img_url = "https:" + data.find("img").get("src")
    if data.find("span", class_="purchaseAvailabilityPPC__amount--2_4GT") == None:
        avg_price = 0
    else:
        avg_price = data.find("span", class_="purchaseAvailabilityPPC__amount--2_4GT").text

    wines = {"wine_name": name, "wine_type": wine_type, "winery_name": winery, "country": country, "region": region, "grape": grape, "year": year, "avg_price": avg_price, "viv_rating": viv_rating, "img_link": img_url}
    wines_to_db.append(wines)
    
    print('название: ', name, "\n Год: ", year,'\n компания:', winery,'\n тип вина:', wine_type,'\n страна производства:', country,'\n регион:', region,'\n тип винограда:', grape,'\n рейтинг вивино:', viv_rating,'\n средняя цена', avg_price, '/',img_url, "\n")

# print(wines_to_db)

db_session.bulk_insert_mappings(Wine, wines_to_db)
db_session.commit()