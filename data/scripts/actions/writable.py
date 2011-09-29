def writable(creature, thing, position, stackpos, **k):
    windowId = creature.textWindow(thing, True, thing.maxTextLen or 0xFF, thing.text if thing.text else "", thing.writtenBy if thing.writtenBy else "", thing.written if thing.written else "") 

    # Function for the writeback
    def writeback(text):
        if len(text) > thing.maxTextLen:
            text = text[:thing.maxTextLen]
            
        thing.text = text
        thing.writtenBy = creature.name()
        thing.written = int(time.time())
        transformTo = thing.writeOnceItemId
        if transformTo:
            thing.itemId = transformTo
            creature.replaceItem(position, stackpos, thing)
            
    creature.windowHandlers[windowId] = writeback
    
useScript = game.scriptsystem.get("use")
for item in game.item.items:
    if item and "writable" in item:
        useScript.reg(game.item.reverseItems[item["cid"]], writable)