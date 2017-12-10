import os, pygame

#Define display class
class pyscope :
    
    screen = None
    pySurface = None
    
    def __init__(self):
        
        "Initializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(size, flags)
        surface = pygame.Surface((320,240))
        self.pySurface = surface.convert()
        
        # Initialise font support
        pygame.font.init()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
