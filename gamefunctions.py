
"""
This module provides utility functions for a text-based RPG game, including
functions for purchasing items, generating random monsters, and printing 
menus and welcome messages.

Functions:
    - print_welcome: Displays a welcome message for the player.
    - print_shop_menu: Displays a shop menu with items and their prices.
    - purchase_item: Simulates purchasing an item and returns the result.
    - new_random_monster: Generates a random monster with attributes.

Typical usage example:
    import gamefunctions
    gamefunctions.print_welcome("Player")
"""

import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    """
    Simulates purchasing a certain quantity of items, given the item price and starting money.
    If unable to afford the full quantity, the maximum affordable quantity is purchased.
    
    Parameters:
        itemPrice (float): The price of a single item.
        startingMoney (float): The amount of money the buyer has.
        quantityToPurchase (int): The number of items the buyer wants to purchase (default is 1).
    
    Returns:
        tuple: A tuple containing the number of items purchased and the remaining money.
    """
    total_cost = itemPrice * quantityToPurchase
    if total_cost > startingMoney:
        quantityToPurchase = int(startingMoney // itemPrice)  # Only buy as many as can be afforded
        total_cost = itemPrice * quantityToPurchase
    remaining_money = startingMoney - total_cost
    return quantityToPurchase, remaining_money


def new_random_monster():
    """
    Generates a random monster with health, power, and money attributes.
    
    Returns:
        dict: A dictionary representing the monster with keys 'name', 'description', 
              'health', 'power', and 'money'.
    """
    monster_options = [
        {
            'name': 'A goblin',
            'description': 'A lonely goblin that attacks quickly with a dagger.',
            'health_range': (1, 5),
            'power_range': (5, 15),
            'money_range': (10, 50)
        },
        {
            'name': 'Vulture',
            'description': 'A vulture scavenging the remains of a battle.',
            'health_range': (1, 2),
            'power_range': (2, 10),
            'money_range': (100, 200)
        },
        {
            'name': 'Dragon',
            'description': 'A powerful dragon with fiery breath blocking your path.',
            'health_range': (50, 100),
            'power_range': (30, 50),
            'money_range': (500, 1000)
        }
    ]
    
    monster = random.choice(monster_options)
    health = random.randint(*monster['health_range'])
    power = random.randint(*monster['power_range'])
    money = round(random.uniform(*monster['money_range']), 2)
    
    return {
        'name': monster['name'],
        'description': monster['description'],
        'health': health,
        'power': power,
        'money': money
    }


def print_welcome(name: str, width: int = 20):
    """
    Prints a centered welcome message within a field of a given width.
    
    Parameters:
        name (str): The name to include in the welcome message.
        width (int): The total width of the message including padding (default is 20).
    
    Returns:
        None
    """
    message = f"Hello, {name}!"
    print(message.center(width))


def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float):
    """
    Prints a shop menu showing two items and their prices, with proper formatting.
    The prices are right-aligned with two decimal places, and the menu is surrounded by a border.
    
    Parameters:
        item1Name (str): The name of the first item.
        item1Price (float): The price of the first item.
        item2Name (str): The name of the second item.
        item2Price (float): The price of the second item.
    
    Returns:
        None
    """
    border = "/----------------------\\\\"
    menu_template = "| {name:<12} ${price:>6.2f} |"
    
    print(border)
    print(menu_template.format(name=item1Name, price=item1Price))
    print(menu_template.format(name=item2Name, price=item2Price))
    print("\\\\----------------------/")


def test_functions():
    """
    Tests all the functions in the module by calling them with sample inputs.
    
    Returns:
        None
    """
    print(purchase_item(1.23, 10, 3))
    print(purchase_item(1.23, 2.01, 3))
    print(purchase_item(3.41, 21.12))

    print(new_random_monster())
    print(new_random_monster())
    print(new_random_monster())

    print_welcome("Jeff")
    print_welcome("Ethan")
    print_welcome("Chris")

    print_shop_menu("Apple", 31, "Bag of Grapes", 1.234)
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
    print_shop_menu("Milk", 2.5, "Orange", 0.99)


if __name__ == "__main__":
    test_functions()
