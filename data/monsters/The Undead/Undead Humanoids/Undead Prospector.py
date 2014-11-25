undead_prospector = genMonster("Undead Prospector", 18, 5976)
undead_prospector.health(100)
undead_prospector.type("blood")
undead_prospector.defense(armor=2, fire=1, earth=0.8, energy=0.7, ice=0.9, holy=1.25, death=0, physical=1, drown=0)
undead_prospector.experience(85)
undead_prospector.speed(180)
undead_prospector.behavior(summonable=440, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)#convinceable?
undead_prospector.walkAround(energy=1, fire=1, poison=1)
undead_prospector.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=1)
undead_prospector.voices("Our mine... leave us alone.", "Turn back...", "These mine is ours... you shall not pass.")
undead_prospector.melee(50)
undead_prospector.loot( (3976, 100, 6), (2148, 100, 29), ("knife", 25.0), ("torch", 55.0), ("brass helmet", 15.0) )