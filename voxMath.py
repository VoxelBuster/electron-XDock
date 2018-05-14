def centerObject(childObj, parentObj):
    return parentObj.width / 2 - childObj.width / 2, parentObj.height / 2 - childObj.height / 2


def alignVertCenters(fixedRect, targetRect):
    return fixedRect.height / 2 - targetRect.height / 2

def addAlphaChannel(rgb, a):
    return rgb[0], rgb[1], rgb[2], a

def hexToRGB(hexStr):
    h = hexStr.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def map(fromFloor, fromCeil, toFloor, toCeil, x):
    fromDelta = fromCeil - fromFloor
    toDelta = toCeil - toFloor
    scaled = float(x - fromFloor) / float(fromDelta)
    return toFloor + (scaled * toDelta)