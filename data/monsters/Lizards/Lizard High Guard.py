lizard_high_guard = game.monster.genMonster("Lizard High Guard", (337, 11272), "a lizard high guard")
lizard_high_guard.setHealth(1800, healthmax=1800)
lizard_high_guard.bloodType(color="blood")
lizard_high_guard.setDefense(armor=25, fire=0.55, earth=0, energy=1, ice=1.1, holy=1, death=1, physical=1, drown=1)
lizard_high_guard.setExperience(1450)
lizard_high_guard.setSpeed(340)
lizard_high_guard.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
lizard_high_guard.walkAround(energy=1, fire=1, poison=0)
lizard_high_guard.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
lizard_high_guard.voices("Hizzzzzzz!", "To armzzzz!", "Engage zze aggrezzor!")
lizard_high_guard.regMelee(261)