This is The One Eyed Raven
It uses facedetection through OpenCV which maps the position of a face to the angle of two servomotors on a pan-tilt rig.
The motors are then able to "run to the position of a face".
A shell is built around the rig and a homemade iris is then following the movement of a face in front of the eye.

Libraries:
OpenCV2 (face detection)
	sudo apt-get install python-opencv

Wiringpi (GPIO control, if LEDs lights inside the eyeball are wanted)
	cd
	git clone git://git.drogon.net/wiringPi
	cd ~/wiringPi
	git pull origin
	cd ~/wiringPi
	./build
	
Adafruit PCA9685 (pwm library for running servos)
	sudo apt-get install git build-essential python-dev
	sudo pip install adafruit-pca9685

Numpy
	pip install numpy
