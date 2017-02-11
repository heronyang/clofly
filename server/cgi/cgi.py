#!/usr/bin/env python
import sys, os

print "Content-Type: text/plain\n";

print 'Requested path: ' + os.environ["PATH_INFO"]

print '========= OS Environment Items =========\n'

for name, value in os.environ.items():
	print '%s\t= %s <br/>' % (name, value)
