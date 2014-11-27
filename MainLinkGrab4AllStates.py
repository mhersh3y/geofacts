import urllib2
from bs4 import BeautifulSoup

url = "http://www.50states.com/facts"

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

li = soup.select("li > a")

LiList = []
for link in li:
	LiList.append(link.get('href'))
	# print LiList ##YAY. i extracted too many links to fact pages that are not states

extractList=[]
for i in LiList:
	if i.startswith('/facts/'):
		extractList.append(i)
print extractList
	


