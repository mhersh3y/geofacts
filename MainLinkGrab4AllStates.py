import urllib2
from bs4 import BeautifulSoup
import unicodedata

def get_state_facts():
	"""
	This function scrapes facts about all 50 United states from a website
	"""
	#Below is the website that links to 50 different fact page URLs, one page for each state
	#Find where each fact page link is documented in HTML
	#Make a list of all fact page URLs we must visit for info
	url = "http://www.50states.com/facts"
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)
	li = soup.find(id="content").select("li > a")
	liList = []
	extractList=[]
	allFactList = []
	for link in li:
		liList.append(link.get('href'))

	for i in liList:
		if i.startswith('/facts/'):
			extractList.append(i)

	#Go to each fact page URL from our list
	#Find where each fact is documented in HTML and make a list of all the facts. Do this for each state
	for i in extractList:
		url = "http://www.50states.com" + i
		page = urllib2.urlopen(url).read()
		soup = BeautifulSoup(page)
		section = soup.find(id="content").find('li')
		factList = []
		for fact in section.stripped_strings:
			fact = fact.encode('ascii', 'ignore')
			fact = fact.replace('\n', '')
 			factList.append(fact)

		factList = factList[0:49]

		#Make a Master list containing the lists of facts generated
		allFactList.append(factList)

	#Make a dictionary where each state acronym is the key and each list of facts for that state are the values
	stateFactsDict= {}
	stateAbbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NM', 'NY', 'NJ', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
	for i in stateAbbr:
		stateFactsDict[1] = factList

	stateFactsDict = dict(zip(stateAbbr,allFactList))
	return stateFactsDict

print get_state_facts()

#this output will give you 50 lists with 50 states each
# i.e. dictionary = {'AL': [fact1, fact2, fact3],
#  			 'AK': [fact1, fact2, fact3],
#  			 'AZ': [fact1, fact2, fact3] ...etc}


