#!/usr/bin/env python
import argparse
from sys import argv, stdout
from googleapiclient.discovery import build
import re
import ConfigParser
from py_bing_search import PyBingWebSearch

# Setup for argument parsing
parser = argparse.ArgumentParser(prog=str(argv[0]), usage='%(prog)s [options]', description='Google Linkedin Scraper to enumerate current employees at a given organization with publicly available Linkedin profiles')

parser.add_argument('-n', help='Number of results from Google', dest='noresults', default=50)
parser.add_argument('-o', help='Name of organization to search for', dest='orgname')
parser.add_argument('--g-dev-key', help='Your Google Developer Key', dest='G_DEVELOPER_KEY', required=False)
parser.add_argument('--g-cx-key', help='Your Google Custom Search Engine key', dest='G_CX_KEY', required=False)
parser.add_argument('--b-api-key', help='Your Bing Web Search api key', dest='B_API_KEY', required=False)
parser.add_argument('-v', "--verbose", help="Verbose output", action="store_true", dest='verbose')
parser.add_argument('-d', "--debug", help="Debugging output (implies -v)", action="store_true", dest='debug')

# parse arguments
args = parser.parse_args()
argsdict = vars(args)
noresults = argsdict['noresults']
orgname = argsdict['orgname']
G_DEVELOPER_KEY = argsdict['G_DEVELOPER_KEY']
G_CX_KEY = argsdict['G_CX_KEY']
verbose = argsdict['verbose']
debug = argsdict['debug']
B_API_KEY = argsdict['B_API_KEY']

if debug:
	verbose = True

# if no orgname provided, grab here
if orgname == None:
	orgname = raw_input('Organization name: ')
query = 'site:linkedin.com inurl:pub -inurl:dir "at " ' + '"' + str(orgname) + '"' + ' \'Current\''

# parse config file
config = ConfigParser.ConfigParser()
config.read('config.cfg')

# parse api keys
try:
	G_DEVELOPER_KEY = config.get('GOOGLE_API_KEYS', 'G_DEVELOPER_KEY')
	if G_DEVELOPER_KEY == None:
		if verbose:
			print "WARN: No Google Developer Key found!"
			G_DEVELOPER_KEY = raw_input('Enter your Google Developer Key (developerKey): ')
except ConfigParser.NoOptionError:
	if verbose:
		print "WARN: G_DEVELOPER_KEY not found in config.cfg"
	G_DEVELOPER_KEY = raw_input('Enter your Google Developer Key (developerKey): ')
	pass
if debug:
	print "DEBUG: Google Dev key is: ", G_DEVELOPER_KEY, type(G_DEVELOPER_KEY)

try:
	G_CX_KEY = config.get('GOOGLE_API_KEYS', 'G_CX_KEY')
	if G_CX_KEY == None:
		if verbose:
			print "WARN: No Google CSE key found!"
		G_CX_KEY = raw_input('Enter your Google CSE key (G_CX_KEY): ')
except ConfigParser.NoOptionError:
	if verbose:
		print "WARN: G_CX_KEY not found in config.cfg"
	G_CX_KEY = raw_input('Enter your Google CSE key (G_CX_KEY): ')
	pass
if debug:
	print "DEBUG: Google CSE key is: ", G_CX_KEY, type(G_CX_KEY)

try:
	B_API_KEY = config.get('BING_API_KEYS', 'B_API_KEY')
	if B_API_KEY == None:
		if verbose:
			print "WARN: No Bing Web Search API Key Found!"
		B_API_KEY = raw_input('Enter your Bing Web Search API Key: ')
except ConfigParser.NoOptionError:
	if verbose:
		print "WARN: B_API_KEY not found in config.cfg"
	B_API_KEY = raw_input('Enter your Bing Web Search API key: ')
	pass
if debug:
	print "DEBUG: Bing API key is ", B_API_KEY, type(B_API_KEY)

if G_CX_KEY or G_DEVELOPER_KEY == None:
	GOOGLE_FLAG = False
else:
	GOOGLE_FLAG = True

if B_API_KEY == None:
	BING_FLAG = False
else:
	BING_FLAG = True


def main():
	if GOOGLE_FLAG == True:
		searchGoogle()
	if BING_FLAG == True:
		searchBing()

