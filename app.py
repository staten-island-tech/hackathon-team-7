import pygame
import random
from pygame.locals import *
import time

# Initialize pygame
pygame.init()

# Set up screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rhythm Game - Osu! Mania-like")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)  # Light gray for borders

# Define constants for game
NOTE_RADIUS = 30  # Bigger radius for the circular notes
NOTE_SPEED = 15  # Constant speed for the notes
BORDER_WIDTH = 5
KEY_WIDTH = 100  # Width for each key column

# Set up fonts
font = pygame.font.SysFont("Arial", 24)

# Function to draw circle-shaped notes
def draw_circle(surface, x, y, radius, color):
    pygame.draw.circle(surface, color, (x, y), radius)

# Function to draw the visual borders for each key (centered on the screen)
def draw_key_borders():
    note_x_positions = [200, 300, 400, 500]  # More centered positions for the 4 keys (Z, X, N, M)
    for x in note_x_positions:
        draw_circle(screen, x, screen_height - NOTE_RADIUS - 5, NOTE_RADIUS, WHITE)  # Draw border as a circle
        pygame.draw.line(screen, GRAY, (x - KEY_WIDTH // 2, 0), (x - KEY_WIDTH // 2, screen_height), 2)  # Left border
        pygame.draw.line(screen, GRAY, (x + KEY_WIDTH // 2, 0), (x + KEY_WIDTH // 2, screen_height), 2)  # Right border

# Note class to represent falling circular notes
class Note:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = NOTE_RADIUS
        self.color = RED
        self.speed = NOTE_SPEED  # Fixed speed
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        draw_circle(surface, self.x, self.y, self.radius, self.color)

# Function to generate notes at random horizontal positions
def create_new_note():
    note_x_positions = [200, 300, 400, 500]  # More centered positions for the 4 keys (Z, X, N, M)
    x = random.choice(note_x_positions)
    y = -50  # Start offscreen
    return Note(x, y)

# Function to check if a key press matches with the note
def check_input(notes, keys_pressed):
    score = 0
    for note in notes[:]:
        if note.y > screen_height - NOTE_RADIUS:
            for key, note_x in keys_pressed.items():
                if pygame.key.get_pressed()[key] and note.x == note_x:  # Matching the center of the circle note
                    score += 1
                    notes.remove(note)
                    break
    return score

# Main game loop
def main():
    clock = pygame.time.Clock()
    notes = []
    score = 0
    keys_pressed = {K_z: 200, K_x: 300, K_n: 400, K_m: 500}  # Z, X, N, M keys mapped to positions
    game_over = False
    last_note_time = time.time()
    
    # Adjust the note generation frequency for more frequent note appearances
    note_interval = 0.15  # Notes will spawn every 0.15 seconds (faster spawn rate)
    
    while not game_over:
        screen.fill(BLACK)

        # Check time to spawn a new note and add it at regular intervals
        current_time = time.time()
        if current_time - last_note_time > note_interval:
            notes.append(create_new_note())  # Add a new note at random positions
            last_note_time = current_time

        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True

        # Move and draw notes
        for note in notes:
            note.move()
            note.draw(screen)

        # Check input
        score += check_input(notes, keys_pressed)

        # Draw the visual circle borders for each key and their dividing lines
        draw_key_borders()

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Remove notes that fall out of the screen
        notes = [note for note in notes if note.y < screen_height]

        pygame.display.flip()
        clock.tick(60)  # 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
