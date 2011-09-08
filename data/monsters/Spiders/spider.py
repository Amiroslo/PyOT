import game.monster

spider = game.monster.genMonster("Spider", (30, 5961), "a spider")
spider.setHealth(20)
spider.bloodType(color="slime")
spider.setDefense(armor=2, fire=1.2, earth=1, energy=1, ice=1, holy=1, death=1, physical=1, drown=1)
spider.setExperience(12)
spider.setSpeed(152)
spider.setBehavior(summonable=210, hostile=1, illusionable=1, convinceable=210, pushable=1, pushItems=0, pushCreatures=0, targetDistance=1, runOnHealth=6)
spider.walkAround(energy=1, fire=1, poison=1)
spider.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)
spider.regMelee(25)