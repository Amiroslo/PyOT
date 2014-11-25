
snake = genMonster("Snake", 28, 2817)
snake.health(15)
snake.type("blood")
snake.defense(armor=2, fire=1.1, earth=1, energy=0.8, ice=1.1, holy=1, death=1, physical=1, drown=1)
snake.experience(10)
snake.speed(120)
snake.behavior(summonable=205, hostile=True, illusionable=True, convinceable=0, pushable=True, pushItems=False, pushCreatures=False, targetDistance=1, runOnHealth=0)
snake.walkAround(energy=1, fire=1, poison=0)
snake.immunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
snake.voices("Zzzzzzt")
snake.melee(8, condition=Condition(CONDITION_POISON, 0, 1, damage=1), conditionChance=100)
