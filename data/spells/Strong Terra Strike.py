
instant = spell.Spell("Strong Terra Strike", "exori gran tera", icon=153, group=None)
instant.require(mana=60, level=70, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(8, 2)
instant.targetEffect() # TODO
instant.effects() # TODO