import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroids')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load ship image and scale it
ship_original_image = pygame.image.load(r'C:\Users\ARU\pygame_project\ship.png')
ship_image = pygame.transform.scale(ship_original_image, (500, 500))  # Adjusted ship size

# Load asteroid image and scale it
asteroid_original_image = pygame.image.load(r'C:\Users\ARU\pygame_project\asteroid.png')
asteroid_image = pygame.transform.scale(asteroid_original_image, (100, 100))

# Load background image and scale it
background_image = pygame.image.load(r'C:\Users\ARU\pygame_project\background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load sounds
thrust_sound = pygame.mixer.Sound(r'C:\Users\ARU\pygame_project\ocean-cruise-liner-ship-32308.mp3')
turn_sound = pygame.mixer.Sound(r'C:\Users\ARU\pygame_project\ocean-cruise-liner-ship-32308.mp3')
#engine_sound = pygame.mixer.Sound(r'C:\Users\ARU\pygame_project\ocean-cruise-liner-ship-32308.mp3')  # Load the engine sound

class Ship:
    def __init__(self):
        self.image = ship_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)  # Center the ship initially
        self.angle = 0
        self.speed = 0
        self.engine_sound_playing = False

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        screen.blit(rotated_image, self.rect)

    def update(self):
        rad = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y -= self.speed * math.sin(rad)

        # Wrap around screen
        if self.rect.x < 0:
            self.rect.x = WIDTH
        elif self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0

    def manage_sound(self, keys):
        if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            if not self.engine_sound_playing:
                engine_sound.play(-1)  # Play the sound in a loop
                self.engine_sound_playing = True
        else:
            if self.engine_sound_playing:
                engine_sound.stop()
                self.engine_sound_playing = False

class Asteroid:
    def __init__(self):
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.randint(4, 6)
        self.angle = random.randint(0, 360)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(rotated_image, self.rect)

    def update(self):
        rad = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(rad)
        self.rect.y -= self.speed * math.sin(rad)

        # Wrap around screen
        if self.rect.x < 0:
            self.rect.x = WIDTH
        elif self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0

class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = background_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ocean(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ocean_width = WIDTH
        ocean_height = HEIGHT - 500  # Adjusted to cover most of the screen height, leaving some space at the bottom

        self.image = pygame.Surface((ocean_width, ocean_height))
        self.image.fill((0, 0, 255))  # Blue color for ocean
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # Center horizontally
        self.rect.bottom = HEIGHT  # Align with the bottom of the screen
        self.alpha = 150  # Transparency value

    def draw(self, screen):
        self.image.set_alpha(self.alpha)  # Set transparency
        screen.blit(self.image, self.rect)

# Create instances
ship = Ship()
background = Background(background_image)
ocean = Ocean()
asteroids = [Asteroid() for _ in range(5)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.angle += 5
        turn_sound.play()
    if keys[pygame.K_RIGHT]:
        ship.angle -= 5
        turn_sound.play()
    if keys[pygame.K_UP]:
        ship.speed += 0.1
        thrust_sound.play()
    if keys[pygame.K_DOWN]:
        ship.speed -= 0.1
        thrust_sound.play()

    # Manage engine sound
    ship.manage_sound(keys)

    # Update game objects
    ship.update()
    for asteroid in asteroids:
        asteroid.update()

    # Draw everything
    screen.fill(BLACK)
    background.draw(screen)  # Draw background first
    ship.draw(screen)
    for asteroid in asteroids:
        asteroid.draw(screen)
    ocean.draw(screen)  # Draw ocean after everything else

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()