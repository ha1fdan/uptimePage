#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

systemctl stop uptimePageServer.service
systemctl disable uptimePageServer.service
rm /etc/systemd/system/uptimePageServer.service
rm -rf /opt/uptimePageServer