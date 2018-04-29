import pygame
import appSettings
import json
import os

pygame.init()

images = {
    'centercircle': 'assets/ui/centercircle.png',
    'center_battery_fg': 'assets/ui/center_battery_fg.png',
    'game_icon': 'assets/ui/game.png',
    'exit_icon': 'assets/ui/exit.png',
    'gear_icon': 'assets/ui/gear.png',
    'power_icon': 'assets/ui/power.png',
    'search_icon': 'assets/ui/search.png',
    'game_icon_hl': 'assets/ui/game-highlighted.png',
    'exit_icon_hl': 'assets/ui/exit-highlighted.png',
    'gear_icon_hl': 'assets/ui/gear-highlighted.png',
    'power_icon_hl': 'assets/ui/power-highlighted.png',
    'search_icon_hl': 'assets/ui/search-highlighted.png',
    'appicon': 'assets/ico/appicon.png',
    'cb_checked': 'assets/ui/cb_checked.png',
    'cb_unchecked': 'assets/ui/cb_unchecked.png'
}

fonts = {
    'header': 'assets/font/header.ttf',
    'monospace': 'assets/font/monospace.ttf'
}

imageMap = {}

fontsMap = {}

def loadImage(imgid):
    temp = pygame.image.load(images[imgid])
    if appSettings.hwAccel:
        surf = pygame.Surface((temp.get_width(), temp.get_height()), pygame.HWSURFACE)
    else:
        surf = pygame.Surface((temp.get_width(), temp.get_height()))
    temp = temp.convert_alpha(surf)
    surf = surf.convert_alpha()
    surf.fill((0, 0, 0, 0))
    surf.blit(temp, (0, 0))
    imageMap[imgid] = surf

def loadExtImg(filename):
    temp = pygame.image.load(filename)
    if appSettings.hwAccel:
        surf = pygame.Surface((temp.get_width(), temp.get_height()), pygame.HWSURFACE)
    else:
        surf = pygame.Surface((temp.get_width(), temp.get_height()))
    temp = temp.convert_alpha(surf)
    surf = surf.convert_alpha()
    surf.fill((0, 0, 0, 0))
    surf.blit(temp, (0, 0))
    return surf

def loadFont(fid, size):
    fontsMap[fid] = pygame.font.Font(fonts[fid], size)


def writeOutSettings():
    obj = {}
    os.makedirs(appSettings.dataDir)
    for attrStr in dir(appSettings):
        obj[attrStr] = getattr(appSettings, attrStr)
    json.dump(obj, open(appSettings.dataDir + 'appSettings.json', 'w+'))

def readSettings():
    if os.path.exists(appSettings.dataDir + 'appSettings.json'):
        obj = json.load(open(appSettings.dataDir + 'appSettings.json', 'r'))
        for attrStr in dir(appSettings):
            setattr(appSettings, attrStr, obj[attrStr])