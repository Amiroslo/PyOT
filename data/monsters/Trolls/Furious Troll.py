furious_troll = game.monster.genMonster("Furious Troll", (281, 7926), "a furious troll")
furious_troll.setHealth(245)
furious_troll.bloodType(color="blood")
furious_troll.setDefense(armor=10, fire=1, earth=1, energy=1, ice=1, holy=1, death=1, physical=1.05, drown=1)
furious_troll.setExperience(185)
furious_troll.setSpeed(195)#incorrect
furious_troll.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
furious_troll.walkAround(energy=0, fire=0, poison=0)
furious_troll.setImmunity(paralyze=0, invisible=1, lifedrain=0, drunk=0)
furious_troll.voices("Slice! Slice!", "DIE!!!")
furious_troll.regMelee(100)