from game.item import Item
import game.item
from twisted.internet import threads, reactor
from twisted.python import log
import bindconstant
import scriptsystem
from collections import deque
import config
import game.enum
import time
import io
import struct
import sys

##### Position class ####
def __uid():
    idsTaken = 1
    while True:
        idsTaken += 1
        yield idsTaken
instanceId = __uid().next

class Position(object):
    __slots__ = ('x', 'y', 'z', 'instanceId')
    def __init__(self, x, y, z=7, instanceId=None):
        self.x = x
        self.y = y
        self.z = z
        self.instanceId = instanceId
        
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and self.z == other.z and self.instanceId == other.instanceId)
        
    def __ne__(self, other):
        return (self.x != other.x or self.y != other.y or self.z != other.z or self.instanceId != other.instanceId)
        
    def copy(self):
        return Position(self.x, self.y, self.z, self.instanceId)
    
    def inRange(self, other, x, y, z=0):
        return ( self.instanceId == other.instanceId and abs(self.x-other.x) <= x and abs(self.y-other.y) <= y and abs(self.z-other.z) <= y ) 

    """def __setattr__(self, name, val):
        if name == 'x':
            if val > 0xFFFF:
                raise game.errors.PositionOutOfRange("Position.x > 0xFFFF")
            elif val < 0:
                raise game.errors.PositionNegative("Position.x is negative")
            
        elif name == 'y':
            if val > 0xFFFF:
                raise game.errors.PositionOutOfRange("Position.y > 0xFFFF")
            elif val < 0:
                raise game.errors.PositionNegative("Position.y is negative")
            
        elif name == 'z':
            if val > 0xFFFF:
                raise game.errors.PositionOutOfRange("Position.z > 0xFFFF")
            elif val < 0:
                raise game.errors.PositionNegative("Position.z is negative")
            
        object.__setattr__(self, name, val)"""

    # Support for the old behavior of list attributes.
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Position doesn't support being treated like a list with the key == %s" % key)
        
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
            
        raise IndexError("Position have no key == %s" % key)

    # Simplifiers
    def getTile(self):
        return getTile(self)
        
    def distanceTo(self, position):
        return abs(self.x-position.x)+abs(self.y-position.y)
    
    def roundPoint(self, steps):
        positions = []
        for x in xrange(-steps, steps+1):
            for y in xrange(-steps, steps+1):
                positions.append((x,y,self.z))
                
        return MultiPosition(self.instanceId, *positions)
        
    # For savings
    def __getstate__(self):
            return (self.x, self.y, self.z, self.instanceId)
            
    def __setstate__(self, data):
        self.x, self.y, self.z, self.instanceId = data

    def __str__(self):
        if not self.instanceId:
            return "[%d, %d, %d]" % (self.x, self.y, self.z)
        else:
            return "[%d, %d, %d - instance %d]" % (self.x, self.y, self.z, self.instanceId)

    def setStackpos(self, x):
        return StackPosition(self.x, self.y, self.z, x, self.instanceId)

class MultiPosition(Position):
    def __init__(self, instanceId=None, *argc):
        self.positions = argc
        self.index = 0
        self.instanceId = instanceId
    
    @property
    def x(self):
        return self.positions[self.index][0]
        
    @property
    def y(self):
        return self.positions[self.index][0]
        
    @property
    def z(self):
        return self.positions[self.index][0]
        
    def __iter__(self):
        return self
        
    def next(self):
        self.index += 1
        if self.index >= len(self.positions):
            raise StopIteration
        return self
        
