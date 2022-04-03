import datetime
import bs4
import pytz
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import requests
import json
import random
import email
import imaplib
import re
from threading import Thread
from time import sleep

import lxml
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# from customMethods import *
# from getDate import *
# import debugBot

import ssl
user = "Udealio"
password = "gXKuZg3at4EZkQDY"
obj = {"username":"Udealio",
"password":"gXKuZg3at4EZkQDY"}
token = requests.post('https://www.udealio.com/token/obtain/', data = obj)
token_json = token.json()
token_json_access = token_json['access']
token_header = "JWT " + token_json_access
header = {'Content-Type': 'application/json',
            'authorization': token_header}

resp_style = requests.get('https://www.udealio.com/apiStyle/', headers=header)
resp_clothing = requests.get('https://www.udealio.com/apiClothing/', headers=header)
resp_clothing_type = requests.get('https://www.udealio.com/apiClothingStyle/', headers=header)


style_list = []
for resp_style_data in resp_style.json():
    style_clothing_list = []
    style_clothing_type_list = []
    style_exclude_list =[]
    
    style_clothing_list.append(resp_style_data['clothing'])
    style_clothing_type_list.append(resp_style_data['clothing_type'])
    style_exclude_list.append(resp_style_data['exclude'])

    temp_clothing_list = []
    for clothing_link_list in style_clothing_list:
        for clothing_link in clothing_link_list:
            split_link_clothing = clothing_link.split('/')
            clothing_id = split_link_clothing[-2]
    
            for resp_clothing_data in resp_clothing.json():
                if str(resp_clothing_data['id']) == str(clothing_id):
                    temp_clothing_list.append(resp_clothing_data['name'])

    temp_clothing_type_list = []
    for clothing_type_link_list in style_clothing_type_list:
        for clothing_type_link in clothing_type_link_list:
            split_link_clothing_type = clothing_type_link.split('/')
            clothing_type_id = split_link_clothing_type[-2]
    
            for resp_clothing_type_data in resp_clothing_type.json():
                if str(resp_clothing_type_data['id']) == str(clothing_type_id):
                    temp_clothing_type_list.append(resp_clothing_type_data['name'])


    temp_exclude_list = []
    for exclude_link_list in style_exclude_list:
        for exclude_link in exclude_link_list:
            split_link_exclude = exclude_link.split('/')
            exclude_type_id = split_link_exclude[-2]
            
            for resp_exclude_data in resp_clothing_type.json():
                if str(resp_exclude_data['id']) == str(exclude_type_id):
                   temp_exclude_list.append(resp_exclude_data['name'])

        temp_style = {'style': resp_style_data['name'], 'clothing': temp_clothing_list, 'clothing_type': temp_clothing_type_list, 'exclude': temp_exclude_list}
        style_list.append(temp_style)

tag_dict = {}
tag_dictkeywords = {}
style_dict = {}
post_list_api = []
link_list_api = []
post_list_cupnation = []
post_list_final = []

def post_list_final_shuffle(post_list_final):
    combined_post_list = []
    for x in post_list_final:
        combined_post_list += x
    post_list_final_shuffled = random.sample(combined_post_list,len(combined_post_list))
    print(post_list_final_shuffled)
    return post_list_final_shuffled

def postToApi():
    class mydict(dict):
            def __str__(self):
                return json.dumps(self)   
    url = 'https://www.udealio.com/apiPosts/'
    user = "Udealio"
    password = "gXKuZg3at4EZkQDY"
    obj = {"username":"Udealio",
    "password":"gXKuZg3at4EZkQDY"}
    token = requests.post('https://www.udealio.com/token/obtain/', data = obj)
    token_json = token.json()
    token_json_access = token_json['access']
    token_header = "JWT " + token_json_access
    header = {'Content-Type': 'application/json',
              'authorization': token_header}
    post_list_shuffled_final = post_list_final_shuffle(post_list_final)

    global numSuccess 
    global numFailed 

    for post in post_list_shuffled_final:
        my_obj = (mydict(post))
        print(my_obj)
        reply = requests.post(url, json=my_obj, headers=header)
        print(reply)
        print(reply.json())
        if(str(reply) == '<Response [201]>'):
            numSuccess += 1
        else:
            numFailed += 1

def post_new_tags(newTag):
    tags_for_posting = []
    for tag in newTag:
        if findTag(tag):
            found_id = findTag(tag)[0][0]
            found_id_to_post = f"https://udealio.com/apiTags/{found_id}"
            tags_for_posting.append(found_id_to_post)
        else:
            url = 'https://udealio.com/apiTags/'
            obj = {"username":"Udealio",
            "password":"gXKuZg3at4EZkQDY"}
            token = requests.post('https://www.udealio.com/token/obtain/', data = obj)
            token_json = token.json()
            token_json_access = token_json['access']
            token_header = "JWT " + token_json_access
            header = {'Content-Type': 'application/json',
                    'authorization': token_header}
            my_obj = {"name": tag,
            "post": []}
            jsondata = json.dumps(my_obj)
            reply = requests.post(url, data=jsondata, headers=header)
            new_id = reply.json()['id']
            new_id_to_post = f"https://udealio.com/apiTags/{new_id}"
            tags_for_posting.append(new_id_to_post)
    return tags_for_posting


