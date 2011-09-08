import game.monster

slime = game.monster.genMonster("Slime", (35, 1496), "a slime")
slime.setHealth(150)
slime.bloodType(color="slime")
slime.setDefense(armor=5, fire=1.1, earth=0, energy=1.1, ice=1.1, holy=1, death=1, physical=1, drown=1)
slime.setExperience(160)
slime.setSpeed(120)
slime.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=0, targetDistance=1, runOnHealth=0)
slime.walkAround(energy=1, fire=1, poison=0)
slime.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
slime.voices("Blubb")
slime.regMelee(107)