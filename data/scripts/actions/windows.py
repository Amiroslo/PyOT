openWindows = 6436, 6437, 6440, 6441, 6444, 6445, 6450, 6451, 6454, 6455, 6458, 6459, 6462, 6463, 6466, 6467, 6470, 6471, 6788, 6789, 7025, 7026,\
            7029, 7030, 10264, 10265, 10488, 10489

closeWindows = 6438, 6439, 6442, 6443, 6446, 6447, 6452, 6453, 6456, 6457, 6460, 6461, 6464, 6465, 6468, 6469, 6472, 6473, 6790, 6791, 7027, 7028,\
            7031, 7032, 10266, 10267, 10490, 10491

def openWindow(creature, thing, position, **k):
    engine.transformItem(thing, thing.itemId+2, position)

def closeWindow(creature, thing, position, **k):
    engine.transformItem(thing, thing.itemId-2, position)

reg('use', openWindows, openWindow)
reg('use', closeWindows, closeWindow)