import json
import os
import re
import socket
import subprocess
from datetime import datetime

import pygame
from pymunk.vec2d import Vec2d

import animation
import appSettings
import assetLoader
import constants
import gradients
import voxMath

# preset window position -- borderless fullscreen
winx, winy = 0, 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(winx, winy)

pygame.init()

print 'Reading app settings file'
assetLoader.readSettings()

display = None

info = pygame.display.Info()
chron = pygame.time.Clock()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Creating display ' + str(info.current_w) + 'x' + str(info.current_h)
if appSettings.hwAccel:
    if appSettings.doubleBuffer:
        display = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF)
    else:
        display = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.NOFRAME | pygame.HWSURFACE)
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
assetLoader.loadImage('game_icon')
assetLoader.loadImage('game_icon_hl')
assetLoader.loadImage('gear_icon')
assetLoader.loadImage('gear_icon_hl')
assetLoader.loadImage('power_icon')
assetLoader.loadImage('power_icon_hl')
assetLoader.loadImage('search_icon')
assetLoader.loadImage('search_icon_hl')
assetLoader.loadImage('cb_checked')
assetLoader.loadImage('cb_unchecked')

assetLoader.loadFont('header', 96)
assetLoader.loadFont('monospace', 48)

bgImage = pygame.transform.smoothscale(assetLoader.loadExtImg(appSettings.bgImage),
                                       (display.get_width(), display.get_height()))


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    if appSettings.hwAccel:
        temp = pygame.Surface((source.get_width(), source.get_height()), pygame.HWSURFACE).convert(target)
    else:
        temp = pygame.Surface((source.get_width(), source.get_height())).convert(target)
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def command(cmdstr):
    if cmdstr == 'Shut Down':
        subprocess.Popen('shutdown -s', shell=True)
    elif cmdstr == 'Reboot':
        subprocess.Popen('shutdown -r', shell=True)
    elif cmdstr == 'Suspend': # hibernate needs to be off otherwise you might get a nasty bootloop like I did
        subprocess.Popen('powercfg -hibernate off', shell=True)
        subprocess.Popen('%windir%\\System32\\rundll32.exe powrprof.dll,SetSuspendState Standby', shell=True)
    else:
        print cmdstr.replace('\\\\','\\')
        subprocess.Popen('"' + cmdstr.replace('\\\\','\\') + '"', shell=True)

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
        elif 'fgScale' in items[j]:
            appSettings.screenRatio = float(re.sub('[^0-9]', '', items[j + 1]))
    ticksUntilBattData -= 1


# Setting base properties for rendering
initialFrame = True

animations = {
    'battery_bar': animation.GUIAnimator(60),
    'mm_expand': animation.GUIAnimator(10),
    'mm_icon_enter': animation.GUIAnimator(15),
    'mm_icon_exit': animation.GUIAnimator(15),
    'mm_icon_enter2': animation.GUIAnimator(15),
    'mm_icon_exit2': animation.GUIAnimator(15),
    'mm_icon_enter3': animation.GUIAnimator(15),
    'mm_icon_exit3': animation.GUIAnimator(15),
    'mm_icon_enter4': animation.GUIAnimator(15),
    'mm_icon_exit4': animation.GUIAnimator(15),
    'mm_icon_enter5': animation.GUIAnimator(15),
    'mm_icon_exit5': animation.GUIAnimator(15),
    'settings_expand': animation.GUIAnimator(10)
}

selectWheelItems = []
selectWheelCommands = []
selectWheelContext = 0

centerScreen = (display.get_width() / 2, display.get_height() / 2)

animations['battery_bar'].loop = True

tempSurf = assetLoader.imageMap['centercircle']
centercircle = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                       int(tempSurf.get_height() * appSettings.screenRatio)))
centerpt = voxMath.centerObject(pygame.Rect((0, 0), (centercircle.get_size()[0], centercircle.get_size()[1])),
                                pygame.Rect((0, 0), (display.get_width(), display.get_height())))
