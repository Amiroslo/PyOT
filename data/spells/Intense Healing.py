instant = spell.Spell("Intense Healing", "exura gran", icon=2, target=TARGET_SELF, group=HEALING_GROUP)
instant.require(mana=70, level=11, maglevel=0, learned=0, vocations=(1, 2, 3, 5, 6, 7))
instant.cooldowns(1, 1)
instant.effects(caster=EFFECT_MAGIC_BLUE)
instant.targetEffect(callback=spell.heal(3.2, 5.4, 20, 40))