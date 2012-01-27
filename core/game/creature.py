from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.internet import reactor
from game.engine import getSpectators, getPlayers
from game.map import placeCreature, removeCreature, getTile, Position, StackPosition
from twisted.python import log
import threading
import game.enum as enum
import config
import time
import copy
import game.scriptsystem
import inspect
import game.errors
import math
import collections

# Unique ids, thread safe too
def __uid():
    idsTaken = 1000
    while True:
        idsTaken += 1
        yield idsTaken
        
__uniqueId = __uid().next
__uniqueLock = threading.Lock()
def uniqueId():
    __uniqueLock.acquire()
    id = __uniqueId()
    __uniqueLock.release()
    return id

allCreatures = {}
#allCreaturesObject = allCreatures.viewvalues()

class CreatureBase(object):
    def __init__(self):
        self.scripts = {"onFollow":[], "onTargetLost":[]}
        
    def regOnFollow(self, function):
        self.scripts["onFollow"].append(function)
        
    def unregOnFollow(self, function):
        self.scripts["onFollow"].remove(function)
        
    def onFollow(self, target):
        for func in self.scripts["onFollow"]:
            game.scriptsystem.scriptPool.callInThread(func, self, target)

    def regOnTargetLost(self, function):
        self.scripts["onTargetLost"].append(function)

    def unregOnTargetLost(self, function):
        self.scripts["onTargetLost"].remove(function)
        
    def onTargetLost(self, target):
        for func in self.scripts["onTargetLost"]:
            game.scriptsystem.scriptPool.callInThread(func, self, target)
            
