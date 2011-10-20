dragon = game.monster.genMonster("Dragon", (34, 5973), "a dragon")
dragon.setHealth(1000)
dragon.bloodType(color="blood")
dragon.setDefense(armor=15, fire=0, earth=0.2, energy=0.8, ice=1.1, holy=1, death=1, physical=1, drown=1)
dragon.setExperience(700)
dragon.setSpeed(180)
dragon.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=300)
dragon.walkAround(energy=0, fire=0, poison=0)
dragon.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
dragon.voices("GROOAAARRR", "FCHHHHH")
dragon.regMelee(120)