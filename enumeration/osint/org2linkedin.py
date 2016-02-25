#!/usr/bin/env python
import urllib
import urllib2
import json as m_json
import argparse
from sys import argv
from BeautifulSoup import BeautifulSoup as bs

# Setup for argument parsing
parser = argparse.ArgumentParser(prog=str(argv[0]), usage='%(prog)s [options]', description='Google Linkedin Scraper to enumerate current employees at a given organization with publicly available Linkedin profiles')

parser.add_argument('-n', help='Number of results from Google', dest='noresults', default=500)
parser.add_argument('-o', help='Name of organization to search for', dest='orgname')

# parse arguments
args = parser.parse_args()
argsdict = vars(args)
noresults = argsdict['noresults']
orgname = argsdict['orgname']

# if no orgname provided, grab here
if orgname == None:
	orgname = raw_input('Organization name: ')
query = ({ 'q': 'site:linkedin.com inurl:pub -inurl:dir "at " ' + '"' + str(orgname) + '"' + ' \'Current\'' })
query = urllib.urlencode(query)
pageno = 0
# divide noresults by 8 for clean output
noresults = int(noresults) / 8


# Grab the user ip and send it in later request so Google is nice to us
print "Need to get your external IP. This can take a bit..."
useripquery = urllib.urlopen('http://ifconfig.me/ip').read()
userip = ({ 'userip' : useripquery.rstrip()})
userip = urllib.urlencode(userip)


while pageno <= int(noresults):
	try:
		# Do Google Search
		response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=8' + '&start=' + str(pageno) + '&' + userip + '&' + query ).read()
		json = m_json.loads ( response )
		results = json [ 'responseData' ] [ 'results' ]
		pageno = pageno + 8
		for result in results:
			title = result['title']
			url = result['url']
			# Visit LinkedIn URL and grab job title
			while True:
				try:
					headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
					req = urllib2.Request(url)
					req.add_header('User-Agent', headers)
					the_page = urllib2.build_opener()
					bspage = bs(the_page.open(req).read())
					formatted_jobtitle = bspage.p.string
					break
				except urllib2.HTTPError:
					# if LinkedIn url is a 404, say couldn't determine
					formatted_jobtitle = "Couldn't determine job title"
					break
			# output results
			print  (title + '; ' + formatted_jobtitle + '; ' + url)
			pass
	except TypeError:
		break	
