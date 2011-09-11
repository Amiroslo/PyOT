import game.scriptsystem
import game.engine
import game.enum

global foods
foods = {}
foods[2328] = (84, "Gulp.")
foods[2362] = (48, "Yum.")
foods[2666] = (180, "Munch.")
foods[2667] = (144, "Munch.")
foods[2668] = (120, "Mmmm.")
foods[2669] = (204, "Munch.")
foods[2670] = (48, "Gulp.")
foods[2671] = (360, "Chomp.")
foods[2672] = (720, "Chomp.")
foods[2673] = (60, "Yum.")
foods[2674] = (72, "Yum.")
foods[2675] = (156, "Yum.")
foods[2676] = (96, "Yum.")
foods[2677] = (12, "Yum.")
foods[2678] = (216, "Slurp.")
foods[2679] = (12, "Yum.")
foods[2680] = (24, "Yum.")
foods[2681] = (108, "Yum.")
foods[2682] = (240, "Yum.")
foods[2683] = (204, "Munch.")
foods[2684] = (60, "Crunch.")
foods[2685] = (72, "Munch.")
foods[2686] = (108, "Crunch.")
foods[2687] = (24, "Crunch.")
foods[2688] = (24, "Mmmm.")
foods[2689] = (120, "Crunch.")
foods[2690] = (72, "Crunch.")
foods[2691] = (96, "Crunch.")
foods[2695] = (72, "Gulp.")
foods[2696] = (108, "Smack.")
foods[2769] = (60, "Crunch.")
foods[2787] = (108, "Crunch.")
foods[2788] = (48, "Crunch.")
foods[2789] = (264, "Munch.")
foods[2790] = (360, "Crunch.")
foods[2791] = (108, "Crunch.")
foods[2792] = (72, "Crunch.")
foods[2793] = (144, "Crunch.")
foods[2794] = (36, "Crunch.")
foods[2795] = (432, "Crunch.")
foods[2796] = (300, "Crunch.")
foods[5097] = (48, "Yum.")
foods[5678] = (96, "Gulp.")
foods[6125] = (96, "Mmmm.")
foods[6278] = (120, "Mmmm.")
foods[6279] = (180, "Mmmm.")
foods[6393] = (144, "Mmmm.")
foods[6394] = (180, "Mmmm.")
foods[6501] = (240, "Mmmm.")
foods[6541] = (72, "Gulp.")
foods[6542] = (72, "Gulp.")
foods[6543] = (72, "Gulp.")
foods[6544] = (72, "Gulp.")
foods[6545] = (72, "Gulp.")
foods[6569] = (12, "Mmmm.")
foods[6574] = (60, "Mmmm.")
foods[7158] = (300, "Munch.")
foods[7159] = (180, "Munch.")
foods[7372] = (0, "Yummy.")
foods[7373] = (0, "Yummy.")
foods[7374] = (0, "Yummy.")
foods[7375] = (0, "Yummy.")
foods[7376] = (0, "Yummy.")
foods[7377] = (0, "Yummy.")
foods[7963] = (720, "Munch.")
foods[8838] = (120, "Gulp.")
foods[8839] = (60, "Yum.")
foods[8840] = (12, "Yum.")
foods[8841] = (12, "Urgh.")
foods[8842] = (84, "Munch.")
foods[8843] = (60, "Crunch.")
foods[8844] = (12, "Gulp.")
foods[8845] = (60, "Munch.")
foods[8847] = (132, "Yum.")
foods[9005] = (88, "Slurp.")
foods[9996] = (0, "Slurp.")
foods[10454] = (0, "Your head begins to feel better.")
foods[11136] = (120, "Mmmm.")
foods[11246] = (180, "Yum.")
foods[11370] = (36, "Urgh.")

def playerEat(creature, ticker=0, lastHP=0, lastMana=0):
    gainhp = creature.getVocation().health
    gainmana = creature.getVocation().mana
    
    
    if ticker == gainhp[1]:
        creature.modifyHealth(gainhp[0])
        lastHP = ticker
    
    if ticker == gainmana[1]:
        creature.modifyMana(gainmana[0])
        lastMana = ticker
        
    creature.regenerate -= 1
    ticker += 1
    if creature.regenerate >= 0:
        game.engine.safeCallLater(1, playerEat, creature, ticker, lastHP, lastMana)
    else:
        creature.regenerate = 0
    
def onUse(creature, thing, position, stackpos, **a):
    global foods
    if not foods[thing.itemId]:
        return

    duration = foods[thing.itemId][0]
    sound = foods[thing.itemId][1]
    thing.count -= 1
    if thing.count:
        creature.replaceItem(position, stackpos, thing)
    else:
        creature.removeItem(position, stackpos)
        
    if creature.regenerate:
        creature.regenerate += duration
        if creature.regenerate > 1500:
            creature.regenerate = max(creature.regenerate, 1500)
            creature.message("You are full.", game.enum.MSG_SPEAK_MONSTER_SAY)
        else:
            creature.message(sound, game.enum.MSG_SPEAK_MONSTER_SAY)
    else:
        creature.regenerate = duration
        playerEat(creature)
        creature.message(sound)
game.scriptsystem.reg('use', foods.keys(), onUse)
    