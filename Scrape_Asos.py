from logging import exception
from typing import KeysView
import urllib.request
from click import style
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import re

#men
def scrape_asos_men_shirts():
    Styles = ["Cropped","Cut Out", "Denim","Grandad Collar", "Jersey Shorts", "Longline", "Muscle", "Novelty", "Overshirts", "Oversized", "Oxford","Racer Back","Raglan","Regular fit","Raglan","Relaxed","Shackets","Skinny","Slim","Sports Shorts","Straight Leg","Tapered","Track","Western"]
    TempCollated = []
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61380,61383&scrollTo=product-201236650'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "clothing":Clothing, "style":Style,"apparel":"Tops","Category":"men"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue

        
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    
    print("Function is working !")
    return

def scrape_asos_men_Accessories():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61384'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "clothing":Clothing, "style":Style,"apparel":"Accessories","Category":"men"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_men_Bottoms():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&page=1&refine=attribute_10992:61375,61377'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Bottoms", "style":Style, "clothing":Clothing,"Category":"men"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_men_Footwear():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61388&scrollTo=product-24479058'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Footwear", "style":Style, "clothing":Clothing,"Category":"men"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_men_Suits_Blazers():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61467&scrollTo=product-201236650'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Suits and Blazers", "style":Style, "clothing":Clothing,"Category":"Men"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

#women
def scrape_asos_women_shirts():
    Styles = ["Cropped","Cut Out", "Denim","Grandad Collar", "Jersey Shorts", "Longline", "Muscle", "Novelty", "Overshirts", "Oversized", "Oxford","Racer Back","Raglan","Regular fit","Raglan","Relaxed","Shackets","Skinny","Slim","Sports Shorts","Straight Leg","Tapered","Track","Western"]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61380,61383'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "clothing":Clothing, "style":Style,"apparel":"Tops","Category":"Women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue

        
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    
    print("Function is working !")
    return

def scrape_asos_women_Accessories():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61384'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "clothing":Clothing, "style":Style,"apparel":"Accessories","Category":"Women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_women_Bottoms():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61375,61376,61377'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Bottoms", "style":Style, "clothing":Clothing,"Category":"Women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_women_Footwear():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61388'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Footwear", "style":Style, "clothing":Clothing,"Category":"Women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_women_Suits_Blazers():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61467'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Suits and Blazers", "style":Style, "clothing":Clothing,"Categroy":"women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return

def scrape_asos_women_Dresses():
    Styles = ["5-Panel","Across Body","Aviator","Baker Boy","Baseball","Blanket","Bobble","Bucket Hat","Cat Eye","Clubmaster & Retro","Docker","Fedora","Fingerless","Flat "]
    TempCollated = []    
    for i in Styles:
        driver = webdriver.Chrome(executable_path=r"D:\DOWNLOADS\ChromeDriver\chromedriver_win32\chromedriver.exe")
        url = 'https://www.asos.com/women/sale/cat/?cid=7046&currentpricerange=0-680&nlid=ww%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61379'
        driver.get(url)
        driver.maximize_window()

        Style = i

        driver.find_elements_by_class_name('_1om7l06')[3].click()
        Search_Styles = driver.find_element_by_class_name("_1TetmAG")
        Search_Styles.send_keys(i)
        time.sleep(2)
        driver.find_element_by_class_name("kx2nDmW").click()
        time.sleep(3)
        driver.find_element_by_class_name("_2pwX7b9").click()

        reached_page_end = False

        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,30):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)
            if bool(soup.find_all("a",class_="_39_qNys")) == True:
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
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
                    Clothing = Apparel_and_Brand[1]
                    FullBrand = Apparel_and_Brand[2]
                    Brand = FullBrand[3:]
                
                else:
                    product_description1 = Product_Descriptions.find_all('a',href=True)
                    prdouct_description = []
                    for x in product_description1:
                        prdouct_description.append(x.text)
                    Clothing = prdouct_description[0]
                    Brand = prdouct_description[1]
                
                temp = {"author": url, "title":Product_title, "link": Product_Link, "tags": Brand, "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "apparel":"Dresses", "style":Style, "clothing":Clothing,"Categroy":"women"}
                TempCollated.append(temp)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue
        print(len(TempCollated))
        print(error_links)
        print(len(error_links))
        driver.close()
    print("Function is working !")
    return
