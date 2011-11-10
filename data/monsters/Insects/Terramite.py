terramite = game.monster.genMonster("Terramite", (346, 11347), "a terramite")
terramite.setHealth(365)
terramite.bloodType(color="slime")
terramite.setDefense(armor=19, fire=1.1, earth=0.8, energy=1.05, ice=1, holy=1, death=1, physical=0.95, drown=1)
terramite.setExperience(160)
terramite.setSpeed(220)
terramite.setBehavior(summonable=505, hostile=1, illusionable=1, convinceable=505, pushable=0, pushItems=1, pushCreatures=0, targetDistance=1, runOnHealth=0)
terramite.walkAround(energy=1, fire=1, poison=1)
terramite.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=1)
terramite.voices("Zrp zrp!")
terramite.regMelee(100)
terramite.loot( (2148, 100, 25), ("terramite legs", 8.5), ("terramite shell", 2.0), ("terramite eggs", 3.25) )