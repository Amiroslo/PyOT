import game.monster

mutated_tiger = game.monster.genMonster("Mutated Tiger", (318, 9913), "a mutated tiger")
mutated_tiger.setHealth(1100)
mutated_tiger.bloodType(color="blood")
mutated_tiger.setDefense(armor=30, fire=0.8, earth=0.2, energy=0.8, ice=-0.8, holy=1, death=1.05, physical=1, drown=1)
mutated_tiger.setExperience(750)
mutated_tiger.setSpeed(245)
mutated_tiger.setBehavior(summonable=0, attackable=1, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=100)
mutated_tiger.walkAround(energy=0, fire=0, poison=0)
mutated_tiger.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=1)
mutated_tiger.voices("GRAAARRRRRR", "CHHHHHHHHHHH")