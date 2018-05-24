# Lagertha Client

The Lagertha Client is a service that allows remote systems management via Lagertha.

Lagertha consists of two components:

>**Lagertha Server** - Creates and manages tasks for Lagertha connected Clients

>**Lagertha Client** - Service that runs on client devices and processes tasks


## Installation

These steps are for installing Lagertha Client on an Ubuntu 16.04.3 box.
Install required python dependencies
```
$ sudo apt-get install git python-apt python-mysql.connector python-configparser python-wget 
```
Clone Lagertha Client to local system
```
$ git clone https://github.com/aaronprisk/lagertha-client.git
$ cd lagertha-client
```
Run Lagertha Client install script and follow steps.
```
$ sudo ./client-install.sh
```
After the install finishes, you'll need to register your host with your Lagertha Server
```
$ cd /usr/share/lagertha
$ sudo ./register.sh
```
Once the Registration completes your system will need to reboot.

The Lagertha Client should now be ready to go!

## What distros are supported?
Right now only Ubuntu-based distros work with the Lagertha Client

## Some Considerations

This project is still very young so please be careful running Lagertha in production. 
