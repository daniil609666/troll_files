import pygame
import random

pygame.init()
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption("RIP PC!")
running = True
random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clock.tick(1000)
            pygame.display.set_caption("YOU CANT CLOSE ME!")
    # Generate new random color and position
    random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Randomize window size
    new_width = random.randint(300, 2800)
    new_height = random.randint(200, 2000)
    
    # Ensure aspect ratio is maintained
    aspect_ratio = screen_width / screen_height
    new_width = int(new_height * aspect_ratio)
    
    # Resize the window
    screen = pygame.display.set_mode((new_width, new_height))
    
    # Fill the entire surface with the new color
    screen.fill(random_color)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
