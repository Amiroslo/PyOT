Mushroom_Sniffer = genMonster("Mushroom Sniffer", (60, 6000), "a mushroom sniffer")
Mushroom_Sniffer.setHealth(250)
Mushroom_Sniffer.bloodType("blood")
Mushroom_Sniffer.setDefense(armor=15, fire=0.1, earth=0.1, energy=0.1, ice=0.1, holy=0.1, death=0.1, physical=0.1, drown=0.1)
Mushroom_Sniffer.setExperience(0)
Mushroom_Sniffer.setSpeed(100)
Mushroom_Sniffer.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=74)
Mushroom_Sniffer.walkAround(energy=0, fire=0, poison=0)
Mushroom_Sniffer.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
Mushroom_Sniffer.voices("Oink", "Sniff sniff", "Uuuoink") #made up
Mushroom_Sniffer.regMelee(0)