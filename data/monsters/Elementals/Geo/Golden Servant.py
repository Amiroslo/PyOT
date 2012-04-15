golden_servant = game.monster.genMonster("Golden Servant", (396, 5980), "a golden servant")
golden_servant.setHealth(550)
golden_servant.bloodType(color="blood")
golden_servant.setDefense(armor=31, fire=0.85, earth=0.2, energy=0.75, ice=1.05, holy=0, death=1, physical=1, drown=1)
golden_servant.setExperience(450)
golden_servant.setSpeed(250)
golden_servant.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
golden_servant.walkAround(energy=0, fire=1, poison=0)
golden_servant.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
golden_servant.voices("Error. LOAD 'PROGRAM',8,1", "Remain. Obedient.")
golden_servant.regMelee(100)
golden_servant.loot( (2148, 100, 125), ("mana potion", 6.25), ("halberd", 2.5), ("health potion", 5.75), ("green mushroom", 2.75), ("gear wheel", 2.75), ("spellbook of enlightenment", 0.5) )