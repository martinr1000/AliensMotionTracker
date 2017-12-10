import pygame, random, math, time, pygame.mixer
import time
import sys
from pygame.locals import *
from contacts import Contacts,Contact
from pyscope import pyscope
from resources import resources
from compass import Compass

class TrackerAudio:

    pygame.mixer.pre_init(44100, -16, 1, 4096)
    pygame.mixer.init()

    def __init__(self, resources):
        #initialise pygame
        self.resources = resources #get the resources class instance
        self.contactsArray = None

    def update(self, wave_size, contactsArray):

        self.contactsArray = contactsArray
        closestDist = self.contactsArray.getClosestContactDistance()

        sounds = []
        if wave_size==0:
            if closestDist==999:
                sounds.append(self.resources.click)
            if closestDist!=999:
                index = self.getSoundDistance()

                sounds.append(self.resources.click)
                sounds.append(self.resources.audioBlip[index])

        for i in range(0,(len(sounds)), 1):
            sounds[i].set_volume(1.0)
            sounds[i].play()

    #get the index of the audio blip representing the nearest contact
    def getSoundDistance(self):
    
        #trackerScale = self.contactsArray.trackerScale
        trackerScale = 30
        audioSize = float(len(self.resources.audioBlip))
        blipIncrement = float(trackerScale) / float(len(self.resources.audioBlip))
        closestDist = self.contactsArray.getClosestContactDistance()

        for x in range(1, len(self.resources.audioBlip)):
            if closestDist<=(x * blipIncrement):
                return x-1
        return int(len(self.resources.audioBlip)-1)
