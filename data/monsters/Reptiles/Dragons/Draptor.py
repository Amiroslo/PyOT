#mostly unknown
draptor = game.monster.genMonster("Draptor", (8, 5980), "a draptor")
draptor.setHealth(3000)
draptor.bloodType(color="blood")
draptor.setDefense(armor=2, fire=1, earth=1, energy=0, ice=1, holy=1, death=1, physical=1, drown=1)#
draptor.setExperience(2400)
draptor.setSpeed(300)
draptor.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=1500)
draptor.walkAround(energy=0, fire=0, poison=0)
draptor.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
#draptor.voices(*arg)
draptor.regMelee(150)
draptor.loot( (2148, 100, 180), ("strong mana potion", 13.25), ("strong health potion", 21.0), ("draptor scales", 5.25) )