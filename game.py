import gamefunctions

def main():
    # Prompt for the player's name and print a welcome message
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name)

    # Display a shop menu
    gamefunctions.print_shop_menu("Sword", 50.0, "Shield", 35.0)

    # Simulate purchasing an item
    quantity, remaining_money = gamefunctions.purchase_item(50.0, 100.0, 1)
    print(f"Purchased {quantity} item(s), remaining money: ${remaining_money:.2f}")

    # Generate and display a random monster
    monster = gamefunctions.new_random_monster()
    print(f"You encounter {monster['name']}! {monster['description']}")

if __name__ == "__main__":
    main()
