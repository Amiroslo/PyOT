instant = spell.Spell("Cure Bleeding", "exana kor", icon=144, target=TARGET_SELF, group=HEALING_GROUP)
instant.require(mana=30, level=30, maglevel=0, learned=0, vocations=(4, 8))
instant.cooldowns(6, 1)
instant.targetEffect(callback=spell.heal(0, 0, 1, 1, cure=game.enum.PHYSICAL)) #physical or melee?
instant.effects(caster=EFFECT_MAGIC_BLUE)