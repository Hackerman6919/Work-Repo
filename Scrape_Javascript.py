# import libraries
from logging import exception
from typing import KeysView
import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

def scrape_asos_men_accessories():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&refine=attribute_10992:61384'
    driver.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    r = requests.get(url,headers=headers)
                                    
    driver.maximize_window()

    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    
    reached_page_end = False
    test_counter_to_remove = 0

    while reached_page_end == False and test_counter_to_remove <=1:
        for i in range(0,30):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        if bool(soup.find_all("a",class_="_39_qNys")) == True:
            driver.find_element_by_class_name('_39_qNys').click()
            time.sleep(1)
            test_counter_to_remove +=1

        else:
            reached_page_end = True
            
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    sections = soup.find_all("section",class_="_3YREj-P")
    products = []
    for i in sections:
        product = i.find_all("article",class_="_2qG85dG")
        for z in product:
            products.append(z)

    TempCollated = []
    error_links = []
    error = 0
    for i in products: 
        try:
            Product_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            # print(Product_Link)
            driver.get(Product_Link)
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource,'html.parser')

            product_info = soup.find('div',class_="product-hero").text #soup .find not = None, use if else statement, do an else to find another type of class that can show product info
            product_info1 = str(product_info).split("\n")
            while("" in product_info1) :
                product_info1.remove("")
            
            Product_title = product_info1[0]

            product_prices = product_info1[1]
            prices_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', product_prices)]
            Old_price = prices_list[0]

            New_price = prices_list[1]

            Discount = abs(prices_list[2])

            Colour = soup.find('span',class_="product-colour").text
            Image = soup.find("img",class_="gallery-image")['src']

            Product_Descriptions = soup.find("div",class_="product-description")
            if len(Product_Descriptions.find_all('a',href=True)) == 1:

                Product_Descriptions_split = str(BeautifulSoup(Product_Descriptions.prettify().split("<br/>")[0],"html.parser").text).split("\n")
                Apparel_and_Brand = []
                for string in Product_Descriptions_split:
                    if (string.strip() != ""):
                        Apparel_and_Brand.append(string.strip())
                Apparel = Apparel_and_Brand[1]
                FullBrand = Apparel_and_Brand[2]
                Brand = FullBrand[3:]
            
            else:
                product_description1 = Product_Descriptions.find_all('a',href=True)
                prdouct_description = []
                for x in product_description1:
                    prdouct_description.append(x.text)
                print(prdouct_description)
                Apparel = prdouct_description[0]
                Brand = prdouct_description[1]
            Styles = ["Cropped","Cut Out", "Denim","Grandada Collar", "Jersey Shorts", "Longline", "Muscle", "Novelty", "Other", "Overshirts", "Oversized", "Oxford","Racer Back","Raglan","Regular fit","Raglan","Relaxed","Shackets","Skinny","Slim","Sports Shorts","Straight Leg","Tapered","Track","Western"]
            
            temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":Apparel }
            TempCollated.append(temp)
        except Exception as e:
            error += 1
            error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            error_links.append(error_Link)
            continue

    print(error_links)
    print(len(error_links))
    print(len(TempCollated))
    print(TempCollated[0])
    driver.close()
    return

scrape_asos_men_accessories()

print("\n")

def scrape_asos_men_shirts():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&refine=attribute_10992:61383'
    driver.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    r = requests.get(url,headers=headers)
    
    driver.maximize_window()

    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    
    reached_page_end = False
    test_counter_to_remove = 0

    while reached_page_end == False and test_counter_to_remove <=1:
        for i in range(0,30):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        if bool(soup.find_all("a",class_="_39_qNys")) == True:
            driver.find_element_by_class_name('_39_qNys').click()
            time.sleep(1)
            test_counter_to_remove +=1

        else:
            reached_page_end = True
            
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    sections = soup.find_all("section",class_="_3YREj-P")
    products = []
    for i in sections:
        product = i.find_all("article",class_="_2qG85dG")
        for z in product:
            products.append(z)

    TempCollated = []
    error_links = []
    error = 0
    for i in products: 
        try:
            Product_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            # print(Product_Link)
            driver.get(Product_Link)
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource,'html.parser')

            product_info = soup.find('div',class_="product-hero").text #soup .find not = None, use if else statement, do an else to find another type of class that can show product info
            product_info1 = str(product_info).split("\n")
            while("" in product_info1) :
                product_info1.remove("")
            
            Product_title = product_info1[0]

            product_prices = product_info1[1]
            prices_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', product_prices)]
            Old_price = prices_list[0]

            New_price = prices_list[1]

            Discount = abs(prices_list[2])

            Colour = soup.find('span',class_="product-colour").text
            
            Product_Descriptions = soup.find("div",class_="product-description")
            
            product_description1 = Product_Descriptions.find_all('a',href=True)
            
            prdouct_description = []
            for x in product_description1:
                prdouct_description.append(x.text)
            
            Apparel = prdouct_description[0]
            Brand = prdouct_description[1]

            Image = soup.find("img",class_="gallery-image")['src']
            
            temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":Apparel }
            TempCollated.append(temp)
        except Exception as e:
            error += 1
            error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            error_links.append(error_Link)
            continue

    print(error_links)
    print(len(error_links))
    print(len(TempCollated))
    print(TempCollated[0])
    driver.close()
    return

