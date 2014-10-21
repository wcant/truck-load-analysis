from urllib import request
from urllib import parse
import json

class geocode:
		"""This class encapsulates the Google Geocode API request and uses
		a local api_key.txt file to assign a key to the request."""

		def __init__(self):
				self.notFound = []

		def outputJson(self, outFile):
				with open(outFile, 'wb') as f:
						json.dump(bl.loads, f)

		def getKey(self,keyFile):
				with open(keyFile, 'r') as f:
						self.key = f.readline()

		def requestCoordinates(self, address):
				url = ("https://maps.googleapis.com/maps/api/geocode/json?address"\
							+"={0}&{1}".format(parse.quote(address.replace(' ', '+')), \
							'key=' + self.key))
				responseData = request.urlopen(url).read()
				#if the address is not recognized then the list index by [0]
				#returns as empty.
				try:
						result = json.loads(responseData.decode('utf8'))['results'][0]
						info = result['geometry']['location']
				except IndexError:
						self.notFound.append(address)
						return {'lat': 'None', 'lng': 'None'}
				return info

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
