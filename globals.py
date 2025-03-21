import os
import pygame

DEBUG = False

screen_size = (0,0)
drunkCursorPos = (0,0)

scrollSpeed = 0.15

oppositeSpawnMinTime = 2000
oppositeSpawnMaxTime = 6000

sameSpawnMinTime = 7000
sameSpawnMaxTime = 13000

player = None
notificationManager = None

def scaleMousePos(pos):
    return (pos[0] * (640/screen_size[0]), pos[1] * (360/screen_size[1]))

def map_value(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another.
    
    :param value: The input value to map.
    :param in_min: The minimum of the input range.
    :param in_max: The maximum of the input range.
    :param out_min: The minimum of the output range.
    :param out_max: The maximum of the output range.
    :return: The mapped value in the new range.
    """
    # Normalize the input value to a 0-1 range
    normalized = (value - in_min) / (in_max - in_min)
    
    # Scale to the output range
    return out_min + (normalized * (out_max - out_min))

def drawFPSCounter(screen,clock,font="arial",size=20,color=(255,255,255),bold=False,italic=False): #Draws the fps counter
    fps=round(clock.get_fps())
    screen.blit(renderText("FPS: "+str(fps),size=size,color=color,font=font,bold=bold,italic=italic),(0,0))

fonts = {}
texts = {}

def renderText(text,size=20,color=(255,255,255),font="arial",bold=False,italic=False): #allows you to render text fast
    font_key=str(font)+str(size)
    text_key=str(font_key)+str(text)+str(color)
    if not font_key in fonts:
        try:
            fonts[font_key]=pygame.font.SysFont(font,int(size), bold=bold, italic=italic) #Tries to load the file from the system
        except: #If that doesn't work
            try:
                fonts[font_key]=pygame.font.Font(font,int(size)) #bold/itallic not supported
            except:
                fonts[font_key]=pygame.font.SysFont("comicsansms", int(size), bold=bold, italic=italic)

    if not text_key in texts:
        texts[text_key]=fonts[font_key].render(str(text),1,color)
    return texts[text_key]


import pygame

def blur(surface, amt, iterations=3):
    """
    Applies a smoother blur effect by performing multiple passes of scaling down and up.
    
    Parameters:
      surface: The pygame.Surface to blur.
      amt: The blur factor; higher values produce a stronger blur.
      iterations: The number of passes to perform. More iterations yield a smoother blur.
    
    Returns:
      A new pygame.Surface that is the blurred version of the input.
    """
    blurred = surface.copy()
    for _ in range(iterations):
        width, height = blurred.get_size()
        scale = 1.0 / amt
        # Calculate the new scaled size (ensuring at least 1 pixel in each dimension)
        scaled_size = (max(1, int(width * scale)), max(1, int(height * scale)))
        # Scale down and then back up to achieve the blur effect
        blurred = pygame.transform.smoothscale(blurred, scaled_size)
        blurred = pygame.transform.smoothscale(blurred, (width, height))
    return blurred
