#!/usr/bin/env python


def install(pkg_name):

	import apt
	import sys
	import time
	import datetime

	tsu = time.time()
	ts = datetime.datetime.fromtimestamp(tsu).strftime('%Y-%m-%d %H:%M:%S')


	cache = apt.cache.Cache()
	cache.open()

	if pkg_name in cache:
		print "* Package found in cache."

		pkg = cache[pkg_name]

		if pkg.is_installed:
			status = 2
	    		print "* {pkg_name} already installed".format(pkg_name=pkg_name)
	    		with open('aptlog.txt', 'a') as f:
				f.write(ts)
	   			f.write(' - Package already installed!\n')


		else:
	  	  pkg.mark_install()

	  	  try:
	    	    cache.commit()
		    status = 1
	  	  except Exception, arg:
		    print >> sys.stderr, " - Sorry, package installation failed [{err}]".format(err=str(arg))
		    with open('aptlog.txt', 'a') as f:
				f.write(ts)
				f.write('Error occured during package install!\n')
		

	else:
		status = 2
		print "*Package not found in cache."
		with open('/var/log/lagertha.log', 'a') as f:
			f.write(ts)
			f.write(' - Package ')
			f.write(pkg_name)
			f.write(' not found in cache. Exiting.\n')

	return status



