import pymysql
import MySQLdb as mdb
import requests
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
# from pyvirtualdisplay import Display
import random
import time
import string
import re
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# matched = 0
# not_matched = 0
# #Create a Mysql Connection
# conn = mdb.connect('localhost','root','7936_Pxd$*M','pxdm_cr')
# conn.set_character_set('utf8')


# Get the SC Items for matching
response = requests.get('http://pricecompare.test/sc-names')
sc_items  = json.loads(response.text)


#Set crawler sleep seconds
sleep_seconds = 5 + (random.random() * 5)

exec(compile(source=open('sites/jumia.py').read(), filename='jumia.py', mode='exec'))
exec(compile(source=open('sites/superprice.py').read(), filename='superprice.py', mode='exec'))
exec(compile(source=open('sites/franko.py').read(), filename='franko.py', mode='exec'))
exec(compile(source=open('sc_sites/gsmarena.py').read(), filename='gsmarena.py', mode='exec'))




merchanr_id = input("1.Jumia\n2.Superprice\n3.Franko\n4.Gsmarena\nPlease Enter Merchant Id:")

browser = webdriver.Firefox()

if merchanr_id == "1":
	browser.get("https://www.jumia.com.gh/mobile-phones/?shipped_from=country_local")
	crawl_jumia(sc_items,process, fuzz)

elif merchanr_id == "2":
	browser.get("https://www.superprice.com/mobile-phones.html?cat=44")
	crawl_superprice(sc_items,process, fuzz)

elif merchanr_id == "3":
	browser.get("https://frankotrading.com/12-mobile-phones")
	crawl_franko(sc_items,process, fuzz)

elif merchanr_id == "4":
	browser.get("https://www.gsmarena.com/makers.php3")
	crawl_gsmarena()

else:
	print("Invalid Merchant ID")





browser.quit()