class StackPosition(Position):
    __slots__ = ('stackpos',)
    
    def __init__(self, x, y, z=7, stackpos=None, instanceId=None):
        self.x = x
        self.y = y
        self.z = z
        self.stackpos = stackpos
        self.instanceId = instanceId

    # For savings
    def __getstate__(self):
        return (self.x, self.y, self.z, self.stackpos, self.instanceId)
            
    def __setstate__(self, data):
        self.x, self.y, self.z, self.stackpos, self.instanceId = data

    def __str__(self):
        if not self.instanceId:
            return "[%d, %d, %d - stack %d]" % (self.x, self.y, self.z, self.stackpos)
        else:
            return "[%d, %d, %d - instance %d, stack - %d]" % (self.x, self.y, self.z, self.instanceId, self.stackpos)

    def getThing(self):
        return self.getTile().getThing(self.stackpos)

    def setStackpos(self, x):
        self.stackpos = x
        
def getTile(pos):
    x,y,z,instanceId = pos.x, pos.y, pos.z, pos.instanceId
    iX = x / 32
    iY = y / 32
    pX = x -iX * 32
    pY = y -iY * 32

    try:
        area = knownMap[instanceId]
    except KeyError:
        knownMap[instanceId] = {}
        area = knownMap[instanceId]
        
    sectorSum = (iX * 32768) + iY
    try:
        return area[sectorSum][z][pX][pY]
    except KeyError:
        if loadTiles(x, y, instanceId):
            try:
                return area[sectorSum][z][pX][pY]
            except:
                return None
    except:
        return None
                
def getHouseId(pos):
    try:
        return getTile(pos).houseId
    except:
        return False
        
def placeCreature(creature, pos):
    try:
        return getTile(pos).placeCreature(creature)
    except:
        return False
        
def removeCreature(creature, pos):
    try:
        return getTile(pos).removeCreature(creature)
    except:
        return False  

DEFAULT_BASE = ''
def newInstance(base=None):
    instance = instanceId()
    if base:
        instances[instance] = base + '/'
    else:
        instances[instance] = DEFAULT_BASE
        
    return instance
        
PACK_ITEMS = 0 # top items
PACK_CREATURES = 8
PACK_FLAGS = 16

class Tile(object):
    __slots__ = ('things', 'countNflags')
    def __init__(self, items, flags=0, count=0):
        self.things = items
        
        if not count:
            self.countNflags = 1

            if len(items) > 1:
                for item in self.things:
                    if item.ontop:
                        self.countNflags += 1
  
        else:
            self.countNflags = count

        if flags:
            self._modpack(PACK_FLAGS, flags)

    def _depack(self, level):
        return (self.countNflags >> level) & 255
        
    def _modpack(self, level, mod):
        self.countNflags += mod << level

    def getCreatureCount(self):
        return self._depack(PACK_CREATURES)
    
    def getItemCount(self):
        return len(self.things) - self._depack(PACK_CREATURES)
        
    def getFlags(self):
        return self._depack(PACK_FLAGS)
        
    def setFlag(self, flag):
        if not self.getFlags() & flag:
            self._modpack(PACK_FLAGS, flag)

    def unsetFlag(self, flag):
        if self.getFlags() & flag:
            self._modpack(PACK_FLAGS, -flag)
            
    def placeCreature(self, creature):
        pos = self._depack(PACK_ITEMS) + self._depack(PACK_CREATURES)

        self.things.insert(pos, creature)
        self._modpack(PACK_CREATURES, 1)

        return pos
        
    def removeCreature(self,creature):
        self._modpack(PACK_CREATURES, -1)
        return self.things.remove(creature)
        
    def placeItem(self, item):
        if item.ontop:
            pos = self._depack(PACK_ITEMS)
            self._modpack(PACK_ITEMS, 1)
        else:
            pos = self._depack(PACK_ITEMS) + self._depack(PACK_CREATURES)
        self.things.insert(pos, item)
        return pos
    
    def placeItemEnd(self, item):
        self.things.append(item)
        return len(self.things)-1

    def ground(self):
        return self.things[0]
        
    def bottomItems(self):
        return self.things[self._depack(PACK_ITEMS) + self._depack(PACK_CREATURES):]
        
    def topItems(self):
        return self.things[:self._depack(PACK_ITEMS)]

    def getItems(self):
        items = self.topItems()[:]
        try:
            items.extend(self.bottomItems())
        except:
            pass
        
        return items
        
    def creatures(self):
        cc = self._depack(PACK_ITEMS)
        return self.things[cc:cc + self._depack(PACK_CREATURES)]
        
    def removeItem(self, item):
        item.stopDecay()
        
        if item.ontop:
            self._modpack(PACK_ITEMS, -1)
        return self.things.remove(item)

    def removeItemWithId(self, itemId):
        for i in self.getItems():
            if i.itemId == itemId:
                self.removeItem(i)
                
    # Fase those calls out
    def removeClientItem(self, cid, stackpos=None):
        if stackpos and self.things[stackpos].cid == cid:
            return self.things.pop(stackpos)
        else:
            for x in self.bottomItems():
                if x.cid == cid:
                    self.things.remove(x)
                    break
    """
    def removeClientCreature(self, stackpos=None):
        if stackpos and self.things[stackpos]:
            self.creatureCount -= 1 << 4
            return self.things.pop(stackpos)  
            
    def placeClientItem(self, cid):
        import game.item
        item = game.item.Item(game.item.sid(cid))
        return self.placeItem(item)"""
        
    def getThing(self, stackpos):
        try:
            return self.things[stackpos]
        except:
            return None
    
    def setThing(self, stackpos, item):
        self.things[stackpos] = item
        
    def findItem(self, sid):
        for x in self.bottomItems():
            if x.itemId == sid:
                return x

    def findStackpos(self, thing):
        return self.things.index(thing)
        
    def findClientItem(self, cid, stackpos=None):
        for x in self.bottomItems():
            if x.cid == cid:
                if stackpos:
                    return (self.things.index(x), x)
                return x
                
    def findCreatureStackpos(self, creature):
        return self.things.index(creature)

    def __getstate__(self):
        return (self.things, self.countNflags)
    
    def __setstate__(self, saved):
        self.things = saved[0]
        self.countNflags = saved[1]
        
