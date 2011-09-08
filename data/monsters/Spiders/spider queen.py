import game.monster

spider_queen = game.monster.genMonster("Spider Queen", (219, 5995), "a spider queen")
spider_queen.setHealth(225)
spider_queen.bloodType(color="slime")
spider_queen.setDefense(-1)
spider_queen.setExperience(120)
spider_queen.setSpeed(280)
spider_queen.setBehavior(summonable=0, hostile=1, illusionable=1, convinceable=0, pushable=0, pushItems=1, pushCreatures=0, targetDistance=1, runOnHealth=0)
spider_queen.walkAround(energy=0, fire=0, poison=0)
spider_queen.setImmunity(paralyze=0, invisible=0, lifedrain=0, drunk=0)