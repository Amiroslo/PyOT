swarmer = genMonster("swarmer", (460, 15385), "a swarmer")
swarmer.health(460, healthmax=460)
swarmer.type("slime")
swarmer.defense(armor=25, fire=1.1, earth=0, energy=0.25, ice=1.05, holy=1, death=1, physical=1, drown=1)
swarmer.experience(350)
swarmer.speed(250) #incorrect
swarmer.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=50)
swarmer.walkAround(energy=1, fire=1, poison=0)
swarmer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
swarmer.regMelee(100, condition=CountdownCondition(CONDITION_POISON, 4), conditionChance=100)