#bindconstant.bind_all(Tile) # Apply constanting to Tile  

class HouseTile(Tile):
    __slots__ = ('houseId', 'position')
    def __getstate__(self):
        
        # Remove all non-loaded things for the sake of the cache. 
        items = []
        cf = self.getFlags()
        for i in self.things:
            if i.fromMap:
                items.append(i)
                if i.ontop:
                    cf += 1
        
        return (items, cf, self.houseId, self.position)
    
    def __setstate__(self, saved):
        self.things = saved[0]      
        self.countNflags = saved[1]  
        self.houseId = saved[2]
        self.position = saved[3]
        
        if self.houseId in houseTiles:
            houseTiles[self.houseId].append(self)
        else:
            houseTiles[self.houseId] = [self]
        
        check = True    
        for i in self.things:
            if "houseDoor" in i.actions:
                if check and self.houseId in houseDoors:
                    houseDoors[self.houseId].append(self.position)
                    check = False
                else:
                    houseDoors[self.houseId] = [self.position]

        try:
            for item in game.house.houseData[self.houseId].data["items"][self.position]:
                self.placeItem(item)
        except KeyError:
            pass
    
#bindconstant.bind_all(HouseTile) # Apply constanting to HouseTile 

import data.map.info as mapInfo
dummyItems = {} 

knownMap = {None: {}} # InstanceId -> {z: [x -> [y]]}

instances = {None: ''}

houseTiles = {}

houseDoors = {}

if config.stackTiles:
    dummyTiles = {}
    
def loadTiles(x,y, instanceId):
    if x < 0 or y < 0:
        return None
    elif x > mapInfo.height or y > mapInfo.width:
        return None
    
    return load(int(x / mapInfo.sectorSize[0]), int(y / mapInfo.sectorSize[1]), instanceId)

### Start New Map Format ###

