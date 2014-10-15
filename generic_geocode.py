from urllib import request
from urllib import parse
import json
import sel_bulkloads as bl

class geocode:
		"""This class encapsulates the Google Geocode API request and uses
		a local api_key.txt file to assign a key to the request."""

		def __init__(self):
				self.address = ''
				self.notFound = []
	
		def getKey(keyFile):
				with open(keyFile, 'r') as f:
						self.key = f.readline()

		def dataRequest(self)
				url = ("http://maps.googleapis.com/maps/api/geocode/json?address"+
							"={0}&{1}".format(parse.quote(self.address.replace(' ', '+')) 						 , 'key=' + self.key))
				


data = 


