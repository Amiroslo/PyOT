instant = spell.Spell("Strong Ice Strike", "exori gran frigo", icon=152, target=TARGET_TARGET, group=ATTACK_GROUP)
instant.require(mana=60, level=80, maglevel=0, learned=0, vocations=(2, 6))
instant.cooldowns(8, 2)
instant.range(4)
instant.area(AREA_WAVE1)
instant.targetEffect(callback=spell.damage(2.8, 4.4, 16, 28, ICE))
instant.effects(area=EFFECT_ICEATTACK, shoot=ANIMATION_SMALLICE)