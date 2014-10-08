from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import sys

URL = "http://www.bulkloadsnow.com"
UNAME = str(sys.argv[1])
PASS = str(sys.argv[2])

driver = webdriver.Firefox()
driver.get(URL)

username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
submit = driver.find_element_by_name('headerlogin')

username.send_keys(UNAME)
password.send_keys(PASS)
submit.send_keys(Keys.RETURN)


