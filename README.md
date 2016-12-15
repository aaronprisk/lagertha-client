# Lagertha Client
**PLEASE NOTE: This is still early in the works so it probably won't work quite yet!**

The Lagertha Client is a service that allows remote systems management via Lagertha.

Lagertha consists of two components:

>**Lagertha Server** - Creates manages tasks for Lagertha connected Clients

> **Lagertha Client** - Service that runs on client devices and processes tasks


## Installation

These steps are for installing Lagertha Client on an Ubuntu 16.04  box.
Install required python dependencies
```
$ sudo apt-get install python-apt python-mysql.connector python-configparser python-wget 
```
Create Lagertha Client directory and clone Lagertha Client Repo to local file
```
$ mkdir lagertha-client
$ cd lagertha-client
$ git clone https://github.com/aaronprisk/lagertha-client.git
```
Run Lagertha Client install script
```
$ cd install
$ sudo ./install.sh
```

After the install finishes, you'll need to register your host with your Lagertha Server
```
$ cd /usr/share/lagertha
$ sudo ./register.sh
```
Once the Registration completes your system will need to reboot.

The Lagertha Client should now be ready to go!

## What distros are supported?
Right now only Debian-based distros work with the Lagertha Client

## Some Considerations

This project is still very young so please be careful running Lagertha in production. 
