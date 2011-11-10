centipede = game.monster.genMonster("Centipede", (124, 6050), "a centipede")
centipede.setHealth(70, healthmax=70)
centipede.bloodType(color="slime")
centipede.setDefense(armor=14, fire=1.15, earth=0, energy=0.9, ice=0.8, holy=1, death=1, physical=1, drown=1)
centipede.setExperience(34)
centipede.setSpeed(195)
centipede.setBehavior(summonable=335, hostile=1, illusionable=1, convinceable=335, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=0)
centipede.walkAround(energy=1, fire=1, poison=0)
centipede.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
centipede.regMelee(45)#poison 1hp/turn
centipede.loot( (2148, 100, 15), ("centipede leg", 10.0) )