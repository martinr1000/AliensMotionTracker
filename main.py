#!/usr/bin/python

#Imports
import pygame, random, math, pygame.mixer, os
import time
import sys

time.sleep(5)

gpioAvailable = True
try:
    import RPi.GPIO as GPIO
except:
    gpioAvailable = False
from audio import TrackerAudio
from pygame.locals import *
from resources import resources
from graphics import TrackerGraphics
from pyscope import pyscope
from startup import StartupGraphics
from calibration import Calibration
from calibrationGraphics import CalibrationGraphics

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEO_CENTERED'] = '1'

buttonTimerStart = 0
buttonTimerCurrent = 0
buttonHoldTime = 0
stateString="TRACK"
changeState=True
numberOfButtonPresses=0
buttonHoldTime=0
#(optional LED) led pin number
ledPin=27
#(optional LED) initial state (TRUE is on FALSE is off)
ledState=False
#(optional LED) time for LED when it is on in seconds
ledOnTime=1
#(optional) time for LED when it is off in seconds
ledOffTime=1

if gpioAvailable:
    GPIO.setmode(GPIO.BCM)
    #setup GPIO for tracker button press
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #setup a blinking LED for the tracker
    GPIO.setup(ledPin, GPIO.OUT)
    #set the initial state of the led
    GPIO.output(ledPin, ledState)

def my_callback(channel):

    global numberOfButtonPresses
    global buttonHoldTime
    global buttonTimerStart

    if GPIO.input(20):
        buttonHoldTime = time.time() - buttonTimerStart
        buttonTimerStart=0
    else:
        numberOfButtonPresses=numberOfButtonPresses+1
        buttonTimerStart=time.time()
    
if gpioAvailable:
    GPIO.add_event_detect(20, GPIO.BOTH, callback=my_callback, bouncetime=300)

#initialise pygame
pygame.init()

#initialise required game classes
scope=pyscope()
resources=resources() #get a resources object instance
ca=Calibration(scope, resources)
cg=CalibrationGraphics(scope, resources, ca)
sg=StartupGraphics(scope, resources) #get the startup graphics instance
tg=TrackerGraphics(scope, resources, ca) #get the tracker graphics instance
ta=TrackerAudio(resources) #get the tracker audio instance
pygame.mouse.set_visible(False) # Hide the mouse pointer

#initialise a clock instance so we can control the game loop
my_clock=pygame.time.Clock()

#enter the game loop
wave_size = 0
args=[]
done=False
currentState=True
startupTimerStart=time.time()
startupTimerCurrent=time.time()
qPress = False
os.system("fbcp &")

#show the startup gracphics
sg.draw()

#initialise the clock instance to track led timings
startTime = time.time()
changeLedState = True

try:
    while done==False:

        endTime = time.time()
        elapsedTime = endTime - startTime
        
        if ledState:
           if elapsedTime >= ledOnTime:
               #turn it off
               changeLedState = True
        else:
           if elapsedTime >= ledOffTime:
               #turn it on
               changeLedState = True

        if changeLedState:
          #change the led state
          if ledState:
            ledState = False
            GPIO.output(ledPin, ledState)    
            #set the change state flag to false as we are awaiting the next state change
            changeLedState = False
            #initialise the clock instance to track led timings
            startTime = time.time()
          else:
            ledState = True
            GPIO.output(ledPin, ledState)    
            #set the change state flag to false as we are awaiting the next state change
            changeLedState = False
            #initialise the clock instance to track led timings
            startTime = time.time()

        if numberOfButtonPresses>1:
            addContact = True
            numberOfButtonPresses=0
        else:
            addContact = False

        #process pygame events
        keys=pygame.key.get_pressed()        
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
                pass
            if event.type == pygame.KEYDOWN:
                if event.key==K_q:
                    qPress = True
                    buttonTimerStart=time.time()
                    buttonTimerCurrent=time.time()
                    buttonHoldTime=0
                if event.key==K_x:
                    done=True
                if event.key==K_UP:
                    addContact = True
            if event.type == pygame.KEYUP:
                if event.key==K_q:
                    qPress=False

        if qPress:
            buttonHoldTime = time.time() - buttonTimerStart

        if buttonHoldTime>4:
            buttonHoldTime=0
            stateString="CALIBRATE"
            ca.initCalibration()
            calibrationStep = 0

        if stateString=="CALIBRATE":
            xy = ca.calibrate(calibrationStep)

            if calibrationStep==0:
                cg.initBackground()
                cg.update(xy, ca)
            if calibrationStep==500:
                stateString="TRACK"
            else:
                cg.update(xy, ca)
                calibrationStep=calibrationStep+1
            
        else:

            #process tracker graphics
            args = tg.update(wave_size, addContact, ca)
            if args!=999:
                #process audio
                ta.update(wave_size, args)

                #check the wave size, if it's 16 then reset otherwise increment
                if wave_size==15:
                    wave_size=0
                else:
                    wave_size+=1

        my_clock.tick(21)
finally:
    print "clean exit"

scope.pySurface.fill((0,0,0))
scope.screen.blit(scope.pySurface,(0,0))
GPIO.cleanup()
os.system("killall fbcp")
pygame.quit()
