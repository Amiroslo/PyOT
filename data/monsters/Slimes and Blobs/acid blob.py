import game.monster

acid_blob = game.monster.genMonster("Acid Blob", (314, 9962), "an acid blob")
acid_blob.setHealth(250)
acid_blob.bloodType(color="slime")
acid_blob.setDefense(armor=10, fire=1.1, earth=0, energy=1.1, ice=0.8, holy=1, death=0, physical=1, drown=1)
acid_blob.setExperience(250)
acid_blob.setSpeed(210)
acid_blob.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=0, targetDistance=1, runOnHealth=0)
acid_blob.walkAround(energy=1, fire=1, poison=0)
acid_blob.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
acid_blob.voices("Kzzchhhh")