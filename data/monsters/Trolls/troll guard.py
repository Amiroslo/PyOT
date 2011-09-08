import game.monster
#file is mostly wrong
troll_guard = game.monster.genMonster("Troll Guard", (281, 7926), "a troll guard")
troll_guard.setHealth(60)
troll_guard.bloodType(color="blood")
troll_guard.setDefense(armor=10, fire=1, earth=1.1, energy=0.85, ice=1, holy=0.9, death=1.1, physical=1, drown=1)
troll_guard.setExperience(25)
troll_guard.setSpeed(120)
troll_guard.setBehavior(summonable=340, hostile=1, illusionable=1, convinceable=340, pushable=1, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=20)
troll_guard.walkAround(energy=1, fire=1, poison=1)
troll_guard.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
troll_guard.regMelee(15)