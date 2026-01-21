"""
Task: 011_flappy-bird-refactored
Prompt: let's try refactoring the main.py in Task 010: I can see there are duplicate codes in class Bird, Pipe, Cloud, Coin. Can you define a base class to include the common methods, and put the duplicate method implementatoin in the base class.

Example Output:
[Pygame window opens]
Bird jumps on SPACE
Pipes move across screen
Score increments on passing pipes
Game Over screen on collision
"""

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_SIZE = 30
PIPE_WIDTH = 50

# Difficulty Levels
DIFFICULTIES = {
    "EASY": {
        "gravity": 0.2,
        "flap_strength": -5.5,
        "pipe_gap": 180,
        "pipe_speed": 2,
        "pipe_frequency": 2000,
        "coin_frequency": 2500
    },
    "MEDIUM": {
        "gravity": 0.25,
        "flap_strength": -6.5,
        "pipe_gap": 150,
        "pipe_speed": 3,
        "pipe_frequency": 1500,
        "coin_frequency": 3000
    },
    "HARD": {
        "gravity": 0.3,
        "flap_strength": -7.5,
        "pipe_gap": 120,
        "pipe_speed": 4,
        "pipe_frequency": 1200,
        "coin_frequency": 4000
    }
}

# Values that get set based on difficulty
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_FREQUENCY = 1500
CLOUD_FREQUENCY = 2000
COIN_FREQUENCY = 3000

# States
STATE_START = "START"
STATE_PLAYING = "PLAYING"
STATE_GAMEOVER = "GAMEOVER"

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vibe Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)

