import pygame

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
    'appicon': 'assets/ico/appicon.png'
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
