#!/usr/bin/env python


def remove(pkg_name):

	import apt
	import sys
	import time
	import datetime
	# Set Timestamp variables
	tsu = time.time()
	ts = datetime.datetime.fromtimestamp(tsu).strftime('%Y-%m-%d %H:%M:%S')
	
	cache = apt.cache.Cache()
	cache.open()
	pkg = cache[pkg_name]

	if pkg.is_installed:
		pkg.mark_delete()
	  	try:
	    	    cache.commit()
	  	except Exception, arg:
		    status = 2
		    print >> sys.stderr, " - Sorry, package removal failed [{err}]".format(err=str(arg))
		    with open('aptlog.txt', 'a') as f:
				f.write(ts)
				f.write('Package removal failed!\n')
		else:
		    print "TASK WAS COMPLETED SUCCESFULLY!"
		    status = 1

	else:
	   status = 2
	   print "{pkg_name} NOT installed".format(pkg_name=pkg_name)
	   with open('/var/log/lagertha.log', 'a') as f:
		f.write(ts)
	   	f.write(' - Package is NOT installed the system. \n')

	return status


