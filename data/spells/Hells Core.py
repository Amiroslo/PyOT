instant = spell.Spell("Hells Core", "exevo gran mas flam", icon=24, group=ATTACK_GROUP)
instant.require(mana=1200, level=60, maglevel=0, learned=0, vocations=(1, 5))
instant.cooldowns(40, 4)
instant.targetEffect(callback=spell.damage(8, 12, 50, 75, FIRE))
instant.effects() # TODO