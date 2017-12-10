import math,sys
smbusAvailable = True
try:
    import smbus
except:
    smbusAvailable = False

class Compass :

    def __init__(self, calibration):

        self.scale = 0.92
        self.xOffset = calibration.xOffset
        self.yOffset = calibration.yOffset

        self.smbusAvailable = smbusAvailable
        if self.smbusAvailable:
            #setup the digital compass
            try:
                self.bus=smbus.SMBus(1)
                self.address=0x1e
            except:
                self.smbusAvailable = False
                return

            #initialize the compass
            try:
                self.write_byte(0, 0b01110000) # set to 8 samples @ 15Hz
            except:
                self.smbusAvailable = False
                return
            self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 10190 (default)
            self.write_byte(2, 0b00000000) # continuous sampling

    #if the calibration object has been updated then update the compass calibration offsets
    def updatexy(self, calibration):
        self.xOffset = calibration.xOffset
        self.yOffset = calibration.yOffset

    def getXyz(self):
        #Read the current direction of the tracker from the digital compass if available
        returnArray = ([])
        if self.smbusAvailable:
            try:
                returnArray.append((self.read_word_2c(3) - self.xOffset) * self.scale)
                returnArray.append((self.read_word_2c(7) - self.yOffset) * self.scale)
                returnArray.append(self.read_word_2c(5) * self.scale)
            except:
                returnArray = ([])
                returnArray.append(999)
        else:
            returnArray.append( 1 )
            returnArray.append( 0 )
            returnArray.append( 0 )
        return returnArray

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address,adr)

    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self,adr):
        val=self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val)+1)
        else:
            return val

    def write_byte(self, adr, value):
        self.bus.write_byte_data(self.address, adr, value)

    def getCompassBearing(self):

        xyz = self.getXyz()
        x_out = xyz[0]
        y_out = xyz[1]

        #Convert the reading from the digital compass to a bearing in degrees
        bearing = math.atan2(y_out, x_out)

        if (bearing < 0):
            bearing += 2 * math.pi

        bearing=math.degrees(bearing)

        return bearing
