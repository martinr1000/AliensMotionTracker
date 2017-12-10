import pygame, random, math, time, pygame.mixer
import time
import sys
from pygame.locals import *
from contacts import Contacts,Contact
from resources import resources
from compass import Compass

class TrackerGraphics:

    smallNumber = ""

    def __init__(self, scope, resources, calibration):
        #initialise pygame
        self.compass=Compass(calibration) #get a compass object
        self.scope = scope #Use a pyscope object so we can run the program from the console
        self.resources = resources #get the resources class instance
        self.contactsArray = Contacts() #get a contacts class instance
        self.text = None
        self.smallnumber_text = None
        self.dots= None
        self.display_scale = None
        self.closest_text = ""
        self.smallnumber = ""

    def update(self, wave_size, addcontact, calibration):

        self.compass.updatexy(calibration)

        if addcontact:
            self.contactsArray.addContact(self.compass.smbusAvailable)

        #Read the current direction of the tracker from the digital compass
        bearing = self.compass.getCompassBearing()

        #rotate the contacts in relation to the grid
        self.contactsArray.updateContactsInWorld(bearing)
      
        #Set the screen background
        backdrop=self.rot_center(self.resources.compass,bearing)
 
        background_colour = (0,0,0) 
        self.scope.pySurface.fill(background_colour) 
        self.scope.pySurface.blit(backdrop,(0,22))
            
        #render our contacts
        if (len(self.contactsArray.ContactArray))>0:
            for x in self.contactsArray.ContactArray:
                trackerScale = self.contactsArray.trackerScale
                opacityIndex = x.getOpacityIndex(wave_size, trackerScale)
                self.scope.pySurface.blit(self.resources.contactBack[opacityIndex], (x.worldX-25,x.worldY-25))
            for x in self.contactsArray.ContactArray:
                trackerScale = self.contactsArray.trackerScale
                opacityIndex = x.getOpacityIndex(wave_size, trackerScale)
                self.scope.pySurface.blit(self.resources.contactFore[opacityIndex], (x.worldX-25,x.worldY-25))

        #render the wave pulse with current wave size
        self.scope.pySurface.blit(self.resources.waves[wave_size], (0,0))

        #Convert the range to the closest blip to text. If no blip present display dashes
        if self.contactsArray.getClosestContactDistance() == 999:
            self.closest_text = ""
            self.smallnumber= ""
        else:
            if wave_size==0:
                self.closest_text=str(self.contactsArray.getClosestContactDistance())
                self.smallnumber = str(random.randint(10,99))
        
        range_prefix=""
        if len(self.closest_text)==1:
            range_prefix='0'
        if len(self.closest_text)==2:
            range_prefix=''
        
        #Render the display
        self.text = self.resources.font.render(str(bearing),1,(215,0,0))
        self.text = self.resources.font.render(range_prefix+self.closest_text,1,(215,0,0))
        self.smallnumber_text=self.resources.smallfont.render(self.smallnumber,1,(215,0,0))
        self.dots = self.resources.smallfont.render("-",1,(215,0,0))
        self.display_scale=self.resources.displayScaleFont.render('m',1,(215,0,0))

        #render the info panel to screen
        self.scope.pySurface.blit(self.resources.info,(0,182))
        self.scope.pySurface.blit(self.text,(129,182))
        self.scope.pySurface.blit(self.smallnumber_text,(170,182))
        self.scope.pySurface.blit(self.dots,(162,182))
        self.scope.pySurface.blit(self.display_scale,(178,195))
        self.scope.screen.blit(self.scope.pySurface,(0,0))

        #update the display and show our images  
        pygame.display.update()

        if wave_size==15:
            self.contactsArray.moveContacts()

        return self.contactsArray

    #Define the image rotation function
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle * -1)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
