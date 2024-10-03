#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

systemctl stop uptimePageClient.service
systemctl disable uptimePageClient.service
rm /etc/systemd/system/uptimePageClient.service
rm -rf /opt/uptimePageClient