decayIncrease = {2041, 2044, 2047, 2050, 2052, 2054, 5812, 7183, 9006}
decayDecrease = {2042, 2045, 2048, 2051, 2053, 2055, 2057, 5813}

def onUse(thing, position, **k):
    if thing.itemId in decayIncrease:
        thing.transform(thing.itemId + 1, position)
    elif item.itemId == 2057: # Candelabrum, on
        thing.transform(2041, position)
    else:
        thing.transform(thing.itemId - 1, position)

    thing.decay(position)

reg("use", decayIncrease|decayDecrease, onUse)