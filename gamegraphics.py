import random
import game

# Constants
GRID_SIZE = 10

# Initialize player, shop, and encounter positions
player_pos = [0, 0]
shop_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Ensure shop and encounter positions do not overlap
while shop_pos == encounter_pos:
    encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

def display_grid():
    """
    Display the grid with player, shop, and encounter positions.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if [x, y] == player_pos:
                print("P", end=" ")  # Player
            elif [x, y] == shop_pos:
                print("S", end=" ")  # Shop
            elif [x, y] == encounter_pos:
                print("E", end=" ")  # Encounter
            else:
                print(".", end=" ")  # Empty space
        print()  # Newline after each row
    print("\nUse W (up), A (left), S (down), D (right) to move. Q to quit.")

def handle_shop():
    """
    Handle interactions with the shop.
    """
    print("You entered the shop! Here are the items available:")
    inventory, gold = game.visit_shop([], 100, [
        {"name": "Sword", "type": "weapon", "damage": 5, "cost": 50},
        {"name": "Health Potion", "type": "consumable", "effect": "heal", "cost": 20}
    ])
    print(f"Your updated inventory: {inventory}, Gold: {gold}")

def handle_encounter():
    """
    Handle random encounter interactions.
    """
    print("A wild monster appeared! Prepare for battle!")
    monster = game.new_random_monster()
    player_hp = game.fight_monster(monster, 30, None, [])
    print(f"Your updated HP: {player_hp}")

def move_player(direction):
    """
    Move the player based on the input direction.
    
    Args:
        direction (str): Direction to move ('w', 'a', 's', 'd').
    """
    global player_pos
    if direction == "w" and player_pos[1] > 0:
        player_pos[1] -= 1
    elif direction == "s" and player_pos[1] < GRID_SIZE - 1:
        player_pos[1] += 1
    elif direction == "a" and player_pos[0] > 0:
        player_pos[0] -= 1
    elif direction == "d" and player_pos[0] < GRID_SIZE - 1:
        player_pos[0] += 1

def main():
    """
    Main function to run the text-based game.
    """
    print("Welcome to the Adventure Game!")
    print("Navigate the grid to explore the shop (S) or encounter enemies (E).")
    
    while True:
        display_grid()
        action = input("Enter your move (w/a/s/d to move, q to quit): ").lower()

        if action == "q":
            print("Thanks for playing! Goodbye.")
            break

        if action in ["w", "a", "s", "d"]:
            move_player(action)

            # Check for interactions
            if player_pos == shop_pos:
                handle_shop()
            elif player_pos == encounter_pos:
                handle_encounter()
        else:
            print("Invalid input. Please use w/a/s/d to move or q to quit.")

if __name__ == "__main__":
    main()
set
