frost_giantess = genMonster("Frost Giantess", 265, 7330)
frost_giantess.health(275)
frost_giantess.type("blood")
frost_giantess.defense(armor=22, fire=1.1, earth=1, energy=1.1, ice=0, holy=0.9, death=1.03, physical=1, drown=1)
frost_giantess.experience(150)
frost_giantess.speed(195)
frost_giantess.behavior(summonable=490, hostile=True, illusionable=True, convinceable=490, pushable=False, pushItems=True, pushCreatures=True, targetDistance=4, runOnHealth=0)
frost_giantess.walkAround(energy=1, fire=1, poison=1)
frost_giantess.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
frost_giantess.voices("Ymirs Mjalle!", "No run so much, must stay fat!", "Horre Sjan Flan!", "Damned fast food.", "Come kiss the cook!")
frost_giantess.melee(60)
frost_giantess.distance(80, ANIMATION_LARGEROCK, chance(21))
frost_giantess.loot( (2148, 100, 40), ("small stone", 20.25, 3), ("ham", 19.75, 2), ("frost giant pelt", 5.0), ("ice cube", 1.75), ("battle shield", 1.75), ("mana potion", 1.0), ("short sword", 8.25), ("norse shield", 0.25), ("shard", 0.0025), ("dark helmet", 0.25), ("club ring", 0.0025) )