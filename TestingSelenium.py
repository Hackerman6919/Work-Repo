from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver = webdriver.Chrome("D:\DOWNLOADS\Chrome Driver\chromedriver_win32\chromedriver.exe")
driver.get("https://forever21.sg/collections/offer")
driver.maximize_window()
reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")

count = 0 
while not reached_page_end:
    
    for i in range(0,30):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        htmlSource = driver.page_source
        soup = BeautifulSoup(htmlSource, 'html.parser')
        if soup.find("div",class_="sc-fznxsB kWAcuz sc-fznMAR kvbDRc privy-widget-popup"):
            driver.find_element_by_class_name('div','sc-fzoiQi ozSmQ privy-dismiss-content').click()
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



