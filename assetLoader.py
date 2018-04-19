import pygame

pygame.init()

images = {
    'centercircle': 'assets/ui/centercircle.png',
    'center_battery_fg': 'assets/ui/center_battery_fg.png'
}

fonts = {
    'header': 'assets/font/header.ttf',
    'monospace': 'assets/font/monospace.ttf'
}

imageMap = {}

fontsMap = {}

def loadImage(imgid):
    imageMap[imgid] = pygame.image.load(images[imgid]).convert_alpha()

def loadFont(fid, size):
    fontsMap[fid] = pygame.font.Font(fonts[fid], size)
