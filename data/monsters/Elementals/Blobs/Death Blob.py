
death_blob = genMonster("Death Blob", 315, 9960)
death_blob.health(320)
death_blob.type("undead")
death_blob.defense(armor=15, fire=1.1, earth=0, energy=1.1, ice=0.9, holy=1.1, death=0, physical=0.8, drown=1)
death_blob.experience(300)
death_blob.speed(230)
death_blob.behavior(summonable=0, hostile=True, illusionable=False, convinceable=0, pushable=False, pushItems=True, pushCreatures=False, targetDistance=1, runOnHealth=0)
death_blob.walkAround(energy=1, fire=1, poison=0)
death_blob.immunity(paralyze=0, invisible=0, lifedrain=1, drunk=1)
death_blob.summon("Death Blob", 10)
death_blob.maxSummons(3)
death_blob.melee(100)
death_blob.loot( ("glob of tar", 13.0) )