#!/usr/bin/env python
import argparse
from sys import argv, stdout
from googleapiclient.discovery import build
import re
import ConfigParser

# Setup for argument parsing
parser = argparse.ArgumentParser(prog=str(argv[0]), usage='%(prog)s [options]', description='Google Linkedin Scraper to enumerate current employees at a given organization with publicly available Linkedin profiles')

parser.add_argument('-n', help='Number of results from Google', dest='noresults', default=50)
parser.add_argument('-o', help='Name of organization to search for', dest='orgname')
parser.add_argument('--dev-key', help='Your Google Developer Key', dest='DEVELOPER_KEY', required=False)
parser.add_argument('--cx-key', help='Your Google Custom Search Engine key', dest='CX_KEY', required=False)
parser.add_argument('-v', "--verbose", help="Verbose output", action="store_true", dest='verbose')
parser.add_argument('-d', "--debug", help="Debugging output (implies -v)", action="store_true", dest='debug')

# parse arguments
args = parser.parse_args()
argsdict = vars(args)
noresults = argsdict['noresults']
orgname = argsdict['orgname']
DEVELOPER_KEY = argsdict['DEVELOPER_KEY']
CX_KEY = argsdict['CX_KEY']
verbose = argsdict['verbose']
debug = argsdict['debug']

if debug:
	verbose = True

# if no orgname provided, grab here
if orgname == None:
	orgname = raw_input('Organization name: ')
query = 'site:linkedin.com inurl:pub -inurl:dir "at " ' + '"' + str(orgname) + '"' + ' \'Current\''

# parse config file
config = ConfigParser.ConfigParser()
config.read('config.cfg')
if DEVELOPER_KEY == None:
	try:
		DEVELOPER_KEY = config.get('GOOGLE_API_KEYS', 'DEVELOPER_KEY')
		if DEVELOPER_KEY == None:
			if verbose:
				print "WARN: No Google Developer Key found!"
			DEVELOPER_KEY = raw_input('Enter your Google Developer Key (developerKey): ')
	except ConfigParser.NoOptionError:
		if verbose:
			print "WARN: DEVELOPER_KEY not found in config.cfg"
		DEVELOPER_KEY = raw_input('Enter your Google Developer Key (developerKey): ')
		pass
	if debug:
		print "DEBUG: Google Dev key is: ", DEVELOPER_KEY, type(DEVELOPER_KEY)

if CX_KEY == None:
	try:
		CX_KEY = config.get('GOOGLE_API_KEYS', 'CX_KEY')
		if CX_KEY == None:	
			if verbose:
				print "WARN: No Google CSE key found!"
			CX_KEY = raw_input('Enter your Google CSE key (cx_key): ')
	except ConfigParser.NoOptionError:
		if verbose:
			print "WARN: CX_KEY not found in config.cfg"
		CX_KEY = raw_input('Enter your Google CSE key (cx_key): ')
		pass
	if debug:
		print "DEBUG: Google CSE key is: ", CX_KEY, type(CX_KEY)

exit()


def main():
	# Visit the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your applicatoin. Copy config.exmpl to config.txt and fill it out
	service = build("customsearch", "v1", developerKey=DEVELOPER_KEY) #pull from config file, set config file to .gitignore, but make template
	counter = 1
	while (counter < noresults):
		if debug:
			print "DEBUG: Is counter <= noresults?: ", (counter < noresults), " Counter: ", counter, " NoResults: ", noresults
		res = service.cse().list(
			q=query,
			cx='CX_KEY', #pull from config file, set config file to .gitignore, but make template
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
						print "Something weird happened, printing exception: "
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
					exit()
				except Exception as e:
					print "ERROR: Something strange happened, printing error: "
					print e
					exit()


if __name__ == '__main__':
  main()
