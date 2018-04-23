from datetime import datetime
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
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(winx, winy)

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
pygame.display.set_caption('Windows X Holo Dock')
assetLoader.loadImage('appicon')
pygame.display.set_icon(assetLoader.imageMap['appicon'])

print 'Connecting to service socket'
try:
    client.connect(('localhost', 19700))
except:
    print 'Connection failed, aborting.'
    exit(7)
print 'Connected on port 19700'
client.setblocking(1)
client.settimeout(1 / appSettings.fpsMax)

print 'Loading core assets'
assetLoader.loadImage('centercircle')
assetLoader.loadImage('center_battery_fg')
assetLoader.loadImage('exit_icon')
assetLoader.loadImage('exit_icon_hl')

assetLoader.loadFont('header', 96)
assetLoader.loadFont('monospace', 36)
bgImage = None

if appSettings.useBgImage:
    bgImage = pygame.transform.smoothscale(pygame.image.load(appSettings.bgImage),
                                           (display.get_width(), display.get_height()))


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


ticksUntilBattData = 5

batteryLevel = 0
isCharging = False

winBg = None

smPaths = []
shortcuts = []


def updateClient():
    global ticksUntilBattData, batteryLevel, isCharging, winBg, smPaths
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
    # print items
    for j in range(0, len(items)):
        if 'batStat' in items[j]:
            battDict = json.loads(items[j + 1])
            batteryLevel = float(battDict['batteryLife'])
            isCharging = bool(battDict['isCharging'])
            continue
        elif 'winBg' in items[j]:
            # print items[j+1]
            winBg = pygame.transform.smoothscale(pygame.image.load(items[j + 1]).convert(), (display.get_width(),
                                                                                             display.get_height()))
            continue
        elif 'smPaths' in items[j]:
            smPaths = json.loads(items[j + 1])['paths']
            for path in smPaths:
                for directory, subdirs, files in os.walk(path):
                    for filename in files:
                        shortcuts.append(os.path.join(path, directory, filename))
            print shortcuts
    ticksUntilBattData -= 1


initialFrame = True

animations = {
    'batteryBar': animation.GUIAnimator(60),
    'mm_expand': animation.GUIAnimator(15)
}

centerScreen = (display.get_width() / 2, display.get_height() / 2)
centerRadius = 512 * appSettings.screenRatio

animations['batteryBar'].loop = True

tempSurf = assetLoader.imageMap['centercircle']
centercircle = pygame.transform.scale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                 int(tempSurf.get_height() * appSettings.screenRatio)))
centerpt = voxMath.centerObject(pygame.Rect((0, 0), (centercircle.get_size()[0], centercircle.get_size()[1])),
                                    pygame.Rect((0, 0), (display.get_width(), display.get_height())))
ccRect = pygame.Rect(centerpt[0], centerpt[1], centercircle.get_width(), centercircle.get_height())

centercircle.set_colorkey((0, 0, 0), pygame.RLEACCEL)
tempSurf = assetLoader.imageMap['center_battery_fg']
centerBatteryFg = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                          int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['exit_icon']
exit_icon = pygame.transform.scale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                 int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['exit_icon_hl']
exit_icon_hl = pygame.transform.scale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                 int(tempSurf.get_height() * appSettings.screenRatio)))

expandMainMenu = False

exitRect = pygame.Rect(0, 0, 0, 0)

def draw():
    global initialFrame, exitRect
    # dirtyRegions = []
    if appSettings.useBgImage:
        if appSettings.useWinBg:
            display.blit(winBg, (0, 0))
        else:
            display.blit(bgImage, (0, 0))
    else:
        pygame.draw.rect(display, voxMath.hexToRGB(appSettings.bgColor), (0, 0, display.get_width(),
                                                                          display.get_height()))

    display.blit(centercircle, centerpt)

    batteryCrop = int((float(centerBatteryFg.get_height()) / 4.0) + (float(centerBatteryFg.get_height()) / 2.0) *
                      (1.0 - batteryLevel))
    cropRect = pygame.Rect(0, batteryCrop, centerBatteryFg.get_width(), int(centerBatteryFg.get_height() - batteryCrop))
    centerBatteryFgCrop = centerBatteryFg.subsurface(cropRect)
    if isCharging:
        absAlpha = int(255.0 * float(((animations['batteryBar'].getCurrentFrame()) % 30) / 30.0))
        if animations['batteryBar'].getCurrentFrame() >= 30:
            blit_alpha(display, centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop), 255 - absAlpha)
        else:
            blit_alpha(display, centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop), absAlpha)
    else:
        display.blit(centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop))

    hour = datetime.now().hour % 12
    if hour == 0:
        hour = 12
    minute = datetime.now().minute
    timeStr = '{:02d}'.format(hour) + ' : ' + '{:02d}'.format(minute)
    timeSurf = assetLoader.fontsMap['header'].render(timeStr, 1, voxMath.hexToRGB('#00fbfe'))
    centertimept = voxMath.centerObject(pygame.Rect((0, 0), (timeSurf.get_size()[0], timeSurf.get_size()[1])),
                                        pygame.Rect((0, 0), (display.get_width(), display.get_height())))
    display.blit(timeSurf, centertimept)
    if expandMainMenu:
        animations['mm_expand'].advance()
        tempPt = (centerScreen[0] - (exit_icon.get_width() / 2), centerScreen[1] + centerRadius)
        exitRect = pygame.Rect(tempPt[0], tempPt[1], exit_icon.get_width(), exit_icon.get_height())
        display.blit(exit_icon, tempPt)
    if appSettings.fpsCounter:
        fpsStr = 'FPS: ' + str(int(chron.get_fps()))
        fpsSurf = assetLoader.fontsMap['monospace'].render(fpsStr, 1, voxMath.hexToRGB('#00fbfe'))
        display.blit(fpsSurf, (25, 25))
    pygame.display.flip()
    '''if initialFrame:
        pygame.display.flip()
        initialFrame = False
    elif dirtyRegions:
        pygame.display.update(pygame.Rect.unionall_ip(dirtyRegions))'''


def render():
    animations['batteryBar'].advance()
    draw()


running = True


def eventLoop():
    global expandMainMenu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print 'User requested exit'
                client.send('quit\n')
                chron.tick(10)
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))  # Triggers a quit event with alt-f4
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ccRect.collidepoint(pygame.mouse.get_pos()):
                    expandMainMenu = not expandMainMenu
                if expandMainMenu:
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))  # Triggers a quit event with alt-f4
        updateClient()
        if not expandMainMenu:
            animations['mm_expand'].reset()
        for i in range(0, 5):
            chron.tick(appSettings.fpsMax)
            render()


print 'Starting main event loop'
client.send('get batStat\n')
eventLoop()
