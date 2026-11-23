from game.dice import Dice

def resolve_player_action(player, enemy, choice: int) -> str:
    if choice == 1:
        return player.attack(enemy)
    if choice == 2: 
        return player.defend()
    if choice == 3:
        return player.use_potion()
    return player.use_special(enemy)

def is_available(character, choice: int):
    return choice != 3 or bool(character.belt)

def choose_enemy_action(enemy) -> int:
    if enemy.hp <= enemy.max_hp * 0.3 and Dice.chance(25):
        return 2
    if Dice.chance(25):
        return 4
    return 1


def build_round_order(player, player_choice, enemy, enemy_choice):
    """Order every attack slot of the round by initiative.

    A combatant attacking with N attacks per round gets N slots; slot k scores
    `initiative / k`. Any other action takes a single slot at full initiative.

    Args:
        player (Character): the player's character.
        player_choice (int): what the player chose.
        enemy (Character): the opponent.
        enemy_choice (int): what the enemy chose.

    Returns:
        list: (actor, target, choice) triples, in the order they resolve.
    """
    slots = []
    for actor, target, choice in ((player, enemy, player_choice),
                                  (enemy, player, enemy_choice)):
        count = actor.attacks_per_round if choice == 1 else 1
        for rank in range(1, count + 1):
            slots.append((actor.initiative / rank, actor, target, choice))

    # Ties: the higher base initiative first, then the player.
    slots.sort(key=lambda slot: (-slot[0], -slot[1].initiative,
                                 0 if slot[1] is player else 1))
    return [(actor, target, choice) for _, actor, target, choice in slots]


def describe_last_exchange(actor, target):
    """Spell out the last blow, for a verbose log.

    Reads what the objects recorded about themselves, the actor's roll, the
    target's damage breakdown, rather than recomputing anything.

    Args:
        actor (Character): who acted.
        target (Character): who was on the receiving end.

    Returns:
        list: extra log lines, possibly empty.
    """
    lines = []
    roll = actor.last_roll
    if roll:
        verdict = "hit" if roll["hit"] else "missed"
        lines.append(f"   jet {roll['roll']} / CC {roll['target']} : {verdict}")
    hit = target.last_damage
    if hit:
        pierced = " (pierce armor)" if hit["pierced"] else ""
        lines.append(f"   raw {hit['raw']} - reduction {hit['reduction']}"
                     f"{pierced} = {hit['dealt']}")
    return lines


def play_round(player, player_choice, enemy, verbose=False):
    """Resolve one whole round and return the lines to log.

    Args:
        player (Character): the player's character.
        player_choice (int): 1 to 4.
        enemy (Character): the opponent.
        verbose (bool): when True, add the dice and damage breakdown.

    Returns:
        list: the lines describing what happened, in order.
    """
    enemy_choice = choose_enemy_action(enemy)

    player.defending = False
    enemy.defending = False

    lines = []
    for actor, target, choice in build_round_order(player, player_choice,
                                                   enemy, enemy_choice):
        if not (player.is_alive() and enemy.is_alive()):
            break
        target.last_damage = None
        lines.append(resolve_player_action(actor, target, choice))
        if verbose:
            lines.extend(describe_last_exchange(actor, target))
    return lines


def collect_spoils(winner, loser):
    """Move the loser's backpack into the winner's, then let the winner rest.

    There is no loot table anywhere: a creature hands over exactly what it was
    carrying, through the same `store` the hero uses.

    Args:
        winner (Character): who is still standing.
        loser (Character): who is not.

    Returns:
        list: the lines describing what was picked up.
    """
    lines = []
    for item in list(loser.backpack):
        if winner.store(item):
            lines.append(f"Loot : {item.name}.")
        else:
            lines.append(f"Bag is full: {item.name} stays on the ground.")
    winner.rest()
    return lines