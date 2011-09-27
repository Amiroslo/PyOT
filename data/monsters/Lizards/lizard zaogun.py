lizard_zaogun = game.monster.genMonster("Lizard Zaogun", (343, 11284), "a lizard zaogun")
lizard_zaogun.setHealth(2955)
lizard_zaogun.bloodType(color="blood")
lizard_zaogun.setDefense(armor=35, fire=0.55, earth=0, energy=0.8, ice=0.85, holy=1, death=0.9, physical=0.5, drown=1)
lizard_zaogun.setExperience(1700)
lizard_zaogun.setSpeed(420)
lizard_zaogun.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=150)
lizard_zaogun.walkAround(energy=0, fire=0, poison=0)
lizard_zaogun.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
lizard_zaogun.voices("Hissss!", "Cowardzz!", "Softzzkinzz from zze zzouzz!", "Zztand and fight!")
lizard_zaogun.regMelee(350)