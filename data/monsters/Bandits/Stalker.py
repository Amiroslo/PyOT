
Stalker = game.monster.genMonster("Stalker", (128, 6080), "a Stalker")
Stalker.setOutfit(95, 116, 95, 114)
Stalker.setTargetChance(10)
Stalker.bloodType("blood")
Stalker.setHealth(120)
Stalker.setExperience(90)
Stalker.setSpeed(260) # Correct
Stalker.walkAround(1,1,1) # energy, fire, poison
Stalker.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=0)
Stalker.setImmunity(0,1,1) # paralyze, invisible, lifedrain
Stalker.setDefense(0, fire=1.0, earth=1.0, energy=1.0, ice=1.0, holy=1.0, death=1.0, physical=1.0, drown=1.0)