import pygame
import appSettings
import socket
import voxMath
import json
import animation
import assetLoader
import os

# preset window position -- borderless fullscreen
winx, winy = 0, 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(winx,winy)

pygame.init()

display = None

info = pygame.display.Info()
chron = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Creating display ' + str(info.current_w) + 'x' + str(info.current_h)
if appSettings.hwAccel:
    display = pygame.display.set_mode(
        (info.current_w, info.current_h), pygame.NOFRAME)
else:
    display = pygame.display.set_mode(
        (info.current_w, info.current_h), pygame.NOFRAME)

print 'Connecting to service socket'
try:
    client.connect(('localhost', 19700))
except:
    print 'Connection failed, aborting.'
    exit(7)
print 'Connected on port 19700'
client.setblocking(1)
client.settimeout(0.05)

print 'Loading core assets'
assetLoader.loadImage('centercircle')
assetLoader.loadImage('center_battery_fg')

assetLoader.loadFont('header', 24)
bgImage = None

if appSettings.useBgImage:
    bgImage = pygame.transform.scale(pygame.image.load(appSettings.bgImage), (display.get_width(), display.get_height()))


ticksUntilBattData = 5

batteryLevel = 0
isCharging = False

def updateClient():
    global ticksUntilBattData, batteryLevel, isCharging
    if ticksUntilBattData < 1:
        client.send('get batStat\n')
        ticksUntilBattData = 5
    buf = ''
    try:
        buf += client.recv(1024)
    except:
        pass
    tempItems = buf.split(';')
    items = []
    for i in tempItems:
        items.extend(i.split('\n'))
    for j in range(0, len(items)):
        if 'batStat' in items[j]:
            battDict = json.loads(items[j+1])
            batteryLevel = battDict['batteryLife']
            isCharging = battDict['isCharging']
            continue
    ticksUntilBattData -= 1

initialFrame = True

animations = {
    'batteryBar': animation.GUIAnimator(60)
}

tempSurf = assetLoader.imageMap['centercircle']
centercircle = pygame.transform.scale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                 int(tempSurf.get_height() * appSettings.screenRatio)))
tempSurf = assetLoader.imageMap['center_battery_fg']
centerBatteryFg = pygame.transform.scale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                 int(tempSurf.get_height() * appSettings.screenRatio)))

def draw():
    global initialFrame
    dirtyRegions = []
    if appSettings.useBgImage:
        display.blit(bgImage, (0, 0))
    else:
        pygame.draw.rect(display, voxMath.hexToRGB(appSettings.bgColor), (0, 0, display.get_width(),
                                                                          display.get_height()))

    centerpt = voxMath.centerObject(pygame.Rect((0, 0), (centercircle.get_size()[0], centercircle.get_size()[1])),
                                    pygame.Rect((0, 0), (display.get_width(), display.get_height())))
    display.blit(centercircle, centerpt)

    print batteryLevel
    batteryCrop = int((float(centerBatteryFg.get_height()) / 4.0) + (float(centerBatteryFg.get_height())) *
                      (1.0-batteryLevel))
    cropRect = pygame.Rect(0, batteryCrop,
                                    int(centerBatteryFg.get_width()), int(centerBatteryFg.get_height() - batteryCrop))
    centerBatteryFgCrop = centerBatteryFg.subsurface(cropRect)
    display.blit(centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop))

    pygame.display.flip()
    '''if initialFrame:
        pygame.display.flip()
        initialFrame = False
    elif dirtyRegions:
        pygame.display.update(pygame.Rect.unionall_ip(dirtyRegions))'''


def render():
    draw()

running = True

def eventLoop():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print 'User requested exit'
                client.send('quit\n')
                chron.tick(10)
                exit(0)
        updateClient()
        for i in range(0, 5):
            chron.tick(appSettings.fps)
            render()


print 'Starting main event loop'
client.send('get batStat\n')
eventLoop()
