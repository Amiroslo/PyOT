hellspawn = game.monster.genMonster("Hellspawn", (322, 9923), "a hellspawn")
hellspawn.setHealth(3500)
hellspawn.bloodType(color="blood")
hellspawn.setDefense(armor=15, fire=0.6, earth=0.2, energy=0.9, ice=1.1, holy=0.7, death=1.05, physical=0.9, drown=1)
hellspawn.setExperience(2550)
hellspawn.setSpeed(300)
hellspawn.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
hellspawn.walkAround(energy=1, fire=0, poison=0)
hellspawn.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
hellspawn.voices("Your fragile bones are like toothpicks to me.", "You little weasel will not live to see another day.", "I'm just a messenger of what's yet to come.", "HRAAAAAAAAAAAAAAAARRRR!", "I'm taking you down with me!")
hellspawn.regMelee(350)#or more