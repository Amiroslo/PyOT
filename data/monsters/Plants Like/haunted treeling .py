import game.monster

haunted_treeling = game.monster.genMonster("Haunted Treeling ", (310, 9867), "a haunted treeling")
haunted_treeling.setHealth(450)
haunted_treeling.bloodType(color="undead")
haunted_treeling.setDefense(armor=25, fire=1.05, earth=0, energy=1, ice=0.9, holy=0.8, death=0.9, physical=1, drown=1)
haunted_treeling.setExperience(310)
haunted_treeling.setSpeed(260)
haunted_treeling.setBehavior(summonable=0, attackable=1, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
haunted_treeling.walkAround(energy=0, fire=0, poison=0)
haunted_treeling.setImmunity(paralyze=1, invisible=0, lifedrain=1, drunk=1)
haunted_treeling.voices("Knarrrz", "Huuhuuhuuuhuuaarrr", "Knorrrrrr")