ccRect = pygame.Rect(centerpt[0], centerpt[1], centercircle.get_width(), centercircle.get_height())

centercircle.set_colorkey((0, 0, 0), pygame.RLEACCEL)
tempSurf = assetLoader.imageMap['center_battery_fg']
centerBatteryFg = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                          int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['exit_icon']
exit_icon = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                    int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['game_icon']
game_icon = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                    int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['gear_icon']
gear_icon = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                    int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['power_icon']
power_icon = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                     int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['search_icon']
search_icon = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                      int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['exit_icon_hl']
exit_icon_hl = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                       int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['game_icon_hl']
game_icon_hl = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                       int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['gear_icon_hl']
gear_icon_hl = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                       int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['power_icon_hl']
power_icon_hl = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                        int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['search_icon_hl']
search_icon_hl = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio),
                                                         int(tempSurf.get_height() * appSettings.screenRatio)))

tempSurf = assetLoader.imageMap['cb_checked']
cb_checked = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio * 0.125),
                                                     int(tempSurf.get_height() * appSettings.screenRatio * 0.125)))

tempSurf = assetLoader.imageMap['cb_unchecked']
cb_unchecked = pygame.transform.smoothscale(tempSurf, (int(tempSurf.get_width() * appSettings.screenRatio * 0.125),
                                                       int(tempSurf.get_height() * appSettings.screenRatio * 0.125)))

hour = datetime.now().hour % 12
if hour == 0:
    hour = 12
minute = datetime.now().minute
timeStr = '{:02d}'.format(hour) + ' : ' + '{:02d}'.format(minute)
timeSurf = assetLoader.fontsMap['header'].render(timeStr, 1, voxMath.hexToRGB(appSettings.themeColor))

settingsHeaderSurf = assetLoader.fontsMap['monospace'].render('Settings', 1, voxMath.hexToRGB(appSettings.themeColor))
settingsHeaderSurf = pygame.transform.smoothscale(settingsHeaderSurf,
                                                  (int(appSettings.screenRatio * settingsHeaderSurf.get_width()),
                                                   int(appSettings.screenRatio * settingsHeaderSurf.get_height())))
dispSettingsLabel = assetLoader.fontsMap['monospace'].render('Display Settings', 1,
                                                             voxMath.hexToRGB(appSettings.themeColor))
dispSettingsLabel = pygame.transform.smoothscale(dispSettingsLabel,
                                                 (int(appSettings.screenRatio * dispSettingsLabel.get_width()),
                                                  int(appSettings.screenRatio * dispSettingsLabel.get_height())))
time12HrLabel = assetLoader.fontsMap['monospace'].render('12-Hour Time', 1, voxMath.hexToRGB(appSettings.themeColor))
time12HrLabel = pygame.transform.smoothscale(time12HrLabel,
                                             (int(appSettings.screenRatio * time12HrLabel.get_width()),
                                              int(appSettings.screenRatio * time12HrLabel.get_height())))
winBgLabel = assetLoader.fontsMap['monospace'].render('Use Desktop BG', 1,
                                                      voxMath.hexToRGB(appSettings.themeColor))
winBgLabel = pygame.transform.smoothscale(winBgLabel,
                                          (int(appSettings.screenRatio * winBgLabel.get_width()),
                                           int(appSettings.screenRatio * winBgLabel.get_height())))
useBgImgLabel = assetLoader.fontsMap['monospace'].render('Background Image', 1,
                                                         voxMath.hexToRGB(appSettings.themeColor))
useBgImgLabel = pygame.transform.smoothscale(useBgImgLabel,
                                             (int(appSettings.screenRatio * useBgImgLabel.get_width()),
                                              int(appSettings.screenRatio * useBgImgLabel.get_height())))
