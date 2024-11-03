import gamefunctions

def main():
    # Initialize player stats
    current_hp = 30
    current_gold = 10
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    # Display shop menu
    gamefunctions.print_shop_menu("Sword", 50.0, "Shield", 35.0)
    
    while True:
        print(f"\nCurrent HP: {current_hp}, Current Gold: {current_gold}")
        print("What would you like to do?")
        print("1) Fight Monster")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            # Initialize monster
            monster = gamefunctions.new_random_monster()
            monster_hp = monster['health']
            print(f"\nYou encounter {monster['name']}! {monster['description']}")
            
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
                    
                    # Monster attacks if it's still alive
                    if monster_hp > 0:
                        monster_damage = monster['power']
                        current_hp -= monster_damage
                        print(f"The {monster['name']} strikes back for {monster_damage} damage! Your HP is now {current_hp}.")
                
                elif action == "2":
                    print("You flee from the battle.")
                    break
                else:
                    print("Invalid action, please choose again.")
            
            # Check if the combat ended with player or monster defeat
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
            print("Thank you for playing! Goodbye.")
            break
        
        else:
            print("Invalid choice, please try again.")
    
    # Simulate purchasing an item
    quantity, remaining_money = gamefunctions.purchase_item(50.0, 100.0, 1)
    print(f"Purchased {quantity} item(s), remaining money: ${remaining_money:.2f}")

if __name__ == "__main__":
    main()
