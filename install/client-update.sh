#!/bin/bash
#Lagertha Client Update Tool
#Version 1.0

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

clear
echo "***********************************"
echo "*** LAGERTHA CLIENT UPDATE TOOL ***"
echo "***          VERSION 1.0        ***"
echo "***********************************"
echo

wget -q http://LAGERTHA/client/VERSION -O /tmp/LAGVERSION

source /tmp/LAGVERSION
echo "Server Version is:"
echo $LAGVERSION
echo "-------------------"
source /usr/share/lagertha/install/VERSION
echo "Current Version is:"
echo $CURVERSION
echo

if [[ $CURVERSION < $LAGVERSION ]]; then
	echo "* STOPPING LAGERTHA SERVICE"
	sudo service lagertha stop
	echo "* DOWNLOADING UPDATE"
        wget -q http://LAGERTHA/client/client.tar.gz -O /tmp/client.tar.gz
	echo "* EXTRACTING UPDATE"
	tar -xf /tmp/client.tar.gz -C /usr/share/lagertha
	echo "* SETTING FILE PERMISSIONS"
	sudo chmod +x /usr/share/lagertha/*.py
	sudo chmod +x /usr/share/lagertha/*.sh
	sudo chmod +x /usr/share/lagertha/install/*.sh
	echo "* UPDATE COMPLETE. RESTARTING LAGERTHA CLIENT."
	sudo service lagertha restart
	echo "* UPDATE TOOL WILL CLOSE IN 5 SECONDS..."
	sleep 5
	exit
fi

echo "No update needed. Exiting update tool..."
sleep 5
exit