class Creature(object):
    
    def __init__(self, data, position, cid=None):
        self.data = data
        self.creatureType = 0
        self.direction = 0
        self.position = position
        self.speed = 100.0
        self.scripts = { "onNextStep":[]}
        self.cid = cid if cid else self.generateClientID()
        self.outfit = [self.data["looktype"], self.data["lookhead"], self.data["lookbody"], self.data["looklegs"], self.data["lookfeet"]]
        self.mount = 0
        self.mounted = 0
        self.addon = self.data["lookaddons"]
        self.action = None
        self.lastAction = 0
        self.extAction = 0
        self.lastStep = 0
        self.target = None # target for follow/attacks
        self.targetMode = 0 # 0 = no particular reason, 1 = attack, 2 = follow
        self.vars = {}
        self.cooldowns = {} # This is a int32, icon are the first 8, then group is the next 7
        self.regenerate = None
        self.alive = True
        self.lastDamager = None
        self.solid = not config.creatureWalkthrough
        self.shield = 0
        self.emblem = 0
        self.skull = 0
        self.knownBy = set()
        self.conditions = {}
        self.walkPattern = None
        self.activeSummons = []
        
        # Options
        self.canMove = True
        
        # We are trackable 
        allCreatures[self.cid] = self

    def actionLock(self, *argc, **kwargs):
        _time = time.time()
        if self.lastAction >= _time:
            if "stopIfLock" in kwargs and kwargs["stopIfLock"]:
                return False
            reactor.callLater(self.lastAction - _time, *argc, **kwargs)
            return False
        else:
            self.lastAction = _time
            return True

    def extActionLock(self, *argc, **kwargs):
        _time = time.time()
        if self.extAction >= _time:
            reactor.callLater(self.extAction - _time, *argc, **kwargs)
            return False
        else:
            return True
            
    @staticmethod
    def actionDecor(f):
        """ Decorator used by external actions """
        def new_f(creature, *argc, **kwargs):
            if not creature.alive or not creature.actionLock(new_f, creature, *argc, **kwargs) or not creature.extActionLock(new_f, creature, *argc, **kwargs) :
                return
            else:
                _time = time.time()
                creature.extAction = _time
                creature.lastAction = _time
                f(creature, *argc, **kwargs)

        return new_f

    def isPlayer(self):
        return False

    def isNPC(self):
        return False
        
    def isMonster(self):
        return False

    def isItem(self):
        return False
        
    def isPushable(self, by):
        return False
    
    def isAttackable(self, by):
        return False

    def isSummon(self):
        return False
            
    def isSummonFor(self, creature):
        return False
        
    def name(self):
        return self.data["name"]

    def description(self):
        return "You see a creature."
        
    def clientId(self):
        return self.cid

    def thingId(self):
        return self.creatureType # Used to indentify my "thing"
    
    def actionIds(self):
        return ('creature',) # Static actionID

    def generateClientID(self):
        raise NotImplementedError("This function must be overrided by a secondary level class!")
        
    def stepDuration(self, ground, delay=1.5):
        #if time.time() - self.lastStep < delay:
        if True:
            if not ground.speed:
                ground.speed = 100
                
            postValue = (config.drawingSpeed - 75) / 1000.0
            return (ground.speed / self.speed) + postValue
        #return delay

    def notPossible(self):
        # Needs to be overrided in player
        # Here we can inform a script if a illigal event
        # Right now, don't care
        return

    def refreshStatus(self, streamX=None): pass
    def refreshSkills(self, streamX=None): pass
    def refreshConditions(self, streamX=None): pass
    
    def despawn(self):
        self.alive = False
        try:
            tile = game.map.getTile(self.position)
            stackpos = tile.findCreatureStackpos(self)
            tile.removeCreature(self)
            
            for spectator in getSpectators(self.position):
                stream = spectator.packet()
                stream.removeTileItem(self.position, stackpos)
                stream.send(spectator)
        except:
            pass
        try:
            if self.respawn:
                if self.spawnTime:
                    reactor.callLater(self.spawnTime, self.base.spawn, self.spawnPosition)
                elif self.spawnTime == 0:
                    return
                    
                else:
                    reactor.callLater(self.base.spawnTime, self.base.spawn, self.spawnPosition)
        except:
            pass
        
    def move(self, direction, spectators=None, level=0, stopIfLock=False):
        # Client will shift us to this position so.
        self.direction = direction % 4
        
        if self.canMove:
            return self._move(direction, spectators, level, stopIfLock)
            
        if self.isPlayer():
            self.cancelWalk()
        
    @inlineCallbacks
    def _move(self, direction, spectators=None, level=0, stopIfLock=False):
        if not self.alive or not level and not self.actionLock(self._move, direction, spectators, level, stopIfLock):
            return
            
        if not self.data["health"] or not self.canMove:
            return
            
        import data.map.info
        
        
        oldPosition = self.position.copy()
        
        # Recalculate position
        position = oldPosition.copy()
        if direction == 0:
            position.y -= 1
        elif direction == 1:
            position.x += 1
        elif direction == 2:
            position.y += 1
        elif direction == 3:
            position.x -= 1
        elif direction == 4:
            position.y += 1
            position.x -= 1
        elif direction == 5:
            position.y += 1
            position.x += 1
        elif direction == 6:
            position.y -= 1
            position.x -= 1
        elif direction == 7:
            position.y -= 1
            position.x += 1

        position.z += level

        # We don't walk out of the map!
        if position.x < 1 or position.y < 1 or position.x > data.map.info.width or position.y > data.map.info.height:
            self.cancelWalk()
            return
                    
        # New Tile
        newTile = getTile(position)
        oldTile = getTile(oldPosition)

        if not newTile:
            self.walkPattern = [] # If we got a queue of moves, we need to end it!
            returnValue(False)
            
        if not oldTile:
            # This always raise
            raise Exception("(old)Tile not found (%s). This shouldn't happend!" % oldPosition)
        
        
        val = yield game.scriptsystem.get("move").runDefer(self)
        if val == False:
            self.walkPattern = [] # If we got a queue of moves, we need to end it!
            returnValue(False)
            return
            
        try:
            oldStackpos = oldTile.findCreatureStackpos(self)
        except:
            self.cancelWalk()
            return

        # Deal with walkOff
        for item in oldTile.getItems():
            game.scriptsystem.get('walkOff').runSync(item, self, None, position=oldPosition)

        # Deal with preWalkOn
        for item in newTile.getItems():
            r = game.scriptsystem.get('preWalkOn').runSync(item, self, None, oldTile=oldTile, newTile=newTile, position=position)
            if r == False:
                self.walkPattern = [] # If we got a queue of moves, we need to end it!
                returnValue(False)
                return
                
        for thing in newTile.things:
            if thing.solid:
                if level and isinstance(thing, Creature):
                    continue
                
                #self.turn(direction) # Fix me?
                self.notPossible()
                self.walkPattern = [] # If we got a queue of moves, we need to end it!
                returnValue(False)
                return

        _time = time.time()
        self.lastStep = _time
        delay = self.stepDuration(newTile.getThing(0)) * (config.diagonalWalkCost if direction > 3 else 1)
        self.lastAction += delay
        self.extAction = _time + (delay/2)
                
        newStackPos = newTile.placeCreature(self)
            
        oldTile.removeCreature(self)
        
        self.position = position
        self.direction = direction % 4
        
        # Mark for save
        if self.isPlayer():
            self.saveData = True
            
        # Send to everyone   
        if not spectators:
            spectators = getPlayers(position, (11, 9))
            
        for spectator in spectators:
            # Make packet
            if not spectator.client:
                continue

            canSeeNew = spectator.canSee(position)
            canSeeOld = spectator.canSee(oldPosition)
            isKnown = self in spectator.knownCreatures
            
            if spectator == self:
                if (oldPosition.z != 7 or position.z < 8) and oldStackpos < 10: # Only as long as it's not 7->8 or 8->7
                    stream = spectator.packet(0x6D)
                    stream.position(oldPosition)
                    stream.uint8(oldStackpos)
                    stream.position(position)   
                else:
                    stream = spectator.packet()
                    stream.removeTileItem(oldPosition, oldStackpos)
                # Levels
                if oldPosition.z > position.z:
                    stream.moveUpPlayer(self, oldPosition)
                        
                elif oldPosition.z < position.z:
                    stream.moveDownPlayer(self, oldPosition)

                # Y movements
                if oldPosition.y > position.y:
                    stream.uint8(0x65)
                    stream.mapDescription(Position(oldPosition.x - 8, self.position.y - 6, self.position.z), 18, 1, self)
                elif oldPosition.y < position.y:
                    stream.uint8(0x67)
                    stream.mapDescription(Position(oldPosition.x - 8, self.position.y + 7, self.position.z), 18, 1, self)
                
                # X movements
                if oldPosition.x < position.x:
                    stream.uint8(0x66)
                    stream.mapDescription(Position(self.position.x + 9, self.position.y - 6, self.position.z), 1, 14, self)
                elif oldPosition.x > position.x:
                    stream.uint8(0x68)
                    stream.mapDescription(Position(self.position.x - 8, self.position.y - 6, self.position.z), 1, 14, self)

                    
                    
            elif (not canSeeOld or not isKnown) and canSeeNew:
                stream = spectator.packet()
                # Too high stack?
                if newStackPos < 10:
                    stream.addTileCreature(position, newStackPos, self, spectator) # This automaticly deals with known list so
                    
            elif canSeeOld and (not canSeeNew or newStackPos >= 10):
                if isKnown:
                    stream = spectator.packet()
                    stream.removeTileItem(oldPosition, oldStackpos)
                    spectator.knownCreatures.remove(self)
                
            elif not canSeeOld and not canSeeNew:
                continue
            elif oldStackpos < 10:
                if not isKnown:
                    raise("Shouldn't happend!")
                    
                if oldPosition.z != 7 or position.z < 8 and newStackPos < 10: # Only as long as it's not 7->8 or 8->7
                    stream = spectator.packet(0x6D)
                    stream.position(oldPosition)
                    stream.uint8(oldStackpos)
                    stream.position(position)  
                    
                else:
                    stream = spectator.packet()
                    stream.removeTileItem(oldPosition, oldStackpos)
                    
            else:
                raise Exception("Shouldn't happend!")
            stream.send(spectator.client) 

        if self.scripts["onNextStep"]:
            scripts = self.scripts["onNextStep"][:]
            self.scripts["onNextStep"] = []
            for script in scripts:
                script(self)
            
        # Deal with walkOn
        for item in newTile.getItems(): # Scripts
            game.scriptsystem.get('walkOn').runSync(item, self, None, position=position, fromPosition=oldPosition)
            if item.teledest:
                try:
                    self.teleport(Position(item.teledest[0], item.teledest[1], item.teledest[2], self.position.instanceId))
                except:
                    log.msg("%d (%s) got a invalid teledist (%s), remove it!" % (item.itemId, item, item.teledest))
                    del item.teledest

            
        # Deal with appear and disappear. Ahh the power of sets :)
        if self.isPlayer():
            ignore = (self,)
        else:
            ignore = ()
        oldPosCreatures = game.engine.getPlayers(oldPosition, ignore=ignore)
        newPosCreatures = game.engine.getPlayers(position, ignore=ignore)
        disappearFrom = oldPosCreatures - newPosCreatures
        appearTo = newPosCreatures - oldPosCreatures
        for creature2 in disappearFrom:
            game.scriptsystem.get('disappear').runSync(creature2, self)
            game.scriptsystem.get('disappear').runSync(self, creature2)
            
        for creature2 in appearTo:
            game.scriptsystem.get('appear').runSync(creature2, self)
            game.scriptsystem.get('appear').runSync(self, creature2)
        
        returnValue(True)
    def magicEffect(self, type, pos=None):
        if not type: return
        
        if not pos or pos[0] == 0xFFFF:
            pos = self.position
        for spectator in getSpectators(pos):
            stream = spectator.packet()
            stream.magicEffect(pos, type)
            stream.send(spectator)
        
    def shoot(self, fromPos, toPos, type):
        if not type: return
        
        if fromPos == toPos:
            self.magicEffect(type, fromPos)
        else:
            for spectator in getSpectators(fromPos) | getSpectators(toPos):
                stream = spectator.packet()
                stream.shoot(fromPos, toPos, type)
                stream.send(spectator)

    def refreshOutfit(self):
        for spectator in game.engine.getSpectators(self.position):
            stream = spectator.packet(0x8E)
            stream.uint32(self.clientId())
            stream.outfit(self.outfit, self.addon, self.mount if self.mounted else 0x00)
            stream.send(spectator)

    def changeMountStatus(self, mounted):
        mount = game.resource.getMount(self.mount)
        if mount:
            self.mounted = mounted
        
            if mount.speed:
                self.setSpeed((self.speed + mount.speed) if mounted else (self.speed - mount.speed))
            self.refreshOutfit()
    
    def setOutfit(self, looktype, lookhead=0, lookbody=0, looklegs=0, lookfeet=0, addon=0):
        self.outfit = [looktype, lookhead, lookbody, looklegs, lookfeet]
        self.addon = addon
        self.refreshOutfit()

    def setSpeed(self, speed):
        if speed != self.speed:
            if speed > 1500:
                speed = 1500.0
            self.speed = float(speed)
            for spectator in getSpectators(self.position):
                stream = spectator.packet(0x8F)
                stream.uint32(self.clientId())
                stream.uint16(self.speed)
                stream.send(spectator)
            
    def onDeath(self):
        #del allCreatures[self.clientId()]
        pass # To be overrided in monster and player

    def remove(self, entriesToo=True):
        """ Remove this creature from the map, stop the brain and so on """
        
        # All remove creatures are dead. No matter if they actually are alive.
        self.alive = False
        
        tile = self.position.getTile()
        try:
            tile.removeCreature(self)
        except:
            pass

        if self.isPlayer():
            ignore = (self,)
        else:
            ignore = ()
            
        for spectator in game.engine.getSpectators(self.position, ignore=ignore):
            stream = spectator.packet(0x69)
            stream.position(self.position)
            stream.tileDescription(tile, spectator.player)
            stream.uint8(0x00)
            stream.uint8(0xFF)
            stream.send(spectator)
        
        # Don't call this on a player
        if entriesToo:
            if self.isPlayer():
                raise Exception("Creature.remove(True) (entriesToo = True) has been called on a player. This is (unfortunatly), not supported (yet?)")
            
            try:
                del allCreatures[self.clientId()]
            except:
                pass
            
    def rename(self, name):
        newSpectators = game.engine.getPlayers(self.position)
        stackpos = game.map.getTile(self.position).findCreatureStackpos(self)
        
        self.data["name"] = name
        for player in self.knownBy:
            stream = player.packet()
            stream.removeTileItem(self.position, stackpos)
            if player in newSpectators:
                stream.addTileCreature(self.position, stackpos, self, player, True)

            stream.send(player.client)

    def privRename(self, player, name):
        if player in self.knownBy:
            stackpos = game.map.getTile(self.position).findCreatureStackpos(self)
            stream = player.packet()
            stream.removeTileItem(self.position, stackpos)
            originalName = self.data["name"]
            
            def doRename():
                self.data["name"] = name
                stream.addTileCreature(self.position, stackpos, self, player, True)
                self.data["name"] = originalName
                stream.send(player.client)     
                
            reactor.callFromThread(doRename) # For thread safety

            
    def hitEffects(self):
        if self.isPlayer() or self.base.blood == game.enum.FLUID_BLOOD:
            return game.enum.COLOR_RED, game.enum.EFFECT_DRAWBLOOD
        elif self.base.blood == game.enum.FLUID_SLIME:
            return game.enum.COLOR_LIGHTGREEN, game.enum.EFFECT_POISON
        elif self.base.blood == game.enum.FLUID_ENERGY:
            return game.enum.COLOR_PURPLE, game.enum.EFFECT_PURPLEENERGY
        elif self.base.blood == game.enum.FLUID_UNDEAD:
            return game.enum.COLOR_GREY, game.enum.EFFECT_HITAREA
        elif self.base.blood == game.enum.FLUID_FIRE:
            return game.enum.COLOR_ORANGE, game.enum.EFFECT_DRAWBLOOD
        
    def damageToBlock(self, dmg, type):
        # Overrided to creatures.
        return dmg
        
    def onHit(self, by, dmg, type, effect=None):
        if not self.alive:
            print "[DEBUG]: A dead creature seem to have been hit"
            return
            
        self.lastDamager = by
          
        if not type == game.enum.DISTANCE:
            dmg = min(self.damageToBlock(dmg, type), 0) # Armor calculations(shielding+armor)
            dmg = max(-self.data["health"], dmg) #wrap this one too?


        if type == game.enum.ICE:
            textColor = game.enum.COLOR_TEAL
            magicEffect = game.enum.EFFECT_ICEATTACK
            
        elif type == game.enum.FIRE:
            textColor = game.enum.COLOR_ORANGE
            magicEffect = game.enum.EFFECT_HITBYFIRE

        elif type == game.enum.EARTH:
            textColor = game.enum.COLOR_LIGHTGREEN
            magicEffect = game.enum.EFFECT_HITBYPOSION
           
        elif type == game.enum.ENERGY:
            textColor = game.enum.COLOR_PURPLE
            magicEffect = game.enum.EFFECT_ENERGYHIT
            
        elif type == game.enum.HOLY:
            textColor = game.enum.COLOR_YELLOW
            magicEffect = game.enum.EFFECT_HOLYDAMAGE
            
        elif type == game.enum.DEATH:
            textColor = game.enum.COLOR_DARKRED
            magicEffect = game.enum.EFFECT_SMALLCLOUDS
            
        elif type == game.enum.DROWN:
            textColor = game.enum.COLOR_LIGHTBLUE
            magicEffect = game.enum.EFFECT_ICEATTACK
			
        elif type == game.enum.DISTANCE:
            textColor, magicEffect = game.enum.COLOR_RED, None
            dmg = min(self.damageToBlock(dmg, type), 0) # Armor calculations(armor only. for now its the same function)
            dmg = max(-self.data["health"], dmg) #wrap this one too?
        elif type == game.enum.LIFEDRAIN:
            textColor = game.enum.COLOR_TEAL
            magicEffect = game.enum.EFFECT_ICEATTACK
            
        else: ### type == game.enum.MELEE:
            textColor, magicEffect = self.hitEffects()           
        if effect:
            magicEffect = effect
            
        dmg = [dmg]
        textColor = [textColor]
        magicEffect = [magicEffect]
        type = [type]
        
        process = game.scriptsystem.get("hit").runSync(self, self.lastDamager, damage=dmg, type=type, textColor=textColor, magicEffect=magicEffect)
        if process == False:
            return
            
        dmg = dmg[0]
        textColor = textColor[0]
        magicEffect = magicEffect[0]
        type = type[0]
        
        if magicEffect:
            self.magicEffect(magicEffect)
            
        if dmg:
            tile = game.map.getTile(self.position)
            for item in tile.getItems():
                if item.itemId in SMALLSPLASHES or item.itemId in FULLSPLASHES:
                    tile.removeItem(item)
                            
            splash = game.item.Item(game.enum.SMALLSPLASH)
                
            if self.isPlayer():
                splash.fluidSource = game.enum.FLUID_BLOOD
            else:
                splash.fluidSource = self.base.blood
            if splash.fluidSource in (game.enum.FLUID_BLOOD, game.enum.FLUID_SLIME):
                tile.placeItem(splash)
                
                # Start decay
                splash.decay(self.position)
                
            updateTile(self.position, tile)
        
        if by and by.isPlayer():
            by.message("%s loses %d hitpoint%s due to your attack." % (self.name().capitalize(), -1 * dmg, 's' if dmg < -1 else ''), 'MSG_DAMAGE_DEALT', value = -1 * dmg, color = textColor, pos=self.position)

        if self.isPlayer():
            if by:
                self.message("You lose %d hitpoint%s due to an attack by %s." % (-1 * dmg, 's' if dmg < -1 else '', by.name().capitalize()), 'MSG_DAMAGE_RECEIVED', value = -1 * dmg, color = textColor, pos=self.position)
            else:
                self.message("You lose %d hitpoint%s." % (-1 * dmg, 's' if dmg < -1 else ''), 'MSG_DAMAGE_RECEIVED', value = -1 * dmg, color = textColor, pos=self.position)

        elif not self.target and self.data["health"] < 1:
            self.follow(by) # If I'm a creature, set my target
        
        # Modify health
        if dmg:
            self.modifyHealth(dmg)
        
            if by and self.data["health"] < 1:
                by.target = None
                by.targetMode = 0
                if by.isPlayer():
                    by.cancelTarget()
        
            return True
        else:
            return False
            
    def onSpawn(self):
        pass # To be overrided
        
    def setHealth(self, health):
        if self.data["health"] == 0 and health:
            self.alive = True
            
        self.data["health"] = max(0, health)
        
        for spectator in getSpectators(self.position):
            stream = spectator.packet(0x8C)
            stream.uint32(self.clientId())
            stream.uint8(int(self.data["health"] * 100 / self.data["healthmax"]))
            stream.send(spectator)
         
        self.refreshStatus()
        
        if self.data["health"] == 0:
            self.alive = False
            self.onDeath()
            return False
            
        return True
           

    def modifyHealth(self, health, spawn=False):
        return self.setHealth(min(self.data["health"] + health, self.data["healthmax"]))
        
    def teleport(self, position):
        """if not self.actionLock(self.teleport, position):
            return False"""
            
        # 4 steps, remove item (creature), send new map and cords, and effects
        oldPosition = self.position.copy()
        
        newTile = getTile(position)
        oldPosCreatures = set()
        if not newTile:
            raise game.errors.SolidTile()
        for i in newTile.getItems():
            if newTile.things[0].solid:
                raise game.errors.SolidTile()

        try:
            oldStackpos = getTile(oldPosition).findCreatureStackpos(self)
            for spectator in getSpectators(oldPosition, ignore=(self,)):
                stream = spectator.packet()
                stream.removeTileItem(oldPosition, oldStackpos)
                stream.magicEffect(oldPosition, 0x02)
                stream.send(spectator)
            oldPosCreatures = game.engine.getCreatures(oldPosition)
        except:
            pass # Just append creature
        
        stackpos = placeCreature(self, position)
        if not stackpos:
            raise game.errors.ImpossibleMove()
        
        removeCreature(self, oldPosition)
        self.position = position
        if self.creatureType == 0 and self.client:
            stream = self.packet()
            try:
                stream.removeTileItem(oldPosition, oldStackpos)
            except:
                pass # Just append
            stream.uint8(0x64)
            stream.position(position)
            stream.mapDescription(Position(position.x - 8, position.y - 6, position.z), 18, 14, self)
            #stream.magicEffect(position, 0x02)
            stream.send(self.client)
        
        newPosCreatures = game.engine.getCreatures(position)
        disappearFrom = oldPosCreatures - newPosCreatures
        appearTo = newPosCreatures - oldPosCreatures
        for creature2 in disappearFrom:
            game.scriptsystem.get('disappear').runSync(creature2, self)

        for creature2 in appearTo:
            game.scriptsystem.get('appear').runSync(creature2, self)    
         
        
        for spectator in getSpectators(position, ignore=(self,)):
            stream = spectator.packet()
            stream.addTileCreature(position, stackpos, self, spectator.player)
            stream.magicEffect(position, 0x02)
            stream.send(spectator)
                
    def turn(self, direction):
        assert direction < 4
        if self.direction == direction:
            return
            
        if not self.alive or not self.actionLock(self.turn, direction):
            return

        self.direction = direction
        self.extAction = time.time() + 0.15
        
        # Make package
        for spectator in getSpectators(self.position):
            stream = spectator.packet(0x6B)
            stream.position(self.position)
            stream.uint8(getTile(self.position).findCreatureStackpos(self))
            stream.uint16(0x63)
            stream.uint32(self.clientId())
            stream.uint8(direction)
            stream.send(spectator)
        
    def turnAgainst(self, position):
        # First north/south
        if position.y > self.position.y:
            return self.turn(2)
        elif position.y < self.position.y:
            return self.turn(0)
        elif position.x > self.position.x:
            return self.turn(1)
        elif position.x < self.position.x:
            return self.turn(3)
            
    def say(self, message, messageType='MSG_SPEAK_SAY'):
        for spectator in getSpectators(self.position, config.sayRange):
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.enum(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(spectator)

    def yell(self, message, messageType='MSG_SPEAK_YELL'):
        for spectator in getSpectators(self.position, config.yellRange):
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.enum(messageType))
            stream.position(self.position)
            stream.string(message.upper())
            stream.send(spectator)

    def whisper(self, message, messageType='MSG_SPEAK_WHISPER'):
        group = getSpectators(self.position, config.whisperRange)
        listeners = getSpectators(self.position, config.sayRange) - group
        
        for spectator in group:
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.enum(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(spectator)

        for spectator in listeners:
            stream = spectator.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.enum(messageType))
            stream.position(self.position)
            stream.string(config.whisperNoise)
            stream.send(spectator)
            
    def broadcast(self, message, messageType='MSG_GAMEMASTER_BROADCAST'):
        import game.players
        for player in game.player.allPlayers.values():
            stream = player.packet(0xAA)
            stream.uint32(0)
            stream.string(self.data["name"])
            stream.uint16(self.data["level"] if "level" in self.data else 0)
            stream.uint8(stream.enum(messageType))
            stream.position(self.position)
            stream.string(message)
            stream.send(player.client)
            
    def sayPrivate(self, message, to, messageType=enum.MSG_PRIVATE_FROM):
        if not to.isPlayer(): return
        
        stream = to.packet(0xAA)
        stream.uint32(0)
        stream.string(self.data["name"])
        stream.uint16(self.data["level"] if "level" in self.data else 0)
        stream.uint8(messageType)
        stream.position(self.position)
        stream.string(message)
        stream.send(to.client)    
        
    def stopAction(self):
        ret = False
        try:
            self.action.cancel()
            ret = True
        except:
            pass
        self.action = None
        return ret
        
    def cancelWalk(self, d=None):
        return # Is only executed on players
        
    def canSee(self, position, radius=(8,6)):
        # We are on ground level and we can't see underground
        # We're on a diffrent instanceLevel
        # Or We are undergorund and we may only see 2 floors
        if (self.position.instanceId != position.instanceId) or (self.position.z <= 7 and position.z > 7) or (self.position.z >= 8 and abs(self.position.z-position.z) > 2): 
            return False
        
        offsetz = self.position.z-position.z
        if (position.x >= self.position.x - radius[0] + offsetz) and (position.x <= self.position.x + radius[0]+1 + offsetz) and (position.y >= self.position.y - radius[1] + offsetz) and (position.y <= self.position.y + radius[1]+1 + offsetz):
            return True
        return False

    def canTarget(self, position, radius=(8,6), allowGroundChange=False):
        if self.position.instanceId != position.instanceId:
            return False
            
        if allowGroundChange and self.position.z != position.z: # We are on ground level and we can't see underground
            return False
        
        if (position.x >= self.position.x - radius[0]) and (position.x <= self.position.x + radius[0]+1) and (position.y >= self.position.y - radius[1]) and (position.y <= self.position.y + radius[1]+1):
            return True
        return False
        
    def distanceStepsTo(self, position):
        return abs(self.position.x-position.x)+abs(self.position.y-position.y)
        
    def inRange(self, position, x, y, z=0):
        return ( position.instanceId == self.position.instanceId and abs(self.position.x-position.x) <= x and abs(self.position.y-position.y) <= y and abs(self.position.z-position.z) <= y )   
    
    def positionInDirection(self, direction):
        position = self.position.copy()
        if direction == 0:
            position.y -= 1
        elif direction == 1:
            position.x += 1
        elif direction == 2:
            position.y += 1
        elif direction == 3:
            position.x -= 1
        elif direction == 4:
            position.y += 1
            position.x -= 1
        elif direction == 5:
            position.y += 1
            position.x += 1
        elif direction == 6:
            position.y -= 1
            position.x -= 1
        elif direction == 7:
            position.y -= 1
            position.x += 1
        return position

    # Personal vars
    def setVar(self, name, value=None):
        try:
            if value == None:
                del self.vars[inspect.stack()[0][1] + name]
            else:
                self.vars[inspect.stack()[0][1] + name] = value
        except:
            return None
            
    def getVar(self, name):
        try:
            return self.vars[inspect.stack()[0][1] + name]
        except:
            return None

    # Global storage
    def setGlobal(self, field, value):
        try:
            game.engine.globalStorage['storage'][field] = value
            game.engine.saveGlobalStorage = True
        except:
            return False
    
    def getGlobal(self, field, default=None):
        try:
            return game.engine.globalStorage['storage'][field]
        except:
            return default
            
    def removeGlobal(self, field):
        try:
            del game.engine.globalStorage['storage'][field]
            game.engine.saveGlobalStorage = True
        except:
            pass

    # Global object storage
    def setGlobalObject(self, field, value):
        try:
            game.engine.globalStorage['objectStorage'][field] = value
            game.engine.saveGlobalStorage = True
        except:
            return False
    
    def getGlobalObject(self, field, default=None):
        try:
            return game.engine.globalStorage['objectStorage'][field]
        except:
            return default
            
    def removeGlobalObject(self, field):
        try:
            del game.engine.globalStorage['objectStorage'][field]
            game.engine.saveGlobalStorage = True
        except:
            pass
        
    def __followCallback(self, who):
        if self.target == who:
            game.engine.autoWalkCreatureTo(self, self.target.position, -1, True)
            self.target.scripts["onNextStep"].append(self.__followCallback)
            
    def follow(self, target):
        """if self.targetMode == 2 and self.target == target:
            self.targetMode = 0
            self.target = None
            return"""

        self.target = target
        self.targetMode = 2
        game.engine.autoWalkCreatureTo(self, self.target.position, -1, True)
        self.target.scripts["onNextStep"].append(self.__followCallback)

    def playerSay(self, player, say, type, channel):
        pass # Override me

    # Change passability
    def setSolid(self, solid):
        if self.solid == solid:
            return
            
        self.solid = solid
        
        for client in getSpectators(self.position):
            stream = client.packet(0x92)
            stream.uint32(self.cid)
            stream.uint8(self.solid)
            stream.send(client)
            
    def setSolidFor(self, player, solid):
        stream = player.packet(0x92)
        stream.uint32(self.cid)
        stream.uint8(solid)
        stream.send(player.client)
        
    # Shields
    def setPartyShield(self, shield):
        if self.shield == shield:
            return
            
        self.shield = shield
    
        for player in getPlayers(self.position):
            stream = player.packet(0x90)
            stream.uint32(self.cid)
            stream.uint8(self.getPartShield(player))
            stream.send(player.client)
            
    def getPartyShield(self, creature):
        return self.shield # TODO
        
    # Emblem
    def setEmblem(self, emblem):
        if self.emblem == emblem:
            return
        
        self.emblem = emblem

        for player in getPlayers(self.position):
            stream = player.packet()
            stream.addTileCreature(self.position, game.map.getTile(self.position).findStackpos(self), self, player)
            stream.send(player.client)
            
    # Skull
    def setSkull(self, skull):
        if self.skull == skull:
            return
        
        self.skull = skull

        for player in getPlayers(self.position):
            stream = player.packet(0x90)
            stream.uint32(self.cid)
            stream.uint8(self.getSkull(player))
            stream.send(player.client)    
            
    def getSkull(self, creature):
        return self.skull # TODO
        
    def square(self, creature, color=27):
        pass
    
    # Conditions
    def condition(self, condition, stackbehavior=enum.CONDITION_LATER, maxLength=0):
        try:
            oldCondition = self.conditions[condition.type]
            if not oldCondition.length:
                raise
            
            if stackbehavior == enum.CONDITION_IGNORE:
                return False
            elif stackbehavior == enum.CONDITION_LATER:
                return reactor.callLater(oldCondition.length * oldCondition.every, self.condition, condition, stackbehavior)
            elif stackbehavior == enum.CONDITION_ADD:
                if maxLength:
                    oldCondition.length = min(condition.length + oldCondition.length, maxLength)
                else:
                    oldCondition.length += condition.length
                    
            elif stackbehavior == enum.CONDITION_MODIFY:
                if maxLength:
                    condition.length = min(condition.length + oldCondition.length, maxLength)
                else:
                    condition.length += oldCondition.length
                    
                self.conditions[condition.type] = condition
            elif stackbehavior == enum.CONDITION_REPLACE:
                oldCondition.stop()
                condition.start(self)
                self.conditions[condition.type] = condition

        except:
            condition.start(self)
            self.conditions[condition.type] = condition
            
   
        self.refreshConditions()

    def multiCondition(self, *argc, **kwargs):
        try:
            stackbehavior = kwargs["stackbehavior"]
        except:
            stackbehavior = enum.CONDITION_LATER
        
        currCon = argc[0]
        for con in argc[1:]:
            currCon.callback = lambda: self.condition(con, stackbehavior)
            currCon = con
            
        self.condition(argc[0], stackbehavior)
        
    def hasCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            self.conditions[conditionType]
            return True
        except:
            return False

    def getCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            return self.conditions[conditionType]
        except:
            return False
            
    def loseCondition(self, conditionType, subtype=""):
        if subtype and isinstance(conditionType, str):
            conditionType = "%s_%s" % (conditionType, subtype)
        try:
            self.condions[conditionType].stop()
            return True
        except:
            return False

    ##############
    ### Spells ###
    ##############
    def castSpell(self, spell, strength=None, target=None):
        game.spell.spells[spell][0](self, strength, target)
    
    #############
    ### House ###
    #############
    def kickFromHouse(self):
        tile = game.map.getTile(self.position)
        try:
            # Find door pos
            doorPos = game.map.houseDoors[tile.houseId]
            
            
            
            # Try north
            found = True
            doorPos[1] -= 1
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break
                    
            if found:
                self.teleport(doorPos)
                return True
            
            # Try south
            found = True
            doorPos[1] += 2 # Two to counter north change
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break
                    
            if found:
                self.teleport(doorPos)
                return True
                
            # Try east
            found = True
            doorPos[1] -= 1 # counter south change
            doorPos[0] -= 1
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break
                    
            if found:
                self.teleport(doorPos)
                return True

            # Try west
            found = True
            doorPos[0] += 2 # counter east change
            testTile = game.map.getTile(doorPos)
            for i in testTile.getItems():
                if i.solid:
                    found = False
                    break
                    
            if found:
                self.teleport(doorPos)
                return True
                
            return False # Not found
            
        except:
            return False # Not in a house
    
    #####################
    ### Compatibility ###
    #####################
    
    def message(self, message, msgType='MSG_INFO_DESCR', color=0, value=0, pos=None):
        pass
    
    def cooldownSpell(self, icon, group, cooldown, groupCooldown=None):
        if groupCooldown == None: groupCooldown = cooldown   
        t = time.time()  + cooldown
        self.cooldowns[icon] = t
        self.cooldowns[group << 8] = t
        
    def cooldownIcon(self, icon, cooldown):
        self.cooldowns[icon] = time.time() + cooldown
        
    def cooldownGroup(self, group, cooldown):
        self.cooldowns[group << 8] = time.time() + cooldown

    ################
    ### Instance ###
    ################
    
    def setInstance(self, instanceId=None):
        # Teleport to the same position within instance
        newPosition = self.position.copy()
        newPosition.instanceId = instanceId
        self.teleport(instanceId)
        
    ###################
    ### Walkability ###
    ###################
    def walkable(self, state=True):
        self.canWalk = state
        
    def toggleWalkable(self):
        self.canWalk = not self.canWalk
    
    ####################
    ### Internal Use ###
    ####################
    def use(self, position, thing):
        game.scriptsystem.get('use').runSync(thing, self, None, position=position, index=0)
        
