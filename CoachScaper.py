"""
Authored: Sun, Feb. 14th, 2016
@author: BDey

What does this do? Gets season stats for all coaches between 1980 - 2016.
How?: 
	Get List off all coaches in every season
	filter to unique coaches
	scrape each coaches page for stats per season.
"""

from bs4 import BeautifulSoup
from urllib import urlopen
import re
import csv

#Example All coaches page for a season: 	'http://www.sports-reference.com/cbb/seasons/1985-coaches.html'
#Example Coach Page: 						 http://www.sports-reference.com/cbb/coaches/reggie-minton-1.html



setofallcoaches = set() #set only stores unique values.


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#First grab all the unique coach links in timeframe
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

urls = 'http://www.sports-reference.com/cbb/seasons/'
for i in range(1980,2015,1):
    page = urlopen(urls + str(i)+'-coaches.html')
    soup = BeautifulSoup(page) #Create the BeautifulSoup object equal to every coach page for every season between 1980-2016  
    	#print urls + str(i)+'-coaches.html'
    	  	
    	#for table in soup.findAll('tr',{ 'class' : ''}):
    for link in soup.findAll('a', href=re.compile("cbb/coaches")):
        coachlink = link['href']
        coachname = link.string
    	#print str(coachlink) 
    
	setofallcoaches.add(coachlink) #write coaches to a set 
    print 'There are '+str(len(setofallcoaches)) + ' distinct coaches in ' + str(i)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#Then visit all links, grab coach stats, then write to a csv.
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
with open('coachdata.csv', 'wb') as csvfile:
	coachdata = csv.writer(csvfile, delimiter=',')
	for coachlink in setofallcoaches:
		baseurl = 'http://www.sports-reference.com'
		"""coachpage = str(baseurl) + str(coachlink) #this just prints the URL as a string, 
			but you get an error beacuse it's a string... User urlopen from urllib library instead.
			http://stackoverflow.com/questions/24768858/beautifulsoup-responses-with-error
			 doc on lib here:https://docs.python.org/2/library/urllib2.html
		"""
		coachpage = urlopen(str(baseurl) + str(coachlink))
		coachpagesoup = BeautifulSoup(coachpage)
		noiftables = []
		iftables = []
		for table in coachpagesoup.findAll('tr',{ 'class' : ''}):
			#print table # this is including non coach tables. Need to filter tr tags whose class = "" AND whose table includes a csk tag...
			#noiftables.append(table)
			#print len(noiftables)
			#name = coachpagesoup.find('h1').string
		 
			if table.findAll(csk=re.compile("\d")):
			#if table.find('a', href=re.compile("cbb/seasons")):
				#iftables.append(table)
		#print "noiftables " + str(len(noiftables)) + " vs iftables: " + str(len(iftables)) # every page includes a tr tag with class = "" that i'm not interested in. include simple simple regular expression if to remove them.
				#print table
				if coachpagesoup.find('h1').string != '^Coaches with':
					name = coachpagesoup.find('h1').string
				try:
					school = table.contents[3].contents[0].string #between 3rd and 4th td tag. print string.
					season = table.contents[1].contents[0].string # 1st and 2nd tag. print string.
					if table.find(title = True):
						conference = table.find(title = True).string # conference 
					totalgames = table.contents[7].contents[0].string
					wins = table.contents[9].contents[0].string
					losses = table.contents[11].contents[0].string
					winlosspercent = table.contents[13].contents[0].string
					notes = table('td')[-1].text #the note field is the last column in every array. grab the last td tag in array, and suck out the text.
			
					coachdata.writerow([name,school,season,conference,totalgames,wins,losses,winlosspercent,notes])
				except Exception, e: #just catch any and all exceptions and keep chuggin'.
    					print type(e)
   				  
				#print name, school, season, conference, totalgames, wins, losses, winlossperct, notes
			