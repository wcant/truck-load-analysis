#/usr/bin/env python

from loadweasel import read_loadweasel_csv 
import glob
import re

files = glob.glob("/Users/wesleycantrell/Google Drive/repo/truck-load-analysis/loadweasel_data/*.csv")

data = read_loadweasel_csv(files)

#get elements 
loadids = [ ] 
loadCity = [ ]
loadState = [ ]
unloadCity = [ ]
unloadState = [ ]
trailer = [ ]

for element in data:
	element = re.sub('[^-,A-Za-z0-9]+', '', element)
	split_str = element.strip().split(",")
	#consider adding regex conditions for each to make sure the strings make sense
	if element[0] != 'LoadID' : 	
		loadids.append(split_str[0])
		loadCity.append(split_str[1])
		loadState.append(split_str[2])
		unloadCity.append(split_str[3])
		unloadState.append(split_str[4])
		trailer.append(split_str[8])
print(trailer)

