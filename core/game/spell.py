import game.scriptsystem # We use the talkactions from here
import game.item
import game.enum
import game.engine

spells = {}
fieldRunes = {}
ATTACK_GROUP = 1
HEALING_GROUP = 2
SUPPORT_GROUP=3
SPECIAL_GROUP = 4

AREA_ONE = ((0,0),)

def typeToEffect(type):
    if type == "fire":
        return (game.enum.EFFECT_HITBYFIRE, game.enum.ANIMATION_FIRE)
    elif type == "poison":
        return (game.enum.EFFECT_HITBYPOISON, game.enum.ANIMATION_POISON)
        
def makeField(fieldId):
    def make(position, **k):
        item = game.item.Item(fieldId)
        
        def effectOverTime(creature, damage, perTime, effect, forTicks, ticks=0):
            ticks += 1
            creature.modifyHealth(-1 * damage)
            creature.magicEffect(creature.position, effect)
            
            
            if ticks < forTicks:
                game.engine.safeCallLater(perTime, effectOverTime, creature, damage, perTime, effect, forTicks, ticks)
                
        def callback(creature, thing, **k):
            if thing.damage:
                creature.magicEffect(creature.position, typeToEffect(thing.field)[0])
                creature.modifyHealth(-1 * thing.damage)
                
            if thing.turns:
                game.engine.safeCallLater(thing.ticks / 1000, effectOverTime, creature, thing.damage, thing.ticks / 1000, typeToEffect(thing.field)[1], thing.turns)
        
        stackpos = game.engine.placeItem(item, position)
        if item.damage:
            game.scriptsystem.reg('walkOn', item, callback)
            if item.duration:
                item.decay(position, stackpos, callback=lambda i: game.scriptsystem.reg('walkOn', i, callback))
                
    return make
    
    
def conjureRune(name, words, make, icon, mana=0, level=0, mlevel=0, soul=1, vocation=None, use=2260, useCount=1, makeCount=1, teached=0, group=3, cooldown=2):
    def conjure(creature, text):
        if not creature.canDoSpell(icon, group):
            creature.exhausted()
            return False
            
        # Checks
        if creature.data["level"] < level:
            creature.notEnough("level")
        elif creature.data["mana"] < mana:
            creature.notEnough("mana")
        elif creature.data["soul"] < soul:
            creature.notEnough("soul")
        elif creature.data["maglevel"] < mlevel:
            creature.notEnough("magic level")
        elif vocation and not creature.data["vocation"] in vocation:
            creature.notPossible()
        else:
            #useItem = creature.findItemById(use, useCount)
            useItem = None
            slot = 0
            if creature.inventory[4] and creature.inventory[4].itemId == use and creature.inventory[4].count >= useCount:
                useItem = creature.inventory[4]
                slot = 5
            elif creature.inventory[5] and creature.inventory[5].itemId == use and creature.inventory[5].count >= useCount:
                useItem = creature.inventory[5]
                slot = 6
            elif creature.inventory[9] and creature.inventory[9].itemId == use and creature.inventory[9].count >= useCount:
                useItem = creature.inventory[9]
                slot = 10
                
            if not useItem:
                creature.needMagicItem()
                creature.magicEffect(creature.position, game.enum.EFFECT_POFF)
                
            else:
                useItem.count -= useCount
                creature.updateInventory(slot) # Send refresh to client
                item = game.item.Item(make,makeCount)

                ret = creature.itemToUse(item)
                if not ret:
                    creature.notEnoughRoom()
                
                if mana:
                    creature.modifyMana(-1 * mana)
                if soul:
                    creature.modifySoul(-1 * soul)
                creature.cooldownSpell(icon, group, cooldown)
                creature.message("Made %dx%s" % (makeCount, name))
                creature.magicEffect(creature.position, game.enum.EFFECT_MAGIC_RED)
    if name in spells:
        print "Warning: Duplicate spell with name %s" % name
    spells[name] = (words, conjure)
    game.scriptsystem.get("talkaction").reg(words, conjure)
    
def fieldRune(rune, level, mlevel, icon, group, area, callback, cooldown=2):
    def fieldrune(creature, thing, onPosition, **k):
        print "I was called!!!"
        if not creature.canDoSpell(icon, group):
            creature.exhausted()
            return False
            
        if creature.data["level"] < level:
            creature.notEnough("level")
        elif creature.data["maglevel"] < mlevel:
            creature.notEnough("magic level")
            
        else:
            useItem = None
            slot = 0
            if creature.inventory[4] and creature.inventory[4] == thing:
                useItem = creature.inventory[4]
                slot = 5
            elif creature.inventory[5] and creature.inventory[5] == thing:
                useItem = creature.inventory[5]
                slot = 6
            elif creature.inventory[9] and creature.inventory[9] == thing:
                useItem = creature.inventory[9]
                slot = 10
                
            if not useItem:
                creature.needMagicItem()
                creature.magicEffect(creature.position, game.enum.EFFECT_POFF)
                
            else:
                useItem.count -= 1
                creature.updateInventory(slot) # Send refresh to client
                
                creature.cooldownSpell(icon, group, cooldown)
                for a in area:
                    pos = onPosition[:]
                    pos[0] += a[0]
                    pos[1] += a[1]
                    callback(pos)
    print "fieldRune was called, rune = ", rune
    fieldRunes[rune] = fieldrune # Just to prevent reset
    game.scriptsystem.get("useWith").reg(rune, fieldrune)
    
def clear():
    fieldRunes.clear()
    spells.clear()