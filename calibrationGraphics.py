import pygame, random, math, time, pygame.mixer
import time
import sys
from pygame.locals import *
from contacts import Contacts,Contact
from resources import resources
from compass import Compass

class CalibrationGraphics:

    smallNumber = ""

    def __init__(self, scope, resources, calibration):
        self.scope = scope #Use a pyscope object so we can run the program from the console
        self.resources = resources #get the resources class instance
        self.calibration = calibration #get a calibration class instance

    def initBackground(self):
        background_colour = (0,0,0) 
        self.scope.screen.fill(background_colour) 

    def update(self, xy, calibration):
        self.scope.screen.blit(self.resources.contactBack[3], (xy[0]-25,xy[1]-25))
        self.scope.screen.blit(self.resources.contactFore[3], (xy[0]-25,xy[1]-25))

        self.draw()    
    
    def draw(self):
        #update the display and show our images  
        pygame.display.update()
