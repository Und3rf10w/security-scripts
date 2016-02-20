#!/usr/bin/env python

import socket
import sys
if len(sys.argv) != 3:
	print "Usage: %s <hostname> <username>" % sys.argv[0]
	sys.exit(1)

# Create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the Server
connect=s.connect((sys.argv[1],25))
# Receive the banner
banner=s.recv(1024)
# print banner
# VRFY a user
s.send('VRFY ' + sys.argv[2] + '\r\n')
result=s.recv(1024)
if result == "502 Use HELO/EHLO first.":
	print "WARN: Server returned:\n%s" % result
	print "INFO: Sending HELO message"
	s.send ('HELO vrfytester' + '\r\n')
	result=s.recv(1024)
	print "INFO: Retrying VRFY request"
	s.send('VRFY ' + sys.argv[2] + '\r\n')
	result=s.recv(1024)
	if result == "502 VRFY disallowed.":
		print "ERR: VRFY disallowed on server!"
		s.close()
		sys.exit(2)
	else:
		print result
elif result.split(' ', 1)[0] == "550":
	print "WARN: Username unknown, server returned:\n%s" % result
	sys.exit(2)
else:
	print result

# Close the socket
s.close()
sys.exit(0)
