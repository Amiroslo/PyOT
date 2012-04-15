lich = game.monster.genMonster(_("Lich"), (99, 6028), _("a lich"))
lich.setHealth(880)
lich.bloodType(color="undead")
lich.setDefense(armor=55, fire=1, earth=0, energy=0.2, ice=1, holy=1.2, death=0, physical=1, drown=1)
lich.setExperience(900)
lich.setSpeed(320)
lich.setBehavior(summonable=0, hostile=1, illusionable=0, convinceable=0, pushable=0, pushItems=1, pushCreatures=1, targetDistance=1, runOnHealth=0)
lich.walkAround(energy=0, fire=1, poison=0)
lich.setImmunity(paralyze=1, invisible=1, lifedrain=1, drunk=0)
lich.voices("Doomed be the living!", "Death awaits all!", "Thy living flesh offends me!", "Death and Decay!", "You will endure agony beyond thy death!", "Pain sweet pain!", "Come to me my children!")
lich.summon("bonebeast", 10)
lich.maxSummons(4)
lich.regMelee(75)
lich.loot( (2148, 100, 120), ("dirty cape", 18.75), ("staff", 61.5), ("black pearl", 5.25), ("ring of healing", 1.0), ("spellbook", 9.5), ("white pearl", 2.5), ("mind stone", 0.5), ("castle shield", 0.25), ("platinum amulet", 0.0025), ("strange helmet", 0.25), ("strong mana potion", 0.5), ("blue robe", 0.0025) )