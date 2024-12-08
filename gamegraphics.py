import pygame
import random
import game  # Assuming you have the `game` module from the previous iterations

# Constants
GRID_SIZE = 10
SQUARE_SIZE = 32
WINDOW_SIZE = GRID_SIZE * SQUARE_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Adventure Game with Monsters")

# Initial positions
player_pos = [0, 0]
shop_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Ensure shop and encounter positions do not overlap
while shop_pos == encounter_pos:
    encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

class WanderingMonster:
    def __init__(self):
        """
        Initialize a wandering monster at a random location on the grid.
        """
        self.position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    
    def move(self):
        """
        Move the monster in a random direction, if within bounds.
        """
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and self.position[1] > 0:
            self.position[1] -= 1
        elif direction == "down" and self.position[1] < GRID_SIZE - 1:
            self.position[1] += 1
        elif direction == "left" and self.position[0] > 0:
            self.position[0] -= 1
        elif direction == "right" and self.position[0] < GRID_SIZE - 1:
            self.position[0] += 1

# List of monsters
monsters = [WanderingMonster()]

def draw_grid():
    """
    Draw the grid and objects (player, shop, encounter, monsters).
    """
    screen.fill(WHITE)

    # Draw grid lines
    for x in range(0, WINDOW_SIZE, SQUARE_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, SQUARE_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WINDOW_SIZE, y))

    # Draw shop
    pygame.draw.circle(screen, GREEN, (shop_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                       shop_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    # Draw encounter
    pygame.draw.circle(screen, RED, (encounter_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                      encounter_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * SQUARE_SIZE, player_pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw monsters
    for monster in monsters:
        monster_rect = pygame.Rect(monster.position[0] * SQUARE_SIZE, monster.position[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, PURPLE, monster_rect)

def handle_shop():
    """
    Handle interactions with the shop.
    """
    print("You entered the shop!")
    game.visit_shop([], 100, [
        {"name": "Sword", "type": "weapon", "damage": 5, "cost": 50},
        {"name": "Health Potion", "type": "consumable", "effect": "heal", "cost": 20}
    ])

def handle_encounter():
    """
    Handle random encounter interactions.
    """
    print("A wild monster appeared!")
    monster = game.new_random_monster()
    game.fight_monster(monster, 30, None, [])

def check_monster_encounter():
    """
    Check if the player and a monster are in the same position, triggering an encounter.
    """
    global monsters
    for monster in monsters:
        if player_pos == monster.position:
            print("You encountered a monster! Fighting...")
            game.fight_monster(game.new_random_monster(), 30, None, [])
            monsters.remove(monster)

def move_player(key):
    """
    Update player position based on key input and trigger events.
    """
    if key == pygame.K_UP and player_pos[1] > 0:
        player_pos[1] -= 1
    elif key == pygame.K_DOWN and player_pos[1] < GRID_SIZE - 1:
        player_pos[1] += 1
    elif key == pygame.K_LEFT and player_pos[0] > 0:
        player_pos[0] -= 1
    elif key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE - 1:
        player_pos[0] += 1

    # Check for interactions
    if player_pos == shop_pos:
        handle_shop()
    elif player_pos == encounter_pos:
        handle_encounter()
    else:
        check_monster_encounter()

def spawn_monsters():
    """
    Spawn two new monsters at random positions.
    """
    for _ in range(2):
        monsters.append(WanderingMonster())

def main():
    """
    Main game loop.
    """
    running = True
    clock = pygame.time.Clock()
    move_counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                else:
                    move_player(event.key)
                    move_counter += 1

                    # Move monsters every other player move
                    if move_counter % 2 == 0:
                        for monster in monsters:
                            monster.move()
        
        # If all monsters are gone, spawn new ones
        if not monsters:
            spawn_monsters()

        draw_grid()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

