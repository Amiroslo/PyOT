juggernaut = genMonster("Juggernaut", (244, 6336), "a juggernaut")
juggernaut.setHealth(20000, healthmax=20000)
juggernaut.bloodType("blood")
juggernaut.setDefense(armor=90, fire=0.7, earth=0.8, energy=1.1, ice=0.9, holy=1.05, death=1, physical=0.8, drown=1)
juggernaut.setExperience(8700)
juggernaut.setSpeed(500)
juggernaut.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
juggernaut.walkAround(energy=1, fire=0, poison=0)
juggernaut.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
juggernaut.voices("RAAARRR!", "GRRRRRR!", "WAHHHH!")
juggernaut.regMelee(1480)
juggernaut.loot( ("ham", 79.0), (3031, 100, 189), ("concentrated demonic blood", 78.25, 4), ("soul orb", 34.5), ("great mana potion", 10.0), ("demonic essence", 44.75, 3), ("rusty armor", 9.25), ("onyx arrow", 5.75, 5), ("great health potion", 9.5), ("platinum coin", 13.75, 4), ("gold ingot", 5.0), ("assassin star", 1.25, 2), ("mastermind shield", 0.25), ("heavy mace", 0.0025), ("spiked squelcher", 2.0), ("demonbone amulet", 0.5), ("closed trap", 0.0025) )