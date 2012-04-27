quara_predator = game.monster.genMonster("Quara Predator", (20, 6067), "a quara predator")
quara_predator.setHealth(2200)
quara_predator.bloodType(color="blood")
quara_predator.setDefense(armor=44, fire=0, earth=1.1, energy=1.25, ice=0, holy=1, death=1, physical=1, drown=0)
quara_predator.setExperience(1600)
quara_predator.setSpeed(520)
quara_predator.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
quara_predator.walkAround(energy=1, fire=0, poison=1)
quara_predator.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
quara_predator.voices("Gnarrr!", "Tcharrr!", "Rrrah!", "Rraaar!")
quara_predator.loot( ("assassin star", 0.5), (2148, 100, 148), ("double axe", 3.0), ("royal spear", 37.5, 7), ("relic sword", 0.5), ("quara bone", 10.25), ("great health potion", 1.0), ("fish fin", 2.0, 3), ("shrimp", 4.75), ("skull helmet", 0.5), ("small diamond", 7.0, 2), ("glacier robe", 0.5), ("giant shrimp", 0.0025) )

quara_predator.regMelee(470)
quara_predator.regSelfSpell("Light Healing", 25, 75, check=chance(20))
quara_predator.regSelfSpell("Haste", 360, 360, length=8, check=chance(9)) #strength time?