def searchGoogle():
	service = build("customsearch", "v1", developerKey=G_DEVELOPER_KEY)
	counter = 1
	while (counter < noresults):
		if debug:
		   print "DEBUG: Is counter <= noresults?: ", (counter < noresults), " Counter: ", counter, " NoResults: ", noresults
		res = service.cse().list(
			q=query,
			cx='G_CX_KEY',
			start=counter,
			num=10,
			lr="lang_en",
			).execute()
		counter += 10
		for item in res['items']:
			try:
				for hcard in item['pagemap']['hcard']:
					if str(orgname).lower() not in str(hcard['title']).lower():
						if debug:
							print "DEBUG: str(orgname) = ", str(orgname).lower(), " str(hcard['title'])", str(hcard['title']).lower()
							if verbose:
								print "INFO: orgname not found in hcard['title']"
								break
						else:
							stdout.write('Name: ')
							stdout.write(re.sub(' \| LinkedIn', ',', str(item['title'])))
							stdout.write(' Role: ')
							stdout.write(str(hcard['title']))
							stdout.write("\n")
			except KeyError:
				if debug:
					print "DEBUG: Caught KeyError exception"
					print item
				try:
					if str(orgname).lower() not in str(item['pagemap']['snippet']).lower():
						if verbose:
							print "INFO: orgname not found in hcard['title'], trying item['pagemap']['snippet']"
						if debug:
							print "DEBUG: str(orgname): ", str(orgname).lower(), " != str(item['pagemap']['snippet']): ", str(item['pagemap']['snippet']).lower()
				except Exception as e:
					print "ERROR: Something weird happened, printing exception: "
					print e
					pass
			except UnicodeEncodeError:
				if debug:
					print "DEBUG: Caught UnicodeEncodeError exception"
					print "DEBUG: Printing item for debugging: "
					print item
					pass
			except HttpError as e:
				print "ERROR: Caught HTTPError, you may be out of queries, see output for more info: "
				print e
				break
			except Exception as e:
				print "Google_ERROR: Something strange happened, printing error: "
				print e
				exit()

def searchBing():
	search_term = "site:linkedin.com instreamset:(url):\"/pub/\" -instreamset:(url):\"/dir/\" && (\"at %s\" || \"at %s\")" % (orgname,orgname.lower())
	bing_web = PyBingWebSearch(B_API_KEY, search_term)
	result = bing_web.search(limit=50, format='json')

	counter = 0
	while counter < 50: 	
		try:
			regex_string = "'\.\s([\w\s]*\sat\s%s)'" % (orgname)
			if debug:
				 print "DEBUG: Bing[", counter,"] first regex_string is: ", regex_string
			m = re.search('\.\s([\w\s]*\sat\sReliaQuest)', result[counter].description, re.IGNORECASE)
			if debug:
				print "DEBUG: Bing[", counter,"] raw results:"
				print "title: ", result[counter].title, " description: ", result[counter].description
			if m == None:
				if debug:
					print "DEBUG: Bing[", counter,"] first regex returned 'None'"
				regex_string = "'^.*at\s%s\.'" % (orgname)
				if debug:
					print "DEBUG: Bing[", counter,"] second regex_string is: ", regex_string
				m = re.search('^.*at\sReliaQuest\.', result[counter].description, re.IGNORECASE)
				if m == None:
					if debug:
						print "DEBUG: Bing[", counter,"] second regex returned 'None'"
					counter+=1
					continue
				else:
					pass
			if debug:
				print "DEBUG: Bing [", counter, "] full regex match: ", str(m.group())
			stdout.write('Name: ')
			stdout.write(str(re.sub(' \| LinkedIn', ',', result[counter].title)))
			stdout.write(' Role: ')
			try:
				stdout.write(str(m.group(1)))
			except IndexError:
				stdout.write(str(m.group()))
				pass
			if verbose:
				stdout.write(' VERBOSE_URL: ')
				stdout.write(result[counter].url)
			stdout.write("\n")
			counter+=1
		except IndexError as e:
			if verbose:
				print "INFO: No additional Bing Search Results available"
			if debug:
				print e
			break
		except Exception as e:
			print "Bing_ERROR: Something strange happened, printing error: "
			print e
			exit()

if __name__ == '__main__':
	main()
