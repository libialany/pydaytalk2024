# link: https://www.geeksforgeeks.org/pygame-tutorial/
# Simple pygame program

import pygame
import sys 
pygame.init()
WIDTH=800
HEIGHT=600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Text Display Game")
#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font setup
font = pygame.font.Font(None, 48)  # None uses default system font, 48 is size
# codigo
def main():
    clock = pygame.time.Clock()
    text = "Welcome to my Text Game!"
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Add ESC key to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Drawing
        screen.fill(BLACK)  # Clear screen with black background
        screen.blit(text_surface, text_rect)  # Draw text
        pygame.display.flip()  # Update display

        # Cap the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()