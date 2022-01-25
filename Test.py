# import libraries
# import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
# specify the url

def scrape_nike():
    driver = webdriver.Chrome(executable_path=r"D:\Downloads\uDealio-master\chromedriver_win32\chromedriver.exe")
    url = 'https://forever21.sg/collections/sale'
    driver.get(url)

    htmlSource = driver.page_source
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    products = soup.findall('div', class_= "inner product-item on-sale")
    links = []
    titles = []
    old_prices = []
    new_prices = []
    discount_percents = []

    for product in products:
        JsonObject = product.get("data-json-product")
        print(JsonObject["handle"])
        print(JsonObject[""])
        print("testing 1")

        image = JsonObject["preview_image"]

        break

        # title = product.find('a').text
        # titles.append(title)

        # link = product.find('a',href=True)['href']
        # links.append(link)

        # pricecontainer = product.find('div',class='product-card__animation_wrapper')
        # old_price = pricecontainer.find('div',class="product-price is--striked-out").text.strip('S$')
        # old_prices.append(old_price)

        # new_price = pricecontainer.find('div',class="product-price is--current-price css-s56yt7").text.strip('S$')

        # new_prices.append(new_price)

        # discount_percent = round((float(old_price)-float(new_price))/float(old_price)*100)
        # discount_percents.append(discount_percent)
    driver.close()
    return

scrape_nike()