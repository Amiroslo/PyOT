spidris_elite = genMonster("Spidris Elite", (457, 15296), "a spidris elite")
spidris_elite.health(5000)
spidris_elite.type("slime")
spidris_elite.defense(armor=50, fire=1, earth=1, energy=1, ice=1, holy=1.1, death=1, physical=1, drown=1)
spidris_elite.experience(4000)
spidris_elite.speed(350) #incorrect
spidris_elite.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
spidris_elite.walkAround(energy=0, fire=0, poison=0)
spidris_elite.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
spidris_elite.regMelee(350)