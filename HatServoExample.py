#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)
def mapValue(x,in_min, in_max, out_min, out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  #value = raw_input()
  #value = int(value)
  panvalue = 70
  tiltvalue = 140
  pwm.setPWM(0, 0, int(mapValue(panvalue,0,180,150,600)))
  pwm.setPWM(1, 0, int(mapValue(tiltvalue,0,180,150,600)))
  time.sleep(1.5)
  panvalue = 120
  tiltvalue = 150
  pwm.setPWM(0, 0, int(mapValue(panvalue,0,180,150,600)))
  pwm.setPWM(1, 0, int(mapValue(tiltvalue,0,180,150,600)))
  time.sleep(1)
  panvalue = 100
  tiltvalue = 130
  pwm.setPWM(0, 0, int(mapValue(panvalue,0,180,150,600)))
  pwm.setPWM(1, 0, int(mapValue(tiltvalue,0,180,150,600)))
  time.sleep(1)
  panvalue = 100
  tiltvalue = 160
  pwm.setPWM(0, 0, int(mapValue(panvalue,0,180,150,600)))
  pwm.setPWM(1, 0, int(mapValue(tiltvalue,0,180,150,600)))
  time.sleep(2)
