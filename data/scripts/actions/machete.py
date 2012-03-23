JUNGLE_GRASS_TRANSFORM = {2782, 3985}
JUNGLE_GRASS_REMOVE = {1499}
SPIDER_WEB = {7538, 7539}

def onUseWith(onThing, onPosition, **k):
    if onThing.itemId in JUNGLE_GRASS_REMOVE:
        onThing.transform(0, onPosition)
        onThing.decay(onPosition)
    elif onThing.itemId in JUNGLE_GRASS_TRANSFORM:
        onThing.transform(onThing.itemId - 1, onPosition)
        onThing.decay(onPosition)
    elif onThing.itemId in SPIDER_WEB:
        onThing.transform(onThing.itemId + 6, onPosition)
        onThing.decay(onPosition)
        
register("useWith", (2420, 2442), onUseWith)
