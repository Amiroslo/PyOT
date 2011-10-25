
quara_hydromancer_scout = game.monster.genMonster("Quara Hydromancer Scout", (47, 6066), "a quara hydromancer scout")
quara_hydromancer_scout.setHealth(1100)
quara_hydromancer_scout.bloodType(color="blood")
quara_hydromancer_scout.setDefense(armor=14, fire=0, earth=1.1, energy=1.1, ice=0, holy=1, death=1, physical=1, drown=0)
quara_hydromancer_scout.setExperience(800)
quara_hydromancer_scout.setSpeed(280)
quara_hydromancer_scout.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=30)
quara_hydromancer_scout.walkAround(energy=1, fire=0, poison=1)
quara_hydromancer_scout.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=1)
quara_hydromancer_scout.voices("Qua hah tsh!", "Teech tsha tshul!", "Quara tsha Fach!", "Tssssha Quara!", "Blubber.", "Blup.")
quara_hydromancer_scout.regMelee(40) #poisons you 5 hp/turn##max melee could be wrong
quara_hydromancer_scout.loot( ("white pearl", 2.25), ("fish", 15.25, 2), ("small emerald", 1.25, 2), (2148, 100, 88), ("quara eye", 9.75), ("fish fin", 1.25, 3), ("black pearl", 1.75), ("wand of cosmic energy", 1.25), ("knight armor", 0.25), ("ring of healing", 0.5) )