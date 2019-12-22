#! /usr/bin/env python3

# sa_crime_to_csv.py - a custom python script that scrapes data from 
# https://www.sanantonio.gov/SAPD/Uniform-Crime-Reports. The script 
# itself is not particularly reusable, but can be modeled for use 
# with other similar web scraping tasks

import requests
import bs4
import csv

def toCsv(elementList, fileName):
	'''Function takes the table elements extracted from the BeautifulSoup
	   element tags stored in elementList, iterates through them and writes
	   the content into a customized csv file'''
	newCsv = open((fileName + '.csv'), 'w', newline='')
	writer = csv.writer(newCsv)

	year = 2019

	monthList = ['Jan', 'Feb', 'Mar', 'Apr', 
				 'May', 'Jun', 'Jul', 'Aug',
				 'Sep', 'Oct', 'Nov', 'Dec']
	
	# create a list of lists and use these to write rows in new csv
	for a in range(len(elementList)):
		row = 1
		data = []
		line = []
		tableElems = bs4.BeautifulSoup(str(elementList[a]))
		table = tableElems.select('tr td')

		# take individual tables and write entries to the variable "line"
		for i in range(len(table)):
			
			# add year to months
			if table[i].get_text() in monthList:
				entry = table[i].get_text() + ' ' + str(year)
			else:
				entry = table[i].get_text()	
			
			# create a new list every 14 entries
			if row < 14:
				line.append(entry)
				row += 1
			# append "line" to "data" every 14 lenes
			else:
				line.append(entry)
				data.append(line)
				row = 1
				line = []
		
		# count years down from 2019
		year -= 1
		
		# unzip lists to transform data 
		(index, jan, feb, mar, 
		 apr, may, jun, jul, aug, 
		 sep, octo, nov, dec, total) = zip(*data)

		# only keep data from months
		rowNames = [jan, feb, mar, apr, 
		            may, jun, jul, aug, 
		            sep,octo, nov, dec]
		
		for row in rowNames:
			writer.writerow(row)
		
	newCsv.close()

res = requests.get('https://www.sanantonio.gov/SAPD/Uniform-Crime-Reports')

try:
	res.raise_for_status()
except Error:
	print("Error: Status Code: " +  res.status_code)

crimeSoup = bs4.BeautifulSoup(res.text)
tableElements = crimeSoup.select('tbody')

toCsv(tableElements, 'crime_in_sa')





	






