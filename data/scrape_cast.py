from bs4 import BeautifulSoup
# import urllib2
import sqlite3
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pprint

base = "http://bigbrother.wikia.com"
bb = "/wiki/Big_Brother_{num}_(US)"
all_stars = "/wiki/Big_Brother_All-Stars_(US)"
celebs = "/wiki/Celebrity_Big_Brother_1_(US)"
ott = "/wiki/Big_Brother:_Over_The_Top"

sql_transaction = []

connection = sqlite3.connect('cast.db')
c = connection.cursor()

page = requests.get(base + celebs)
soup = BeautifulSoup(page.content, "html.parser")

houseguests_header = soup.find('span', id="HouseGuests")
houseguest = houseguests_header.find_next('td')

hrefs = []

while houseguest != None:
	houseguests_href = houseguest.find_next('a')['href']
	houseguest = houseguest.find_next('td')

	if houseguests_href.startswith('/wiki/') and houseguests_href not in hrefs:
		hrefs.append(houseguests_href)

#print(hrefs)

url = base + hrefs[0]

caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "normal"

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
firefox_profile.set_preference("dom.max_script_run_time", 10)

driver = webdriver.Firefox(desired_capabilities=caps, firefox_profile=firefox_profile)

driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# page = requests.get(base + celebs)
# soup = BeautifulSoup(page.content, "lxml")

houseguest_info = soup.table

name = houseguest_info.find('th').text.rstrip().lstrip()
cast = []
cur_cast = {'Name': name}

for tr in houseguest_info.find_all('tr'):
	td = tr.find_all('td')
	if len(td) > 1:
		cur_cast[td[0].text.rstrip().lstrip()] = td[1].text.rstrip().lstrip()

cast.append(cur_cast)
pprint.pprint(cur_cast)
# for href in hrefs:
# 	url = base + href
# 	page = requests.get(base + celebs)
# 	soup = BeautifulSoup(page.content, "html.parser")
# 	html = BeautifulSoup(page.text, "lxml")
# 	print(html)

# 	verify_contestant = soup.find('div', class_="page-header__categories-links")
# 	#print(verify_contestant)
# 	# if html.find(text='Houseguest Profile'):
# 	# 	print('contains for ' + url)
