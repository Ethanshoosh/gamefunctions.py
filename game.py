import gamefunctions

def main():
    # Prompt for the player's name and print a welcome message
    current_hp = 30
    current_gold = 10
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)
    
    # Display a shop menu
    gamefunctions.print_shop_menu("Sword", 50.0, "Shield", 35.0)
    
    while True:
        print(f"\nCurrent HP: {current_hp}, Current Gold: {current_gold}")
        print("What would you like to do?")
        print("1) Fight Monster")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            monster = gamefunctions.new_random_monster()
            print(f"\nYou encounter {monster['name']}! {monster['description']}")
            current_hp -= monster['power']
            print(f"The {monster['name']} deals {monster['power']} damage! Your HP is now {current_hp}.")
            
            if current_hp <= 0:
                print("You have been defeated. Game over!")
                break
        
        elif choice == "2":
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