attributeIds = ('actions', 'count', 'solid','blockprojectile','blockpath','usable','pickable','movable','stackable','ontop','hangable','rotatable','animation', 'doorId', 'depotId', 'text', 'written', 'writtenBy', 'description', 'teledest')

# Format (Work in Progress)
"""
    <uint8>floor_level
    floorLevel < 60
        <loop>32x32

        <uint16>itemId
        <uint8>attributeCount / other
        
        itemId >= 100:
            every attributeCount (
                See attribute format
            )

        itemId == 50:
            <int32> Tile flags
            
        itemId == 51:
            <uint32> houseId
            
        itemId == 0:
            skip attributeCount fields
            
        {
            ; -> go to next tile
            | -> skip the remaining y tiles
            ! -> skip the remaining x and y tiles
            , -> more items
        }
        
    floorLevel == 60:
        <uint16>center X
        <uint16>center Y
        <uint8>center Z
        <uint8> Radius from center creature might walk
        <uint8> count (
            <uint8> type (61 for Monster, 62 for NPC)
            <uint8> nameLength
            <string> Name
             
            <int8> X from center
            <int8> Y from center
                
            <uint16> spawntime in seconds
                       
            }
        )
    Attribute format:
    
    {
        <uint8>attributeId
        <char>attributeType
        {
            attributeType == i (
                <int32>value
            )
            attributeType == s (
                <uint16>valueLength
                <string with length valueLength>value
            )
            attributeType == b (
                <bool>value
            )
            attributeType == l (
                <uint8>listItems
                <repeat this block for listItems times> -> value
            )
        }
        
        
    }
"""