scrape_asos_men_shirts()

print("\n")

def scrape_asos_men_bottom():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61375,61377'
    driver.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    r = requests.get(url,headers=headers)
    
    driver.maximize_window()

    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    
    reached_page_end = False
    test_counter_to_remove = 0

    while reached_page_end == False and test_counter_to_remove <=1:
        for i in range(0,30):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        if bool(soup.find_all("a",class_="_39_qNys")) == True:
            driver.find_element_by_class_name('_39_qNys').click()
            time.sleep(1)
            test_counter_to_remove +=1

        else:
            reached_page_end = True
            
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    sections = soup.find_all("section",class_="_3YREj-P")
    products = []
    for i in sections:
        product = i.find_all("article",class_="_2qG85dG")
        for z in product:
            products.append(z)

    TempCollated = []
    error_links = []
    error = 0
    for i in products: 
        try:
            Product_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            # print(Product_Link)
            driver.get(Product_Link)
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource,'html.parser')

            product_info = soup.find('div',class_="product-hero").text #soup .find not = None, use if else statement, do an else to find another type of class that can show product info
            product_info1 = str(product_info).split("\n")
            while("" in product_info1) :
                product_info1.remove("")
            
            Product_title = product_info1[0]

            product_prices = product_info1[1]
            prices_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', product_prices)]
            Old_price = prices_list[0]

            New_price = prices_list[1]

            Discount = abs(prices_list[2])

            Colour = soup.find('span',class_="product-colour").text
            
            Product_Descriptions = soup.find("div",class_="product-description")
            
            product_description1 = Product_Descriptions.find_all('a',href=True)
            
            prdouct_description = []
            for x in product_description1:
                prdouct_description.append(x.text)
            
            Apparel = prdouct_description[0]
            Brand = prdouct_description[1]

            Image = soup.find("img",class_="gallery-image")['src']
            
            temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":Apparel }
            TempCollated.append(temp)
        except Exception as e:
            error += 1
            error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            error_links.append(error_Link)
            continue

    print(error_links)
    print(len(error_links))
    print(len(TempCollated))
    print(TempCollated[0])
    driver.close()
    return

scrape_asos_men_bottom()

print("\n")

def scrape_asos_men_footwear():
    driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
    url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61388'
    driver.get(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    r = requests.get(url,headers=headers)
    
    driver.maximize_window()

    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    
    reached_page_end = False
    test_counter_to_remove = 0

    while reached_page_end == False and test_counter_to_remove <=1:
        for i in range(0,30):
            ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)
        if bool(soup.find_all("a",class_="_39_qNys")) == True:
            driver.find_element_by_class_name('_39_qNys').click()
            time.sleep(1)
            test_counter_to_remove +=1

        else:
            reached_page_end = True
            
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')

    sections = soup.find_all("section",class_="_3YREj-P")
    products = []
    for i in sections:
        product = i.find_all("article",class_="_2qG85dG")
        for z in product:
            products.append(z)

    TempCollated = []
    error_links = []
    error = 0
    for i in products: 
        try:
            Product_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            # print(Product_Link)
            driver.get(Product_Link)
            htmlSource = driver.page_source
            soup = BeautifulSoup(htmlSource,'html.parser')

            product_info = soup.find('div',class_="product-hero").text #soup .find not = None, use if else statement, do an else to find another type of class that can show product info
            product_info1 = str(product_info).split("\n")
            while("" in product_info1) :
                product_info1.remove("")
            
            Product_title = product_info1[0]

            product_prices = product_info1[1]
            prices_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', product_prices)]
            Old_price = prices_list[0]

            New_price = prices_list[1]

            Discount = abs(prices_list[2])

            Colour = soup.find('span',class_="product-colour").text
            
            Product_Descriptions = soup.find("div",class_="product-description")
            
            product_description1 = Product_Descriptions.find_all('a',href=True)
            
            prdouct_description = []
            for x in product_description1:
                prdouct_description.append(x.text)
            
            Apparel = prdouct_description[0]
            Brand = prdouct_description[1]

            Image = soup.find("img",class_="gallery-image")['src']
            
            temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":Apparel }
            TempCollated.append(temp)
        except Exception as e:
            error += 1
            error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
            error_links.append(error_Link)
            continue

    print(error_links)
    print(len(error_links))
    print(len(TempCollated))
    print(TempCollated[0])
    driver.close()
    return

scrape_asos_men_footwear()


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


