#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:22:45 2020

@author: Amy
"""
## install selenium and import libraries



import selenium
from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd 
import time 
"""
options = webdriver.ChromeOptions()
# headless option setting
options.add_argument('headless')
options.add_argument("no-sandbox")

# browser window size
options.add_argument('window-size=1920x1080')

 

# options which makes the cralwer as a human 
options.add_argument("lang=ko_KR") # fake plugin
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36') # user-agent 이름 설정

 

# driver directory
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

 

driver.get('https://naver.com')

driver.implicitly_wait(3)

driver.quit() # driver 종료[출처] python으로 크롤링 하기 기초 1- selenium|작성자 ALMADEN
"""

# search result URL 
def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" +word
    return url
    
# open first posting 
def select_first(driver) :
    first = driver.find_element_by_css_selector("div._9AhH0")
    first.click()
    time.sleep(3)    
    
### get the info dta
import re

def get_content(driver):
    # load the html info to current page 
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # load main contents 
    try:
         content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    # load hashtags  
    tags = re.findall(r'#[^\s#,\\]+', content)
    # load date time
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    # load likes 
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
    except:
        like = 0
    # load location 
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
    # save the info 
    data = [content, date, like, place, tags]
    return data




### open next post

def move_next(driver):
    right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(3)


# instagram log in url 
loginUrl = 'https://www.instagram.com/accounts/login'

# driver load

driver= webdriver.Chrome(executable_path ='/Users/appleuser/Downloads/chromedriver')
driver.implicitly_wait(5)

# website login
driver.get(loginUrl)

# ID and PW info
username = '030summer'
userpw = 'Letmein1@@'

# login info
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(userpw)
driver.implicitly_wait(5)

driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').submit()
                                                          
later = driver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')                                            
later.click()
Notnow = driver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm')
Notnow.click()


# instagram search page URL 
word = 'running'
url = insta_searching(word)

# go to the search page 
driver.get(url)
time.sleep(3)

#open first post 
select_first(driver)


# result
results = [ ] 


# crowling 
target = 10 # number of the post which you cralw
for i in range (target):
    data = get_content(driver) #load the post info 
    results.append(data)
    move_next(driver)
    
print(results[:2])





results_df = pd.DataFrame(results)
results_df.columns = ['content','data','like','place','tags']
results_df.to_excel('/Users/appleuser/Documents/thesis/list.xlsx')







    
    
    
    
    
    
    
