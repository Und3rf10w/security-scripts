#!/usr/bin/python
# Simple fuzz against a target
import socket
from sys import exit,argv

if len(argv) < 3:
	print  "Grabs the banner of a remote TCP service"
	print "Usage: %s <Target IP Address/hostname> <Target Port>" % str(argv[0])
	exit(1)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=s.connect((str(argv[1]),int(argv[2])))
s.settimeout(5.0)
print(s.recv(1024)) # Grab the banner, do not remove
s.close()
exit(0)
