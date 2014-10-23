
minotaur_mage = genMonster("Minotaur Mage", (23, 5981), "a minotaur mage")
minotaur_mage.setHealth(155)
minotaur_mage.bloodType("blood")
minotaur_mage.setDefense(armor=20, fire=1.1, earth=0.8, energy=0.8, ice=1, holy=0.9, death=1.05, physical=1, drown=1)
minotaur_mage.setExperience(150)
minotaur_mage.setSpeed(170)
minotaur_mage.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=4, runOnHealth=0)
minotaur_mage.walkAround(energy=1, fire=1, poison=1)
minotaur_mage.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=1)
minotaur_mage.voices("Learrn tha secrret uf deathhh!", "Kaplar!")
minotaur_mage.regMelee(20)
minotaur_mage.loot( ("minotaur horn", 4.25, 2), (2148, 100, 35), ("carrot", 58.0, 8), ("purple robe", 5.5), ("minotaur leather", 2.0, 3), ("leather legs", 5.0), ("torch", 4.5), ("leather helmet", 3.75), ("taurus mace", 0.75), ("wand of cosmic energy", 0.5), ("mana potion", 0.5) )