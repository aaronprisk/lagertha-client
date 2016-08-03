#!/usr/bin/env python


def update():

	import apt
	import apt.progress
	import sys
	import time
	import datetime

	tsu = time.time()
	ts = datetime.datetime.fromtimestamp(tsu).strftime('%Y-%m-%d %H:%M:%S')


	# First of all, open the cache
	cache = apt.Cache()
	# Now, lets update the package list
	try:
		cache.update()
	except Exception as e:
			error = str(e)
			print "* Could not update cache. Check internet connectivity. \nContinuing update process..."
			with open('aptlog.txt', 'a') as f:
				f.write(ts)
				f.write(" - Could not update cache. Check internet connectivity. \n")

	# We need to re-open the cache because it needs to read the package list
	cache.open(None)
	# Set cache.upgrade() to cache.upgrade(True) for dist-upgrade
	cache.upgrade()
	#Set varaible to record packages involved in upgrade
	pkglist = cache.get_changes()
	if (pkglist == []):
		print "* No packages to update!"
	else:
		print "* Updates to be installed: ", pkglist

	# Call commit() to initiate upgrade
	try:
		cache.commit()
		print "* Following packages were updated:", pkglist
		print "* Update task completed with no major errors."
		status = 1
		with open('aptlog.txt', 'a') as f:
			f.write(ts)
			f.write(' - Update process completed with no major errors.\n')
	except Exception, arg:
		status = 2
		with open('/var/log/lagertha.log', 'a') as f:
			error =  (sys.stderr, " - Sorry, package update failed[{err}]".format(err=str(arg)))
			print >> sys.stderr, " - Sorry, package update failed[{err}]".format(err=str(arg))
			f.write(ts)
			f.write(' - Update task failed!\n')
	return status




