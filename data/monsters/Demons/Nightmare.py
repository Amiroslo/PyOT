nightmare = game.monster.genMonster("Nightmare", (245, 6340), "a nightmare")
nightmare.setHealth(2700)
nightmare.bloodType(color="blood")
nightmare.setDefense(armor=25, fire=0.8, earth=0, energy=0.8, ice=0.9, holy=1.25, death=0, physical=1, drown=1)
nightmare.setExperience(2150)
nightmare.setSpeed(380)
nightmare.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=300)
nightmare.walkAround(energy=1, fire=1, poison=0)
nightmare.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
nightmare.voices("Close your eyes... I want to show you something.", "I will haunt you forever!", "Pffffrrrrrrrrrrrr.", "I will make you scream.", "Take a ride with me.", "Weeeheeheeeheee!")
nightmare.regMelee(150)
nightmare.loot( ("power bolt", 24.75, 4), ("ham", 29.75), ("scythe leg", 10.0), ("essence of a bad dream", 15.25), ("soul orb", 21.0), ("concentrated demonic blood", 29.75, 2), ("demonic essence", 10.25, 3), (2148, 100, 155), ("death ring", 1.25), ("platinum coin", 4.75, 3), ("skeleton decoration", 0.25), ("knight legs", 1.0), ("ancient shield", 1.0), ("boots of haste", 0.25), ("war axe", 0.0025), (5669, 0.0025) )