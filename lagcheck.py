#!/usr/bin/python
#Lagertha Client - V0.75
import mysql.connector as lagertha
import time
import random
import apt
import sys
from datetime import datetime
from ConfigParser import SafeConfigParser
from aptinstall import install
from aptremove import remove
from aptupdate import update
from wallpaper import wallpaper

#Pull server settings from config file
config = SafeConfigParser()
config.read("/usr/share/lagertha/settings.conf")
lag_server = config.get('SERVER','lag_server')
mac = config.get('CLIENT','mac')
lag_db = config.get('SERVER','lag_db')
lag_user = config.get('SERVER','lag_user')
lag_pass = config.get('SERVER','lag_pass')

#Set default values
status = "0"

# Connect to Lagertha Server
lagertha_connection = lagertha.connect(host=lag_server, user=lag_user, password=lag_pass, database=lag_db)
cursor = lagertha_connection.cursor(buffered=True)

# Update check frequency
try:
	cursor.execute("SELECT check_freq FROM settings WHERE settings_id = 1")
	
except lagertha.Error as dberr:
	        print("* Could not pull settings from Lagertha Server.. {}".format(dberr))
		print "* Skipping check frequency update."
else:	

		print "* Setting client check frequency.."
		new_freq = str(cursor.fetchone()[0])
		config.set('CLIENT','check_freq',new_freq)
		with open('/usr/share/lagertha/settings.conf', 'wb') as configfile:
			config.write(configfile)

# Set check frequency variable
check_freq = int(config.get('CLIENT','check_freq'))


# Main task check loop
while True:


	try:
		cursor.execute("SELECT taskid,tasktype,package FROM tasks WHERE mac = " + mac + " AND pending = 1")

	except lagertha.Error as dberr:
	        print("* Could not connect to Lagertha Server.. {}".format(dberr))
		print "* Retrying in 10 seconds..."
		time.sleep(10)
	else:	
		print "* Connected to Lagertha server... Checking for pending tasks"
		for taskid, tasktype, package in cursor:
			cur_task = taskid
			pkgname = package
			task = tasktype
			print("* TASK FOUND: Tasks Type: {}").format(tasktype)
			if task == 0: 
				print "* UPDATE task found.. Starting update process.."
				status = update()
				query = str("UPDATE tasks SET pending =0, status =" + str(status) + " WHERE taskid =" + str(cur_task))
				cursor.execute(query)
			elif task == 1:
				print "* INSTALL task found.. Starting install process.."
				status = install(pkgname)
				query = str("UPDATE tasks SET pending =0, status =" + str(status) + " WHERE taskid =" + str(cur_task))
				cursor.execute(query)
			elif task == 2:
				print "* REMOVE task found.. Starting removal process.."
				status = remove(pkgname)
				query = str("UPDATE tasks SET pending =0, status =" + str(status) + " WHERE taskid =" + str(cur_task))
				cursor.execute(query)
			elif task == 3:
				print "* WALLPAPER task found.. Starting wallpaper process.."
				status = wallpaper(lag_server)
				query = str("UPDATE tasks SET pending =0, status =" + str(status) + " WHERE taskid =" + str(cur_task))
				cursor.execute(query)

		#Update timestamp of latest task check
		curtime = datetime.now()
		hostquery = str("UPDATE hosts SET last_check = '" + str(curtime) + "' WHERE mac = " + mac)
		cursor.execute(hostquery)

		#Commit queries, close mySQL session and wait for next check
		lagertha_connection.commit()
		lagertha_connection.close()
		nextchk= random.random()*check_freq
		print "* Next task check in ",nextchk, "seconds."
		time.sleep(nextchk)

		#Reconnect for next check
		lagertha_connection = lagertha.connect(host=lag_server, user=lag_user, password=lag_pass, database=lag_db)
		cursor = lagertha_connection.cursor(buffered=True)



	



