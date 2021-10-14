#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 21:50:40 2021

@author: appleuser
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import re
import time
import pyperclip
from bs4 import BeautifulSoup
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

driver= webdriver.Chrome(executable_path ='/Users/appleuser/.wdm/drivers/chromedriver/mac64/88.0.4324.96/chromedriver')

# Access to Newyork times  
url="https://www.nytimes.com/section/business/energy-environment"   
driver.get(url)  
time.sleep(2) 
action=ActionChains(driver)  
time.sleep(2)       

# cookie accept
coockie = driver.find_element_by_xpath("""//*[@id="site-content"]/div[2]/div[2]/div/div[2]/button""").click()
ac = Alert(driver)
ac.accept()

# search renewable
search = driver.find_element_by_xpath("""//*[@id="collection-business-energy-environment"]/div[1]/div/nav/ul/li[2]/a/span[1]""").click()  
renewable = driver.find_element_by_xpath("""//*[@id="search-tab-input"]""")
renewable.send_keys("renewable")

# select option 'newest'
select_subject = Select(driver.find_element_by_xpath("""//*[@id="sort-filter"]"""))                        
select_subject.select_by_value('newest')

# scroll down the pages
body = driver.find_element_by_css_selector('body')
for i in range (10):
    body.send_keys(Keys.END) # page down
    time.sleep(2)

# collect headlines 
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# set a box
boxes = driver.find_elements_by_css_selector("#stream-panel > div.css-13mho3u > ol > li")

# create empty variables
result = [ ]


for box in boxes:      
    ls = []
    ls.append(box.find_element_by_css_selector("div.css-1lc2l26.e1xfvim33 > span").text) #Date
    ls.append(box.find_element_by_css_selector("a > h2").text) #title
    ls.append(box.find_element_by_css_selector("a > p").text) #headline
    result.append(ls)


# save the result
result_df = pd.DataFrame(result)
result_df.columns = ['date','title', 'headline']
result_df.to_csv('/Users/appleuser/Documents/Thesis/db.csv', index = False)
result_df.to_excel('/Users/appleuser/Documents/Thesis/db.xlsx')



