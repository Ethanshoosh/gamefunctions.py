import json
import gamefunctions

def save_game(filename, inventory, gold, hp, equipped_weapon):
    """
    Save the current game state to a file.
    
    Args:
        filename (str): The file name to save the game.
        inventory (list): The player's inventory.
        gold (int): The player's current gold.
        hp (int): The player's current HP.
        equipped_weapon (dict or None): The currently equipped weapon.
    """
    game_data = {
        "inventory": inventory,
        "gold": gold,
        "hp": hp,
        "equipped_weapon": equipped_weapon
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
        tuple: The loaded inventory, gold, HP, and equipped weapon.
    """
    try:
        with open(filename, 'r') as f:
            game_data = json.load(f)
            inventory = game_data.get("inventory", [])
            gold = game_data.get("gold", 100)
            hp = game_data.get("hp", 30)
            equipped_weapon = game_data.get("equipped_weapon", None)
        print(f"Game loaded from {filename}.")
        return inventory, gold, hp, equipped_weapon
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return [], 100, 30, None
    except json.JSONDecodeError:
        print("Error loading the game file. Starting a new game.")
        return [], 100, 30, None

def display_inventory(inventory, equipped_weapon):
    """
    Display the player's inventory with equipped status.
    
    Args:
        inventory (list): The player's inventory.
        equipped_weapon (dict or None): The currently equipped weapon.
    """
    print("Your inventory:")
    for item in inventory:
        status = ""
        if item == equipped_weapon:
            status = " (Equipped)"
        print(f"- {item['name']} (Type: {item['type']}){status}")

def equip_item(inventory, item_name):
    """
    Equip a weapon from the inventory.
    
    Args:
        inventory (list): The player's inventory.
        item_name (str): The name of the item to equip.
    
    Returns:
        dict or None: The equipped item, or None if not successful.
    """
    for item in inventory:
        if item["name"] == item_name:
            if item["type"] == "weapon":
                print(f"You have equipped the {item_name}.")
                return item
            else:
                print(f"{item_name} is not a weapon and cannot be equipped.")
                return None
    print(f"{item_name} is not in your inventory.")
    return None

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
            player_damage = gamefunctions.calculate_damage()
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

def main():
    """Main function to run the game."""
    inventory, gold, hp, equipped_weapon = [], 100, 30, None
    shop_items = [
        {"name": "Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "damage": 5, "cost": 50},
        {"name": "Magic Potion", "type": "consumable", "effect": "defeat monster", "consumed": False, "cost": 30}
    ]

    print("Welcome to the Adventure Game!")
    load_choice = input("Would you like to (1) start a new game or (2) load a saved game? Enter 1 or 2: ")
    if load_choice == "2":
        inventory, gold, hp, equipped_weapon = load_game("savegame.json")

    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)

    while True:
        print(f"\nCurrent HP: {hp}, Current Gold: {gold}")
        print("What would you like to do?")
        print("1) Fight Monster")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) View Inventory")
        print("5) Save and Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")
        if choice == "1":
            monster = gamefunctions.new_random_monster()
            hp = fight_monster(monster, hp, equipped_weapon, inventory)
        elif choice == "2":
            if gold >= 5:
                gold -= 5
                hp = 30
                print("You slept and restored your HP to full.")
            else:
                print("Not enough gold to sleep!")
        elif choice == "3":
            inventory, gold = visit_shop(inventory, gold, shop_items)
        elif choice == "4":
            display_inventory(inventory, equipped_weapon)
        elif choice == "5":
            save_game("savegame.json", inventory, gold, hp, equipped_weapon)
            print("Thank you for playing! Goodbye.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
