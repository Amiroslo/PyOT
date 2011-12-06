acolyte_of_darkness = game.monster.genMonster("Acolyte of Darkness", (9, 6080), "an acolyte of darkness")
acolyte_of_darkness.setHealth(325, healthmax=325)
acolyte_of_darkness.bloodType(color="blood")
acolyte_of_darkness.setDefense(armor=20, fire=0, earth=0, energy=1, ice=1, holy=1.35, death=0, physical=1, drown=1)
acolyte_of_darkness.setExperience(200)
acolyte_of_darkness.setSpeed(300)#
acolyte_of_darkness.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
acolyte_of_darkness.walkAround(energy=0, fire=0, poison=0)
acolyte_of_darkness.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
acolyte_of_darkness.regMelee(120)
acolyte_of_darkness.loot( ("midnight shard", 4.5) )