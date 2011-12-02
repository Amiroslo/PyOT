conjure = spell.Spell("Avalanche", "adori mas frigo", icon=23, group=SUPPORT_GROUP)
conjure.require(mana=530, level=30, maglevel=0, soul=3, learned=0, vocations=(2, 6))
conjure.use(2260)
conjure.cooldowns(0, 3)
conjure.targetEffect(callback=spell.conjure(2274, 3))

# Incomplete!
rune = spell.Rune(2274, icon=115, count=3, target=TARGET_TARGET, group=ATTACK_GROUP)
rune.cooldowns(0, 2)
rune.area(AREA_CIRCLE3)
rune.require(mana=0, level=30, maglevel=0)
rune.targetEffect(callback=spell.damage(1.2, 2.85, 7, 16, ICE))
rune.effects(area=EFFECT_ICEAREA, shoot=ANIMATION_ICE) # TODO