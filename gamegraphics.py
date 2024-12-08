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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Adventure Game")

# Initialize player, shop, and encounter positions
player_pos = [0, 0]
shop_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Ensure shop and encounter positions do not overlap
while shop_pos == encounter_pos:
    encounter_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

def draw_grid():
    """
    Draw the grid, player, shop, and encounter positions.
    """
    screen.fill(WHITE)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw shop
    pygame.draw.circle(screen, GREEN, (shop_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                       shop_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    # Draw encounter
    pygame.draw.circle(screen, RED, (encounter_pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                      encounter_pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)

    # Draw player
    player_rect = pygame.Rect(player_pos[0] * SQUARE_SIZE, player_pos[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, BLUE, player_rect)

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

def move_player(key):
    """
    Move the player based on the arrow key pressed.
    """
    if key == pygame.K_UP and player_pos[1] > 0:
        player_pos[1] -= 1
    elif key == pygame.K_DOWN and player_pos[1] < GRID_SIZE - 1:
        player_pos[1] += 1
    elif key == pygame.K_LEFT and player_pos[0] > 0:
        player_pos[0] -= 1
    elif key == pygame.K_RIGHT and player_pos[0] < GRID_SIZE - 1:
        player_pos[0] += 1

def main():
    """
    Main game loop.
    """
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                else:
                    move_player(event.key)

                    # Check for interactions
                    if player_pos == shop_pos:
                        handle_shop()
                    elif player_pos == encounter_pos:
                        handle_encounter()

        draw_grid()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

