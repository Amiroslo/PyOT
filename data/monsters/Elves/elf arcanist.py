elf_arcanist = game.monster.genMonster("Elf Arcanist", (63, 6011), "an elf arcanist")
elf_arcanist.setHealth(220, healthmax=220)
elf_arcanist.bloodType(color="blood")
elf_arcanist.setDefense(armor=9, fire=0.5, earth=1, energy=0.8, ice=1, holy=1.1, death=0.8, physical=1, drown=1)
elf_arcanist.setExperience(175)
elf_arcanist.setSpeed(230)
elf_arcanist.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=0, targetDistance=4, runOnHealth=0)
elf_arcanist.walkAround(energy=1, fire=1, poison=1)
elf_arcanist.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=0)
elf_arcanist.voices("I'll bring balance upon you!", "Vihil Ealuel", "For the Daughter of the Stars!", "Tha'shi Cenath", "Feel my wrath!")
elf_arcanist.regMelee(35)