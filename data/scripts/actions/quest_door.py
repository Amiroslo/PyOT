doors = 1223, 1225, 1241, 1243, 1255, 1257, 3542, 3551, 5105, 5114, 5123, 5132, 5288, 5290, 5745, 5748, 6202, 6204, 6259, 6261, 6898, 6907,\
        7040, 7049, 8551, 8553, 9175, 9177, 9277, 9279, 10278, 10475, 10484, 10791


def openDoor(creature, thing, position, **k):
    if not thing.actions:
        engine.transformItem(thing, thing.itemId+1, position)
        return

    canEnter = True
    for action in actions:
        if not creature.getStorage(action):
            canEnter = False

    if not canEnter:
        creature.message("The door is sealed against unwanted intruders.")
    
    engine.transformItem(thing, thing.itemId+1, position)

reg('use', doors, openDoor)