def loadSectorMap(code, instanceId, baseX, baseY):
    thisSectorMap = {}
    pos = 0
    codeLength = len(code)
    skip = False
    skip_remaining = False
    houseId = 0
    housePosition = None
    yRowGotItem = False
    
    # Avoid 1k calls to making the format :)
    # Pypy need a special treatment to avoid this.
    
    if sys.subversion[0] == 'PyPy':
        ll_unpack = struct.unpack
        l_unpack = lambda data: ll_unpack("<HB", data)
        long_unpack = lambda data: ll_unpack("<i", data)
        spawn_unpack = lambda data: ll_unpack("<HHBBB", data)
        creature_unpack  = lambda data: ll_unpack("<bbH", data)
    else:
        l_unpack = struct.Struct("<HB").unpack
        long_unpack = struct.Struct("<i").unpack
        creature_unpack = struct.Struct("<bbH").unpack
        spawn_unpack = struct.Struct("<HHBBB").unpack
    
    # Bind them locally, this is suppose to make a small speedup as well, local things can be more optimized :)
    # Pypy gain nothing, but CPython does.
    l_Item = game.item.Item
    l_Tile = Tile
    l_HouseTile = HouseTile
    
    # Also attempt to local the itemCache, pypy doesn't like this tho.
    l_itemCache = dummyItems
    l_attributes = attributeIds
    
    # Spawn commands
    l_getNPC = game.npc.getNPC
    l_getMonster = game.monster.getMonster
    
    # This is the Z loop (floor), we read the first byte
    while True:
        if pos >= codeLength:
           return thisSectorMap
           
        # First byte where we're at.
        level = ord(code[pos])
        pos += 1
        
        if level == 60:
            centerX, centerY, centerZ, centerRadius, creatureCount = spawn_unpack(code[pos:pos+7])
            
            pos += 7
                            
            # Mark a position
            centerPoint = Position(centerX, centerY, centerZ, instanceId)
                            
            # Here we use attrNr as a count for 
            for numCreature in xrange(creatureCount):
                creatureType = ord(code[pos])
                nameLength = ord(code[pos+1])
                name = code[pos+2:pos+nameLength+2]
                pos += 2 + nameLength
                spawnX, spawnY, spawnTime = creature_unpack(code[pos:pos+4])
                pos += 4
                if creatureType == 61:
                    creature = l_getMonster(name)
                else:
                    creature = l_getNPC(name)
                if creature:
                    creature.spawn(Position(centerX+spawnX, centerY+spawnY, centerZ, instanceId), radius=centerRadius, spawnTime=spawnTime, radiusTo=centerPoint)
                else:
                    print "Spawning of %s '%s' failed, it doesn't exist!" % ("Monster" if creatureType == 61 else "NPC", name)
                                    
            continue
        
        # An x level list for this floor
        xlevel = []
        
        # Speedup call.
        l_xlevel_append = xlevel.append
        
        # Loop over the 32 x rows
        for xr in xrange(32):
            # The real X position
            xPosition = xr + baseX
            
            # An y level list
            ywork = []
            
            # Speed up call
            l_ywork_append = ywork.append
            
            # Since we need to deal with skips we need to deal with counts and not a static loop (pypy will have a problem unroll this hehe)
            yr = 0
            
            while yr < 32:
                # The real Y position
                yPosition = yr + baseY
                
                # The items array and the flags for the Tile.
                items = []
                flags = 0
                
                # Speed up call
                l_items_append = items.append
                
                # We have no limit on the amount of items that a Tile might have. Loop until we hit a end.
                while True:
                    # uint16 itemId / type
                    # uint16 attrNr / count
                    itemId, attrNr = l_unpack(code[pos:pos+3])

                    # Do we have a positive id? If not its a blank tile
                    if itemId:
                        # Tile flags
                        if itemId == 50:
                            pos += 2
                            # int32
                            flags = long_unpack(code[pos:pos+4])[0]
                            pos += 5
                        
                        # HouseId?
                        elif itemId == 51:
                            pos += 2
                            # int32
                            houseId = long_unpack(code[pos:pos+4])[0]
                            housePosition = (xPosition, yPosition, level)
                            pos += 5
                            
                        elif attrNr:
                            pos += 3
                            attr = {}
                            for n in xrange(attrNr):
                                name = l_attributes[ord(code[pos])]
                                    
                                opCode = code[pos+1]
                                pos += 2
                                
                                if opCode == "i":
                                    pos += 4
                                    value = long_unpack(code[pos-4:pos])[0]
                                elif opCode == "s":
                                    valueLength = long_unpack(code[pos:pos+4])[0]
                                    pos += valueLength + 4
                                    value = code[pos-valueLength:pos]
                                elif opCode == "b":
                                    pos += 1
                                    value = bool(ord(code[pos-1]))
                                elif opCode == "l":
                                    value = []
                                    length = ord(code[pos])

                                    pos += 1
                                    for i in xrange(length):
                                        opCode = code[pos]
                                        pos += 1
                                        if opCode == "i":
                                            pos += 4
                                            item = long_unpack(code[pos-4:pos])[0]
                                        elif opCode == "s":
                                            valueLength = long_unpack(code[pos:pos+4])[0]
                                            pos += valueLength + 4
                                            item = code[pos-valueLength:pos]
                                        elif opCode == "b":
                                            pos += 1
                                            item = bool(ord(code[pos-1]))
                                        value.append(item)
                                        
                                attr[name] = value
                                
                            pos += 1
                            item = l_Item(itemId, **attr)
                            item.fromMap = True
                            l_items_append(item)
                        else:
                            pos += 4
                            try:
                                l_items_append(l_itemCache[itemId])
                            except KeyError:
                                item = l_Item(itemId)
                                item.tileStacked = True
                                item.fromMap = True
                                l_itemCache[itemId] = item
                                l_items_append(item)

                    else:
                        pos += 4
                        if attrNr:
                            for x in xrange(attrNr):
                                l_ywork_append(None)
                            yr += attrNr -1
                        else:
                            l_ywork_append(None)
                        yRowGotItem = True
                        
                    
                        
                    v = code[pos-1]
                    if v == ';': break
                    elif v == '|':
                        skip = True
                        break
                    elif v == '!':
                        skip = True
                        skip_remaining = True
                        break
                    # otherwise it should be ",", we don't need to vertify this.
                if items:
                    if houseId:
                        tile = l_HouseTile(items, flags)
                        tile.houseId = houseId
                        tile.position = housePosition
                        
                        # Find and cache doors
                        for i in tile.getItems():
                            if "houseDoor" in i.actions:
                                try:
                                    houseDoors[houseId].append(housePosition)
                                    break
                                except:
                                    houseDoors[houseId] = [housePosition]
                                
                        
                        if houseId in houseTiles:
                            houseTiles[houseId].append(tile)
                        else:
                            houseTiles[houseId] = [tile]
                            
                        try:
                            for item in game.house.houseData[houseId].data["items"][housePosition]:
                                tile.placeItem(item)
                        except KeyError:
                            pass
    
                        houseId = 0
                        housePosition = None
                        l_ywork_append(tile)
                    else:
                        l_ywork_append(l_Tile(items, flags))
                elif not yRowGotItem:
                    l_ywork_append(None)
                    yRowGotItem = False
                yr += 1

                if skip:
                    skip = False
                    break                
            l_xlevel_append(ywork)
            if skip_remaining:
                skip_remaining = False
                break
                
        thisSectorMap[level] = xlevel
           
