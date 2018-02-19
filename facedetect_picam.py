import cv2
import sys
import numpy as np
import glob
import random
import math
import pygame   #sounds
import time
from time import sleep
import wiringpi # Servo Control
from picamera.array import PiRGBArray
from picamera import PiCamera
from Adafruit_PWM_Servo_Driver import PWM

#pygame.init()
#pygame.mixer.init()
#R2 = pygame.mixer.Sound('/home/pi/Desktop/TheEye/sounds/r2d2.ogg')
#blip1 = pygame.mixer.Sound('/home/pi/Desktop/TheEye/sounds/blip1.ogg')
#blip2 = pygame.mixer.Sound('/home/pi/Desktop/TheEye/sounds/blip2.ogg')

wiringpi.wiringPiSetupGpio()    # use 'GPIO naming'
#pan = 18    # set #18 and 13 to be PWM outputs
#tilt = 13

# Initialise the PWM device using the default address
pwm = PWM(0x40)

pan = 0
tilt = 1
LED = 16
wiringpi.pinMode(LED, 1)
#wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

#wiringpi.pinMode(pan, wiringpi.GPIO.PWM_OUTPUT)
#wiringpi.pinMode(tilt, wiringpi.GPIO.PWM_OUTPUT)
#wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)      # set the PWM mode to milliseconds stype
#wiringpi.pwmSetClock(192)       # divide down clock
#wiringpi.pwmSetRange(2000)

face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]
lastface = 0
faceX, faceY, faceW, faceH = 0,0,0,0

camangle = 25

panCP = 0
panDP = 0
tiltCP = 0
tiltDP = 0

#face detection setup
frontalface = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')      #frontal face
profileface = cv2.CascadeClassifier("haarcascade_profileface.xml")		# side face pattern detection

camera = PiCamera()
width = 320
height = 240
camera.resolution = (width, height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(width, height))

#functions
def runServo(servo, angle):
    if servo==tilt:
        angle = mapValue(angle, 180, 0, 150, 600)
    else:
        angle = mapValue(angle, 0, 180, 150, 600)
    pwm.setPWM(servo,0,angle)
def mapValue(x,in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r+=step
def swirlMode():
    swirltimer=time.time()
    #R2.play()
    for i in drange(0,360,0.1):
        a = 25*math.sin(i)+80
        b = 25*math.cos(i)+100
        runServo(pan,int(a))
        runServo(tilt,int(b))
        sleep(0.012)
        if time.time()-swirltimer>1.5:
            #runServo(pan, 90)
            #runServo(tilt, 90)
            return
def random():
    panvalue = 70
    tiltvalue = 140
    runServo(pan, int(mapValue(panvalue,width,0,150,60)))
    runServo(tilt, int(mapValue(tiltvalue,height,0,0,70)))
    time.sleep(1.5)
    panvalue = 120
    tiltvalue = 150
    runServo(pan, int(mapValue(panvalue,width,0,150,60)))
    runServo(tilt, int(mapValue(tiltvalue,height,0,0,70)))
    time.sleep(1)
    panvalue = 100
    tiltvalue = 130
    runServo(pan, int(mapValue(panvalue,width,0,150,60)))
    runServo(tilt, int(mapValue(tiltvalue,height,0,0,70)))
    time.sleep(1)
    panvalue = 100
    tiltvalue = 160
    runServo(pan, int(mapValue(panvalue,width,0,150,60)))
    runServo(tilt, int(mapValue(tiltvalue,height,0,0,70)))
    time.sleep(2)

ravenmode=False
swirlmode=False
swirltimer=time.time()
lasttime=time.time()
wiringpi.digitalWrite(LED,1)

#set servos to initial position
runServo(pan, 100)
runServo(tilt, 50)
random()
sleep(1)
print "starting..."
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    image = frame.array
    rawCapture.truncate(0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceFound = False
    if not faceFound:
        if lastface == 0 or lastface == 1:
            fface = frontalface.detectMultiScale(gray,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(30,30))
            if fface != ():		# if we found a frontal face...
                lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
                for f in fface:		# f in fface is an array with a rectangle representing a face
                    faceFound = True
                    face = f
                    
    if not faceFound:				# if we didnt find a face yet...
        if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
            pfacer = profileface.detectMultiScale(gray,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(40,40))
            if pfacer != ():		# if we found a profile face...
                lastface = 2
                for f in pfacer:
                    faceFound = True
                    face = f

    if not faceFound:				# a final attempt
        if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
            cv2.flip(image,1,image)	#	flip the image
            pfacel = profileface.detectMultiScale(gray,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(40,40))
            if pfacel != ():
                lastface = 3
                for f in pfacel:
                        faceFound = True
                        face = f
                face[0] = width - face[0] - 150 #flip coordinate x with a joker value of 150...........
            cv2.flip(image,1,image)	#flip the image back

    if not faceFound:		        #if no face was found...-
	lastface = 0		        #the next loop needs to know
	#face = [width/2,height/2,1,1]   #default position

    x,y,w,h = face
    Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center
    print str(Cface[0]) + "," + str(Cface[1])

    if faceFound:
        lasttime=time.time()    #reset ravenmode timer
        ravenmode=False
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        panDP=x+w/2
        tiltDP=y+h/2

    if abs(panCP-panDP)>5:
        panCP-=(panCP-panDP)/1.7
        runServo(pan, mapValue(int(panCP), width, 0, 150, 60))
        #sleep(0.01)
    else:
        panCP=panDP
        runServo(pan, mapValue(int(panCP), width, 0, 150, 60))
    if abs(tiltCP-tiltDP)>5:
        tiltCP-=(tiltCP-tiltDP)/1.7
        runServo(tilt, mapValue(int(tiltCP), height, 0, 0, 70))
        #sleep(0.01)
    else:
        tiltCP=tiltDP
        runServo(tilt, mapValue(int(tiltCP), height, 0, 0, 70))
        
    
    #cv2.imshow('Video', image) # Display the resulting frame
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time()-lasttime > 10:
        runServo(pan, 100)
        runServo(tilt, 50)

# When everything is done, release the capture
#camera.release()
cv2.destroyAllWindows()
wiringpi.digitalWrite(LED,0)