hwAccelLabel = assetLoader.fontsMap['monospace'].render('HW Acceleration', 1, voxMath.hexToRGB(appSettings.themeColor))
hwAccelLabel = pygame.transform.smoothscale(hwAccelLabel,
                                            (int(appSettings.screenRatio * hwAccelLabel.get_width()),
                                             int(appSettings.screenRatio * hwAccelLabel.get_height())))
showFPSLabel = assetLoader.fontsMap['monospace'].render('Show FPS', 1, voxMath.hexToRGB(appSettings.themeColor))
showFPSLabel = pygame.transform.smoothscale(showFPSLabel,
                                            (int(appSettings.screenRatio * showFPSLabel.get_width()),
                                             int(appSettings.screenRatio * showFPSLabel.get_height())))
fgScaleLabel = assetLoader.fontsMap['monospace'].render('FG Scale: ' + str(appSettings.screenRatio), 1,
                                                        voxMath.hexToRGB(appSettings.themeColor))
fgScaleLabel = pygame.transform.smoothscale(fgScaleLabel,
                                            (int(appSettings.screenRatio * fgScaleLabel.get_width()),
                                             int(appSettings.screenRatio * fgScaleLabel.get_height())))
restartLabel = assetLoader.fontsMap['monospace'].render('Restart to apply', 1, voxMath.hexToRGB('#ff0000'))
restartLabel = pygame.transform.smoothscale(restartLabel,
                                            (int(appSettings.screenRatio * restartLabel.get_width()),
                                             int(appSettings.screenRatio * restartLabel.get_height())))

expandMainMenu = False
showSettings = False

exitRect = pygame.Rect(0, 0, 0, 0)
gamesRect = pygame.Rect(0, 0, 0, 0)
gearRect = pygame.Rect(0, 0, 0, 0)
searchRect = pygame.Rect(0, 0, 0, 0)
powerRect = pygame.Rect(0, 0, 0, 0)

needRestart = False

scrollDelta = 0
totalScroll = 0
scrollOffset = 0
scrollMenuClick = False


