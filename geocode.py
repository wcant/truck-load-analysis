import urllib as ul
import json
import sel_bulkloads as bl

#Store addresses that were not found by geocode()
notFound=[]
def geocode(addr):
		#go RTFM and fix this line width
		url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s" %   (ul.parse.quote(addr.replace(' ', '+')))
		data = ul.request.urlopen(url).read()	
		#if address is not recognized then the list indexed by [0]
		#returns as empty
		try:
				info = json.loads(data.decode('utf8'))['results'][0]['geometry']['location']
		except IndexError:
				notFound.append(addr)
				return {'lat': 'None', 'lng': 'None'}
		return info

#with open('data.json', 'rb') as f:
#	loads = json.load(f)

i=0
while (i < len(bl.loads)):
		coordinates = geocode(bl.loads[i]['origin_city']
													+bl.loads[i]['origin_state'])
		bl.loads[i]['origin_lat'] = coordinates['lat']
		bl.loads[i]['origin_lng'] = coordinates['lng']
		coordinates = geocode(bl.loads[i]['destination_city']
													+bl.loads[i]['destination_state'])
		bl.loads[i]['destination_lat'] = coordinates['lat']
		bl.loads[i]['destination_lng'] = coordinates['lng']
		i+=1

with open('bulkloads_data/data.json', 'wb') as f:
		json.dump(bl.loads, f)
