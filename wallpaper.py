#!/usr/bin/env python
# aptinstall.py

def wallpaper(lag_server):

	import os
	import sys
	import wget
	import urllib

	try:
		urllib.urlretrieve("http://" + lag_server + "/walls/wall.jpg", filename="/usr/share/lagertha/wall.jpg")
		status = 1
		os.system("xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/image-path --set /usr/share/lagertha/wall.jpg")
		return status
	except:
		print "Couldn't download new wallpaper!!!"
		status = 2
		return status
		
