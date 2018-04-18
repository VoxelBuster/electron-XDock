def centerObject(childObj, parentObj):
    return parentObj.width / 2 - childObj.width / 2, parentObj.height / 2 - childObj.height / 2

def hexToRGB(hexStr):
    h = hexStr.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
