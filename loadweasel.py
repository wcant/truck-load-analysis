#/usr/bin/env python
import glob
import os.path
import re

def read_loadweasel_csv (dataLocation):
	data = [ ] 
	for files in dataLocation:
		with open(files) as f:
			content = f.readlines()
			data.extend(content)
	return data
	
#def filter_unique_loadid (data):
#	for load in data:
#		loadids = data


