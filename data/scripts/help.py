import game.scriptsystem as scriptsystem
from packet import TibiaPacket
from game.map import placeCreature, getTile
import game.engine, game.item
from game.creature import Creature
import game.errors

def callback(player, text):
    player.message("No you!!")
    
def repeater(player, text):
    player.message(text)
    
def teleporter(player, text):
    x,y,z = text.split(',')
    pos = [int(x),int(y),int(z)]
    try:
        player.teleport(pos)
    except game.errors.SolidTile:
        player.message("Can't teleport to solid tiles!")
    else:
        player.message("Welcome to %s" % text)
    
def tiler(player, text):
    #try:
        global last
        if len(text.split(" ")) < 2:
            pos = player.position
            id = int(text.split(" ")[0])
        else:
            x,y,z = text.split(" ")[0].split(',')
            pos = [int(x),int(y),int(z)]
            id = int(text.split(" ")[1])
            
        if not id in game.item.items:
            player.message("Item not found!")
            return False
        item = game.item.Item( id )
        last = id
        getTile([pos[0], pos[1]-1, pos[2]]).setThing(0, item)

        game.engine.updateTile([pos[0], pos[1]-1, pos[2]], getTile([pos[0], pos[1]-1, pos[2]]))
        player.magicEffect([pos[0], pos[1]-1, pos[2]], 0x03)
    #except:
    #    player.message("Not possible!")
        return False
        
global last
last = 0
def tilerE(player, text):
    global last
    last += 1
    return tiler(player, str(last))
    
def mypos(player, text):
    player.message("Your position is: "+str(player.position))
    print str(player.position) # Print to console to be sure
scriptsystem.get("talkaction").reg("help", callback)
scriptsystem.get("talkactionFirstWord").reg('rep', repeater)
scriptsystem.get("talkactionFirstWord").reg('teleport', teleporter)
scriptsystem.get("talkactionFirstWord").reg('set', tiler)
scriptsystem.get("talkaction").reg('t', tilerE)
scriptsystem.get("talkaction").reg('mypos', mypos)
def speedsetter(player, text):
    try:
        player.setSpeed(int(text))
    except:
        player.message("Invalid speed!")
scriptsystem.get("talkactionFirstWord").reg('speed', speedsetter)



# First use of actions :p
def testContainer(creature, thing, position, stackpos, index):
    # Each time you open it, add a bag. I use this code to test max capasity stuff
    if position[1] == 3:
        bag1 = game.item.Item(1987)
        thing.container.placeItem(bag1)
    
    
    if not thing.opened:
        # Open a bag inside a bag?
        open = True
        bagFound = creature.getContainer(index)    
            
        if bagFound:
            # Virtual close
            creature.openContainers[index].opened = False
                
            # Virtual switch
            thing.opened = True
            thing.parent = creature.openContainers[index]
                
            # Update the container
            creature.updateContainer(thing, parent=1)
            open = False
        
        if open:
            # Open a new one
            parent = 0

            if position[0] == 0xFFFF and position[1] >= 64:
                parent = 1
                item.parent = creature.openContainers[position[2]-64]
            creature.openContainer(thing, parent=parent)

        # Opened from ground, close it on next step :)
        if position[0] != 0xFFFF:
            creature.scripts["onNextStep"].append(lambda who: creature.closeContainer(thing))
    else:
        creature.closeContainer(thing)
        
scriptsystem.get("use").reg(1987, testContainer)


def makeitem(creature, text):
    try:
        count = 1
        if ' ' in text:
            count = int(text.split(" ")[1])
        text = int(text.split(" ")[0])
        if text >= 1000:
            newitem = game.item.Item(text, count)
            bag = creature.inventory[2]
            creature.itemToContainer(bag, newitem)
        else:
            raise
    except:
        creature.message("Invalid Item!")
         
    return False

scriptsystem.get("talkactionFirstWord").reg('i', makeitem)


# Reimport tester
def reimporter(player, text):
    scriptsystem.reimporter()
    return False

def saySomething(player, text):
    player.say("Test 1")
    return False
    
scriptsystem.get("talkaction").reg('reload', reimporter)
scriptsystem.get("talkaction").reg('reloadtest', saySomething)

# Tester of container functions
def popItems(player, text):
    i,c = map(int, text.split(" "))
    item = player.findItemById(i,c)
    return False
    
scriptsystem.get("talkactionFirstWord").reg('pop', popItems)