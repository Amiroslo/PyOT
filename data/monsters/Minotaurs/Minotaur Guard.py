
minotaur_guard = game.monster.genMonster("Minotaur Guard", (29, 5983), "a minotaur guard")
minotaur_guard.setHealth(185)
minotaur_guard.bloodType(color="blood")
minotaur_guard.setDefense(armor=20, fire=0.8, earth=1, energy=1, ice=1.1, holy=0.9, death=1.1, physical=1, drown=1)
minotaur_guard.setExperience(160)
minotaur_guard.setSpeed(190)
minotaur_guard.setBehavior(summonable=550, hostile=1, illusionable=1, convinceable=550, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
minotaur_guard.walkAround(energy=1, fire=1, poison=1)
minotaur_guard.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
minotaur_guard.voices("Kirrl Karrrl!", "Kaplar")
minotaur_guard.regMelee(100)