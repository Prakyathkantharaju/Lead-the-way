import pygame.camera
import pygame.image
import sys

pygame.camera.init()

# overlay = pygame.image.load("overlay.png")
#overlay = pygame.image.load('overlay.bmp')

cameras = pygame.camera.list_cameras()

print("Using camera %s ..." % cameras[0])

webcam = pygame.camera.Camera(cameras[0])

webcam.start()

# grab first frame
img = webcam.get_image()

WIDTH = img.get_width() * 2
HEIGHT = img.get_height()
print(WIDTH)
print(HEIGHT)

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption("pyGame Camera View")

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()
    
    # draw frame
    screen.blit(img, (0,0))
    # screen.blit(overlay,(258,178))
    pygame.display.flip()
    # grab next frame    
    img = webcam.get_image()