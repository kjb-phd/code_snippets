#! Scraper for cliffbarackman.com

#for circumventing the login page
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time
from time import sleep
import pickle

#for parsing the html DOM and cleaning up the results
import bs4
from bs4 import BeautifulSoup
import re

#for parsing the second-tier pages
import urllib
from urllib.parse import urlparse
from urllib.request import urlopen
import html5lib

#for file manipulation 
import os
import csv


#set options and set target page
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
driver.get('https://cliffbarackman.com/forum/')


#login credentials and options to circumvent login
username = driver.find_element_by_id('log')
username.send_keys('kjbourgault@protonmail.com')
password = driver.find_element_by_id('pwd')
time.sleep(2)
password.send_keys('H82luz1!~seatko')
sign_in = driver.find_element_by_xpath('//*[@name="Submit"]')
sign_in.click()

#get cookies on first run
#pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))

#load cookies
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
	if 'expiry' in cookie:
         del cookie['expiry']
driver.add_cookie(cookie)

#parse html
html = driver.page_source
soup = BeautifulSoup(html, 'html5lib')

#for visually deciphering HTML structure
#print(soup.prettify())

#remove unwanted links -  
recent_added_links = soup.find('div', {'id': 'qlContent'})
recent_added_links.decompose()

weird_links = soup.find('option', value=re.compile('https://cliffbarackman.com/forum/too-weird-to-categorize-by-region-but-possibly-real/'))
weird_links.decompose()

extra_links = soup.find('option', value=re.compile('https://cliffbarackman.com/forum/expectations/'))
extra_links.decompose()

#set scraping target for raw region links
urls = []

for links in soup.find_all('option', value=re.compile('https://cliffbarackman.com/forum/*')):
	link = links['value']
	encoded_link = urllib.parse.quote(link, safe = '://')
	urls.append(encoded_link)


with open('urls.csv', 'a+', newline="") as csvf:
	writer = csv.writer(csvf, delimiter=",", lineterminator='\n')
	for url in urls:
		writer.writerow([url])
	print('success!!')


	