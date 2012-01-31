worker_golem = game.monster.genMonster("Worker Golem", (304, 9801), "a worker golem")
worker_golem.setHealth(1470, healthmax=1470)
worker_golem.bloodType(color="blood")
worker_golem.setDefense(armor=37, fire=1, earth=0.5, energy=1.05, ice=0.9, holy=0.5, death=0.9, physical=0.9, drown=1)
worker_golem.setExperience(1250)
worker_golem.setSpeed(270)
worker_golem.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
worker_golem.walkAround(energy=1, fire=1, poison=0)
worker_golem.setImmunity(paralyze=1, invisible=1, lifedrain=0, drunk=0)
worker_golem.voices("INTRUDER ALARM!", "klonk klonk klonk", "Rrrtttarrrttarrrtta", "Awaiting orders.", "Secret objective complete.")
worker_golem.regMelee(240)
worker_golem.loot( ("gear wheel", 1.0), (2148, 100, 140), ("nail", 16.25, 5), ("gear crystal", 2.0), ("war hammer", 1.0), ("small diamond", 1.5, 2), ("great health potion", 2.0), ("iron ore", 1.25, 3), ("life crystal", 1.0), ("crystal pedestal", 0.25), ("berserk potion", 1.0), ("rusty armor", 1.5), ("great spirit potion", 0.75), ("rusty legs", 1.25), ("great mana potion", 1.5), ("might ring", 0.5), ("bonebreaker", 0.0025), ("spiked squelcher", 0.75) )