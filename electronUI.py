import pygame
import appSettings
import socket
import voxMath
import json
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
        (info.current_w * appSettings.screenRatio, info.current_h * appSettings.screenRatio), pygame.NOFRAME)
else:
    display = pygame.display.set_mode(
        (info.current_w * appSettings.screenRatio, info.current_h * appSettings.screenRatio), pygame.NOFRAME)

print 'Connecting to service socket'
try:
    client.connect(('localhost', 19700))
except:
    print 'Connection failed, aborting.'
    exit(7)
print 'Connected on port 19700'
client.setblocking(1)
client.settimeout(0.1)

print 'Loading core assets'
assetLoader.loadImage('centercircle')
assetLoader.loadImage('center_battery_fg')

assetLoader.loadFont('header', 24)
bgImage = None

if appSettings.useBgImage:
    bgImage = pygame.transform.scale(pygame.image.load(appSettings.bgImage), (display.get_width(), display.get_height()))


ticksUntilBattData = 5

def updateClient():
    global ticksUntilBattData
    if ticksUntilBattData < 1:
        client.send('get batStat\n')
        ticksUntilBattData = 5
    buf = ''
    try:
        buf += client.recv(1024)
    except:
        pass
    print buf
    tempItems = buf.split(';')
    items = []
    for i in tempItems:
        items.extend(i.split('\n'))
    for j in range(0, len(items)):
        if 'batStat' in items[j]:
            battDict = json.loads(items[j+1])
            print str(battDict['batteryLife'])
            continue
    ticksUntilBattData -= 1

initialFrame = True

def draw():
    global initialFrame
    dirtyRegions = []
    if appSettings.useBgImage:
        display.blit(bgImage, (0, 0))
    else:
        pygame.draw.rect(display, voxMath.hexToRGB(appSettings.bgColor), (0, 0, display.get_width(), display.get_height()))

    if initialFrame:
        pygame.display.flip()
        initialFrame = False
    elif dirtyRegions:
        pygame.display.update(pygame.Rect.unionall_ip(dirtyRegions))


def render():
    draw()

running = True

def eventLoop():
    while running:
        updateClient()
        for i in range(0, 5):
            chron.tick(appSettings.fps)
            render()


print 'Starting main event loop'
client.send('get batStat\n')
eventLoop()
