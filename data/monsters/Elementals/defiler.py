defiler = game.monster.genMonster("Defiler", (238, 6532), "a defiler")
defiler.setHealth(3650)
defiler.bloodType(color="slime")
defiler.setDefense(armor=10, fire=1.25, earth=0, energy=0.9, ice=0.8, holy=1, death=1, physical=1, drown=1)
defiler.setExperience(3700)
defiler.setSpeed(260)
defiler.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
defiler.walkAround(energy=1, fire=1, poison=0)
defiler.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
defiler.voices("Blubb", "Blubb Blubb")
defiler.regMelee(240)#and poisons you