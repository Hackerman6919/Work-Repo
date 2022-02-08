# import libraries
from typing import KeysView
import urllib.request
from pydantic import Json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# specify the url

def scrape_nike():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\Chrome Driver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.nike.com/sg/w/sale-3yaep'
    driver.get(url)
    time.sleep(5)
    htmlSource = driver.page_source
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    products = soup.find_all('div', class_ = "product-card__body")
    links = []
    titles = []
    old_prices = []
    new_prices = []
    discount_percents = []
    for product in products:
        title = product.find('a').text
        titles.append(title)

        link = product.find('a',href=True)['href']
        links.append(link)
        
        price_container = product.find('div',class_='product-card__animation_wrapper')
        old_price = price_container.find('div',class_="product-price is--striked-out").text.strip('S$')
        old_prices.append(old_price)

        new_price = price_container.find('div',class_="product-price is--current-price css-s56yt7").text.strip('S$')

        new_prices.append(new_price)

        discount_percent = round((float(old_price)-float(new_price))/float(old_price)*100)
        discount_percents.append(discount_percent)

    print(old_prices)
    driver.close()
    return
# scrape_nike()

def scrape_uniqlo_women():
    driver = webdriver.Chrome(executable_path=r'D:\DOWNLOADS\Chrome Driver\chromedriver_win32\chromedriver.exe')
    url = 'https://www.uniqlo.com/sg/en/feature/limited-offers/women'
    driver.get(url)
    time.sleep(5)
    htmlSource = driver.page_source
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    products = soup.find_all('div', class_ = "fr-grid-item w4")
    print(products)
    links = []
    titles = []
    old_prices = []
    new_prices = []
    discount_percents = []
    #for product in products:
    driver.close()
    return

# scrape_uniqlo_women()



# Link not working
def scrape_asos():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\Chrome Driver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.asos.com/women/sale/cat/?cid=7046&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&page=2'
    driver.get(url)
    time.sleep(5)
    htmlSource = driver.page_source
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    products = soup.find_all('div', class_ = "product-card-content-badges-wrapper___2brrU")
    links = []
    titles = []
    old_prices = []
    new_prices = []
    discount_percents = []
    for product in products:
        title = product.find('gl-paragraph gl-paragraph--s gl-product-card__title').text
        titles.append(title)

        # price_container = product.find('div',class_='product-card__animation_wrapper')
        old_price = product.find('div',class_="gl-price-item gl-price-item--crossed notranslate").text.strip('S$')
        old_prices.append(old_price)

        new_price = product.find('div',class_="gl-price-item gl-price-item--sale notranslate").text.strip('S$')

        new_prices.append(new_price)

        discount_percent = round((float(old_price)-float(new_price))/float(old_price)*100)
        discount_percents.append(discount_percent)
    print(old_prices)
    driver.close()
    return


def scrape_forever21():
    driver = webdriver.Chrome(executable_path=r"D:\Downloads\uDealio-master\chromedriver_win32\chromedriver.exe")
    url = 'https://forever21.sg/collections/sale'
    driver.get(url)
    time.sleep(5)
    r = requests.get(url)
    
    driver.maximize_window()
    time.sleep(1)

    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    count = 0 
    while not reached_page_end:
        
        for i in range(0,30):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource, 'html.parser')
            if soup.find("div",class_="sc-fznxsB kWAcuz sc-fznMAR kvbDRc privy-widget-popup"):
                driver.find_element_by_css_selector('sc-fzoiQi ozSmQ privy-dismiss-content').click()
                # closebutton = driver.find_element_by_id("Oval")
                # closebutton.click()
            else:
                print("popup not found")    
            
        count = count+1
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if count >1:
            reached_page_end = True
        elif last_height == new_height:
            reached_page_end = True 
        else:
            last_height=new_height
    
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    products = soup.find_all('div', class_ = "grid-item col-6 col-md-4 col-lg-3")
    print(len(products))
    titles = []
    ImageLinks = []
    temp_list = []
    for product in products:
        # JsonObject = product.find('div',class_="inner product-item on-sale")
        
        link = product.find('a', class_="product-title change-text",href=True)['href']
        link1 = "https://forever21.sg/" + link
        
        #Takin
        fulltitle = product.find('a',class_="product-title change-text") 
        title = fulltitle.find('span').text.strip()
        titleAddon = fulltitle.find_all('span')[1].text
        CombinedTitle = title+ titleAddon
        titles.append(title+titleAddon)
        
        #Take Image Link
        images = product.find_all("picture")
        image = images[0].find_all("source")[0].attrs['data-srcset']
        ImageLinks.append(image)

        try:

            pricelist = product.find("div",class_="price-regular")
            newprice = pricelist.text.strip()
            old_price = ""
            discount_percent = ""
            
        except:
            pricelist = product.find("div",class_="price-sale")
            old_price = pricelist.find('span',class_="old-price").text
            newprice = pricelist.find('span',class_='special-price').text
            discount_percent = round((float(old_price.strip("$"))-float(newprice.strip("$")))/float(old_price.strip("$"))*100)
            discount_percent1 = str(abs(discount_percent)) + "%"
        temp = {"author": url, "title":CombinedTitle, "link": link1, "tags": "Forever 21", "scrapedPostImage":image, "New Price":newprice, "Old Price":old_price, "Discount Percent":discount_percent1}
        temp_list.append(temp)
    
    driver.close()

    print(temp_list)
    return

scrape_forever21()
