instant = spell.Spell("Divine Caldera", "exevo mas san", icon=124, group=ATTACK_GROUP)
instant.require(mana=140, level=50, maglevel=0, learned=0, vocations=(3, 7))
instant.cooldowns(4, 2)
instant.targetEffect(callback=spell.damage(3.2, 4.8, 20, 30, HOLY))
instant.effects() # TODO