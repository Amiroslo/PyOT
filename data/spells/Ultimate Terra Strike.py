instant = spell.Spell("Ultimate Terra Strike", "exori max tera", icon=157, group=ATTACK_GROUP)
instant.require(mana=100, level=90, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(30, 4)
instant.targetEffect(callback=spell.damage(4.5, 7.3, 35, 55, EARTH))
instant.effects() # TODO