class Condition(object):
    def __init__(self, type, subtype="", length=1, every=1, check=None, *argc, **kwargs):
        self.length = length
        self.every = every
        self.creature = None
        self.tickEvent = None
        self.check = check
        
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = type
        self.effectArgs = argc
        self.effectKwargs = kwargs
        
        try:
            self.effect
        except:
            if type == CONDITION_FIRE:
                self.effect = self.effectFire
            elif type == CONDITION_POISON:
                self.effect = self.effectPoison
            elif type == CONDITION_REGENERATEHEALTH:
                self.effect = self.effectRegenerateHealth
            elif type == CONDITION_REGENERATEMANA:
                self.effect = self.effectRegenerateMana
                
    def start(self, creature):
        self.creature = creature
        if self.creature.isPlayer():
            self.saveCondition = True
            
        self.init()
        self.tick()
        
    def stop(self):
        try:
            self.tickEvent.cancel()
        except:
            pass
        
        self.finish()
        
    def init(self):
        pass

    def callback(self): pass
    
    def finish(self):
        del self.creature.conditions[self.type]
        if self.creature.isPlayer():
            self.saveCondition = True
        self.creature.refreshConditions()
        self.callback()

    def effectPoison(self, damage=0, minDamage=0, maxDamage=0):
        self.creature.magicEffect(EFFECT_HITBYPOISON)
        self.creature.modifyHealth(-(damage or random.randint(minDamage, maxDamage)))

    def effectFire(self, damage=0, minDamage=0, maxDamage=0):
        self.creature.magicEffect(EFFECT_HITBYFIRE)
        self.creature.modifyHealth(-(damage or random.randint(minDamage, maxDamage)))

    def effectRegenerateHealth(self, gainhp=None):
        if not gainhp:
            gainhp = self.creature.getVocation().health
            self.creature.modifyHealth(gainhp[0])
            
        else:    
            self.creature.modifyHealth(gainhp)

    def effectRegenerateMana(self, gainmana=None):
        if not gainmana:
            gainmana = self.creature.getVocation().mana
            self.creature.modifyMana(gainmana[0])
            
        else:    
            self.creature.modifyMana(gainmana)
                    
    def tick(self):
        if not self.creature:
            return
            
        self.effect(*self.effectArgs, **self.effectKwargs)
        self.length -= self.every # This "can" become negative!
        
        if self.check: # This is what we do if we got a check function, independantly of the length
            if self.check(self.creature):
                self.tickEvent = reactor.callLater(self.every, self.tick)
            else:
                self.finish()
                
        elif self.length > 0:
            self.tickEvent = reactor.callLater(self.every, self.tick)
        else:
            self.finish()
            
    def copy(self):
        return copy.deepcopy(self)
        
    def __getstate__(self):
        d = self.__dict__.copy()
        d["creature"] = None
        return d

