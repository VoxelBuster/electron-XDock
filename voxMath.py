# Various methods used for mathematical and other useful operations
# Created by VoxelBuster

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

def avg(*numbers):
    sum = 0
    for i in numbers:
        sum += i
    return sum / len(numbers)

def getAdjacentItems(lst, center, num_extend):
    final = []
    maxidx = len(lst) - 1
    for i in range(1, num_extend):
        idx = center - i
        if idx < 0:
            idx = maxidx + idx
        final.append(lst[idx])
    final.append(lst[center])
    for i in range(1, num_extend):
        idx = center + i
        if idx > maxidx:
            idx = idx - maxidx
        final.append(lst[idx])
    return final