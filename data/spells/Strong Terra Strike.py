instant = spell.Spell("Strong Terra Strike", "exori gran tera", icon=153, group=ATTACK_GROUP)
instant.require(mana=60, level=70, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(8, 2)
instant.targetEffect(callback=spell.damage(2.8, 4.4, 16, 28, EARTH))
instant.effects() # TODO