
import json
import random

def save_game(filename, inventory, gold, hp, equipped_weapon, player_pos):
    """
    Save the current game state to a file.
    
    Args:
        filename (str): The file name to save the game.
        inventory (list): The player's inventory.
        gold (int): The player's current gold.
        hp (int): The player's current HP.
        equipped_weapon (dict or None): The currently equipped weapon.
        player_pos (list): The player's current position on the grid.
    """
    game_data = {
        "inventory": inventory,
        "gold": gold,
        "hp": hp,
        "equipped_weapon": equipped_weapon,
        "player_pos": player_pos
    }
    with open(filename, 'w') as f:
        json.dump(game_data, f, indent=4)
    print(f"Game saved to {filename}.")

def load_game(filename):
    """
    Load the game state from a file.
    
    Args:
        filename (str): The file name to load the game.
    
    Returns:
        tuple: The loaded inventory, gold, HP, equipped weapon, and player position.
    """
    try:
        with open(filename, 'r') as f:
            game_data = json.load(f)
            inventory = game_data.get("inventory", [])
            gold = game_data.get("gold", 100)
            hp = game_data.get("hp", 30)
            equipped_weapon = game_data.get("equipped_weapon", None)
            player_pos = game_data.get("player_pos", [0, 0])
        print(f"Game loaded from {filename}.")
        return inventory, gold, hp, equipped_weapon, player_pos
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return [], 100, 30, None, [0, 0]
    except json.JSONDecodeError:
        print("Error loading the game file. Starting a new game.")
        return [], 100, 30, None, [0, 0]

def visit_shop(inventory, gold, shop_items):
    """
    Handle shop interactions.
    
    Args:
        inventory (list): The player's inventory.
        gold (int): The player's current gold.
        shop_items (list): Items available in the shop.
    
    Returns:
        tuple: Updated inventory and gold after shopping.
    """
    print("Welcome to the shop! Here are the available items:")
    for i, item in enumerate(shop_items, 1):
        print(f"{i}) {item['name']} - Cost: {item['cost']} Gold")
    item_choice = input("Enter the number of the item you want to purchase (or 'q' to quit): ")
    if item_choice.isdigit():
        item_choice = int(item_choice) - 1
        if 0 <= item_choice < len(shop_items):
            item = shop_items[item_choice]
            if gold >= item['cost']:
                gold -= item['cost']
                inventory.append(item.copy())
                print(f"Purchased {item['name']}!")
            else:
                print("Not enough gold to buy this item.")
        else:
            print("Invalid choice.")
    else:
        print("Exiting shop.")
    return inventory, gold

def fight_monster(monster, hp, equipped_weapon, inventory):
    """
    Handle a monster encounter and combat.
    
    Args:
        monster (dict): The monster to fight.
        hp (int): The player's current HP.
        equipped_weapon (dict or None): The equipped weapon.
        inventory (list): The player's inventory.
    
    Returns:
        int: Updated HP after the battle.
    """
    monster_hp = monster['health']
    print(f"\nYou encounter {monster['name']}! {monster['description']}")

    # Check for Magic Potion
    if any(item['name'] == "Magic Potion" and not item["consumed"] for item in inventory):
        use_potion = input("You have a Magic Potion. Use it to defeat the monster instantly? (y/n): ").lower()
        if use_potion == "y":
            for item in inventory:
                if item["name"] == "Magic Potion":
                    item["consumed"] = True
            print("You used the Magic Potion and defeated the monster instantly!")
            return hp

    # Combat loop
    while monster_hp > 0 and hp > 0:
        print("\nChoose your action:")
        print("1) Attack")
        print("2) Flee")
        action = input("Enter your choice (1/2): ")

        if action == "1":
            # Player attacks
            player_damage = calculate_damage()
            if equipped_weapon:
                player_damage += equipped_weapon["damage"]
            monster_hp -= player_damage
            print(f"You deal {player_damage} damage to the {monster['name']}. Monster HP is now {monster_hp}.")

            if monster_hp > 0:
                monster_damage = monster['power']
                hp -= monster_damage
                print(f"The {monster['name']} strikes back for {monster_damage} damage! Your HP is now {hp}.")
        
        elif action == "2":
            print("You flee from the battle.")
            return hp
        else:
            print("Invalid action, please choose again.")
    
    if hp <= 0:
        print("You have been defeated. Game over!")
    elif monster_hp <= 0:
        print(f"You defeated the {monster['name']}!")
    return hp

def new_random_monster():
    """
    Generate a random monster for encounters.
    
    Returns:
        dict: The randomly generated monster.
    """
    monsters = [
        {"name": "Goblin", "description": "A sneaky little creature.", "health": 20, "power": 5},
        {"name": "Orc", "description": "A big brute with a club.", "health": 30, "power": 8},
        {"name": "Dragon", "description": "A fearsome fire-breathing beast.", "health": 50, "power": 15}
    ]
    return random.choice(monsters)

def calculate_damage():
    """
    Calculate the damage dealt by the player.
    
    Returns:
        int: The calculated damage.
    """
    return random.randint(1, 5)