# REALLY BAD CODING PAST THIS POINT
def draw():
    global initialFrame, exitRect, gamesRect, searchRect, gearRect, powerRect, showSettings, timeSurf, scrollDelta, scrollOffset, totalScroll, scrollMenuClick
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
        absAlpha = int(255.0 * float(((animations['battery_bar'].getCurrentFrame()) % 30) / 30.0))
        if animations['battery_bar'].getCurrentFrame() >= 30:
            blit_alpha(display, centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop), 255 - absAlpha)
        else:
            blit_alpha(display, centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop), absAlpha)
    else:
        display.blit(centerBatteryFgCrop, (centerpt[0], centerpt[1] + batteryCrop))

    centertimept = voxMath.centerObject(pygame.Rect((0, 0), (timeSurf.get_size()[0], timeSurf.get_size()[1])),
                                        pygame.Rect((0, 0), (display.get_width(), display.get_height())))
    display.blit(timeSurf, centertimept)

    if expandMainMenu:  # Engage stupid amounts of vector and animation math
        centerRadius = centercircle.get_height() / 2 * 1.1
        animations['mm_expand'].advance()
        absAlpha = 255 * float(animations['mm_expand'].getCurrentFrame()) / 10.0
        centerRadius -= exit_icon.get_width() - (
                exit_icon.get_width() * float(animations['mm_expand'].getCurrentFrame()) / 10.0)
        tempPt = (centerScreen[0] - (exit_icon.get_width() / 2), centerScreen[1] + centerRadius)
        exitRect = pygame.Rect(tempPt[0], tempPt[1], exit_icon.get_width(), exit_icon.get_height())
        if exitRect.collidepoint(pygame.mouse.get_pos()):
            animations['mm_icon_exit'].reset()
            animations['mm_icon_enter'].advance()
            alphaHl = 255 * float(animations['mm_icon_enter'].getCurrentFrame()) / 15.0
            blit_alpha(display, exit_icon_hl, tempPt, alphaHl)
        else:
            animations['mm_icon_enter'].reset()
            animations['mm_icon_exit'].advance()
            alphaHl = 255 * (1.0 - (float(animations['mm_icon_exit'].getCurrentFrame()) / 15.0))
            blit_alpha(display, exit_icon, tempPt, absAlpha)
            blit_alpha(display, exit_icon_hl, tempPt, alphaHl)
        refVec = Vec2d(0, centerRadius)
        refVec.rotate_degrees(90)
        tempPt = (centerScreen[0] + int(refVec.x) - game_icon.get_width(), centerScreen[1] - game_icon.get_width() / 2)
        gamesRect = pygame.Rect(tempPt[0], tempPt[1], game_icon.get_width(), game_icon.get_height())
        if gamesRect.collidepoint(pygame.mouse.get_pos()):
            animations['mm_icon_exit2'].reset()
            animations['mm_icon_enter2'].advance()
            alphaHl2 = 255 * float(animations['mm_icon_enter2'].getCurrentFrame()) / 15.0
            blit_alpha(display, game_icon_hl, tempPt, alphaHl2)
        else:
            animations['mm_icon_enter2'].reset()
            animations['mm_icon_exit2'].advance()
            alphaHl2 = 255 * (1.0 - (float(animations['mm_icon_exit2'].getCurrentFrame()) / 15.0))
            blit_alpha(display, game_icon, tempPt, absAlpha)
            blit_alpha(display, game_icon_hl, tempPt, alphaHl2)
        refVec.rotate_degrees(-45)
        tempPt = (centerScreen[0] + int(refVec.x) - gear_icon.get_width(), centerScreen[1] + int(refVec.y))
        gearRect = pygame.Rect(tempPt[0], tempPt[1], gear_icon.get_width(), gear_icon.get_height())
        if gearRect.collidepoint(pygame.mouse.get_pos()):
            animations['mm_icon_exit3'].reset()
            animations['mm_icon_enter3'].advance()
            alphaHl3 = 255 * float(animations['mm_icon_enter3'].getCurrentFrame()) / 15.0
            blit_alpha(display, gear_icon_hl, tempPt, alphaHl3)
        else:
            animations['mm_icon_enter3'].reset()
            animations['mm_icon_exit3'].advance()
            alphaHl3 = 255 * (1.0 - (float(animations['mm_icon_exit3'].getCurrentFrame()) / 15.0))
            blit_alpha(display, gear_icon, tempPt, absAlpha)
            blit_alpha(display, gear_icon_hl, tempPt, alphaHl3)
        refVec.rotate_degrees(-90)
        tempPt = (centerScreen[0] + int(refVec.x), centerScreen[1] + int(refVec.y))
        powerRect = pygame.Rect(tempPt[0], tempPt[1], power_icon.get_width(), power_icon.get_height())
        if powerRect.collidepoint(pygame.mouse.get_pos()):
            animations['mm_icon_exit4'].reset()
            animations['mm_icon_enter4'].advance()
            alphaHl4 = 255 * float(animations['mm_icon_enter4'].getCurrentFrame()) / 15.0
            blit_alpha(display, power_icon_hl, tempPt, alphaHl4)
        else:
            animations['mm_icon_enter4'].reset()
            animations['mm_icon_exit4'].advance()
            alphaHl4 = 255 * (1.0 - (float(animations['mm_icon_exit4'].getCurrentFrame()) / 15.0))
            blit_alpha(display, power_icon, tempPt, absAlpha)
            blit_alpha(display, power_icon_hl, tempPt, alphaHl4)
        refVec.rotate_degrees(-45)
        tempPt = (centerScreen[0] + int(refVec.x), centerScreen[1] + int(refVec.y) - search_icon.get_height() / 2)
        searchRect = pygame.Rect(tempPt[0], tempPt[1], search_icon.get_width(), search_icon.get_height())
        if searchRect.collidepoint(pygame.mouse.get_pos()):
            animations['mm_icon_exit5'].reset()
            animations['mm_icon_enter5'].advance()
            alphaHl5 = 255 * float(animations['mm_icon_enter5'].getCurrentFrame()) / 15.0
            blit_alpha(display, search_icon_hl, tempPt, alphaHl5)
        else:
            animations['mm_icon_enter5'].reset()
            animations['mm_icon_exit5'].advance()
            alphaHl5 = 255 * (1.0 - (float(animations['mm_icon_exit5'].getCurrentFrame()) / 15.0))
            blit_alpha(display, search_icon, tempPt, absAlpha)
            blit_alpha(display, search_icon_hl, tempPt, alphaHl5)
    if showSettings:
        animations['settings_expand'].advance()
        s = pygame.Surface((display.get_width() / 4, display.get_height()), pygame.HWSURFACE)
        s.set_alpha(196)  # alpha level
        s.fill(voxMath.hexToRGB(appSettings.themeAccentColor))
        s.blit(settingsHeaderSurf, (10, 20))
        s.blit(time12HrLabel, (25, 75))
        s.blit(useBgImgLabel, (25, 130))
        s.blit(winBgLabel, (25, 185))
        timeLabelRect = pygame.Rect(0, 0, time12HrLabel.get_width(), time12HrLabel.get_height())
        wbgRect = pygame.Rect(0, 0, winBgLabel.get_width(), winBgLabel.get_height())
        useBgRect = pygame.Rect(0, 0, useBgImgLabel.get_width(), useBgImgLabel.get_height())
        hwAccelRect = pygame.Rect(0, 0, hwAccelLabel.get_width(), hwAccelLabel.get_height())
        showFPSRect = pygame.Rect(0, 0, showFPSLabel.get_width(), showFPSLabel.get_height())
        fgScaleRect = pygame.Rect(0, 0, fgScaleLabel.get_width(), fgScaleLabel.get_height())
        cbRect = pygame.Rect(0, 0, cb_checked.get_width(), cb_checked.get_height())
        if appSettings.time12Hr:
            s.blit(cb_checked,
                   (25 + time12HrLabel.get_width() + 20, voxMath.alignVertCenters(timeLabelRect, cbRect) + 75))
        else:
            s.blit(cb_unchecked,
                   (25 + time12HrLabel.get_width() + 20, voxMath.alignVertCenters(timeLabelRect, cbRect) + 75))
        if appSettings.useBgImage:
            s.blit(cb_checked,
                   (25 + useBgImgLabel.get_width() + 20, voxMath.alignVertCenters(useBgRect, cbRect) + 130))
        else:
            s.blit(cb_unchecked,
                   (25 + useBgImgLabel.get_width() + 20, voxMath.alignVertCenters(useBgRect, cbRect) + 130))
        if appSettings.useWinBg:
            s.blit(cb_checked, (25 + winBgLabel.get_width() + 20, voxMath.alignVertCenters(wbgRect, cbRect) + 185))
        else:
            s.blit(cb_unchecked, (25 + winBgLabel.get_width() + 20, voxMath.alignVertCenters(wbgRect, cbRect) + 185))
        s.blit(dispSettingsLabel, (25, 300))
        s.blit(hwAccelLabel, (25, 355))
        s.blit(fgScaleLabel, (25, 410))
        s.blit(showFPSLabel, (25, 465))
        if appSettings.hwAccel:
            s.blit(cb_checked,
                   (25 + hwAccelLabel.get_width() + 20, voxMath.alignVertCenters(hwAccelRect, cbRect) + 355))
        else:
            s.blit(cb_unchecked,
                   (25 + hwAccelLabel.get_width() + 20, voxMath.alignVertCenters(hwAccelRect, cbRect) + 355))
        if appSettings.fpsCounter:
            s.blit(cb_checked,
                   (25 + showFPSLabel.get_width() + 20, voxMath.alignVertCenters(showFPSRect, cbRect) + 465))
        else:
            s.blit(cb_unchecked,
                   (25 + showFPSLabel.get_width() + 20, voxMath.alignVertCenters(showFPSRect, cbRect) + 465))
        if needRestart:
            s.blit(restartLabel, (25, s.get_height() - 60))
        display.blit(s, (display.get_width() - float(s.get_width())
                         * float(animations['settings_expand'].getCurrentFrame() + 1) / 10.0, 0))

    for idx in range(len(selectWheelItems)):
        accentRgb = voxMath.hexToRGB(appSettings.themeAccentColor)
        gradRect = pygame.Rect(0, 0, (display.get_width() - centercircle.get_width()) / 2, display.get_height() / 8)
        centerY = voxMath.alignVertCenters(pygame.Rect((0,0), display.get_size()), gradRect)
        gradSpacing = (gradRect.height + 15)
        totalScroll += scrollDelta * gradSpacing
        scrollDelta = 0
        if totalScroll < -1:
            totalScroll += 2
            scrollOffset -= 2
        elif totalScroll > 1:
            totalScroll -= 2
            scrollOffset += 2
        distanceFromCenterY = scrollOffset + gradSpacing * idx
        if distanceFromCenterY + centerY > display.get_height() or distanceFromCenterY + centerY < 0:
            continue # don't draw stuff that isnt on the screen
        itemSurf = gradients.horizontal((gradRect.width, gradRect.height), voxMath.addAlphaChannel(accentRgb, 0),
                                        voxMath.addAlphaChannel(accentRgb, 127))
        surfText = assetLoader.fontsMap['monospace'].render(selectWheelItems[idx], 0, (255, 255, 255))
        itemSurf.blit(surfText, voxMath.centerObject(pygame.Rect(0, 0, surfText.get_width(), surfText.get_height()), gradRect))
        opacity = int(voxMath.map(0, 512, 255, 0, float(abs(distanceFromCenterY))))
        blit_alpha(display, itemSurf, (display.get_width() - gradRect.width, centerY + distanceFromCenterY), opacity)
        if scrollMenuClick: # woo event handling in the render function
            if pygame.Rect(0, centerY + distanceFromCenterY, display.get_width(), gradRect.height).collidepoint(pygame.mouse.get_pos()):
                if selectWheelContext == 1:
                    command(selectWheelItems[idx])
                else:
                    command(selectWheelCommands[idx])
    scrollMenuClick = False
    if appSettings.fpsCounter:
        fpsStr = 'FPS: ' + str(int(chron.get_fps()))
        fpsSurf = assetLoader.fontsMap['monospace'].render(fpsStr, 1, voxMath.hexToRGB(appSettings.themeColor))
        display.blit(fpsSurf, (25, 25))
    pygame.display.flip()
    '''if initialFrame:
        pygame.display.flip()
        initialFrame = False
    elif dirtyRegions:
        pygame.display.update(pygame.Rect.unionall_ip(dirtyRegions))'''


