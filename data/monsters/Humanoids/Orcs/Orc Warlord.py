orc_warlord = genMonster("Orc Warlord", (2, 6008), "an orc warlord")
orc_warlord.setHealth(950, healthmax=950)
orc_warlord.bloodType("blood")
orc_warlord.setDefense(armor=30, fire=0.2, earth=1.1, energy=0.8, ice=1, holy=0.9, death=1.05, physical=1, drown=1)
orc_warlord.setExperience(670)
orc_warlord.setSpeed(290)
orc_warlord.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
orc_warlord.walkAround(energy=1, fire=0, poison=1)
orc_warlord.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
orc_warlord.voices("Ikem rambo zambo!", "Orc buta bana!", "Ranat Ulderek!", "Fetchi Maruk Buta")
orc_warlord.regMelee(250)
orc_warlord.regDistance(200, ANIMATION_THROWINGSTAR, chance(21))
orc_warlord.loot( ("broken helmet", 26.0), ("orc leather", 19.25), ("orc tooth", 10.0), ("orcish axe", 4.0), ("skull belt", 6.0), ("throwing star", 100, 18), ("health potion", 0.25), ("fish", 16.75, 2), ("scimitar", 3.25), (2148, 100, 45), ("plate armor", 8.75), ("two handed sword", 1.75), ("brass armor", 0.75), ("hunting spear", 4.0), ("plate legs", 5.25), ("dark helmet", 1.0), ("protection amulet", 2.0) )