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

echo "*Creating Lagertha Client Directory"
mkdir /usr/share/lagertha
echo "*Copying Lagertha Scripts"
cp -r * /usr/share/lagertha/ > /dev/null
echo "*Copying service file"
cp install/lagertha.service /lib/systemd/system/
echo "Enter IP Address of Lagertha Server: "
read lagip
sudo sed -i "s/SERVERIP/$lagip/g" /usr/share/lagertha/settings.conf
sudo sed -i "s/SERVERIP/$lagip/g" /usr/share/lagertha/support/register.cnf
echo "*Registering service"
systemctl daemon-reload
echo "------------------------------------------------------------"
echo "*Lagertha Service is now installed."
echo "*Please run Lagertha Client Registration to complete setup:" 
echo "sudo /usr/share/lagertha/register.sh"
