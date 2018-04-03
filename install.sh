#!/bin/sh

if [ $USER != "root" ]
  then echo "please run this script as root"
  exit
fi


#copy the systemd service
cp /home/pi/datalogger/tcp.service /etc/systemd/system/tcp.service
chown root /etc/systemd/system/tcp.service
chmod 777 /etc/systemd/system/tcp.service

#enable the server to start it after boot
systemctl enable tcp.service
