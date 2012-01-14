skeleton = game.monster.genMonster("Skeleton", (33, 5972), "a skeleton")
skeleton.setHealth(50)
skeleton.bloodType(color="undead")
skeleton.setDefense(armor=3, fire=1, earth=1, energy=1, ice=1, holy=1.25, death=0, physical=1, drown=1)
skeleton.setExperience(35)
skeleton.setSpeed(154)
skeleton.setBehavior(summonable=300, hostile=1, illusionable=1, convinceable=300, pushable=0, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=0)
skeleton.walkAround(energy=1, fire=1, poison=1)
skeleton.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
skeleton.regMelee(17)
skeleton.loot( (2148, 100, 10), ("brass shield", 3.0), ("sword", 2.0), ("hatchet", 5.5), ("mace", 5.25), ("pelvis bone", 9.75), ("bone", 49.75), ("torch", 9.75), ("viking helmet", 7.5) )