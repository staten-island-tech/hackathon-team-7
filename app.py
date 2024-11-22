import pygame
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Define constants for the game
NOTE_RADIUS = 30
NOTE_SPEED = 10
KEY_WIDTH = 100  # Width for each key column
KEY_HEIGHT = 100  # Height for the key border (from bottom of the screen)
NOTE_SPACING = 120  # Horizontal spacing between notes (this ensures the keys don't overlap)

# Set up fonts
font = pygame.font.SysFont("Arial", 24)

# Define positions for the notes corresponding to the keys
NOTE_X_POSITIONS = [200, 320, 440, 560]  # Adjusted for non-overlapping key positions
KEYS = {K_z: 0, K_x: 1, K_n: 2, K_m: 3}  # Map keys to note positions

# Note class to represent falling notes
class Note:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = NOTE_RADIUS
        self.color = RED
        self.speed = NOTE_SPEED
    
    def move(self):
        self.y += self.speed
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

# Function to create new notes at random positions
def create_new_note():
    x = random.choice(NOTE_X_POSITIONS)
    y = -50  # Start offscreen
    return Note(x, y)

# Function to check if a key press hits a note
def check_input(notes, keys_pressed):
    score = 0
    for note in notes[:]:
        if note.y > screen_height - NOTE_RADIUS:  # Note reaches the hit zone (bottom of the screen)
            for key, note_pos in keys_pressed.items():
                if pygame.key.get_pressed()[key] and note.x == NOTE_X_POSITIONS[note_pos]:
                    score += 1
                    notes.remove(note)  # Remove the note after it is hit
                    break  # Stop checking once one note is hit
    return score

# Draw key borders (visual representation of key zones)
def draw_key_borders():
    for idx, x in enumerate(NOTE_X_POSITIONS):
        # Draw the key border area (a rectangle for each key zone)
        pygame.draw.rect(screen, GRAY, (x - KEY_WIDTH // 2, screen_height - KEY_HEIGHT, KEY_WIDTH, KEY_HEIGHT), 2)

        # Draw dividers between each key (vertical lines)
        if idx < len(NOTE_X_POSITIONS) - 1:  # No divider after the last key
            next_x = NOTE_X_POSITIONS[idx + 1] - KEY_WIDTH // 2
            pygame.draw.line(screen, GRAY, (x + KEY_WIDTH // 2, screen_height - KEY_HEIGHT), 
                             (next_x - KEY_WIDTH // 2, screen_height - KEY_HEIGHT), 3)

# Main game loop
def main():
    clock = pygame.time.Clock()
    notes = []
    score = 0
    keys_pressed = {K_z: 0, K_x: 1, K_n: 2, K_m: 3}  # Map keys to note positions
    last_note_time = time.time()
    note_interval = 0.5  # Notes spawn every 0.5 seconds

    game_over = False
    while not game_over:
        screen.fill(BLACK)

        # Check time to spawn a new note
        current_time = time.time()
        if current_time - last_note_time > note_interval:
            notes.append(create_new_note())  # Add new note at random position
            last_note_time = current_time

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True

        # Move and draw notes
        for note in notes:
            note.move()
            note.draw(screen)

        # Check input and update score
        score = check_input(notes, keys_pressed)

        # Draw the visual borders for each key and dividers between them
        draw_key_borders()

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Remove notes that are off-screen
        notes = [note for note in notes if note.y < screen_height]

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
