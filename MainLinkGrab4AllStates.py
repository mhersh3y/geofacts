import urllib2
from bs4 import BeautifulSoup

url = "http://www.50states.com/facts"

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

li = soup.find(id="content").select("li > a")

LiList = []
for link in li:
	LiList.append(link.get('href'))
	# print LiList ##YAY. i extracted too many links to fact pages that are not states

extractList=[]
for i in LiList:
	if i.startswith('/facts/'):
		extractList.append(i)
#print extractList

for i in extractList:
	url = "http://www.50states.com" + i
#url = "http://www.50states.com/facts/alabama.htm"
##used that url for practice runs of the script
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)

	section = soup.find(id="content").find('li')
	sectionStripped = section.stripped_strings
#removes extra characters from the text
	
	factList = []
	for fact in sectionStripped:
 		factList.append(fact)
	print factList
#this output will give you 50 lists with 50 states each


#if we want we can a dictionary where
#the key is the state name and 
#and the value is the list of facts 
# i.e. dictionary = {'AL': [fact, fact, fact],
#  			 'AK': [fact, fact, fact],
#  			 'AZ': [fact, fact, fact] ...etc}
#this might be helpful
#stateAbbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NM', 'NY', 'NJ', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


