smbusAvailable = True
try:
    import smbus
except:
    smbusAvailable = False
import time, math, os, random

class Calibration:

    xOffset = 0
    yOffset = 0

    def __init__(self, scope, resources):

        current_file_path = __file__
        self.offsetFilePath = os.path.dirname(__file__) + "//offsets.txt"

        #initialise smbus and read existing values
        self.smbusAvailable = smbusAvailable
        if self.smbusAvailable:
            #setup the digital compass
            try:
                self.bus=smbus.SMBus(1)
                self.address=0x1e
            except:
                self.smbusAvailable = False
                return
            
        self.xOffset = 0
        self.yOffset = 0
        self.readOffsetsFromFile()
    
    def read_byte(self, adr): 
        return self.bus.read_byte_data(address, adr)
    
    def read_word(self, adr): 
        high = self.bus.read_byte_data(self.address, adr) 
        low = self.bus.read_byte_data(self.address, adr+1) 
        val = (high << 8) + low 
        return val 

    def read_word_2c(self, adr): 

        val = self.read_word(adr) 
        if (val >= 0x8000): 
            return -((65535 - val) + 1) 
        else: 
            return val 

    def write_byte(self, adr, value): 
        self.bus.write_byte_data(self.address, adr, value) 

    #define a method to read the existing x and y offset values from file
    def readOffsetsFromFile(self):
        try:
            target = open(self.offsetFilePath, 'r')
        except:
            self.xOffset = 0
            self.yOffset = 0
            return

        contents = target.readlines()
        target.close()
        try:
            self.xOffset = float(contents[0].rsplit('=', 1)[-1])
            self.yOffset = float(contents[1].rsplit('=', 1)[-1])
        except:
            self.xOffset = 0
            self.yOffset = 0

    #define a method to write the new x and y offset values back to file
    def writeOffsetsToFile(self):
        try:
            target = open(self.offsetFilePath, 'w')
        except:
            return

        xOffsetString = "xOffset=" + self.xOffset.string()
        yOffsetString = "yOffset=" + self.yOffset.string()

        target.write(xOffsetString)
        target.write(yOffsetString)
        target.close()
            

    #init calibration
    def initCalibration(self):

        if smbusAvailable:

            self.write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz 
            self.write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default) 
            self.write_byte(2, 0b00000000) # Continuous sampling 

            #scale = 0.92 

        self.minx = 0 
        self.maxx = 0 
        self.miny = 0 
        self.maxy = 0 

    #calibration method
    def calibrate(self, index):

        #read calibration steps
        if index<500:

            if self.smbusAvailable:
                x_out = self.read_word_2c(3) 
                y_out = self.read_word_2c(7) 
                z_out = self.read_word_2c(5)
            else:
                #compass is unavailable so provide random values to test
                #calibration graphics
                angle = random.randint(0, 359)
                dist = random.randint(100,150)
                xmultiplier = math.sin(math.radians(angle))
                x_out = dist*xmultiplier
                ymultiplier = math.cos(math.radians(angle))
                y_out = dist*ymultiplier

            if x_out < self.minx: 
                self.minx=x_out 

            if y_out < self.miny: 
                self.miny=y_out
                    
            if x_out > self.maxx: 
                self.maxx=x_out 

            if y_out > self.maxy: 
                self.maxy=y_out

            return x_out,y_out

        else:

            #update the x and y offset values
            self.xOffset = (self.maxx + self.minx) / 2
            self.yOffset = (self.maxy + self.miny) / 2

            #update the file offset values
            self.writeOffsetsToFile()

            return self.xOffset,self.yOffset
