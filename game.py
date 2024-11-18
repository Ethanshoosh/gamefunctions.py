import json
import gamefunctions

# Initialize inventory and shop items
inventory = []
shop_items = [
    {"name": "Sword", "type": "weapon", "maxDurability": 10, "currentDurability": 10, "damage": 5, "cost": 50},
    {"name": "Magic Potion", "type": "consumable", "effect": "defeat monster", "consumed": False, "cost": 30}
]

def save_game(filename="savegame.json"):
    """Save the current game state to a file."""
    game_data = {
        "inventory": inventory,
        "gold": current_gold
    }
    
    with open(filename, 'w') as f:
        json.dump(game_data, f, indent=4)
    print(f"Game saved to {filename}.")

def load_game(filename="savegame.json"):
    """Load the game state from a file."""
    global inventory, current_gold
    try:
        with open(filename, 'r') as f:
            game_data = json.load(f)
            inventory = game_data.get("inventory", [])
            current_gold = game_data.get("gold", 100)
        print(f"Game loaded from {filename}.")
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
    except json.JSONDecodeError:
        print("Error loading the game file. Starting a new game.")

def main():
    global current_hp, current_gold, inventory
    current_hp = 30
    current_gold = 100

    # Start or load game
    print("Welcome to the Adventure Game!")
    load_choice = input("Would you like to (1) start a new game or (2) load a saved game? Enter 1 or 2: ")
    
    if load_choice == "2":
        filename = input("Enter the save filename: ")
        load_game(filename)
    elif load_choice != "1":
        print("Invalid choice, starting a new game.")
    
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    # Main game loop
    while True:
        print(f"\nCurrent HP: {current_hp}, Current Gold: {current_gold}")
        print("What would you like to do?")
        print("1) Fight Monster")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) View Inventory")
        print("5) Save and Quit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice == "1":
            # Encounter a monster
            monster = gamefunctions.new_random_monster()
            monster_hp = monster['health']
            print(f"\nYou encounter {monster['name']}! {monster['description']}")
            
            # Check for magic potion
            if any(item['name'] == "Magic Potion" and not item["consumed"] for item in inventory):
                use_potion = input("You have a Magic Potion. Use it to defeat the monster instantly? (y/n): ").lower()
                if use_potion == "y":
                    for item in inventory:
                        if item["name"] == "Magic Potion":
                            item["consumed"] = True
                    print("You used the Magic Potion and defeated the monster instantly!")
                    continue

            # Combat loop
            while monster_hp > 0 and current_hp > 0:
                print("\nChoose your action:")
                print("1) Attack")
                print("2) Flee")
                action = input("Enter your choice (1/2): ")
                
                if action == "1":
                    # Player attacks
                    player_damage = gamefunctions.calculate_damage()
                    monster_hp -= player_damage
                    print(f"You deal {player_damage} damage to the {monster['name']}. Monster HP is now {monster_hp}.")
                    
                    if monster_hp > 0:
                        monster_damage = monster['power']
                        current_hp -= monster_damage
                        print(f"The {monster['name']} strikes back for {monster_damage} damage! Your HP is now {current_hp}.")
                
                elif action == "2":
                    print("You flee from the battle.")
                    break
                else:
                    print("Invalid action, please choose again.")
            
            if current_hp <= 0:
                print("You have been defeated. Game over!")
                break
            elif monster_hp <= 0:
                print(f"You defeated the {monster['name']}!")
        
        elif choice == "2":
            # Sleep to restore HP
            if current_gold >= 5:
                current_gold -= 5
                current_hp = 30
                print("You slept and restored your HP to full.")
            else:
                print("Not enough gold to sleep!")
        
        elif choice == "3":
            # Visit shop
            print("Welcome to the shop! Here are the available items:")
            for i, item in enumerate(shop_items, 1):
                print(f"{i}) {item['name']} - Cost: {item['cost']} Gold")
            
            item_choice = input("Enter the number of the item you want to purchase (or 'q' to quit): ")
            if item_choice.isdigit():
                item_choice = int(item_choice) - 1
                if 0 <= item_choice < len(shop_items):
                    item = shop_items[item_choice]
                    if current_gold >= item['cost']:
                        current_gold -= item['cost']
                        inventory.append(item.copy())
                        print(f"Purchased {item['name']}!")
                    else:
                        print("Not enough gold to buy this item.")
            else:
                print("Exiting shop.")
        
        elif choice == "4":
            # View inventory
            display_inventory()
            equip_item_prompt()
        
        elif choice == "5":
            # Save and quit
            save_choice = input("Enter filename to save your game (default is 'savegame.json'): ") or "savegame.json"
            save_game(save_choice)
            print("Thank you for playing! Goodbye.")
            break
        
        else:
            print("Invalid choice, please try again.")

def display_inventory():
    print("Your inventory:")
    for item in inventory:
        print(f"- {item['name']} (Type: {item['type']})")

def equip_item_prompt():
    item_type = input("Enter the type of item to equip (e.g., 'weapon'): ")
    equippable_items = get_equippable_items(inventory, item_type)
    
    if not equippable_items:
        print("No items of this type to equip.")
    else:
        for i, item in enumerate(equippable_items, 1):
            print(f"{i}) {item['name']}")
        
        choice = input("Enter the number of the item to equip (or 'q' to cancel): ")
        if choice.isdigit():
            choice = int(choice) - 1
            if 0 <= choice < len(equippable_items):
                equipped_item = equip_item(equippable_items[choice]['name'])
                if equipped_item:
                    print(f"Equipped {equipped_item['name']} successfully!")

def get_equippable_items(inventory, item_type):
    return [item for item in inventory if item['type'] == item_type]

def equip_item(item_name):
    for item in inventory:
        if item['name'] == item_name:
            if item['type'] in ["weapon", "shield"]:
                print(f"You have equipped the {item_name}.")
                return item
            else:
                print(f"{item_name} cannot be equipped.")
                return None
    print(f"{item_name} is not in your inventory.")
    return None

if __name__ == "__main__":
    main()

