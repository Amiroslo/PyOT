cyclops_smith = genMonster("Cyclops Smith", (277, 7740), "a cyclops smith")
cyclops_smith.setHealth(435)
cyclops_smith.bloodType("blood")
cyclops_smith.setDefense(armor=30, fire=0.9, earth=1.1, energy=0.8, ice=1, holy=0.8, death=1.05, physical=1, drown=1)
cyclops_smith.setExperience(255)
cyclops_smith.setSpeed(220)
cyclops_smith.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=695, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
cyclops_smith.walkAround(energy=1, fire=1, poison=1)
cyclops_smith.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
cyclops_smith.voices("Outis emoi g' onoma.", "Whack da humy!", "Ai humy phary ty kaynon")
cyclops_smith.regMelee(150)
cyclops_smith.loot( (3031, 100, 70), ("meat", 50.5), ("cyclops toe", 8.75), ("heavy machete", 2.25), ("battle axe", 5.25), ("battle hammer", 4.75), ("battle shield", 6.5), ("double axe", 0.75), ("plate shield", 2.0), ("spiked squelcher", 0.0025), ("strong health potion", 0.5), ("cyclops trophy", 0.25), ("dark helmet", 0.25), ("club ring", 0.25) )