#!/bin/bash

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "****************************************************"
echo "********* LAGERTHA CLIENT INSTALLER * **************"
echo "****************************************************"
echo
echo "This script installs the Lagertha Service on your computer."
read -s -n 1 -p "PRESS ANY KEY TO CONTINUE"
if [ -f /lib/systemd/system/lagertha.service ]; then
	echo -e "\n* Lagertha Service already installed. Exiting."
	exit
fi
echo "*Copying service file"
cp lagertha.service /lib/systemd/system/
echo "*Registering service"
systemctl daemon-reload
echo "Lagertha Service is now installed."
echo "Please run Lagertha Client Registration to complete setup"
