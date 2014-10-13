import cookielib
import mechanize
import sys
import html2text
import json

# Username and password(respectively) must be passed as arguments
# from the command line.
UNAME = str(sys.argv[1])
PASS = str(sys.argv[2])

URL = "http://www.bulkloadsnow.com"

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.addheaders = [('User-agent', 'Firefox')]

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# html2text
h = html2text.HTML2Text()
h.ignore_links = True

# Debugging messages
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

page = br.open(URL)

# Show response headers
#print page.info()

# Show available forms
#for form in br.forms():
#	print form

# Login
br.select_form('login')
br.form['username']=UNAME
br.form['password']=PASS
br.submit()
#print br.response().read() 

# Look at links
#for l in br.links():
#	print l

#Click LOADS link
req = br.click_link(text='LOADS')
br.open(req)

#for form in br.forms():
#	print form

br.select_form('CFForm_4')
br.form["equip_origin_state"]=["ALL"]
br.submit()

raw_text = h.handle(br.response().read()).splitlines()
text = ''.join(raw_text)

fieldNames = ["origin_city", "origin_state", "destination_city", 
							"destination_state", "start_date", "end_date", "loads", 
							"rate", "equip", "miles", "added", "posted_by"]

# Get initial conditions load retrieval loop
loads = {}
ithLoad = 0
startIndex = 0
endIndex = len(text)
# Loop over the number of occurences of 'view', which signals
# the beginning of a new load.
result = None
while result is None:
	startLoadIndex = text.index('view', startIndex, endIndex)
	try:
		endLoadIndex = text.index('view', startLoadIndex+1) 
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

print str(len(loads))+" loads found."

with open('data.json', 'wb') as fp:
	json.dump(loads, fp)

