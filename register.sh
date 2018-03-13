#!/bin/bash

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "****************************************************"
echo "******** LAGERTHA CLIENT REGISTRATION **************"
echo "****************************************************"
echo


#Stop Lagertha Service if Running
echo "* Stopping Lagertha Service."
$(service lagertha stop)

# Checking distro
os=$(lsb_release -sd)

#Find MAC address of ethernet interface
if [ -f /sys/class/net/e*/address ]; then
	echo "* Found ethernet interface. Pulling address.";
	mac=$(cat /sys/class/net/e*/address)
fi

echo "* Connecting to Lagertha Server."
echo "* Checking to see if host is already registered."
newhost=$(mysql --defaults-file=/usr/share/lagertha/support/register.cnf -s -N << EOF
use lagertha;
SELECT hostname as "" FROM hosts WHERE mac LIKE '$mac';
EOF
)

# If client is not registered, go through registration process
if [ -z "$newhost" ]; then
	#Assign existing hostname to $hostn
	hostn=$(cat /etc/hostname)

	echo "* Host is NOT registered."
	echo "*******************REGISTRATION*********************"
	#Display existing hostname
	echo "* Existing local hostname is: $hostn"
	
	#Ask for new hostname $newhost
	echo "* Enter hostname for registration: "
	read newhost
	
	#Check DB for host with that entered hostname
	nameexist=$(mysql --defaults-file=/usr/share/lagertha/support/register.cnf << EOF
	use lagertha;
	SELECT COUNT(hostname) as "" FROM hosts WHERE hostname ='$newhost';
EOF
	)
	#Check DB for host with that entered hostname and loop until corrected
	while [[ $nameexist -ne "0" ]];
	do
		#If name already exists prompt for reentry	
		echo "* $newhost is already in use. Enter new hostname for client: "
		read newhost

		nameexist=$(mysql --defaults-file=/usr/share/lagertha/support/register.cnf << EOF
		use lagertha;
		SELECT COUNT(hostname) as "" FROM hosts WHERE hostname ='$newhost';
EOF
		)
	done
	

	#change hostname in /etc/hosts & /etc/hostname
	sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
	sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
	
	#set mac address in lagertha config file
	sudo sed -i "s/MACADDRESS/$mac/g" /usr/share/lagertha/settings.conf

	#display new hostname
	echo "* Your new hostname: $newhost has been set"
	echo "* Registering with Lagertha Server..."
	echo "*****************************************************"
	mysql --defaults-file=/usr/share/lagertha/support/register.cnf << EOF
	use lagertha;
	INSERT INTO hosts (mac, hostname, os, details) VALUES ('$mac', '$newhost', '$os', 'Registered via Client Tool');
EOF
	echo "Lagertha Client setup is complete!"
	#Press a key to reboot and finish setup
	read -s -n 1 -p "PRESS ANY KEY TO REBOOT AND COMPLETE SETUP"
	sudo reboot

fi

# If client is already registered set hostname assigned in DB
echo "* This client is already registered as: $newhost"
echo "* Setting local hostname.."
	#Assign existing hostname to $hostn
	hostn=$(cat /etc/hostname)
	#change hostname in /etc/hosts & /etc/hostname
	sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
	sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
	
#set mac address in lagertha config file if not already done
sudo sed -i "s/MACADDRESS/$mac/g" /usr/share/lagertha/settings.conf

echo "*****************************************************"
echo "* Lagertha Client setup is complete!"
#Press a key to reboot and finish setup
read -s -n 1 -p "PRESS ANY KEY TO REBOOT AND COMPLETE SETUP"
#Reboot computer to complete setup
sudo reboot
