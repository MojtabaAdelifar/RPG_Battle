from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# instantiate black magics
fire = Spell("Fire", 30, 1000, "black")
thunder = Spell("Thunder", 30, 1000, "black")
blizzard = Spell("Blizzard", 35, 1000, "black")
meteor = Spell("Meteor", 50, 2000, "black")
quake = Spell("Quake", 20, 1400, "black")

# instantiate white magics
cure = Spell("Cure", 50, 1200, "white")
cura = Spell("Cura", 80, 2000, "white")
curegara = Spell("Curegara", 100, 5000, "white")


# create some items
potion = Item("Potion", "potion", "Heals 50 HP", 500, 15)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 1000, 5)
superpotion = Item("SuperPotion", "potion", "Heals 500 HP", 5000, 5)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one member party", 10000, 2)
megaelixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 10000, 5)
grenade = Item("Grenade", "attack", "Deals 500 damge", 5000, 3)


player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [potion, hipotion, superpotion, elixer, megaelixer, grenade]
enemy_spells = [fire, thunder, curegara]
enemy_items = [superpotion, grenade]

# declare characters in the game
player1 = Person("Luna", 3040, 100, 2000, 35, player_spells, player_items)
player2 = Person("Lina", 2000, 400, 3000, 40, player_spells, player_items)
player3 = Person("Garo", 4210, 205, 4000, 45, player_spells, player_items)


# create enemies
enemy1 = Person("Razor", 4000, 200, 5000, 225, enemy_spells, enemy_items)
enemy2 = Person("Robb ", 5000, 100, 2000, 100, enemy_spells, enemy_items)
enemy3 = Person("zero ", 7000, 150, 4000, 50, enemy_spells, enemy_items)


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]


running = True
i = 0

while running:

    print("Name                        HP                                               MP")
    # get HP and MP
    for player in players:
            player.get_stats()

    print("\n")
    # get enemies HP/MP
    for enemy in enemies:
            enemy.get_enemy_stats()

    for player in players:
        print("\n" + bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)
        print("===================")

        if player.hp == 0:
            del player

        else:
            # get a list of actions (1. Attack, 2. Magic, 3. Item)
            player.choose_action()
            choice = input("Enter the action:")
            index = int(choice) - 1

            # choose the enemy target
            enemy = player.choose_enemy(enemies)

            if index == 0:
                dmg = player.generate_damage()
                enemies[enemy].take_damage(dmg)
                print(player.name + " attacked for " + enemies[enemy].name.replace(" ", ""), str(dmg),
                      "points of damgae")

            elif index == 1:
                player.choose_spell()
                magic_choice = int(input("Choose magic:")) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                player.reduce_mp(spell.cost)
                current_mp = player.get_mp()

                if current_mp < spell.cost:
                    print(bcolors.FAIL + "Magic point is not enough" + bcolors.ENDC)
                    continue

                magic_dmg = spell.generate_spell_dmg()

                if spell.type == "white":
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + '\n' + spell.name + " heals for " + str(magic_dmg) + " HP" + bcolors.ENDC)

                elif spell.type == "black":
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + " deals for " + str(magic_dmg) + " points of dmg to " + enemies[
                        enemy].name + bcolors.ENDC)

            elif index == 2:
                player.choose_item()
                item_choice = int(input("Choose item: ")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]

                if item.quantity == 0:
                    print(bcolors.FAIL + "\n" + " None left..." + bcolors.ENDC)
                    continue

                item.quantity = item.quantity - 1

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + bcolors.ENDC)

                elif item.type == "elixer":
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores player HP/MP" + bcolors.ENDC)

                elif item.type == "attack":
                    enemies[enemy].take_damage(item.prop)
                    print(bcolors.FAIL + "\n" + item.name + " deals for " + str(
                        item.prop) + " points of damage to " + enemies[enemy].name + bcolors.ENDC)

    for enemy in enemies:

        if enemy.hp == 0:
            del enemy
        else:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks for " + players[target].name,
                  str(enemy_dmg) + " points of damage ")

    defeated_players = 0
    defeated_enemies = 0

    for player in players:
        if player.hp == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.hp == 0:
            defeated_enemies += 1

    if defeated_players == 3:
        print(bcolors.FAIL + "The enemy has won!" + bcolors.ENDC)
        running = False

    elif defeated_enemies == 3:
        print(bcolors.OKGREEN + "You have won!" + bcolors.ENDC)
        running = False
