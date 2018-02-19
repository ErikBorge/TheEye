import cv2
import sys

# Servo Control
import time
import wiringpi
from time import sleep

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
pan = 18
tilt = 13
wiringpi.pinMode(pan, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(tilt, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
 
# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

facedetected = False
faceX, faceY, faceW, faceH = 0,0,0,0

def runServo(servo, angle):
    wiringpi.pwmWrite(servo, angle+70)


#face detection setup
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 200)		# I have found this to be about the highest-
video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 150)

def mapValue(x,in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

def faceDetect():
    global faceY
    global faceX
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.5,
        minNeighbors=5,
        minSize=(10, 10),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faceX = x
        faceY = y
        faceW = w
        faceH = h
    
    # Display the resulting frame
    cv2.imshow('Video', frame)


while True:
    faceDetect()
    print (faceX+faceW/2, faceY+faceH/2)
    runServo(pan, mapValue(faceX+faceW/2, 200, 0, 60, 100))
    runServo(tilt, mapValue(faceY+faceH/2, 150, 0, 70, 100))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
