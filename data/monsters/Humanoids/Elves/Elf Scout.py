elf_scout = game.monster.genMonster("Elf Scout", (64, 6012), "an elf scout")
elf_scout.setHealth(160, healthmax=160)
elf_scout.bloodType(color="blood")
elf_scout.setDefense(armor=7, fire=1, earth=1, energy=1, ice=1, holy=1, death=1.1, physical=1, drown=1)
elf_scout.setExperience(75)
elf_scout.setSpeed(225)
elf_scout.setBehavior(summonable=360, hostile=1, illusionable=1, convinceable=360, pushable=0, pushItems=1, pushCreatures=0, targetDistance=4, runOnHealth=0)
elf_scout.walkAround(energy=1, fire=1, poison=1)
elf_scout.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=0)
elf_scout.voices("Tha'shi Ab'Dendriel!", "Evicor guide my arrow!", "Your existence will end here!", "Feel the sting of my arrows!", "Thy blood will quench the soil's thirst!")
elf_scout.regMelee(40)
elf_scout.regDistance(80, ANIMATION_ARROW, game.monster.chance(21))
elf_scout.loot( ("poison arrow", 36.0, 4), ("elven scouting glass", 9.75), ("elvish talisman", 4.75), ("arrow", 100, 12), (2148, 100, 25), ("grapes", 17.75), ("bow", 4.0), ("waterskin", 1.25), ("sandals", 0.75), (5921, 0.75), ("elvish bow", 0.0025) )