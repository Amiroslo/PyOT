from core.game.game import getSpectators
from core.packet import TibiaPacket
from core.game.map import placeCreature, removeCreature
class Creature:
    idsTaken = 0
    def __init__(self, data, position, cid=None):
        self.data = data
        self.creatureType = 0
        self.direction = 0
        self.position = position
        self.stackpos = 1
        self.speed = 0x0032
        self.scripts = {}
        self.cid = cid if cid else self.generateClientID()
        
    def name(self):
        return self.data["name"]

    def clientId(self):
        return self.cid

    def generateClientID(self):
        self.idsTaken = self.idsTaken + 1
        return 0x10000001 + self.idsTaken
        
    def stepDuration(self, tile):
        return (1000 * tile.speed / self.speed) * 1 # TODO

    def move(self, direction):
        import data.map.info
        self.direction = direction
        
        # Make packet
        stream = TibiaPacket(0x6D)
        stream.position(self.position)
        stream.uint8(self.stackpos)
        
        removeCreature(self, self.position)
        
        # Recalculate position
        position = self.position[:] # Important not to remove the : here, we don't want a reference!
        if direction is 0:
            position[1] = self.position[1] - 1
        elif direction is 1:
            position[0] = self.position[0] + 1
        elif direction is 2:
            position[1] = self.position[1] + 1
        else:
            position[0] = self.position[0] - 1
          
        # We don't walk out of the map!
        if position[0] < 1 or position[1] < 1 or position[0] > data.map.info.width or position[1] > data.map.info.height:
           return False
          
          
        stream.position(position)
        placeCreature(self, position)
        
        self.position = position
        # Send to everyone
        stream.sendto(getSpectators(position))
        
        
        
        return True # Required for auto walkings
class Monster(Creature):
    def __init__(self, position, cid=None):
        Creature.__init__(self, data, position, cid)
        self.creatureType = 1