from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import sys
import html2text

""" This entire program assumes each load does not contain the string
		'view' anywhere other than at the beginning of each load listing.
"""
#error catching variables
errorStates = []
URL0 = "http://www.bulkloadsnow.com"
#UNAME = str(sys.argv[1])
#PASS = str(sys.argv[2])
UNAME = input("Enter username: ")
PASS = input("Enter password: ")

h = html2text.HTML2Text()
h.ignore_links = True

#long timeout is necessary because the page is so damn big
driver = webdriver.Firefox()
driver.set_page_load_timeout(25)
driver.get(URL0)

#Login
username = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')
submit = driver.find_element_by_name('headerlogin')
username.send_keys(UNAME)
password.send_keys(PASS)
submit.send_keys(Keys.RETURN)

#LOADS page
def getAvailableStates():
		link = driver.find_element_by_link_text('LOADS')
		link.send_keys(Keys.RETURN)
		form = driver.find_element_by_id('CFForm_4')
		dropdown = form.find_element_by_id('equip_origin_state')
		availableStates = dropdown.text.split('\n')
		return availableStates

text = {}
availableStates = getAvailableStates()
for state in availableStates:
		print(state)
		try:
				link = driver.find_element_by_link_text('LOADS')
				link.send_keys(Keys.RETURN)
				form = driver.find_element_by_id('CFForm_4')
				dropdown = form.find_element_by_id('equip_origin_state')
				dropdown.send_keys(state)
				dropdown.submit()
				rawHtml = driver.page_source
				rawText = h.handle(rawHtml).splitlines()
				text[state] = ''.join(rawText)
		except:
				errorStates.append(state)
				continue

fieldNames = ["origin_city", "origin_state", "destination_city", 
							"destination_state", "start_date", "end_date", "loads", 
							"rate", "equip", "miles", "added", "posted_by"]
1/0
# Get initial conditions load retrieval loop
loads = {}
ithLoad = 0
startIndex = 0
endIndex = len(text)
# Loop over the number of occurences of 'view', which signals
# the beginning of a new load.
result = None
while result is None:
	startLoadIndex = text.index(' view ', startIndex, endIndex)
	try:
		endLoadIndex = text.index(' view ', startLoadIndex+1) 
	except ValueError:
		stopString = 'Offline Chat | Send E-mail'
		endLoadIndex = text.index(stopString, startLoadIndex+len(stopString))
		fieldValues = text[startLoadIndex:endLoadIndex].split('|')[1:13]
		loads[ithLoad] = dict(zip(fieldNames, fieldValues))
		result = 1
		break
	#start at 1 to ignore the 'view' string, end at 13 to ignore excess
	fieldValues = text[startLoadIndex:endLoadIndex].split('|')[1:13]
	loads[ithLoad] = dict(zip(fieldNames, fieldValues))
	startIndex = endLoadIndex
	ithLoad+=1

print(str(len(loads))+" loads found.")

#with open('data.json', 'wb') as fp:
#	json.dump(loads, fp)

