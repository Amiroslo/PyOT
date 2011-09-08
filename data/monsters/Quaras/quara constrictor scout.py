import game.monster

quara_constrictor_scout = game.monster.genMonster("Quara Constrictor Scout", (46, 6065), "a quara constrictor scout")
quara_constrictor_scout.setHealth(450)
quara_constrictor_scout.bloodType(color="blood")
quara_constrictor_scout.setDefense(armor=15, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=1, physical=1, drown=0)
quara_constrictor_scout.setExperience(200)
quara_constrictor_scout.setSpeed(290)
quara_constrictor_scout.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=20)
quara_constrictor_scout.walkAround(energy=1, fire=0, poison=1)
quara_constrictor_scout.setImmunity(paralyze=1, invisible=0, lifedrain=0, drunk=1)
quara_constrictor_scout.voices("Boohaa!", "Tssss!", "Gluh! Gluh!", "Gaaahhh!")
quara_constrictor_scout.regMelee(130) #or more