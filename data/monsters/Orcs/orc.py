import game.monster

orc = game.monster.genMonster("Orc", (5, 5966), "an orc")
orc.setHealth(70)
orc.bloodType(color="blood")
orc.setDefense(armor=4, fire=1, earth=1.1, energy=0.8, ice=1, holy=0.9, death=1.1, physical=1, drown=1)
orc.setExperience(25)
orc.setSpeed(150)
orc.setBehavior(summonable=300, attackable=1, hostile=1, illusionable=1, convinceable=300, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=15)
orc.walkAround(energy=1, fire=1, poison=1)
orc.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
orc.voices("Grow truk grrrrr.", "Prek tars, dekklep zurk.", "Grak brrretz!")