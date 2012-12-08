dragon_hatchling = genMonster("Dragon Hatchling", (271, 7621), "a dragon hatchling")
dragon_hatchling.setHealth(380)
dragon_hatchling.bloodType("blood")
dragon_hatchling.setDefense(armor=25, fire=0, earth=0.25, energy=1.05, ice=1.1, holy=1, death=1, physical=1, drown=1)
dragon_hatchling.setExperience(185)
dragon_hatchling.setSpeed(170)
dragon_hatchling.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=75)
dragon_hatchling.walkAround(energy=1, fire=0, poison=1)
dragon_hatchling.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
dragon_hatchling.voices("Fchu?", "Rooawwrr")
dragon_hatchling.loot( (2148, 100, 55), ("dragon ham", 53.5), (12413, 3.5), ("health potion", 0.25) )
 
dfwave = spell.Spell("drag fwave", target=TARGET_AREA)
dfwave.area(AREA_WAVE8)
dfwave.element(FIRE)
dfwave.effects(area=EFFECT_HITBYFIRE)
 
dragon_hatchling.regMelee(55)
dragon_hatchling.regTargetSpell("drag fwave", 60, 90, check=chance(20))
dragon_hatchling.regSelfSpell("Light Healing", 25, 55, check=chance(18)) #how much?
dragon_hatchling.regTargetSpell(2304, 30, 55, check=chance(20))