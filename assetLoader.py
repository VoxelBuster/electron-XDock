import pygame
import appSettings
import json
import os
import re

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
    if not os.path.isdir(appSettings.dataDir):
        os.makedirs(appSettings.dataDir)
    obj['dataDir'] = appSettings.dataDir
    obj['debug'] = appSettings.debug
    obj['time12Hr'] = appSettings.time12Hr
    obj['screenRatio'] = appSettings.screenRatio
    obj['fpsMax'] = appSettings.fpsMax
    obj['doubleBuffer'] = appSettings.doubleBuffer
    obj['textGlow'] = appSettings.textGlow
    obj['fpsCounter'] = appSettings.fpsCounter
    obj['useBgImage'] = appSettings.useBgImage
    obj['useWinBg'] = appSettings.useWinBg
    obj['bgColor'] = appSettings.bgColor
    obj['themeColor'] = appSettings.themeColor
    obj['themeAccentColor'] = appSettings.themeAccentColor
    obj['bgImage'] = appSettings.bgImage
    obj['hwAccel'] = appSettings.hwAccel
    obj['visualizer'] = appSettings.visualizer
    obj['visualizerChannel'] = appSettings.visualizerChannel
    obj['amplitudeAverageDepth'] = appSettings.amplitudeAverageDepth
    obj['amplitudeDampen'] = appSettings.amplitudeDampen
    obj['visualizerResolution'] = appSettings.visualizerResolution
    obj['visualizerAlpha'] = appSettings.visualizerAlpha
    obj['visualizerPlacement'] = appSettings.visualizerPlacement
    obj['visualizerColor'] = appSettings.visualizerColor
    obj['amplitudeDampenRadial'] = appSettings.amplitudeDampenRadial
    json.dump(obj, open(appSettings.dataDir + 'appSettings.json', 'w+'))


def readSettings():
    try:
        if os.path.exists(appSettings.dataDir + 'appSettings.json'):
            obj = json.load(open(appSettings.dataDir + 'appSettings.json', 'r'))
            appSettings.dataDir = obj['dataDir']
            appSettings.debug = obj['debug']
            appSettings.time12Hr = obj['time12Hr']
            appSettings.screenRatio = obj['screenRatio']
            appSettings.fpsMax = obj['fpsMax']
            appSettings.doubleBuffer = obj['doubleBuffer']
            appSettings.textGlow = obj['textGlow']
            appSettings.fpsCounter = obj['fpsCounter']
            appSettings.useBgImage = obj['useBgImage']
            appSettings.useWinBg = obj['useWinBg']
            appSettings.bgColor = obj['bgColor']
            appSettings.themeColor = obj['themeColor']
            appSettings.themeAccentColor = obj['themeAccentColor']
            appSettings.bgImage = obj['bgImage']
            appSettings.hwAccel = obj['hwAccel']
            appSettings.visualizerChannel = obj['visualizerChannel']
            appSettings.visualizer = obj['visualizer']
            appSettings.amplitudeAverageDepth = obj['amplitudeAverageDepth']
            appSettings.amplitudeDampen = obj['amplitudeDampen']
            appSettings.visualizerResolution = obj['visualizerResolution']
            appSettings.visualizerAlpha = obj['visualizerAlpha']
            appSettings.visualizerPlacement = obj['visualizerPlacement']
            appSettings.visualizerColor = obj['visualizerColor']
            appSettings.amplitudeDampenRadial = obj['amplitudeDampenRadial']
    except Exception as e:
        print e
        os.remove(appSettings.dataDir + 'appSettings.json')

def readPathsFiles():
    try:
        if os.path.exists(appSettings.dataDir + 'gamesPaths.txt'):
            f = open(appSettings.dataDir + 'gamesPaths.txt', 'r')
            appSettings.gamesPaths.extend(re.compile('(\r\n|\r|\n)').split(f.read()))
        if os.path.exists(appSettings.dataDir + 'appPaths.txt'):
            f = open(appSettings.dataDir + 'appPaths.txt', 'r')
            appSettings.appPaths.extend(re.compile('(\r\n|\r|\n)').split(f.read()))
    except Exception as e:
        print e
