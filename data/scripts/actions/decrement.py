decrease = 1480, 1635, 1637, 1639, 1641, 1787, 1789, 1791, 1793, 1874, 1876, 1946, 2038, 2040, 2059, 2061, 2065, 2067, 2069, 2163, 2579, 3698,\
            3700, 3710, 3744, 3746, 3948, 3950, 7059, 8685, 8687, 8689, 8691, 9576, 9578, 9580, 9582, 9748, 9750, 9826, 9828, 9885, 9888, 9890,\
            9893, 9896, 9899, 9902, 9905

def onUse(creature, thing, position, stackpos, **k):
    if position[0] == 0xFFFF:
        thing.itemId -= 1
        creature.replaceItem(position, stackpos, thing)
    else:
        engine.transformItem(thing, thing.itemId-1, position)

reg('use', decrease, onUse)