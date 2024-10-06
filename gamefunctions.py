import random

def purchase_item(itemPrice: float, startingMoney: float, quantityToPurchase: int = 1):
    total_cost = itemPrice * quantityToPurchase
    if total_cost > startingMoney:
        quantityToPurchase = int(startingMoney // itemPrice)
        total_cost = itemPrice * quantityToPurchase
    remaining_money = startingMoney - total_cost
    return quantityToPurchase, remaining_money


def new_random_monster():
  
    monster_options = [
        {
            'name': 'A goblin',
            'description': 'This is a lonely lonely goblin. When it sees you, it rushes at you quickly with a sharp dagger in hand.',
            'health_range': (1, 5),
            'power_range': (5, 15),
            'money_range': (10, 50)
        },
        {
            'name': 'Vulture',
            'description': 'You discover a vulture eating the remains of two goblins that appear to have killed each other. They were carrying a chest that contains a small treasure horde.',
            'health_range': (1, 2),
            'power_range': (2, 10),
            'money_range': (100, 200)
        },
        {
            'name': 'Dragon',
            'description': 'A powerful dragon blocks your path, its fiery breath warming the air around you.',
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

print(purchase_item(1.23, 10, 3))
print(purchase_item(1.23, 2.01, 3)) 
print(purchase_item(3.41, 21.12))

print(new_random_monster())
print(new_random_monster())
print(new_random_monster())
