import pygame, math, time
import sys
from pygame.locals import *

class StartupGraphics:

    def __init__(self, scope, resources):
        #initialise pygame
        self.scope = scope #Use a pyscope object so we can run the program from the console
        self.resources = resources #get the resources class instance
        self.start1Time=0
        self.start2Time=3
        self.endTime=8
        self.animationStepMultiplier = float(float(self.start2Time) / float(4))
        self.opacityMultiplier = float(255) / float(self.animationStepMultiplier)
        self.wOpacityIndex=0
        self.wOpacityStartTime=0
        self.yOpacityIndex=0
        self.yOpacityStartTime=float(self.animationStepMultiplier * 1)
        self.logoOpacityIndex=0
        self.logoOpacityStartTime=float(self.animationStepMultiplier * 2)
        self.taglineOpacityIndex=0
        self.taglineOpacityStartTime=float(self.animationStepMultiplier * 3)
        self.status="START1"
        self.currentTime = 0
        self.animation2StepMultiplier = float(float(self.endTime) - float(self.start2Time)) / float(15)

    def draw(self):

        done=False

        #currentStartUpTime = startupTimerCurrent - startupTimerStart
        startupTimerStart=time.time()
        startupTimerCurrent=time.time()

        while done==False:
        
            self.status="STARTFINISH"

            currentTime = startupTimerCurrent - startupTimerStart
            self.currentTime = currentTime

            #print(str(self.start1Time))
            #print(str(self.start2Time))
            if self.start1Time <= self.currentTime and self.currentTime < self.start2Time:
                self.status="START1"
            elif self.currentTime <= self.endTime:
                entryStatus=self.status
                self.status="START2"
            else:
                done=True
                continue

            #draw the current start screen
            if self.status=="START1":
                self.draw1()
            elif self.status=="START2":
                self.draw2()

            startupTimerCurrent=time.time()

    def draw1(self):       
        background_colour = (0,0,0) 
        self.scope.pySurface.fill(background_colour)

        #get the current opacity value
        if self.currentTime < self.yOpacityStartTime:
            #we are just rendering w at the current opacity index
            opacity = float(self.currentTime) * float(self.opacityMultiplier)
        elif self.currentTime < self.logoOpacityStartTime:
            #we are rending w at 255 opacity and y at the current opacity index
            opacity = (float(self.currentTime) * float(self.opacityMultiplier)) - 255
        elif self.currentTime < self.taglineOpacityStartTime:
            #we are rending w and y at 255 opacity and logo at the current opacity index
            opacity = (float(self.currentTime) * float(self.opacityMultiplier)) - 510
        else:
            #we are rending w, y and logo at 255 opacity and the tagline at the current opacity index
            opacity = (float(self.currentTime) * float(self.opacityMultiplier)) - 765

        #get the current opacity index
        imageIndex = 0
        if opacity < 5:
            imageIndex = 0
        elif opacity < 30:
            imageIndex = 1
        elif opacity < 55:
            imageIndex = 2
        elif opacity < 80:
            imageIndex = 3
        elif opacity < 105:
            imageIndex = 4
        elif opacity < 130:
            imageIndex = 5
        elif opacity < 155:
            imageIndex = 6
        elif opacity < 180:
            imageIndex = 7
        elif opacity < 205:
            imageIndex = 8
        elif opacity < 230:
            imageIndex = 9
        elif opacity < 255:
            imageIndex = 10

        #blit the current image to screen
        if self.currentTime < self.yOpacityStartTime:
            #we are just rendering w at the current opacity index
            self.scope.pySurface.blit(self.resources.w[imageIndex],(0,0))
        elif self.currentTime < self.logoOpacityStartTime:
            #we are rending w at 255 opacity and y at the current opacity index
            self.scope.pySurface.blit(self.resources.w[10],(0,0))
            self.scope.pySurface.blit(self.resources.y[imageIndex],(0,0))
        elif self.currentTime < self.taglineOpacityStartTime:
            #we are rending w and y at 255 opacity and logo at the current opacity index
            self.scope.pySurface.blit(self.resources.w[10],(0,0))
            self.scope.pySurface.blit(self.resources.y[10],(0,0))
            self.scope.pySurface.blit(self.resources.logo[imageIndex],(0,0))
        else:
            #we are rending w, y and logo at 255 opacity and the tagline at the current opacity index
            self.scope.pySurface.blit(self.resources.w[10],(0,0))
            self.scope.pySurface.blit(self.resources.y[10],(0,0))
            self.scope.pySurface.blit(self.resources.logo[10],(0,0))
            self.scope.pySurface.blit(self.resources.tag[imageIndex],(0,0))

        self.scope.screen.blit(self.scope.pySurface,(0,0))

        pygame.display.update()

    def draw2(self):
        
        background_colour = (0,0,0) 
        self.scope.pySurface.fill(background_colour)
        currentTime = float(self.currentTime) - float(self.start2Time)
        step = int(currentTime / self.animation2StepMultiplier)
        if step>14:
            step=14
        self.scope.pySurface.blit(self.resources.setup[step],(0,0))
        self.scope.screen.blit(self.scope.pySurface,(0,0))
        pygame.display.update()

    