def scrape_asos_men():
    new_titles = []

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress","localhost:6969")
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("user-agent=Mozilla/5.0")

    Category_Dict = {"tops":"https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61380,61383", "bottoms":"https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61375,61377","footwear":"https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61388","accessories":"https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61384,61387","suits and blazers":"https://www.asos.com/men/sale/cat/?cid=8409&currentpricerange=0-725&nlid=mw%7Csale%7Cshop%20sale%20by%20product%7Csale%20view%20all&refine=attribute_10992:61467"}
    TempCollated = []

    for Cateogry_Links in Category_Dict:
        url = Category_Dict[Cateogry_Links]
        apparel = Cateogry_Links

        t = Thread(target=OpenLocalHostChrome)  
        t.daemon = True               
        t.start()
        snooziness = int("5")
        sleep(snooziness)
        t = Thread(target=OpenOriginalDirectory)  
        t.daemon = True
        t.start()

        driver = webdriver.Chrome(executable_path=r"C:\Program Files\Google\Chrome\Application\chromedriver_win32_99\chromedriver.exe", chrome_options=options)
        driver.get(url)
        driver.execute_script("window.open()")
        print(driver.window_handles)
        driver.switch_to_window(driver.window_handles[0])
        driver.maximize_window()

        reached_page_end = False
        test_counter_to_remove = 0 
        htmlSource = driver.page_source
        asos_page = soup(htmlSource, 'html.parser')
        while reached_page_end == False:
            for i in range(0,7):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
                print('down')
            if driver.find_element_by_class_name('_39_qNys'):
                driver.find_element_by_class_name('_39_qNys').click()
                time.sleep(1)
                test_counter_to_remove+=1
                if test_counter_to_remove > 0:
                    reached_page_end = True
                print(test_counter_to_remove)
            else:
                reached_page_end = True
                print(reached_page_end)
        print('out') 
        htmlSource = driver.page_source
        asos_page = soup(htmlSource, 'html.parser')
        sections = asos_page.find_all("section",class_="_3YREj-P")
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
                asos_page = soup(htmlSource,'html.parser')

                product_info = asos_page.find('div',class_="product-hero").text #soup .find not = None, use if else statement, do an else to find another type of class that can show product info
                product_info1 = str(product_info).split("\n")
                while("" in product_info1) :
                    product_info1.remove("")
                Product_title = product_info1[0]
                product_prices = product_info1[1]
                prices_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', product_prices)]
                Old_price = prices_list[0]
                New_price = prices_list[1]
                Discount = abs(prices_list[2])
                Colour = asos_page.find('span',class_="product-colour").text
                Image = asos_page.find("img",class_="gallery-image")['src']
                Product_Descriptions = asos_page.find("div",class_="product-description")
                if len(Product_Descriptions.find_all('a',href=True)) == 1:
                    Product_Descriptions_split = str(soup(Product_Descriptions.prettify().split("<br/>")[0],"html.parser").text).split("\n")
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

                post_style_list = []
                clothing_type_list=[]
                for style in style_list:
                    exclude = False
                    for exclusion in style['exclude']:
                        exclusion = exclusion.lower()
                        if exclusion in Product_title.lower():
                            exclude = True
                    if exclude == False:
                        for clothing in style['clothing']:
                            clothing = clothing.lower()
                            if clothing in Product_title.lower():
                                if style['style'] not in post_style_list:
                                    post_style_list.append(style['style'])
                                
                        for clothing_type in style['clothing_type']:
                            clothing_type = clothing_type.lower()
                            if clothing_type in Product_title.lower():
                                clothing_type_list.append(clothing_type)
                                if style['style'] not in post_style_list:
                                    post_style_list.append(style['style'])
                                
                
                temp = {"author": "https://www.udealio.com/apiUser/7/", "title":Product_title, "link": Product_Link, "tags": post_new_tags([Brand]), "scrapedPostImage":Image, "new Price":New_price, "old Price":Old_price, "discount Percent":Discount, "colour":Colour, "clothing":Clothing, "clothing_type": clothing_type, "style":post_style_list,"apparel":apparel,"Category":"Men"}
                print(temp)
                if Product_title not in post_list_api:
                    if Product_Link not in link_list_api: 
                        if Product_title not in new_titles:
                            TempCollated.append(temp)
                            new_titles.append(Product_title)
                post_list_final.append(TempCollated)
            except Exception as e:
                error += 1
                error_Link = i.find('a',class_="_3TqU78D",href=True)['href']
                error_links.append(error_Link)
                continue

    
    print(len(TempCollated))
    print(error_links)
    print(len(error_links))
    driver.close()
    postToApi()

    print("Function is working !")
    return

