novice_of_the_cult = genMonster("Novice of the Cult", (133, 6080), "a novice of the cult")
novice_of_the_cult.setOutfit(114, 95, 114, 114)
novice_of_the_cult.health(285)
novice_of_the_cult.type("blood")
novice_of_the_cult.defense(armor=16, fire=1.05, earth=0.9, energy=1.08, ice=0.9, holy=0.9, death=1.08, physical=1.1, drown=1)
novice_of_the_cult.experience(100)
novice_of_the_cult.speed(210)
novice_of_the_cult.behavior(summonable=0, hostile=True, illusionable=True, convinceable=0, pushable=False, pushItems=True, pushCreatures=True, targetDistance=1, runOnHealth=40)
novice_of_the_cult.walkAround(energy=1, fire=1, poison=1)
novice_of_the_cult.immunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
novice_of_the_cult.summon("chicken", 10)
novice_of_the_cult.maxSummons(1)
novice_of_the_cult.voices("Fear us!", "You will not tell anyone what you have seen!", "Your curiosity will be punished!")
novice_of_the_cult.regMelee(65, condition=CountdownCondition(CONDITION_POISON, 1), conditionChance=100)