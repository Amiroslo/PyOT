humorless_fungus = genMonster("Humorless Fungus", 517, 18382) #almost everything is unknown health, stance, etc...--corpse(may be right)
humorless_fungus.health(1000, healthmax=1000)
humorless_fungus.type("blood")
humorless_fungus.defense(armor=25, fire=0.95, earth=0, energy=0.85, ice=0.85, holy=0.95, death=1, physical=1, drown=1)
humorless_fungus.experience(0)
humorless_fungus.speed(400)
humorless_fungus.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=0)
humorless_fungus.walkAround(energy=0, fire=0, poison=0)
humorless_fungus.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
humorless_fungus.voices("Munch munch munch!","Chatter".)
humorless_fungus.melee(480)