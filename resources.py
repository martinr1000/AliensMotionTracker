import pygame, sys, os

#load resources for the tracker
class resources:

    def __init__(self):

        current_file_path = __file__
        current_file_dir = os.path.dirname(__file__)
        resourcesDirPath = current_file_dir + "//resources"

        #Load the audio files
        self.click=pygame.mixer.Sound(resourcesDirPath + "/click.wav")
        self.audioBlip = []
        self.audioBlip.append(pygame.mixer.Sound(resourcesDirPath + "/trackerF.wav"))
        self.audioBlip.append(pygame.mixer.Sound(resourcesDirPath + "/trackerE.wav"))
        self.audioBlip.append(pygame.mixer.Sound(resourcesDirPath + "/trackerD.wav"))
        self.audioBlip.append(pygame.mixer.Sound(resourcesDirPath + "/trackerC.wav"))
        self.audioBlip.append(pygame.mixer.Sound(resourcesDirPath + "/trackerB.wav"))
         
        #Load the image files
        self.info=pygame.image.load(resourcesDirPath + "/hudBottom.png").convert()
        self.compass=pygame.image.load(resourcesDirPath + "/motiontrackerhud.png").convert()

        #get the startup settings screens
        self.setup=[]
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon1.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon2.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon3.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon4.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon5.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon6.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon7.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon8.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon9.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon10.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon11.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon12.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon13.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon14.png").convert())
        self.setup.append(pygame.image.load(resourcesDirPath + "//startup//start2//icon15.png").convert())

        #get the weyland image animation frames
        self.w=[]
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_5.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_30.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_55.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_80.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_105.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_130.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_155.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_180.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_205.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_230.png").convert_alpha())
        self.w.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy1_255.png").convert_alpha())

        #get the yutani image animation frames
        self.y=[]
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_5.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_30.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_55.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_80.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_105.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_130.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_155.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_180.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_205.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_230.png").convert_alpha())
        self.y.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy2_255.png").convert_alpha())

        #get the weyland yutani logo image animation frames
        self.logo=[]
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_5.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_30.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_55.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_80.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_105.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_130.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_155.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_180.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_205.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_230.png").convert_alpha())
        self.logo.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy3_255.png").convert_alpha())

        #get the weyland yutani tagline image animation frames
        self.tag=[]
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_5.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_30.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_55.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_80.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_105.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_130.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_155.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_180.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_205.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_230.png").convert_alpha())
        self.tag.append(pygame.image.load(resourcesDirPath + "//startup//start1//wy4_255.png").convert_alpha())

        #load the background contact images
        self.contactBack = []
        for i in range(0,4,1):
            imageName = resourcesDirPath + "/contactback" + str(i) + ".png"
            self.contactBack.append(pygame.image.load(imageName).convert_alpha())

        #load the foreground contact images
        self.contactFore = []
        for i in range(0,4,1):
            imageName = resourcesDirPath + "/contactfore" + str(i) + ".png"
            self.contactFore.append(pygame.image.load(imageName).convert_alpha())

        #load the radar wave images                  
        self.waves = []
        for i in range(0,16,1):
            imageName = resourcesDirPath + "/motiontrackerrings" + str(i) + ".png"
            self.waves.append(pygame.image.load(imageName).convert_alpha())

        #load the fonts
        self.font = pygame.font.Font(None, 38)
        self.smallfont = pygame.font.Font(None, 25)
        self.displayScaleFont = pygame.font.Font(None, 20)
