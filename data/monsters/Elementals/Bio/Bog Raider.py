bog_raider = genMonster("Bog Raider", (299, 8951), "a bog raider")
bog_raider.health(1300, healthmax=1300)
bog_raider.type("blood")
bog_raider.defense(armor=22, fire=0.15, earth=0.7, energy=1.1, ice=1.05, holy=1.05, death=0.95, physical=1.05, drown=1)
bog_raider.experience(800)
bog_raider.speed(300)
bog_raider.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
bog_raider.walkAround(energy=1, fire=1, poison=1)
bog_raider.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
bog_raider.voices("Tchhh!", "Slurp!")
bog_raider.regMelee(180, condition=CountdownCondition(CONDITION_POISON, 4), conditionChance=100)
bog_raider.loot( (2148, 100, 105), ("boggy dreads", 10.0), ("great health potion", 1.75), ("springsprout rod", 1.0), ("great spirit potion", 2.0), ("plate legs", 2.0), ("ultimate health potion", 0.75), ("belted cape", 0.5), ("paladin armor", 0.0025) )