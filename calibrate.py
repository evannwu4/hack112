import cv2, pygame, os, sys

def takeImg(camera):      

    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30
     
    # Now we can initialize the camera capture object with the cv2.VideoCapture class.
    # All it needs is the index to a camera port.
     
    # Captures a single image from the camera and returns it in PIL format
    def get_image():
        # read is the easiest way to get a full image out of a VideoCapture object.
        retval, im = camera.read()
        return im
     
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    for i in xrange(ramp_frames):
        temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = blur = cv2.GaussianBlur(get_image(),(15,15),0)
    file = "image.png"
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(file, camera_capture)
     

def getColor():
    pygame.init()
    width = 640
    height = 480
    resolution = (width, height)
    pygame.display.set_mode(resolution)
    screen = pygame.display.get_surface()
    img = pygame.image.load('image.png')
    myfont = pygame.font.SysFont("monospace", 30)
    # render text
    label = myfont.render("Click on your Object!", 1, (255,255,0))
    
    while 1: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
     
        screen.blit(img,(0,0))
        label_rect = label.get_rect(center=(width/2, height/8))
        screen.blit(label, label_rect)
        pygame.display.flip()
        mouseState = pygame.mouse.get_pressed()
        xAdj = 10
        mx, my = pygame.mouse.get_pos()
        color = (100,100,100)
        notClicked = True
        if mouseState[0] and notClicked:
            r = []
            g = []
            b = []
            for i in range(mx-xAdj, mx+xAdj+1):
                for j in range(my-xAdj, my+xAdj+1):
                    color = screen.get_at((i, j))
                    r += [color[0]]
                    g += [color[1]]
                    b += [color[2]]
            color = (sum(r)/len(r), sum(g)/len(g), sum(b)/len(b))
            notClicked = False
        

def run():
    camera = cv2.VideoCapture(0)
    takeImg(camera)
    del(camera)
    getColor()

    
run()
    
