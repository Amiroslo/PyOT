Stone_Devourer = game.monster.genMonster("Stone Devourer", (486, 15864), "a stone devourer")
Stone_Devourer.setHealth(4200)
Stone_Devourer.bloodType(color="undead")
Stone_Devourer.setDefense(armor=65, fire=0, earth=0, energy=0.7, ice=0.7, holy=0.7, death=0.7, physical=0.9, drown=0.7)
Stone_Devourer.setExperience(2900)
Stone_Devourer.setSpeed(500)
Stone_Devourer.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
Stone_Devourer.walkAround(energy=0, fire=0, poison=0)
Stone_Devourer.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Stone_Devourer.voices("Rumble!")
Stone_Devourer.regMelee(950)