def render():
    animations['battery_bar'].advance()
    draw()

running = True

def eventLoop():
    global expandMainMenu, showSettings, timeSurf, hour, minute, timeStr, fgScaleLabel, needRestart, selectWheelItems, selectWheelContext, scrollDelta, scrollMenuClick, selectWheelCommands, scrollOffset
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
            # elif event.type == pygame.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selectWheelContext > 0:
                    if event.button == 4:
                        scrollDelta += 1
                    elif event.button == 5:
                        scrollDelta -= 1
                    elif event.button == 1: # oh god this is where it gets dicey
                        if pygame.mouse.get_pos()[0] > float(display.get_width()) * 0.8:
                            scrollMenuClick = True
                if expandMainMenu and event.button == 1:
                    if exitRect.collidepoint(pygame.mouse.get_pos()):
                        pygame.event.post(pygame.event.Event(pygame.QUIT, {}))  # Triggers a quit event with alt-f4
                    elif gearRect.collidepoint(pygame.mouse.get_pos()):
                        showSettings = not showSettings
                        if not showSettings:
                            animations['settings_expand'].reset()
                        expandMainMenu = False
                    elif powerRect.collidepoint(pygame.mouse.get_pos()):
                        showSettings = False
                        animations['settings_expand'].reset()
                        scrollOffset = 0
                        selectWheelContext = 1
                        selectWheelItems = ['Shut Down', 'Reboot', 'Suspend']
                    elif searchRect.collidepoint(pygame.mouse.get_pos()):
                        selectWheelContext = 2
                        scrollOffset = 0
                        selectWheelItems = []
                        selectWheelCommands = []
                        for sc in shortcuts:
                            templist = sc.split('\\')
                            selectWheelItems.append(templist[len(templist) - 1].replace('.lnk',''))
                            selectWheelCommands.append(sc)
                        showSettings = False
                        animations['settings_expand'].reset()
                    elif gamesRect.collidepoint(pygame.mouse.get_pos()):
                        scrollOffset = 0
                        selectWheelContext = 3
                        showSettings = False
                        animations['settings_expand'].reset()
                if ccRect.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                    expandMainMenu = not expandMainMenu
                    if not expandMainMenu:
                        animations['mm_expand'].reverse = True
                    else:
                        animations['mm_expand'].reverse = False
                if showSettings and event.button == 1:
                    selectWheelContext = 0
                    selectWheelItems = []
                    settingsXY = (display.get_width() - display.get_width() / 4, 0)
                    rowRect = pygame.Rect(settingsXY[0], 75, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        appSettings.time12Hr = not appSettings.time12Hr
                        assetLoader.writeOutSettings()
                    rowRect = pygame.Rect(settingsXY[0], 130, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        appSettings.useBgImage = not appSettings.useBgImage
                        assetLoader.writeOutSettings()
                    rowRect = pygame.Rect(settingsXY[0], 185, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        appSettings.useWinBg = not appSettings.useWinBg
                        assetLoader.writeOutSettings()
                    rowRect = pygame.Rect(settingsXY[0], 355, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        appSettings.hwAccel = not appSettings.hwAccel
                        needRestart = True
                        assetLoader.writeOutSettings()
                    rowRect = pygame.Rect(settingsXY[0], 410, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        for i in constants.fgRatioList:
                            if appSettings.screenRatio == constants.fgRatioList[len(constants.fgRatioList) - 1]:
                                appSettings.screenRatio = constants.fgRatioList[0]
                                break
                            if appSettings.screenRatio < i:
                                appSettings.screenRatio = i
                                break
                        needRestart = True
                        assetLoader.writeOutSettings()
                    rowRect = pygame.Rect(settingsXY[0], 465, display.get_width() / 4, 45)
                    if rowRect.collidepoint(pygame.mouse.get_pos()):
                        appSettings.fpsCounter = not appSettings.fpsCounter
                        assetLoader.writeOutSettings()
        updateClient()
        if appSettings.time12Hr:
            hour = datetime.now().hour % 12
            if hour == 0:
                hour = 12
        else:
            hour = datetime.now().hour
        minute = datetime.now().minute
        timeStr = '{:02d}'.format(hour) + ' : ' + '{:02d}'.format(minute)
        timeSurf = assetLoader.fontsMap['header'].render(timeStr, 1, voxMath.hexToRGB('#00fbfe'))
        fgScaleLabel = assetLoader.fontsMap['monospace'].render('FG Scale: ' + str(appSettings.screenRatio), 1,
                                                                voxMath.hexToRGB(appSettings.themeColor))
        fgScaleLabel = pygame.transform.smoothscale(fgScaleLabel,
                                                    (int(appSettings.screenRatio * fgScaleLabel.get_width()),
                                                     int(appSettings.screenRatio * fgScaleLabel.get_height())))
        if not expandMainMenu:
            animations['mm_expand'].reset()
        for i in range(0, 5):
            chron.tick(appSettings.fpsMax)
            render()


print 'Starting main event loop'
client.send('get batStat\n')
eventLoop()
