#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

mkdir -p /opt/uptimePageServer

cp start.sh /opt/uptimePageServer
chmod +x /opt/uptimePageServer/start.sh
cp main.py /opt/uptimePageServer
cp requirements.txt /opt/uptimePageServer
cp -r templates /opt/uptimePageServer
cp -r config /opt/uptimePageServer
python3 -m pip install -r /opt/uptimePageServer/requirements.txt

chown -R root:root /opt/uptimePageServer
chmod -R 755 /opt/uptimePageServer

cp uptimePageServer.service /etc/systemd/system
systemctl daemon-reload
systemctl enable uptimePageServer.service
systemctl start uptimePageServer.service

echo "Server installed successfully"