### End New Map Format ###
def load(sectorX, sectorY, instanceId):
    sectorSum = (sectorX * 32768) + sectorY
    
    if sectorSum in knownMap[instanceId]:
        return False
          
    print "Loading %d.%d.sec" % (sectorX, sectorY)
    t = time.time()
    
    # Attempt to load a sector file
    try:
        with io.open("data/map/%s%d.%d.sec" % (instances[instanceId], sectorX, sectorY), "rb") as f:
            knownMap[instanceId][sectorSum] = loadSectorMap(f.read(), instanceId, sectorX * 32, sectorY * 32)
    except IOError:
        # No? Mark it as empty
        knownMap[instanceId][sectorSum] = None
        return False
        
    print "Loading of %d.%d.sec took: %f" % (sectorX, sectorY, time.time() - t)    
    
    if config.performSectorUnload:
        reactor.callLater(config.performSectorUnloadEvery, reactor.callInThread, _unloadMap, sectorX, sectorY, instanceId)
    
    scriptsystem.get('postLoadSector').runSync("%d.%d" % (sectorX, sectorY), None, None, sector=knownMap[instanceId][sectorSum], instanceId=instanceId)
    
    return True

# Map cleaner
def _unloadCheck(sectorX, sectorY, instanceId):
    # Calculate the x->x and y->y ranges
    # We're using a little higher values here to avoid reloading again 
    
    xMin = (sectorX * mapInfo.sectorSize[0]) + 14
    xMax = (xMin + mapInfo.sectorSize[0]) + 14
    yMin = (sectorY * mapInfo.sectorSize[1]) + 11
    yMax = (yMin + mapInfo.sectorSize[1]) + 11
    try:
        for player in game.player.allPlayers.viewvalues():
            pos = player.position # Pre get this one for sake of speed, saves us a total of 4 operations per player
            
            # Two cases have to match, the player got to be within the field, or be able to see either end (x or y)
            if instanceId == pos.instanceId and (pos[0] < xMax or pos[0] > xMin) and (pos[1] < yMax or pos[1] > yMin):
                return False # He can see us, cancel the unloading
    except:
        return False # Players was changed.
        
    return True
    
def _unloadMap(sectorX, sectorY, instanceId):
    print "Checking %d.%d.sec (instanceId %s)" % (sectorX, sectorY, instanceId)
    t = time.time()
    if _unloadCheck(sectorX, sectorY, instanceId):
        print "Unloading...."
        unload(sectorX, sectorY)
        print "Unloading took: %f" % (time.time() - t)   
        
def unload(sectorX, sectorY, instanceId):
    sectorSum = (sectorX * 32768) + sectorY
    try:
        del knownMap[instanceId][sectorSum]
    except:
        pass