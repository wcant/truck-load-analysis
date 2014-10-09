import cookielib
import mechanize
import sys
import html2text
import urllib, json, csv
# Username and password(respectively) must be passed as arguments
# from the command line.

#geocoding function from google api
def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")  
    return info

UNAME = str(sys.argv[1])
PASS = str(sys.argv[2])

URL = "http://www.bulkloadsnow.com"

# Browser
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

# Follows refresh 0 but not hangs on refresh>0
#br.set_handle_refresh(mechanize.http.HTTPRefreshProcessor(), max_time=1)

# Open site
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
br.submit()
raw_text = h.handle(br.response().read()).splitlines()
text = ''.join(raw_text)

# Get initial conditions load retrieval loop
nLoads = text.count('view')//2
loads = {}
ithLoad = 0
startIndex = 0
endIndex = len(text)

fieldNames = ["origin_city", "origin_state", "destination_city", 
							"destination_state", "start_date", "end_date", "loads", 
							"rate", "equip", "miles", "added", "posted_by"]

# Loop over the number of occurences of 'view', which signals
# the beginning of a new load.
while(ithLoad <= nLoads):
	startLoadIndex = text.index('view', startIndex, endIndex)
	try:
		endLoadIndex = text.index('view', startLoadIndex+1) 
	except ValueError:
		endLoadIndex = text.index('Offline Chat | Send E-mail', startLoadIndex+1)
		fieldValues = text[startLoadIndex:endLoadIndex].split('|')[1:13]
		break
	#start at 1 to ignore the 'view' string, end at 13 to ignore excess
	fieldValues = text[startLoadIndex:endLoadIndex].split('|')[1:13]
	loads[ithLoad] = dict(zip(fieldNames, fieldValues))
	startIndex = endLoadIndex
	ithLoad+=1

with open('data.json', 'wb') as fp:
	json.dump(loads, fp)

#with open('loads.txt', 'w') as f:
#	f.write(','.join(fieldNames))
#	for line in text:
#		f.write(line+'\n')


