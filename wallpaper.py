#!/usr/bin/env python
# aptinstall.py

def wallpaper(lag_server,pkgname):

	import os
	import sys
	import wget
	import urllib

	try:
		urllib.urlretrieve("http://" + lag_server + "/" + pkgname, filename="/usr/share/lagertha/wall.jpg")
		status = 1
		os.system("xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/image-path --set /usr/share/lagertha/wall.jpg")
		os.system("xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor1/image-path --set /usr/share/lagertha/wall.jpg")
		return status
	except:
		print "Error: Couldn't download new wallpaper from server"
		status = 2
		return status
		