# Sound setup
pygame.mixer.init()
try:
    flap_sound = pygame.mixer.Sound("011_flappy-bird-refactored/assets/flap.wav")
    score_sound = pygame.mixer.Sound("011_flappy-bird-refactored/assets/score.wav")
    crash_sound = pygame.mixer.Sound("011_flappy-bird-refactored/assets/crash.wav")
    select_sound = pygame.mixer.Sound("011_flappy-bird-refactored/assets/select.wav")
    
    # Background Music
    try:
        pygame.mixer.music.load("011_flappy-bird-refactored/assets/music.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1) # Loop indefinitely
    except:
        print("Warning: music.wav not found. Playing without background music.")
except:
    flap_sound = score_sound = crash_sound = select_sound = None
    print("Warning: Sounds not found. Playing without audio.")

# Sprite setup
try:
    bird_img = pygame.image.load("011_flappy-bird-refactored/assets/bird.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (BIRD_SIZE + 10, BIRD_SIZE + 10))
except:
    bird_img = None
    print("Warning: bird.png not found. Using rectangle.")

class GameObject:
    def __init__(self, x, y, width, height, speed=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self):
        pass

    def is_off_screen(self):
        return self.rect.right < 0

class Bird(GameObject):
    def __init__(self):
        super().__init__(50, SCREEN_HEIGHT // 2, BIRD_SIZE, BIRD_SIZE)
        self.velocity = 0
        self.angle = 0

    def jump(self):
        self.velocity = FLAP_STRENGTH
        if flap_sound: flap_sound.play()

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)
        # Calculate rotation based on velocity
        self.angle = -self.velocity * 3 

    def draw(self):
        if bird_img:
            # Rotate and center the image
            rotated_bird = pygame.transform.rotate(bird_img, self.angle)
            new_rect = rotated_bird.get_rect(center=self.rect.center)
            screen.blit(rotated_bird, new_rect)
        else:
            pygame.draw.rect(screen, YELLOW, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

class Pipe(GameObject):
    def __init__(self):
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
        # We still need both rects, but we'll use GameObject for movement and state
        super().__init__(SCREEN_WIDTH, 0, PIPE_WIDTH, self.gap_y, PIPE_SPEED)
        self.top_rect = self.rect
        self.bottom_rect = pygame.Rect(SCREEN_WIDTH, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        self.passed = False

    def update(self):
        super().update()
        self.bottom_rect.x = self.rect.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, BLACK, self.top_rect, 2)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)
        pygame.draw.rect(screen, BLACK, self.bottom_rect, 2)

class Cloud(GameObject):
    def __init__(self):
        width = random.randint(60, 100)
        height = random.randint(30, 50)
        speed = random.uniform(0.5, 1.5)
        super().__init__(SCREEN_WIDTH, random.randint(20, 200), width, height, speed)
        self.width = width
        self.height = height

    def draw(self):
        # Draw a simple bubbly cloud using ellipses
        pygame.draw.ellipse(screen, WHITE, self.rect)
        pygame.draw.ellipse(screen, WHITE, (self.rect.x + 20, self.rect.y - 10, self.width - 20, self.height))
        pygame.draw.ellipse(screen, WHITE, (self.rect.x - 10, self.rect.y + 5, self.width - 20, self.height))

class Coin(GameObject):
    def __init__(self):
        size = 20
        super().__init__(SCREEN_WIDTH, random.randint(100, SCREEN_HEIGHT - 100), size, size, PIPE_SPEED)
        self.size = size

    def draw(self):
        # Shiny iconic coin
        pygame.draw.circle(screen, GOLD, self.rect.center, self.size // 2)
        pygame.draw.circle(screen, YELLOW, self.rect.center, self.size // 2 - 2)
        # Add a "shine" highlight
        pygame.draw.circle(screen, WHITE, (self.rect.centerx - 4, self.rect.centery - 4), 3)

def draw_text(text, color, x, y, center=False):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def main():
    global GRAVITY, FLAP_STRENGTH, PIPE_GAP, PIPE_SPEED, PIPE_FREQUENCY, COIN_FREQUENCY
    
    bird = Bird()
    pipes = []
    clouds = []
    coins = []
    score = 0
    game_state = STATE_START
    difficulty_selected = "MEDIUM"
    
    last_pipe_time = pygame.time.get_ticks()
    last_cloud_time = pygame.time.get_ticks()
    last_coin_time = pygame.time.get_ticks()

    def set_difficulty(level):
        global GRAVITY, FLAP_STRENGTH, PIPE_GAP, PIPE_SPEED, PIPE_FREQUENCY, COIN_FREQUENCY
        config = DIFFICULTIES[level]
        GRAVITY = config["gravity"]
        FLAP_STRENGTH = config["flap_strength"]
        PIPE_GAP = config["pipe_gap"]
        PIPE_SPEED = config["pipe_speed"]
        PIPE_FREQUENCY = config["pipe_frequency"]
        COIN_FREQUENCY = config["coin_frequency"]

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_START:
                    if event.key == pygame.K_1:
                        if select_sound: select_sound.play()
                        set_difficulty("EASY")
                        game_state = STATE_PLAYING
                        last_pipe_time = current_time
                        last_cloud_time = current_time
                        last_coin_time = current_time
                    elif event.key == pygame.K_2:
                        if select_sound: select_sound.play()
                        set_difficulty("MEDIUM")
                        game_state = STATE_PLAYING
                        last_pipe_time = current_time
                        last_cloud_time = current_time
                        last_coin_time = current_time
                    elif event.key == pygame.K_3:
                        if select_sound: select_sound.play()
                        set_difficulty("HARD")
                        game_state = STATE_PLAYING
                        last_pipe_time = current_time
                        last_cloud_time = current_time
                        last_coin_time = current_time
                elif game_state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif game_state == STATE_GAMEOVER:
                    if event.key == pygame.K_SPACE:
                        # Reset for Start Screen
                        bird = Bird()
                        pipes = []
                        clouds = []
                        coins = []
                        score = 0
                        game_state = STATE_START
                        last_pipe_time = current_time # Reset timers for next play
                        last_cloud_time = current_time
                        last_coin_time = current_time

        # Background
        screen.fill(SKY_BLUE)

        # Cloud logic (draw behind everything)
        if current_time - last_cloud_time > CLOUD_FREQUENCY:
            clouds.append(Cloud())
            last_cloud_time = current_time

        for cloud in clouds[:]:
            cloud.update()
            cloud.draw()
            if cloud.is_off_screen():
                clouds.remove(cloud)

        if game_state == STATE_START:
            # Draw Start Screen
            screen.blit(pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA), (0,0)) # Dim overlay
            draw_text("VIBE FLAPPY BIRD", BLACK, SCREEN_WIDTH // 2, 100, True)
            draw_text("Select Difficulty:", BLACK, SCREEN_WIDTH // 2, 200, True)
            draw_text("1: EASY", GREEN, SCREEN_WIDTH // 2, 260, True)
            draw_text("2: MEDIUM", YELLOW, SCREEN_WIDTH // 2, 310, True)
            draw_text("3: HARD", RED, SCREEN_WIDTH // 2, 360, True)
            draw_text("Press 1, 2, or 3 to Start", BLACK, SCREEN_WIDTH // 2, 450, True)

        elif game_state == STATE_PLAYING:
            # Bird logic
            bird.update()
            bird.draw()

            # Pipe spawning
            if current_time - last_pipe_time > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe_time = current_time

            # Coin spawning
            if current_time - last_coin_time > COIN_FREQUENCY:
                coins.append(Coin())
                last_coin_time = current_time

            # Pipe logic
            for pipe in pipes[:]:
                pipe.update()
                pipe.draw()

                # Collision detection
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    if crash_sound: crash_sound.play()
                    game_state = STATE_GAMEOVER

                # Scoring
                if not pipe.passed and pipe.top_rect.right < bird.rect.left:
                    if score_sound: score_sound.play()
                    score += 1
                    pipe.passed = True

                # Cleanup
                if pipe.is_off_screen():
                    pipes.remove(pipe)

            # Coin logic
            for coin in coins[:]:
                coin.update()
                coin.draw()

                # Collection detection
                if bird.rect.colliderect(coin.rect):
                    if score_sound: score_sound.play()
                    score += 1
                    coins.remove(coin)
                elif coin.is_off_screen():
                    coins.remove(coin)

            # Boundary collision
            if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                if crash_sound: crash_sound.play()
                game_state = STATE_GAMEOVER

            # Draw score
            draw_text(f"Score: {score}", BLACK, 10, 10)
        elif game_state == STATE_GAMEOVER:
            # Game Over screen
            draw_text("GAME OVER", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, True)
            draw_text(f"Final Score: {score}", BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, True)
            draw_text("Press SPACE to Return to Menu", BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, True)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
