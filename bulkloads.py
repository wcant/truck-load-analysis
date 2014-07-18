import cookielib
import mechanize
import sys
import html2text

# Username and password(respectively) must be passed as arguments
# from the command line.
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
text = h.handle(br.response().read()).splitlines()

# Get initial conditions load retrieval loop
nLoads = text.count('view')
loads =[]
ithLoad = 0
startIndex = 0
endIndex = len(text)
# Loop over the number of occurences of 'view', which signals
# the beginning of a new load.
while(ithLoad < nLoads):
	loadIndex = text.index('view', startIndex, endIndex)
	endLoadIndex= text.index('view', loadIndex+1) 
	loads.append(text[loadIndex+1:endLoadIndex])
	startIndex = endLoadIndex+1
	ithLoad+=1
	


#f = open('loads.txt', 'w')
#for line in text:
#	f.write(line+'\n')



