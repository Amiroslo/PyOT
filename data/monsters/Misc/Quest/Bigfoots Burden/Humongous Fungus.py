humongous_fungus = game.monster.genMonster("Humongous Fungus", (488, 18382), "a humongous fungus")#mostly unkniown including corpse(may be right)
humongous_fungus.setHealth(3400, healthmax=3400)
humongous_fungus.bloodType(color="blood")
humongous_fungus.setDefense(armor=40, fire=0.95, earth=0, energy=0.85, ice=0.85, holy=0.95, death=0.65, physical=1, drown=1)
humongous_fungus.setExperience(2600)
humongous_fungus.setSpeed(500)
humongous_fungus.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
humongous_fungus.walkAround(energy=0, fire=0, poison=0)
humongous_fungus.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
humongous_fungus.voices("Munch munch munch!")
humongous_fungus.regMelee(330)