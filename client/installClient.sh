#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

mkdir -p /opt/uptimePageClient

cp start.sh /opt/uptimePageClient
chmod +x /opt/uptimePageClient/start.sh
cp main.py /opt/uptimePageClient
cp requirements.txt /opt/uptimePageClient
python3 -m pip install -r /opt/uptimePageClient/requirements.txt

chown -R root:root /opt/uptimePageClient
chmod -R 755 /opt/uptimePageClient

cp uptimePageClient.service /etc/systemd/system
systemctl daemon-reload
systemctl enable uptimePageClient.service
systemctl start uptimePageClient.service

echo "Client installed successfully"