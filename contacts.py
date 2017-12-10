import random, math, sys, pygame

class Contacts():
    # Contacts class acts as storage and processing for
    # individual contact class elements,
    
    def __init__(self):
        # each Contacts class stores an array contact classes
        self.ContactArray = ([])
        self.ClosestScreenDist = 999
        #Declare the tracker maximum scale in meters to scale all screen distance values to
        self.trackerScale = 30

    #define a method to add a contact
    def addContact(self, compassActive):
        if compassActive:
            seedAngle = random.randint(0, 359)
        else:
            seedAngle = 0
            
        #for i in range(0,50,1):
        self.ContactArray.append(Contact(seedAngle))

    #define a function to move all contacts towards the center
    def moveContacts(self):

        newContactArray = ([])

        #loop through the contact array and move each item closer to the center
        #if an item reaches the center do not add it back into the contacts array
        for i in range(0,len(self.ContactArray),1):
            self.ContactArray[i].moveCloser()
            if self.ContactArray[i].outOfScope!=True:
                if self.ContactArray[i].distanceFromCentre<self.ClosestScreenDist:
                    self.ClosestScreenDist = self.ContactArray[i].distanceFromCentre
                
                newContactArray.append(self.ContactArray[i])

        self.ContactArray = newContactArray
        if len(self.ContactArray)==0:
            self.ClosestScreenDist = 999

    #define a function to return the closest screen value converted into the tracker distance scale
    def getClosestContactDistance(self):

        if self.ClosestScreenDist==999:
            contactDist = 999
        else:
            scaleFactor = float(self.trackerScale) / float(182)
            contactDist = scaleFactor * self.ClosestScreenDist
            
        return int(contactDist)

    #define a function to rotate all contacts in relation to the current grid bearing
    def updateContactsInWorld(self, bearing):

        for i in range(0,len(self.ContactArray),1):
            self.ContactArray[i].updateContactInWorld(bearing)

class Contact():
    # Contact contains positional data for a contact blip

    def __init__(self, seedAngle):
       # contact stores x and y positional data
       startPos = self.generateRandomStartPosition(seedAngle)       
       self.x = startPos[0]
       self.y = startPos[1]
       self.centreX = 160
       self.centreY = 182
       self.worldX = startPos[0]
       self.worldY = startPos[1]
       self.distanceFromCentre = 999
       self.opacityIndex = 0
       self.outOfScope = False

    #Define a function that returns an x,y co ordinate for an image given a bearing and distance
    def generateRandomStartPosition(self, seedAngle):

        angle = seedAngle + random.randint(-45, 45)
       
        if angle < 0:
            angle = 360 + angle
        elif angle > 360:
            angle = angle - 360

        startDistance = 182 + random.randint(0, 10)
        xy = self.getNewXY(angle, startDistance)
        return xy

    #define a function to return x/y coordinates for a given distance and bearing from the hud center
    def getNewXY(self,angle,dist):

        #find the x coordinate which is 160 +or- dist * cos angle
        xmultiplier = math.sin(math.radians(angle))
        distSin = dist*xmultiplier
        x = 160+distSin

        #find the y coordinate which is 182 +or- dist * cos angle
        ymultiplier = math.cos(math.radians(angle))
        distCos = dist*ymultiplier
        y = 182-distCos
        
        return (x,y)

    #define function to move contact closer to the center hud position
    def moveCloser(self):

        #get the current x/y coords
        currentX = self.x
        currentY = self.y

        #find the angle that the contact is currently pointing towards
        currentAngle = self.getContactBearing(currentX, currentY)

        #get the current distance from the center to the contact
        currentDist = self.getContactDistanceFromHud(currentX, currentY)

        #reduce the distance by a random amount between 1 and 3
        newDist = currentDist - random.randint(0, 3)

        #set the distance member value
        self.distanceFromCentre = newDist

        #check that the contact is still in scope (i.e. gt 0)
        if newDist <= 0:
          self.outOfScope = True
          return

        #change the bearing randomly with a random increment between +- 3 degrees
        deltaAngle = random.randint(-5, 5)
        newAngle = currentAngle+deltaAngle
        
        if newAngle<0:
            newAngle = 360 + newAngle
        elif newAngle>360:
            newAngle = newAngle - 360

        #get a new set of x/y coords based upon the new bearing and distance
        newXYcoords = self.getNewXY(newAngle, newDist)

        #update the contact x/y position
        self.x = newXYcoords[0]
        self.y = newXYcoords[1]

    #define function to get bearing from the hud center to the contact x/y coordinates
    def getContactBearing(self, x, y):

        dx = x - 160
        dy = y - 182

        if dx==0:
            if dy>0:
                angleDeg = 180
            else:
                angleDeg = 0
            return angleDeg
        else:
            angleRad = math.atan(dy / dx)
            angleDeg = abs(math.degrees(angleRad))

        if dx >= 0:
          if dy <= 0:
             returnAngle = 90 - angleDeg
          else:
             returnAngle = 90 + angleDeg
        else:
          if dy < 0:
             returnAngle = 270 + angleDeg
          else:
             returnAngle = 270 - angleDeg

        return returnAngle

    #define function to get distance from the hud center to the contact x/y coordinates
    def getContactDistanceFromHud(self, x, y):

        dx = x - 160
        dy = y - 182
        
        dist = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
        return dist

    #define a function to rotate each contact
    #about the centre point in relation to the world grid
    def updateContactInWorld(self, bearing):

        worldPoint = ([])
        worldPoint.append(self.x)
        worldPoint.append(self.y)

        centrePoint = ([])
        centrePoint.append(self.centreX)
        centrePoint.append(self.centreY)

        newPoint = self.rotatePoint(centrePoint, worldPoint, bearing)
        self.worldX = newPoint[0]
        self.worldY = newPoint[1]
        return newPoint

    def rotatePoint(self, centerPoint,point,angle): 
        """Rotates a point around another centerPoint. Angle is in degrees. Rotation is counter-clockwise""" 
        angle = math.radians(angle) 
        temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1] 
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle)) 
        temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1] 
        return temp_point

    def getOpacityIndex(self, wave_size, trackerScale):
        "set the opacity index of the current contact, this is used to render"
        "out each contact with respect to the tracker wave"
        multiplier = float(16) / float(trackerScale)
        waveIndex1 = (int(multiplier * self.getContactDistance(trackerScale))-1)

        diff = wave_size-waveIndex1

        #get the current Index based upon the distance of the wave in relation to the conact
        if diff<0:
            return 0
        elif diff<2:
            return 3
        elif diff<10:
            return 2
        elif diff<16:
            return 1
        else:
            return 1

    #define a function to return the closest screen value converted into the tracker distance scale
    def getContactDistance(self, trackerScale):

        scaleFactor = float(trackerScale) / float(182)
        contactDist = scaleFactor * self.distanceFromCentre
            
        return int(contactDist)



            
