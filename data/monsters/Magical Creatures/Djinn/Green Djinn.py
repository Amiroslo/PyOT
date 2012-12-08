green_djinn = genMonster("Green Djinn", (51, 6016), "a green djinn")
green_djinn.setHealth(330)
green_djinn.bloodType("blood")
green_djinn.setDefense(armor=22, fire=0.8, earth=1, energy=0.5, ice=1.1, holy=1.13, death=0.8, physical=0.8, drown=1)
green_djinn.setExperience(215)
green_djinn.setSpeed(220)
green_djinn.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
green_djinn.walkAround(energy=1, fire=1, poison=1)
green_djinn.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
green_djinn.voices("Good wishes are for fairytales", "I wish you a merry trip to hell!", "Muahahahahaha", "I grant you a deathwish!")
green_djinn.regMelee(110)
green_djinn.loot( ("green piece of cloth", 2.0, 3), (2148, 100, 115), (12412, 2.25), ("small emerald", 6.75, 4), ("royal spear", 7.5, 2), ("cheese", 24.75), ("grave flower", 1.0), ("mana potion", 0.5), ("small oil lamp", 0.75), ("book", 2.5), ("mystic turban", 0.25) )