#!/bin/sh
#launcher.sh
#navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/pi/Desktop/TheEye
sudo python facedetect_picam.py &
cd /
