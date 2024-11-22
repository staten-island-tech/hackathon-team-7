import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rhythm Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load assets (e.g., note image)
note_image = pygame.Surface((50, 50))  # A placeholder for the note image
note_image.fill(RED)  # Fill it with red color for now

# Music setup (Replace with your own music file)
music = 'assets/music.mp3'

# Set up the clock and FPS
clock = pygame.time.Clock()
fps = 60

# Game variables
notes = []
note_speed = 5
score = 0
note_interval = 1000  # Interval in milliseconds to spawn a note
last_note_time = pygame.time.get_ticks()

# Load music
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely

# Lane positions (x-coordinates for each lane)
lanes = {
    'LEFT': 100,
    'UP': 250,
    'RIGHT': 400,
    'DOWN': 550
}

# Define Note class
class Note:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key

    def update(self):
        self.y += note_speed  # Move the note down
        if self.y > screen_height:  # Remove notes when they reach the bottom
            notes.remove(self)

    def draw(self):
        screen.blit(note_image, (self.x, self.y))

# Display score text
def display_text(text, x, y, font_size=40, color=WHITE):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Check player input
def check_input():
    global score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for note in notes:
                    if note.key == 'LEFT' and screen_height - note.y < 50:
                        score += 1
                        notes.remove(note)
                        break
            elif event.key == pygame.K_UP:
                for note in notes:
                    if note.key == 'UP' and screen_height - note.y < 50:
                        score += 1
                        notes.remove(note)
                        break
            elif event.key == pygame.K_RIGHT:
                for note in notes:
                    if note.key == 'RIGHT' and screen_height - note.y < 50:
                        score += 1
                        notes.remove(note)
                        break
            elif event.key == pygame.K_DOWN:
                for note in notes:
                    if note.key == 'DOWN' and screen_height - note.y < 50:
                        score += 1
                        notes.remove(note)
                        break

# Main game loop
def game_loop():
    global last_note_time, notes

    while True:
        screen.fill(BLACK)  # Clear the screen with a black background

        # Add new notes periodically
        if pygame.time.get_ticks() - last_note_time > note_interval:
            note_lane = random.choice(list(lanes.keys()))  # Randomly pick a lane
            note_x = lanes[note_lane]  # Get the x-coordinate of the chosen lane
            notes.append(Note(note_x, 0, note_lane))  # Add new note to list
            last_note_time = pygame.time.get_ticks()

        # Update and draw notes
        for note in notes:
            note.update()
            note.draw()

        # Check player input
        check_input()

        # Draw the score on the screen
        display_text(f"Score: {score}", 10, 10)

        # Update the screen display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(fps)

# Run the game
if __name__ == "__main__":
    game_loop()