class Boost(Condition):
    def __init__(self, type, mod, length, subtype="", percent=False, *argc, **kwargs):
        self.length = length
        self.creature = None
        self.tickEvent = None
        if subtype and isinstance(type, str):
            self.type = "%s_%s" % (type, subtype)
        else:
            self.type = '_'.join(type)
        self.ptype = [type] if not isinstance(type, list) else type
        self.effectArgs = argc
        self.effectKwargs = kwargs
        self.mod = [mod] if not isinstance(mod, list) else mod
        self.percent = percent
    
    def add(self, type, mod):
        self.ptype.append(type)
        self.mod.append(mod)
        return self
        
    def tick(self): pass
    def init(self):
        pid = 0
        for ptype in self.ptype:
            # Apply
            try:
                pvalue = getattr(self.creature, ptype)
                inStruct = 0
            except:
                pvalue = self.creature.data[ptype]
                inStruct = 1
            
            if isinstance(self.mod[pid], int):
                if self.percent:
                    pvalue *= self.mod[pid]
                else:
                    pvalue += self.mod[pid]
            else:
                pvalue = self.mod[pid](self.creature, ptype, True)
                
            # Hack
            if ptype == "speed":
                self.type = game.enum.CONDITION_HASTE
                self.creature.setSpeed(pvalue)
            else:
                if inStruct == 0:
                    setattr(self.creature, ptype, pvalue)
                else:
                    self.creature.data[ptype] = pvalue
            pid += 1
            
        self.tickEvent = reactor.callLater(self.length, self.finish)
            
        self.creature.refreshStatus()
    def callback(self):
        pid = 0
        for ptype in self.ptype:
            # Apply
            try:
                pvalue = getattr(self.creature, ptype)
                inStruct = 0
            except:
                pvalue = self.creature.data[ptype]
                inStruct = 1
            
            if isinstance(self.mod[pid], int):
                if self.percent:
                    pvalue /= self.mod[pid]
                else:
                    pvalue -= self.mod[pid]
            else:
                pvalue = self.mod[pid](self.creature, ptype, False)
                
            # Hack
            if ptype == "speed":
                self.creature.setSpeed(pvalue)
            else:
                if inStruct == 0:
                    setattr(self.creature, ptype, pvalue)
                else:
                    self.creature.data[ptype] = pvalue
                
            pid += 1
        self.creature.refreshStatus()
        
def MultiCondition(type, subtype="", *argc):
    conditions = []
    for x in argc:
        conditions.append(Condition(type, subtype, **x))
        
    for index in len(conditions):
        if index != len(conditions)-1:
            conditions[index].callback = lambda self: self.creature.condition(conditions[index+1])
    
    return conditions[0]
    