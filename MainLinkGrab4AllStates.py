import urllib2
from bs4 import BeautifulSoup
import pickle
import unicodedata

def get_state_facts():

	#Below is the URL that links to 50 different fact pages, one page of facts for each state
	url = "http://www.50states.com/facts"

	#Crawl to the URL
	#Navigate to where each fact page link is documented in HTML
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)

	li = soup.find(id="content").select("li > a")

	#There is a different URL for each state's fact page
	#Make a list of all fact page URLs we must visit. Each item in the list represents a fact page for one state
	LiList = []
	for link in li:
		LiList.append(link.get('href'))
		#print LiList
	#returns

	allFactList = []
	extractList=[]
	for i in LiList:

		if i.startswith('/facts/'):
			extractList.append(i)
	#print extractList

	for i in extractList:
		url = "http://www.50states.com" + i

	#Crawl to each fact page URL from our list of 50 fact pages
	#Navigate to where each fact is documented in HTML
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
		section = soup.find(id="content").find('li')

	#make a list of all the facts for one state
		factList = []
		for fact in section.stripped_strings:
			fact = fact.encode('ascii', 'ignore')
			fact = fact.replace('\n', '')
 			factList.append(fact)

		factList = factList[0:49]
 		#print factList

#make a Master list. 
#This Master list is a list containing the list of facts generated for each state. A list with 50 lists in it, one list for each state
		allFactList.append(factList)


#make a dictionary where each state acronym is the key and each list of facts for that state are the values
stateFactsDict= {}
stateAbbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NM', 'NY', 'NJ', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
for i in stateAbbr:
	stateFactsDict[1] = factList

stateFactsDict = dict(zip(stateAbbr,allFactList))

return stateFactsDict

get_state_facts()

#this output will give you 50 lists with 50 states each
# i.e. dictionary = {'AL': [fact1, fact2, fact3],
#  			 'AK': [fact1, fact2, fact3],
#  			 'AZ': [fact1, fact2, fact3] ...etc}


