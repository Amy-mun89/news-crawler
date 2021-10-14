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
# headless 옵션 설정
options.add_argument('headless')
options.add_argument("no-sandbox")

# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')

 

# 사람처럼 보이게 하는 옵션들
options.add_argument("lang=ko_KR") # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36') # user-agent 이름 설정

 

# 드라이버 위치 경로 입력
driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

 

driver.get('https://naver.com')

driver.implicitly_wait(3)

driver.quit() # driver 종료[출처] python으로 크롤링 하기 기초 1- selenium|작성자 ALMADEN
"""

# 검색결과 URL
def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" +word
    return url
    
# 첫번재 게시글 열기
def select_first(driver) :
    first = driver.find_element_by_css_selector("div._9AhH0")
    first.click()
    time.sleep(3)    
    
### 게시글 정보 가져오기

import re

def get_content(driver):
    # 현재 페이지에  html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 본문 내용 가져오기
    try:
         content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    # 본문 내용에서 해시태그 가져오기 
    tags = re.findall(r'#[^\s#,\\]+', content)
    # 작성일자 정보 가져오기
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    # 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1]
    except:
        like = 0
    # 위치정보 가져오기
    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''
    # 수집한 정보 저장하기
    data = [content, date, like, place, tags]
    return data




### 다음 게시글 열기

def move_next(driver):
    right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(3)


# 인스타 로그인 url
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


# 인스타 검색페이지 URL
word = 'running'
url = insta_searching(word)

# 검색페이지 접속
driver.get(url)
time.sleep(3)

# 첫번째 게시글 열기
select_first(driver)


# result
results = [ ] 


# crowling 
target = 10 #크롤링할 게시물 수
for i in range (target):
    data = get_content(driver) #게시물 정보 가져오기
    results.append(data)
    move_next(driver)
    
print(results[:2])





results_df = pd.DataFrame(results)
results_df.columns = ['content','data','like','place','tags']
results_df.to_excel('/Users/appleuser/Documents/thesis/list.xlsx')







    
    
    
    
    
    
    