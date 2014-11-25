duskbringer = genMonster("Duskbringer", 300, 8955)
duskbringer.health(3000, healthmax=3000)
duskbringer.type("blood")
duskbringer.defense(armor=59, fire=0.6, earth=0.2, energy=0.95, ice=1.1, holy=0.7, death=1.05, physical=1, drown=1)
duskbringer.experience(2600)
duskbringer.speed(300)
duskbringer.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
duskbringer.walkAround(energy=0, fire=0, poison=0)
duskbringer.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
duskbringer.voices("Death!", "Come a little closer!", "The end is near!")
duskbringer.melee(350)
duskbringer.loot( ("midnight shard", 9.0) )